//! Test doubles. These imitate the *protocol* of ComfyUI and of the GPU provider so the client code can be
//! exercised end to end without a GPU. They exist only in tests and are never part of the app.
#![allow(dead_code)]
use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::{Arc, Mutex};
use studio_core::secrets::MemoryStore;
use studio_core::App;

pub struct Env {
    pub dir: tempfile::TempDir,
    pub app: Arc<App>,
}
impl Env {
    pub fn new() -> Env {
        let dir = tempfile::tempdir().unwrap();
        let app = start(dir.path());
        Env { dir, app }
    }
    pub fn restart(&mut self, clean: bool) {
        if clean { self.app.shutdown(); }
        self.app = start(self.dir.path());
    }
    pub fn call(&self, cmd: &str, args: Value) -> Value {
        let out = studio_core::rpc::call(&self.app, cmd, &args);
        assert!(out["ok"] == true, "{cmd} failed: {}", out["error"]);
        out["data"].clone()
    }
    pub fn fail(&self, cmd: &str, args: Value) -> String {
        let out = studio_core::rpc::call(&self.app, cmd, &args);
        assert!(out["ok"] == false, "{cmd} should have failed but returned {}", out["data"]);
        out["error"]["code"].as_str().unwrap().to_string()
    }
    pub fn file(&self, name: &str) -> PathBuf { self.dir.path().join(name) }
    pub fn set(&self, key: &str, value: &str) { studio_core::db::set_setting(&self.app.db.lock().unwrap(), key, value).unwrap(); }
}
fn start(dir: &Path) -> Arc<App> {
    std::fs::create_dir_all(dir.join("config")).unwrap();
    std::fs::write(dir.join("config/config.json"), json!({ "library_root": dir.join("Library").to_string_lossy() }).to_string()).unwrap();
    App::start(&dir.join("config"), Box::new(MemoryStore::default()), None).unwrap()
}

pub fn ffmpeg(args: &[&str]) {
    let out = Command::new("ffmpeg").args(["-y", "-v", "error"]).args(args).output().expect("ffmpeg must be installed to run the tests");
    assert!(out.status.success(), "ffmpeg failed: {}", String::from_utf8_lossy(&out.stderr));
}
pub fn make_video(path: &Path, seconds: f64, size: &str, with_audio: bool) {
    let v = format!("testsrc2=s={size}:r=24:d={seconds}");
    let a = format!("sine=frequency=440:duration={seconds}");
    let p = path.to_string_lossy().to_string();
    if with_audio { ffmpeg(&["-f", "lavfi", "-i", &v, "-f", "lavfi", "-i", &a, "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", &p]); } else { ffmpeg(&["-f", "lavfi", "-i", &v, "-pix_fmt", "yuv420p", &p]); }
}
pub fn make_image(path: &Path) { ffmpeg(&["-f", "lavfi", "-i", "testsrc2=s=640x360", "-frames:v", "1", &path.to_string_lossy()]); }
pub fn make_audio(path: &Path, seconds: f64) { ffmpeg(&["-f", "lavfi", "-i", &format!("sine=frequency=330:duration={seconds}"), &path.to_string_lossy()]); }

// ── tiny HTTP + WebSocket server ─────────────────────────────────────────────
pub struct Req { pub method: String, pub path: String, pub query: String, pub headers: HashMap<String, String>, pub body: Vec<u8> }
pub struct Resp { pub status: u16, pub content_type: &'static str, pub body: Vec<u8> }
pub fn json_resp(status: u16, v: Value) -> Resp { Resp { status, content_type: "application/json", body: v.to_string().into_bytes() } }

fn read_request(stream: &mut TcpStream) -> Option<Req> {
    let mut buf = Vec::new();
    let mut tmp = [0u8; 4096];
    let header_end = loop {
        let n = stream.read(&mut tmp).ok()?;
        if n == 0 { return None; }
        buf.extend_from_slice(&tmp[..n]);
        if let Some(pos) = buf.windows(4).position(|w| w == b"\r\n\r\n") { break pos + 4; }
    };
    let head = String::from_utf8_lossy(&buf[..header_end]).to_string();
    let mut lines = head.lines();
    let mut first = lines.next()?.split_whitespace();
    let (method, target) = (first.next()?.to_string(), first.next()?.to_string());
    let headers: HashMap<String, String> = lines.filter_map(|l| l.split_once(':').map(|(k, v)| (k.trim().to_lowercase(), v.trim().to_string()))).collect();
    let len: usize = headers.get("content-length").and_then(|v| v.parse().ok()).unwrap_or(0);
    let mut body = buf[header_end..].to_vec();
    while body.len() < len { let n = stream.read(&mut tmp).ok()?; if n == 0 { break; } body.extend_from_slice(&tmp[..n]); }
    let (path, query) = target.split_once('?').map(|(p, q)| (p.to_string(), q.to_string())).unwrap_or((target, String::new()));
    Some(Req { method, path, query, headers, body })
}

/// Starts a server on a free loopback port. `http` answers ordinary requests; `ws` is called with each
/// accepted WebSocket (path /ws) and may push messages.
pub fn serve(http: impl Fn(&Req) -> Resp + Send + Sync + 'static, ws: impl Fn(&mut tungstenite::WebSocket<TcpStream>) + Send + Sync + 'static) -> String {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = listener.local_addr().unwrap();
    let (http, ws) = (Arc::new(http), Arc::new(ws));
    std::thread::spawn(move || {
        for stream in listener.incoming().flatten() {
            let (http, ws) = (http.clone(), ws.clone());
            std::thread::spawn(move || {
                let mut stream = stream;
                let mut peek = [0u8; 8];
                let n = stream.peek(&mut peek).unwrap_or(0);
                if &peek[..n.min(7)] == b"GET /ws" {
                    if let Ok(mut socket) = tungstenite::accept(stream) { ws(&mut socket); let _ = socket.close(None); }
                    return;
                }
                let Some(req) = read_request(&mut stream) else { return };
                let r = http(&req);
                let _ = write!(stream, "HTTP/1.1 {} X\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n", r.status, r.content_type, r.body.len());
                let _ = stream.write_all(&r.body);
            });
        }
    });
    format!("http://127.0.0.1:{}", addr.port())
}

// ── fake ComfyUI ─────────────────────────────────────────────────────────────
#[derive(Default)]
pub struct ComfyState {
    pub token: Option<String>,
    pub missing_files: Vec<String>,
    pub missing_nodes: Vec<String>,
    pub fail_generation: bool,
    pub polls_until_done: u32,
    pub serve_broken_video: bool,
    pub prompts: Vec<(String, Value)>,
    pub polls: HashMap<String, u32>,
    pub canceled: Vec<String>,
    pub uploads: u32,
    pub ws_connections: u32,
    pub unauthorized: u32,
}
pub fn fake_comfy(video: PathBuf) -> (String, Arc<Mutex<ComfyState>>) {
    let state = Arc::new(Mutex::new(ComfyState { polls_until_done: 2, ..Default::default() }));
    let (s1, s2) = (state.clone(), state.clone());
    let url = serve(move |req| {
        let mut st = s1.lock().unwrap();
        if let Some(t) = &st.token { if req.headers.get("authorization") != Some(&format!("Bearer {t}")) { st.unauthorized += 1; return json_resp(401, json!({ "error": "unauthorized" })); } }
        let known = ["wan2.2_ti2v_5B_fp16.safetensors", "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "wan2.2_vae.safetensors", "style-1.0.0.safetensors"];
        match (req.method.as_str(), req.path.as_str()) {
            ("GET", "/system_stats") => json_resp(200, json!({ "system": { "comfyui_version": "test", "os": "posix" }, "devices": [{ "name": "cuda:0 TEST GPU", "vram_total": 51_000_000_000u64, "vram_free": 48_000_000_000u64 }] })),
            ("GET", p) if p.starts_with("/object_info/") => { let class = &p[13..]; if st.missing_nodes.iter().any(|n| n == class) { json_resp(200, json!({})) } else { json_resp(200, json!({ class: { "input": {} } })) } }
            ("GET", p) if p.starts_with("/models/") => json_resp(200, json!(known.iter().filter(|k| !st.missing_files.iter().any(|m| m == *k)).collect::<Vec<_>>())),
            ("POST", "/upload/image") => { st.uploads += 1; json_resp(200, json!({ "name": "ref.png", "subfolder": "", "type": "input" })) }
            ("POST", "/prompt") => {
                let body: Value = serde_json::from_slice(&req.body).unwrap_or_default();
                if !body["prompt"].is_object() || body["client_id"].as_str().is_none() { return json_resp(400, json!({ "error": { "type": "invalid_prompt", "message": "bad body" }, "node_errors": {} })); }
                let id = uuid::Uuid::new_v4().to_string();
                st.prompts.push((id.clone(), body["prompt"].clone()));
                json_resp(200, json!({ "prompt_id": id, "number": 1, "node_errors": {} }))
            }
            ("GET", "/queue") => { let running: Vec<Value> = st.prompts.iter().filter(|(id, _)| st.polls.get(id).copied().unwrap_or(0) < st.polls_until_done && !st.canceled.contains(id)).map(|(id, _)| json!([0, id])).collect(); json_resp(200, json!({ "queue_running": running, "queue_pending": [] })) }
            ("GET", p) if p.starts_with("/history/") => {
                let id = p[9..].to_string();
                if st.canceled.contains(&id) { return json_resp(200, json!({ id: { "status": { "status_str": "error", "completed": false, "messages": [["execution_interrupted", {}]] }, "outputs": {} } })); }
                let n = { let e = st.polls.entry(id.clone()).or_insert(0); *e += 1; *e };
                if n < st.polls_until_done { return json_resp(200, json!({})); }
                if st.fail_generation { return json_resp(200, json!({ id: { "status": { "status_str": "error", "completed": false, "messages": [["execution_error", { "node_type": "KSampler", "exception_message": "CUDA out of memory" }]] }, "outputs": {} } })); }
                json_resp(200, json!({ id: { "status": { "status_str": "success", "completed": true, "messages": [] }, "outputs": { "save": { "images": [{ "filename": "cs_00001_.mp4", "subfolder": "cinematic-studio", "type": "output" }], "animated": [true] } } } }))
            }
            ("GET", "/view") => { if st.serve_broken_video { Resp { status: 200, content_type: "video/mp4", body: vec![7u8; 5000] } } else { Resp { status: 200, content_type: "video/mp4", body: std::fs::read(&video).unwrap() } } }
            ("POST", "/interrupt") | ("POST", "/queue") => { let body: Value = serde_json::from_slice(&req.body).unwrap_or_default(); for id in body["delete"].as_array().cloned().unwrap_or_default().iter().chain(body.get("prompt_id")) { if let Some(s) = id.as_str() { if !st.canceled.contains(&s.to_string()) { st.canceled.push(s.to_string()); } } } json_resp(200, json!({})) }
            _ => json_resp(404, json!({ "error": "not found" })),
        }
    }, move |socket| {
        let id = { let mut st = s2.lock().unwrap(); st.ws_connections += 1; st.prompts.last().map(|p| p.0.clone()).unwrap_or_default() };
        let _ = socket.send(tungstenite::Message::Text(json!({ "type": "execution_start", "data": { "prompt_id": id } }).to_string().into()));
        for k in 1..=4 { let _ = socket.send(tungstenite::Message::Text(json!({ "type": "progress", "data": { "value": k, "max": 4, "prompt_id": id, "node": "sample" } }).to_string().into())); std::thread::sleep(std::time::Duration::from_millis(120)); }
        std::thread::sleep(std::time::Duration::from_secs(3));
    });
    (url, state)
}

// ── fake GPU provider (RunPod v2 shapes) ─────────────────────────────────────
#[derive(Default)]
pub struct GpuFake { pub running: bool, pub starts: u32, pub stops: u32, pub bad_key: bool }
pub fn fake_gpu() -> (String, Arc<Mutex<GpuFake>>) {
    let state = Arc::new(Mutex::new(GpuFake::default()));
    let s = state.clone();
    let url = serve(move |req| {
        let mut st = s.lock().unwrap();
        if st.bad_key || req.headers.get("authorization").map(|a| a.as_str()) != Some("Bearer test-gpu-key") { return json_resp(401, json!({ "error": "unauthorized" })); }
        match (req.method.as_str(), req.path.as_str()) {
            ("GET", "/v2/pods/pod123") => json_resp(200, json!({ "id": "pod123", "name": "studio-a6000", "status": if st.running { "RUNNING" } else { "EXITED" }, "cost": 0.5, "startedAt": if st.running { json!(chrono::Utc::now().to_rfc3339()) } else { Value::Null }, "gpu": { "displayName": "RTX A6000" } })),
            ("POST", "/v2/pods/pod123/action") => { let b: Value = serde_json::from_slice(&req.body).unwrap_or_default(); match b["action"].as_str() { Some("start") => { st.running = true; st.starts += 1; } Some("stop") => { st.running = false; st.stops += 1; } _ => return json_resp(422, json!({ "error": "bad action" })) } json_resp(200, json!({})) }
            _ => json_resp(404, json!({ "error": "not found" })),
        }
    }, |_| {});
    (url, state)
}
