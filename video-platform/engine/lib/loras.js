import fs from 'node:fs';
import path from 'node:path';
import { all, get, run, now, id, parse, dataDir, sha256File } from './db.js';
import { getVariant } from './registry.js';
import { ApiError } from './jobs.js';
import { SPECIALTIES } from './router.js';

/**
 * LoRA registry. A LoRA belongs to exactly one base model variant (a Wan LoRA does not load on LTX).
 * Versions are immutable: the file is stored under its SHA-256, with the trainer, its commit, the
 * dataset snapshot and the training config that produced it, so any version can be reproduced or blamed.
 * Status flow: candidate → staging → production → retired. Only one production version per LoRA;
 * promotion to production needs a finished evaluation run that used this exact version.
 */
const FLOW = { candidate: ['staging', 'retired'], staging: ['production', 'candidate', 'retired'], production: ['retired', 'staging'], retired: ['candidate'] };

export function list() {
  return all('SELECT * FROM loras ORDER BY created_at DESC').map((l) => ({ id: l.id, slug: l.slug, name: l.name, specialty: l.specialty, baseModel: l.base_model, baseVariant: l.base_variant, trigger: l.trigger, notes: l.notes,
    versions: all('SELECT * FROM lora_versions WHERE lora_id = ? ORDER BY created_at DESC', l.id).map(pub) }));
}
const pub = (v) => ({ id: v.id, version: v.version, status: v.status, sha256: v.sha256, sizeMb: Math.round(v.size / 1048576 * 10) / 10, strength: v.strength, trainer: v.trainer, trainerCommit: v.trainer_commit, baseWeightsRef: v.base_weights_ref,
  datasetId: v.dataset_id, datasetSnapshot: v.dataset_snapshot, config: parse(v.config_json, null), evalRunId: v.eval_run_id, createdAt: v.created_at });

export function create(b) {
  if (!/^[a-z0-9][a-z0-9-]{2,60}$/.test(b.slug || '')) throw new ApiError(400, 'bad_slug');
  if (!SPECIALTIES.includes(b.specialty)) throw new ApiError(400, 'bad_specialty', SPECIALTIES);
  if (!getVariant(b.baseModel, b.baseVariant)) throw new ApiError(400, 'unknown_base_model');
  if (get('SELECT 1 FROM loras WHERE slug = ?', b.slug)) throw new ApiError(409, 'slug_taken');
  const lid = id('lora');
  run('INSERT INTO loras (id, slug, name, specialty, base_model, base_variant, trigger, notes, created_at) VALUES (?,?,?,?,?,?,?,?,?)', lid, b.slug, String(b.name || b.slug).slice(0, 120), b.specialty, b.baseModel, b.baseVariant, b.trigger ? String(b.trigger).slice(0, 60) : null, b.notes ? String(b.notes).slice(0, 2000) : null, now());
  return list().find((l) => l.id === lid);
}

/** Registers a trained file that already sits on the engine host (path), copying it into the registry store. */
export async function addVersion(slug, b) {
  const l = get('SELECT * FROM loras WHERE slug = ?', slug);
  if (!l) throw new ApiError(404, 'lora_not_found');
  if (!/^\d+\.\d+\.\d+$/.test(b.version || '')) throw new ApiError(400, 'version_must_be_semver');
  if (get('SELECT 1 FROM lora_versions WHERE lora_id = ? AND version = ?', l.id, b.version)) throw new ApiError(409, 'version_exists');
  const src = path.resolve(String(b.path || ''));
  if (!src.endsWith('.safetensors') || !fs.existsSync(src)) throw new ApiError(400, 'file_must_be_existing_safetensors'); // safetensors only: no pickled code
  for (const k of ['trainer', 'trainerCommit', 'datasetSnapshot']) if (!b[k]) throw new ApiError(400, 'provenance_required', `${k} is required so the version can be reproduced`);
  const sha = await sha256File(src);
  const dest = path.join(dataDir, 'loras', `${sha}.safetensors`);
  if (!fs.existsSync(dest)) fs.copyFileSync(src, dest);
  const vid = id('lv');
  run(`INSERT INTO lora_versions (id, lora_id, version, file, sha256, size, strength, trainer, trainer_commit, base_weights_ref, dataset_id, dataset_snapshot, config_json, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)`,
    vid, l.id, b.version, dest, sha, fs.statSync(dest).size, Number(b.strength) || 1.0, String(b.trainer), String(b.trainerCommit), b.baseWeightsRef || null, b.datasetId || null, String(b.datasetSnapshot), b.config ? JSON.stringify(b.config) : null, now());
  return pub(get('SELECT * FROM lora_versions WHERE id = ?', vid));
}

export function setStatus(slug, version, { status, evalRunId, by }) {
  const v = get('SELECT v.* FROM lora_versions v JOIN loras l ON l.id = v.lora_id WHERE l.slug = ? AND v.version = ?', slug, version);
  if (!v) throw new ApiError(404, 'version_not_found');
  if (!FLOW[v.status]?.includes(status)) throw new ApiError(400, 'bad_transition', `${v.status} → ${FLOW[v.status].join(' | ')}`);
  if (status === 'production') {
    const r = get("SELECT * FROM eval_runs WHERE id = ? AND status = 'done' AND lora_version_id = ?", evalRunId || '', v.id);
    if (!r) throw new ApiError(400, 'evaluation_required', 'a finished evaluation run of this exact version is needed before production');
    if (parse(r.summary_json, {}).gate !== 'pass') throw new ApiError(400, 'evaluation_failed', parse(r.summary_json, {}).gateReasons);
    run("UPDATE lora_versions SET status = 'retired' WHERE lora_id = ? AND status = 'production'", v.lora_id); // one production version at a time
  }
  run('UPDATE lora_versions SET status = ?, eval_run_id = COALESCE(?, eval_run_id), promoted_by = ? WHERE id = ?', status, evalRunId || null, by ? String(by).slice(0, 80) : null, v.id);
  return pub(get('SELECT * FROM lora_versions WHERE id = ?', v.id));
}
