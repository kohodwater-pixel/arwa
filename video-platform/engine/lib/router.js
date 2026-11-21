import { models, licenceAllows, maxSeconds } from './registry.js';
import { all, get, parse } from './db.js';

/**
 * Automatic model selection. Every candidate (model, variant) is first filtered by hard constraints
 * (task, aspect ratio, licence policy, a live worker that has it), then scored against the profile of
 * the project type. The answer always carries the ranking and the reasons, so a choice can be audited.
 *
 * `strengths` in the model manifests are starting assumptions. As soon as an evaluation run exists
 * for a specialty, its measured score replaces the assumption (see evalBonus) — the router is meant
 * to be driven by our own tests, not by reputation.
 */
export const SPECIALTIES = ['gulf_ads', 'luxury_real_estate', 'saudi_tourism'];
const TYPE_TO_SPECIALTY = { commercial: 'gulf_ads', product: 'gulf_ads', social: 'gulf_ads', real_estate: 'luxury_real_estate', tourism: 'saudi_tourism' };

// weight of each strength per project type (sum is irrelevant; only the ranking matters)
const PROFILES = {
  commercial: { motion: 3, detail: 3, adherence: 3, resolution: 2, speed: 1, audio: 1 },
  product: { detail: 4, adherence: 3, motion: 2, resolution: 2, speed: 1 },
  real_estate: { resolution: 4, detail: 3, stability: 4, i2v: 4, motion: 1, speed: 1 },   // real property photos → image-to-video
  tourism: { resolution: 3, detail: 3, motion: 3, stability: 2, adherence: 2, speed: 1 },
  social: { speed: 4, audio: 3, motion: 2, adherence: 2, detail: 1 },
  short_film: { motion: 3, adherence: 3, detail: 3, stability: 2, audio: 1 },
  creative: { motion: 3, adherence: 3, detail: 2, speed: 1 },
  motion_graphics: { adherence: 3, stability: 3, speed: 2, detail: 1 },
};
const WORKER_TTL_MS = 45_000;

export function liveWorkers() {
  return all('SELECT * FROM workers WHERE last_seen > ?', Date.now() - WORKER_TTL_MS).map((w) => ({ ...w, models: parse(w.models_json, []) }));
}
const workerHas = (w, modelId, variantId) => w.models.some((m) => m.id === modelId && (!m.variants || m.variants.includes(variantId)));

function evalBonus(specialty, modelId, variantId) {
  if (!specialty) return null;
  const r = get(`SELECT summary_json FROM eval_runs WHERE status = 'done' AND model = ? AND variant = ? AND suite = ? AND lora_version_id IS NULL ORDER BY created_at DESC LIMIT 1`, modelId, variantId, specialty);
  const s = parse(r?.summary_json, null);
  return s && typeof s.score === 'number' ? s.score : null; // 0..100
}

export function candidates({ task = 't2v', aspect, quality, videoType = 'creative', specialty, wantAudio = false, duration, requireOnline = true }) {
  const spec = specialty || TYPE_TO_SPECIALTY[videoType] || null;
  const profile = PROFILES[videoType] || PROFILES.creative;
  const workers = liveWorkers();
  const out = [];
  for (const m of models) {
    for (const v of m.variants) {
      const reasons = [], blocked = [];
      if (!v.tasks.includes(task)) blocked.push(`does not do ${task}`);
      if (aspect && !v.sizes[aspect]) blocked.push(`no ${aspect}`);
      if (!licenceAllows(m)) blocked.push(`licence: ${m.license.commercial}`);
      if (duration && duration > maxSeconds(v)) blocked.push(`clips up to ${maxSeconds(v)} s only`);
      const online = workers.filter((w) => workerHas(w, m.id, v.id));
      if (requireOnline && !online.length) blocked.push('no live worker has it');
      let score = 0;
      for (const [k, w] of Object.entries(profile)) score += w * (v.strengths?.[k] ?? 0);
      const measured = evalBonus(spec, m.id, v.id);
      if (measured != null) { score = score * 0.4 + measured * 0.6; reasons.push(`measured ${measured.toFixed(0)}/100 on the ${spec} suite`); } else reasons.push('scored on starting assumptions (no evaluation run yet)');
      if (quality && v.tier !== quality) blocked.push(`tier is ${v.tier}, not ${quality}`); // the platform advertised this tier's limits
      if (wantAudio && v.audio) { score += 5; reasons.push('generates audio'); }
      const lora = spec && get(`SELECT l.slug, v.version FROM loras l JOIN lora_versions v ON v.lora_id = l.id WHERE l.specialty = ? AND l.base_model = ? AND l.base_variant = ? AND v.status = 'production' ORDER BY v.created_at DESC LIMIT 1`, spec, m.id, v.id);
      if (lora) { score += 12; reasons.push(`production LoRA ${lora.slug}@${lora.version}`); }
      if (online.some((w) => !w.current_job)) { score += 2; reasons.push('a worker is idle'); }
      out.push({ model: m.id, variant: v.id, label: `${m.label} · ${v.label}`, score: Math.round(score * 10) / 10, blocked, reasons, tier: v.tier, online: online.length, maxSeconds: maxSeconds(v), lora: lora || null, specialty: spec });
    }
  }
  return out.sort((a, b) => (a.blocked.length ? 1 : 0) - (b.blocked.length ? 1 : 0) || b.score - a.score);
}

export function selectModel(req) {
  const ranked = candidates(req);
  const best = ranked.find((c) => !c.blocked.length);
  return { choice: best || null, ranked };
}
