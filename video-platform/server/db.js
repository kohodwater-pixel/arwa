import path from 'node:path';
import crypto from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { config } from './config.js';

export const db = new DatabaseSync(process.env.DB_FILE || path.join(config.dataDir, 'app.db'));
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA busy_timeout = 5000;');

const migrations = [
  `
  CREATE TABLE users (
    id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE, name TEXT NOT NULL, password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', status TEXT NOT NULL DEFAULT 'active', locale TEXT NOT NULL DEFAULT 'ar',
    limits_json TEXT, created_at INTEGER NOT NULL, last_login_at INTEGER
  );
  CREATE TABLE sessions (
    token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at INTEGER NOT NULL, expires_at INTEGER NOT NULL
  );
  CREATE TABLE password_resets (
    token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at INTEGER NOT NULL, used_at INTEGER
  );
  CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
  CREATE TABLE provider_settings (
    provider_id TEXT PRIMARY KEY, enabled INTEGER NOT NULL DEFAULT 1, credentials_enc TEXT, updated_at INTEGER
  );
  CREATE TABLE projects (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL, description TEXT NOT NULL, video_type TEXT NOT NULL, style TEXT NOT NULL,
    duration INTEGER NOT NULL, aspect TEXT NOT NULL, quality TEXT NOT NULL, provider_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft', is_demo INTEGER NOT NULL DEFAULT 0,
    treatment_json TEXT, audio_json TEXT, options_json TEXT, final_asset_id TEXT, share_token TEXT UNIQUE,
    error TEXT, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
  );
  CREATE INDEX projects_user ON projects(user_id, updated_at);
  CREATE TABLE scenes (
    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    position INTEGER NOT NULL, role TEXT, title TEXT NOT NULL, description TEXT NOT NULL, duration INTEGER NOT NULL,
    shot_size TEXT, camera_move TEXT, camera_angle TEXT, lighting TEXT, prompt TEXT NOT NULL,
    prompt_edited INTEGER NOT NULL DEFAULT 0, variant INTEGER NOT NULL DEFAULT 0,
    action_en TEXT, reference_asset_id TEXT, voiceover TEXT,
    status TEXT NOT NULL DEFAULT 'pending', clip_asset_id TEXT, progress REAL, error TEXT
  );
  CREATE INDEX scenes_project ON scenes(project_id, position);
  CREATE TABLE assets (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id TEXT REFERENCES projects(id) ON DELETE SET NULL,
    kind TEXT NOT NULL, filename TEXT NOT NULL, mime TEXT NOT NULL, size INTEGER NOT NULL, storage_key TEXT NOT NULL,
    duration REAL, width INTEGER, height INTEGER, is_demo INTEGER NOT NULL DEFAULT 0, created_at INTEGER NOT NULL
  );
  CREATE INDEX assets_user ON assets(user_id, kind);
  CREATE TABLE jobs (
    id TEXT PRIMARY KEY, type TEXT NOT NULL, user_id TEXT NOT NULL, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    scene_id TEXT, status TEXT NOT NULL DEFAULT 'queued', attempts INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL DEFAULT 3,
    run_at INTEGER NOT NULL, provider_id TEXT, provider_job_id TEXT, progress REAL, payload_json TEXT, error TEXT,
    created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL, started_at INTEGER, finished_at INTEGER
  );
  CREATE INDEX jobs_due ON jobs(status, run_at);
  CREATE INDEX jobs_project ON jobs(project_id);
  CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, level TEXT NOT NULL, event TEXT NOT NULL,
    user_id TEXT, project_id TEXT, job_id TEXT, message TEXT, data_json TEXT
  );
  CREATE INDEX logs_ts ON logs(ts);
  CREATE TABLE usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, project_id TEXT, provider_id TEXT NOT NULL,
    seconds REAL NOT NULL, is_demo INTEGER NOT NULL DEFAULT 0, created_at INTEGER NOT NULL
  );
  CREATE INDEX usage_user ON usage(user_id, created_at);
  `,
];

db.exec('CREATE TABLE IF NOT EXISTS schema_version (v INTEGER NOT NULL)');
let current = db.prepare('SELECT MAX(v) AS v FROM schema_version').get().v || 0;
for (; current < migrations.length; current++) {
  db.exec('BEGIN');
  try {
    db.exec(migrations[current]);
    db.prepare('INSERT INTO schema_version (v) VALUES (?)').run(current + 1);
    db.exec('COMMIT');
  } catch (e) { db.exec('ROLLBACK'); throw e; }
}

const cache = new Map();
const stmt = (sql) => { let s = cache.get(sql); if (!s) { s = db.prepare(sql); cache.set(sql, s); } return s; };
export const get = (sql, ...p) => stmt(sql).get(...p);
export const all = (sql, ...p) => stmt(sql).all(...p);
export const run = (sql, ...p) => stmt(sql).run(...p);
export const now = () => Date.now();
export const id = () => crypto.randomUUID();

export function tx(fn) {
  db.exec('BEGIN IMMEDIATE');
  try { const r = fn(); db.exec('COMMIT'); return r; } catch (e) { db.exec('ROLLBACK'); throw e; }
}

/** UPDATE helper: update('projects', id, {status:'x'}) */
export function update(table, rowId, fields) {
  const keys = Object.keys(fields);
  if (!keys.length) return;
  run(`UPDATE ${table} SET ${keys.map((k) => `${k} = ?`).join(', ')} WHERE id = ?`, ...keys.map((k) => fields[k] ?? null), rowId);
}

export const getSetting = (key, fallback) => {
  const r = get('SELECT value FROM settings WHERE key = ?', key);
  return r ? JSON.parse(r.value) : fallback;
};
export const setSetting = (key, value) =>
  run('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value', key, JSON.stringify(value));
