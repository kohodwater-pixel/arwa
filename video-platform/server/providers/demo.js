import fs from 'node:fs';
import crypto from 'node:crypto';
import { renderDemoClip } from '../ffmpeg.js';
import { storage } from '../storage.js';
import { fitClip } from './http.js';

/**
 * Demo provider. It does NOT generate video with AI: it renders a labelled placeholder card for each
 * scene so the whole pipeline (queue, progress, storage, assembly, audio mix, library) can be tried
 * without a provider key. Every clip is stamped "DEMO MODE — NOT AN AI-GENERATED VIDEO" and projects
 * made with it are flagged is_demo everywhere in the UI.
 */
const jobs = new Map(); // jobId → { started, ms, file, error, done }
const QUALITIES = [{
  id: 'standard', label: 'Demo preview · 480p', resolution: '480p',
  aspects: { '16:9': '16:9', '9:16': '9:16', '1:1': '1:1', '4:5': '4:5' }, clip: { min: 2, max: 10 },
  maxPromptChars: 2000, negativePrompt: true, imageToVideo: true, nativeAudio: false,
}];

export default {
  id: 'demo', label: 'Demo mode', demo: true, verified: 'local',
  credentialFields: [],
  qualities: () => QUALITIES,
  maxConcurrent: 4,
  minPollMs: 800,

  async submit({ duration, aspect, meta = {} }) {
    const jobId = 'demo_' + crypto.randomBytes(8).toString('hex');
    const clip = fitClip(QUALITIES[0].clip, duration);
    const file = storage.tmpPath('mp4');
    const job = { started: Date.now(), ms: 1500 + clip * 250, file, done: false, error: null };
    jobs.set(jobId, job);
    renderDemoClip({ out: file, duration: clip, aspect, lines: [`Scene ${meta.index ?? '?'} of ${meta.total ?? '?'}  -  ${meta.cameraMove || ''}`, `${clip}s  -  ${aspect}  -  placeholder card, no AI model was called`] })
      .then(() => { job.done = true; }, (e) => { job.error = String(e.message || e); });
    return { jobId, clipDuration: clip };
  },

  async poll(jobId) {
    const j = jobs.get(jobId);
    if (!j) return { status: 'failed', error: 'demo job lost after a server restart', retryable: true };
    if (j.error) { jobs.delete(jobId); return { status: 'failed', error: j.error, retryable: true }; }
    const p = Math.min(1, (Date.now() - j.started) / j.ms);
    if (j.done && p >= 1) { jobs.delete(jobId); return { status: 'succeeded', localFile: j.file }; }
    return { status: 'running', progress: Math.min(0.97, p) };
  },
  async cancel(jobId) { const j = jobs.get(jobId); jobs.delete(jobId); if (j) fs.promises.unlink(j.file).catch(() => {}); },
};
