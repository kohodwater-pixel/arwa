import fs from 'node:fs';
import fsp from 'node:fs/promises';
import { Readable } from 'node:stream';
import { pipeline as pipe } from 'node:stream/promises';
import { all, get, run, update, now, id } from './db.js';
import { config } from './config.js';
import { storage } from './storage.js';
import { sign } from './secrets.js';
import * as log from './log.js';
import * as queue from './queue.js';
import { probe, lastFrame, assemble, poster } from './ffmpeg.js';
import { getProvider, getCredentials, isConfigured, isEnabled, getQuality } from './providers/index.js';
import { ProviderError } from './providers/http.js';
import { negativePrompt } from './engine/index.js';
import { getAudioProvider, audioCreds, audioDirection, defaultAudio } from './audio/index.js';

const MAX_VIDEO_BYTES = 1024 * 1024 * 1024;
const JOB_TIMEOUT_MS = 30 * 60e3;
const parse = (s, d) => { try { return s ? JSON.parse(s) : d; } catch { return d; } };

export function createAsset({ userId, projectId, kind, filename, mime, storageKey, size, meta = {}, isDemo = false }) {
  const assetId = id();
  run('INSERT INTO assets (id, user_id, project_id, kind, filename, mime, size, storage_key, duration, width, height, is_demo, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
    assetId, userId, projectId, kind, filename, mime, size, storageKey, meta.duration ?? null, meta.width ?? null, meta.height ?? null, isDemo ? 1 : 0, now());
  return assetId;
}

export const publicAssetUrl = (assetId, ttlMs = 3600e3) => {
  const exp = now() + ttlMs;
  return `${config.publicBaseUrl}/api/public/assets/${assetId}?exp=${exp}&sig=${sign(`${assetId}.${exp}`)}`;
};

async function download(url, headers, dest, allowInsecure = false) {
  // plain http is accepted only from our own engine service, whose address the administrator configured
  if (!/^https:\/\//.test(url) && !(allowInsecure && /^http:\/\//.test(url))) throw new ProviderError('provider returned a non-https video URL');
  let res;
  try { res = await fetch(url, { headers: headers || {}, redirect: 'follow', signal: AbortSignal.timeout(10 * 60e3) }); }
  catch (e) { throw new ProviderError(`download failed: ${e.cause?.code || e.message}`, { retryable: true }); }
  if (!res.ok || !res.body) throw new ProviderError(`download failed: HTTP ${res.status}`, { retryable: res.status >= 500 || res.status === 429 });
  let bytes = 0;
  const guard = async function* (src) { for await (const chunk of src) { bytes += chunk.length; if (bytes > MAX_VIDEO_BYTES) throw new ProviderError('video larger than 1 GB'); yield chunk; } };
  try { await pipe(Readable.fromWeb(res.body), guard, fs.createWriteStream(dest)); }
  catch (e) { await fsp.unlink(dest).catch(() => {}); throw e instanceof ProviderError ? e : new ProviderError(`download interrupted: ${e.message}`, { retryable: true }); }
}

/** Queues generation for the given scenes (default: every scene that has no finished clip). */
export function startGeneration(project, sceneIds = null) {
  const scenes = all('SELECT * FROM scenes WHERE project_id = ? ORDER BY position', project.id)
    .filter((s) => (sceneIds ? sceneIds.includes(s.id) : s.status !== 'completed'));
  for (const s of scenes) {
    queue.cancelProjectJobs(project.id, s.id);
    update('scenes', s.id, { status: 'queued', progress: 0, error: null, clip_asset_id: sceneIds ? null : s.clip_asset_id });
    queue.enqueue({ type: 'scene', userId: project.user_id, projectId: project.id, sceneId: s.id, providerId: project.provider_id });
  }
  for (const j of queue.activeJobs(project.id, 'assemble')) update('jobs', j.id, { status: 'canceled', finished_at: now() });
  update('projects', project.id, { status: scenes.length ? 'generating' : project.status, error: null, updated_at: now() });
  log.info('project.generation_started', `${scenes.length} scene(s) queued on ${project.provider_id}`, { userId: project.user_id, projectId: project.id });
  if (!scenes.length) maybeFinish(project.id);
  return scenes.length;
}

/** Decides what happens to the project after a scene finished or failed. Synchronous on purpose. */
export function maybeFinish(projectId) {
  const project = get('SELECT * FROM projects WHERE id = ?', projectId);
  if (!project || !['generating', 'queued'].includes(project.status)) return;
  const scenes = all('SELECT status FROM scenes WHERE project_id = ?', projectId);
  if (scenes.some((s) => ['queued', 'generating'].includes(s.status))) return;
  if (scenes.length && scenes.every((s) => s.status === 'completed')) return startAssembly(project);
  update('projects', projectId, { status: 'failed', error: 'scenes_failed', updated_at: now() });
}

export function startAssembly(project) {
  if (queue.activeJobs(project.id, 'assemble').length) return;
  update('projects', project.id, { status: 'assembling', error: null, updated_at: now() });
  queue.enqueue({ type: 'assemble', userId: project.user_id, projectId: project.id, maxAttempts: 2 });
}

export async function cancelProject(project) {
  const jobs = queue.cancelProjectJobs(project.id);
  for (const j of jobs) {
    if (!j.provider_job_id) continue;
    const p = getProvider(j.provider_id);
    try { await p?.cancel?.(j.provider_job_id, getCredentials(p)); } catch (e) { log.warn('provider.cancel_failed', String(e.message || e), { projectId: project.id, jobId: j.id }); }
  }
  run("UPDATE scenes SET status = 'pending', progress = NULL WHERE project_id = ? AND status IN ('queued','generating')", project.id);
  update('projects', project.id, { status: 'canceled', updated_at: now() });
  log.info('project.canceled', 'generation canceled by user', { userId: project.user_id, projectId: project.id });
}

// ── scene job ────────────────────────────────────────────────────────────────
async function sceneJob(job) {
  const scene = get('SELECT * FROM scenes WHERE id = ?', job.scene_id);
  const project = get('SELECT * FROM projects WHERE id = ?', job.project_id);
  if (!scene || !project) return { done: true };
  const ctx = { userId: project.user_id, projectId: project.id, jobId: job.id };
  const provider = getProvider(project.provider_id);
  if (!provider || !isEnabled(provider) || !isConfigured(provider)) throw new ProviderError('provider is not configured', { code: 'provider_not_configured' });
  const creds = getCredentials(provider);
  const quality = getQuality(provider, project.quality);
  if (!quality) throw new ProviderError('quality tier no longer offered by the provider', { code: 'provider_rejected' });
  const options = parse(project.options_json, {});
  const payload = parse(job.payload_json, {});

  if (!job.provider_job_id) {
    // frame chaining: start this scene from the last frame of the previous one
    let image = null;
    const ref = scene.reference_asset_id && get("SELECT * FROM assets WHERE id = ? AND kind = 'reference_image'", scene.reference_asset_id);
    if (quality.imageToVideo && ref) {
      image = quality.imageByUrl ? { url: publicAssetUrl(ref.id) } : { buffer: await storage.read(ref.storage_key), mime: ref.mime };
    } else if (quality.imageToVideo && !quality.imageByUrl && options.chainFrames && scene.position > 0) {
      const prev = get('SELECT * FROM scenes WHERE project_id = ? AND position = ?', project.id, scene.position - 1);
      if (prev && prev.status !== 'completed') {
        if (prev.status === 'failed') throw new ProviderError('the previous scene failed, so its last frame is not available', { code: 'chain_broken' });
        return { again: 3000 };
      }
      const clip = prev && get('SELECT * FROM assets WHERE id = ?', prev.clip_asset_id);
      if (clip) {
        const png = storage.tmpPath('png');
        try { await lastFrame(storage.localPath(clip.storage_key), png); image = { buffer: await fsp.readFile(png), mime: 'image/png' }; }
        finally { await fsp.unlink(png).catch(() => {}); }
      }
    }
    const busy = get("SELECT COUNT(*) AS n FROM jobs WHERE provider_id = ? AND provider_job_id IS NOT NULL AND status IN ('queued','running')", provider.id).n;
    if (busy >= (provider.maxConcurrent || 2)) return { again: 3000 };

    const audio = parse(project.audio_json, null);
    const total = get('SELECT COUNT(*) AS n FROM scenes WHERE project_id = ?', project.id).n;
    const treatment = parse(project.treatment_json, null);
    const extra = quality.nativeAudio ? audioDirection(audio) : '';
    const prompt = (scene.prompt + extra).slice(0, quality.maxPromptChars);
    const res = await provider.submit({
      prompt, negativePrompt: quality.negativePrompt && treatment ? negativePrompt(treatment) : undefined,
      duration: scene.duration, aspect: project.aspect, quality: project.quality, image, wantAudio: quality.nativeAudio,
      meta: { index: scene.position + 1, total, cameraMove: scene.camera_move, videoType: project.video_type, clientRef: `${project.id}:${scene.position + 1}` },
    }, creds);
    update('jobs', job.id, { provider_job_id: res.jobId, payload_json: JSON.stringify({ ...payload, clipDuration: res.clipDuration, submittedAt: now() }), updated_at: now() });
    update('scenes', scene.id, { status: 'generating', progress: 0, error: null });
    log.info('provider.submitted', `scene ${scene.position + 1} → ${provider.id} job ${res.jobId}${res.info ? ` (${res.info})` : ''}`, ctx);
    return { again: provider.minPollMs || config.pollIntervalMs };
  }

  if (now() - (payload.submittedAt || job.started_at || now()) > JOB_TIMEOUT_MS) throw new ProviderError('generation timed out after 30 minutes', { retryable: true, code: 'provider_timeout' });
  const st = await provider.poll(job.provider_job_id, creds);
  if (st.status === 'pending' || st.status === 'running') {
    if (typeof st.progress === 'number') { update('scenes', scene.id, { progress: st.progress }); update('jobs', job.id, { progress: st.progress }); }
    return { again: provider.minPollMs || config.pollIntervalMs };
  }
  if (st.status === 'failed') throw new ProviderError(st.error || 'generation failed', { retryable: !!st.retryable, code: 'provider_generation_failed' });

  // succeeded → bring the clip into our own storage (provider URLs expire)
  const tmp = st.localFile || storage.tmpPath('mp4');
  if (!st.localFile) await download(st.videoUrl, st.downloadHeaders, tmp, provider.id === 'selfhosted' && st.allowInsecure);
  const sceneIsDemo = provider.demo || !!st.demo;   // a mock GPU worker produces placeholders: label them like demo output
  if (sceneIsDemo && !project.is_demo) update('projects', project.id, { is_demo: 1 });
  let meta;
  try { meta = await probe(tmp); } catch { meta = null; }
  if (!meta?.hasVideo) { await fsp.unlink(tmp).catch(() => {}); throw new ProviderError('the provider returned a file that is not a playable video', { retryable: true }); }
  const key = storage.newKey(project.user_id, 'mp4');
  const size = await storage.putFile(key, tmp);
  const assetId = createAsset({ userId: project.user_id, projectId: project.id, kind: 'scene_clip', filename: `scene-${scene.position + 1}.mp4`, mime: 'video/mp4', storageKey: key, size, meta, isDemo: sceneIsDemo });
  update('scenes', scene.id, { status: 'completed', progress: 1, clip_asset_id: assetId, error: null });
  run('INSERT INTO usage (user_id, project_id, provider_id, seconds, is_demo, created_at) VALUES (?,?,?,?,?,?)', project.user_id, project.id, provider.id, payload.clipDuration || scene.duration, sceneIsDemo ? 1 : 0, now());
  log.info('scene.completed', `scene ${scene.position + 1} stored (${Math.round(size / 1024)} KB)`, ctx);
  maybeFinish(project.id);
  return { done: true };
}

function sceneFailed(job, err) {
  if (job.scene_id) update('scenes', job.scene_id, { status: 'failed', error: `${err?.code || 'error'}: ${String(err?.message || err).slice(0, 400)}` });
  maybeFinish(job.project_id);
}

// ── assemble job ─────────────────────────────────────────────────────────────
async function saveAudio(project, kind, buffer) {
  const tmp = storage.tmpPath('mp3');
  await fsp.writeFile(tmp, buffer);
  const meta = await probe(tmp);
  const key = storage.newKey(project.user_id, 'mp3');
  const size = await storage.putFile(key, tmp);
  return createAsset({ userId: project.user_id, projectId: project.id, kind, filename: `${kind}.mp3`, mime: 'audio/mpeg', storageKey: key, size, meta });
}

/** Resolves the audio settings into a list of files to mix. Generated audio is cached per prompt. */
async function resolveTracks(project, scenes, total) {
  const audio = parse(project.audio_json, null) || defaultAudio();
  const cache = audio.generated || {};
  const tracks = [];
  const ap = getAudioProvider();
  const creds = ap && audioCreds(ap);
  const file = (assetId) => { const a = assetId && get('SELECT * FROM assets WHERE id = ? AND user_id = ?', assetId, project.user_id); return a ? storage.localPath(a.storage_key) : null; };
  const generated = async (slot, cacheKey, make) => {
    if (cache[slot]?.key === cacheKey && file(cache[slot].assetId)) return file(cache[slot].assetId);
    if (!ap) throw new ProviderError('audio generation was requested but no audio provider is configured', { code: 'audio_not_configured' });
    const assetId = await saveAudio(project, slot.startsWith('vo') ? 'voiceover' : slot, await make());
    cache[slot] = { key: cacheKey, assetId };
    return file(assetId);
  };

  for (const k of ['music', 'ambience', 'sfx']) {
    const t = audio[k];
    if (t.mode === 'upload' && file(t.assetId)) tracks.push({ path: file(t.assetId), volume: t.volume, loop: k !== 'sfx' });
    else if (t.mode === 'generate' && t.prompt.trim()) {
      const secs = k === 'music' ? total : Math.min(30, total);
      const p = await generated(k, `${t.prompt}|${secs}`, () => (k === 'music' ? ap.music({ prompt: t.prompt, seconds: secs }, creds) : ap.effect({ prompt: t.prompt, seconds: secs, loop: k === 'ambience' }, creds)));
      tracks.push({ path: p, volume: t.volume, loop: k !== 'sfx' });
    }
  }
  const vo = audio.voiceover;
  if (vo.mode === 'upload' && file(vo.assetId)) tracks.push({ path: file(vo.assetId), volume: vo.volume, offset: 0 });
  else if (vo.mode === 'generate') {
    if (!vo.voiceId) throw new ProviderError('voice-over generation needs a voice to be selected', { code: 'audio_voice_missing' });
    // sync: each scene's line starts when its scene starts
    let offset = 0;
    for (const s of scenes) {
      const text = (s.voiceover || '').trim();
      if (text) tracks.push({ path: await generated(`vo_${s.id}`, `${vo.voiceId}|${text}`, () => ap.voiceover({ text, voiceId: vo.voiceId }, creds)), volume: vo.volume, offset });
      offset += s.duration;
    }
    if (!scenes.some((s) => (s.voiceover || '').trim()) && vo.prompt.trim()) tracks.push({ path: await generated('vo_all', `${vo.voiceId}|${vo.prompt}`, () => ap.voiceover({ text: vo.prompt, voiceId: vo.voiceId }, creds)), volume: vo.volume, offset: 0 });
  }
  update('projects', project.id, { audio_json: JSON.stringify({ ...audio, generated: cache }) });
  return { tracks, clipAudioVolume: audio.clipAudioVolume };
}

async function assembleJob(job) {
  const project = get('SELECT * FROM projects WHERE id = ?', job.project_id);
  if (!project) return { done: true };
  const ctx = { userId: project.user_id, projectId: project.id, jobId: job.id };
  const scenes = all('SELECT * FROM scenes WHERE project_id = ? ORDER BY position', project.id);
  const clips = scenes.map((s) => {
    const a = get('SELECT * FROM assets WHERE id = ?', s.clip_asset_id);
    if (!a) throw new Error(`scene ${s.position + 1} has no clip`);
    return { path: storage.localPath(a.storage_key), asset: a, target: s.duration };
  });
  const metas = await Promise.all(clips.map((c) => probe(c.path)));
  const list = clips.map((c, i) => ({ path: c.path, duration: c.target, sourceDuration: Math.min(c.target, metas[i].duration || c.target), hasAudio: metas[i].hasAudio }));
  const total = list.reduce((s, c) => s + c.duration, 0);
  const { tracks, clipAudioVolume } = await resolveTracks(project, scenes, total);
  const width = Math.floor((metas[0].width || 1280) / 2) * 2, height = Math.floor((metas[0].height || 720) / 2) * 2;
  const out = storage.tmpPath('mp4');
  await assemble({ clips: list, tracks, out, width, height, clipAudioVolume });
  const meta = await probe(out);
  const isDemo = !!project.is_demo;
  const key = storage.newKey(project.user_id, 'mp4');
  const size = await storage.putFile(key, out);
  const finalId = createAsset({ userId: project.user_id, projectId: project.id, kind: 'final_video', filename: `film${isDemo ? '-demo' : ''}.mp4`, mime: 'video/mp4', storageKey: key, size, meta, isDemo });
  try {
    const jpg = storage.tmpPath('jpg');
    await poster(storage.localPath(key), jpg, Math.min(1, total / 2));
    const pk = storage.newKey(project.user_id, 'jpg');
    const ps = await storage.putFile(pk, jpg);
    const posterId = createAsset({ userId: project.user_id, projectId: project.id, kind: 'poster', filename: 'poster.jpg', mime: 'image/jpeg', storageKey: pk, size: ps, isDemo });
    const options = parse(project.options_json, {});
    update('projects', project.id, { options_json: JSON.stringify({ ...options, posterAssetId: posterId }) });
  } catch (e) { log.warn('assemble.poster_failed', String(e.message || e), ctx); }
  update('projects', project.id, { status: 'completed', final_asset_id: finalId, error: null, updated_at: now() });
  log.info('project.completed', `final film ${meta.duration?.toFixed(1)}s, ${width}x${height}, ${tracks.length} audio track(s)`, ctx);
  return { done: true };
}

function assembleFailed(job, err) {
  update('projects', job.project_id, { status: 'failed', error: `assembly: ${String(err?.message || err).slice(0, 400)}`, updated_at: now() });
}

export function registerPipeline() {
  queue.register('scene', sceneJob, sceneFailed);
  queue.register('assemble', assembleJob, assembleFailed);
}
