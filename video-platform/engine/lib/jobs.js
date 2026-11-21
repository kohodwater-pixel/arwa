import fs from 'node:fs';
import path from 'node:path';
import { all, get, run, now, id, parse, dataDir } from './db.js';
import { getModel, getVariant, licenceAllows } from './registry.js';
import { selectModel } from './router.js';

export class ApiError extends Error { constructor(status, code, detail) { super(code); this.status = status; this.code = code; this.detail = detail; } }
const LEASE_MS = 90_000;      // a worker must report progress at least this often
const MAX_ATTEMPTS = 3;

/** Platform → engine: create a generation. model may be "auto". */
export function createGeneration(body) {
  const task = body.image ? 'i2v' : body.task || 't2v';
  let modelId = body.model, variantId = body.variant, reason = 'requested explicitly', specialty = body.specialty || null;
  if (!modelId || modelId === 'auto') {
    const { choice, ranked } = selectModel({ task, aspect: body.aspect, quality: body.quality, videoType: body.videoType, specialty: body.specialty, wantAudio: body.wantAudio, duration: Number(body.duration) || undefined });
    if (!choice) throw new ApiError(409, 'no_model_available', ranked.slice(0, 6).map((c) => `${c.model}/${c.variant}: ${c.blocked.join(', ')}`));
    modelId = choice.model; variantId = choice.variant; specialty = choice.specialty;
    reason = `auto: ${choice.reasons.join('; ')} (score ${choice.score})`;
  }
  const model = getModel(modelId), variant = getVariant(modelId, variantId);
  if (!model || !variant) throw new ApiError(400, 'unknown_model');
  if (!licenceAllows(model)) throw new ApiError(403, 'licence_not_accepted', model.license.notes);
  if (!variant.tasks.includes(task)) throw new ApiError(400, 'task_not_supported');
  if (!variant.sizes[body.aspect]) throw new ApiError(400, 'aspect_not_supported', Object.keys(variant.sizes));
  if (typeof body.prompt !== 'string' || body.prompt.trim().length < 3) throw new ApiError(400, 'prompt_required');

  let loraVersion = null;
  if (body.lora) {
    loraVersion = get(`SELECT v.*, l.base_model, l.base_variant, l.trigger FROM lora_versions v JOIN loras l ON l.id = v.lora_id
                       WHERE l.slug = ? AND ${body.lora.version ? 'v.version = ?' : "v.status = 'production'"} ORDER BY v.created_at DESC LIMIT 1`, ...[body.lora.slug, body.lora.version].filter(Boolean));
    if (!loraVersion) throw new ApiError(404, 'lora_not_found');
    if (loraVersion.base_model !== modelId || loraVersion.base_variant !== variantId) throw new ApiError(400, 'lora_base_mismatch', `${loraVersion.base_model}/${loraVersion.base_variant}`);
  } else if (body.autoLora !== false && specialty) {
    loraVersion = get(`SELECT v.*, l.trigger FROM lora_versions v JOIN loras l ON l.id = v.lora_id WHERE l.specialty = ? AND l.base_model = ? AND l.base_variant = ? AND v.status = 'production' ORDER BY v.created_at DESC LIMIT 1`, specialty, modelId, variantId) || null;
  }

  const jobId = id('gen');
  let inputImage = null;
  if (body.image?.base64) {
    const buf = Buffer.from(body.image.base64, 'base64');
    if (buf.length > 20 * 1024 * 1024) throw new ApiError(413, 'image_too_large');
    inputImage = path.join(dataDir, 'inputs', `${jobId}.${body.image.mime === 'image/png' ? 'png' : 'jpg'}`);
    fs.writeFileSync(inputImage, buf);
  }
  const spec = model.plan(variant, { prompt: body.prompt.trim(), negativePrompt: body.negativePrompt || '', seconds: Number(body.duration) || 5, aspect: body.aspect, seed: Number.isInteger(body.seed) ? body.seed : Math.floor(Math.random() * 2 ** 31), task });
  if (loraVersion) { spec.lora = { sha256: loraVersion.sha256, strength: loraVersion.strength, trigger: loraVersion.trigger || null }; if (loraVersion.trigger && !spec.prompt.includes(loraVersion.trigger)) spec.prompt = `${loraVersion.trigger}, ${spec.prompt}`; }
  run(`INSERT INTO jobs (id, model, variant, task, spec_json, reason, lora_version_id, input_image, client_ref, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)`,
    jobId, modelId, variantId, task, JSON.stringify(spec), reason, loraVersion?.id || null, inputImage, String(body.clientRef || '').slice(0, 120) || null, now());
  return publicJob(get('SELECT * FROM jobs WHERE id = ?', jobId));
}

export function publicJob(j) {
  if (!j) return null;
  const spec = parse(j.spec_json, {});
  return { id: j.id, status: j.status, model: j.model, variant: j.variant, task: j.task, reason: j.reason, progress: j.progress, stage: j.stage, error: j.error, mock: !!j.mock,
    seconds: spec.seconds, clipSeconds: spec.frames && spec.fps ? spec.frames / spec.fps : null, width: spec.width, height: spec.height, seed: spec.seed,
    lora: j.lora_version_id, gpuSeconds: j.gpu_seconds, attempts: j.attempts, createdAt: j.created_at, finishedAt: j.finished_at };
}

/** Puts jobs whose worker went silent back in the queue (or fails them after too many attempts). */
export function reapLeases() {
  for (const j of all("SELECT * FROM jobs WHERE status = 'running' AND lease_until < ?", now())) {
    if (j.attempts >= MAX_ATTEMPTS) run("UPDATE jobs SET status = 'failed', error = ?, finished_at = ? WHERE id = ?", 'worker stopped responding (3 attempts)', now(), j.id);
    else run("UPDATE jobs SET status = 'queued', worker_id = NULL, lease_until = NULL, progress = NULL, stage = 'requeued after worker timeout' WHERE id = ?", j.id);
    run('UPDATE workers SET current_job = NULL WHERE current_job = ?', j.id);
  }
}

/** Worker → engine: take the oldest queued job this worker can run. One job per worker at a time. */
export function claim(worker) {
  reapLeases();
  const models = parse(worker.models_json, []);
  for (const j of all("SELECT * FROM jobs WHERE status = 'queued' ORDER BY created_at LIMIT 50")) {
    const m = models.find((x) => x.id === j.model && (!x.variants || x.variants.includes(j.variant)));
    if (!m) continue;
    const taken = run("UPDATE jobs SET status = 'running', worker_id = ?, lease_until = ?, attempts = attempts + 1, started_at = COALESCE(started_at, ?), stage = 'claimed', mock = ? WHERE id = ? AND status = 'queued'", worker.id, now() + LEASE_MS, now(), worker.mock ? 1 : 0, j.id);
    if (!taken.changes) continue;
    run('UPDATE workers SET current_job = ? WHERE id = ?', j.id, worker.id);
    const lora = j.lora_version_id && get('SELECT sha256, size FROM lora_versions WHERE id = ?', j.lora_version_id);
    return { id: j.id, model: j.model, variant: j.variant, task: j.task, spec: parse(j.spec_json, {}), hasImage: !!j.input_image, lora: lora || null, leaseSeconds: LEASE_MS / 1000 };
  }
  return null;
}

const owned = (jobId, worker) => { const j = get('SELECT * FROM jobs WHERE id = ?', jobId); if (!j || j.worker_id !== worker.id) throw new ApiError(404, 'job_not_yours'); return j; };

export function progress(jobId, worker, { progress: p, stage }) {
  const j = owned(jobId, worker);
  if (j.status === 'canceled') return { cancel: true };
  run('UPDATE jobs SET progress = ?, stage = ?, lease_until = ? WHERE id = ?', typeof p === 'number' ? Math.min(1, Math.max(0, p)) : j.progress, String(stage || j.stage || '').slice(0, 120), now() + LEASE_MS, jobId);
  return { cancel: false };
}
export function complete(jobId, worker, file, { gpuSeconds, mock }) {
  const j = owned(jobId, worker);
  run("UPDATE jobs SET status = CASE WHEN status = 'canceled' THEN 'canceled' ELSE 'succeeded' END, output_file = ?, progress = 1, stage = 'done', gpu_seconds = ?, mock = ?, finished_at = ?, lease_until = NULL WHERE id = ?", file, gpuSeconds ?? null, mock ? 1 : 0, now(), j.id);
  run('UPDATE workers SET current_job = NULL WHERE id = ?', worker.id);
}
export function fail(jobId, worker, { error, retryable }) {
  const j = owned(jobId, worker);
  const again = retryable && j.attempts < MAX_ATTEMPTS;
  run(`UPDATE jobs SET status = ?, error = ?, worker_id = NULL, lease_until = NULL, finished_at = ? WHERE id = ?`, again ? 'queued' : 'failed', String(error || 'failed').slice(0, 1000), again ? null : now(), j.id);
  run('UPDATE workers SET current_job = NULL WHERE id = ?', worker.id);
}
export function cancel(jobId) {
  const j = get('SELECT * FROM jobs WHERE id = ?', jobId);
  if (!j) throw new ApiError(404, 'not_found');
  if (['queued', 'running'].includes(j.status)) run("UPDATE jobs SET status = 'canceled', finished_at = ? WHERE id = ?", now(), jobId); // a running worker learns on its next progress call
  return publicJob(get('SELECT * FROM jobs WHERE id = ?', jobId));
}
