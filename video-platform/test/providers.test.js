/**
 * Adapter contract tests. A local HTTP server answers with the response shapes documented by each
 * provider, and the adapters are pointed at it by replacing global fetch. This checks request
 * building and response parsing only — it is NOT a test against the real services.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import os from 'node:os'; import path from 'node:path'; import fs from 'node:fs';
process.env.NODE_ENV = 'test';
process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-test-'));

const runway = (await import('../server/providers/runway.js')).default;
const luma = (await import('../server/providers/luma.js')).default;
const veo = (await import('../server/providers/veo.js')).default;
const kling = (await import('../server/providers/kling.js')).default;
const { fitClip, ProviderError } = await import('../server/providers/http.js');

const calls = [];
let reply = () => [200, {}];
const server = http.createServer((req, res) => {
  let body = ''; req.on('data', (c) => (body += c));
  req.on('end', () => { const call = { method: req.method, url: req.url, headers: req.headers, body: body ? JSON.parse(body) : null }; calls.push(call); const [status, json, headers] = reply(call); res.writeHead(status, { 'content-type': 'application/json', ...(headers || {}) }); res.end(JSON.stringify(json)); });
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;
const realFetch = globalThis.fetch;
globalThis.fetch = (url, init) => { const u = new URL(url); return realFetch(`http://127.0.0.1:${port}${u.pathname}${u.search}`, { ...init, headers: { ...(init?.headers || {}), 'x-real-host': u.host } }); };
test.after(() => { server.close(); globalThis.fetch = realFetch; });
const last = () => calls.at(-1);

test('fitClip picks the smallest clip that covers the scene', () => {
  assert.equal(fitClip({ values: [4, 6, 8] }, 5), 6); assert.equal(fitClip({ values: [5, 9] }, 10), 9); assert.equal(fitClip({ min: 2, max: 10 }, 7), 7);
});

test('runway: text_to_video, image_to_video, task states', async () => {
  reply = () => [200, { id: 'task-1' }];
  const r = await runway.submit({ prompt: 'p', duration: 7, aspect: '9:16', quality: 'standard' }, { apiKey: 'k' });
  assert.deepEqual(r, { jobId: 'task-1', clipDuration: 7 });
  assert.equal(last().url, '/v1/text_to_video'); assert.equal(last().headers.authorization, 'Bearer k'); assert.equal(last().headers['x-runway-version'], '2024-11-06');
  assert.deepEqual(last().body, { model: 'gen4.5', promptText: 'p', ratio: '720:1280', duration: 7 });
  await runway.submit({ prompt: 'p', duration: 5, aspect: '16:9', quality: 'standard', image: { buffer: Buffer.from('x'), mime: 'image/png' } }, { apiKey: 'k' });
  assert.equal(last().url, '/v1/image_to_video'); assert.equal(last().body.promptImage[0].uri, 'data:image/png;base64,eA==');
  await assert.rejects(runway.submit({ prompt: 'p', duration: 5, aspect: '1:1', quality: 'standard' }, { apiKey: 'k' }), /does not support/);
  reply = () => [200, { status: 'RUNNING', progress: 0.4 }]; assert.deepEqual(await runway.poll('task-1', { apiKey: 'k' }), { status: 'running', progress: 0.4 });
  reply = () => [200, { status: 'THROTTLED' }]; assert.equal((await runway.poll('task-1', { apiKey: 'k' })).status, 'pending');
  reply = () => [200, { status: 'SUCCEEDED', output: ['https://cdn/x.mp4'] }]; assert.deepEqual(await runway.poll('task-1', { apiKey: 'k' }), { status: 'succeeded', videoUrl: 'https://cdn/x.mp4' });
  reply = () => [200, { status: 'FAILED', failure: 'blocked', failureCode: 'SAFETY.INPUT.TEXT' }]; const f = await runway.poll('task-1', { apiKey: 'k' }); assert.equal(f.status, 'failed'); assert.equal(f.retryable, false);
});

test('errors: 401 is an auth error, 429 is retryable with retry-after', async () => {
  reply = () => [401, { error: 'Invalid API key' }];
  await assert.rejects(runway.poll('t', { apiKey: 'bad' }), (e) => e instanceof ProviderError && e.code === 'provider_auth' && !e.retryable);
  reply = () => [429, { error: 'slow down' }, { 'retry-after': '7' }];
  await assert.rejects(runway.poll('t', { apiKey: 'k' }), (e) => e.retryable && e.retryAfterMs === 7000);
});

test('luma: generation body and states', async () => {
  reply = () => [200, { id: 'gen-1', state: 'queued' }];
  const r = await luma.submit({ prompt: 'p', duration: 6, aspect: '1:1', quality: 'high', image: { url: 'https://me/a.png' } }, { apiKey: 'k' });
  assert.equal(r.clipDuration, 9); assert.equal(last().url, '/dream-machine/v1/generations/video');
  assert.deepEqual(last().body, { generation_type: 'video', model: 'ray-2', prompt: 'p', aspect_ratio: '1:1', resolution: '1080p', duration: '9s', keyframes: { frame0: { type: 'image', url: 'https://me/a.png' } } });
  reply = () => [200, { state: 'dreaming' }]; assert.equal((await luma.poll('gen-1', { apiKey: 'k' })).status, 'running');
  reply = () => [200, { state: 'completed', assets: { video: 'https://cdn/l.mp4' } }]; assert.equal((await luma.poll('gen-1', { apiKey: 'k' })).videoUrl, 'https://cdn/l.mp4');
  reply = () => [200, { state: 'failed', failure_reason: 'moderation' }]; assert.equal((await luma.poll('gen-1', { apiKey: 'k' })).retryable, false);
});

test('veo: predictLongRunning body, operation polling, download header', async () => {
  reply = () => [200, { name: 'models/veo-3.1-fast-generate-preview/operations/abc' }];
  const r = await veo.submit({ prompt: 'p', negativePrompt: 'text', duration: 5, aspect: '16:9', quality: 'standard', image: { buffer: Buffer.from('x'), mime: 'image/jpeg' } }, { apiKey: 'g' });
  assert.equal(r.clipDuration, 6); assert.equal(last().url, '/v1beta/models/veo-3.1-fast-generate-preview:predictLongRunning'); assert.equal(last().headers['x-goog-api-key'], 'g');
  assert.deepEqual(last().body, { instances: [{ prompt: 'p', image: { bytesBase64Encoded: 'eA==', mimeType: 'image/jpeg' } }], parameters: { aspectRatio: '16:9', resolution: '720p', durationSeconds: 6, sampleCount: 1, negativePrompt: 'text' } });
  reply = () => [200, { name: r.jobId }]; assert.equal((await veo.poll(r.jobId, { apiKey: 'g' })).status, 'running');
  reply = () => [200, { done: true, response: { generateVideoResponse: { generatedSamples: [{ video: { uri: 'https://g/files/1:download?alt=media' } }] } } }];
  const ok = await veo.poll(r.jobId, { apiKey: 'g' }); assert.equal(ok.status, 'succeeded'); assert.deepEqual(ok.downloadHeaders, { 'x-goog-api-key': 'g' });
  reply = () => [200, { done: true, response: { generateVideoResponse: { raiMediaFilteredReasons: ['blocked'] } } }]; assert.equal((await veo.poll(r.jobId, { apiKey: 'g' })).status, 'failed');
});

test('kling: signed JWT, body, states', async () => {
  reply = () => [200, { code: 0, data: { task_id: 'kt1', task_status: 'submitted' } }];
  const r = await kling.submit({ prompt: 'p', negativePrompt: 'n', duration: 6, aspect: '9:16', quality: 'high' }, { accessKey: 'ak', secretKey: 'sk' });
  assert.equal(r.jobId, 'text2video:kt1'); assert.equal(r.clipDuration, 10);
  const [h, p] = last().headers.authorization.replace('Bearer ', '').split('.').slice(0, 2).map((x) => JSON.parse(Buffer.from(x, 'base64url')));
  assert.equal(h.alg, 'HS256'); assert.equal(p.iss, 'ak'); assert.ok(p.exp > Date.now() / 1000);
  assert.deepEqual(last().body, { model_name: 'kling-v2-6', prompt: 'p', mode: 'pro', aspect_ratio: '9:16', duration: '10', negative_prompt: 'n' });
  reply = () => [200, { code: 0, data: { task_status: 'succeed', task_result: { videos: [{ url: 'https://k/v.mp4' }] } } }]; assert.equal((await kling.poll(r.jobId, { accessKey: 'ak', secretKey: 'sk' })).videoUrl, 'https://k/v.mp4');
  reply = () => [200, { code: 1303, message: 'concurrency' }]; await assert.rejects(kling.poll(r.jobId, { accessKey: 'ak', secretKey: 'sk' }), (e) => e.retryable);
});
