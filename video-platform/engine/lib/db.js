import path from 'node:path';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';

/** Engine control-plane database. Separate from the platform's database on purpose: the engine is its own service. */
export const dataDir = path.resolve(process.env.ENGINE_DATA_DIR || path.join(import.meta.dirname, '..', 'data'));
fs.mkdirSync(path.join(dataDir, 'outputs'), { recursive: true });
fs.mkdirSync(path.join(dataDir, 'loras'), { recursive: true });
fs.mkdirSync(path.join(dataDir, 'inputs'), { recursive: true });

export const db = new DatabaseSync(path.join(dataDir, 'engine.db'));
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA busy_timeout = 5000;');
db.exec(`
CREATE TABLE IF NOT EXISTS workers (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, gpu TEXT, vram_gb REAL, models_json TEXT NOT NULL,
  mock INTEGER NOT NULL DEFAULT 0, region TEXT, registered_at INTEGER NOT NULL, last_seen INTEGER NOT NULL, current_job TEXT
);
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY, status TEXT NOT NULL DEFAULT 'queued',          -- queued | running | succeeded | failed | canceled
  model TEXT NOT NULL, variant TEXT NOT NULL, task TEXT NOT NULL, spec_json TEXT NOT NULL, reason TEXT,
  lora_version_id TEXT, input_image TEXT, client_ref TEXT,
  worker_id TEXT, lease_until INTEGER, attempts INTEGER NOT NULL DEFAULT 0, progress REAL, stage TEXT,
  output_file TEXT, mock INTEGER NOT NULL DEFAULT 0, gpu_seconds REAL, error TEXT,
  created_at INTEGER NOT NULL, started_at INTEGER, finished_at INTEGER
);
CREATE INDEX IF NOT EXISTS jobs_status ON jobs(status, created_at);

-- LoRA registry: a LoRA is a named specialisation; each training run that is kept is a version.
CREATE TABLE IF NOT EXISTS loras (
  id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL, specialty TEXT NOT NULL,
  base_model TEXT NOT NULL, base_variant TEXT NOT NULL, trigger TEXT, notes TEXT, created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS lora_versions (
  id TEXT PRIMARY KEY, lora_id TEXT NOT NULL REFERENCES loras(id) ON DELETE CASCADE, version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'candidate',                             -- candidate | staging | production | retired
  file TEXT NOT NULL, sha256 TEXT NOT NULL, size INTEGER NOT NULL, strength REAL NOT NULL DEFAULT 1.0,
  trainer TEXT, trainer_commit TEXT, base_weights_ref TEXT, dataset_id TEXT, dataset_snapshot TEXT,
  config_json TEXT, eval_run_id TEXT, promoted_by TEXT, created_at INTEGER NOT NULL,
  UNIQUE (lora_id, version)
);

-- Dataset management: every clip carries its rights record; nothing is exported for training without one.
CREATE TABLE IF NOT EXISTS datasets (
  id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL, specialty TEXT NOT NULL,
  target_json TEXT NOT NULL, created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS dataset_items (
  id TEXT PRIMARY KEY, dataset_id TEXT NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
  file TEXT NOT NULL, sha256 TEXT NOT NULL, kind TEXT NOT NULL,          -- video | image
  duration REAL, width INTEGER, height INTEGER, fps REAL, has_audio INTEGER,
  scene_cuts INTEGER, checks_json TEXT, status TEXT NOT NULL DEFAULT 'pending',  -- pending | approved | rejected
  reject_reason TEXT, caption TEXT, caption_source TEXT, split TEXT NOT NULL DEFAULT 'train',
  rights_source TEXT, rights_holder TEXT, rights_license TEXT, rights_people_consent TEXT, rights_doc TEXT,
  added_at INTEGER NOT NULL, UNIQUE (dataset_id, sha256)
);

-- Evaluation: one run = one configuration (model + variant + optional LoRA) over a fixed prompt suite.
CREATE TABLE IF NOT EXISTS eval_runs (
  id TEXT PRIMARY KEY, suite TEXT NOT NULL, label TEXT NOT NULL, model TEXT NOT NULL, variant TEXT NOT NULL,
  lora_version_id TEXT, seeds_json TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'running', summary_json TEXT, created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS eval_samples (
  id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES eval_runs(id) ON DELETE CASCADE, prompt_id TEXT NOT NULL, seed INTEGER NOT NULL,
  job_id TEXT, metrics_json TEXT, gpu_seconds REAL
);
CREATE TABLE IF NOT EXISTS eval_votes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, suite TEXT NOT NULL, prompt_id TEXT NOT NULL, seed INTEGER NOT NULL,
  run_a TEXT NOT NULL, run_b TEXT NOT NULL, winner TEXT NOT NULL,       -- 'a' | 'b' | 'tie'
  criterion TEXT NOT NULL, rater TEXT, created_at INTEGER NOT NULL
);
`);

const cache = new Map();
const st = (sql) => { let s = cache.get(sql); if (!s) { s = db.prepare(sql); cache.set(sql, s); } return s; };
export const get = (sql, ...p) => st(sql).get(...p);
export const all = (sql, ...p) => st(sql).all(...p);
export const run = (sql, ...p) => st(sql).run(...p);
export const now = () => Date.now();
export const id = (prefix) => `${prefix}_${crypto.randomBytes(9).toString('base64url')}`;
export const sha256File = (file) => new Promise((res, rej) => { const h = crypto.createHash('sha256'); fs.createReadStream(file).on('data', (d) => h.update(d)).on('end', () => res(h.digest('hex'))).on('error', rej); });
export const parse = (s, d) => { try { return s ? JSON.parse(s) : d; } catch { return d; } };
