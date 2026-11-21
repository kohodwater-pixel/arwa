//! SQLite schema. Media bytes never go in here: only paths, hashes and metadata.
use crate::error::Result;
use rusqlite::Connection;
use std::path::Path;

const MIGRATIONS: &[&str] = &["
CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);

CREATE TABLE projects (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
  video_type TEXT NOT NULL DEFAULT 'commercial', style TEXT NOT NULL DEFAULT 'auto',
  aspect TEXT NOT NULL DEFAULT '16:9', duration INTEGER NOT NULL DEFAULT 15,
  model_id TEXT NOT NULL DEFAULT 'wan22-ti2v-5b', model_config_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'draft',              -- draft | storyboard | generating | ready | exported
  folder TEXT NOT NULL,                               -- relative to the library root
  director_json TEXT, timeline_json TEXT,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);

CREATE TABLE scenes (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  position INTEGER NOT NULL, role TEXT, title TEXT NOT NULL, duration INTEGER NOT NULL,
  description TEXT NOT NULL DEFAULT '', prompt TEXT NOT NULL DEFAULT '', negative_prompt TEXT NOT NULL DEFAULT '',
  prompt_edited INTEGER NOT NULL DEFAULT 0, camera_move TEXT, shot_size TEXT, camera_angle TEXT, lighting TEXT,
  reference_media_id TEXT, seed INTEGER,
  status TEXT NOT NULL DEFAULT 'pending',             -- pending | queued | generating | completed | failed
  video_path TEXT, preview_path TEXT, video_duration REAL, error TEXT, updated_at TEXT NOT NULL
);
CREATE INDEX scenes_project ON scenes(project_id, position);

CREATE TABLE jobs (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE, scene_id TEXT,
  kind TEXT NOT NULL,                                 -- generate | export
  provider TEXT, model_id TEXT,
  status TEXT NOT NULL DEFAULT 'queued',              -- queued | blocked | submitted | running | downloading | succeeded | failed | canceled
  blocked_reason TEXT, remote_id TEXT, progress REAL, stage TEXT, attempts INTEGER NOT NULL DEFAULT 0,
  request_json TEXT, result_path TEXT, error TEXT,
  created_at TEXT NOT NULL, started_at TEXT, finished_at TEXT
);
CREATE INDEX jobs_status ON jobs(status, created_at);

CREATE TABLE media (
  id TEXT PRIMARY KEY, project_id TEXT REFERENCES projects(id) ON DELETE SET NULL, folder TEXT NOT NULL DEFAULT '',
  kind TEXT NOT NULL,                                 -- image | video | audio
  name TEXT NOT NULL, path TEXT NOT NULL,             -- absolute path of the user's original file (never copied or modified)
  sha256 TEXT NOT NULL, size INTEGER NOT NULL, duration REAL, width INTEGER, height INTEGER, fps REAL,
  thumb_path TEXT, missing INTEGER NOT NULL DEFAULT 0, corrupted INTEGER NOT NULL DEFAULT 0, imported_at TEXT NOT NULL
);
CREATE INDEX media_hash ON media(sha256);

CREATE TABLE exports (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  path TEXT NOT NULL, preset TEXT NOT NULL, width INTEGER, height INTEGER, duration REAL, size INTEGER,
  status TEXT NOT NULL, metadata_json TEXT, error TEXT, created_at TEXT NOT NULL
);

CREATE TABLE loras (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, family TEXT NOT NULL,   -- model family the file was trained for, e.g. wan22-a14b
  specialty TEXT NOT NULL, version TEXT NOT NULL, file_path TEXT NOT NULL, sha256 TEXT NOT NULL, size INTEGER NOT NULL,
  trigger TEXT, strength REAL NOT NULL DEFAULT 1.0, enabled INTEGER NOT NULL DEFAULT 0,
  trainer TEXT, source TEXT, notes TEXT, created_at TEXT NOT NULL,
  UNIQUE (name, family, version)
);
CREATE TABLE lora_datasets (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, specialty TEXT NOT NULL, folder TEXT NOT NULL,
  rights_note TEXT NOT NULL, clip_count INTEGER NOT NULL DEFAULT 0, notes TEXT, created_at TEXT NOT NULL
);
CREATE TABLE lora_training_runs (
  id TEXT PRIMARY KEY, dataset_id TEXT REFERENCES lora_datasets(id) ON DELETE SET NULL, lora_id TEXT REFERENCES loras(id) ON DELETE SET NULL,
  family TEXT NOT NULL, tool TEXT NOT NULL DEFAULT 'musubi-tuner',
  status TEXT NOT NULL DEFAULT 'planned',             -- planned | approved | recorded
  config_json TEXT, approved_by TEXT, estimated_cost_sar REAL, notes TEXT, created_at TEXT NOT NULL
);

CREATE TABLE gpu_sessions (
  id TEXT PRIMARY KEY, provider TEXT NOT NULL, instance_id TEXT NOT NULL,
  started_at TEXT NOT NULL, stopped_at TEXT, rate_usd_per_hour REAL NOT NULL, usd_to_sar REAL NOT NULL,
  approved_by TEXT NOT NULL, stop_reason TEXT
);
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, level TEXT NOT NULL, event TEXT NOT NULL, message TEXT NOT NULL
);
"];

pub fn open(file: &Path) -> Result<Connection> {
    let conn = Connection::open(file)?;
    conn.execute_batch("PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA busy_timeout = 5000; PRAGMA synchronous = NORMAL;")?;
    conn.execute_batch("CREATE TABLE IF NOT EXISTS schema_version (v INTEGER NOT NULL)")?;
    let mut current: i64 = conn.query_row("SELECT COALESCE(MAX(v), 0) FROM schema_version", [], |r| r.get(0))?;
    while (current as usize) < MIGRATIONS.len() {
        let tx = conn.unchecked_transaction()?;
        tx.execute_batch(MIGRATIONS[current as usize])?;
        tx.execute("INSERT INTO schema_version (v) VALUES (?1)", [current + 1])?;
        tx.commit()?;
        current += 1;
    }
    Ok(conn)
}

pub fn now() -> String {
    chrono::Utc::now().to_rfc3339_opts(chrono::SecondsFormat::Millis, true)
}
pub fn new_id() -> String {
    uuid::Uuid::new_v4().to_string()
}

pub fn get_setting(conn: &Connection, key: &str) -> Option<String> {
    conn.query_row("SELECT value FROM settings WHERE key = ?1", [key], |r| r.get(0)).ok()
}
pub fn set_setting(conn: &Connection, key: &str, value: &str) -> Result<()> {
    conn.execute("INSERT INTO settings (key, value) VALUES (?1, ?2) ON CONFLICT(key) DO UPDATE SET value = excluded.value", [key, value])?;
    Ok(())
}
pub fn audit(conn: &Connection, level: &str, event: &str, message: &str) {
    let _ = conn.execute("INSERT INTO audit_log (ts, level, event, message) VALUES (?1, ?2, ?3, ?4)", [&now(), level, event, &message.chars().take(1000).collect::<String>()]);
}

/// Runs a query and returns every row as a JSON object keyed by column name.
pub fn rows(conn: &Connection, sql: &str, params: &[&dyn rusqlite::ToSql]) -> Result<Vec<serde_json::Value>> {
    let mut stmt = conn.prepare(sql)?;
    let names: Vec<String> = stmt.column_names().iter().map(|s| s.to_string()).collect();
    let out = stmt
        .query_map(params, |row| {
            let mut m = serde_json::Map::new();
            for (i, n) in names.iter().enumerate() {
                let v = match row.get_ref(i)? {
                    rusqlite::types::ValueRef::Null => serde_json::Value::Null,
                    rusqlite::types::ValueRef::Integer(x) => x.into(),
                    rusqlite::types::ValueRef::Real(x) => serde_json::json!(x),
                    rusqlite::types::ValueRef::Text(t) => String::from_utf8_lossy(t).to_string().into(),
                    rusqlite::types::ValueRef::Blob(_) => serde_json::Value::Null,
                };
                m.insert(n.clone(), v);
            }
            Ok(serde_json::Value::Object(m))
        })?
        .collect::<std::result::Result<Vec<_>, _>>()?;
    Ok(out)
}
pub fn row(conn: &Connection, sql: &str, params: &[&dyn rusqlite::ToSql]) -> Result<Option<serde_json::Value>> {
    Ok(rows(conn, sql, params)?.into_iter().next())
}
