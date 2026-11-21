//! ComfyUI HTTP + WebSocket client.
//! Endpoints and message types are those of Comfy-Org/ComfyUI server.py and execution.py @ afcb984:
//!   POST /prompt · GET /history/{id} · GET /queue · POST /queue {delete} · POST /interrupt {prompt_id}
//!   GET /view · POST /upload/image · GET /system_stats · GET /object_info/{class} · GET /models/{folder}
//!   WS /ws?clientId= → status, execution_start, execution_cached, executing, progress, executed,
//!                      execution_success, execution_error, execution_interrupted
use super::ModelAdapter;
use crate::db;
use crate::error::{err, AppError, Result};
use crate::App;
use serde_json::{json, Value};
use std::io::{Read, Write};
use std::path::Path;
use std::time::{Duration, Instant};

const MAX_DOWNLOAD: u64 = 4 * 1024 * 1024 * 1024;

pub struct Comfy {
    base: url::Url,
    token: Option<String>,
    agent: ureq::Agent,
    pub client_id: String,
}

#[derive(Debug, Clone)]
pub struct OutputFile {
    pub filename: String,
    pub subfolder: String,
    pub kind: String,
}
#[derive(Debug)]
pub enum Outcome {
    Finished(Vec<OutputFile>),
    Failed(String),
    Canceled,
}

/// Remote servers must use HTTPS. Plain HTTP is accepted only for a ComfyUI on this same computer.
pub fn validate_url(raw: &str) -> Result<url::Url> {
    let u = url::Url::parse(raw.trim()).map_err(|_| AppError::new("bad_url", "enter a full address such as https://host:port"))?;
    let host = u.host_str().unwrap_or("").to_lowercase();
    let local = host == "localhost" || host == "127.0.0.1" || host == "[::1]" || host == "::1";
    match u.scheme() {
        "https" => {}
        "http" if local => {}
        "http" => return err("insecure_url", "a remote ComfyUI must be reached over https; plain http is allowed only for localhost"),
        _ => return err("bad_url", "only http(s) addresses are accepted"),
    }
    if !u.username().is_empty() || u.password().is_some() {
        return err("bad_url", "do not put credentials in the address; use the access token field");
    }
    if u.query().is_some() || u.fragment().is_some() {
        return err("bad_url", "the address must not contain a query string");
    }
    Ok(u)
}

fn map_err(e: ureq::Error) -> AppError {
    match e {
        ureq::Error::Status(401, _) | ureq::Error::Status(403, _) => AppError::new("comfy_auth", "the server refused the access token"),
        ureq::Error::Status(code, resp) => {
            let body = resp.into_string().unwrap_or_default();
            AppError::new("comfy_error", format!("HTTP {code}: {}", body.chars().take(600).collect::<String>()))
        }
        ureq::Error::Transport(t) => AppError::new("comfy_unreachable", t.to_string()),
    }
}

impl Comfy {
    pub fn new(base: &str, token: Option<String>) -> Result<Self> {
        let agent = ureq::AgentBuilder::new().timeout_connect(Duration::from_secs(8)).timeout_read(Duration::from_secs(60)).redirects(0).build();
        Ok(Self { base: validate_url(base)?, token: token.filter(|t| !t.is_empty()), agent, client_id: uuid::Uuid::new_v4().simple().to_string() })
    }
    pub fn from_app(app: &App) -> Result<Self> {
        let base = { db::get_setting(&app.db.lock().unwrap(), "comfy_url") }.filter(|u| !u.trim().is_empty()).ok_or_else(|| AppError::new("comfy_not_configured", "no ComfyUI address is set"))?;
        Self::new(&base, app.secrets.get("comfy_token")?)
    }
    fn url(&self, path: &str) -> String {
        format!("{}{}", self.base.as_str().trim_end_matches('/'), path)
    }
    fn auth(&self, req: ureq::Request) -> ureq::Request {
        match &self.token {
            Some(t) => req.set("Authorization", &format!("Bearer {t}")),
            None => req,
        }
    }
    fn get(&self, path: &str) -> Result<Value> {
        self.auth(self.agent.get(&self.url(path))).call().map_err(map_err)?.into_json().map_err(|e| AppError::new("comfy_error", e.to_string()))
    }
    fn post(&self, path: &str, body: &Value) -> Result<Value> {
        let resp = self.auth(self.agent.post(&self.url(path))).send_json(body.clone()).map_err(map_err)?;
        let text = resp.into_string().unwrap_or_default();
        Ok(serde_json::from_str(&text).unwrap_or(Value::Null))
    }

    /// Device name and VRAM as reported by the server itself.
    pub fn system_stats(&self) -> Result<Value> {
        let s = self.get("/system_stats")?;
        let d = &s["devices"][0];
        Ok(json!({ "comfyui_version": s["system"]["comfyui_version"], "device": d["name"], "vram_total": d["vram_total"], "vram_free": d["vram_free"], "os": s["system"]["os"] }))
    }
    pub fn node_exists(&self, class: &str) -> Result<bool> {
        Ok(self.get(&format!("/object_info/{class}"))?.get(class).is_some())
    }
    pub fn models(&self, folder: &str) -> Result<Vec<String>> {
        Ok(self.get(&format!("/models/{folder}"))?.as_array().map(|a| a.iter().filter_map(|x| x.as_str().map(String::from)).collect()).unwrap_or_default())
    }
    /// Checks that the server has every node class and model file the adapter's workflow needs.
    pub fn preflight(&self, adapter: &dyn ModelAdapter) -> Result<Value> {
        let info = adapter.info();
        let mut missing_nodes = vec![];
        for n in info.required_nodes {
            if !self.node_exists(n)? { missing_nodes.push(*n); }
        }
        let mut cache: std::collections::HashMap<&str, Vec<String>> = Default::default();
        let mut files = vec![];
        for f in info.files {
            if !cache.contains_key(f.folder) { cache.insert(f.folder, self.models(f.folder)?); }
            // ComfyUI lists files with their sub-folder; compare by file name
            let present = cache[f.folder].iter().any(|m| m.replace('\\', "/").rsplit('/').next() == Some(f.name));
            files.push(json!({ "folder": f.folder, "name": f.name, "present": present }));
        }
        let ready = missing_nodes.is_empty() && files.iter().all(|f| f["present"] == true);
        Ok(json!({ "model": info.id, "ready": ready, "missing_nodes": missing_nodes, "files": files }))
    }

    pub fn upload_image(&self, file: &Path) -> Result<String> {
        let bytes = std::fs::read(file)?;
        let boundary = format!("----cinematic{}", uuid::Uuid::new_v4().simple());
        let ext = file.extension().and_then(|e| e.to_str()).unwrap_or("png").to_lowercase();
        let name = format!("cs_{}.{}", uuid::Uuid::new_v4().simple(), if ["png", "jpg", "jpeg", "webp"].contains(&ext.as_str()) { ext } else { "png".into() });
        let mut body: Vec<u8> = Vec::with_capacity(bytes.len() + 512);
        write!(body, "--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\nContent-Type: application/octet-stream\r\n\r\n")?;
        body.extend_from_slice(&bytes);
        write!(body, "\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n")?;
        let resp = self.auth(self.agent.post(&self.url("/upload/image"))).set("Content-Type", &format!("multipart/form-data; boundary={boundary}")).send_bytes(&body).map_err(map_err)?;
        let j: Value = resp.into_json().map_err(|e| AppError::new("comfy_error", e.to_string()))?;
        let stored = j["name"].as_str().ok_or_else(|| AppError::new("comfy_error", "upload returned no file name"))?;
        Ok(match j["subfolder"].as_str().filter(|s| !s.is_empty()) { Some(sub) => format!("{sub}/{stored}"), None => stored.to_string() })
    }

    /// Queues a workflow. The id is accepted only from the server's own answer.
    pub fn submit(&self, workflow: &Value) -> Result<String> {
        let resp = self.auth(self.agent.post(&self.url("/prompt"))).send_json(json!({ "prompt": workflow, "client_id": self.client_id }));
        match resp {
            Ok(r) => {
                let j: Value = r.into_json().map_err(|e| AppError::new("comfy_error", e.to_string()))?;
                if j["node_errors"].as_object().map(|o| !o.is_empty()).unwrap_or(false) {
                    return err("workflow_rejected", j["node_errors"].to_string().chars().take(800).collect::<String>());
                }
                j["prompt_id"].as_str().map(String::from).ok_or_else(|| AppError::new("comfy_error", "the server returned no prompt_id"))
            }
            Err(ureq::Error::Status(400, r)) => {
                let j: Value = r.into_json().unwrap_or(Value::Null);
                let msg = format!("{} {}", j["error"]["message"].as_str().unwrap_or("the server rejected the workflow"), j["node_errors"]);
                err("workflow_rejected", msg.chars().take(900).collect::<String>())
            }
            Err(e) => Err(map_err(e)),
        }
    }
    pub fn history(&self, prompt_id: &str) -> Result<Option<Value>> {
        Ok(self.get(&format!("/history/{prompt_id}"))?.get(prompt_id).cloned())
    }
    /// "running", "pending" or "unknown" (not in the queue: finished, failed or lost).
    pub fn queue_state(&self, prompt_id: &str) -> Result<&'static str> {
        let q = self.get("/queue")?;
        let has = |list: &Value| list.as_array().map(|a| a.iter().any(|item| item[1] == prompt_id)).unwrap_or(false);
        Ok(if has(&q["queue_running"]) { "running" } else if has(&q["queue_pending"]) { "pending" } else { "unknown" })
    }
    pub fn cancel(&self, prompt_id: &str) -> Result<()> {
        self.post("/queue", &json!({ "delete": [prompt_id] }))?;
        self.post("/interrupt", &json!({ "prompt_id": prompt_id }))?;
        Ok(())
    }

    fn outcome_from_history(&self, entry: &Value, output_node: &str) -> Outcome {
        let status = &entry["status"];
        if status["status_str"] == "error" {
            let msg = status["messages"].as_array().and_then(|m| m.iter().find(|x| x[0] == "execution_error").map(|x| format!("{}: {}", x[1]["node_type"].as_str().unwrap_or("node"), x[1]["exception_message"].as_str().unwrap_or("error")))).unwrap_or_else(|| "the workflow failed on the server".into());
            return Outcome::Failed(msg.chars().take(600).collect());
        }
        if status["messages"].as_array().map(|m| m.iter().any(|x| x[0] == "execution_interrupted")).unwrap_or(false) {
            return Outcome::Canceled;
        }
        let mut files = vec![];
        let outputs = &entry["outputs"];
        let nodes: Vec<&Value> = match outputs.get(output_node) { Some(n) => vec![n], None => outputs.as_object().map(|o| o.values().collect()).unwrap_or_default() };
        for n in nodes {
            for key in ["images", "video", "videos", "gifs"] {
                for f in n[key].as_array().cloned().unwrap_or_default() {
                    if let Some(name) = f["filename"].as_str() {
                        files.push(OutputFile { filename: name.to_string(), subfolder: f["subfolder"].as_str().unwrap_or("").to_string(), kind: f["type"].as_str().unwrap_or("output").to_string() });
                    }
                }
            }
        }
        if files.is_empty() { Outcome::Failed("the server finished but returned no video file".into()) } else { Outcome::Finished(files) }
    }

    /// Follows a prompt to its end. Progress comes from the WebSocket; /history is the source of truth for
    /// the result and is also polled, so a dropped socket never strands a job.
    pub fn track(&self, prompt_id: &str, output_node: &str, timeout: Duration, mut on_progress: impl FnMut(Option<f64>, &str), should_cancel: impl Fn() -> bool) -> Result<Outcome> {
        let started = Instant::now();
        let mut socket = self.open_socket().ok();
        let mut last_poll = Instant::now() - Duration::from_secs(10);
        let mut cancel_sent = false;
        let mut unknown_since: Option<Instant> = None;
        loop {
            if started.elapsed() > timeout {
                let _ = self.cancel(prompt_id);
                return Ok(Outcome::Failed(format!("no result after {} minutes", timeout.as_secs() / 60)));
            }
            if should_cancel() && !cancel_sent {
                self.cancel(prompt_id)?;
                cancel_sent = true;
            }
            if last_poll.elapsed() >= Duration::from_secs(3) {
                last_poll = Instant::now();
                if let Some(entry) = self.history(prompt_id)? {
                    return Ok(if cancel_sent { Outcome::Canceled } else { self.outcome_from_history(&entry, output_node) });
                }
                match self.queue_state(prompt_id)? {
                    "unknown" => {
                        // not queued and no history yet: allow a short grace period, then treat as lost or canceled
                        let since = *unknown_since.get_or_insert(Instant::now());
                        if since.elapsed() > Duration::from_secs(20) {
                            return Ok(if cancel_sent { Outcome::Canceled } else { Outcome::Failed("the server no longer knows this job (it may have restarted)".into()) });
                        }
                    }
                    state => { unknown_since = None; if state == "pending" { on_progress(None, "waiting in the server queue"); } }
                }
                if socket.is_none() { socket = self.open_socket().ok(); }
            }
            let Some(ws) = socket.as_mut() else { std::thread::sleep(Duration::from_millis(700)); continue };
            match ws.read() {
                Ok(tungstenite::Message::Text(text)) => {
                    let Ok(m) = serde_json::from_str::<Value>(text.as_ref()) else { continue };
                    let d = &m["data"];
                    if d["prompt_id"].as_str().map(|p| p != prompt_id).unwrap_or(false) { continue; }
                    match m["type"].as_str().unwrap_or("") {
                        "progress" => { if let (Some(v), Some(max)) = (d["value"].as_f64(), d["max"].as_f64()) { if max > 0.0 { on_progress(Some((v / max).clamp(0.0, 1.0)), "sampling"); } } }
                        "executing" => { if let Some(node) = d["node"].as_str() { on_progress(None, &format!("running node {node}")); } }
                        "execution_start" => on_progress(Some(0.0), "started"),
                        "execution_success" | "execution_error" | "execution_interrupted" => { last_poll = Instant::now() - Duration::from_secs(10); }
                        _ => {}
                    }
                }
                Ok(_) => {}
                Err(tungstenite::Error::Io(e)) if matches!(e.kind(), std::io::ErrorKind::WouldBlock | std::io::ErrorKind::TimedOut) => {}
                Err(_) => { socket = None; }
            }
        }
    }

    fn open_socket(&self) -> Result<tungstenite::WebSocket<tungstenite::stream::MaybeTlsStream<std::net::TcpStream>>> {
        use tungstenite::client::IntoClientRequest;
        let mut ws_url = self.base.clone();
        ws_url.set_scheme(if self.base.scheme() == "https" { "wss" } else { "ws" }).ok();
        ws_url.set_path(&format!("{}/ws", self.base.path().trim_end_matches('/')));
        ws_url.set_query(Some(&format!("clientId={}", self.client_id)));
        let mut req = ws_url.as_str().into_client_request().map_err(|e| AppError::new("comfy_unreachable", e.to_string()))?;
        if let Some(t) = &self.token {
            req.headers_mut().insert("Authorization", format!("Bearer {t}").parse().map_err(|_| AppError::new("bad_token", "the access token contains characters that cannot be sent"))?);
        }
        let (ws, _) = tungstenite::connect(req).map_err(|e| AppError::new("comfy_unreachable", e.to_string()))?;
        let t = Some(Duration::from_millis(900));
        match ws.get_ref() {
            tungstenite::stream::MaybeTlsStream::Plain(s) => { let _ = s.set_read_timeout(t); }
            tungstenite::stream::MaybeTlsStream::Rustls(s) => { let _ = s.get_ref().set_read_timeout(t); }
            _ => {}
        }
        Ok(ws)
    }

    /// Downloads one output file from this same server into `dest`. The URL is built here from the configured
    /// address; nothing the server returns is used as a URL or as a local path.
    pub fn download(&self, file: &OutputFile, dest: &Path) -> Result<u64> {
        if !["output", "temp"].contains(&file.kind.as_str()) || file.filename.contains(['/', '\\']) || file.filename.contains("..") || file.subfolder.contains("..") {
            return err("unsafe_output", "the server returned an unexpected file location");
        }
        let mut u = url::Url::parse(&self.url("/view")).map_err(|e| AppError::new("bad_url", e.to_string()))?;
        u.query_pairs_mut().append_pair("filename", &file.filename).append_pair("subfolder", &file.subfolder).append_pair("type", &file.kind);
        let agent = ureq::AgentBuilder::new().timeout_connect(Duration::from_secs(8)).timeout(Duration::from_secs(1800)).redirects(0).build();
        let resp = self.auth(agent.get(u.as_str())).call().map_err(map_err)?;
        let tmp = dest.with_extension("part");
        if let Some(p) = dest.parent() { std::fs::create_dir_all(p)?; }
        let mut out = std::fs::File::create(&tmp)?;
        let mut reader = resp.into_reader().take(MAX_DOWNLOAD + 1);
        let mut buf = vec![0u8; 1 << 16];
        let mut total = 0u64;
        loop {
            let n = reader.read(&mut buf).map_err(|e| AppError::new("download_interrupted", e.to_string()))?;
            if n == 0 { break; }
            total += n as u64;
            if total > MAX_DOWNLOAD { drop(out); let _ = std::fs::remove_file(&tmp); return err("download_too_large", "the file is larger than 4 GB"); }
            out.write_all(&buf[..n])?;
        }
        out.flush()?;
        drop(out);
        if total < 1024 { let _ = std::fs::remove_file(&tmp); return err("download_empty", "the server sent an empty file"); }
        std::fs::rename(&tmp, dest)?;
        Ok(total)
    }
}
