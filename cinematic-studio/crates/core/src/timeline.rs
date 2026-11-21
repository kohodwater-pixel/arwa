//! Timeline and export. The timeline is plain JSON stored on the project:
//!
//! { "clips":  [{ "scene_id", "trim_in", "trim_out", "transition": { "kind": "cut"|"fade"|"dissolve"|"wipeleft"|"slideleft", "duration" } }],
//!   "audio":  [{ "id", "media_id", "track": "audio"|"voiceover"|"music", "start", "volume", "fade_in", "fade_out", "trim_in" }],
//!   "color":  { "brightness": -1..1, "contrast": 0..2, "saturation": 0..3 },
//!   "clip_audio_volume": 0..2,
//!   "output": { "preset": "source"|"1080p"|"720p", "fps": 24|25|30, "crf": 14..30 } }
//!
//! `plan` is a pure function from that JSON to an FFmpeg argument list, so it is unit-tested without
//! running FFmpeg. The four tracks are a deliberate minimum; adding a track type means adding one arm here.
use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::ffmpeg;
use crate::App;
use rusqlite::params;
use serde_json::{json, Value};
use std::io::{BufRead, BufReader};
use std::path::PathBuf;
use std::process::Stdio;

pub const TRANSITIONS: [&str; 5] = ["cut", "fade", "dissolve", "wipeleft", "slideleft"];
pub const TRACKS: [&str; 3] = ["audio", "voiceover", "music"];

#[derive(Debug, Clone)]
pub struct ClipSource {
    pub path: PathBuf,
    pub duration: f64,
    pub has_audio: bool,
    pub width: i64,
    pub height: i64,
}
#[derive(Debug, Clone)]
pub struct AudioSource {
    pub path: PathBuf,
    pub duration: f64,
}
#[derive(Debug)]
pub struct Plan {
    pub args: Vec<String>,
    pub duration: f64,
    pub width: i64,
    pub height: i64,
    pub fps: i64,
}

fn f(v: &Value, key: &str, default: f64) -> f64 {
    v.get(key).and_then(Value::as_f64).filter(|x| x.is_finite()).unwrap_or(default)
}
fn even(n: i64) -> i64 {
    (n / 2 * 2).max(2)
}
fn preset_size(preset: &str, aspect: &str, source: (i64, i64)) -> (i64, i64) {
    let long: f64 = match preset { "1080p" => 1920.0, "720p" => 1280.0, _ => return (even(source.0), even(source.1)) };
    let ratio: f64 = match aspect { "9:16" => 9.0 / 16.0, "1:1" => 1.0, "4:5" => 0.8, _ => 16.0 / 9.0 };
    let (w, h) = if ratio >= 1.0 { (long, long / ratio) } else { (long * ratio, long) };
    (even(w.round() as i64), even(h.round() as i64))
}

/// Default timeline: every finished scene in storyboard order, hard cuts, no extra audio.
pub fn default_timeline(scenes: &[Value]) -> Value {
    json!({ "clips": scenes.iter().filter(|s| s["status"] == "completed").map(|s| json!({ "scene_id": s["id"], "trim_in": 0.0, "trim_out": Value::Null, "transition": { "kind": "cut", "duration": 0.0 } })).collect::<Vec<_>>(),
        "audio": [], "color": { "brightness": 0.0, "contrast": 1.0, "saturation": 1.0 }, "clip_audio_volume": 1.0, "output": { "preset": "source", "fps": 24, "crf": 18 } })
}

pub fn plan(timeline: &Value, clips: &[ClipSource], audio: &[(Value, AudioSource)], aspect: &str, out: &str, title: &str) -> Result<Plan> {
    let items = timeline["clips"].as_array().cloned().unwrap_or_default();
    if items.is_empty() || items.len() != clips.len() { return err("empty_timeline", "the timeline has no finished scenes to export"); }
    let output = &timeline["output"];
    let fps = output["fps"].as_i64().filter(|x| [24, 25, 30, 50, 60].contains(x)).unwrap_or(24);
    let crf = output["crf"].as_i64().unwrap_or(18).clamp(14, 30);
    let (w, h) = preset_size(output["preset"].as_str().unwrap_or("source"), aspect, (clips[0].width, clips[0].height));
    let clip_vol = f(timeline, "clip_audio_volume", 1.0).clamp(0.0, 2.0);
    let with_clip_audio = clip_vol > 0.0 && clips.iter().any(|c| c.has_audio);

    let mut args: Vec<String> = vec!["-y".into(), "-v".into(), "error".into(), "-progress".into(), "pipe:1".into(), "-nostats".into()];
    for c in clips { args.push("-i".into()); args.push(c.path.to_string_lossy().to_string()); }
    for (_, a) in audio { args.push("-i".into()); args.push(a.path.to_string_lossy().to_string()); }

    let mut fc: Vec<String> = vec![];
    let mut durations: Vec<f64> = vec![];
    for (i, (item, src)) in items.iter().zip(clips).enumerate() {
        let tin = f(item, "trim_in", 0.0).clamp(0.0, (src.duration - 0.1).max(0.0));
        let tout = item["trim_out"].as_f64().unwrap_or(src.duration).clamp(tin + 0.1, src.duration.max(tin + 0.1));
        let d = tout - tin;
        durations.push(d);
        fc.push(format!("[{i}:v]trim=start={tin:.3}:end={tout:.3},setpts=PTS-STARTPTS,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},format=yuv420p,setsar=1[v{i}]"));
        if with_clip_audio {
            if src.has_audio {
                fc.push(format!("[{i}:a]atrim=start={tin:.3}:end={tout:.3},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={clip_vol:.3},apad=whole_dur={d:.3}[a{i}]"));
            } else {
                fc.push(format!("anullsrc=r=48000:cl=stereo,atrim=0:{d:.3}[a{i}]"));
            }
        }
    }
    // join clips left to right; a transition overlaps its two clips, so it shortens the film by its length
    let (mut vlabel, mut alabel, mut total) = ("v0".to_string(), "a0".to_string(), durations[0]);
    for i in 1..items.len() {
        let tr = &items[i]["transition"];
        let kind = tr["kind"].as_str().filter(|k| TRANSITIONS.contains(k)).unwrap_or("cut");
        let t = if kind == "cut" { 0.0 } else { f(tr, "duration", 0.5).clamp(0.1, (durations[i - 1].min(durations[i]) / 2.0).max(0.1)) };
        let (vn, an) = (format!("x{i}"), format!("y{i}"));
        if t == 0.0 {
            fc.push(format!("[{vlabel}][v{i}]concat=n=2:v=1:a=0[{vn}]"));
            if with_clip_audio { fc.push(format!("[{alabel}][a{i}]concat=n=2:v=0:a=1[{an}]")); }
            total += durations[i];
        } else {
            fc.push(format!("[{vlabel}][v{i}]xfade=transition={kind}:duration={t:.3}:offset={:.3}[{vn}]", total - t));
            if with_clip_audio { fc.push(format!("[{alabel}][a{i}]acrossfade=d={t:.3}[{an}]")); }
            total += durations[i] - t;
        }
        vlabel = vn;
        alabel = an;
    }
    let color = &timeline["color"];
    let (b, c, s) = (f(color, "brightness", 0.0).clamp(-1.0, 1.0), f(color, "contrast", 1.0).clamp(0.0, 2.0), f(color, "saturation", 1.0).clamp(0.0, 3.0));
    if b != 0.0 || c != 1.0 || s != 1.0 {
        fc.push(format!("[{vlabel}]eq=brightness={b:.3}:contrast={c:.3}:saturation={s:.3}[vout]"));
    } else {
        fc.push(format!("[{vlabel}]null[vout]"));
    }
    let with_audio = with_clip_audio || !audio.is_empty();
    if with_audio {
        let mut mix: Vec<String> = vec![];
        if with_clip_audio { mix.push(format!("[{alabel}]")); } else { fc.push(format!("anullsrc=r=48000:cl=stereo,atrim=0:{total:.3}[abase]")); mix.push("[abase]".into()); }
        for (k, (item, src)) in audio.iter().enumerate() {
            let idx = clips.len() + k;
            let start = f(item, "start", 0.0).clamp(0.0, total);
            let tin = f(item, "trim_in", 0.0).clamp(0.0, (src.duration - 0.05).max(0.0));
            let len = (src.duration - tin).min(total - start).max(0.05);
            let vol = f(item, "volume", 1.0).clamp(0.0, 2.0);
            let (fi, fo) = (f(item, "fade_in", 0.0).clamp(0.0, len / 2.0), f(item, "fade_out", 0.0).clamp(0.0, len / 2.0));
            let mut chain = format!("[{idx}:a]atrim=start={tin:.3}:duration={len:.3},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={vol:.3}");
            if fi > 0.0 { chain.push_str(&format!(",afade=t=in:st=0:d={fi:.3}")); }
            if fo > 0.0 { chain.push_str(&format!(",afade=t=out:st={:.3}:d={fo:.3}", len - fo)); }
            if start > 0.0 { chain.push_str(&format!(",adelay={}:all=1", (start * 1000.0).round() as i64)); }
            chain.push_str(&format!("[t{k}]"));
            fc.push(chain);
            mix.push(format!("[t{k}]"));
        }
        if mix.len() > 1 {
            fc.push(format!("{}amix=inputs={}:normalize=0:duration=first:dropout_transition=0,alimiter=limit=0.95[aout]", mix.join(""), mix.len()));
        } else {
            fc.push(format!("{}anull[aout]", mix[0]));
        }
    }
    args.extend(["-filter_complex".into(), fc.join(";"), "-map".into(), "[vout]".into()]);
    if with_audio { args.extend(["-map".into(), "[aout]".into(), "-c:a".into(), "aac".into(), "-b:a".into(), "192k".into()]); }
    args.extend(["-t".into(), format!("{total:.3}"), "-c:v".into(), "libx264".into(), "-preset".into(), "medium".into(), "-crf".into(), crf.to_string(), "-pix_fmt".into(), "yuv420p".into(),
        "-movflags".into(), "+faststart".into(), "-metadata".into(), format!("title={}", title.replace(['\n', '\r'], " ")), "-metadata".into(), "encoder=Cinematic Studio".into(), out.to_string()]);
    Ok(Plan { args, duration: total, width: w, height: h, fps })
}

/// Renders the project's timeline to an MP4 in its exports folder, verifies the result, writes the
/// metadata sidecar and records the export. Returns Null when canceled.
pub fn render(app: &App, project_id: &str, options: &Value, mut on_progress: impl FnMut(f64), is_canceled: impl Fn() -> bool) -> Result<Value> {
    let tools = app.tools()?;
    let lib = app.lib();
    let (project, scenes, media_rows) = {
        let conn = app.db.lock().unwrap();
        (row(&conn, "SELECT * FROM projects WHERE id = ?1", &[&project_id])?.ok_or_else(|| AppError::new("project_not_found", project_id.to_string()))?,
         rows(&conn, "SELECT * FROM scenes WHERE project_id = ?1 ORDER BY position", &[&project_id])?,
         rows(&conn, "SELECT * FROM media WHERE kind = 'audio'", &[])?)
    };
    let mut timeline: Value = project["timeline_json"].as_str().and_then(|s| serde_json::from_str(s).ok()).filter(|t: &Value| t["clips"].as_array().map(|c| !c.is_empty()).unwrap_or(false)).unwrap_or_else(|| default_timeline(&scenes));
    if let Some(o) = options.get("output") { timeline["output"] = o.clone(); }
    // drop clips whose scene no longer has a finished video; refuse if nothing is left
    let mut clips = vec![];
    let mut kept = vec![];
    for item in timeline["clips"].as_array().cloned().unwrap_or_default() {
        let Some(scene) = scenes.iter().find(|s| s["id"] == item["scene_id"] && s["status"] == "completed") else { continue };
        let path = lib.resolve(scene["video_path"].as_str().unwrap_or(""))?;
        let info = ffmpeg::probe(&tools, &path).map_err(|_| AppError::new("missing_scene_video", format!("the video of scene {} is missing or unreadable", scene["position"].as_i64().unwrap_or(0) + 1)))?;
        clips.push(ClipSource { path, duration: info.duration.unwrap_or(0.0), has_audio: info.has_audio, width: info.width.unwrap_or(1280), height: info.height.unwrap_or(720) });
        kept.push(item);
    }
    timeline["clips"] = json!(kept);
    let mut audio = vec![];
    for item in timeline["audio"].as_array().cloned().unwrap_or_default() {
        let Some(m) = media_rows.iter().find(|m| m["id"] == item["media_id"]) else { return err("missing_audio", "an audio item on the timeline is no longer in the media library") };
        let path = PathBuf::from(m["path"].as_str().unwrap_or(""));
        if !path.is_file() { return err("missing_audio", format!("audio file not found: {}", m["name"].as_str().unwrap_or(""))); }
        audio.push((item, AudioSource { path, duration: m["duration"].as_f64().unwrap_or(0.0) }));
    }
    let name = project["name"].as_str().unwrap_or("project");
    let rel = format!("{}/exports/{}-{}.mp4", project["folder"].as_str().unwrap_or(""), crate::paths::slug(name, 40), chrono::Utc::now().format("%Y%m%d-%H%M%S"));
    let out = lib.resolve(&rel)?;
    std::fs::create_dir_all(out.parent().unwrap())?;
    let plan = plan(&timeline, &clips, &audio, project["aspect"].as_str().unwrap_or("16:9"), &out.to_string_lossy(), name)?;

    let mut cmd = std::process::Command::new(&tools.ffmpeg);
    cmd.args(&plan.args).stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::piped());
    #[cfg(windows)]
    { use std::os::windows::process::CommandExt; cmd.creation_flags(0x0800_0000); }
    let mut child = cmd.spawn().map_err(|e| AppError::new("ffmpeg_missing", e.to_string()))?;
    let stderr = child.stderr.take();
    let err_thread = std::thread::spawn(move || { let mut s = String::new(); if let Some(mut e) = stderr { let _ = std::io::Read::read_to_string(&mut e, &mut s); } s });
    if let Some(stdout) = child.stdout.take() {
        for line in BufReader::new(stdout).lines().map_while(|l| l.ok()) {
            if let Some(us) = line.strip_prefix("out_time_us=").or_else(|| line.strip_prefix("out_time_ms=")).and_then(|v| v.trim().parse::<f64>().ok()) {
                on_progress((us / 1_000_000.0 / plan.duration).clamp(0.0, 0.99));
            }
            if is_canceled() { let _ = child.kill(); let _ = child.wait(); let _ = std::fs::remove_file(&out); return Ok(Value::Null); }
        }
    }
    let status = child.wait()?;
    let stderr_text = err_thread.join().unwrap_or_default();
    let record = |status: &str, info: Option<&ffmpeg::MediaInfo>, error: Option<&str>| -> Result<Value> {
        let conn = app.db.lock().unwrap();
        let id = new_id();
        let size = std::fs::metadata(&out).map(|m| m.len() as i64).ok();
        let meta = json!({ "project": name, "exported_at": now(), "duration": plan.duration, "width": plan.width, "height": plan.height, "fps": plan.fps, "timeline": timeline, "model": project["model_id"],
            "scenes": scenes.iter().map(|s| json!({ "position": s["position"], "title": s["title"], "duration": s["duration"], "prompt": s["prompt"], "negative_prompt": s["negative_prompt"], "camera_move": s["camera_move"], "seed": s["seed"] })).collect::<Vec<_>>() });
        conn.execute("INSERT INTO exports (id, project_id, path, preset, width, height, duration, size, status, metadata_json, error, created_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12)",
            params![id, project_id, rel, timeline["output"]["preset"].as_str().unwrap_or("source"), plan.width, plan.height, info.and_then(|i| i.duration), size, status, meta.to_string(), error, now()])?;
        if status == "completed" {
            std::fs::write(out.with_extension("json"), serde_json::to_vec_pretty(&meta)?)?;
            conn.execute("UPDATE projects SET status = 'exported', updated_at = ?1 WHERE id = ?2", params![now(), project_id])?;
            db::audit(&conn, "info", "export.completed", &rel);
        }
        Ok(json!({ "id": id, "path": out.to_string_lossy(), "relative_path": rel, "duration": info.and_then(|i| i.duration), "width": plan.width, "height": plan.height, "size": size }))
    };
    if !status.success() {
        let tail: String = stderr_text.chars().rev().take(600).collect::<String>().chars().rev().collect();
        let _ = std::fs::remove_file(&out);
        let _ = record("failed", None, Some(&tail));
        return err("export_failed", tail);
    }
    // an export counts only if the written file decodes from start to end
    match ffmpeg::verify_playable(&tools, &out) {
        Ok(info) => { on_progress(1.0); record("completed", Some(&info), None) }
        Err(e) => { let _ = record("failed", None, Some(&e.message)); err("export_failed", format!("the exported file does not play: {}", e.message)) }
    }
}
