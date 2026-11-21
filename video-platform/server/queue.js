import { all, get, run, update, now, id } from './db.js';
import { config } from './config.js';
import * as log from './log.js';

/**
 * Durable job queue on SQLite. Jobs survive restarts: a job that was running when the process
 * stopped is put back in the queue and resumes from its stored provider job id, so nothing is
 * submitted twice. The interface (register / enqueue) is small on purpose, so the queue can be
 * replaced by Redis/BullMQ or a cloud queue when several worker processes are needed.
 *
 * A handler returns { done: true } or { again: ms } (run me again later), or throws.
 * Thrown errors with `retryable: true` are retried with exponential backoff up to max_attempts.
 */
const handlers = new Map();
const failHooks = new Map();
let inflight = 0, timer = null;

export function register(type, handler, onFail) { handlers.set(type, handler); if (onFail) failHooks.set(type, onFail); }

export function enqueue({ type, userId, projectId, sceneId = null, providerId = null, payload = {}, maxAttempts = 3, delayMs = 0 }) {
  const jobId = id(), t = now();
  run(`INSERT INTO jobs (id, type, user_id, project_id, scene_id, status, attempts, max_attempts, run_at, provider_id, payload_json, created_at, updated_at)
       VALUES (?,?,?,?,?, 'queued', 0, ?, ?, ?, ?, ?, ?)`, jobId, type, userId, projectId, sceneId, maxAttempts, t + delayMs, providerId, JSON.stringify(payload), t, t);
  return jobId;
}

const backoff = (attempt) => Math.min(120_000, 5000 * 2 ** attempt);

async function execute(job) {
  const ctx = { userId: job.user_id, projectId: job.project_id, jobId: job.id };
  try {
    const handler = handlers.get(job.type);
    if (!handler) throw new Error(`no handler for job type ${job.type}`);
    const result = await handler(job);
    const fresh = get('SELECT status FROM jobs WHERE id = ?', job.id);
    if (!fresh || fresh.status === 'canceled') return;
    if (result?.done) update('jobs', job.id, { status: 'succeeded', progress: 1, finished_at: now(), updated_at: now(), error: null });
    else update('jobs', job.id, { status: 'queued', run_at: now() + (result?.again ?? config.pollIntervalMs), updated_at: now() });
  } catch (e) {
    const fresh = get('SELECT * FROM jobs WHERE id = ?', job.id);
    if (!fresh || fresh.status === 'canceled') return;
    const message = String(e?.message || e).slice(0, 800);
    const attempts = fresh.attempts + 1;
    if (e?.retryable && attempts < fresh.max_attempts) {
      const wait = e.retryAfterMs || backoff(attempts);
      update('jobs', job.id, { status: 'queued', attempts, provider_job_id: null, progress: null, run_at: now() + wait, error: message, updated_at: now() });
      log.warn('job.retry', message, { ...ctx, attempt: attempts, waitMs: wait, type: job.type });
    } else {
      update('jobs', job.id, { status: 'failed', attempts, error: message, finished_at: now(), updated_at: now() });
      log.error('job.failed', message, { ...ctx, type: job.type, code: e?.code });
      try { failHooks.get(job.type)?.(fresh, e); } catch (hookErr) { log.error('job.fail_hook', String(hookErr.message || hookErr), ctx); }
    }
  }
}

function tick() {
  const free = config.queueConcurrency - inflight;
  if (free <= 0) return;
  const due = all("SELECT * FROM jobs WHERE status = 'queued' AND run_at <= ? ORDER BY run_at LIMIT ?", now(), free);
  for (const job of due) {
    const claimed = run("UPDATE jobs SET status = 'running', started_at = COALESCE(started_at, ?), updated_at = ? WHERE id = ? AND status = 'queued'", now(), now(), job.id);
    if (!claimed.changes) continue;
    inflight++;
    execute(job).finally(() => { inflight--; });
  }
}

export function startWorker() {
  const stuck = run("UPDATE jobs SET status = 'queued', run_at = ? WHERE status = 'running'", now());
  if (stuck.changes) log.info('queue.recovered', `${stuck.changes} job(s) resumed after restart`);
  timer = setInterval(() => { try { tick(); } catch (e) { log.error('queue.tick', String(e.message || e)); } }, config.queueTickMs);
  timer.unref?.();
}
export function stopWorker() { clearInterval(timer); }

/** Cancels every unfinished job of a project; returns them so the caller can cancel at the provider. */
export function cancelProjectJobs(projectId, sceneId = null) {
  const jobs = sceneId
    ? all("SELECT * FROM jobs WHERE project_id = ? AND scene_id = ? AND status IN ('queued','running')", projectId, sceneId)
    : all("SELECT * FROM jobs WHERE project_id = ? AND status IN ('queued','running')", projectId);
  for (const j of jobs) update('jobs', j.id, { status: 'canceled', finished_at: now(), updated_at: now() });
  return jobs;
}
export const activeJobs = (projectId, type) => all("SELECT * FROM jobs WHERE project_id = ? AND type = ? AND status IN ('queued','running')", projectId, type);
