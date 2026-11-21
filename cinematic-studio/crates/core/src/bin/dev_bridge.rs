//! Development bridge: serves the built UI and the same `rpc::call` the desktop shell uses, over HTTP on
//! 127.0.0.1, so the whole app can be driven in a browser (and by browser tests) on any OS.
//! It is a development tool: it is not part of the installer and it only listens on the loopback address.
use std::io::Read;
use std::path::PathBuf;
use studio_core::{files, jobs, rpc, secrets::MemoryStore, App};

fn main() {
    let arg = |name: &str| std::env::args().skip_while(|a| a != name).nth(1);
    let port = arg("--port").unwrap_or_else(|| "4310".into());
    let config = PathBuf::from(arg("--config").expect("--config <dir> is required"));
    let dist = arg("--dist").map(PathBuf::from);
    let app = App::start(&config, Box::new(MemoryStore::default()), None).expect("start");
    let _worker = jobs::start_worker(app.clone());
    let server = tiny_http::Server::http(format!("127.0.0.1:{port}")).expect("bind");
    eprintln!("dev bridge on http://127.0.0.1:{port} (library: {})", app.lib().root.display());
    let header = |k: &str, v: &str| tiny_http::Header::from_bytes(k.as_bytes(), v.as_bytes()).unwrap();
    for mut req in server.incoming_requests() {
        let url = req.url().to_string();
        let (path, query) = url.split_once('?').map(|(p, q)| (p.to_string(), q.to_string())).unwrap_or((url.clone(), String::new()));
        if req.method() == &tiny_http::Method::Post && path == "/rpc" {
            let mut body = String::new();
            let _ = req.as_reader().take(40_000_000).read_to_string(&mut body);
            let v: serde_json::Value = serde_json::from_str(&body).unwrap_or_default();
            let out = rpc::call(&app, v["cmd"].as_str().unwrap_or(""), &v["args"]);
            let _ = req.respond(tiny_http::Response::from_string(out.to_string()).with_header(header("Content-Type", "application/json")));
        } else if path == "/file" {
            let p = query.split('&').find_map(|kv| kv.strip_prefix("path=")).map(|v| url::form_urlencoded::parse(format!("x={v}").as_bytes()).next().map(|(_, v)| v.to_string()).unwrap_or_default()).unwrap_or_default();
            let range = req.headers().iter().find(|h| h.field.equiv("Range")).map(|h| h.value.as_str().to_string());
            match files::serve(&app, &p, range.as_deref()) {
                Ok(s) => {
                    let mut resp = tiny_http::Response::from_data(s.body).with_status_code(s.status).with_header(header("Content-Type", s.mime)).with_header(header("Accept-Ranges", "bytes"));
                    if let Some((a, b)) = s.range { resp = resp.with_header(header("Content-Range", &format!("bytes {a}-{b}/{}", s.total))); }
                    let _ = req.respond(resp);
                }
                Err(_) => { let _ = req.respond(tiny_http::Response::from_string("forbidden").with_status_code(403)); }
            }
        } else if let Some(d) = &dist {
            let rel = path.trim_start_matches('/');
            let file = studio_core::paths::safe_join(d, if rel.is_empty() { "index.html" } else { rel }).ok().filter(|f| f.is_file()).unwrap_or_else(|| d.join("index.html"));
            match std::fs::read(&file) {
                Ok(bytes) => { let mime = match file.extension().and_then(|e| e.to_str()) { Some("html") => "text/html; charset=utf-8", Some("js") => "text/javascript", Some("css") => "text/css", Some("svg") => "image/svg+xml", Some("ttf") => "font/ttf", Some("png") => "image/png", _ => "application/octet-stream" };
                    let _ = req.respond(tiny_http::Response::from_data(bytes).with_header(header("Content-Type", mime))); }
                Err(_) => { let _ = req.respond(tiny_http::Response::from_string("not found").with_status_code(404)); }
            }
        } else {
            let _ = req.respond(tiny_http::Response::from_string("not found").with_status_code(404));
        }
    }
}
