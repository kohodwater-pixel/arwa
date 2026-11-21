//! Render queue: generation jobs (ComfyUI) and export jobs (FFmpeg) run one at a time on a background thread.
//! The database is the queue, so jobs survive a restart; a generation that was already submitted re-attaches
//! to the server by its remote id instead of being submitted (and paid for) twice.
use crate::comfy::{self, client::{Comfy, Outcome}, GenerationRequest};
use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::{gpu, App};
use rusqlite::params;
use serde_json::{json, Value};
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::time::Duration;

const ACTIVE: &str = "('queued','blocked','submitted','running','downloading')";
const GENERATION_TIMEOUT: Duration = Duration::from_secs(45 * 60);
const MAX_ATTEMPTS: i64 = 2;

pub fn list(app: &App, project_id: Option<&str>) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let sql = format!("SELECT j.*, p.name AS project_name, s.title AS scene_title, s.position AS scene_position FROM jobs j
        LEFT JOIN projects p ON p.id = j.project_id LEFT JOIN scenes s ON s.id = j.scene_id {} ORDER BY j.created_at DESC LIMIT 300", if project_id.is_some() { "WHERE j.project_id = ?1" } else { "" });
    Ok(json!(match project_id { Some(p) => rows(&conn, &sql, &[&p])?, None => rows(&conn, &sql, &[])? }))
}

/// Queues generation for the given scenes (or every scene that has no finished clip, or all when `all`).
pub fn enqueue_generation(app: &App, project_id: &str, scene_ids: Option<Vec<String>>, all: bool) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    gpu::assert_can_accept_jobs(&conn)?;
    let project = row(&conn, "SELECT * FROM projects WHERE id = ?1", &[&project_id])?.ok_or_else(|| AppError::new("project_not_found", project_id.to_string()))?;
    let model_id = project["model_id"].as_str().unwrap_or("");
    let adapter = comfy::adapter(model_id).ok_or_else(|| AppError::new("unknown_model", model_id.to_string()))?;
    let info = adapter.info();
    let aspect = project["aspect"].as_str().unwrap_or("");
    if !info.sizes.iter().any(|(a, _, _)| *a == aspect) {
        return err("aspect_not_supported", format!("{} does not generate {aspect}", info.label));
    }
    let scenes = rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&project_id])?;
    let mut queued = 0;
    for s in &scenes {
        let sid = s["id"].as_str().unwrap_or("");
        let wanted = match &scene_ids { Some(ids) => ids.iter().any(|i| i == sid), None => all || s["status"] != "completed" };
        if !wanted { continue; }
        let busy: i64 = conn.query_row(&format!("SELECT COUNT(*) FROM jobs WHERE scene_id = ?1 AND status IN {ACTIVE}"), [sid], |r| r.get(0))?;
        if busy > 0 { continue; }
        if s["prompt"].as_str().unwrap_or("").trim().is_empty() { return err("empty_prompt", format!("scene {} has no prompt", s["position"].as_i64().unwrap_or(0) + 1)); }
        if s["duration"].as_f64().unwrap_or(0.0) > comfy::max_seconds(&info) + 0.01 {
            return err("scene_too_long", format!("scene {} is longer than the {:.0} s this model generates in one clip", s["position"].as_i64().unwrap_or(0) + 1, comfy::max_seconds(&info)));
        }
        if !info.tasks.contains(&"t2v") && s["reference_media_id"].is_null() {
            return err("reference_required", format!("scene {} needs a visual reference: {} is image-to-video only", s["position"].as_i64().unwrap_or(0) + 1, info.label));
        }
        conn.execute("INSERT INTO jobs (id, project_id, scene_id, kind, provider, model_id, status, created_at) VALUES (?1,?2,?3,'generate','comfyui',?4,'queued',?5)", params![new_id(), project_id, sid, model_id, now()])?;
        conn.execute("UPDATE scenes SET status = 'queued', error = NULL WHERE id = ?1", [sid])?;
        queued += 1;
    }
    if queued > 0 { conn.execute("UPDATE projects SET status = 'generating', updated_at = ?1 WHERE id = ?2", params![now(), project_id])?; }
    Ok(json!({ "queued": queued }))
}

pub fn enqueue_export(app: &App, project_id: &str, options: &Value) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    row(&conn, "SELECT id FROM projects WHERE id = ?1", &[&project_id])?.ok_or_else(|| AppError::new("project_not_found", project_id.to_string()))?;
    let busy: i64 = conn.query_row(&format!("SELECT COUNT(*) FROM jobs WHERE project_id = ?1 AND kind = 'export' AND status IN {ACTIVE}"), [project_id], |r| r.get(0))?;
    if busy > 0 { return err("export_running", "an export of this project is already in the queue"); }
    let id = new_id();
    conn.execute("INSERT INTO jobs (id, project_id, kind, provider, status, request_json, created_at) VALUES (?1,?2,'export','ffmpeg','queued',?3,?4)", params![id, project_id, options.to_string(), now()])?;
    Ok(json!({ "job_id": id }))
}

fn restore_scene(conn: &rusqlite::Connection, scene_id: Option<&str>, error: Option<&str>) {
    if let Some(sid) = scene_id {
        let _ = conn.execute("UPDATE scenes SET status = CASE WHEN ?2 IS NOT NULL THEN 'failed' WHEN video_path IS NOT NULL THEN 'completed' ELSE 'pending' END, error = ?2 WHERE id = ?1", params![sid, error]);
    }
}
fn refresh_project(conn: &rusqlite::Connection, project_id: &str) {
    let active: i64 = conn.query_row(&format!("SELECT COUNT(*) FROM jobs WHERE project_id = ?1 AND kind = 'generate' AND status IN {ACTIVE}"), [project_id], |r| r.get(0)).unwrap_or(0);
    if active == 0 {
        let pending: i64 = conn.query_row("SELECT COUNT(*) FROM scenes WHERE project_id = ?1 AND status != 'completed'", [project_id], |r| r.get(0)).unwrap_or(1);
        let _ = conn.execute("UPDATE projects SET status = ?1, updated_at = ?2 WHERE id = ?3 AND status = 'generating'", params![if pending == 0 { "ready" } else { "storyboard" }, now(), project_id]);
    }
}

pub fn cancel(app: &App, job_id: &str) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let job = row(&conn, "SELECT * FROM jobs WHERE id = ?1", &[&job_id])?.ok_or_else(|| AppError::new("job_not_found", job_id.to_string()))?;
    let status = job["status"].as_str().unwrap_or("");
    if !["queued", "blocked", "submitted", "running", "downloading"].contains(&status) { return err("job_not_active", "this job is not running"); }
    // For a job already on the server the worker sees this status and tells the server to stop.
    conn.execute("UPDATE jobs SET status = 'canceled', finished_at = ?1, stage = 'canceled by user' WHERE id = ?2", params![now(), job_id])?;
    restore_scene(&conn, job["scene_id"].as_str(), None);
    refresh_project(&conn, job["project_id"].as_str().unwrap_or(""));
    Ok(json!({ "ok": true }))
}

pub fn retry(app: &App, job_id: &str) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let job = row(&conn, "SELECT * FROM jobs WHERE id = ?1", &[&job_id])?.ok_or_else(|| AppError::new("job_not_found", job_id.to_string()))?;
    if !["failed", "canceled"].contains(&job["status"].as_str().unwrap_or("")) { return err("job_not_retryable", "only failed or canceled jobs can be retried"); }
    if job["kind"] == "generate" { gpu::assert_can_accept_jobs(&conn)?; }
    conn.execute("UPDATE jobs SET status = 'queued', remote_id = NULL, error = NULL, blocked_reason = NULL, progress = NULL, stage = 'retry', attempts = 0, finished_at = NULL WHERE id = ?1", [job_id])?;
    if let Some(sid) = job["scene_id"].as_str() { conn.execute("UPDATE scenes SET status = 'queued', error = NULL WHERE id = ?1", [sid])?; }
    if job["kind"] == "generate" { conn.execute("UPDATE projects SET status = 'generating' WHERE id = ?1", [job["project_id"].as_str()])?; }
    Ok(json!({ "ok": true }))
}

pub fn clear_finished(app: &App) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let n = conn.execute("DELETE FROM jobs WHERE status IN ('succeeded','failed','canceled')", [])?;
    Ok(json!({ "removed": n }))
}

// ── worker ───────────────────────────────────────────────────────────────────
fn set(app: &App, job_id: &str, sql_set: &str, p: &[&dyn rusqlite::ToSql]) {
    let conn = app.db.lock().unwrap();
    let mut all: Vec<&dyn rusqlite::ToSql> = p.to_vec();
    all.push(&job_id);
    let _ = conn.execute(&format!("UPDATE jobs SET {sql_set} WHERE id = ?{}", all.len()), all.as_slice());
}
fn is_canceled(app: &App, job_id: &str) -> bool {
    let conn = app.db.lock().unwrap();
    conn.query_row("SELECT status FROM jobs WHERE id = ?1", [job_id], |r| r.get::<_, String>(0)).map(|s| s == "canceled").unwrap_or(true)
}
fn block(app: &App, job_id: &str, reason: &str) {
    set(app, job_id, "status = 'blocked', blocked_reason = ?1, stage = ?1", &[&reason]);
}
fn fail(app: &App, job: &Value, e: &AppError) {
    let msg = format!("{}: {}", e.code, e.message);
    let conn = app.db.lock().unwrap();
    let _ = conn.execute("UPDATE jobs SET status = 'failed', error = ?1, finished_at = ?2 WHERE id = ?3 AND status != 'canceled'", params![msg, now(), job["id"].as_str()]);
    restore_scene(&conn, job["scene_id"].as_str(), Some(&msg));
    refresh_project(&conn, job["project_id"].as_str().unwrap_or(""));
    db::audit(&conn, "error", "job.failed", &msg);
}

/// Conditions that are nobody's error and may clear by themselves: the job waits as "blocked".
const WAITING: [&str; 4] = ["comfy_not_configured", "comfy_unreachable", "gpu_stopped", "budget_exceeded"];

fn generate(app: &App, job: &Value) -> Result<()> {
    let job_id = job["id"].as_str().unwrap_or("");
    let (project, scene, reference, loras, gpu_provider) = {
        let conn = app.db.lock().unwrap();
        let project = row(&conn, "SELECT * FROM projects WHERE id = ?1", &[&job["project_id"].as_str()])?.ok_or_else(|| AppError::new("project_not_found", ""))?;
        let scene = row(&conn, "SELECT * FROM scenes WHERE id = ?1", &[&job["scene_id"].as_str()])?.ok_or_else(|| AppError::new("scene_not_found", "the scene was deleted"))?;
        let reference = match scene["reference_media_id"].as_str() { Some(m) => row(&conn, "SELECT * FROM media WHERE id = ?1 AND kind = 'image'", &[&m])?, None => None };
        gpu::assert_can_accept_jobs(&conn)?;
        let adapter = comfy::adapter(job["model_id"].as_str().unwrap_or("")).ok_or_else(|| AppError::new("unknown_model", ""))?;
        let loras = rows(&conn, "SELECT * FROM loras WHERE enabled = 1 AND family = ?1", &[&adapter.info().lora_family])?;
        (project, scene, reference, loras, gpu::provider_id(&conn))
    };
    let adapter = comfy::adapter(job["model_id"].as_str().unwrap_or("")).unwrap();
    let info = adapter.info();
    if gpu_provider == "runpod" {
        let st = gpu::sync(app).map_err(|e| AppError::new("gpu_stopped", format!("GPU status could not be read: {}", e.message)))?;
        if st.state != gpu::GpuState::Running { return err("gpu_stopped", "the cloud GPU is not running; start it from the GPU Manager (approval required)"); }
    }
    let comfy = Comfy::from_app(app)?;

    let mut remote = job["remote_id"].as_str().map(String::from);
    if remote.is_none() {
        let pre = comfy.preflight(adapter.as_ref())?;
        if pre["ready"] != true { return err("model_not_ready", format!("the ComfyUI server is missing nodes or model files: {}", pre)); }
        let mut lora_list = vec![];
        if !loras.is_empty() {
            let on_server = comfy.models("loras")?;
            for l in &loras {
                let file = std::path::Path::new(l["file_path"].as_str().unwrap_or("")).file_name().map(|f| f.to_string_lossy().to_string()).unwrap_or_default();
                let found = on_server.iter().find(|m| m.replace('\\', "/").rsplit('/').next() == Some(file.as_str()));
                match found { Some(m) => lora_list.push((m.clone(), l["strength"].as_f64().unwrap_or(1.0))), None => return err("lora_not_on_server", format!("LoRA file {file} is enabled here but is not in the server's loras folder")) }
            }
        }
        let start_image = match &reference {
            Some(m) => { let p = std::path::Path::new(m["path"].as_str().unwrap_or("")); if !p.is_file() { return err("reference_missing", "the scene's reference image is no longer on disk"); } Some(comfy.upload_image(p)?) }
            None => None,
        };
        let mut prompt = scene["prompt"].as_str().unwrap_or("").to_string();
        for l in &loras { if let Some(t) = l["trigger"].as_str().filter(|t| !t.trim().is_empty()) { if !prompt.contains(t) { prompt = format!("{t}, {prompt}"); } } }
        let seed = scene["seed"].as_u64().unwrap_or_else(|| (uuid::Uuid::new_v4().as_u128() & 0xFFFF_FFFF_FFFF) as u64);
        let req = GenerationRequest { prompt, negative_prompt: scene["negative_prompt"].as_str().unwrap_or("").to_string(), aspect: project["aspect"].as_str().unwrap_or("16:9").to_string(),
            seconds: scene["duration"].as_f64().unwrap_or(5.0), seed, start_image, loras: lora_list, filename_prefix: format!("cinematic-studio/{}", &job_id[..8]) };
        let workflow = adapter.workflow(&req)?;
        if is_canceled(app, job_id) { return Ok(()); }
        let id = comfy.submit(&workflow)?;      // from here on the server is working (and the GPU is billing)
        set(app, job_id, "status = 'submitted', remote_id = ?1, started_at = ?2, stage = 'submitted', request_json = ?3", &[&id, &now(), &json!({ "seed": seed, "frames": comfy::frames_for(&info, req.seconds), "fps": info.fps, "model": info.id }).to_string()]);
        { let conn = app.db.lock().unwrap(); let _ = conn.execute("UPDATE scenes SET status = 'generating', seed = COALESCE(seed, ?1) WHERE id = ?2", params![seed as i64, scene["id"].as_str()]); gpu::touch_activity(&conn); }
        remote = Some(id);
    }
    let remote = remote.unwrap();
    set(app, job_id, "status = 'running'", &[]);
    let outcome = comfy.track(&remote, adapter.output_node(), GENERATION_TIMEOUT,
        |p, stage| { match p { Some(v) => set(app, job_id, "progress = ?1, stage = ?2", &[&v, &stage]), None => set(app, job_id, "stage = ?1", &[&stage]) } },
        || is_canceled(app, job_id) || app.shutting_down.load(Ordering::SeqCst))?;
    { let conn = app.db.lock().unwrap(); gpu::touch_activity(&conn); }
    let files = match outcome {
        Outcome::Canceled => { let conn = app.db.lock().unwrap(); restore_scene(&conn, scene["id"].as_str(), None); refresh_project(&conn, project["id"].as_str().unwrap_or("")); return Ok(()); }
        Outcome::Failed(msg) => return err("generation_failed", msg),
        Outcome::Finished(f) => f,
    };
    // The job is done only when the file is on this computer and FFmpeg can decode all of it.
    set(app, job_id, "status = 'downloading', stage = 'downloading', progress = 1.0", &[]);
    let lib = app.lib();
    let folder = project["folder"].as_str().unwrap_or("");
    let rel = format!("{folder}/scenes/scene-{:02}-{}.mp4", scene["position"].as_i64().unwrap_or(0) + 1, &job_id[..8]);
    let dest = lib.resolve(&rel)?;
    let video = files.iter().find(|f| f.filename.to_lowercase().ends_with(".mp4")).unwrap_or(&files[0]);
    comfy.download(video, &dest)?;
    let tools = app.tools()?;
    let media = crate::ffmpeg::verify_playable(&tools, &dest).map_err(|e| { let _ = std::fs::remove_file(&dest); AppError::new("invalid_output", format!("the downloaded file does not play: {}", e.message)) })?;
    let preview_rel = format!("{folder}/scenes/scene-{:02}-{}.jpg", scene["position"].as_i64().unwrap_or(0) + 1, &job_id[..8]);
    let preview = crate::ffmpeg::thumbnail(&tools, &dest, &lib.resolve(&preview_rel)?, media.duration.unwrap_or(1.0) / 2.0).is_ok();
    let conn = app.db.lock().unwrap();
    // keep the previous take aside instead of deleting it
    for key in ["video_path", "preview_path"] {
        if let Some(old) = scene[key].as_str().and_then(|p| lib.resolve(p).ok()).filter(|p| p.is_file() && *p != dest) {
            let aside = dest.parent().unwrap().join("_replaced");
            let _ = std::fs::create_dir_all(&aside);
            let _ = std::fs::rename(&old, aside.join(old.file_name().unwrap_or_default()));
        }
    }
    conn.execute("UPDATE scenes SET status = 'completed', video_path = ?1, preview_path = ?2, video_duration = ?3, error = NULL, updated_at = ?4 WHERE id = ?5", params![rel, if preview { Some(preview_rel) } else { None }, media.duration, now(), scene["id"].as_str()])?;
    conn.execute("UPDATE jobs SET status = 'succeeded', result_path = ?1, finished_at = ?2, stage = 'done' WHERE id = ?3", params![rel, now(), job_id])?;
    refresh_project(&conn, project["id"].as_str().unwrap_or(""));
    db::audit(&conn, "info", "job.succeeded", &format!("scene {} generated ({:.1} s)", scene["position"].as_i64().unwrap_or(0) + 1, media.duration.unwrap_or(0.0)));
    drop(conn);
    let _ = crate::projects::snapshot(app, project["id"].as_str().unwrap_or(""));
    Ok(())
}

fn export(app: &App, job: &Value) -> Result<()> {
    let job_id = job["id"].as_str().unwrap_or("");
    set(app, job_id, "status = 'running', started_at = ?1, stage = 'rendering'", &[&now()]);
    let options: Value = job["request_json"].as_str().and_then(|s| serde_json::from_str(s).ok()).unwrap_or(json!({}));
    let out = crate::timeline::render(app, job["project_id"].as_str().unwrap_or(""), &options, |p| set(app, job_id, "progress = ?1", &[&p]), || is_canceled(app, job_id))?;
    if out.is_null() { return Ok(()); } // canceled
    set(app, job_id, "status = 'succeeded', result_path = ?1, finished_at = ?2, stage = 'done', progress = 1.0", &[&out["path"].as_str().unwrap_or(""), &now()]);
    Ok(())
}

/// One pass of the worker: returns true when a job was processed.
pub fn tick(app: &App) -> bool {
    let next = {
        let conn = app.db.lock().unwrap();
        row(&conn, "SELECT * FROM jobs WHERE status = 'queued' OR (status = 'blocked') ORDER BY CASE status WHEN 'queued' THEN 0 ELSE 1 END, created_at LIMIT 1", &[]).ok().flatten()
    };
    let Some(job) = next else { return false };
    let job_id = job["id"].as_str().unwrap_or("").to_string();
    let was_blocked = job["status"] == "blocked";
    let result = if job["kind"] == "export" { export(app, &job) } else { generate(app, &job) };
    if let Err(e) = result {
        if WAITING.contains(&e.code.as_str()) && job["remote_id"].is_null() {
            block(app, &job_id, &e.code);
        } else if ["download_interrupted", "comfy_unreachable"].contains(&e.code.as_str()) && job["attempts"].as_i64().unwrap_or(0) + 1 < MAX_ATTEMPTS {
            // the server may still hold the result: try again from the stored remote id
            set(app, &job_id, "status = 'queued', attempts = attempts + 1, stage = 'retrying after a connection problem'", &[]);
        } else if !is_canceled(app, &job_id) {
            fail(app, &job, &e);
        }
    }
    !was_blocked
}

/// Starts the background worker thread. It also reconciles the GPU ledger and applies the idle shutdown.
pub fn start_worker(app: Arc<App>) -> std::thread::JoinHandle<()> {
    std::thread::spawn(move || {
        let mut last_gpu = std::time::Instant::now();
        while !app.shutting_down.load(Ordering::SeqCst) {
            let worked = tick(&app);
            if last_gpu.elapsed() > Duration::from_secs(30) {
                last_gpu = std::time::Instant::now();
                let _ = gpu::idle_check(&app);
            }
            std::thread::sleep(Duration::from_millis(if worked { 150 } else { 1500 }));
        }
    })
}
