/**
 * Engine control plane. A separate service from the web platform:
 *   platform ──(API key)──► this service ◄──(worker token, outbound only)── GPU workers
 * Workers pull jobs, so a rented GPU needs no inbound port and can sit behind NAT.
 * No third-party dependencies: Node's own http and sqlite.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { pipeline } from 'node:stream/promises';
import { all, get, run, now, id, parse, dataDir } from './lib/db.js';
import { models, licenceAllows, maxSeconds, minSeconds } from './lib/registry.js';
import { candidates, liveWorkers } from './lib/router.js';
import { ApiError, createGeneration, publicJob, claim, progress, complete, fail, cancel, reapLeases, ownedRunning } from './lib/jobs.js';
import * as loras from './lib/loras.js';
import * as evals from './lib/eval.js';

const PORT = Number(process.env.ENGINE_PORT || 4200);
const API_KEY = process.env.ENGINE_API_KEY || '';
const WORKER_TOKEN = process.env.ENGINE_WORKER_TOKEN || '';
if (!API_KEY || !WORKER_TOKEN) { console.error('ENGINE_API_KEY and ENGINE_WORKER_TOKEN must both be set'); process.exit(1); }
const MAX_OUTPUT = 2 * 1024 ** 3;

const safeEq = (a, b) => { const x = Buffer.from(String(a)), y = Buffer.from(String(b)); return x.length === y.length && crypto.timingSafeEqual(x, y); };
const bearer = (req) => (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
const send = (res, status, body) => { const s = JSON.stringify(body); res.writeHead(status, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(s) }); res.end(s); };
async function json(req, limit = 30 * 1024 * 1024) {
  const chunks = []; let n = 0;
  for await (const c of req) { n += c.length; if (n > limit) throw new ApiError(413, 'body_too_large'); chunks.push(c); }
  if (!n) return {};
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch { throw new ApiError(400, 'bad_json'); }
}
const log = (event, data = {}) => console.log(JSON.stringify({ ts: new Date().toISOString(), event, ...data }));

/** What the platform may offer right now: only variants that pass the licence gate AND have a live worker. */
function capabilities() {
  const workers = liveWorkers();
  return {
    workersOnline: workers.length,
    mockOnly: workers.length > 0 && workers.every((w) => w.mock),
    models: models.map((m) => ({
      id: m.id, label: m.label, licence: { ...m.license, allowed: licenceAllows(m) }, prompt: m.prompt,
      variants: m.variants.map((v) => ({
        id: v.id, label: v.label, tier: v.tier, tasks: v.tasks, aspects: Object.keys(v.sizes), fps: v.fps, audio: !!v.audio, vramGb: v.vramGb,
        clip: { min: minSeconds(v), max: maxSeconds(v) }, maxPromptChars: m.prompt.maxChars, negativePrompt: !!m.prompt.negative,
        online: workers.filter((w) => w.models.some((x) => x.id === m.id && (!x.variants || x.variants.includes(v.id)))).length,
      })),
    })),
  };
}

const hash = (t) => crypto.createHash('sha256').update(String(t)).digest('hex');
/** A worker is identified by its id AND the secret it was given when it registered; a name alone proves nothing. */
function workerOf(req) {
  const w = get('SELECT * FROM workers WHERE id = ?', req.headers['x-worker-id'] || '');
  if (!w || !w.secret_hash || !safeEq(hash(req.headers['x-worker-secret'] || ''), w.secret_hash)) throw new ApiError(401, 'unknown_worker');
  run('UPDATE workers SET last_seen = ? WHERE id = ?', now(), w.id);
  return w;
}

const routes = [
  // ── platform API ──
  ['GET', /^\/v1\/health$/, 'api', () => ({ ok: true, workersOnline: liveWorkers().length, queued: get("SELECT COUNT(*) n FROM jobs WHERE status = 'queued'").n })],
  ['GET', /^\/v1\/capabilities$/, 'api', () => capabilities()],
  ['POST', /^\/v1\/route$/, 'api', async (req) => ({ ranked: candidates({ requireOnline: false, ...(await json(req)) }) })],
  ['POST', /^\/v1\/generations$/, 'api', async (req) => { const j = createGeneration(await json(req)); log('job.created', { id: j.id, model: j.model, variant: j.variant, reason: j.reason }); return [201, j]; }],
  ['GET', /^\/v1\/generations\/([\w-]+)$/, 'api', (_r, _s, m) => { reapLeases(); const j = publicJob(get('SELECT * FROM jobs WHERE id = ?', m[1])); if (!j) throw new ApiError(404, 'not_found'); return j; }],
  ['DELETE', /^\/v1\/generations\/([\w-]+)$/, 'api', (_r, _s, m) => cancel(m[1])],
  ['GET', /^\/v1\/generations\/([\w-]+)\/content$/, 'api', (_r, res, m) => {
    const j = get('SELECT * FROM jobs WHERE id = ?', m[1]);
    if (!j || j.status !== 'succeeded' || !j.output_file || !fs.existsSync(j.output_file)) throw new ApiError(404, 'no_output');
    res.writeHead(200, { 'content-type': 'video/mp4', 'content-length': fs.statSync(j.output_file).size, 'x-engine-mock': j.mock ? '1' : '0' });
    fs.createReadStream(j.output_file).pipe(res); return null;
  }],
  ['GET', /^\/v1\/workers$/, 'api', () => ({ workers: all('SELECT * FROM workers ORDER BY last_seen DESC').map((w) => ({ id: w.id, name: w.name, gpu: w.gpu, vramGb: w.vram_gb, mock: !!w.mock, region: w.region, models: parse(w.models_json, []), online: w.last_seen > now() - 45000, currentJob: w.current_job, lastSeen: w.last_seen })) })],
  ['GET', /^\/v1\/jobs$/, 'api', () => ({ jobs: all('SELECT * FROM jobs ORDER BY created_at DESC LIMIT 100').map(publicJob) })],
  // LoRA registry
  ['GET', /^\/v1\/loras$/, 'api', () => ({ loras: loras.list() })],
  ['POST', /^\/v1\/loras$/, 'api', async (req) => [201, loras.create(await json(req))]],
  ['POST', /^\/v1\/loras\/([\w-]+)\/versions$/, 'api', async (req, _s, m) => [201, await loras.addVersion(m[1], await json(req))]],
  ['POST', /^\/v1\/loras\/([\w-]+)\/versions\/([\w.-]+)\/status$/, 'api', async (req, _s, m) => loras.setStatus(m[1], m[2], await json(req))],
  // evaluation
  ['GET', /^\/v1\/eval\/suites$/, 'api', () => ({ suites: evals.suites() })],
  ['POST', /^\/v1\/eval\/runs$/, 'api', async (req) => [201, evals.startRun(await json(req))]],
  ['GET', /^\/v1\/eval\/runs\/([\w-]+)$/, 'api', async (_r, _s, m) => evals.collect(m[1])],
  ['POST', /^\/v1\/eval\/votes$/, 'api', async (req) => [201, evals.vote(await json(req))]],
  ['GET', /^\/v1\/eval\/compare$/, 'api', (req) => evals.compare(new URL(req.url, 'http://x').searchParams.get('suite'))],

  // ── worker API ──
  ['POST', /^\/v1\/worker\/register$/, 'worker', async (req) => {
    const b = await json(req);
    if (!b.name || !Array.isArray(b.models)) throw new ApiError(400, 'bad_registration');
    const known = b.models.filter((m) => models.some((x) => x.id === m.id));
    // Re-registration keeps the same record only when the caller proves it is that worker (id + secret).
    // Otherwise a new record is created; an existing worker's id is never handed out by name.
    const prev = get('SELECT * FROM workers WHERE id = ?', String(b.workerId || ''));
    const same = prev && prev.secret_hash && safeEq(hash(b.workerSecret || ''), prev.secret_hash);
    const wid = same ? prev.id : id('wrk');
    const secret = same ? null : crypto.randomBytes(32).toString('base64url');
    run(`INSERT INTO workers (id, name, gpu, vram_gb, models_json, mock, region, registered_at, last_seen, secret_hash) VALUES (?,?,?,?,?,?,?,?,?,?)
         ON CONFLICT(id) DO UPDATE SET name = excluded.name, gpu = excluded.gpu, vram_gb = excluded.vram_gb, models_json = excluded.models_json, mock = excluded.mock, region = excluded.region, last_seen = excluded.last_seen`,
      wid, String(b.name).slice(0, 80), String(b.gpu || '').slice(0, 80), Number(b.vramGb) || null, JSON.stringify(known), b.mock ? 1 : 0, String(b.region || '').slice(0, 40), now(), now(), same ? prev.secret_hash : hash(secret));
    log('worker.registered', { id: wid, name: b.name, gpu: b.gpu, mock: !!b.mock, models: known.map((m) => m.id) });
    return { workerId: wid, ...(secret ? { workerSecret: secret } : {}), accepted: known.map((m) => m.id), ignored: b.models.filter((m) => !known.includes(m)).map((m) => m.id) };
  }],
  ['POST', /^\/v1\/worker\/claim$/, 'worker', (req) => { const job = claim(workerOf(req)); if (job) log('job.claimed', { id: job.id, worker: req.headers['x-worker-id'] }); return job ? job : [204, null]; }],
  ['POST', /^\/v1\/worker\/jobs\/([\w-]+)\/progress$/, 'worker', async (req, _s, m) => progress(m[1], workerOf(req), await json(req))],
  ['POST', /^\/v1\/worker\/jobs\/([\w-]+)\/fail$/, 'worker', async (req, _s, m) => { const b = await json(req); fail(m[1], workerOf(req), b); log('job.failed', { id: m[1], error: b.error }); return { ok: true }; }],
  ['PUT', /^\/v1\/worker\/jobs\/([\w-]+)\/result$/, 'worker', async (req, _s, m) => {
    const w = workerOf(req);
    ownedRunning(m[1], w);                                       // check BEFORE accepting a single byte
    const file = path.join(dataDir, 'outputs', `${m[1]}.mp4`);
    const part = `${file}.${crypto.randomBytes(6).toString('hex')}.part`;
    let n = 0;
    try {
      await pipeline(req, async function* (src) { for await (const c of src) { n += c.length; if (n > MAX_OUTPUT) throw new ApiError(413, 'output_too_large'); yield c; } }, fs.createWriteStream(part));
      if (n < 1000) throw new ApiError(400, 'empty_output');
      ownedRunning(m[1], w);                                     // still ours after the upload (the lease may have moved)
      fs.renameSync(part, file);
    } catch (e) { fs.rmSync(part, { force: true }); throw e; }
    complete(m[1], w, file, { gpuSeconds: Number(req.headers['x-gpu-seconds']) || null, mock: req.headers['x-mock'] === '1' || !!w.mock });
    log('job.succeeded', { id: m[1], bytes: n, mock: req.headers['x-mock'] === '1' });
    return { ok: true };
  }],
  ['GET', /^\/v1\/worker\/jobs\/([\w-]+)\/image$/, 'worker', (req, res, m) => {
    const j = ownedRunning(m[1], workerOf(req));               // only the worker that holds the job may read its input
    if (!j?.input_image || !fs.existsSync(j.input_image)) throw new ApiError(404, 'no_image');
    res.writeHead(200, { 'content-type': j.input_image.endsWith('.png') ? 'image/png' : 'image/jpeg' }); fs.createReadStream(j.input_image).pipe(res); return null;
  }],
  ['GET', /^\/v1\/worker\/loras\/([a-f0-9]{64})$/, 'worker', (req, res, m) => {
    workerOf(req); const v = get('SELECT file, size FROM lora_versions WHERE sha256 = ?', m[1]);
    if (!v || !fs.existsSync(v.file)) throw new ApiError(404, 'no_lora');
    res.writeHead(200, { 'content-type': 'application/octet-stream', 'content-length': v.size }); fs.createReadStream(v.file).pipe(res); return null;
  }],
];

export const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    const route = routes.find(([method, re]) => method === req.method && re.test(url.pathname));
    if (!route) throw new ApiError(404, 'not_found');
    const [, re, scope, handler] = route;
    if (!safeEq(bearer(req), scope === 'api' ? API_KEY : WORKER_TOKEN)) throw new ApiError(401, 'unauthorized');
    const out = await handler(req, res, url.pathname.match(re));
    if (out === null) return;                                   // handler streamed the response itself
    if (Array.isArray(out)) return out[1] === null ? (res.writeHead(out[0]), res.end()) : send(res, out[0], out[1]);
    send(res, 200, out);
  } catch (e) {
    if (res.headersSent) return res.destroy();
    if (e instanceof ApiError) return send(res, e.status, { error: e.code, detail: e.detail });
    log('error', { message: String(e?.stack || e).slice(0, 800) });
    send(res, 500, { error: 'server_error' });
  }
});
server.listen(PORT, () => log('engine.listening', { port: PORT, models: models.map((m) => m.id), policy: process.env.ENGINE_LICENSE_POLICY || 'commercial' }));
