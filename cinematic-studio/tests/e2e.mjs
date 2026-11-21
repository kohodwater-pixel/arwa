// Browser test of the real UI against the real Rust core (through the dev bridge), real SQLite and real FFmpeg.
// The only stand-in is tests/fake-comfy.mjs, which replaces the GPU server. Run: npm run build && cargo build -p studio-core --features dev-bridge && node tests/e2e.mjs
import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { startFakeComfy } from './fake-comfy.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const root = path.resolve(import.meta.dirname, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-e2e-'));
const shots = process.env.SHOTS || path.join(tmp, 'shots'); fs.mkdirSync(shots, { recursive: true });
const lib = path.join(tmp, 'Cinematic Studio'), cfg = path.join(tmp, 'config'); fs.mkdirSync(cfg);
fs.writeFileSync(path.join(cfg, 'config.json'), JSON.stringify({ library_root: lib }));
const ff = (...a) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...a]);
const clip = path.join(tmp, 'server-clip.mp4'), image = path.join(tmp, 'reference.png'), music = path.join(tmp, 'music.wav'), notMedia = path.join(tmp, 'fake.png');
ff('-f', 'lavfi', '-i', 'testsrc2=size=1280x704:rate=24:duration=3', '-pix_fmt', 'yuv420p', clip);
ff('-f', 'lavfi', '-i', 'testsrc2=size=1280x704:duration=1', '-frames:v', '1', image);
ff('-f', 'lavfi', '-i', 'sine=frequency=330:duration=20', music);
fs.writeFileSync(notMedia, 'not an image');

const PORT = 4300 + Math.floor(Math.random() * 500);
const base = `http://127.0.0.1:${PORT}`;
let bridge;
const startBridge = async () => {
  bridge = spawn(path.join(root, 'target/debug/dev-bridge'), ['--port', String(PORT), '--config', cfg, '--dist', path.join(root, 'dist')], { stdio: ['ignore', 'ignore', 'pipe'] });
  bridge.stderr.on('data', (d) => process.env.VERBOSE && process.stderr.write(d));
  for (let i = 0; i < 80; i++) { try { const r = await fetch(`${base}/rpc`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"cmd":"app_status","args":{}}' }); if (r.ok) return; } catch { /* not up yet */ } await new Promise((r) => setTimeout(r, 100)); }
  throw new Error('bridge did not start');
};
const rpc = async (cmd, args = {}) => { const r = await (await fetch(`${base}/rpc`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cmd, args }) })).json(); if (!r.ok) throw new Error(`${cmd}: ${r.error.code}`); return r.data; };

const results = [];
let page, browser;
const step = async (name, fn) => { try { await fn(); results.push([true, name]); console.log(`  ok   ${name}`); } catch (e) { results.push([false, name]); console.log(`  FAIL ${name}\n       ${String(e.message).split('\n')[0]}`); await page?.screenshot({ path: path.join(shots, `FAIL-${results.length}.png`) }).catch(() => {}); } };
const expect = (cond, msg) => { if (!cond) throw new Error(msg); };
const shot = (name) => page.screenshot({ path: path.join(shots, `${name}.png`) });
const nav = (id) => page.click(`[data-nav="${id}"]`);
const waitJobs = async (pred, ms = 60000) => { const t = Date.now(); for (;;) { const j = await rpc('jobs_list'); if (pred(j)) return j; if (Date.now() - t > ms) throw new Error(`jobs timeout: ${JSON.stringify(j.map((x) => [x.kind, x.status, x.blocked_reason, x.error]))}`); await new Promise((r) => setTimeout(r, 300)); } };
let promptAnswers = [];

const comfy = await startFakeComfy(clip);
await startBridge();
browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
page = await ctx.newPage();
const consoleErrors = [];
page.on('console', (m) => m.type() === 'error' && !/Failed to load resource|ERR_/.test(m.text()) && consoleErrors.push(m.text()));
page.on('pageerror', (e) => consoleErrors.push(String(e)));
page.on('dialog', (d) => d.accept(promptAnswers.shift() || ''));
let projectId;

await step('opens in Arabic, right to left, with an empty studio and the six library folders', async () => {
  await page.goto(base);
  await page.waitForSelector('[data-view="dashboard"]');
  expect(await page.evaluate(() => document.documentElement.dir) === 'rtl', 'not rtl');
  for (const d of ['Projects', 'Assets', 'Models', 'Cache', 'Logs', 'Backups']) expect(fs.statSync(path.join(lib, d)).isDirectory(), d);
  expect(fs.existsSync(path.join(lib, 'cinematic-studio.db')), 'db');
  await shot('01-dashboard-empty');
});
await step('creates a project from an Arabic idea', async () => {
  await page.click('[data-action="new-project"]');
  await page.fill('[data-field="name"]', 'إعلان سيارة الرياض');
  await page.fill('[data-field="description"]', 'سيارة رياضية سوداء تسير بسرعة في شوارع الرياض ليلًا تحت المطر مع أضواء نيون وأجواء فاخرة');
  await page.click('[data-action="create-project"]');
  await page.waitForSelector('[data-view="creator"]');
  const list = await rpc('projects_list'); projectId = list[0].id;
  expect(fs.existsSync(path.join(lib, list[0].folder, 'project.json')), 'project.json snapshot');
});
await step('the director turns it into twelve English decisions and a storyboard', async () => {
  await page.click('[data-action="direct"]');
  await page.waitForSelector('[data-director]');
  const text = await page.textContent('[data-director]');
  expect(/sports car/.test(text) && /Riyadh/.test(text) && /Neon/.test(text), 'decisions missing');
  expect((await page.locator('[data-draft-scenes] li').count()) === 3, 'expected 3 scenes');
  await shot('02-creator');
  await page.click('[data-action="save-storyboard"]');
  await page.waitForSelector('[data-storyboard]');
  expect((await page.locator('[data-scene]').count()) === 3, 'storyboard scenes');
  const p = await rpc('project_get', { id: projectId });
  expect(p.scenes.every((s) => s.prompt && !/[؀-ۿ]/.test(s.prompt)), 'prompts must be English');
  expect(p.director.lighting.includes('Neon'), 'director saved');
});
await step('without a server, generation waits and nothing is faked', async () => {
  await page.click('[data-action="generate-missing"]');
  const jobs = await waitJobs((j) => j.length === 3 && j.every((x) => x.status === 'blocked' || x.status === 'queued') && j.some((x) => x.status === 'blocked'));
  expect(jobs.find((x) => x.status === 'blocked').blocked_reason === 'comfy_not_configured', 'reason');
  const p = await rpc('project_get', { id: projectId });
  expect(p.scenes.every((s) => !s.video_path), 'no video may exist');
  await nav('queue');
  await page.waitForSelector('[data-job="blocked"]');
  await shot('03-queue-waiting');
});
await step('settings refuse an unencrypted remote server', async () => {
  await nav('settings');
  await page.fill('[data-field="comfy_url"]', 'http://203.0.113.9:8188');
  expect(await page.isDisabled('[data-action="save-comfy"]'), 'save should be disabled');
  let refused = false; try { await rpc('setting_set', { key: 'comfy_url', value: 'http://203.0.113.9:8188' }); } catch (e) { refused = /insecure_url/.test(e.message); }
  expect(refused, 'core must refuse too');
});
await step('connects to the server and the waiting jobs run to verified clips', async () => {
  await page.fill('[data-field="comfy_url"]', comfy.url);
  await page.click('[data-action="save-comfy"]');
  await page.waitForSelector('[data-comfy-ok]');
  await shot('04-settings-connected');
  await waitJobs((j) => j.filter((x) => x.kind === 'generate').every((x) => x.status === 'succeeded'), 90000);
  const p = await rpc('project_get', { id: projectId });
  expect(p.scenes.every((s) => s.status === 'completed' && s.video_path && s.preview_path), 'scenes completed');
  for (const s of p.scenes) { const f = path.join(lib, s.video_path); expect(fs.statSync(f).size > 1000, 'clip on disk'); expect(Math.abs(s.video_duration - 3) < 0.2, 'probed duration'); }
  expect(comfy.state.prompts.length === 3, 'three submissions, none twice');
  expect(comfy.state.prompts[0].graph.unet.inputs.unet_name === 'wan2.2_ti2v_5B_fp16.safetensors', 'Wan 2.2 graph');
});
await step('storyboard shows the clips; the web view can read them through the core', async () => {
  await nav('storyboard');
  await page.waitForSelector('[data-scene] video');
  const src = await page.getAttribute('[data-scene] video', 'src');
  const r = await page.evaluate(async (u) => { const x = await fetch(u); return { status: x.status, type: x.headers.get('content-type'), size: (await x.arrayBuffer()).byteLength }; }, src);
  expect([200, 206].includes(r.status) && r.type === 'video/mp4' && r.size > 1000, JSON.stringify(r));
  const denied = await page.evaluate(async () => (await fetch('/file?path=' + encodeURIComponent('/etc/passwd'))).status);
  expect(denied === 403, 'files outside the library must be refused');
  await shot('05-storyboard');
});
await step('storyboard editing: add, reorder, new take, delete', async () => {
  await page.click('[data-action="add-scene"]');
  await page.waitForFunction(() => document.querySelectorAll('[data-scene]').length === 4);
  let p = await rpc('project_get', { id: projectId });
  const added = p.scenes[3].id;
  await page.click(`[data-scene="${added}"] button[aria-label="قدّم المشهد"]`);
  await page.waitForFunction((id) => document.querySelectorAll('[data-scene]')[2]?.getAttribute('data-scene') === id, added);
  await page.click(`[data-scene="${added}"] [data-action="delete"]`);
  await page.click('[role="dialog"] button:has-text("حذف")');
  await page.waitForFunction(() => document.querySelectorAll('[data-scene]').length === 3);
  const before = p.scenes[1];
  await page.click(`[data-scene="${before.id}"] [data-action="new-take"]`);
  await page.waitForFunction(async () => true);
  for (let i = 0; i < 30; i++) { p = await rpc('project_get', { id: projectId }); if (p.scenes[1].prompt !== before.prompt) break; await new Promise((r) => setTimeout(r, 100)); }
  expect(p.scenes[1].prompt !== before.prompt && p.scenes[1].status === 'pending', 'new take must change the prompt and retire the clip');
  expect(fs.readdirSync(path.join(lib, p.folder, 'scenes', '_replaced')).length >= 1, 'old clip kept aside');
});
await step('scene editor: a directing change rewrites the prompt; a hand edit is kept', async () => {
  const p0 = await rpc('project_get', { id: projectId });
  const s = p0.scenes[1];
  await page.click(`[data-scene="${s.id}"] [data-action="edit"]`);
  await page.waitForSelector('[data-view="scene"]');
  await page.selectOption('[data-field="camera_move"]', 'orbit');
  await page.waitForFunction(() => /orbit/i.test(document.querySelector('[data-field="prompt"]').value));
  await page.waitForSelector('[data-save-state="saved"]');
  await page.fill('[data-field="prompt"]', 'Hand written prompt for the test.');
  await new Promise((r) => setTimeout(r, 900)); await page.waitForSelector('[data-save-state="saved"]');
  const p = await rpc('project_get', { id: projectId });
  expect(p.scenes[1].prompt === 'Hand written prompt for the test.' && p.scenes[1].prompt_edited === 1 && p.scenes[1].camera_move === 'orbit', 'saved');
  await page.click('[data-action="generate-scene"]');
  await waitJobs((j) => j.filter((x) => x.kind === 'generate').every((x) => x.status === 'succeeded') && j.length === 4, 60000);
  await page.waitForSelector('[data-scene-video]');
  expect(comfy.state.prompts.at(-1).graph.pos.inputs.text === 'Hand written prompt for the test.', 'the edited prompt is what was sent');
  await shot('06-scene-editor');
});
await step('prompt editor: changing a decision updates un-edited scenes only', async () => {
  await nav('prompt');
  await page.fill('[data-director-field="lighting"]', 'Hard noon sunlight with crisp shadows');
  await page.waitForFunction(() => !document.querySelector('[data-action="apply-prompts"]').disabled);
  await shot('07-prompt-editor');
  await page.click('[data-action="apply-prompts"]');
  for (let i = 0; i < 40; i++) { const p = await rpc('project_get', { id: projectId }); if (p.scenes[0].prompt.includes('Hard noon sunlight')) break; await new Promise((r) => setTimeout(r, 150)); }
  const p = await rpc('project_get', { id: projectId });
  expect(p.scenes[0].prompt.includes('Hard noon sunlight') && p.scenes[2].prompt.includes('Hard noon sunlight'), 'un-edited scenes rewritten');
  expect(p.scenes[1].prompt === 'Hand written prompt for the test.', 'hand-edited scene untouched');
  await rpc('generate', { project_id: projectId });
  await waitJobs((j) => j.every((x) => x.status === 'succeeded'), 90000);
});
await step('media library: import, type check by content, duplicates, search, originals untouched', async () => {
  await nav('media');
  promptAnswers = [[image, music, notMedia].join(';')];
  await page.click('[data-action="import-media"]');
  await page.waitForFunction(() => document.querySelectorAll('[data-media]').length === 2);
  await page.waitForSelector('[data-toast="bad"]');
  promptAnswers = [image];
  await page.click('[data-action="import-media"]');
  await page.waitForSelector('[data-toast="info"]:has-text("مكرر")');
  expect((await rpc('media_list')).items.length === 2, 'duplicate not added');
  await page.fill('[data-field="search"]', 'music');
  await page.waitForFunction(() => document.querySelectorAll('[data-media]').length === 1);
  await page.fill('[data-field="search"]', '');
  await page.click('[data-kind="image"]');
  await page.waitForFunction(() => document.querySelectorAll('[data-media]').length === 1);
  await page.click('[data-media]');
  await page.waitForSelector('aside img');
  expect(fs.existsSync(image) && fs.existsSync(music), 'originals stay in place');
  expect(fs.readdirSync(path.join(lib, 'Cache', 'thumbs')).length >= 1, 'thumbnail in Cache');
  await shot('08-media');
});
await step('audio studio and timeline: music on its track, a transition, trims', async () => {
  await nav('audio');
  await page.click('[data-add-audio="music"]');
  await page.click('[role="dialog"] [data-media]');
  await page.waitForSelector('[data-audio-item]');
  await nav('timeline');
  await page.waitForSelector('[data-clip="1"]');
  await page.click('[data-clip="1"]');
  await page.selectOption('[data-field="transition"]', 'fade');
  await page.fill('[data-field="trim_out"]', '2.5');
  await new Promise((r) => setTimeout(r, 800)); await page.waitForSelector('[data-save-state="saved"]');
  const t = (await rpc('timeline_get', { project_id: projectId })).timeline;
  expect(t.clips.length === 3 && t.clips[1].transition.kind === 'fade' && t.clips[1].trim_out === 2.5 && t.audio.length === 1 && t.audio[0].track === 'music', JSON.stringify(t));
  await shot('09-timeline');
});
await step('export: FFmpeg renders a playable MP4 with the audio track and a metadata file', async () => {
  await nav('export');
  await page.selectOption('[data-field="preset"]', '720p');
  await new Promise((r) => setTimeout(r, 800));
  await page.click('[data-action="export"]');
  await waitJobs((j) => j.some((x) => x.kind === 'export' && ['succeeded', 'failed'].includes(x.status)), 120000);
  const p = await rpc('project_get', { id: projectId });
  const e = p.exports[0];
  expect(e.status === 'completed', `export ${e.status}: ${e.error}`);
  const file = path.join(lib, e.path);
  const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_streams', '-show_format', '-of', 'json', file]).toString());
  const v = probe.streams.find((s) => s.codec_type === 'video'), a = probe.streams.find((s) => s.codec_type === 'audio');
  expect(v.codec_name === 'h264' && v.width === 1280 && v.height === 720 && a, 'h264 720p with audio');
  expect(Math.abs(Number(probe.format.duration) - 8) < 0.25, `3 + 2.5 − 0.5 (fade) + 3 = 8 s, got ${probe.format.duration}`);
  execFileSync('ffmpeg', ['-v', 'error', '-xerror', '-i', file, '-f', 'null', '-']);
  expect(fs.existsSync(file.replace(/\.mp4$/, '.json')), 'metadata sidecar');
  await page.waitForSelector('[data-export="completed"]');
  await shot('10-export');
  await nav('preview');
  await page.waitForSelector('[data-preview]');
  await shot('11-preview');
});
await step('GPU manager: budget 1000 SAR, nothing starts without configuration and approval', async () => {
  await nav('gpu');
  await page.waitForSelector('[data-budget-spent]');
  expect(/1000 SAR/.test(await page.textContent('[data-budget-spent]')), 'budget limit');
  expect((await page.locator('[data-action="gpu-start"]').count()) === 0, 'no start button while not configured');
  let code = ''; try { await rpc('gpu_start', {}); } catch (e) { code = e.message; }
  expect(/approval_required/.test(code), 'core refuses a start without approval');
  await shot('12-gpu');
  await nav('models');
  await page.waitForSelector('[data-models]');
  await page.waitForFunction(() => /جاهز على الخادم/.test(document.querySelector('[data-models]').textContent));
  await shot('13-models');
});
await step('English: the interface switches to left-to-right', async () => {
  await page.click('[data-lang="en"]');
  await page.waitForFunction(() => document.documentElement.dir === 'ltr');
  await nav('dashboard');
  await page.waitForSelector('text=All projects');
  await shot('14-dashboard-en');
  await page.click('[data-lang="ar"]');
});
await step('crash and restart: everything is still there and the app says it recovered', async () => {
  await rpc('generate', { project_id: projectId, all: true });
  await waitJobs((j) => j.some((x) => ['submitted', 'running'].includes(x.status)), 20000).catch(() => {});
  bridge.kill('SIGKILL');
  await new Promise((r) => setTimeout(r, 400));
  await startBridge();
  const st = await rpc('app_status');
  expect(st.recovered === true, 'recovered flag');
  expect(st.settings.comfy_url === comfy.url, 'settings kept');
  const p = await rpc('project_get', { id: projectId });
  expect(p.name === 'إعلان سيارة الرياض' && p.scenes.length === 3 && p.exports.length === 1 && p.director, 'project intact');
  await page.reload();
  await page.waitForSelector('[data-open-last]');
  expect(/غير طبيعي/.test(await page.textContent('main')), 'recovery notice');
  await shot('15-recovered');
  await waitJobs((j) => j.every((x) => !['queued', 'submitted', 'running', 'downloading', 'blocked'].includes(x.status)), 90000);
  const subs = comfy.state.prompts.length;
  expect(subs <= 4 + 3 + 3 + 1, `no duplicate submissions after restart (${subs})`);
  await page.click('[data-open-last]');
  await page.waitForSelector('[data-storyboard]');
});
await step('duplicate, back up and delete a project (files are kept)', async () => {
  const copy = await rpc('project_duplicate', { id: projectId });
  const b = await rpc('project_backup', { id: projectId });
  expect(fs.statSync(b.path).size > 1000, 'backup zip');
  await nav('dashboard');
  await page.waitForSelector(`[data-project="${copy.id}"]`);
  await page.click(`[data-delete="${copy.id}"]`);
  await page.click('[role="dialog"] button:has-text("حذف")');
  await page.waitForFunction((id) => !document.querySelector(`[data-project="${id}"]`), copy.id);
  expect(fs.readdirSync(path.join(lib, 'Backups', 'Deleted')).length === 1, 'deleted project kept under Backups/Deleted');
  await shot('16-dashboard');
});
await step('no errors in the browser console', async () => { expect(consoleErrors.length === 0, consoleErrors.slice(0, 3).join(' | ')); });

await browser.close(); bridge.kill(); comfy.close();
const failed = results.filter(([ok]) => !ok).length;
console.log(`\n${results.length - failed} passed, ${failed} failed · screenshots: ${shots}`);
process.exit(failed ? 1 : 0);
