import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
import { execFileSync } from 'node:child_process';

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'engine-test-'));
process.env.ENGINE_DATA_DIR = path.join(tmp, 'data');
delete process.env.ENGINE_LICENSE_POLICY; delete process.env.ENGINE_ACCEPTED_LICENCES;

const { run, get, now } = await import('../lib/db.js');
const { models, getVariant, framesFor, licenceAllows } = await import('../lib/registry.js');
const { selectModel, candidates } = await import('../lib/router.js');
const jobs = await import('../lib/jobs.js');
const loras = await import('../lib/loras.js');
const evals = await import('../lib/eval.js');
const datasets = await import('../lib/datasets.js');

const clip = (file, { w = 1280, h = 720, d = 5, fps = 16, cut = false } = {}) => execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', cut ? `testsrc2=s=${w}x${h}:r=${fps}:d=${d / 2}` : `testsrc2=s=${w}x${h}:r=${fps}:d=${d}`,
  ...(cut ? ['-f', 'lavfi', '-i', `color=c=red:s=${w}x${h}:r=${fps}:d=${d / 2}`, '-filter_complex', '[0:v][1:v]concat=n=2:v=1[v]', '-map', '[v]'] : []), '-pix_fmt', 'yuv420p', file]);
const worker = (name, list, mock = 0) => run('INSERT INTO workers (id, name, gpu, vram_gb, models_json, mock, registered_at, last_seen) VALUES (?,?,?,?,?,?,?,?)', name, name, 'test', 80, JSON.stringify(list), mock, now(), now());

test('frame planning follows each model rule and never exceeds its maximum', () => {
  assert.equal(framesFor(getVariant('wan22', 'ti2v-5b'), 5), 121);      // 24 fps, 4n+1
  assert.equal(framesFor(getVariant('wan22', 'a14b-720p'), 5), 81);     // 16 fps, 4n+1
  assert.equal(framesFor(getVariant('wan22', 'a14b-720p'), 3), 49);
  assert.equal(framesFor(getVariant('ltx2', 'distilled'), 4), 97);      // 8k+1
  assert.equal(framesFor(getVariant('wan22', 'a14b-720p'), 30), 81);    // capped
  for (const m of models) for (const v of m.variants) for (const s of [1, 2, 3, 4, 5]) { const n = framesFor(v, s); assert.equal((n - v.frames.offset) % v.frames.step, 0, `${m.id}/${v.id}`); }
});

test('licence gate: Apache models pass; conditional licences need an explicit acceptance', () => {
  const by = (id) => models.find((m) => m.id === id);
  assert.equal(licenceAllows(by('wan22')), true);
  assert.equal(licenceAllows(by('ltx2')), false);
  assert.equal(licenceAllows(by('hunyuan15')), false);
  process.env.ENGINE_ACCEPTED_LICENCES = 'hunyuan15';
  assert.equal(licenceAllows(by('hunyuan15')), true);
  delete process.env.ENGINE_ACCEPTED_LICENCES;
});

test('router: nothing without a worker; then picks by tier, task, duration and explains itself', () => {
  assert.equal(selectModel({ aspect: '16:9', quality: 'standard', videoType: 'commercial' }).choice, null);
  worker('w-5b', [{ id: 'wan22', variants: ['ti2v-5b'] }]);
  worker('w-a14', [{ id: 'wan22', variants: ['a14b-720p'] }, { id: 'ltx2' }]);
  let r = selectModel({ aspect: '16:9', quality: 'standard', videoType: 'commercial', duration: 5 });
  assert.equal(`${r.choice.model}/${r.choice.variant}`, 'wan22/ti2v-5b');
  r = selectModel({ aspect: '9:16', quality: 'high', videoType: 'real_estate', task: 'i2v' });
  assert.equal(`${r.choice.model}/${r.choice.variant}`, 'wan22/a14b-720p');
  assert.match(r.choice.reasons.join(' '), /starting assumptions/);
  assert.ok(candidates({ aspect: '16:9', quality: 'high' }).find((c) => c.model === 'ltx2' && c.variant === 'dfr').blocked.some((b) => b.startsWith('licence')), 'a worker having LTX does not bypass the licence gate');
  assert.equal(selectModel({ aspect: '16:9', quality: 'high', duration: 8 }).choice, null, 'no variant online covers 8 s');
  assert.equal(selectModel({ aspect: '1:1', quality: 'standard' }).choice, null, 'no licensed variant online does 1:1');
});

test('jobs: create → claim → progress → complete; lease expiry requeues; mock is recorded', () => {
  const j = jobs.createGeneration({ model: 'auto', quality: 'standard', aspect: '16:9', duration: 5, prompt: 'A white SUV at night', videoType: 'commercial' });
  assert.equal(j.variant, 'ti2v-5b'); assert.equal(j.clipSeconds, 121 / 24);
  assert.throws(() => jobs.createGeneration({ model: 'ltx2', variant: 'distilled', aspect: '16:9', prompt: 'x y z' }), (e) => e.code === 'licence_not_accepted');
  assert.throws(() => jobs.createGeneration({ model: 'wan22', variant: 'ti2v-5b', aspect: '1:1', prompt: 'x y z' }), (e) => e.code === 'aspect_not_supported');
  const w5 = get('SELECT * FROM workers WHERE id = ?', 'w-5b'), wa = get('SELECT * FROM workers WHERE id = ?', 'w-a14');
  assert.equal(jobs.claim(wa), null, 'a worker without the variant gets nothing');
  const c = jobs.claim(w5); assert.equal(c.id, j.id); assert.equal(c.spec.wanTask, 'ti2v-5B'); assert.equal(c.spec.size, '1280*704');
  assert.equal(jobs.claim(w5), null);
  run('UPDATE jobs SET lease_until = ? WHERE id = ?', now() - 1, j.id);               // worker went silent
  jobs.reapLeases(); assert.equal(get('SELECT status FROM jobs WHERE id = ?', j.id).status, 'queued');
  const c2 = jobs.claim(w5); assert.equal(c2.id, j.id);
  assert.deepEqual(jobs.progress(j.id, w5, { progress: 0.5, stage: 'generating' }), { cancel: false });
  assert.throws(() => jobs.progress(j.id, wa, {}), (e) => e.code === 'job_not_yours');
  jobs.complete(j.id, w5, '/nonexistent.mp4', { gpuSeconds: 12, mock: false });
  const done = jobs.publicJob(get('SELECT * FROM jobs WHERE id = ?', j.id));
  assert.equal(done.status, 'succeeded'); assert.equal(done.attempts, 2); assert.equal(done.mock, false);
});

test('evaluation: technical gate scores real clips; Bradley–Terry ranks votes', async () => {
  const good = path.join(tmp, 'good.mp4'); clip(good, { w: 1280, h: 704, d: 5, fps: 24 });
  const spec = { width: 1280, height: 704, frames: 120, fps: 24 };
  const s = await evals.scoreClip(good, spec);
  assert.equal(s.checks.size.pass, true); assert.equal(s.checks.duration.pass, true); assert.equal(s.checks.notFrozen.pass, true);
  const frozen = path.join(tmp, 'frozen.mp4'); execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=gray:s=640x360:r=24:d=5', '-pix_fmt', 'yuv420p', frozen]);
  const f = await evals.scoreClip(frozen, spec);
  assert.equal(f.checks.size.pass, false); assert.equal(f.checks.notFrozen.pass, false); assert.equal(f.checks.hasMotion.pass, false);
  assert.ok(f.technicalScore < s.technicalScore);
  const v = (a, b, winner) => ({ run_a: a, run_b: b, winner });
  const bt = evals.bradleyTerry([...Array(8).fill(v('A', 'B', 'a')), ...Array(2).fill(v('A', 'B', 'b')), ...Array(6).fill(v('B', 'C', 'a')), ...Array(4).fill(v('B', 'C', 'b')), v('A', 'C', 'tie')]);
  assert.ok(bt.A > bt.B && bt.B > bt.C, JSON.stringify(bt));
  assert.equal(evals.suites().length, 3);
});

test('LoRA registry: provenance required, immutable versions, production only after a passing evaluation', async () => {
  const l = loras.create({ slug: 'gulf-ads-wan-a14b', name: 'Gulf ads', specialty: 'gulf_ads', baseModel: 'wan22', baseVariant: 'a14b-720p', trigger: 'gulfads style' });
  assert.equal(l.versions.length, 0);
  assert.throws(() => loras.create({ slug: 'x-y-z', specialty: 'gulf_ads', baseModel: 'wan22', baseVariant: 'nope' }), (e) => e.code === 'unknown_base_model');
  const file = path.join(tmp, 'lora.safetensors'); fs.writeFileSync(file, Buffer.alloc(4096, 7));
  await assert.rejects(loras.addVersion(l.slug, { version: '1.0.0', path: file }), (e) => e.code === 'provenance_required');
  await assert.rejects(loras.addVersion(l.slug, { version: '1.0.0', path: path.join(tmp, 'x.ckpt'), trainer: 't', trainerCommit: 'c', datasetSnapshot: 'd' }), (e) => e.code === 'file_must_be_existing_safetensors');
  const v = await loras.addVersion(l.slug, { version: '1.0.0', path: file, trainer: 'musubi-tuner', trainerCommit: 'f8a1b03', datasetSnapshot: 'abc123', config: { network_dim: 32 } });
  assert.equal(v.status, 'candidate'); assert.equal(v.sha256.length, 64);
  await assert.rejects(loras.addVersion(l.slug, { version: '1.0.0', path: file, trainer: 't', trainerCommit: 'c', datasetSnapshot: 'd' }), (e) => e.code === 'version_exists');
  assert.throws(() => loras.setStatus(l.slug, '1.0.0', { status: 'production' }), (e) => e.code === 'bad_transition');
  loras.setStatus(l.slug, '1.0.0', { status: 'staging' });
  assert.throws(() => loras.setStatus(l.slug, '1.0.0', { status: 'production' }), (e) => e.code === 'evaluation_required');
  run("INSERT INTO eval_runs (id, suite, label, model, variant, lora_version_id, seeds_json, status, summary_json, created_at) VALUES ('ev1','gulf_ads','t','wan22','a14b-720p',?, '[1]', 'done', ?, ?)", v.id, JSON.stringify({ gate: 'fail', gateReasons: ['technical score 70 is below 90'] }), now());
  assert.throws(() => loras.setStatus(l.slug, '1.0.0', { status: 'production', evalRunId: 'ev1' }), (e) => e.code === 'evaluation_failed');
  run("UPDATE eval_runs SET summary_json = ? WHERE id = 'ev1'", JSON.stringify({ gate: 'pass', score: 95 }));
  assert.equal(loras.setStatus(l.slug, '1.0.0', { status: 'production', evalRunId: 'ev1', by: 'tester' }).status, 'production');
  // a production LoRA for the specialty tips the router and is attached automatically, with its trigger word
  const r = selectModel({ aspect: '16:9', videoType: 'commercial', quality: 'high' });
  assert.match(r.choice.reasons.join(' '), /production LoRA gulf-ads-wan-a14b@1.0.0/);
  const j = jobs.createGeneration({ model: 'auto', quality: 'high', aspect: '16:9', duration: 5, prompt: 'A perfume bottle on marble', videoType: 'commercial' });
  const claimed = jobs.claim(get('SELECT * FROM workers WHERE id = ?', 'w-a14'));
  assert.equal(claimed.id, j.id); assert.equal(claimed.lora.sha256, v.sha256); assert.ok(claimed.spec.prompt.startsWith('gulfads style, '));
});

test('datasets: rights required, automatic checks, review, snapshot, export in trainer format', async () => {
  const src = path.join(tmp, 'clips'); fs.mkdirSync(src);
  clip(path.join(src, 'a.mp4'), { d: 6 }); fs.writeFileSync(path.join(src, 'a.txt'), 'A slow dolly-in through a bright living room.');
  clip(path.join(src, 'b.mp4'), { d: 6, cut: true });            // two shots in one clip
  clip(path.join(src, 'c.mp4'), { w: 640, h: 360, d: 6 });       // too small
  fs.copyFileSync(path.join(src, 'a.mp4'), path.join(src, 'z-copy.mp4'));
  datasets.create({ slug: 'real-estate-v1', specialty: 'luxury_real_estate' });
  await assert.rejects(datasets.ingest('real-estate-v1', src, { source: 'client shoot' }), /rights\.holder is required/);
  const rep = await datasets.ingest('real-estate-v1', src, { source: 'client shoot 2026-10', holder: 'Example Developments', license: 'written permission for model training', doc: 'contracts/permission.pdf' });
  assert.equal(rep.added, 3); assert.equal(rep.duplicate, 1); assert.equal(rep.flagged, 2);
  const list = datasets.items('real-estate-v1');
  const a = list.find((i) => i.file === 'a.mp4'), b = list.find((i) => i.file === 'b.mp4'), c = list.find((i) => i.file === 'c.mp4');
  assert.equal(a.checksOk, true); assert.ok(b.cuts >= 1); assert.equal(c.checksOk, false);
  assert.throws(() => datasets.review('real-estate-v1', b.id, { status: 'approved' }), /failed automatic checks/);
  assert.throws(() => datasets.review('real-estate-v1', c.id, { status: 'rejected' }), /needs a reason/);
  datasets.review('real-estate-v1', c.id, { status: 'rejected', reason: 'below target resolution' });
  datasets.review('real-estate-v1', a.id, { status: 'approved' });
  const before = datasets.snapshot('real-estate-v1').hash;
  const out = datasets.exportFor('real-estate-v1', 'musubi-tuner', path.join(tmp, 'exports'));
  assert.equal(out.train + out.val, 1); assert.equal(out.snapshot, before);
  const toml = fs.readFileSync(out.config, 'utf8');
  assert.match(toml, /resolution = \[1280, 720\]/); assert.match(toml, /target_frames = \[81\]/); assert.match(toml, /enable_bucket = true/);
  const manifest = JSON.parse(fs.readFileSync(path.join(out.root, 'MANIFEST.json'), 'utf8'));
  assert.equal(manifest.items[0].rights.holder, 'Example Developments');
  datasets.review('real-estate-v1', a.id, { caption: 'A slow dolly-in through a sunlit double-height living room.' });
  assert.notEqual(datasets.snapshot('real-estate-v1').hash, before, 'changing a caption changes the snapshot');
});
