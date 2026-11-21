//! The single entry point the UI talks to. Every command the app supports is listed in this match:
//! this is the allow-list. A name that is not here does nothing.
use crate::args::*;
use crate::comfy::{self, client::Comfy};
use crate::db::{self, rows};
use crate::error::{err, AppError, Result};
use crate::{gpu, jobs, lora, media, projects, secrets, timeline, App};
use serde_json::{json, Value};
use std::path::Path;

/// Settings the UI may change, with their validation.
fn set_setting(app: &App, key: &str, value: &str) -> Result<()> {
    let v = value.trim();
    match key {
        "comfy_url" => { if !v.is_empty() { comfy::client::validate_url(v)?; } }
        "ffmpeg_dir" => { if !v.is_empty() && crate::ffmpeg::locate(Some(v), None).is_none() { return err("ffmpeg_missing", "ffmpeg and ffprobe were not found in that folder"); } }
        "language" => one_of(v, &["ar", "en"], "language")?,
        "gpu_provider" => one_of(v, &["none", "runpod"], "gpu_provider")?,
        "gpu_instance_id" => { if !v.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_') || v.len() > 64 { return err("bad_instance_id", "unexpected characters in the instance id"); } }
        "gpu_budget_sar" | "usd_to_sar" | "gpu_idle_minutes" | "gpu_rate_usd" => {
            let n: f64 = v.parse().map_err(|_| AppError::new("bad_request", "a number is required"))?;
            let (lo, hi) = match key { "gpu_budget_sar" => (0.0, 1_000_000.0), "usd_to_sar" => (0.1, 100.0), "gpu_idle_minutes" => (1.0, 240.0), _ => (0.0, 100.0) };
            if !n.is_finite() || n < lo || n > hi { return err("bad_request", format!("{key} must be between {lo} and {hi}")); }
        }
        "operator_name" => {}
        _ => return err("unknown_setting", key.to_string()),
    }
    let conn = app.db.lock().unwrap();
    db::set_setting(&conn, key, &limit(v, 500))?;
    if key.starts_with("gpu_") || key == "usd_to_sar" { db::audit(&conn, "info", "settings.gpu", &format!("{key} changed to {}", limit(v, 60))); }
    Ok(())
}
const SETTING_KEYS: [&str; 10] = ["comfy_url", "ffmpeg_dir", "language", "gpu_provider", "gpu_instance_id", "gpu_budget_sar", "usd_to_sar", "gpu_idle_minutes", "gpu_rate_usd", "operator_name"];

fn app_status(app: &App) -> Result<Value> {
    let tools = app.tools().ok();
    let conn = app.db.lock().unwrap();
    let settings: serde_json::Map<String, Value> = SETTING_KEYS.iter().map(|k| (k.to_string(), json!(db::get_setting(&conn, k)))).collect();
    Ok(json!({
        "version": env!("CARGO_PKG_VERSION"), "library_root": app.lib().root.to_string_lossy(), "default_library_root": crate::paths::default_library_root().to_string_lossy(),
        "ffmpeg": tools.as_ref().map(|t| json!({ "ffmpeg": t.ffmpeg.to_string_lossy(), "ffprobe": t.ffprobe.to_string_lossy() })),
        "recovered": app.recovered, "recovered_jobs": app.recovered_jobs, "last_project": db::get_setting(&conn, "last_project"),
        "settings": settings, "comfy_token_stored": app.secrets.get("comfy_token")?.is_some(), "gpu_key_stored": app.secrets.get("gpu_api_key")?.is_some(), "secret_backend": app.secrets.backend(),
        "counts": { "projects": conn.query_row("SELECT COUNT(*) FROM projects", [], |r| r.get::<_, i64>(0))?, "media": conn.query_row("SELECT COUNT(*) FROM media", [], |r| r.get::<_, i64>(0))?,
                    "active_jobs": conn.query_row("SELECT COUNT(*) FROM jobs WHERE status IN ('queued','blocked','submitted','running','downloading')", [], |r| r.get::<_, i64>(0))? },
        "budget": gpu::budget(&conn)?, "gpu_provider": gpu::provider_id(&conn),
    }))
}

/// Live check of the ComfyUI server: reachable, authenticated, device/VRAM, and what each model adapter still needs.
fn comfy_status(app: &App) -> Result<Value> {
    let comfy = match Comfy::from_app(app) { Ok(c) => c, Err(e) => return Ok(json!({ "configured": false, "connected": false, "error": { "code": e.code, "message": e.message } })) };
    match comfy.system_stats() {
        Err(e) => Ok(json!({ "configured": true, "connected": false, "error": { "code": e.code, "message": e.message } })),
        Ok(stats) => {
            let mut models = vec![];
            for a in comfy::adapters() {
                models.push(match comfy.preflight(a.as_ref()) { Ok(p) => p, Err(e) => json!({ "model": a.info().id, "ready": false, "error": e.message }) });
            }
            Ok(json!({ "configured": true, "connected": true, "system": stats, "models": models }))
        }
    }
}

fn timeline_get(app: &App, project_id: &str) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let p = db::row(&conn, "SELECT timeline_json FROM projects WHERE id = ?1", &[&project_id])?.ok_or_else(|| AppError::new("project_not_found", project_id.to_string()))?;
    let scenes = rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&project_id])?;
    let stored: Option<Value> = p["timeline_json"].as_str().and_then(|s| serde_json::from_str(s).ok());
    let mut tl = stored.clone().filter(|t: &Value| t["clips"].is_array()).unwrap_or_else(|| timeline::default_timeline(&scenes));
    // keep the stored timeline in step with the storyboard: drop clips of scenes that are gone, append new finished scenes
    let mut clips: Vec<Value> = tl["clips"].as_array().cloned().unwrap_or_default().into_iter().filter(|c| scenes.iter().any(|s| s["id"] == c["scene_id"] && s["status"] == "completed")).collect();
    for s in scenes.iter().filter(|s| s["status"] == "completed") {
        if !clips.iter().any(|c| c["scene_id"] == s["id"]) { clips.push(json!({ "scene_id": s["id"], "trim_in": 0.0, "trim_out": Value::Null, "transition": { "kind": "cut", "duration": 0.0 } })); }
    }
    tl["clips"] = json!(clips);
    Ok(json!({ "timeline": tl, "saved": stored.is_some(), "transitions": timeline::TRANSITIONS, "tracks": timeline::TRACKS }))
}

/// Opens a folder of the library in the system file manager. The program is fixed; only a path inside the library is accepted.
fn reveal(app: &App, path: &str) -> Result<Value> {
    let p = Path::new(path);
    let target = if p.is_file() { p.parent().unwrap_or(p) } else { p };
    if !target.is_dir() || !app.lib().contains(target) { return err("forbidden", "only folders inside the library can be opened"); }
    let program = if cfg!(windows) { "explorer.exe" } else if cfg!(target_os = "macos") { "open" } else { "xdg-open" };
    std::process::Command::new(program).arg(target).spawn().map_err(|e| AppError::new("io", e.to_string()))?;
    Ok(json!({ "ok": true }))
}

pub fn dispatch(app: &App, cmd: &str, a: &Value) -> Result<Value> {
    match cmd {
        // app and settings
        "app_status" => app_status(app),
        "app_shutdown" => { app.shutdown(); Ok(json!({ "ok": true })) }
        "setting_set" => { set_setting(app, str_req(a, "key")?, str_opt(a, "value").unwrap_or(""))?; app_status(app) }
        "library_set" => { app.set_library(Path::new(str_req(a, "path")?))?; app_status(app) }
        "secret_set" => { let n = str_req(a, "name")?; secrets::check_name(n)?; app.secrets.set(n, str_req(a, "value")?)?; let c = app.db.lock().unwrap(); db::audit(&c, "info", "secret.set", n); Ok(json!({ "ok": true })) }
        "secret_delete" => { let n = str_req(a, "name")?; secrets::check_name(n)?; app.secrets.delete(n)?; Ok(json!({ "ok": true })) }
        "audit_log" => { let c = app.db.lock().unwrap(); Ok(json!(rows(&c, "SELECT * FROM audit_log ORDER BY id DESC LIMIT 300", &[])?)) }
        "reveal" => reveal(app, str_req(a, "path")?),
        // projects
        "projects_list" => projects::list(app),
        "project_create" => projects::create(app, a),
        "project_get" => projects::get(app, str_req(a, "id")?),
        "project_update" => projects::update(app, str_req(a, "id")?, &a["patch"]),
        "project_delete" => projects::delete(app, str_req(a, "id")?, bool_opt(a, "purge").unwrap_or(false)),
        "project_duplicate" => projects::duplicate(app, str_req(a, "id")?),
        "project_backup" => projects::backup(app, str_req(a, "id")?),
        "project_export_archive" => projects::export_archive(app, str_req(a, "id")?, str_req(a, "dest")?),
        "project_import_archive" => projects::import_archive(app, str_req(a, "path")?),
        "project_integrity" => projects::integrity(app, str_req(a, "id")?),
        // storyboard
        "storyboard_replace" => projects::storyboard_replace(app, str_req(a, "project_id")?, &a["scenes"]),
        "scene_add" => projects::scene_add(app, str_req(a, "project_id")?, &a["scene"], i64_opt(a, "position")),
        "scene_update" => projects::scene_update(app, str_req(a, "id")?, &a["patch"]),
        "scene_delete" => projects::scene_delete(app, str_req(a, "id")?),
        "scenes_reorder" => projects::scenes_reorder(app, str_req(a, "project_id")?, &a["order"]),
        // media
        "media_import" => media::import(app, a),
        "media_list" => media::list(app, a),
        "media_update" => media::update(app, str_req(a, "id")?, a),
        "media_remove" => media::remove(app, str_req(a, "id")?),
        "media_verify" => media::verify(app),
        // models and ComfyUI
        "models_list" => Ok(json!(comfy::adapters().iter().map(|x| { let i = x.info(); let mut v = serde_json::to_value(&i).unwrap_or(Value::Null); v["max_seconds"] = json!(comfy::max_seconds(&i)); v }).collect::<Vec<_>>())),
        "comfy_status" => comfy_status(app),
        // queue
        "jobs_list" => jobs::list(app, str_opt(a, "project_id")),
        "generate" => jobs::enqueue_generation(app, str_req(a, "project_id")?, a["scene_ids"].as_array().map(|x| x.iter().filter_map(|s| s.as_str().map(String::from)).collect()), bool_opt(a, "all").unwrap_or(false)),
        "export" => jobs::enqueue_export(app, str_req(a, "project_id")?, a.get("options").unwrap_or(&Value::Null)),
        "job_cancel" => jobs::cancel(app, str_req(a, "id")?),
        "job_retry" => jobs::retry(app, str_req(a, "id")?),
        "jobs_clear_finished" => jobs::clear_finished(app),
        "timeline_get" => timeline_get(app, str_req(a, "project_id")?),
        // GPU
        "gpu_status" => gpu::status(app),
        "gpu_start" => gpu::start(app, bool_opt(a, "approved").unwrap_or(false), str_opt(a, "approved_by").unwrap_or("")),
        "gpu_stop" => gpu::stop(app, "stopped by user"),
        // LoRA
        "lora_list" => lora::list(app),
        "lora_import" => lora::import(app, a),
        "lora_update" => lora::update(app, str_req(a, "id")?, a),
        "lora_remove" => lora::remove(app, str_req(a, "id")?),
        "lora_dataset_add" => lora::dataset_add(app, a),
        "lora_dataset_remove" => lora::dataset_remove(app, str_req(a, "id")?),
        "lora_run_plan" => lora::run_plan(app, a),
        "lora_run_update" => lora::run_update(app, str_req(a, "id")?, a),
        _ => err("unknown_command", cmd.to_string()),
    }
}

/// Same as `dispatch`, with the result shaped for transport: { ok, data } or { ok: false, error }.
pub fn call(app: &App, cmd: &str, args: &Value) -> Value {
    match dispatch(app, cmd, args) {
        Ok(data) => json!({ "ok": true, "data": data }),
        Err(e) => {
            let secrets = [app.secrets.get("comfy_token").ok().flatten(), app.secrets.get("gpu_api_key").ok().flatten()];
            json!({ "ok": false, "error": { "code": e.code, "message": secrets::redact(&e.message, &secrets) } })
        }
    }
}
