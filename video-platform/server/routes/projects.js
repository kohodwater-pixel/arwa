import { Router } from 'express';
import { all, get, run, update, now, id, tx } from '../db.js';
import { config } from '../config.js';
import { HttpError, requireAuth } from '../auth.js';
import { storage } from '../storage.js';
import * as log from '../log.js';
import { randomToken } from '../secrets.js';
import { direct, redirectScene, withPrompts, videoTypes, styles, cameraMoves, shotSizes, byId, compileMasterPrompt } from '../engine/index.js';
import { roleTitle } from '../engine/storyboard.js';
import { getProvider, isConfigured, isEnabled, getQuality } from '../providers/index.js';
import { sanitizeAudio, defaultAudio, getAudioProvider, TRACKS } from '../audio/index.js';
import { startGeneration, startAssembly, cancelProject } from '../pipeline.js';
import { assertCanGenerate } from '../limits.js';
import { assetJson } from './assets.js';

export const projectsRouter = Router();
projectsRouter.use(requireAuth);

const ACTIVE = ['queued', 'generating', 'assembling'];
const GENERATED_KINDS = ['scene_clip', 'final_video', 'poster', 'voiceover', 'music', 'sfx', 'ambience'];
const parse = (s, d) => { try { return s ? JSON.parse(s) : d; } catch { return d; } };
const ctxOf = (req, p) => ({ userId: req.user.id, projectId: p?.id });

function own(req) {
  const p = get('SELECT * FROM projects WHERE id = ?', req.params.id);
  if (!p || (p.user_id !== req.user.id && req.user.role !== 'admin')) throw new HttpError(404, 'project_not_found');
  return p;
}
const assertIdle = (p) => { if (ACTIVE.includes(p.status)) throw new HttpError(409, 'project_busy'); };
const scenesOf = (pid) => all('SELECT * FROM scenes WHERE project_id = ? ORDER BY position', pid);

/** Checks provider / quality / aspect against what the connected engine really supports. */
function resolveSettings({ providerId, quality, aspect }) {
  const provider = getProvider(providerId);
  if (!provider || !isEnabled(provider)) throw new HttpError(400, 'provider_unavailable');
  if (!isConfigured(provider)) throw new HttpError(400, 'provider_not_configured');
  const q = getQuality(provider, quality);
  if (!q) throw new HttpError(400, 'unsupported_option', undefined, { field: 'quality' });
  if (!q.aspects.includes(aspect)) throw new HttpError(400, 'unsupported_option', undefined, { field: 'aspect' });
  return { provider, q, caps: { clip: q.clip, maxPromptChars: q.maxPromptChars, negativePrompt: q.negativePrompt } };
}

function readSettings(body, base = {}) {
  const s = {
    description: body.description !== undefined ? String(body.description).trim() : base.description,
    title: body.title !== undefined ? String(body.title).trim().slice(0, 120) : base.title,
    videoType: body.videoType ?? base.video_type, style: body.style ?? base.style,
    duration: body.duration !== undefined ? Math.round(Number(body.duration)) : base.duration,
    aspect: body.aspect ?? base.aspect, quality: body.quality ?? base.quality, providerId: body.providerId ?? base.provider_id,
  };
  if (!s.description || s.description.length < 10) throw new HttpError(400, 'description_too_short');
  if (s.description.length > 4000) throw new HttpError(400, 'description_too_long');
  if (!byId(videoTypes, s.videoType)) throw new HttpError(400, 'unsupported_option', undefined, { field: 'videoType' });
  if (!byId(styles, s.style)) throw new HttpError(400, 'unsupported_option', undefined, { field: 'style' });
  if (!Number.isFinite(s.duration) || s.duration < 2 || s.duration > config.maxProjectSeconds) throw new HttpError(400, 'bad_duration', undefined, { max: config.maxProjectSeconds });
  if (!s.title) s.title = s.description.replace(/\s+/g, ' ').slice(0, 60);
  return s;
}

async function removeAssets(rows) {
  for (const a of rows) { run('DELETE FROM assets WHERE id = ?', a.id); await storage.remove(a.storage_key); }
}
async function dropClip(scene) {
  if (!scene.clip_asset_id) return;
  await removeAssets(all('SELECT * FROM assets WHERE id = ?', scene.clip_asset_id));
}

function insertScene(projectId, s, position) {
  const sid = id();
  run(`INSERT INTO scenes (id, project_id, position, role, title, description, duration, shot_size, camera_move, camera_angle, lighting, prompt, prompt_edited, variant, action_en, reference_asset_id, voiceover, status)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'pending')`,
    sid, projectId, position, s.role || 'action', s.title, s.description, s.duration, s.shot_size, s.camera_move, s.camera_angle || null, s.lighting || null,
    s.prompt || '', s.prompt_edited ? 1 : 0, s.variant || 0, s.action_en || null, s.reference_asset_id || null, s.voiceover || null);
  return sid;
}

/** Re-numbers scenes, recompiles the prompts that the user has not hand-edited and syncs the project duration. */
function refresh(project) {
  const { caps } = resolveSettings({ providerId: project.provider_id, quality: project.quality, aspect: project.aspect });
  const t = parse(project.treatment_json, null);
  const scenes = scenesOf(project.id);
  scenes.forEach((s, i) => { if (s.position !== i) { update('scenes', s.id, { position: i }); s.position = i; } });
  if (t) withPrompts(scenes, t, caps).forEach((s) => update('scenes', s.id, { prompt: s.prompt }));
  const total = scenes.reduce((n, s) => n + s.duration, 0);
  update('projects', project.id, { duration: total || project.duration, updated_at: now() });
}

/** A change that invalidates finished video: the project goes back to the storyboard stage. */
function reopen(project) {
  if (['completed', 'failed', 'canceled'].includes(project.status)) update('projects', project.id, { status: 'storyboard', error: null, updated_at: now() });
}

function sceneJson(s) {
  return { id: s.id, position: s.position, role: s.role, title: s.title, description: s.description, duration: s.duration, shotSize: s.shot_size, cameraMove: s.camera_move,
    cameraAngle: s.camera_angle, lighting: s.lighting, prompt: s.prompt, promptEdited: !!s.prompt_edited, referenceAssetId: s.reference_asset_id, voiceover: s.voiceover || '',
    status: s.status, progress: s.progress, error: s.error, clip: s.clip_asset_id ? assetJson(get('SELECT * FROM assets WHERE id = ?', s.clip_asset_id)) : null };
}

export function projectJson(p, full = false) {
  const provider = getProvider(p.provider_id);
  const options = parse(p.options_json, {});
  const base = {
    id: p.id, title: p.title, description: p.description, videoType: p.video_type, style: p.style, duration: p.duration, aspect: p.aspect, quality: p.quality,
    providerId: p.provider_id, providerLabel: provider?.label || p.provider_id, status: p.status, isDemo: !!p.is_demo, error: p.error,
    createdAt: p.created_at, updatedAt: p.updated_at, shareToken: p.share_token || null,
    posterUrl: options.posterAssetId && p.final_asset_id ? `/api/assets/${options.posterAssetId}/file` : null,
    final: p.final_asset_id ? assetJson(get('SELECT * FROM assets WHERE id = ?', p.final_asset_id)) : null,
  };
  const sc = full ? scenesOf(p.id) : all('SELECT status, progress FROM scenes WHERE project_id = ?', p.id);
  const done = sc.filter((s) => s.status === 'completed').length;
  base.sceneCount = sc.length;
  base.scenesCompleted = done;
  base.progress = !sc.length ? 0 : p.status === 'completed' ? 1 : (sc.reduce((n, s) => n + (s.status === 'completed' ? 1 : s.status === 'generating' ? Math.min(0.95, s.progress || 0.05) : 0), 0) / sc.length) * (p.status === 'assembling' ? 1 : 0.95);
  if (!full) return base;
  const audio = parse(p.audio_json, null) || defaultAudio();
  delete audio.generated;
  return {
    ...base, treatment: parse(p.treatment_json, null), audio, options: { chainFrames: !!options.chainFrames },
    capabilities: provider ? getQuality(provider, p.quality) : null,
    providerUsable: !!provider && isEnabled(provider) && isConfigured(provider),
    scenes: sc.map(sceneJson),
    references: all("SELECT * FROM assets WHERE project_id = ? AND kind IN ('reference_image','reference_video') ORDER BY created_at", p.id).map(assetJson),
    audioFiles: all("SELECT * FROM assets WHERE user_id = ? AND kind = 'audio_upload' ORDER BY created_at DESC LIMIT 100", p.user_id).map(assetJson),
  };
}

async function buildStoryboard(req, project) {
  const { caps } = resolveSettings({ providerId: project.provider_id, quality: project.quality, aspect: project.aspect });
  const { treatment, scenes } = await direct({ description: project.description, videoType: project.video_type, style: project.style, duration: project.duration, caps, ctx: ctxOf(req, project) });
  const old = scenesOf(project.id);
  for (const s of old) await dropClip(s);
  tx(() => {
    run('DELETE FROM scenes WHERE project_id = ?', project.id);
    scenes.forEach((s, i) => insertScene(project.id, s, i));
    update('projects', project.id, { treatment_json: JSON.stringify(treatment), status: 'storyboard', error: null, updated_at: now() });
  });
  log.info('engine.storyboard', `${scenes.length} scene(s), director: ${treatment.engine}`, ctxOf(req, project));
}

// ── list / create ────────────────────────────────────────────────────────────
projectsRouter.get('/', (req, res) => {
  const groups = { completed: ['completed'], active: ACTIVE, failed: ['failed', 'canceled'], drafts: ['draft', 'storyboard'] };
  const st = groups[req.query.status];
  const q = String(req.query.q || '').trim().slice(0, 80);
  const where = ['user_id = ?'], params = [req.user.id];
  if (st) { where.push(`status IN (${st.map(() => '?').join(',')})`); params.push(...st); }
  if (q) { where.push('(title LIKE ? OR description LIKE ?)'); params.push(`%${q}%`, `%${q}%`); }
  const rows = all(`SELECT * FROM projects WHERE ${where.join(' AND ')} ORDER BY updated_at DESC LIMIT 200`, ...params);
  const counts = {};
  for (const [k, list] of Object.entries(groups)) counts[k] = get(`SELECT COUNT(*) AS n FROM projects WHERE user_id = ? AND status IN (${list.map(() => '?').join(',')})`, req.user.id, ...list).n;
  counts.all = get('SELECT COUNT(*) AS n FROM projects WHERE user_id = ?', req.user.id).n;
  res.json({ projects: rows.map((p) => projectJson(p)), counts });
});

projectsRouter.post('/', async (req, res) => {
  const s = readSettings(req.body || {});
  const { provider } = resolveSettings(s);
  const pid = id(), t = now();
  const audio = sanitizeAudio(req.body?.audio);
  const options = { chainFrames: !!req.body?.options?.chainFrames };
  run(`INSERT INTO projects (id, user_id, title, description, video_type, style, duration, aspect, quality, provider_id, status, is_demo, audio_json, options_json, created_at, updated_at)
       VALUES (?,?,?,?,?,?,?,?,?,?, 'draft', ?, ?, ?, ?, ?)`,
    pid, req.user.id, s.title, s.description, s.videoType, s.style, s.duration, s.aspect, s.quality, s.providerId, provider.demo ? 1 : 0, JSON.stringify(audio), JSON.stringify(options), t, t);
  for (const aid of Array.isArray(req.body?.referenceAssetIds) ? req.body.referenceAssetIds.slice(0, 20) : [])
    run("UPDATE assets SET project_id = ? WHERE id = ? AND user_id = ? AND kind IN ('reference_image','reference_video')", pid, String(aid), req.user.id);
  const project = get('SELECT * FROM projects WHERE id = ?', pid);
  if (!req.body?.draft) await buildStoryboard(req, project);
  log.info('project.created', req.body?.draft ? 'saved as draft' : 'created with storyboard', ctxOf(req, project));
  res.status(201).json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', pid), true) });
});

projectsRouter.get('/:id', (req, res) => res.json({ project: projectJson(own(req), true) }));

projectsRouter.patch('/:id', async (req, res) => {
  const p = own(req); assertIdle(p);
  const b = req.body || {};
  const s = readSettings(b, p);
  const { provider, q } = resolveSettings(s);
  const engineChanged = s.providerId !== p.provider_id || s.quality !== p.quality || s.aspect !== p.aspect;
  const f = { title: s.title, description: s.description, video_type: s.videoType, style: s.style, aspect: s.aspect, quality: s.quality, provider_id: s.providerId, is_demo: provider.demo ? 1 : 0, updated_at: now() };
  const scenes = scenesOf(p.id);
  if (!scenes.length) f.duration = s.duration;
  if (b.audio) f.audio_json = JSON.stringify({ ...sanitizeAudio(b.audio, sanitizeAudio(parse(p.audio_json, null))), generated: parse(p.audio_json, {})?.generated });
  if (b.options) f.options_json = JSON.stringify({ ...parse(p.options_json, {}), chainFrames: !!b.options.chainFrames });
  update('projects', p.id, f);
  if (engineChanged && scenes.length) {
    for (const sc of scenes) { await dropClip(sc); update('scenes', sc.id, { status: 'pending', clip_asset_id: null, progress: null, error: null, duration: Math.min(sc.duration, q.clip.max) }); }
    reopen(p);
  }
  if (scenes.length) refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  res.json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });
});

projectsRouter.delete('/:id', async (req, res) => {
  const p = own(req);
  if (ACTIVE.includes(p.status)) await cancelProject(p);
  await removeAssets(all(`SELECT * FROM assets WHERE project_id = ? AND kind IN (${GENERATED_KINDS.map(() => '?').join(',')})`, p.id, ...GENERATED_KINDS));
  run('DELETE FROM projects WHERE id = ?', p.id);
  log.info('project.deleted', p.title, { userId: req.user.id });
  res.json({ ok: true });
});

projectsRouter.post('/:id/duplicate', (req, res) => {
  const p = own(req);
  const pid = id(), t = now();
  const audio = parse(p.audio_json, null); if (audio) delete audio.generated;
  const options = parse(p.options_json, {}); delete options.posterAssetId;
  const scenes = scenesOf(p.id);
  const suffix = /[؀-ۿ]/.test(p.title) ? ' (نسخة)' : ' (copy)';
  tx(() => {
    run(`INSERT INTO projects (id, user_id, title, description, video_type, style, duration, aspect, quality, provider_id, status, is_demo, treatment_json, audio_json, options_json, created_at, updated_at)
         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`,
      pid, req.user.id, (p.title + suffix).slice(0, 120), p.description, p.video_type, p.style, p.duration, p.aspect, p.quality, p.provider_id, scenes.length ? 'storyboard' : 'draft', p.is_demo, p.treatment_json, audio ? JSON.stringify(audio) : null, JSON.stringify(options), t, t);
    scenes.forEach((s, i) => insertScene(pid, s, i));
  });
  res.status(201).json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', pid), true) });
});

projectsRouter.post('/:id/storyboard', async (req, res) => {
  const p = own(req); assertIdle(p);
  if (req.body?.duration !== undefined) {
    const d = Math.round(Number(req.body.duration));
    if (!Number.isFinite(d) || d < 2 || d > config.maxProjectSeconds) throw new HttpError(400, 'bad_duration', undefined, { max: config.maxProjectSeconds });
    update('projects', p.id, { duration: d });
  }
  await buildStoryboard(req, get('SELECT * FROM projects WHERE id = ?', p.id));
  res.json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });
});

// ── scenes ───────────────────────────────────────────────────────────────────
function ownScene(req, p) {
  const s = get('SELECT * FROM scenes WHERE id = ? AND project_id = ?', req.params.sid, p.id);
  if (!s) throw new HttpError(404, 'scene_not_found');
  return s;
}
const done = (res, p) => res.json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });

projectsRouter.patch('/:id/scenes/:sid', async (req, res) => {
  const p = own(req); assertIdle(p);
  const s = ownScene(req, p), b = req.body || {};
  const { q } = resolveSettings({ providerId: p.provider_id, quality: p.quality, aspect: p.aspect });
  const f = {}; let visual = false;
  if (b.title !== undefined) f.title = String(b.title).trim().slice(0, 80) || s.title;
  if (b.voiceover !== undefined) f.voiceover = String(b.voiceover).slice(0, 1000);
  if (b.description !== undefined && String(b.description).trim() !== s.description) {
    f.description = String(b.description).trim().slice(0, 1500);
    if (f.description.length < 3) throw new HttpError(400, 'description_too_short');
    f.action_en = null; f.prompt_edited = 0; visual = true; // the user's own words now drive the prompt
  }
  if (b.duration !== undefined && Number(b.duration) !== s.duration) {
    const d = Math.round(Number(b.duration));
    if (!Number.isFinite(d) || d < 1 || d > q.clip.max) throw new HttpError(400, 'bad_scene_duration', undefined, { max: q.clip.max });
    const total = scenesOf(p.id).reduce((n, x) => n + (x.id === s.id ? d : x.duration), 0);
    if (total > config.maxProjectSeconds) throw new HttpError(400, 'bad_duration', undefined, { max: config.maxProjectSeconds });
    f.duration = d; visual = true;
  }
  if (b.cameraMove !== undefined && b.cameraMove !== s.camera_move) { if (!byId(cameraMoves, b.cameraMove)) throw new HttpError(400, 'unsupported_option', undefined, { field: 'cameraMove' }); f.camera_move = b.cameraMove; f.prompt_edited = 0; visual = true; }
  if (b.shotSize !== undefined && b.shotSize !== s.shot_size) { if (!byId(shotSizes, b.shotSize)) throw new HttpError(400, 'unsupported_option', undefined, { field: 'shotSize' }); f.shot_size = b.shotSize; f.prompt_edited = 0; visual = true; }
  if (b.referenceAssetId !== undefined && b.referenceAssetId !== s.reference_asset_id) {
    if (b.referenceAssetId) {
      const a = get("SELECT id FROM assets WHERE id = ? AND user_id = ? AND kind = 'reference_image'", String(b.referenceAssetId), p.user_id);
      if (!a) throw new HttpError(400, 'reference_must_be_image');
      if (!q.imageToVideo) throw new HttpError(400, 'reference_not_supported');
    }
    f.reference_asset_id = b.referenceAssetId || null; visual = true;
  }
  if (b.prompt !== undefined && String(b.prompt).trim() !== s.prompt) {
    const pr = String(b.prompt).trim();
    if (pr.length < 10 || pr.length > q.maxPromptChars) throw new HttpError(400, 'bad_prompt_length', undefined, { max: q.maxPromptChars });
    f.prompt = pr; f.prompt_edited = 1; visual = true;
  }
  if (b.resetPrompt) { f.prompt_edited = 0; visual = true; }
  if (visual) { await dropClip(s); Object.assign(f, { status: 'pending', clip_asset_id: null, progress: null, error: null }); reopen(p); }
  update('scenes', s.id, f);
  refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  done(res, p);
});

projectsRouter.post('/:id/scenes', (req, res) => {
  const p = own(req); assertIdle(p);
  const scenes = scenesOf(p.id);
  if (scenes.length >= 24) throw new HttpError(400, 'too_many_scenes');
  const { q } = resolveSettings({ providerId: p.provider_id, quality: p.quality, aspect: p.aspect });
  const duration = Math.min(q.clip.max, 5);
  if (scenes.reduce((n, s) => n + s.duration, 0) + duration > config.maxProjectSeconds) throw new HttpError(400, 'bad_duration', undefined, { max: config.maxProjectSeconds });
  const t = parse(p.treatment_json, null);
  const lang = t?.language || 'ar';
  const after = Math.min(scenes.length, Math.max(0, Number.isInteger(req.body?.position) ? req.body.position : scenes.length));
  tx(() => {
    run('UPDATE scenes SET position = position + 1000 WHERE project_id = ? AND position >= ?', p.id, after);
    insertScene(p.id, { role: 'action', title: roleTitle('action', lang), description: lang === 'ar' ? 'اكتب وصف هذا المشهد: ماذا يظهر في الكادر وماذا يتحرك.' : 'Describe this scene: what is in frame and what moves.',
      duration, shot_size: 'medium', camera_move: 'dolly_in', lighting: t?.lighting?.scheme }, after);
  });
  // close the gap left by the temporary +1000 shift
  all('SELECT id FROM scenes WHERE project_id = ? ORDER BY CASE WHEN position >= 1000 THEN position - 999.5 ELSE position END', p.id).forEach((r, i) => update('scenes', r.id, { position: i }));
  reopen(p);
  refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  done(res, p);
});

projectsRouter.delete('/:id/scenes/:sid', async (req, res) => {
  const p = own(req); assertIdle(p);
  const s = ownScene(req, p);
  if (scenesOf(p.id).length <= 1) throw new HttpError(400, 'last_scene');
  await dropClip(s);
  run('DELETE FROM scenes WHERE id = ?', s.id);
  reopen(p);
  refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  done(res, p);
});

projectsRouter.post('/:id/scenes/reorder', (req, res) => {
  const p = own(req); assertIdle(p);
  const scenes = scenesOf(p.id);
  const order = Array.isArray(req.body?.order) ? req.body.order.map(String) : [];
  if (order.length !== scenes.length || new Set(order).size !== order.length || !order.every((x) => scenes.some((s) => s.id === x))) throw new HttpError(400, 'bad_order');
  if (order.some((x, i) => scenes[i].id !== x)) {
    tx(() => order.forEach((sid, i) => update('scenes', sid, { position: i })));
    reopen(p); // the cut order changed: the film must be assembled again
  }
  refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  done(res, p);
});

/** New take on one storyboard scene (text only; no video is generated here). */
projectsRouter.post('/:id/scenes/:sid/regenerate', async (req, res) => {
  const p = own(req); assertIdle(p);
  const s = ownScene(req, p);
  const t = parse(p.treatment_json, null);
  if (!t) throw new HttpError(400, 'no_storyboard');
  const scenes = scenesOf(p.id);
  const next = await redirectScene(t, scenes, s.position, { ctx: ctxOf(req, p) });
  await dropClip(s);
  update('scenes', s.id, { title: next.title, description: next.description, camera_move: next.camera_move, shot_size: next.shot_size, camera_angle: next.camera_angle, action_en: next.action_en || null,
    variant: next.variant, prompt_edited: 0, status: 'pending', clip_asset_id: null, progress: null, error: null });
  reopen(p);
  refresh(get('SELECT * FROM projects WHERE id = ?', p.id));
  done(res, p);
});

// ── generation ───────────────────────────────────────────────────────────────
function preflight(req, p, scenes, toGenerate) {
  if (!scenes.length) throw new HttpError(400, 'no_storyboard');
  const { provider, q } = resolveSettings({ providerId: p.provider_id, quality: p.quality, aspect: p.aspect });
  const bad = scenes.find((s) => s.duration > q.clip.max);
  if (bad) throw new HttpError(400, 'bad_scene_duration', undefined, { max: q.clip.max, scene: bad.position + 1 });
  const audio = parse(p.audio_json, null);
  if (audio && TRACKS.some((k) => audio[k]?.mode === 'generate') && !getAudioProvider()) throw new HttpError(400, 'audio_not_configured');
  if (audio?.voiceover?.mode === 'generate' && !audio.voiceover.voiceId) throw new HttpError(400, 'audio_voice_missing');
  assertCanGenerate(req.user, { seconds: toGenerate.reduce((n, s) => n + s.duration, 0), isDemo: provider.demo });
  update('projects', p.id, { is_demo: provider.demo ? 1 : 0 });
}

projectsRouter.post('/:id/generate', (req, res) => {
  const p = own(req); assertIdle(p);
  const scenes = scenesOf(p.id);
  const all_ = !!req.body?.all; // regenerate every scene, not only the unfinished ones
  const todo = all_ ? scenes : scenes.filter((s) => s.status !== 'completed');
  preflight(req, p, scenes, todo);
  startGeneration(get('SELECT * FROM projects WHERE id = ?', p.id), all_ ? scenes.map((s) => s.id) : null);
  res.status(202).json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });
});

/** Regenerates the video of one scene; the film is re-assembled automatically when it finishes. */
projectsRouter.post('/:id/scenes/:sid/generate', (req, res) => {
  const p = own(req); assertIdle(p);
  const s = ownScene(req, p);
  const scenes = scenesOf(p.id);
  preflight(req, p, scenes, [s, ...scenes.filter((x) => x.id !== s.id && x.status !== 'completed')]);
  const ids = [s.id, ...scenes.filter((x) => x.id !== s.id && x.status !== 'completed').map((x) => x.id)];
  startGeneration(get('SELECT * FROM projects WHERE id = ?', p.id), ids);
  res.status(202).json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });
});

projectsRouter.post('/:id/cancel', async (req, res) => {
  const p = own(req);
  if (!ACTIVE.includes(p.status)) throw new HttpError(409, 'not_running');
  await cancelProject(p);
  done(res, p);
});

/** Mixes the film again from the existing clips (after an audio or order change). */
projectsRouter.post('/:id/assemble', (req, res) => {
  const p = own(req); assertIdle(p);
  const scenes = scenesOf(p.id);
  if (!scenes.length || scenes.some((s) => s.status !== 'completed')) throw new HttpError(400, 'scenes_incomplete');
  const audio = parse(p.audio_json, null);
  if (audio && TRACKS.some((k) => audio[k]?.mode === 'generate') && !getAudioProvider()) throw new HttpError(400, 'audio_not_configured');
  startAssembly(p);
  res.status(202).json({ project: projectJson(get('SELECT * FROM projects WHERE id = ?', p.id), true) });
});

projectsRouter.post('/:id/share', (req, res) => {
  const p = own(req);
  if (req.body?.enabled && (p.status !== 'completed' || !p.final_asset_id)) throw new HttpError(400, 'not_completed');
  update('projects', p.id, { share_token: req.body?.enabled ? p.share_token || randomToken(18) : null });
  done(res, p);
});

projectsRouter.get('/:id/master-prompt', (req, res) => {
  const t = parse(own(req).treatment_json, null);
  if (!t) throw new HttpError(400, 'no_storyboard');
  res.json({ masterPrompt: t.masterPrompt || compileMasterPrompt(t) });
});
