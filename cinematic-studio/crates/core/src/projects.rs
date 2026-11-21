//! Projects and scenes. Every change is written to SQLite at once (that is the auto-save) and mirrored to
//! `project.json` in the project folder, so a project folder is self-describing and can be re-imported.
use crate::args::*;
use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::paths::{safe_join, slug, Library};
use crate::App;
use rusqlite::{params, Connection};
use serde_json::{json, Value};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};

pub const ASPECTS: [&str; 4] = ["16:9", "9:16", "1:1", "4:5"];
pub const VIDEO_TYPES: [&str; 8] = ["commercial", "short_film", "tourism", "real_estate", "product", "creative", "social", "motion_graphics"];
const MAX_SCENES: usize = 40;
const MAX_ARCHIVE_BYTES: u64 = 20 * 1024 * 1024 * 1024;

fn project_row(conn: &Connection, id: &str) -> Result<Value> {
    row(conn, "SELECT * FROM projects WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("project_not_found", id.to_string()))
}
pub fn folder_of(lib: &Library, project: &Value) -> Result<PathBuf> {
    lib.resolve(project["folder"].as_str().unwrap_or(""))
}
fn touch(conn: &Connection, id: &str) -> Result<()> {
    conn.execute("UPDATE projects SET updated_at = ?1 WHERE id = ?2", params![now(), id])?;
    Ok(())
}
fn parse_json_fields(mut p: Value) -> Value {
    for k in ["director_json", "timeline_json", "model_config_json"] {
        let parsed = p[k].as_str().and_then(|s| serde_json::from_str::<Value>(s).ok()).unwrap_or(Value::Null);
        p[k.trim_end_matches("_json")] = parsed;
        if let Some(o) = p.as_object_mut() {
            o.remove(k);
        }
    }
    p
}

pub fn create(app: &App, a: &Value) -> Result<Value> {
    let name = limit(str_req(a, "name")?.trim(), 120);
    let video_type = str_opt(a, "video_type").unwrap_or("commercial");
    one_of(video_type, &VIDEO_TYPES, "video_type")?;
    let aspect = str_opt(a, "aspect").unwrap_or("16:9");
    one_of(aspect, &ASPECTS, "aspect")?;
    let duration = i64_opt(a, "duration").unwrap_or(15).clamp(2, 600);
    let id = new_id();
    let lib = app.lib();
    let folder = format!("Projects/{}-{}", slug(&name, 40), &id[..8]);
    let dir = lib.resolve(&folder)?;
    for sub in ["scenes", "exports", "refs"] {
        std::fs::create_dir_all(dir.join(sub))?;
    }
    let t = now();
    {
        let conn = app.db.lock().unwrap();
        conn.execute(
            "INSERT INTO projects (id, name, description, video_type, style, aspect, duration, model_id, folder, created_at, updated_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?10)",
            params![id, name, limit(str_opt(a, "description").unwrap_or(""), 4000), video_type, limit(str_opt(a, "style").unwrap_or("auto"), 40), aspect, duration, limit(str_opt(a, "model_id").unwrap_or("wan22-ti2v-5b"), 60), folder, t],
        )?;
        db::set_setting(&conn, "last_project", &id)?;
        db::audit(&conn, "info", "project.created", &name);
    }
    snapshot(app, &id)?;
    get(app, &id)
}

pub fn list(app: &App) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let items = rows(
        &conn,
        "SELECT p.id, p.name, p.description, p.video_type, p.aspect, p.duration, p.model_id, p.status, p.created_at, p.updated_at, p.folder,
                (SELECT COUNT(*) FROM scenes s WHERE s.project_id = p.id) AS scene_count,
                (SELECT COUNT(*) FROM scenes s WHERE s.project_id = p.id AND s.status = 'completed') AS scenes_done,
                (SELECT preview_path FROM scenes s WHERE s.project_id = p.id AND s.preview_path IS NOT NULL ORDER BY position LIMIT 1) AS preview_path
         FROM projects p ORDER BY p.updated_at DESC",
        &[],
    )?;
    Ok(json!(items))
}

pub fn get(app: &App, id: &str) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let mut p = parse_json_fields(project_row(&conn, id)?);
    p["scenes"] = json!(rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&id])?);
    p["exports"] = json!(rows(&conn, "SELECT * FROM exports WHERE project_id = ?1 ORDER BY created_at DESC", &[&id])?);
    p["absolute_folder"] = json!(app.lib().resolve(p["folder"].as_str().unwrap_or(""))?.to_string_lossy());
    db::set_setting(&conn, "last_project", id)?;
    Ok(p)
}

/// Whitelisted project fields only; unknown keys are ignored.
pub fn update(app: &App, id: &str, patch: &Value) -> Result<Value> {
    {
        let conn = app.db.lock().unwrap();
        project_row(&conn, id)?;
        if let Some(v) = str_opt(patch, "name").filter(|v| !v.trim().is_empty()) {
            conn.execute("UPDATE projects SET name = ?1 WHERE id = ?2", params![limit(v.trim(), 120), id])?;
        }
        if let Some(v) = str_opt(patch, "description") {
            conn.execute("UPDATE projects SET description = ?1 WHERE id = ?2", params![limit(v, 4000), id])?;
        }
        if let Some(v) = str_opt(patch, "video_type") {
            one_of(v, &VIDEO_TYPES, "video_type")?;
            conn.execute("UPDATE projects SET video_type = ?1 WHERE id = ?2", params![v, id])?;
        }
        if let Some(v) = str_opt(patch, "aspect") {
            one_of(v, &ASPECTS, "aspect")?;
            conn.execute("UPDATE projects SET aspect = ?1 WHERE id = ?2", params![v, id])?;
        }
        if let Some(v) = str_opt(patch, "style") {
            conn.execute("UPDATE projects SET style = ?1 WHERE id = ?2", params![limit(v, 40), id])?;
        }
        if let Some(v) = str_opt(patch, "model_id") {
            conn.execute("UPDATE projects SET model_id = ?1 WHERE id = ?2", params![limit(v, 60), id])?;
        }
        if let Some(v) = i64_opt(patch, "duration") {
            conn.execute("UPDATE projects SET duration = ?1 WHERE id = ?2", params![v.clamp(2, 600), id])?;
        }
        if let Some(v) = str_opt(patch, "status") {
            one_of(v, &["draft", "storyboard", "generating", "ready", "exported"], "status")?;
            conn.execute("UPDATE projects SET status = ?1 WHERE id = ?2", params![v, id])?;
        }
        for (key, col) in [("director", "director_json"), ("timeline", "timeline_json"), ("model_config", "model_config_json")] {
            if let Some(v) = patch.get(key) {
                let text = serde_json::to_string(v)?;
                if text.len() > 2_000_000 {
                    return err("bad_request", format!("{key} is too large"));
                }
                conn.execute(&format!("UPDATE projects SET {col} = ?1 WHERE id = ?2"), params![text, id])?;
            }
        }
        touch(&conn, id)?;
    }
    snapshot(app, id)?;
    get(app, id)
}

// ── scenes ─────────────────────────────────────────────────────────────────
fn scene_values(s: &Value) -> Result<(String, i64, String, String, String)> {
    let title = limit(str_opt(s, "title").unwrap_or("Scene"), 120);
    let duration = i64_opt(s, "duration").unwrap_or(5).clamp(1, 30);
    Ok((title, duration, limit(str_opt(s, "description").unwrap_or(""), 2000), limit(str_opt(s, "prompt").unwrap_or(""), 6000), limit(str_opt(s, "negative_prompt").unwrap_or(""), 3000)))
}
fn insert_scene(conn: &Connection, project_id: &str, position: i64, s: &Value) -> Result<String> {
    let (title, duration, description, prompt, negative) = scene_values(s)?;
    let id = new_id();
    conn.execute(
        "INSERT INTO scenes (id, project_id, position, role, title, duration, description, prompt, negative_prompt, prompt_edited, camera_move, shot_size, camera_angle, lighting, reference_media_id, seed, updated_at)
         VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14,?15,?16,?17)",
        params![id, project_id, position, str_opt(s, "role"), title, duration, description, prompt, negative, bool_opt(s, "prompt_edited").unwrap_or(false) as i64,
            str_opt(s, "camera_move"), str_opt(s, "shot_size"), str_opt(s, "camera_angle"), str_opt(s, "lighting"), str_opt(s, "reference_media_id"), i64_opt(s, "seed"), now()],
    )?;
    Ok(id)
}
fn renumber(conn: &Connection, project_id: &str) -> Result<()> {
    let ids: Vec<String> = { let mut st = conn.prepare("SELECT id FROM scenes WHERE project_id = ?1 ORDER BY position, updated_at")?; let v = st.query_map([project_id], |r| r.get(0))?.collect::<std::result::Result<Vec<String>, _>>()?; v };
    for (i, sid) in ids.iter().enumerate() {
        conn.execute("UPDATE scenes SET position = ?1 WHERE id = ?2", params![i as i64, sid])?;
    }
    let total: i64 = conn.query_row("SELECT COALESCE(SUM(duration), 0) FROM scenes WHERE project_id = ?1", [project_id], |r| r.get(0))?;
    if total > 0 {
        conn.execute("UPDATE projects SET duration = ?1 WHERE id = ?2", params![total, project_id])?;
    }
    touch(conn, project_id)
}
/// Generated files of a scene are moved aside, not deleted, when the scene changes or goes away.
fn retire_scene_files(lib: &Library, project: &Value, scene: &Value) {
    let Ok(dir) = folder_of(lib, project) else { return };
    for key in ["video_path", "preview_path"] {
        if let Some(rel) = scene[key].as_str() {
            if let Ok(p) = lib.resolve(rel) {
                if p.is_file() {
                    let old = dir.join("scenes").join("_replaced");
                    let _ = std::fs::create_dir_all(&old);
                    let _ = std::fs::rename(&p, old.join(format!("{}-{}", chrono::Utc::now().format("%Y%m%d%H%M%S"), p.file_name().unwrap_or_default().to_string_lossy())));
                }
            }
        }
    }
}

/// Replaces the whole storyboard (used when the director builds a new one).
pub fn storyboard_replace(app: &App, project_id: &str, scenes: &Value) -> Result<Value> {
    let list = scenes.as_array().ok_or_else(|| AppError::new("bad_request", "scenes must be a list"))?;
    if list.is_empty() || list.len() > MAX_SCENES {
        return err("bad_request", format!("a storyboard has 1 to {MAX_SCENES} scenes"));
    }
    {
        let conn = app.db.lock().unwrap();
        let project = project_row(&conn, project_id)?;
        let active: i64 = conn.query_row("SELECT COUNT(*) FROM jobs WHERE project_id = ?1 AND status IN ('queued','blocked','submitted','running','downloading')", [project_id], |r| r.get(0))?;
        if active > 0 {
            return err("project_busy", "cancel the running jobs before rebuilding the storyboard");
        }
        let lib = app.lib();
        for old in rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1", &[&project_id])? {
            retire_scene_files(&lib, &project, &old);
        }
        let tx = conn.unchecked_transaction()?;
        tx.execute("DELETE FROM scenes WHERE project_id = ?1", [project_id])?;
        for (i, s) in list.iter().enumerate() {
            insert_scene(&tx, project_id, i as i64, s)?;
        }
        tx.execute("UPDATE projects SET status = 'storyboard' WHERE id = ?1", [project_id])?;
        tx.commit()?;
        renumber(&conn, project_id)?;
    }
    snapshot(app, project_id)?;
    get(app, project_id)
}

pub fn scene_add(app: &App, project_id: &str, scene: &Value, position: Option<i64>) -> Result<Value> {
    {
        let conn = app.db.lock().unwrap();
        project_row(&conn, project_id)?;
        let count: i64 = conn.query_row("SELECT COUNT(*) FROM scenes WHERE project_id = ?1", [project_id], |r| r.get(0))?;
        if count as usize >= MAX_SCENES {
            return err("bad_request", "too many scenes");
        }
        let pos = position.unwrap_or(count).clamp(0, count);
        conn.execute("UPDATE scenes SET position = position + 1 WHERE project_id = ?1 AND position >= ?2", params![project_id, pos])?;
        insert_scene(&conn, project_id, pos, scene)?;
        renumber(&conn, project_id)?;
    }
    snapshot(app, project_id)?;
    get(app, project_id)
}

pub fn scene_update(app: &App, scene_id: &str, patch: &Value) -> Result<Value> {
    let project_id: String;
    {
        let conn = app.db.lock().unwrap();
        let scene = row(&conn, "SELECT * FROM scenes WHERE id = ?1", &[&scene_id])?.ok_or_else(|| AppError::new("scene_not_found", scene_id.to_string()))?;
        project_id = scene["project_id"].as_str().unwrap_or("").to_string();
        if ["queued", "generating"].contains(&scene["status"].as_str().unwrap_or("")) {
            return err("scene_busy", "this scene is being generated");
        }
        let mut visual = false;
        let text_fields: [(&str, usize, bool); 8] = [("title", 120, false), ("description", 2000, true), ("prompt", 6000, true), ("negative_prompt", 3000, true), ("camera_move", 40, true), ("shot_size", 40, true), ("camera_angle", 80, true), ("lighting", 120, true)];
        for (key, max, is_visual) in text_fields {
            if let Some(v) = str_opt(patch, key) {
                if scene[key].as_str().unwrap_or("") != v {
                    conn.execute(&format!("UPDATE scenes SET {key} = ?1 WHERE id = ?2"), params![limit(v, max), scene_id])?;
                    visual |= is_visual;
                }
            }
        }
        if let Some(d) = i64_opt(patch, "duration") {
            if scene["duration"].as_i64() != Some(d) {
                conn.execute("UPDATE scenes SET duration = ?1 WHERE id = ?2", params![d.clamp(1, 30), scene_id])?;
                visual = true;
            }
        }
        if patch.get("seed").is_some() {
            conn.execute("UPDATE scenes SET seed = ?1 WHERE id = ?2", params![i64_opt(patch, "seed"), scene_id])?;
            visual = true;
        }
        if let Some(v) = patch.get("reference_media_id") {
            let mid = v.as_str();
            if let Some(m) = mid {
                let ok: i64 = conn.query_row("SELECT COUNT(*) FROM media WHERE id = ?1 AND kind = 'image'", [m], |r| r.get(0))?;
                if ok == 0 {
                    return err("bad_request", "the visual reference must be an image from the media library");
                }
            }
            conn.execute("UPDATE scenes SET reference_media_id = ?1 WHERE id = ?2", params![mid, scene_id])?;
            visual = true;
        }
        if let Some(v) = bool_opt(patch, "prompt_edited") {
            conn.execute("UPDATE scenes SET prompt_edited = ?1 WHERE id = ?2", params![v as i64, scene_id])?;
        }
        // A change to what the scene shows makes its generated clip stale: keep the file aside, mark the scene pending.
        if visual && scene["status"] == "completed" && bool_opt(patch, "keep_video") != Some(true) {
            let project = project_row(&conn, &project_id)?;
            retire_scene_files(&app.lib(), &project, &scene);
            conn.execute("UPDATE scenes SET status = 'pending', video_path = NULL, preview_path = NULL, video_duration = NULL, error = NULL WHERE id = ?1", [scene_id])?;
        }
        conn.execute("UPDATE scenes SET updated_at = ?1 WHERE id = ?2", params![now(), scene_id])?;
        renumber(&conn, &project_id)?;
    }
    snapshot(app, &project_id)?;
    get(app, &project_id)
}

pub fn scene_delete(app: &App, scene_id: &str) -> Result<Value> {
    let project_id: String;
    {
        let conn = app.db.lock().unwrap();
        let scene = row(&conn, "SELECT * FROM scenes WHERE id = ?1", &[&scene_id])?.ok_or_else(|| AppError::new("scene_not_found", scene_id.to_string()))?;
        project_id = scene["project_id"].as_str().unwrap_or("").to_string();
        if ["queued", "generating"].contains(&scene["status"].as_str().unwrap_or("")) {
            return err("scene_busy", "this scene is being generated");
        }
        let project = project_row(&conn, &project_id)?;
        retire_scene_files(&app.lib(), &project, &scene);
        conn.execute("DELETE FROM scenes WHERE id = ?1", [scene_id])?;
        renumber(&conn, &project_id)?;
    }
    snapshot(app, &project_id)?;
    get(app, &project_id)
}

pub fn scenes_reorder(app: &App, project_id: &str, order: &Value) -> Result<Value> {
    let ids: Vec<&str> = order.as_array().map(|a| a.iter().filter_map(Value::as_str).collect()).unwrap_or_default();
    {
        let conn = app.db.lock().unwrap();
        let existing: Vec<String> = { let mut st = conn.prepare("SELECT id FROM scenes WHERE project_id = ?1")?; let v = st.query_map([project_id], |r| r.get(0))?.collect::<std::result::Result<Vec<String>, _>>()?; v };
        let mut sorted_a: Vec<&str> = ids.clone();
        let mut sorted_b: Vec<&str> = existing.iter().map(String::as_str).collect();
        sorted_a.sort();
        sorted_b.sort();
        if sorted_a != sorted_b {
            return err("bad_request", "the new order must list every scene exactly once");
        }
        let tx = conn.unchecked_transaction()?;
        for (i, sid) in ids.iter().enumerate() {
            tx.execute("UPDATE scenes SET position = ?1 WHERE id = ?2", params![i as i64, sid])?;
        }
        tx.commit()?;
        touch(&conn, project_id)?;
    }
    snapshot(app, project_id)?;
    get(app, project_id)
}

// ── snapshot, backup, export, import, duplicate, delete ──────────────────────
/// Writes project.json (atomically: temp file then rename) next to the project's media.
pub fn snapshot(app: &App, id: &str) -> Result<()> {
    let conn = app.db.lock().unwrap();
    let project = project_row(&conn, id)?;
    let scenes = rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&id])?;
    let media = rows(&conn, "SELECT id, kind, name, path, sha256, size, folder FROM media WHERE project_id = ?1 OR id IN (SELECT reference_media_id FROM scenes WHERE project_id = ?1)", &[&id])?;
    let dir = folder_of(&app.lib(), &project)?;
    std::fs::create_dir_all(&dir)?;
    let doc = json!({ "format": "cinematic-studio-project", "format_version": 1, "saved_at": now(), "project": project, "scenes": scenes, "media_references": media });
    let tmp = dir.join("project.json.tmp");
    std::fs::write(&tmp, serde_json::to_vec_pretty(&doc)?)?;
    std::fs::rename(&tmp, dir.join("project.json"))?;
    Ok(())
}

fn zip_dir(src: &Path, dest: &Path) -> Result<u64> {
    let file = std::fs::File::create(dest)?;
    let mut zip = zip::ZipWriter::new(file);
    let opts = zip::write::SimpleFileOptions::default().compression_method(zip::CompressionMethod::Deflated).large_file(true);
    let mut stack = vec![src.to_path_buf()];
    let mut count = 0u64;
    while let Some(dir) = stack.pop() {
        for entry in std::fs::read_dir(&dir)? {
            let entry = entry?;
            let path = entry.path();
            let ft = entry.file_type()?;
            if ft.is_symlink() {
                continue; // never follow links out of the project
            }
            let name = path.strip_prefix(src).unwrap().to_string_lossy().replace('\\', "/");
            if ft.is_dir() {
                stack.push(path);
            } else if !name.ends_with(".tmp") {
                zip.start_file(name, opts)?;
                let mut f = std::fs::File::open(&path)?;
                std::io::copy(&mut f, &mut zip)?;
                count += 1;
            }
        }
    }
    zip.finish()?;
    Ok(count)
}

pub fn backup(app: &App, id: &str) -> Result<Value> {
    snapshot(app, id)?;
    let (project, lib) = { let conn = app.db.lock().unwrap(); (project_row(&conn, id)?, app.lib()) };
    let name = format!("{}-{}.zip", slug(project["name"].as_str().unwrap_or("project"), 40), chrono::Utc::now().format("%Y%m%d-%H%M%S"));
    let dest = lib.dir("Backups").join(&name);
    let files = zip_dir(&folder_of(&lib, &project)?, &dest)?;
    let conn = app.db.lock().unwrap();
    db::audit(&conn, "info", "project.backup", &name);
    Ok(json!({ "path": dest.to_string_lossy(), "files": files, "size": std::fs::metadata(&dest)?.len() }))
}

/// Exports a project as one .zip the user can move to another machine.
pub fn export_archive(app: &App, id: &str, dest: &str) -> Result<Value> {
    let dest = PathBuf::from(dest);
    if !dest.is_absolute() || dest.extension().and_then(|e| e.to_str()) != Some("zip") {
        return err("bad_path", "choose an absolute path ending in .zip");
    }
    snapshot(app, id)?;
    let (project, lib) = { let conn = app.db.lock().unwrap(); (project_row(&conn, id)?, app.lib()) };
    let files = zip_dir(&folder_of(&lib, &project)?, &dest)?;
    Ok(json!({ "path": dest.to_string_lossy(), "files": files, "size": std::fs::metadata(&dest)?.len() }))
}

/// Imports a project archive. Every entry name is checked before anything is written (zip-slip guard),
/// and the total unpacked size is capped.
pub fn import_archive(app: &App, archive: &str) -> Result<Value> {
    let file = std::fs::File::open(archive).map_err(|e| AppError::new("bad_path", e.to_string()))?;
    let mut zip = zip::ZipArchive::new(file)?;
    let mut doc_text = String::new();
    zip.by_name("project.json").map_err(|_| AppError::new("not_a_project", "the archive has no project.json"))?.take(8_000_000).read_to_string(&mut doc_text)?;
    let doc: Value = serde_json::from_str(&doc_text)?;
    if doc["format"] != "cinematic-studio-project" {
        return err("not_a_project", "unknown project format");
    }
    let mut total: u64 = 0;
    for i in 0..zip.len() {
        let e = zip.by_index(i)?;
        total += e.size();
        if e.enclosed_name().is_none() || total > MAX_ARCHIVE_BYTES {
            return err("unsafe_archive", "the archive contains an unsafe path or is too large");
        }
    }
    let src = &doc["project"];
    let id = new_id();
    let lib = app.lib();
    let name = limit(src["name"].as_str().unwrap_or("Imported project"), 120);
    let folder = format!("Projects/{}-{}", slug(&name, 40), &id[..8]);
    let dir = lib.resolve(&folder)?;
    std::fs::create_dir_all(&dir)?;
    for i in 0..zip.len() {
        let mut e = zip.by_index(i)?;
        let rel = e.enclosed_name().ok_or_else(|| AppError::new("unsafe_archive", "unsafe path"))?;
        let out = safe_join(&dir, &rel.to_string_lossy())?;
        if e.is_dir() {
            std::fs::create_dir_all(&out)?;
        } else {
            if let Some(p) = out.parent() {
                std::fs::create_dir_all(p)?;
            }
            let mut f = std::fs::File::create(&out)?;
            std::io::copy(&mut e, &mut f)?;
            f.flush()?;
        }
    }
    let old_folder = src["folder"].as_str().unwrap_or("").to_string();
    let rebase = |v: &Value| -> Option<String> { v.as_str().map(|p| p.replacen(&old_folder, &folder, 1)).filter(|p| lib.resolve(p).map(|x| x.is_file()).unwrap_or(false)) };
    let t = now();
    {
        let conn = app.db.lock().unwrap();
        let aspect = src["aspect"].as_str().filter(|a| ASPECTS.contains(a)).unwrap_or("16:9");
        let vt = src["video_type"].as_str().filter(|a| VIDEO_TYPES.contains(a)).unwrap_or("commercial");
        conn.execute(
            "INSERT INTO projects (id, name, description, video_type, style, aspect, duration, model_id, model_config_json, status, folder, director_json, timeline_json, created_at, updated_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14,?14)",
            params![id, name, limit(src["description"].as_str().unwrap_or(""), 4000), vt, src["style"].as_str().unwrap_or("auto"), aspect, src["duration"].as_i64().unwrap_or(15).clamp(2, 600),
                src["model_id"].as_str().unwrap_or("wan22-ti2v-5b"), src["model_config_json"].as_str().unwrap_or("{}"), "storyboard", folder, src["director_json"].as_str(), Option::<String>::None, t],
        )?;
        for (i, s) in doc["scenes"].as_array().cloned().unwrap_or_default().iter().take(MAX_SCENES).enumerate() {
            let sid = insert_scene(&conn, &id, i as i64, s)?;
            let video = rebase(&s["video_path"]);
            conn.execute("UPDATE scenes SET video_path = ?1, preview_path = ?2, video_duration = ?3, status = ?4, reference_media_id = NULL WHERE id = ?5",
                params![video, rebase(&s["preview_path"]), s["video_duration"].as_f64(), if video.is_some() { "completed" } else { "pending" }, sid])?;
        }
        db::audit(&conn, "info", "project.imported", &name);
    }
    snapshot(app, &id)?;
    get(app, &id)
}

fn copy_dir(src: &Path, dest: &Path) -> Result<()> {
    std::fs::create_dir_all(dest)?;
    for entry in std::fs::read_dir(src)? {
        let entry = entry?;
        let ft = entry.file_type()?;
        let to = dest.join(entry.file_name());
        if ft.is_dir() {
            if entry.file_name() != "_replaced" {
                copy_dir(&entry.path(), &to)?;
            }
        } else if ft.is_file() {
            std::fs::copy(entry.path(), to)?;
        }
    }
    Ok(())
}

pub fn duplicate(app: &App, id: &str) -> Result<Value> {
    snapshot(app, id)?;
    let lib = app.lib();
    let new = new_id();
    {
        let conn = app.db.lock().unwrap();
        let src = project_row(&conn, id)?;
        let name = limit(&format!("{} (copy)", src["name"].as_str().unwrap_or("")), 120);
        let old_folder = src["folder"].as_str().unwrap_or("").to_string();
        let folder = format!("Projects/{}-{}", slug(&name, 40), &new[..8]);
        copy_dir(&lib.resolve(&old_folder)?, &lib.resolve(&folder)?)?;
        let t = now();
        conn.execute(
            "INSERT INTO projects (id, name, description, video_type, style, aspect, duration, model_id, model_config_json, status, folder, director_json, timeline_json, created_at, updated_at)
             SELECT ?1, ?2, description, video_type, style, aspect, duration, model_id, model_config_json, CASE WHEN status = 'generating' THEN 'storyboard' ELSE status END, ?3, director_json, NULL, ?4, ?4 FROM projects WHERE id = ?5",
            params![new, name, folder, t, id],
        )?;
        for s in rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&id])? {
            let sid = insert_scene(&conn, &new, s["position"].as_i64().unwrap_or(0), &s)?;
            let re = |v: &Value| v.as_str().map(|p| p.replacen(&old_folder, &folder, 1));
            let done = s["status"] == "completed";
            conn.execute("UPDATE scenes SET video_path = ?1, preview_path = ?2, video_duration = ?3, status = ?4 WHERE id = ?5",
                params![if done { re(&s["video_path"]) } else { None }, if done { re(&s["preview_path"]) } else { None }, s["video_duration"].as_f64(), if done { "completed" } else { "pending" }, sid])?;
        }
    }
    snapshot(app, &new)?;
    get(app, &new)
}

/// Removes the project from the app. Its folder is moved to Backups/Deleted (not erased) unless `purge` is set.
pub fn delete(app: &App, id: &str, purge: bool) -> Result<Value> {
    let lib = app.lib();
    let conn = app.db.lock().unwrap();
    let project = project_row(&conn, id)?;
    let active: i64 = conn.query_row("SELECT COUNT(*) FROM jobs WHERE project_id = ?1 AND status IN ('submitted','running','downloading')", [id], |r| r.get(0))?;
    if active > 0 {
        return err("project_busy", "cancel the running jobs first");
    }
    let dir = folder_of(&lib, &project)?;
    let mut kept: Option<String> = None;
    if dir.is_dir() {
        if purge {
            std::fs::remove_dir_all(&dir)?;
        } else {
            let bin = lib.dir("Backups").join("Deleted");
            std::fs::create_dir_all(&bin)?;
            let dest = bin.join(format!("{}-{}", chrono::Utc::now().format("%Y%m%d-%H%M%S"), dir.file_name().unwrap_or_default().to_string_lossy()));
            std::fs::rename(&dir, &dest)?;
            kept = Some(dest.to_string_lossy().to_string());
        }
    }
    conn.execute("DELETE FROM projects WHERE id = ?1", [id])?;
    db::audit(&conn, "info", "project.deleted", project["name"].as_str().unwrap_or(""));
    Ok(json!({ "ok": true, "kept_at": kept }))
}

/// Finds generated files that are gone or no longer decode, and referenced originals that moved.
pub fn integrity(app: &App, id: &str) -> Result<Value> {
    let lib = app.lib();
    let tools = app.tools().ok();
    let (scenes, media) = {
        let conn = app.db.lock().unwrap();
        project_row(&conn, id)?;
        (rows(&conn, "SELECT id, position, title, video_path FROM scenes WHERE project_id = ?1 AND video_path IS NOT NULL ORDER BY position", &[&id])?,
         rows(&conn, "SELECT id, name, path FROM media WHERE project_id = ?1 OR id IN (SELECT reference_media_id FROM scenes WHERE project_id = ?1)", &[&id])?)
    };
    let mut missing = vec![];
    let mut corrupted = vec![];
    for s in &scenes {
        match lib.resolve(s["video_path"].as_str().unwrap_or("")) {
            Ok(p) if p.is_file() => {
                if let Some(t) = &tools {
                    if crate::ffmpeg::verify_playable(t, &p).is_err() {
                        corrupted.push(json!({ "scene": s["position"].as_i64().unwrap_or(0) + 1, "title": s["title"], "file": p.to_string_lossy() }));
                    }
                }
            }
            _ => missing.push(json!({ "scene": s["position"].as_i64().unwrap_or(0) + 1, "title": s["title"], "file": s["video_path"] })),
        }
    }
    let missing_media: Vec<Value> = media.iter().filter(|m| !Path::new(m["path"].as_str().unwrap_or("")).is_file()).map(|m| json!({ "name": m["name"], "file": m["path"] })).collect();
    {
        let conn = app.db.lock().unwrap();
        for m in &missing {
            conn.execute("UPDATE scenes SET status = 'pending', error = 'the generated file is missing', video_path = NULL, preview_path = NULL WHERE project_id = ?1 AND video_path = ?2", params![id, m["file"].as_str()])?;
        }
    }
    Ok(json!({ "checked_scenes": scenes.len(), "missing_videos": missing, "corrupted_videos": corrupted, "missing_media": missing_media, "decoded": tools.is_some() }))
}
