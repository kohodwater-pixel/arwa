import { request, ProviderError, fitClip } from './http.js';

/**
 * Luma Dream Machine adapter.
 * Source: official SDK lumalabs/lumaai-node v1.21.0, read 2026-11-21 (the SDK may lag the API):
 *   POST /dream-machine/v1/generations/video, GET /generations/{id}, DELETE /generations/{id}
 * The API has no seed and no negative-prompt field, and no numeric progress.
 * Assumption (not in the SDK): prompt length limit — kept conservative at 2000 characters.
 * Reference images must be reachable by URL, so image-to-video needs PUBLIC_BASE_URL.
 * Not exercised against the live API in this build.
 */
const BASE = 'https://api.lumalabs.ai/dream-machine/v1';
const headers = (c) => ({ authorization: `Bearer ${c.apiKey}` });
const tier = (id, label, model, resolution) => ({
  id, label, model, resolution,
  aspects: { '16:9': '16:9', '9:16': '9:16', '1:1': '1:1' }, clip: { min: 5, max: 9, values: [5, 9] },
  maxPromptChars: 2000, negativePrompt: false, imageToVideo: 'url', nativeAudio: false,
});
const QUALITIES = [tier('standard', 'Ray Flash 2 · 720p', 'ray-flash-2', '720p'), tier('high', 'Ray 2 · 1080p', 'ray-2', '1080p'), tier('ultra', 'Ray 2 · 4K', 'ray-2', '4k')];

export default {
  id: 'luma', label: 'Luma Dream Machine', demo: false, verified: 'sdk',
  docsUrl: 'https://docs.lumalabs.ai/',
  credentialFields: [{ key: 'apiKey', label: 'API key', env: 'LUMA_API_KEY', secret: true, required: true }],
  qualities: () => QUALITIES,
  maxConcurrent: 3,
  minPollMs: 5000,

  async submit({ prompt, duration, aspect, quality, image }, creds) {
    const q = QUALITIES.find((x) => x.id === quality);
    if (!q?.aspects[aspect]) throw new ProviderError(`Luma does not support ${aspect}`, { code: 'provider_rejected' });
    const clip = fitClip(q.clip, duration);
    const body = { generation_type: 'video', model: q.model, prompt, aspect_ratio: q.aspects[aspect], resolution: q.resolution, duration: `${clip}s` };
    if (image?.url) body.keyframes = { frame0: { type: 'image', url: image.url } };
    const res = await request(`${BASE}/generations/video`, { method: 'POST', headers: headers(creds), json: body });
    if (!res.id) throw new ProviderError('Luma returned no generation id');
    return { jobId: res.id, clipDuration: clip };
  },

  async poll(jobId, creds) {
    const g = await request(`${BASE}/generations/${encodeURIComponent(jobId)}`, { headers: headers(creds) });
    if (g.state === 'completed') return g.assets?.video ? { status: 'succeeded', videoUrl: g.assets.video } : { status: 'failed', error: 'no video asset returned', retryable: true };
    if (g.state === 'failed') return { status: 'failed', error: g.failure_reason || 'generation failed', retryable: !/moderat|safety|policy/i.test(g.failure_reason || '') };
    return { status: g.state === 'dreaming' ? 'running' : 'pending' };
  },
  cancel: (jobId, creds) => request(`${BASE}/generations/${encodeURIComponent(jobId)}`, { method: 'DELETE', headers: headers(creds) }),
  test: (creds) => request(`${BASE}/generations?limit=1`, { headers: headers(creds), timeoutMs: 15000 }),
};
