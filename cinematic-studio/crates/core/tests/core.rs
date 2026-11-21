mod support;
use serde_json::{json, Value};
use std::time::Duration;
use support::*;

fn scene(title: &str, d: i64) -> Value {
    json!({ "title": title, "duration": d, "description": "desc", "prompt": format!("Wide shot. {title}."), "camera_move": "dolly_in", "shot_size": "wide", "role": "establish" })
}
fn project(env: &Env, name: &str) -> String {
    let p = env.call("project_create", json!({ "name": name, "description": "A test film", "video_type": "commercial", "aspect": "16:9", "duration": 10 }));
    let id = p["id"].as_str().unwrap().to_string();
    env.call("storyboard_replace", json!({ "project_id": id, "scenes": [scene("Opening", 3), scene("Detail", 4), scene("Closing", 3)] }));
    id
}
/// Marks every scene as generated, with a real playable file in the project folder.
fn fill_videos(env: &Env, id: &str, with_audio: bool) {
    let p = env.call("project_get", json!({ "id": id }));
    let folder = p["folder"].as_str().unwrap();
    for s in p["scenes"].as_array().unwrap() {
        let rel = format!("{folder}/scenes/s{}.mp4", s["position"]);
        make_video(&env.app.lib().resolve(&rel).unwrap(), s["duration"].as_f64().unwrap() + 0.5, "640x360", with_audio);
        env.app.db.lock().unwrap().execute("UPDATE scenes SET status = 'completed', video_path = ?1, video_duration = ?2 WHERE id = ?3", rusqlite::params![rel, s["duration"].as_f64().unwrap() + 0.5, s["id"].as_str()]).unwrap();
    }
}
fn wait_for(env: &Env, what: impl Fn(&Value) -> bool) -> Value {
    for _ in 0..200 {
        let jobs = env.call("jobs_list", json!({}));
        if what(&jobs) { return jobs; }
        std::thread::sleep(Duration::from_millis(100));
    }
    panic!("timed out; jobs: {}", env.call("jobs_list", json!({})));
}

#[test]
fn library_layout_and_startup() {
    let env = Env::new();
    let st = env.call("app_status", json!({}));
    for d in ["Projects", "Assets", "Models", "Cache", "Logs", "Backups"] { assert!(env.app.lib().dir(d).is_dir(), "{d}"); }
    assert_eq!(st["recovered"], false);
    assert!(st["ffmpeg"].is_object(), "ffmpeg located");
    assert_eq!(st["budget"]["limit_sar"], 1000.0);
}

#[test]
fn project_saved_reopened_after_restart() {
    let mut env = Env::new();
    let id = project(&env, "فيلم العطر / Perfume: film?");
    let p = env.call("project_get", json!({ "id": id }));
    assert_eq!(p["scenes"].as_array().unwrap().len(), 3);
    assert_eq!(p["duration"], 10);
    let folder = env.app.lib().resolve(p["folder"].as_str().unwrap()).unwrap();
    assert!(folder.join("project.json").is_file(), "snapshot written beside the media");
    assert!(!p["folder"].as_str().unwrap().contains(['?', ':', '/'].as_ref()) || p["folder"].as_str().unwrap().starts_with("Projects/"));
    env.call("project_update", json!({ "id": id, "patch": { "name": "Perfume film", "director": { "lighting": "Golden Hour" } } }));
    env.restart(true);
    let again = env.call("project_get", json!({ "id": id }));
    assert_eq!(again["name"], "Perfume film");
    assert_eq!(again["director"]["lighting"], "Golden Hour");
    assert_eq!(again["scenes"][1]["title"], "Detail");
    assert_eq!(env.call("app_status", json!({}))["recovered"], false);
    assert_eq!(env.call("app_status", json!({}))["last_project"], id);
}

#[test]
fn crash_recovery_resumes_inflight_jobs() {
    let mut env = Env::new();
    let id = project(&env, "Crash");
    env.call("generate", json!({ "project_id": id }));
    env.app.db.lock().unwrap().execute("UPDATE jobs SET status = 'running', remote_id = 'abc' WHERE rowid = (SELECT MIN(rowid) FROM jobs)", []).unwrap();
    env.restart(false); // no clean shutdown
    let st = env.call("app_status", json!({}));
    assert_eq!(st["recovered"], true);
    assert_eq!(st["recovered_jobs"], 1);
    let jobs = env.call("jobs_list", json!({}));
    let resumed = jobs.as_array().unwrap().iter().find(|j| j["remote_id"] == "abc").unwrap();
    assert_eq!(resumed["status"], "queued");          // back in the queue…
    assert_eq!(resumed["remote_id"], "abc");          // …and still attached to the server's job: not submitted twice
    assert_eq!(env.call("project_get", json!({ "id": id }))["scenes"].as_array().unwrap().len(), 3, "no project data lost");
}

#[test]
fn storyboard_editing() {
    let env = Env::new();
    let id = project(&env, "Edit");
    let p = env.call("project_get", json!({ "id": id }));
    let ids: Vec<String> = p["scenes"].as_array().unwrap().iter().map(|s| s["id"].as_str().unwrap().to_string()).collect();
    let p = env.call("scene_update", json!({ "id": ids[1], "patch": { "duration": 5, "camera_move": "orbit", "prompt": "Macro shot of the bottle." } }));
    assert_eq!(p["scenes"][1]["camera_move"], "orbit");
    assert_eq!(p["duration"], 11, "project duration follows the scenes");
    let p = env.call("scenes_reorder", json!({ "project_id": id, "order": [ids[2], ids[0], ids[1]] }));
    assert_eq!(p["scenes"][0]["title"], "Closing");
    assert_eq!(env.fail("scenes_reorder", json!({ "project_id": id, "order": [ids[0]] })), "bad_request");
    let p = env.call("scene_add", json!({ "project_id": id, "scene": scene("Extra", 2), "position": 1 }));
    assert_eq!(p["scenes"].as_array().unwrap().iter().map(|s| s["title"].as_str().unwrap()).collect::<Vec<_>>(), ["Closing", "Extra", "Opening", "Detail"]);
    assert!(p["scenes"].as_array().unwrap().iter().enumerate().all(|(i, s)| s["position"] == i as i64));
    let extra = p["scenes"][1]["id"].as_str().unwrap().to_string();
    assert_eq!(env.call("scene_delete", json!({ "id": extra }))["scenes"].as_array().unwrap().len(), 3);
    // editing a generated scene keeps the old take aside and marks the scene stale
    fill_videos(&env, &id, false);
    let before = env.call("project_get", json!({ "id": id }));
    let old = env.app.lib().resolve(before["scenes"][0]["video_path"].as_str().unwrap()).unwrap();
    let after = env.call("scene_update", json!({ "id": before["scenes"][0]["id"], "patch": { "prompt": "A different shot." } }));
    assert_eq!(after["scenes"][0]["status"], "pending");
    assert!(!old.exists() && old.parent().unwrap().join("_replaced").read_dir().unwrap().count() == 1, "old take moved aside, not deleted");
}

#[test]
fn duplicate_backup_export_import_delete() {
    let env = Env::new();
    let id = project(&env, "Round trip");
    fill_videos(&env, &id, false);
    let copy = env.call("project_duplicate", json!({ "id": id }));
    assert_ne!(copy["id"], id);
    assert_eq!(copy["scenes"][0]["status"], "completed");
    assert!(env.app.lib().resolve(copy["scenes"][0]["video_path"].as_str().unwrap()).unwrap().is_file(), "the copy has its own files");
    let b = env.call("project_backup", json!({ "id": id }));
    assert!(std::path::Path::new(b["path"].as_str().unwrap()).is_file() && b["files"].as_i64().unwrap() >= 4);
    let zip = env.file("out.zip");
    env.call("project_export_archive", json!({ "id": id, "dest": zip.to_string_lossy() }));
    assert_eq!(env.fail("project_export_archive", json!({ "id": id, "dest": "relative.zip" })), "bad_path");
    let imported = env.call("project_import_archive", json!({ "path": zip.to_string_lossy() }));
    assert_eq!(imported["name"], "Round trip");
    assert_eq!(imported["scenes"].as_array().unwrap().len(), 3);
    assert_eq!(imported["scenes"][2]["status"], "completed");
    assert!(env.app.lib().resolve(imported["scenes"][2]["video_path"].as_str().unwrap()).unwrap().is_file());
    let folder = env.app.lib().resolve(copy["folder"].as_str().unwrap()).unwrap();
    let d = env.call("project_delete", json!({ "id": copy["id"] }));
    assert!(!folder.exists() && std::path::Path::new(d["kept_at"].as_str().unwrap()).is_dir(), "deleted project is kept under Backups/Deleted");
    assert_eq!(env.call("projects_list", json!({})).as_array().unwrap().len(), 2);
}

#[test]
fn import_refuses_unsafe_archives() {
    let env = Env::new();
    // an archive whose entry tries to leave the project folder
    let evil = env.file("evil.zip");
    {
        use std::io::Write;
        let mut z = zip::ZipWriter::new(std::fs::File::create(&evil).unwrap());
        let o = zip::write::SimpleFileOptions::default();
        z.start_file("project.json", o).unwrap();
        z.write_all(json!({ "format": "cinematic-studio-project", "project": { "name": "x", "folder": "Projects/x" }, "scenes": [] }).to_string().as_bytes()).unwrap();
        z.start_file("../../escaped.txt", o).unwrap();
        z.write_all(b"owned").unwrap();
        z.finish().unwrap();
    }
    assert_eq!(env.fail("project_import_archive", json!({ "path": evil.to_string_lossy() })), "unsafe_archive");
    assert!(!env.dir.path().join("escaped.txt").exists() && !env.app.lib().root.join("escaped.txt").exists());
    assert_eq!(env.call("projects_list", json!({})).as_array().unwrap().len(), 0, "nothing was created");
    let not = env.file("not.zip");
    std::fs::write(&not, b"hello").unwrap();
    assert_eq!(env.fail("project_import_archive", json!({ "path": not.to_string_lossy() })), "archive");
}

#[test]
fn integrity_detects_missing_and_corrupted_media() {
    let env = Env::new();
    let id = project(&env, "Integrity");
    fill_videos(&env, &id, false);
    let p = env.call("project_get", json!({ "id": id }));
    let path = |i: usize| env.app.lib().resolve(p["scenes"][i]["video_path"].as_str().unwrap()).unwrap();
    std::fs::remove_file(path(0)).unwrap();
    std::fs::write(path(1), vec![0u8; 3000]).unwrap();
    let r = env.call("project_integrity", json!({ "id": id }));
    assert_eq!(r["missing_videos"].as_array().unwrap().len(), 1);
    assert_eq!(r["corrupted_videos"].as_array().unwrap().len(), 1);
    assert_eq!(r["corrupted_videos"][0]["scene"], 2);
    assert_eq!(env.call("project_get", json!({ "id": id }))["scenes"][0]["status"], "pending", "a scene whose file is gone must be generated again");
}

#[test]
fn media_library() {
    let env = Env::new();
    let (img, vid, aud, fake) = (env.file("ref.png"), env.file("clip.mp4"), env.file("music.wav"), env.file("fake.png"));
    make_image(&img); make_video(&vid, 2.0, "320x240", true); make_audio(&aud, 3.0);
    std::fs::write(&fake, b"this is not an image at all").unwrap();
    std::fs::copy(&img, env.file("copy.png")).unwrap();
    let paths = [&img, &vid, &aud, &fake, &env.file("copy.png"), &env.file("nope.mp4")].iter().map(|p| p.to_string_lossy().to_string()).collect::<Vec<_>>();
    let r = env.call("media_import", json!({ "paths": paths, "folder": "Shoot A" }));
    let r = r.as_array().unwrap();
    assert_eq!(r.iter().filter(|x| x["ok"] == true).count(), 4);
    assert_eq!(r[3]["error"], "unsupported_type", "type comes from the file content, not its name");
    assert_eq!(r[4]["duplicate"], true, "same content is detected as a duplicate");
    assert_eq!(r[5]["error"], "file_missing");
    assert_eq!(r[1]["media"]["kind"], "video");
    assert!(r[1]["media"]["duration"].as_f64().unwrap() > 1.5 && r[1]["media"]["width"] == 320);
    assert!(env.app.lib().resolve(r[0]["media"]["thumb_path"].as_str().unwrap()).unwrap().is_file(), "thumbnail in Cache");
    assert!(img.is_file(), "the original stays where it is");
    let l = env.call("media_list", json!({ "kind": "audio" }));
    assert_eq!(l["items"].as_array().unwrap().len(), 1);
    assert_eq!(env.call("media_list", json!({ "q": "CLIP" }))["items"].as_array().unwrap().len(), 1);
    assert_eq!(l["folders"][0]["folder"], "Shoot A");
    std::fs::remove_file(&vid).unwrap();
    assert_eq!(env.call("media_verify", json!({}))["missing"], 1);
    let id = r[0]["media"]["id"].as_str().unwrap();
    env.call("media_remove", json!({ "id": id }));
    assert!(img.is_file(), "removing a library entry never deletes the user's file");
}

#[test]
fn security_rules() {
    let env = Env::new();
    assert_eq!(env.fail("no_such_command", json!({})), "unknown_command");
    assert_eq!(env.fail("setting_set", json!({ "key": "comfy_url", "value": "http://203.0.113.10:8188" })), "insecure_url");
    assert_eq!(env.fail("setting_set", json!({ "key": "comfy_url", "value": "https://user:pw@host" })), "bad_url");
    env.call("setting_set", json!({ "key": "comfy_url", "value": "https://gpu.example.com" }));
    env.call("setting_set", json!({ "key": "comfy_url", "value": "http://127.0.0.1:8188" }));
    assert_eq!(env.fail("setting_set", json!({ "key": "gpu_api_base", "value": "http://evil" })), "unknown_setting");
    assert_eq!(env.fail("secret_set", json!({ "name": "anything", "value": "x" })), "bad_secret_name");
    // secrets go to the secret store and never appear in status, settings or the database
    env.call("secret_set", json!({ "name": "gpu_api_key", "value": "SECRET-KEY-123456" }));
    let st = env.call("app_status", json!({}));
    assert_eq!(st["gpu_key_stored"], true);
    assert!(!st.to_string().contains("SECRET-KEY"));
    let db_bytes = std::fs::read(env.app.lib().db_file()).unwrap();
    assert!(!String::from_utf8_lossy(&db_bytes).contains("SECRET-KEY"), "the key is not in SQLite");
    // file access: library files yes, the database no, anything else no
    let outside = env.file("private.txt");
    std::fs::write(&outside, b"private").unwrap();
    assert!(!studio_core::files::allowed(&env.app, &outside));
    assert!(!studio_core::files::allowed(&env.app, &env.app.lib().db_file()));
    assert!(studio_core::files::serve(&env.app, "../../etc/passwd", None).is_err());
    let id = project(&env, "Files");
    let snap = env.app.lib().resolve(env.call("project_get", json!({ "id": id }))["folder"].as_str().unwrap()).unwrap().join("project.json");
    assert!(studio_core::files::allowed(&env.app, &snap));
    assert!(studio_core::paths::safe_join(&env.app.lib().root, "../x").is_err() && studio_core::paths::safe_join(&env.app.lib().root, "/etc/passwd").is_err());
    assert_eq!(env.fail("reveal", json!({ "path": env.dir.path().to_string_lossy() })), "forbidden");
}

#[test]
fn generation_end_to_end_against_protocol_double() {
    let env = Env::new();
    let sample = env.file("server-output.mp4");
    make_video(&sample, 3.0, "1280x704", false);
    let (url, comfy) = fake_comfy(sample);
    comfy.lock().unwrap().token = Some("tok-abcdef".into());
    let id = project(&env, "Generate");

    // not configured → the job waits; nothing is faked
    env.call("generate", json!({ "project_id": id, "scene_ids": [env.call("project_get", json!({ "id": id }))["scenes"][0]["id"]] }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "blocked");
    assert_eq!(j[0]["blocked_reason"], "comfy_not_configured");
    assert_eq!(env.call("comfy_status", json!({}))["configured"], false);

    // wrong token → refused by the server, reported as such
    env.call("setting_set", json!({ "key": "comfy_url", "value": url }));
    env.call("secret_set", json!({ "name": "comfy_token", "value": "wrong-token" }));
    let st = env.call("comfy_status", json!({}));
    assert_eq!(st["connected"], false);
    assert_eq!(st["error"]["code"], "comfy_auth");

    env.call("secret_set", json!({ "name": "comfy_token", "value": "tok-abcdef" }));
    let st = env.call("comfy_status", json!({}));
    assert_eq!(st["connected"], true);
    assert_eq!(st["system"]["device"], "cuda:0 TEST GPU");
    assert_eq!(st["models"][0]["ready"], true);
    assert_eq!(st["models"][1]["ready"], false, "the 14B files are not on this server, and the app says so");

    studio_core::jobs::tick(&env.app); // the blocked job now runs
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "succeeded", "{}", j[0]);
    let p = env.call("project_get", json!({ "id": id }));
    let s0 = &p["scenes"][0];
    assert_eq!(s0["status"], "completed");
    let file = env.app.lib().resolve(s0["video_path"].as_str().unwrap()).unwrap();
    assert!(file.is_file() && (s0["video_duration"].as_f64().unwrap() - 3.0).abs() < 0.2, "downloaded and probed");
    assert!(env.app.lib().resolve(s0["preview_path"].as_str().unwrap()).unwrap().is_file(), "preview image made");
    // what was sent: the official graph, the scene's prompt, the model's frame rule
    let st = comfy.lock().unwrap();
    let wf = &st.prompts[0].1;
    assert_eq!(wf["unet"]["inputs"]["unet_name"], "wan2.2_ti2v_5B_fp16.safetensors");
    assert_eq!(wf["pos"]["inputs"]["text"], "Wide shot. Opening.");
    assert_eq!(wf["latent"]["inputs"]["length"], 73, "3 s at 24 fps → 4n+1 frames");
    assert_eq!((wf["latent"]["inputs"]["width"].as_i64(), wf["latent"]["inputs"]["height"].as_i64()), (Some(1280), Some(704)));
    assert_eq!(wf["sample"]["inputs"]["steps"], 20);
    assert!(st.ws_connections >= 1, "progress was followed over the WebSocket");
    assert!(j[0]["progress"].as_f64().unwrap() >= 0.99);
}

#[test]
fn generation_failures_are_reported_not_hidden() {
    let env = Env::new();
    let sample = env.file("out.mp4");
    make_video(&sample, 3.0, "640x360", false);
    let (url, comfy) = fake_comfy(sample);
    env.call("setting_set", json!({ "key": "comfy_url", "value": url }));
    let id = project(&env, "Failures");
    let scenes: Vec<String> = env.call("project_get", json!({ "id": id }))["scenes"].as_array().unwrap().iter().map(|s| s["id"].as_str().unwrap().to_string()).collect();

    // 1) a model file is missing on the server → clear failure before anything is submitted
    comfy.lock().unwrap().missing_files = vec!["wan2.2_vae.safetensors".into()];
    env.call("generate", json!({ "project_id": id, "scene_ids": [scenes[0]] }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "failed");
    assert!(j[0]["error"].as_str().unwrap().starts_with("model_not_ready"));
    assert_eq!(comfy.lock().unwrap().prompts.len(), 0, "nothing was submitted");
    comfy.lock().unwrap().missing_files.clear();

    // 2) the server reports an execution error
    comfy.lock().unwrap().fail_generation = true;
    env.call("job_retry", json!({ "id": j[0]["id"] }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "failed");
    assert!(j[0]["error"].as_str().unwrap().contains("CUDA out of memory"));
    assert_eq!(env.call("project_get", json!({ "id": id }))["scenes"][0]["status"], "failed");
    comfy.lock().unwrap().fail_generation = false;

    // 3) the server says success but the file does not play → not accepted as a result
    comfy.lock().unwrap().serve_broken_video = true;
    env.call("job_retry", json!({ "id": j[0]["id"] }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "failed");
    assert!(j[0]["error"].as_str().unwrap().starts_with("invalid_output"), "{}", j[0]["error"]);
    assert!(env.call("project_get", json!({ "id": id }))["scenes"][0]["video_path"].is_null());
    comfy.lock().unwrap().serve_broken_video = false;

    // 4) retry now succeeds
    env.call("job_retry", json!({ "id": j[0]["id"] }));
    studio_core::jobs::tick(&env.app);
    assert_eq!(env.call("jobs_list", json!({}))[0]["status"], "succeeded");

    // 5) the server becomes unreachable (GPU disconnect): the next job waits instead of failing
    env.call("setting_set", json!({ "key": "comfy_url", "value": "http://127.0.0.1:9" }));
    env.call("generate", json!({ "project_id": id, "scene_ids": [scenes[1]] }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    let waiting = j.as_array().unwrap().iter().find(|x| x["scene_id"] == scenes[1].as_str()).unwrap();
    assert_eq!(waiting["status"], "blocked");
    assert_eq!(waiting["blocked_reason"], "comfy_unreachable");
}

#[test]
fn cancel_a_running_generation() {
    let env = Env::new();
    let sample = env.file("out.mp4");
    make_video(&sample, 2.0, "640x360", false);
    let (url, comfy) = fake_comfy(sample);
    comfy.lock().unwrap().polls_until_done = 1000; // never finishes on its own
    env.call("setting_set", json!({ "key": "comfy_url", "value": url }));
    let id = project(&env, "Cancel");
    let sid = env.call("project_get", json!({ "id": id }))["scenes"][0]["id"].as_str().unwrap().to_string();
    env.call("generate", json!({ "project_id": id, "scene_ids": [sid] }));
    let app = env.app.clone();
    let worker = std::thread::spawn(move || { studio_core::jobs::tick(&app); });
    let jobs = wait_for(&env, |j| j[0]["status"] == "running");
    env.call("job_cancel", json!({ "id": jobs[0]["id"] }));
    worker.join().unwrap();
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "canceled");
    assert_eq!(comfy.lock().unwrap().canceled.len(), 1, "the server was told to stop");
    assert_eq!(env.call("project_get", json!({ "id": id }))["scenes"][0]["status"], "pending");
    assert_eq!(env.fail("job_cancel", json!({ "id": j[0]["id"] })), "job_not_active");
}

#[test]
fn gpu_approval_budget_and_idle_shutdown() {
    let env = Env::new();
    let (url, gpu) = fake_gpu();
    env.call("setting_set", json!({ "key": "gpu_provider", "value": "runpod" }));
    env.call("setting_set", json!({ "key": "gpu_instance_id", "value": "pod123" }));
    env.set("gpu_api_base", &url);
    assert_eq!(env.call("gpu_status", json!({}))["configured"], false, "no key stored yet");
    env.call("secret_set", json!({ "name": "gpu_api_key", "value": "test-gpu-key" }));
    let st = env.call("gpu_status", json!({}));
    assert_eq!(st["instance"]["state"], "stopped");
    assert_eq!(st["instance"]["rate_usd_per_hour"], 0.5);

    // no approval → no start, and the provider is never called
    assert_eq!(env.fail("gpu_start", json!({})), "approval_required");
    assert_eq!(env.fail("gpu_start", json!({ "approved": true, "approved_by": "" })), "approval_required");
    assert_eq!(gpu.lock().unwrap().starts, 0);
    env.call("gpu_start", json!({ "approved": true, "approved_by": "Khalid" }));
    assert_eq!(gpu.lock().unwrap().starts, 1);
    let st = env.call("gpu_status", json!({}));
    assert_eq!(st["instance"]["state"], "running");
    assert_eq!(st["session"]["approved_by"], "Khalid");

    // budget thresholds: 1000 SAR, sessions at 0.5 USD/h × 3.75 = 1.875 SAR/h
    let add_hours = |h: f64| { env.app.db.lock().unwrap().execute("INSERT INTO gpu_sessions (id, provider, instance_id, started_at, stopped_at, rate_usd_per_hour, usd_to_sar, approved_by) VALUES (?1,'runpod','pod123',?2,?3,0.5,3.75,'test')",
        rusqlite::params![uuid::Uuid::new_v4().to_string(), (chrono::Utc::now() - chrono::Duration::minutes(1)).to_rfc3339(), (chrono::Utc::now() - chrono::Duration::minutes(1) + chrono::Duration::milliseconds((h * 3_600_000.0) as i64)).to_rfc3339()]).unwrap(); };
    // sessions are dated inside the current month even on the 1st: start one minute ago and run "forward" on paper
    add_hours(380.0);
    assert_eq!(env.call("gpu_status", json!({}))["budget"]["level"], "warn70");
    add_hours(110.0);
    assert_eq!(env.call("gpu_status", json!({}))["budget"]["level"], "warn90");
    let id = project(&env, "Budget");
    assert_eq!(env.call("generate", json!({ "project_id": id }))["queued"], 3, "still accepted below 100%");
    add_hours(60.0);
    let b = env.call("gpu_status", json!({}))["budget"].clone();
    assert_eq!(b["level"], "blocked");
    assert!(b["spent_sar"].as_f64().unwrap() >= 1000.0);
    let id2 = project(&env, "Over budget");
    assert_eq!(env.fail("generate", json!({ "project_id": id2 })), "budget_exceeded");
    env.call("gpu_stop", json!({}));
    assert_eq!(env.fail("gpu_start", json!({ "approved": true, "approved_by": "Khalid" })), "budget_exceeded");
    // raising the limit is the manager's explicit decision and is written to the audit log
    env.call("setting_set", json!({ "key": "gpu_budget_sar", "value": "2000" }));
    assert_eq!(env.call("gpu_status", json!({}))["budget"]["level"], "ok");
    assert!(env.call("audit_log", json!({})).as_array().unwrap().iter().any(|l| l["event"] == "settings.gpu" && l["message"].as_str().unwrap().contains("gpu_budget_sar")));

    // idle shutdown: running, nothing queued, last activity long ago → stopped automatically
    for j in env.call("jobs_list", json!({})).as_array().unwrap() { env.call("job_cancel", json!({ "id": j["id"] })); }
    env.call("gpu_start", json!({ "approved": true, "approved_by": "Khalid" }));
    env.set("gpu_last_activity", &(chrono::Utc::now() - chrono::Duration::minutes(30)).to_rfc3339());
    let stops = gpu.lock().unwrap().stops;
    assert!(studio_core::gpu::idle_check(&env.app).unwrap());
    assert_eq!(gpu.lock().unwrap().stops, stops + 1);
    assert_eq!(env.call("gpu_status", json!({}))["sessions"][0]["stop_reason"], "automatic idle shutdown");

    // a generation job does not start the GPU by itself: it waits
    env.call("setting_set", json!({ "key": "comfy_url", "value": "http://127.0.0.1:9" }));
    env.call("generate", json!({ "project_id": id }));
    let starts = gpu.lock().unwrap().starts;
    studio_core::jobs::tick(&env.app);
    assert_eq!(gpu.lock().unwrap().starts, starts, "no automatic start");
    assert!(env.call("jobs_list", json!({})).as_array().unwrap().iter().any(|j| j["status"] == "blocked" && j["blocked_reason"] == "gpu_stopped"));
    // a bad key is reported, and the key never appears in the error
    env.call("secret_set", json!({ "name": "gpu_api_key", "value": "another-wrong-key-999" }));
    let st = env.call("gpu_status", json!({}));
    assert_eq!(st["error"]["code"], "gpu_auth");
    assert!(!st.to_string().contains("another-wrong-key-999"));
}

#[test]
fn timeline_plan_arithmetic() {
    use studio_core::timeline::*;
    let clip = |d: f64, a: bool| ClipSource { path: "/x/c.mp4".into(), duration: d, has_audio: a, width: 1280, height: 704 };
    let tl = json!({ "clips": [ { "scene_id": "a", "trim_in": 0.0, "trim_out": 4.0 }, { "scene_id": "b", "trim_in": 1.0, "trim_out": 5.0, "transition": { "kind": "dissolve", "duration": 1.0 } }, { "scene_id": "c", "transition": { "kind": "cut" } } ],
        "color": { "brightness": 0.05, "contrast": 1.1, "saturation": 1.2 }, "output": { "preset": "1080p", "fps": 30, "crf": 20 },
        "audio": [ { "media_id": "m", "track": "music", "start": 2.0, "volume": 0.5, "fade_in": 1.0, "fade_out": 1.0 } ] });
    let audio = vec![(tl["audio"][0].clone(), AudioSource { path: "/x/m.wav".into(), duration: 30.0 })];
    let p = plan(&tl, &[clip(5.0, false), clip(5.0, false), clip(3.0, false)], &audio, "16:9", "/out.mp4", "T").unwrap();
    assert!((p.duration - 10.0).abs() < 1e-6, "4 + 4 − 1 (dissolve) + 3 = 10, got {}", p.duration);
    assert_eq!((p.width, p.height, p.fps), (1920, 1080, 30));
    let fc = &p.args[p.args.iter().position(|a| a == "-filter_complex").unwrap() + 1];
    assert!(fc.contains("xfade=transition=dissolve:duration=1.000:offset=3.000"), "{fc}");
    assert!(fc.contains("concat=n=2:v=1:a=0") && fc.contains("eq=brightness=0.050:contrast=1.100:saturation=1.200"));
    assert!(fc.contains("adelay=2000:all=1") && fc.contains("volume=0.500") && fc.contains("afade=t=out:st=7.000:d=1.000"), "{fc}");
    assert!(p.args.contains(&"+faststart".to_string()) && p.args.contains(&"20".to_string()));
    assert_eq!(preset_check("9:16"), (1080, 1920));
    assert!(plan(&json!({ "clips": [] }), &[], &[], "16:9", "/o.mp4", "T").is_err());
    fn preset_check(aspect: &str) -> (i64, i64) {
        let c = ClipSource { path: "/c.mp4".into(), duration: 2.0, has_audio: false, width: 704, height: 1280 };
        let p = plan(&json!({ "clips": [{ "scene_id": "a" }], "output": { "preset": "1080p" } }), &[c], &[], aspect, "/o.mp4", "T").unwrap();
        (p.width, p.height)
    }
}

#[test]
fn export_renders_a_playable_mp4_with_audio_tracks() {
    let env = Env::new();
    let id = project(&env, "Export film");
    fill_videos(&env, &id, true);
    let (music, voice) = (env.file("music.wav"), env.file("voice.wav"));
    make_audio(&music, 20.0); make_audio(&voice, 2.0);
    let m = env.call("media_import", json!({ "paths": [music.to_string_lossy(), voice.to_string_lossy()] }));
    let mut tl = env.call("timeline_get", json!({ "project_id": id }))["timeline"].clone();
    assert_eq!(tl["clips"].as_array().unwrap().len(), 3);
    tl["clips"][0]["trim_out"] = json!(3.0);
    tl["clips"][1]["trim_out"] = json!(4.0);
    tl["clips"][2]["trim_out"] = json!(3.0);
    tl["clips"][1]["transition"] = json!({ "kind": "fade", "duration": 1.0 });
    tl["audio"] = json!([ { "id": "1", "media_id": m[0]["media"]["id"], "track": "music", "start": 0.0, "volume": 0.4, "fade_out": 1.5 }, { "id": "2", "media_id": m[1]["media"]["id"], "track": "voiceover", "start": 4.0, "volume": 1.0 } ]);
    tl["color"] = json!({ "brightness": 0.02, "contrast": 1.05, "saturation": 1.1 });
    env.call("project_update", json!({ "id": id, "patch": { "timeline": tl } }));
    env.call("export", json!({ "project_id": id, "options": { "output": { "preset": "720p", "fps": 24, "crf": 23 } } }));
    assert_eq!(env.fail("export", json!({ "project_id": id })), "export_running");
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert_eq!(j[0]["status"], "succeeded", "{}", j[0]);
    let p = env.call("project_get", json!({ "id": id }));
    let e = &p["exports"][0];
    assert_eq!(e["status"], "completed");
    assert!((e["duration"].as_f64().unwrap() - 9.0).abs() < 0.15, "3 + 4 − 1 + 3 = 9 s, got {}", e["duration"]);
    assert_eq!((e["width"].as_i64(), e["height"].as_i64()), (Some(1280), Some(720)));
    let file = env.app.lib().resolve(e["path"].as_str().unwrap()).unwrap();
    let info = studio_core::ffmpeg::verify_playable(&env.app.tools().unwrap(), &file).unwrap();
    assert!(info.has_audio && info.video_codec.as_deref() == Some("h264"));
    let meta: Value = serde_json::from_slice(&std::fs::read(file.with_extension("json")).unwrap()).unwrap();
    assert_eq!(meta["scenes"].as_array().unwrap().len(), 3);
    assert_eq!(p["status"], "exported");
    // a film with a missing scene video is refused with the scene named
    std::fs::remove_file(env.app.lib().resolve(p["scenes"][1]["video_path"].as_str().unwrap()).unwrap()).unwrap();
    env.call("export", json!({ "project_id": id }));
    studio_core::jobs::tick(&env.app);
    let j = env.call("jobs_list", json!({}));
    assert!(j[0]["status"] == "failed" && j[0]["error"].as_str().unwrap().contains("scene 2"), "{}", j[0]);
}

#[test]
fn lora_library() {
    let env = Env::new();
    let good = env.file("style.safetensors");
    let header = br#"{"__metadata__":{"ss_network_dim":"32"},"lora.weight":{"dtype":"F16","shape":[1],"data_offsets":[0,2]}}"#;
    let mut bytes = (header.len() as u64).to_le_bytes().to_vec();
    bytes.extend_from_slice(header); bytes.extend_from_slice(&[0, 0]);
    std::fs::write(&good, &bytes).unwrap();
    let pickle = env.file("model.ckpt");
    std::fs::write(&pickle, b"\x80\x04pickle").unwrap();
    let renamed = env.file("renamed.safetensors");
    std::fs::write(&renamed, b"\x80\x04 this is a pickle with a new name").unwrap();
    let args = |path: &std::path::Path, version: &str, family: &str| json!({ "path": path.to_string_lossy(), "name": "Style", "family": family, "specialty": "luxury_real_estate", "version": version, "trigger": "lxre style" });
    assert_eq!(env.fail("lora_import", args(&pickle, "1.0.0", "wan22-5b")), "not_safetensors");
    assert_eq!(env.fail("lora_import", args(&renamed, "1.0.0", "wan22-5b")), "not_safetensors");
    assert_eq!(env.fail("lora_import", args(&good, "1.0.0", "sdxl")), "bad_request");
    let v1 = env.call("lora_import", args(&good, "1.0.0", "wan22-5b"));
    assert_eq!(v1["enabled"], 0, "imported disabled");
    assert!(env.app.lib().resolve(v1["file_path"].as_str().unwrap()).unwrap().is_file());
    assert!(v1["notes"].as_str().unwrap().contains("\"network_dim\":\"32\""), "metadata read from the file header");
    assert_eq!(env.fail("lora_import", args(&good, "1.0.0", "wan22-5b")), "version_exists");
    let v2 = env.call("lora_import", args(&good, "1.1.0", "wan22-5b"));
    let other = env.call("lora_import", args(&good, "1.0.0", "wan22-a14b-i2v"));
    env.call("lora_update", json!({ "id": v1["id"], "enabled": true }));
    env.call("lora_update", json!({ "id": other["id"], "enabled": true }));
    env.call("lora_update", json!({ "id": v2["id"], "enabled": true, "strength": 0.8 }));
    let l = env.call("lora_list", json!({}));
    let on: Vec<&Value> = l["loras"].as_array().unwrap().iter().filter(|x| x["enabled"] == 1).collect();
    assert_eq!(on.len(), 2, "one enabled version per name and family; the other family is independent");
    assert!(on.iter().any(|x| x["version"] == "1.1.0") && !on.iter().any(|x| x["id"] == v1["id"]));
    // datasets need a rights note; a training run is only a record and needs a named approver
    let folder = env.file("dataset");
    std::fs::create_dir_all(&folder).unwrap();
    make_video(&folder.join("a.mp4"), 1.0, "320x240", false);
    assert_eq!(env.fail("lora_dataset_add", json!({ "name": "Villas", "specialty": "luxury_real_estate", "folder": folder.to_string_lossy() })), "rights_required");
    let d = env.call("lora_dataset_add", json!({ "name": "Villas", "specialty": "luxury_real_estate", "folder": folder.to_string_lossy(), "rights_note": "Own shoot, 2026-10" }));
    assert_eq!(d["clip_count"], 1);
    let run = env.call("lora_run_plan", json!({ "family": "wan22-a14b-i2v", "dataset_id": d["id"], "estimated_cost_sar": 120.0 }));
    assert_eq!(run["status"], "planned");
    assert_eq!(env.fail("lora_run_update", json!({ "id": run["id"], "status": "approved" })), "approval_required");
    assert_eq!(env.call("lora_run_update", json!({ "id": run["id"], "status": "approved", "approved_by": "Khalid" }))["approved_by"], "Khalid");
    env.call("lora_remove", json!({ "id": v1["id"] }));
    assert!(env.app.lib().dir("Backups").join("Deleted").read_dir().unwrap().count() >= 1);
}

#[test]
fn enabled_lora_is_applied_only_to_its_family_and_must_be_on_the_server() {
    let env = Env::new();
    let sample = env.file("out.mp4");
    make_video(&sample, 2.0, "640x360", false);
    let (url, comfy) = fake_comfy(sample);
    env.call("setting_set", json!({ "key": "comfy_url", "value": url }));
    let f = env.file("style.safetensors");
    let header = br#"{"t":{"dtype":"F16","shape":[1],"data_offsets":[0,2]}}"#;
    let mut bytes = (header.len() as u64).to_le_bytes().to_vec(); bytes.extend_from_slice(header); bytes.extend_from_slice(&[0, 0]);
    std::fs::write(&f, &bytes).unwrap();
    let mk = |family: &str| env.call("lora_import", json!({ "path": f.to_string_lossy(), "name": "style", "family": family, "specialty": "saudi_tourism", "version": "1.0.0", "trigger": "sa-tour" }));
    let (a, b) = (mk("wan22-5b"), mk("wan22-a14b-i2v"));
    env.call("lora_update", json!({ "id": a["id"], "enabled": true, "strength": 0.7 }));
    env.call("lora_update", json!({ "id": b["id"], "enabled": true }));
    let id = project(&env, "LoRA");
    let sid = env.call("project_get", json!({ "id": id }))["scenes"][0]["id"].as_str().unwrap().to_string();
    env.call("generate", json!({ "project_id": id, "scene_ids": [sid] }));
    studio_core::jobs::tick(&env.app);
    assert_eq!(env.call("jobs_list", json!({}))[0]["status"], "succeeded", "{}", env.call("jobs_list", json!({}))[0]);
    let wf = comfy.lock().unwrap().prompts[0].1.clone();
    assert_eq!(wf["lora0"]["class_type"], "LoraLoaderModelOnly");
    assert_eq!(wf["lora0"]["inputs"]["lora_name"], "style-1.0.0.safetensors");
    assert_eq!(wf["lora0"]["inputs"]["strength_model"], 0.7);
    assert!(wf.get("lora1").is_none(), "the LoRA of another model family is not applied");
    assert_eq!(wf["shift"]["inputs"]["model"][0], "lora0");
    assert!(wf["pos"]["inputs"]["text"].as_str().unwrap().starts_with("sa-tour, "));
    // enabled here but absent on the server → refused, not silently skipped
    comfy.lock().unwrap().missing_files = vec!["style-1.0.0.safetensors".into()];
    env.call("generate", json!({ "project_id": id, "scene_ids": [sid] }));
    studio_core::jobs::tick(&env.app);
    assert!(env.call("jobs_list", json!({}))[0]["error"].as_str().unwrap().starts_with("lora_not_on_server"));
}

#[test]
fn model_limits_are_enforced_before_queueing() {
    let env = Env::new();
    let id = project(&env, "Limits");
    let s = env.call("project_get", json!({ "id": id }))["scenes"][0]["id"].as_str().unwrap().to_string();
    env.call("scene_update", json!({ "id": s, "patch": { "duration": 9 } }));
    assert_eq!(env.fail("generate", json!({ "project_id": id })), "scene_too_long");
    env.call("scene_update", json!({ "id": s, "patch": { "duration": 5 } }));
    env.call("project_update", json!({ "id": id, "patch": { "aspect": "1:1" } }));
    assert_eq!(env.fail("generate", json!({ "project_id": id })), "aspect_not_supported");
    env.call("project_update", json!({ "id": id, "patch": { "aspect": "16:9", "model_id": "wan22-i2v-a14b-4step" } }));
    assert_eq!(env.fail("generate", json!({ "project_id": id })), "reference_required");
    let models = env.call("models_list", json!({}));
    assert_eq!(models[0]["id"], "wan22-ti2v-5b");
    assert!((models[0]["max_seconds"].as_f64().unwrap() - 121.0 / 24.0).abs() < 1e-9);
}
