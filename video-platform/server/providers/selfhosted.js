import { request, ProviderError } from './http.js';

/**
 * Self-hosted engine adapter. Talks to our own engine service (video-platform/engine), which queues the
 * job, picks the open-source model, and hands it to a GPU worker. Unlike the third-party adapters, what
 * this provider can do is not fixed: it is whatever the engine reports right now — models that pass the
 * licence policy AND have a live worker. With no worker online it offers nothing.
 */
const TIERS = ['standard', 'high', 'ultra'];
let cache = { at: 0, qualities: [], mockOnly: false, workersOnline: 0, error: 'not checked yet' };
const base = (c) => String(c.engineUrl || '').replace(/\/$/, '');
const headers = (c) => ({ authorization: `Bearer ${c.apiKey}` });

function toQualities(cap) {
  const out = [];
  for (const tier of TIERS) {
    const vs = cap.models.filter((m) => m.licence.allowed).flatMap((m) => m.variants.filter((v) => v.tier === tier && v.online > 0).map((v) => ({ ...v, model: m.label })));
    if (!vs.length) continue;
    const aspects = [...new Set(vs.flatMap((v) => v.aspects))].filter((a) => ['16:9', '9:16', '1:1', '4:5'].includes(a));
    if (!aspects.length) continue;
    const models = [...new Set(vs.map((v) => v.model))].join(' / ');
    out.push({
      id: tier, label: `${cap.mockOnly ? 'MOCK worker · ' : ''}${models} · ${tier}`, resolution: vs.map((v) => v.label).join(', '),
      aspects: Object.fromEntries(aspects.map((a) => [a, a])),
      clip: { min: Math.max(...vs.map((v) => v.clip.min)), max: Math.min(...vs.map((v) => v.clip.max)) },
      maxPromptChars: Math.min(...vs.map((v) => v.maxPromptChars)), negativePrompt: vs.every((v) => v.negativePrompt),
      imageToVideo: vs.some((v) => v.tasks.includes('i2v')), nativeAudio: vs.every((v) => v.audio),
    });
  }
  return out;
}

export default {
  id: 'selfhosted', label: 'Self-hosted engine', demo: false, verified: 'own',
  credentialFields: [
    { key: 'engineUrl', label: 'Engine URL', env: 'ENGINE_URL', secret: false, required: true, placeholder: 'http://127.0.0.1:4200' },
    { key: 'apiKey', label: 'Engine API key', env: 'ENGINE_API_KEY', secret: true, required: true },
  ],
  qualities: () => cache.qualities,
  status: () => ({ workersOnline: cache.workersOnline, mockOnly: cache.mockOnly, error: cache.error, checkedAt: cache.at }),
  maxConcurrent: 8,      // the engine queues; workers set the real pace
  minPollMs: 2000,

  /** Called by the registry on a timer and after settings change. */
  async refresh(creds) {
    if (!creds.engineUrl || !creds.apiKey) { cache = { at: Date.now(), qualities: [], mockOnly: false, workersOnline: 0, error: 'not configured' }; return; }
    try {
      const cap = await request(`${base(creds)}/v1/capabilities`, { headers: headers(creds), timeoutMs: 8000 });
      cache = { at: Date.now(), qualities: toQualities(cap), mockOnly: !!cap.mockOnly, workersOnline: cap.workersOnline, error: cap.workersOnline ? null : 'no GPU worker is online' };
    } catch (e) { cache = { at: Date.now(), qualities: [], mockOnly: false, workersOnline: 0, error: String(e.message).slice(0, 160) }; }
  },

  async submit({ prompt, negativePrompt, duration, aspect, quality, image, seed, wantAudio, meta = {} }, creds) {
    const body = { model: 'auto', quality, aspect, duration, prompt, negativePrompt, seed, wantAudio, videoType: meta.videoType, clientRef: meta.clientRef };
    if (image?.buffer) body.image = { base64: image.buffer.toString('base64'), mime: image.mime };
    let job;
    try { job = await request(`${base(creds)}/v1/generations`, { method: 'POST', headers: headers(creds), json: body }); }
    catch (e) { if (e.status === 409) throw new ProviderError('no model can take this job right now (no live worker, or the licence policy excludes the candidates)', { retryable: true, code: 'engine_no_model' }); throw e; }
    return { jobId: job.id, clipDuration: job.clipSeconds || duration, info: `${job.model}/${job.variant} — ${job.reason}` };
  },

  async poll(jobId, creds) {
    const j = await request(`${base(creds)}/v1/generations/${encodeURIComponent(jobId)}`, { headers: headers(creds) });
    if (j.status === 'succeeded') return { status: 'succeeded', videoUrl: `${base(creds)}/v1/generations/${encodeURIComponent(jobId)}/content`, downloadHeaders: headers(creds), allowInsecure: true, demo: !!j.mock };
    if (j.status === 'failed') return { status: 'failed', error: j.error || 'generation failed', retryable: false }; // the engine already retried on its side
    if (j.status === 'canceled') return { status: 'failed', error: 'canceled at the engine', retryable: false };
    return { status: j.status === 'running' ? 'running' : 'pending', progress: typeof j.progress === 'number' ? j.progress : undefined };
  },
  cancel: (jobId, creds) => request(`${base(creds)}/v1/generations/${encodeURIComponent(jobId)}`, { method: 'DELETE', headers: headers(creds) }),
  test: (creds) => request(`${base(creds)}/v1/health`, { headers: headers(creds), timeoutMs: 8000 }),
};
