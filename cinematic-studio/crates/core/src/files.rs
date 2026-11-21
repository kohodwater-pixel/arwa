//! Read-only file access for the UI (video preview, thumbnails). The web view never receives general file
//! system access: it may read a file only if it is inside the library or is a registered media original.
use crate::error::{err, Result};
use crate::App;
use std::io::{Read, Seek, SeekFrom};
use std::path::{Path, PathBuf};

const CHUNK: u64 = 4 * 1024 * 1024;

pub fn allowed(app: &App, path: &Path) -> bool {
    let Ok(real) = path.canonicalize() else { return false };
    if !real.is_file() { return false; }
    if app.lib().contains(&real) {
        // the database and its journal are never served
        return !real.file_name().map(|n| n.to_string_lossy().starts_with("cinematic-studio.db")).unwrap_or(true);
    }
    let conn = app.db.lock().unwrap();
    let p = path.to_string_lossy().to_string();
    conn.query_row("SELECT COUNT(*) FROM media WHERE path = ?1", [&p], |r| r.get::<_, i64>(0)).map(|n| n > 0).unwrap_or(false)
}

pub fn mime(path: &Path) -> &'static str {
    match path.extension().and_then(|e| e.to_str()).unwrap_or("").to_lowercase().as_str() {
        "mp4" | "m4v" => "video/mp4", "mov" => "video/quicktime", "webm" => "video/webm", "jpg" | "jpeg" => "image/jpeg", "png" => "image/png", "webp" => "image/webp",
        "mp3" => "audio/mpeg", "wav" => "audio/wav", "m4a" => "audio/mp4", "ogg" => "audio/ogg", "flac" => "audio/flac", "json" => "application/json", _ => "application/octet-stream",
    }
}

pub struct Served {
    pub status: u16,
    pub mime: &'static str,
    pub body: Vec<u8>,
    pub total: u64,
    /// (first byte, last byte) when answering a Range request
    pub range: Option<(u64, u64)>,
}

/// Serves a whole small file, or one bounded chunk of a large one (HTTP Range), so video can seek.
pub fn serve(app: &App, path: &str, range: Option<&str>) -> Result<Served> {
    let p = PathBuf::from(path);
    if !p.is_absolute() || !allowed(app, &p) { return err("forbidden", "this file is not available to the app"); }
    let mut f = std::fs::File::open(&p)?;
    let total = f.metadata()?.len();
    let parsed = range.and_then(|r| r.strip_prefix("bytes=")).and_then(|r| { let mut it = r.splitn(2, '-'); let a = it.next()?.trim().parse::<u64>().ok()?; let b = it.next().and_then(|x| x.trim().parse::<u64>().ok()); Some((a, b)) });
    match parsed {
        Some((start, end)) if start < total => {
            let end = end.unwrap_or(total - 1).min(total - 1).min(start + CHUNK - 1);
            let mut body = vec![0u8; (end - start + 1) as usize];
            f.seek(SeekFrom::Start(start))?;
            f.read_exact(&mut body)?;
            Ok(Served { status: 206, mime: mime(&p), body, total, range: Some((start, end)) })
        }
        Some(_) => err("bad_range", "range outside the file"),
        None if total > CHUNK => {
            let mut body = vec![0u8; CHUNK as usize];
            f.read_exact(&mut body)?;
            Ok(Served { status: 206, mime: mime(&p), body, total, range: Some((0, CHUNK - 1)) })
        }
        None => { let mut body = Vec::with_capacity(total as usize); f.read_to_end(&mut body)?; Ok(Served { status: 200, mime: mime(&p), body, total, range: None }) }
    }
}
