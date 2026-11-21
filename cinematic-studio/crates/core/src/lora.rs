//! LoRA library, training datasets and training history.
//! A LoRA belongs to one model family and is only ever applied to that family.
//! Nothing here starts a training run: a run can be planned and approved as a record, and the training itself
//! is done outside the app with Musubi Tuner. Recording a plan never spends money.
use crate::args::*;
use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::App;
use rusqlite::params;
use serde_json::{json, Value};
use std::io::Read;
use std::path::Path;

pub const SPECIALTIES: [&str; 4] = ["gulf_commercial_advertising", "luxury_real_estate", "saudi_tourism", "luxury_product_cinematography"];

pub fn families() -> Vec<&'static str> {
    let mut f: Vec<&'static str> = crate::comfy::adapters().iter().map(|a| a.info().lora_family).collect();
    f.extend(["wan22-a14b-t2v", "hunyuan15"]);
    f.sort();
    f.dedup();
    f
}

/// A .safetensors file starts with an 8-byte little-endian header length followed by a JSON object.
/// Other formats (.ckpt, .pt, .bin) can carry executable code and are refused.
fn check_safetensors(path: &Path) -> Result<Value> {
    if path.extension().and_then(|e| e.to_str()).map(|e| e.to_lowercase()) != Some("safetensors".into()) { return err("not_safetensors", "only .safetensors files are accepted"); }
    let mut f = std::fs::File::open(path)?;
    let mut len = [0u8; 8];
    f.read_exact(&mut len).map_err(|_| AppError::new("not_safetensors", "the file is too short"))?;
    let n = u64::from_le_bytes(len);
    if n < 2 || n > 100 * 1024 * 1024 { return err("not_safetensors", "the header length is not plausible"); }
    let mut head = vec![0u8; n as usize];
    f.read_exact(&mut head).map_err(|_| AppError::new("not_safetensors", "the header is incomplete"))?;
    let j: Value = serde_json::from_slice(&head).map_err(|_| AppError::new("not_safetensors", "the header is not valid JSON"))?;
    if !j.is_object() { return err("not_safetensors", "the header is not a JSON object"); }
    // trainers write their settings under __metadata__; keep a small, useful subset
    let meta = &j["__metadata__"];
    let pick = |k: &str| meta.get(k).and_then(Value::as_str).map(|s| limit(s, 200));
    Ok(json!({ "tensors": j.as_object().map(|o| o.len().saturating_sub(1)).unwrap_or(0), "network_dim": pick("ss_network_dim"), "network_alpha": pick("ss_network_alpha"), "base_model": pick("ss_base_model_version").or_else(|| pick("ss_sd_model_name")), "trainer_note": pick("ss_training_comment") }))
}

pub fn import(app: &App, a: &Value) -> Result<Value> {
    let src = Path::new(str_req(a, "path")?);
    if !src.is_absolute() || !src.is_file() { return err("bad_path", "choose an existing file"); }
    let family = str_req(a, "family")?;
    if !families().contains(&family) { return err("bad_request", format!("family must be one of: {}", families().join(", "))); }
    let specialty = str_req(a, "specialty")?;
    one_of(specialty, &SPECIALTIES, "specialty")?;
    let name = crate::paths::slug(str_req(a, "name")?, 60);
    let version = limit(str_opt(a, "version").unwrap_or("1.0.0"), 20);
    if !version.chars().all(|c| c.is_ascii_alphanumeric() || c == '.' || c == '-') { return err("bad_request", "version may contain letters, digits, dots and hyphens"); }
    let header = check_safetensors(src)?;
    let hash = crate::media::sha256_file(src)?;
    let lib = app.lib();
    let rel = format!("Models/loras/{family}/{name}-{version}.safetensors");
    let dest = lib.resolve(&rel)?;
    {
        let conn = app.db.lock().unwrap();
        let dup: i64 = conn.query_row("SELECT COUNT(*) FROM loras WHERE name = ?1 AND family = ?2 AND version = ?3", params![name, family, version], |r| r.get(0))?;
        if dup > 0 || dest.exists() { return err("version_exists", "this name and version already exist for this model family; versions are never overwritten"); }
    }
    std::fs::create_dir_all(dest.parent().unwrap())?;
    std::fs::copy(src, &dest)?;
    let id = new_id();
    let conn = app.db.lock().unwrap();
    conn.execute("INSERT INTO loras (id, name, family, specialty, version, file_path, sha256, size, trigger, strength, enabled, trainer, source, notes, created_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,0,?11,?12,?13,?14)",
        params![id, name, family, specialty, version, rel, hash, std::fs::metadata(&dest)?.len() as i64, str_opt(a, "trigger").map(|t| limit(t, 60)), f64_opt(a, "strength").unwrap_or(1.0).clamp(0.0, 2.0),
            str_opt(a, "trainer").map(|t| limit(t, 80)), src.to_string_lossy(), json!({ "note": str_opt(a, "notes").map(|n| limit(n, 2000)), "header": header }).to_string(), now()])?;
    db::audit(&conn, "info", "lora.imported", &format!("{name} {version} ({family})"));
    row(&conn, "SELECT * FROM loras WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("database", "insert failed"))
}

pub fn list(app: &App) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    Ok(json!({ "loras": rows(&conn, "SELECT * FROM loras ORDER BY family, name, created_at DESC", &[])?, "families": families(), "specialties": SPECIALTIES,
        "datasets": rows(&conn, "SELECT * FROM lora_datasets ORDER BY created_at DESC", &[])?,
        "runs": rows(&conn, "SELECT r.*, d.name AS dataset_name, l.name AS lora_name FROM lora_training_runs r LEFT JOIN lora_datasets d ON d.id = r.dataset_id LEFT JOIN loras l ON l.id = r.lora_id ORDER BY r.created_at DESC", &[])? }))
}

pub fn update(app: &App, id: &str, a: &Value) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    let l = row(&conn, "SELECT * FROM loras WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("lora_not_found", id.to_string()))?;
    if let Some(e) = bool_opt(a, "enabled") {
        if e {
            // one enabled version per (name, family): enabling a version disables its siblings
            conn.execute("UPDATE loras SET enabled = 0 WHERE name = ?1 AND family = ?2", params![l["name"].as_str(), l["family"].as_str()])?;
        }
        conn.execute("UPDATE loras SET enabled = ?1 WHERE id = ?2", params![e as i64, id])?;
    }
    if let Some(s) = f64_opt(a, "strength") { conn.execute("UPDATE loras SET strength = ?1 WHERE id = ?2", params![s.clamp(0.0, 2.0), id])?; }
    if a.get("trigger").is_some() { conn.execute("UPDATE loras SET trigger = ?1 WHERE id = ?2", params![str_opt(a, "trigger").map(|t| limit(t, 60)), id])?; }
    row(&conn, "SELECT * FROM loras WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("lora_not_found", id.to_string()))
}

/// Removes the entry; the file is moved to Backups/Deleted rather than erased.
pub fn remove(app: &App, id: &str) -> Result<Value> {
    let lib = app.lib();
    let conn = app.db.lock().unwrap();
    let l = row(&conn, "SELECT * FROM loras WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("lora_not_found", id.to_string()))?;
    if let Ok(p) = lib.resolve(l["file_path"].as_str().unwrap_or("")) {
        if p.is_file() {
            let bin = lib.dir("Backups").join("Deleted");
            std::fs::create_dir_all(&bin)?;
            std::fs::rename(&p, bin.join(format!("{}-{}", chrono::Utc::now().format("%Y%m%d-%H%M%S"), p.file_name().unwrap_or_default().to_string_lossy())))?;
        }
    }
    conn.execute("DELETE FROM loras WHERE id = ?1", [id])?;
    Ok(json!({ "ok": true }))
}

pub fn dataset_add(app: &App, a: &Value) -> Result<Value> {
    let folder = Path::new(str_req(a, "folder")?);
    if !folder.is_absolute() || !folder.is_dir() { return err("bad_path", "choose an existing folder"); }
    let specialty = str_req(a, "specialty")?;
    one_of(specialty, &SPECIALTIES, "specialty")?;
    let rights = str_req(a, "rights_note").map_err(|_| AppError::new("rights_required", "say where the clips come from and what permits training on them"))?;
    let clips = std::fs::read_dir(folder)?.filter_map(|e| e.ok()).filter(|e| e.path().extension().and_then(|x| x.to_str()).map(|x| ["mp4", "mov", "mkv", "webm"].contains(&x.to_lowercase().as_str())).unwrap_or(false)).count();
    let id = new_id();
    let conn = app.db.lock().unwrap();
    conn.execute("INSERT INTO lora_datasets (id, name, specialty, folder, rights_note, clip_count, notes, created_at) VALUES (?1,?2,?3,?4,?5,?6,?7,?8)",
        params![id, limit(str_req(a, "name")?, 120), specialty, folder.to_string_lossy(), limit(rights, 1000), clips as i64, str_opt(a, "notes").map(|n| limit(n, 2000)), now()])?;
    row(&conn, "SELECT * FROM lora_datasets WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("database", "insert failed"))
}
pub fn dataset_remove(app: &App, id: &str) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    conn.execute("DELETE FROM lora_datasets WHERE id = ?1", [id])?; // the folder itself is the user's and is not touched
    Ok(json!({ "ok": true }))
}

/// Records a planned training run. It stays "planned" until a named person approves it; approval is a
/// record of the decision, not a trigger: the app never launches training.
pub fn run_plan(app: &App, a: &Value) -> Result<Value> {
    let family = str_req(a, "family")?;
    if !families().contains(&family) { return err("bad_request", "unknown model family"); }
    let id = new_id();
    let conn = app.db.lock().unwrap();
    conn.execute("INSERT INTO lora_training_runs (id, dataset_id, family, tool, status, config_json, estimated_cost_sar, notes, created_at) VALUES (?1,?2,?3,'musubi-tuner','planned',?4,?5,?6,?7)",
        params![id, str_opt(a, "dataset_id"), family, a.get("config").map(|c| c.to_string()), f64_opt(a, "estimated_cost_sar"), str_opt(a, "notes").map(|n| limit(n, 2000)), now()])?;
    row(&conn, "SELECT * FROM lora_training_runs WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("database", "insert failed"))
}
pub fn run_update(app: &App, id: &str, a: &Value) -> Result<Value> {
    let conn = app.db.lock().unwrap();
    if let Some(status) = str_opt(a, "status") {
        one_of(status, &["planned", "approved", "recorded"], "status")?;
        if status == "approved" {
            let by = str_req(a, "approved_by").map_err(|_| AppError::new("approval_required", "an approval needs the approver's name"))?;
            conn.execute("UPDATE lora_training_runs SET status = 'approved', approved_by = ?1 WHERE id = ?2", params![limit(by, 80), id])?;
            db::audit(&conn, "info", "lora.run_approved", &format!("training run approved by {}", limit(by, 80)));
        } else {
            conn.execute("UPDATE lora_training_runs SET status = ?1 WHERE id = ?2", params![status, id])?;
        }
    }
    if a.get("lora_id").is_some() { conn.execute("UPDATE lora_training_runs SET lora_id = ?1 WHERE id = ?2", params![str_opt(a, "lora_id"), id])?; }
    if let Some(n) = str_opt(a, "notes") { conn.execute("UPDATE lora_training_runs SET notes = ?1 WHERE id = ?2", params![limit(n, 2000), id])?; }
    row(&conn, "SELECT * FROM lora_training_runs WHERE id = ?1", &[&id])?.ok_or_else(|| AppError::new("run_not_found", id.to_string()))
}
