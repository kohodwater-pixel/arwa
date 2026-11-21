import crypto from 'node:crypto';
import { request, ProviderError, fitClip } from './http.js';

/**
 * Kling AI adapter — EXPERIMENTAL.
 * Kling's documentation host could not be opened when this adapter was written (2026-11-21) and Kling publishes
 * no official SDK, so the request and response shapes below come from search snippets of the official pages and
 * from prior knowledge. Confirm them against the Kling developer console before relying on this adapter:
 *   auth: JWT HS256 { iss: accessKey, exp: now+1800, nbf: now-5 } → Authorization: Bearer <jwt>
 *   POST /v1/videos/text2video | /v1/videos/image2video,  GET /v1/videos/{kind}/{task_id}
 * The base URL and the model name are settings, because they differ by region and change with releases.
 */
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
function jwt(c) {
  const now = Math.floor(Date.now() / 1000);
  const head = `${b64({ alg: 'HS256', typ: 'JWT' })}.${b64({ iss: c.accessKey, exp: now + 1800, nbf: now - 5 })}`;
  return `${head}.${crypto.createHmac('sha256', c.secretKey).update(head).digest('base64url')}`;
}
const base = (c) => (c.baseUrl || 'https://api-singapore.klingai.com').replace(/\/$/, '');
const headers = (c) => ({ authorization: `Bearer ${jwt(c)}` });
const tier = (id, label, mode) => ({
  id, label, mode, resolution: mode === 'pro' ? '1080p' : '720p',
  aspects: { '16:9': '16:9', '9:16': '9:16', '1:1': '1:1' }, clip: { min: 5, max: 10, values: [5, 10] },
  maxPromptChars: 2500, negativePrompt: true, imageToVideo: true, nativeAudio: false,
});
const QUALITIES = [tier('standard', 'Kling · Standard', 'std'), tier('high', 'Kling · Pro', 'pro')];
const check = (res) => { if (res.code !== 0) throw new ProviderError(`Kling ${res.code}: ${res.message}`, { retryable: [1302, 1303].includes(res.code) || res.code >= 5000, code: res.code >= 1000 && res.code < 1100 ? 'provider_auth' : 'provider_rejected' }); return res.data; };

export default {
  id: 'kling', label: 'Kling AI', demo: false, verified: 'unverified',
  docsUrl: 'https://app.klingai.com/global/dev/document-api',
  credentialFields: [
    { key: 'accessKey', label: 'Access key', env: 'KLING_ACCESS_KEY', secret: true, required: true },
    { key: 'secretKey', label: 'Secret key', env: 'KLING_SECRET_KEY', secret: true, required: true },
    { key: 'baseUrl', label: 'API base URL', env: 'KLING_BASE_URL', secret: false, required: false, placeholder: 'https://api-singapore.klingai.com' },
    { key: 'model', label: 'Model name', env: 'KLING_MODEL', secret: false, required: false, placeholder: 'kling-v2-6' },
  ],
  qualities: () => QUALITIES,
  maxConcurrent: 2,
  minPollMs: 8000,

  async submit({ prompt, negativePrompt, duration, aspect, quality, image }, creds) {
    if (creds.baseUrl && !/^https:\/\/[a-z0-9.-]+\.klingai\.com$/i.test(base(creds))) throw new ProviderError('Kling base URL must be an https klingai.com host', { code: 'provider_rejected' });
    const q = QUALITIES.find((x) => x.id === quality);
    if (!q?.aspects[aspect]) throw new ProviderError(`Kling does not support ${aspect}`, { code: 'provider_rejected' });
    const clip = fitClip(q.clip, duration);
    const body = { model_name: creds.model || 'kling-v2-6', prompt, mode: q.mode, aspect_ratio: q.aspects[aspect], duration: String(clip) };
    if (negativePrompt) body.negative_prompt = negativePrompt.slice(0, 2500);
    const kind = image?.buffer ? 'image2video' : 'text2video';
    if (image?.buffer) body.image = image.buffer.toString('base64');
    const data = check(await request(`${base(creds)}/v1/videos/${kind}`, { method: 'POST', headers: headers(creds), json: body }));
    if (!data?.task_id) throw new ProviderError('Kling returned no task id');
    return { jobId: `${kind}:${data.task_id}`, clipDuration: clip };
  },

  async poll(jobId, creds) {
    const [kind, taskId] = jobId.split(':');
    if (!['text2video', 'image2video'].includes(kind)) throw new ProviderError('bad Kling job id');
    const d = check(await request(`${base(creds)}/v1/videos/${kind}/${encodeURIComponent(taskId)}`, { headers: headers(creds) }));
    if (d.task_status === 'succeed') { const url = d.task_result?.videos?.[0]?.url; return url ? { status: 'succeeded', videoUrl: url } : { status: 'failed', error: 'no video returned', retryable: true }; }
    if (d.task_status === 'failed') return { status: 'failed', error: d.task_status_msg || 'generation failed', retryable: false };
    return { status: d.task_status === 'processing' ? 'running' : 'pending' };
  },
  test: async (creds) => check(await request(`${base(creds)}/v1/videos/text2video?pageNum=1&pageSize=1`, { headers: headers(creds), timeoutMs: 15000 })),
};
