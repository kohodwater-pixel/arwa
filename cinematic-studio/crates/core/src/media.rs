//! Media library. Originals stay where the user keeps them: the library stores a reference, a hash,
//! measured metadata and a small thumbnail in Cache/.
use crate::args::*;
use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::App;
use rusqlite::params;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::io::Read;
use std::path::Path;

const MAX_BYTES: u64 = 8 * 1024 * 1024 * 1024;

/// File type by content signature. The extension and anything the OS claims are ignored.
pub fn sniff(head: &[u8]) -> Option<(&'static str, &'static str)> {
    let s = |a: usize, b: usize| head.get(a..b).map(|x| String::from_utf8_lossy(x).to_string()).unwrap_or_default();
    if head.starts_with(&[0x89, b'P', b'N', b'G', 0x0d, 0x0a, 0x1a, 0x0a]) { return Some(("image", "png")); }
    if head.starts_with(&[0xff, 0xd8, 0xff]) { return Some(("image", "jpg")); }
    if s(0, 4) == "RIFF" && s(8, 12) == "WEBP" { return Some(("image", "webp")); }
    if s(0, 4) == "RIFF" && s(8, 12) == "WAVE" { return Some(("audio", "wav")); }
    if s(0, 3) == "ID3" || (head.len() > 1 && head[0] == 0xff && (head[1] & 0xe0) == 0xe0 && (head[1] & 0x06) != 0) { return Some(("audio", "mp3")); }
    if s(0, 4) == "OggS" { return Some(("audio", "ogg")); }
    if s(0, 4) == "fLaC" { return Some(("audio", "flac")); }
    if s(4, 8) == "ftyp" {
        let brand = s(8, 12);
        if brand.starts_with("M4A") || brand.starts_with("M4B") { return Some(("audio", "m4a")); }
        if brand.starts_with("qt") { return Some(("video", "mov")); }
        return Some(("video", "mp4"));
    }
    if head.starts_with(&[0x1a, 0x45, 0xdf, 0xa3]) { return Some(("video", "webm")); }
    None
}

pub fn sha256_file(path: &Path) -> Result<String> {
    let mut f = std::fs::File::open(path)?;
    let mut h = Sha256::new();
    let mut buf = vec![0u8; 1 << 20];
    loop {
        let n = f.read(&mut buf)?;
        if n == 0 { break; }
        h.update(&buf[..n]);
    }
    Ok(hex::encode(h.finalize()))
}

fn import_one(app: &App, path: &str, project_id: Option<&str>, folder: &str) -> Result<Value> {
    let p = Path::new(path);
    if !p.is_absolute() { return err("bad_path", "an absolute path is required"); }
    let meta = std::fs::symlink_metadata(p).map_err(|_| AppError::new("file_missing", path.to_string()))?;
    if !meta.is_file() { return err("not_a_file", "only regular files can be imported"); }
    if meta.len() == 0 || meta.len() > MAX_BYTES { return err("bad_size", "the file is empty or larger than 8 GB"); }
    let mut head = [0u8; 16];
    let n = std::fs::File::open(p)?.read(&mut head)?;
    let (kind, _ext) = sniff(&head[..n]).ok_or_else(|| AppError::new("unsupported_type", "not a supported image, video or audio file"))?;
    let hash = sha256_file(p)?;
    {
        let conn = app.db.lock().unwrap();
        if let Some(existing) = row(&conn, "SELECT * FROM media WHERE sha256 = ?1", &[&hash])? {
            let mut e = existing;
            e["duplicate"] = json!(true);
            return Ok(e);
        }
    }
    let tools = app.tools()?;
    let info = crate::ffmpeg::probe(&tools, p)?;
    if (kind == "audio" && !info.has_audio) || (kind != "audio" && !info.has_video) {
        return err("unreadable_media", "the file does not contain a readable stream of its type");
    }
    let lib = app.lib();
    let mut thumb: Option<String> = None;
    if kind != "audio" {
        let rel = format!("Cache/thumbs/{}.jpg", &hash[..24]);
        let at = if kind == "video" { (info.duration.unwrap_or(0.0) / 3.0).min(2.0) } else { 0.0 };
        if crate::ffmpeg::thumbnail(&tools, p, &lib.resolve(&rel)?, at).is_ok() { thumb = Some(rel); }
    }
    let id = new_id();
    let name = limit(&p.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default(), 200);
    let conn = app.db.lock().unwrap();
    conn.execute(
        "INSERT INTO media (id, project_id, folder, kind, name, path, sha256, size, duration, width, height, fps, thumb_path, imported_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14)",
        params![id, project_id, limit(folder, 80), kind, name, p.to_string_lossy(), hash, meta.len() as i64, info.duration, info.width, info.height, info.fps, thumb, now()],
    )?;
    let mut out = row(&conn, "SELECT * FROM media WHERE id = ?1", &[&id])?.unwrap();
    out["duplicate"] = json!(false);
    Ok(out)
}

/// Imports several files; one bad file does not stop the rest. Each result says what happened.
pub fn import(app: &App, a: &Value) -> Result<Value> {
    let paths: Vec<&str> = a["paths"].as_array().map(|x| x.iter().filter_map(Value::as_str).collect()).unwrap_or_default();
    if paths.is_empty() || paths.len() > 500 { return err("bad_request", "choose between 1 and 500 files"); }
    let (project, folder) = (str_opt(a, "project_id"), str_opt(a, "folder").unwrap_or(""));
    let mut results = vec![];
    for p in paths {
        match import_one(app, p, project, folder) {
            Ok(m) => results.push(json!({ "path": p, "ok": true, "duplicate": m["duplicate"], "media": m })),
            Err(e) => results.push(json!({ "path": p, "ok": false, "error": e.code, "detail": e.message })),
        }
    }
    Ok(json!(results))
}

pub fn list(app: &App, a: &Value) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let mut sql = String::from("SELECT * FROM media WHERE 1=1");
    let mut p: Vec<String> = vec![];
    if let Some(k) = str_opt(a, "kind").filter(|k| ["image", "video", "audio"].contains(k)) { sql.push_str(&format!(" AND kind = ?{}", p.len() + 1)); p.push(k.into()); }
    if let Some(f) = str_opt(a, "folder") { sql.push_str(&format!(" AND folder = ?{}", p.len() + 1)); p.push(f.into()); }
    if let Some(pr) = str_opt(a, "project_id") { sql.push_str(&format!(" AND project_id = ?{}", p.len() + 1)); p.push(pr.into()); }
    if let Some(q) = str_opt(a, "q").filter(|q| !q.trim().is_empty()) { sql.push_str(&format!(" AND name LIKE ?{} ESCAPE '\\'", p.len() + 1)); p.push(format!("%{}%", q.trim().replace('\\', "\\\\").replace('%', "\\%").replace('_', "\\_"))); }
    sql.push_str(" ORDER BY imported_at DESC LIMIT 1000");
    let refs: Vec<&dyn rusqlite::ToSql> = p.iter().map(|s| s as &dyn rusqlite::ToSql).collect();
    let items = rows(&conn, &sql, &refs)?;
    let folders: Vec<Value> = rows(&conn, "SELECT folder, COUNT(*) AS count FROM media GROUP BY folder ORDER BY folder", &[])?;
    Ok(json!({ "items": items, "folders": folders }))
}

pub fn update(app: &App, id: &str, a: &Value) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    if let Some(f) = str_opt(a, "folder") { conn.execute("UPDATE media SET folder = ?1 WHERE id = ?2", params![limit(f.trim(), 80), id])?; }
    if a.get("project_id").is_some() { conn.execute("UPDATE media SET project_id = ?1 WHERE id = ?2", params![str_opt(a, "project_id"), id])?; }
    row(&conn, "SELECT * FROM media WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("media_not_found", id.to_string()))
}

/// Forgets the library entry and its thumbnail. The user's original file is not touched.
pub fn remove(app: &App, id: &str) -> Result<Value> {
    let lib = app.lib();
    let conn = app.db.lock().unwrap();
    let m = row(&conn, "SELECT * FROM media WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("media_not_found", id.to_string()))?;
    conn.execute("UPDATE scenes SET reference_media_id = NULL WHERE reference_media_id = ?1", [id])?;
    conn.execute("DELETE FROM media WHERE id = ?1", [id])?;
    if let Some(t) = m["thumb_path"].as_str() { if let Ok(p) = lib.resolve(t) { let _ = std::fs::remove_file(p); } }
    Ok(json!({ "ok": true }))
}

/// Re-checks every entry: is the original still there, and (for a changed file) does it still decode?
pub fn verify(app: &App) -> Result<Value> {
    let items = { let conn = app.db.lock().unwrap(); rows(&conn, "SELECT id, path, size, kind FROM media", &[])? };
    let tools = app.tools().ok();
    let (mut missing, mut corrupted) = (0, 0);
    for m in &items {
        let p = Path::new(m["path"].as_str().unwrap_or(""));
        let (mut is_missing, mut is_corrupt) = (false, false);
        match std::fs::metadata(p) {
            Err(_) => is_missing = true,
            Ok(md) => {
                if md.len() as i64 != m["size"].as_i64().unwrap_or(-1) {
                    is_corrupt = match &tools { Some(t) => crate::ffmpeg::probe(t, p).is_err(), None => true };
                }
            }
        }
        missing += is_missing as i32;
        corrupted += is_corrupt as i32;
        let conn = app.db.lock().unwrap();
        conn.execute("UPDATE media SET missing = ?1, corrupted = ?2 WHERE id = ?3", params![is_missing as i64, is_corrupt as i64, m["id"].as_str()])?;
    }
    let conn = app.db.lock().unwrap();
    db::audit(&conn, "info", "media.verify", &format!("{} checked, {missing} missing, {corrupted} corrupted", items.len()));
    Ok(json!({ "checked": items.len(), "missing": missing, "corrupted": corrupted }))
}
