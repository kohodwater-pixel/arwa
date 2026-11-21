import { request, ProviderError, fitClip } from './http.js';

/**
 * Google Veo adapter (Gemini API).
 * Source: google-gemini/cookbook quickstarts/Get_started_Veo_REST.ipynb and googleapis/js-genai, read 2026-11-21:
 *   POST /v1beta/models/{model}:predictLongRunning  → { name: "models/…/operations/…" }
 *   GET  /v1beta/{operation name}                   → response.generateVideoResponse.generatedSamples[0].video.uri
 *   the video is downloaded from that URI with the API key header.
 * Assumptions not confirmed in those sources: 1080p clips are generated at 8 s only; a finished operation carries
 * `done: true`; safety blocks are reported in raiMediaFilteredReasons. Veo 3.x always generates an audio track.
 * Not exercised against the live API in this build.
 */
const BASE = 'https://generativelanguage.googleapis.com/v1beta';
const headers = (c) => ({ 'x-goog-api-key': c.apiKey });
const QUALITIES = [
  { id: 'standard', label: 'Veo 3.1 Fast · 720p', model: 'veo-3.1-fast-generate-preview', resolution: '720p',
    aspects: { '16:9': '16:9', '9:16': '9:16' }, clip: { min: 4, max: 8, values: [4, 6, 8] },
    maxPromptChars: 2400, negativePrompt: true, imageToVideo: true, nativeAudio: true },
  { id: 'high', label: 'Veo 3.1 · 1080p', model: 'veo-3.1-generate-preview', resolution: '1080p',
    aspects: { '16:9': '16:9', '9:16': '9:16' }, clip: { min: 8, max: 8, values: [8] },
    maxPromptChars: 2400, negativePrompt: true, imageToVideo: true, nativeAudio: true },
];

export default {
  id: 'veo', label: 'Google Veo', demo: false, verified: 'sdk',
  docsUrl: 'https://ai.google.dev/gemini-api/docs/video',
  credentialFields: [{ key: 'apiKey', label: 'Gemini API key', env: 'GEMINI_API_KEY', secret: true, required: true }],
  qualities: () => QUALITIES,
  maxConcurrent: 2,
  minPollMs: 10000,

  async submit({ prompt, negativePrompt, duration, aspect, quality, image, seed }, creds) {
    const q = QUALITIES.find((x) => x.id === quality);
    if (!q?.aspects[aspect]) throw new ProviderError(`Veo does not support ${aspect}`, { code: 'provider_rejected' });
    const clip = fitClip(q.clip, duration);
    const instance = { prompt };
    if (image?.buffer) instance.image = { bytesBase64Encoded: image.buffer.toString('base64'), mimeType: image.mime };
    const parameters = { aspectRatio: q.aspects[aspect], resolution: q.resolution, durationSeconds: clip, sampleCount: 1 };
    if (negativePrompt) parameters.negativePrompt = negativePrompt;
    if (Number.isInteger(seed)) parameters.seed = seed;
    const res = await request(`${BASE}/models/${q.model}:predictLongRunning`, { method: 'POST', headers: headers(creds), json: { instances: [instance], parameters } });
    if (!res.name) throw new ProviderError('Veo returned no operation name');
    return { jobId: res.name, clipDuration: clip };
  },

  async poll(jobId, creds) {
    if (!/^[\w\-./]+$/.test(jobId)) throw new ProviderError('bad operation name');
    const op = await request(`${BASE}/${jobId}`, { headers: headers(creds) });
    if (op.error) return { status: 'failed', error: `${op.error.code || ''} ${op.error.message || 'generation failed'}`.trim(), retryable: [429, 500, 503].includes(op.error.code) };
    const r = op.response?.generateVideoResponse;
    const uri = r?.generatedSamples?.[0]?.video?.uri;
    if (uri) return { status: 'succeeded', videoUrl: uri, downloadHeaders: headers(creds) };
    if (op.done || r) return { status: 'failed', error: (r?.raiMediaFilteredReasons || []).join('; ') || 'no video returned (possibly filtered)', retryable: false };
    return { status: 'running' };
  },
  test: (creds) => request(`${BASE}/models?pageSize=1`, { headers: headers(creds), timeoutMs: 15000 }),
};
