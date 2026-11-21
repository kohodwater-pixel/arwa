import { Router } from 'express';
import { get } from '../db.js';
import { config } from '../config.js';
import { HttpError, requireAuth, rateLimit } from '../auth.js';
import { analyze, compileMasterPrompt, videoTypes, styles, cameraMoves, shotSizes, aiDirectorAvailable, byId } from '../engine/index.js';
import { providers, describeProvider, isEnabled } from '../providers/index.js';
import { getAudioProvider, audioCreds } from '../audio/index.js';
import { uploadRules } from '../uploads.js';
import { sendAsset } from './assets.js';

export const metaRouter = Router();
const pub = (list) => list.map(({ id, ar, en }) => ({ id, ar, en }));
let ffmpegOk = null;
export const setFfmpeg = (v) => { ffmpegOk = v; };

metaRouter.get('/meta', (_req, res) => {
  const ap = getAudioProvider();
  res.json({
    appName: config.appName,
    videoTypes: pub(videoTypes), styles: pub(styles), cameraMoves: pub(cameraMoves), shotSizes: pub(shotSizes),
    durations: [5, 10, 15, 30, 60], maxProjectSeconds: config.maxProjectSeconds,
    providers: providers.filter(isEnabled).map((p) => describeProvider(p)),
    audio: { provider: ap ? { id: ap.id, label: ap.label, ...ap.capabilities } : null },
    aiDirector: aiDirectorAvailable(), ffmpeg: ffmpegOk, uploadRules,
  });
});

/** Instant "Cinematic Production Prompt" preview of the director's reading of a description. */
metaRouter.post('/engine/enhance', requireAuth, rateLimit({ windowMs: 60e3, max: 60, key: (r) => r.user.id }), (req, res) => {
  const description = String(req.body?.description || '').trim();
  if (description.length < 10) throw new HttpError(400, 'description_too_short');
  if (description.length > 4000) throw new HttpError(400, 'description_too_long');
  const videoType = byId(videoTypes, req.body?.videoType) ? req.body.videoType : 'creative';
  const style = byId(styles, req.body?.style) ? req.body.style : 'auto';
  const t = analyze(description, { videoType, style });
  res.json({ treatment: { ...t, masterPrompt: compileMasterPrompt(t) }, aiDirector: aiDirectorAvailable() });
});

let voiceCache = { at: 0, voices: [] };
metaRouter.get('/audio/voices', requireAuth, async (_req, res) => {
  const ap = getAudioProvider();
  if (!ap) return res.json({ configured: false, voices: [] });
  if (Date.now() - voiceCache.at > 10 * 60e3) {
    try { voiceCache = { at: Date.now(), voices: await ap.voices(audioCreds(ap)) }; }
    catch (e) { return res.json({ configured: true, voices: [], error: String(e.message).slice(0, 200) }); }
  }
  res.json({ configured: true, voices: voiceCache.voices });
});

// ── public share links ───────────────────────────────────────────────────────
const shared = (token) => {
  const p = /^[\w-]{10,60}$/.test(token) && get("SELECT * FROM projects WHERE share_token = ? AND status = 'completed'", token);
  if (!p || !p.final_asset_id) throw new HttpError(404, 'not_found');
  return p;
};
metaRouter.get('/share/:token', (req, res) => {
  const p = shared(req.params.token);
  res.json({ title: p.title, duration: p.duration, aspect: p.aspect, isDemo: !!p.is_demo, videoUrl: `/api/share/${p.share_token}/video`, appName: config.appName });
});
metaRouter.get('/share/:token/video', (req, res) => {
  const p = shared(req.params.token);
  sendAsset(res, get('SELECT * FROM assets WHERE id = ?', p.final_asset_id), req.query.download === '1');
});
