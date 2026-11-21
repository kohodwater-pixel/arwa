//! Desktop shell. It is deliberately thin: a window, one command (`rpc`) that forwards to the core's
//! allow-list, and one read-only URI scheme (`studio://`) for showing media the core permits.
//! Everything the app does lives in `studio_core` and is tested there.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use studio_core::{files, jobs, secrets, App};
use tauri::http::{Request, Response};
use tauri::{Manager, RunEvent};

struct Core {
    app: Arc<App>,
    ui_seen: AtomicBool,
}

/// The only command exposed to the web view. `cmd` is matched against the core's allow-list.
#[tauri::command]
async fn rpc(state: tauri::State<'_, Core>, cmd: String, args: serde_json::Value) -> Result<serde_json::Value, String> {
    let app = state.app.clone();
    if !state.ui_seen.swap(true, Ordering::SeqCst) {
        // first call from the interface: leave a line in Logs so support (and the installer test) can see the UI reached the core
        let _ = std::fs::write(app.lib().dir("Logs").join("ui-connected.txt"), format!("{} {}\n", studio_core::db::now(), env!("CARGO_PKG_VERSION")));
    }
    tauri::async_runtime::spawn_blocking(move || studio_core::rpc::call(&app, &cmd, &args)).await.map_err(|e| e.to_string())
}

fn query_path(uri: &str) -> Option<String> {
    let q = uri.split_once('?')?.1;
    url::form_urlencoded::parse(q.as_bytes()).find(|(k, _)| k == "path").map(|(_, v)| v.into_owned())
}

fn serve_file(app: &App, request: &Request<Vec<u8>>) -> Response<Vec<u8>> {
    let deny = |code: u16| Response::builder().status(code).body(Vec::new()).unwrap();
    let Some(path) = query_path(&request.uri().to_string()) else { return deny(400) };
    let range = request.headers().get("range").and_then(|v| v.to_str().ok());
    match files::serve(app, &path, range) {
        Ok(s) => {
            let mut r = Response::builder().status(s.status).header("Content-Type", s.mime).header("Accept-Ranges", "bytes").header("Cache-Control", "no-store");
            if let Some((a, b)) = s.range { r = r.header("Content-Range", format!("bytes {a}-{b}/{}", s.total)); }
            r.body(s.body).unwrap_or_else(|_| deny(500))
        }
        Err(_) => deny(403),
    }
}

fn main() {
    let app = tauri::Builder::default()
        // one running copy only: two copies would share the database and confuse crash recovery
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(w) = app.get_webview_window("main") { let _ = w.unminimize(); let _ = w.set_focus(); }
        }))
        .plugin(tauri_plugin_dialog::init())
        .register_asynchronous_uri_scheme_protocol("studio", |ctx, request, responder| {
            let core = ctx.app_handle().state::<Core>().app.clone();
            std::thread::spawn(move || responder.respond(serve_file(&core, &request)));
        })
        .setup(|app| {
            let config_dir = app.path().app_config_dir()?;
            let bundled = app.path().resource_dir().ok().map(|d| d.join("resources").join("ffmpeg"));
            let core = App::start(&config_dir, secrets::default_store(), bundled).map_err(|e| format!("{}: {}", e.code, e.message))?;
            jobs::start_worker(core.clone());
            app.manage(Core { app: core, ui_seen: AtomicBool::new(false) });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![rpc])
        .build(tauri::generate_context!())
        .expect("error while building Cinematic Studio");

    app.run(|handle, event| {
        if let RunEvent::Exit = event {
            // marks the session as cleanly closed; without this line the next start reports a recovery
            if let Some(core) = handle.try_state::<Core>() { core.app.shutdown(); }
        }
    });
}
