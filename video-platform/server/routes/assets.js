import { Router } from 'express';
import fs from 'node:fs';
import { all, get, run } from '../db.js';
import { HttpError, requireAuth } from '../auth.js';
import { storage } from '../storage.js';
import { uploadMiddleware, inspectUpload } from '../uploads.js';
import { createAsset } from '../pipeline.js';
import { assertStorage } from '../limits.js';
import { sign, safeEqual } from '../secrets.js';
import * as log from '../log.js';

export const assetsRouter = Router();
export const publicAssetsRouter = Router();

export const assetJson = (a) => a && ({
  id: a.id, kind: a.kind, filename: a.filename, mime: a.mime, size: a.size, duration: a.duration, width: a.width, height: a.height,
  isDemo: !!a.is_demo, projectId: a.project_id, createdAt: a.created_at, url: `/api/assets/${a.id}/file`,
});

function send(res, asset, download) {
  const file = storage.localPath(asset.storage_key);
  if (!fs.existsSync(file)) throw new HttpError(404, 'file_missing');
  res.setHeader('Content-Type', asset.mime);
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Cache-Control', 'private, max-age=3600');
  if (download) res.setHeader('Content-Disposition', `attachment; filename="${asset.filename.replace(/[^\w.\-]/g, '_')}"`);
  res.sendFile(file, { acceptRanges: true, headers: { 'Content-Type': asset.mime } });
}
export { send as sendAsset };

assetsRouter.use(requireAuth);

assetsRouter.post('/', (req, res, next) => {
  uploadMiddleware(req, res, (err) => {
    if (err) return next(new HttpError(err.code === 'LIMIT_FILE_SIZE' ? 413 : 400, err.code === 'LIMIT_FILE_SIZE' ? 'file_too_large' : 'upload_failed'));
    next();
  });
}, async (req, res) => {
  const purpose = req.body?.purpose === 'audio' ? 'audio' : 'reference';
  const info = await inspectUpload(req.file, purpose === 'audio' ? ['audio'] : ['image', 'video']);
  try { assertStorage(req.user); } catch (e) { fs.promises.unlink(req.file.path).catch(() => {}); throw e; }
  let projectId = null;
  if (req.body?.projectId) {
    const p = get('SELECT id FROM projects WHERE id = ? AND user_id = ?', String(req.body.projectId), req.user.id);
    if (!p) { fs.promises.unlink(req.file.path).catch(() => {}); throw new HttpError(404, 'project_not_found'); }
    projectId = p.id;
  }
  const key = storage.newKey(req.user.id, info.ext);
  const size = await storage.putFile(key, req.file.path);
  const kind = info.kind === 'audio' ? 'audio_upload' : info.kind === 'image' ? 'reference_image' : 'reference_video';
  const filename = String(req.file.originalname || 'file').replace(/[^\p{L}\p{N}.\-_ ]/gu, '_').slice(0, 120) || `file.${info.ext}`;
  const assetId = createAsset({ userId: req.user.id, projectId, kind, filename, mime: info.mime, storageKey: key, size, meta: info.meta });
  log.info('asset.uploaded', `${kind} ${Math.round(size / 1024)} KB`, { userId: req.user.id, projectId });
  res.status(201).json({ asset: assetJson(get('SELECT * FROM assets WHERE id = ?', assetId)) });
});

assetsRouter.get('/', (req, res) => {
  const kinds = String(req.query.kinds || 'reference_image,reference_video,audio_upload').split(',').filter((k) => /^[a-z_]+$/.test(k));
  const rows = all(`SELECT * FROM assets WHERE user_id = ? AND kind IN (${kinds.map(() => '?').join(',')}) ORDER BY created_at DESC LIMIT 300`, req.user.id, ...kinds);
  res.json({ assets: rows.map(assetJson) });
});

assetsRouter.get('/:id/file', (req, res) => {
  const a = get('SELECT * FROM assets WHERE id = ?', req.params.id);
  if (!a || (a.user_id !== req.user.id && req.user.role !== 'admin')) throw new HttpError(404, 'not_found');
  send(res, a, req.query.download === '1');
});

assetsRouter.delete('/:id', async (req, res) => {
  const a = get('SELECT * FROM assets WHERE id = ? AND user_id = ?', req.params.id, req.user.id);
  if (!a) throw new HttpError(404, 'not_found');
  if (!['reference_image', 'reference_video', 'audio_upload'].includes(a.kind)) throw new HttpError(400, 'not_deletable');
  run('UPDATE scenes SET reference_asset_id = NULL WHERE reference_asset_id = ?', a.id);
  run('DELETE FROM assets WHERE id = ?', a.id);
  await storage.remove(a.storage_key);
  res.json({ ok: true });
});

/** Short-lived signed URL for providers that fetch reference images themselves. */
publicAssetsRouter.get('/assets/:id', (req, res) => {
  const { exp, sig } = req.query;
  if (!exp || !sig || Number(exp) < Date.now() || !safeEqual(sig, sign(`${req.params.id}.${exp}`))) throw new HttpError(403, 'forbidden');
  const a = get("SELECT * FROM assets WHERE id = ? AND kind = 'reference_image'", req.params.id);
  if (!a) throw new HttpError(404, 'not_found');
  send(res, a, false);
});
