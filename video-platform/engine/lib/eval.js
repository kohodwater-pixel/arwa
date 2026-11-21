import fs from 'node:fs';
import path from 'node:path';
import { all, get, run, now, id, parse } from './db.js';
import { getModel, getVariant } from './registry.js';
import { ApiError, createGeneration } from './jobs.js';
import { probe, technical } from './ffmpeg.js';

/**
 * Output quality evaluation and model comparison.
 *
 * A suite is a fixed list of prompts for one specialty (engine/suites/<specialty>.json). A run generates
 * every prompt with the same seeds on one configuration (model + variant + optional LoRA version), so two
 * runs differ only in the thing being compared.
 *
 * Three layers of evidence, weakest to strongest:
 *  1. Technical gate (automatic, here): right size, length and frame rate; no frozen or black spans;
 *     frame-to-frame change that is neither dead nor erratic. It catches broken output, it does not judge beauty.
 *  2. Model-based metrics (optional, on a GPU worker; not implemented in this prototype): prompt adherence
 *     with a CLIP-style scorer, VBench-style dimensions, subject consistency between scenes.
 *  3. Blind pairwise votes by people (here): two clips of the same prompt and seed, labels hidden, one
 *     criterion at a time. Scores are fitted with Bradley–Terry. This is the layer that decides.
 * Mock output is never scored: a run on a mock worker is marked invalid.
 */
const dir = path.join(import.meta.dirname, '..', 'suites');
export const suites = () => fs.readdirSync(dir).filter((f) => f.endsWith('.json')).map((f) => { const s = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); return { id: s.id, name: s.name, prompts: s.prompts.length, criteria: s.criteria }; });
const loadSuite = (sid) => { const f = path.join(dir, `${String(sid).replace(/[^a-z_]/g, '')}.json`); if (!fs.existsSync(f)) throw new ApiError(404, 'suite_not_found'); return JSON.parse(fs.readFileSync(f, 'utf8')); };

export function startRun({ suite: sid, label, model, variant, lora, seeds = [11, 23], aspect = '16:9', seconds = 5, limit }) {
  const suite = loadSuite(sid);
  if (!getVariant(model, variant)) throw new ApiError(400, 'unknown_model');
  const runId = id('eval');
  const loraRow = lora ? get('SELECT v.id FROM lora_versions v JOIN loras l ON l.id = v.lora_id WHERE l.slug = ? AND v.version = ?', lora.slug, lora.version) : null;
  if (lora && !loraRow) throw new ApiError(404, 'lora_not_found');
  run('INSERT INTO eval_runs (id, suite, label, model, variant, lora_version_id, seeds_json, created_at) VALUES (?,?,?,?,?,?,?,?)', runId, suite.id, String(label || `${model}/${variant}`).slice(0, 80), model, variant, loraRow?.id || null, JSON.stringify(seeds), now());
  for (const p of suite.prompts.slice(0, limit || suite.prompts.length)) for (const seed of seeds) {
    const job = createGeneration({ model, variant, prompt: p.prompt, negativePrompt: suite.negative || '', duration: seconds, aspect: p.aspect || aspect, seed, lora: lora || undefined, autoLora: false, clientRef: `${runId}:${p.id}:${seed}` });
    run('INSERT INTO eval_samples (id, run_id, prompt_id, seed, job_id) VALUES (?,?,?,?,?)', id('es'), runId, p.id, seed, job.id);
  }
  return { runId, samples: get('SELECT COUNT(*) n FROM eval_samples WHERE run_id = ?', runId).n };
}

/** Scores one finished clip against what was asked for. Each check is pass/fail with the measured value. */
export async function scoreClip(file, spec) {
  const p = await probe(file); const t = await technical(file);
  const want = spec.frames / spec.fps;
  const checks = {
    playable: { pass: !!p.hasVideo, value: p.codec },
    size: { pass: p.width === spec.width && p.height === spec.height, value: `${p.width}x${p.height}`, want: `${spec.width}x${spec.height}` },
    duration: { pass: Math.abs((p.duration || 0) - want) <= 0.35, value: p.duration, want },
    frameRate: { pass: Math.abs((p.fps || 0) - spec.fps) <= 0.6, value: p.fps, want: spec.fps },
    notFrozen: { pass: t.frozenSeconds <= want * 0.15, value: t.frozenSeconds },
    notBlack: { pass: t.blackSeconds <= 0.3, value: t.blackSeconds },
    hasMotion: { pass: t.motionMean >= 0.15, value: Math.round(t.motionMean * 100) / 100 },
    steadyMotion: { pass: t.motionJitter <= 1.5, value: Math.round(t.motionJitter * 100) / 100 },
  };
  const passed = Object.values(checks).filter((c) => c.pass).length;
  return { checks, technicalScore: Math.round((passed / Object.keys(checks).length) * 100), blurMean: t.blurMean };
}

/** Pulls finished jobs into the run, scores them, and closes the run when every sample is in. */
export async function collect(runId) {
  const r = get('SELECT * FROM eval_runs WHERE id = ?', runId);
  if (!r) throw new ApiError(404, 'run_not_found');
  const samples = all('SELECT s.*, j.status, j.output_file, j.spec_json, j.mock, j.gpu_seconds AS job_gpu, j.error FROM eval_samples s LEFT JOIN jobs j ON j.id = s.job_id WHERE s.run_id = ?', runId);
  for (const s of samples) {
    if (s.metrics_json || s.status !== 'succeeded') continue;
    const m = s.mock ? { mock: true } : await scoreClip(s.output_file, parse(s.spec_json, {}));
    run('UPDATE eval_samples SET metrics_json = ?, gpu_seconds = ? WHERE id = ?', JSON.stringify(m), s.job_gpu, s.id); s.metrics_json = JSON.stringify(m);
  }
  const done = samples.filter((s) => ['succeeded', 'failed', 'canceled'].includes(s.status));
  let summary = parse(r.summary_json, null);
  if (done.length === samples.length && r.status === 'running') {
    const scored = samples.map((s) => parse(s.metrics_json, null)).filter(Boolean);
    const mock = scored.some((m) => m.mock);
    const failed = samples.filter((s) => s.status !== 'succeeded').length;
    const tech = scored.filter((m) => !m.mock).map((m) => m.technicalScore);
    const mean = tech.length ? tech.reduce((a, b) => a + b, 0) / tech.length : 0;
    const gpu = samples.reduce((n, s) => n + (s.gpu_seconds || 0), 0);
    const reasons = [];
    if (mock) reasons.push('generated by a mock worker: not a real model output');
    if (failed) reasons.push(`${failed} of ${samples.length} generations failed`);
    if (!mock && mean < 90) reasons.push(`technical score ${mean.toFixed(0)} is below 90`);
    summary = { samples: samples.length, failed, mock, technicalScore: Math.round(mean), score: mock ? null : Math.round(mean), gpuSecondsPerClip: samples.length ? Math.round(gpu / samples.length) : null, gate: reasons.length ? 'fail' : 'pass', gateReasons: reasons };
    run("UPDATE eval_runs SET status = ?, summary_json = ? WHERE id = ?", mock ? 'invalid' : 'done', JSON.stringify(summary), runId);
  }
  const fresh = get('SELECT * FROM eval_runs WHERE id = ?', runId);
  return { id: runId, suite: r.suite, label: r.label, model: r.model, variant: r.variant, status: fresh.status, progress: `${done.length}/${samples.length}`, summary,
    samples: samples.map((s) => ({ prompt: s.prompt_id, seed: s.seed, job: s.job_id, status: s.status, error: s.error, metrics: parse(s.metrics_json, null) })) };
}

export function vote({ suite, promptId, seed, runA, runB, winner, criterion, rater }) {
  const s = loadSuite(suite);
  if (!s.criteria.includes(criterion)) throw new ApiError(400, 'bad_criterion', s.criteria);
  if (!['a', 'b', 'tie'].includes(winner)) throw new ApiError(400, 'bad_winner');
  for (const r of [runA, runB]) if (!get("SELECT 1 FROM eval_runs WHERE id = ? AND suite = ? AND status = 'done'", r, s.id)) throw new ApiError(400, 'run_not_comparable', r);
  run('INSERT INTO eval_votes (suite, prompt_id, seed, run_a, run_b, winner, criterion, rater, created_at) VALUES (?,?,?,?,?,?,?,?,?)', s.id, String(promptId), Number(seed), runA, runB, winner, criterion, rater ? String(rater).slice(0, 60) : null, now());
  return { ok: true };
}

/** Bradley–Terry strengths from pairwise votes (ties count half to each side), scaled so the mean is 100. */
export function bradleyTerry(votes) {
  const ids = [...new Set(votes.flatMap((v) => [v.run_a, v.run_b]))];
  if (!ids.length) return {};
  const wins = Object.fromEntries(ids.map((i) => [i, 0.5])); // small prior so an unbeaten run stays finite
  const games = {};
  for (const v of votes) {
    const a = v.winner === 'a' ? 1 : v.winner === 'tie' ? 0.5 : 0;
    wins[v.run_a] += a; wins[v.run_b] += 1 - a;
    const k = [v.run_a, v.run_b].sort().join('|'); games[k] = (games[k] || 0) + 1;
  }
  let p = Object.fromEntries(ids.map((i) => [i, 1]));
  for (let it = 0; it < 200; it++) {
    const next = {};
    for (const i of ids) {
      let denom = 0;
      for (const j of ids) if (i !== j) { const n = games[[i, j].sort().join('|')] || 0; if (n) denom += n / (p[i] + p[j]); }
      next[i] = denom ? wins[i] / denom : p[i];
    }
    const mean = ids.reduce((s, i) => s + next[i], 0) / ids.length;
    for (const i of ids) next[i] /= mean;
    p = next;
  }
  return Object.fromEntries(ids.map((i) => [i, Math.round(p[i] * 100)]));
}

export function compare(suiteId) {
  const s = loadSuite(suiteId);
  const runs = all("SELECT * FROM eval_runs WHERE suite = ? AND status = 'done' ORDER BY created_at DESC", s.id);
  const votes = all('SELECT * FROM eval_votes WHERE suite = ?', s.id);
  const overall = bradleyTerry(votes);
  const perCriterion = Object.fromEntries(s.criteria.map((c) => [c, bradleyTerry(votes.filter((v) => v.criterion === c))]));
  return { suite: s.id, votes: votes.length, note: votes.length < 30 ? 'fewer than 30 votes: treat the human ranking as provisional' : null,
    runs: runs.map((r) => { const sum = parse(r.summary_json, {}); return { id: r.id, label: r.label, model: r.model, variant: r.variant, lora: r.lora_version_id, technicalScore: sum.technicalScore, gate: sum.gate, gpuSecondsPerClip: sum.gpuSecondsPerClip, human: overall[r.id] ?? null, byCriterion: Object.fromEntries(s.criteria.map((c) => [c, perCriterion[c][r.id] ?? null])) }; }) };
}
