import { request, ProviderError, fitClip } from './http.js';

/**
 * Runway API adapter.
 * Source: official SDK runwayml/sdk-node v4.29.0 (generated from Runway's OpenAPI spec), read 2026-11-21:
 *   POST /v1/text_to_video, POST /v1/image_to_video, GET /v1/tasks/{id}, DELETE /v1/tasks/{id}
 *   headers: Authorization: Bearer <key>, X-Runway-Version: 2024-11-06
 * Not exercised against the live API in this build (no key was available).
 */
const BASE = 'https://api.dev.runwayml.com';
const headers = (c) => ({ authorization: `Bearer ${c.apiKey}`, 'x-runway-version': '2024-11-06' });

const QUALITIES = [
  { id: 'standard', label: 'Gen-4.5 · 720p', model: 'gen4.5', resolution: '720p',
    aspects: { '16:9': '1280:720', '9:16': '720:1280' }, clip: { min: 2, max: 10 },
    maxPromptChars: 1000, negativePrompt: false, imageToVideo: true, nativeAudio: false },
  { id: 'high', label: 'Veo 3.1 · 1080p', model: 'veo3.1', resolution: '1080p',
    aspects: { '16:9': '1920:1080', '9:16': '1080:1920' }, clip: { min: 4, max: 8, values: [4, 6, 8] },
    maxPromptChars: 1000, negativePrompt: false, imageToVideo: false, nativeAudio: true },
];

export default {
  id: 'runway', label: 'Runway', demo: false, verified: 'sdk',
  docsUrl: 'https://docs.dev.runwayml.com/',
  credentialFields: [{ key: 'apiKey', label: 'API secret', env: 'RUNWAY_API_KEY', secret: true, required: true }],
  qualities: () => QUALITIES,
  maxConcurrent: 3,
  minPollMs: 5000,

  async submit({ prompt, duration, aspect, quality, image, seed, wantAudio }, creds) {
    const q = QUALITIES.find((x) => x.id === quality);
    const ratio = q?.aspects[aspect];
    if (!ratio) throw new ProviderError(`Runway ${quality} does not support ${aspect}`, { code: 'provider_rejected' });
    const body = { model: q.model, promptText: prompt, ratio, duration: fitClip(q.clip, duration) };
    if (Number.isInteger(seed)) body.seed = seed;
    if (q.nativeAudio) body.audio = !!wantAudio;
    let path = '/v1/text_to_video';
    if (image && q.imageToVideo) {
      if (image.buffer.length > 5 * 1024 * 1024) throw new ProviderError('reference image larger than 5 MB', { code: 'provider_rejected' });
      path = '/v1/image_to_video';
      body.promptImage = [{ uri: `data:${image.mime};base64,${image.buffer.toString('base64')}`, position: 'first' }];
    }
    const res = await request(BASE + path, { method: 'POST', headers: headers(creds), json: body });
    if (!res.id) throw new ProviderError('Runway returned no task id');
    return { jobId: res.id, clipDuration: body.duration };
  },

  async poll(jobId, creds) {
    const t = await request(`${BASE}/v1/tasks/${encodeURIComponent(jobId)}`, { headers: headers(creds) });
    switch (t.status) {
      case 'SUCCEEDED': return t.output?.[0] ? { status: 'succeeded', videoUrl: t.output[0] } : { status: 'failed', error: 'no output returned', retryable: true };
      case 'FAILED': return { status: 'failed', error: [t.failureCode, t.failure].filter(Boolean).join(': ') || 'generation failed', retryable: !/SAFETY|MODERATION|INPUT/i.test(t.failureCode || '') };
      case 'CANCELLED': return { status: 'failed', error: 'cancelled at provider', retryable: false };
      case 'RUNNING': return { status: 'running', progress: typeof t.progress === 'number' ? Math.min(1, Math.max(0, t.progress)) : undefined };
      default: return { status: 'pending' }; // PENDING, THROTTLED
    }
  },
  cancel: (jobId, creds) => request(`${BASE}/v1/tasks/${encodeURIComponent(jobId)}`, { method: 'DELETE', headers: headers(creds) }),
  test: (creds) => request(`${BASE}/v1/organization`, { headers: headers(creds), timeoutMs: 15000 }),
};
