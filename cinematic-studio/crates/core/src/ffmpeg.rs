//! FFmpeg / ffprobe invocation. Programs are started directly with an argument array: there is no
//! shell, so nothing a user types can become a command. Only these two programs are ever executed.
use crate::error::{err, AppError, Result};
use serde::Serialize;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

#[derive(Debug, Clone)]
pub struct Tools {
    pub ffmpeg: PathBuf,
    pub ffprobe: PathBuf,
}

fn exe(name: &str) -> String {
    if cfg!(windows) { format!("{name}.exe") } else { name.to_string() }
}

/// Looks in: the folder chosen in Settings, the folder bundled with the app, then PATH.
pub fn locate(configured: Option<&str>, bundled: Option<&Path>) -> Option<Tools> {
    let mut dirs: Vec<PathBuf> = Vec::new();
    if let Some(c) = configured.filter(|c| !c.trim().is_empty()) {
        let p = PathBuf::from(c);
        dirs.push(if p.is_file() { p.parent().map(Path::to_path_buf).unwrap_or(p) } else { p });
    }
    if let Some(b) = bundled {
        dirs.push(b.to_path_buf());
    }
    if let Some(path) = std::env::var_os("PATH") {
        dirs.extend(std::env::split_paths(&path));
    }
    for d in dirs {
        let (f, p) = (d.join(exe("ffmpeg")), d.join(exe("ffprobe")));
        if f.is_file() && p.is_file() {
            return Some(Tools { ffmpeg: f, ffprobe: p });
        }
    }
    None
}

fn command(program: &Path) -> Command {
    let mut c = Command::new(program);
    c.stdin(Stdio::null());
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        c.creation_flags(0x0800_0000); // CREATE_NO_WINDOW: no console flashes behind the app
    }
    c
}

pub fn run(program: &Path, args: &[String]) -> Result<(String, String)> {
    let out = command(program).args(args).output().map_err(|e| AppError::new("ffmpeg_missing", format!("could not start {}: {e}", program.display())))?;
    let (stdout, stderr) = (String::from_utf8_lossy(&out.stdout).to_string(), String::from_utf8_lossy(&out.stderr).to_string());
    if !out.status.success() {
        let tail: String = stderr.chars().rev().take(700).collect::<String>().chars().rev().collect();
        return err("ffmpeg_failed", tail);
    }
    Ok((stdout, stderr))
}

#[derive(Debug, Clone, Serialize, Default)]
pub struct MediaInfo {
    pub duration: Option<f64>,
    pub width: Option<i64>,
    pub height: Option<i64>,
    pub fps: Option<f64>,
    pub has_video: bool,
    pub has_audio: bool,
    pub video_codec: Option<String>,
    pub audio_codec: Option<String>,
    pub format: String,
}

pub fn probe(tools: &Tools, file: &Path) -> Result<MediaInfo> {
    let args: Vec<String> = ["-v", "error", "-print_format", "json", "-show_format", "-show_streams"].iter().map(|s| s.to_string()).chain([file.to_string_lossy().to_string()]).collect();
    let (out, _) = run(&tools.ffprobe, &args).map_err(|e| AppError::new("unreadable_media", e.message))?;
    let j: serde_json::Value = serde_json::from_str(&out)?;
    let streams = j["streams"].as_array().cloned().unwrap_or_default();
    let v = streams.iter().find(|s| s["codec_type"] == "video");
    let a = streams.iter().find(|s| s["codec_type"] == "audio");
    let num = |x: &serde_json::Value| x.as_str().and_then(|s| s.parse::<f64>().ok()).or_else(|| x.as_f64());
    let fps = v.and_then(|s| s["avg_frame_rate"].as_str()).and_then(|r| {
        let mut p = r.split('/');
        let (n, d) = (p.next()?.parse::<f64>().ok()?, p.next()?.parse::<f64>().ok()?);
        if d > 0.0 && n > 0.0 { Some(n / d) } else { None }
    });
    Ok(MediaInfo {
        duration: num(&j["format"]["duration"]).or_else(|| v.and_then(|s| num(&s["duration"]))),
        width: v.and_then(|s| s["width"].as_i64()),
        height: v.and_then(|s| s["height"].as_i64()),
        fps,
        has_video: v.is_some(),
        has_audio: a.is_some(),
        video_codec: v.and_then(|s| s["codec_name"].as_str()).map(String::from),
        audio_codec: a.and_then(|s| s["codec_name"].as_str()).map(String::from),
        format: j["format"]["format_name"].as_str().unwrap_or("").to_string(),
    })
}

/// A file counts as playable only if FFmpeg can actually decode it from start to end.
pub fn verify_playable(tools: &Tools, file: &Path) -> Result<MediaInfo> {
    let info = probe(tools, file)?;
    if !info.has_video {
        return err("not_a_video", "the file has no video stream");
    }
    let args: Vec<String> = ["-v", "error", "-xerror", "-i"].iter().map(|s| s.to_string()).chain([file.to_string_lossy().to_string(), "-f".into(), "null".into(), "-".into()]).collect();
    run(&tools.ffmpeg, &args).map_err(|e| AppError::new("corrupted_media", e.message))?;
    Ok(info)
}

pub fn thumbnail(tools: &Tools, src: &Path, dest: &Path, at_seconds: f64) -> Result<()> {
    if let Some(p) = dest.parent() {
        std::fs::create_dir_all(p)?;
    }
    let s = |x: &str| x.to_string();
    let args = vec![s("-y"), s("-v"), s("error"), s("-ss"), format!("{at_seconds:.2}"), s("-i"), src.to_string_lossy().to_string(), s("-frames:v"), s("1"), s("-vf"), s("scale=480:-2"), s("-q:v"), s("4"), s("-update"), s("1"), dest.to_string_lossy().to_string()];
    run(&tools.ffmpeg, &args).map(|_| ())
}
