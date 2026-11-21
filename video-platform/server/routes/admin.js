import { Router } from 'express';
import { all, get, run, update, now, getSetting, setSetting } from '../db.js';
import { config } from '../config.js';
import { HttpError, requireAdmin, publicUser, createResetToken, destroyUserSessions } from '../auth.js';
import { providers, getProvider, describeProvider, saveProviderSettings, getCredentials, isConfigured } from '../providers/index.js';
import { audioProviders } from '../audio/index.js';
import { limitsFor, usageFor } from '../limits.js';
import { maybeFinish } from '../pipeline.js';
import * as log from '../log.js';

export const adminRouter = Router();
adminRouter.use(requireAdmin);
const allProviders = () => [...providers, ...audioProviders];

adminRouter.get('/overview', (_req, res) => {
  const count = (sql, ...p) => get(sql, ...p).n;
  const day = now() - 864e5;
  res.json({
    users: count('SELECT COUNT(*) AS n FROM users'),
    projects: count('SELECT COUNT(*) AS n FROM projects'),
    completed: count("SELECT COUNT(*) AS n FROM projects WHERE status = 'completed'"),
    activeJobs: count("SELECT COUNT(*) AS n FROM jobs WHERE status IN ('queued','running')"),
    failedJobs24h: count("SELECT COUNT(*) AS n FROM jobs WHERE status = 'failed' AND updated_at > ?", day),
    secondsToday: Math.round(get('SELECT COALESCE(SUM(seconds),0) AS n FROM usage WHERE is_demo = 0 AND created_at > ?', day).n),
    demoSecondsToday: Math.round(get('SELECT COALESCE(SUM(seconds),0) AS n FROM usage WHERE is_demo = 1 AND created_at > ?', day).n),
    storageMb: Math.round(get('SELECT COALESCE(SUM(size),0) AS n FROM assets').n / 1048576),
    providers: providers.map((p) => ({ id: p.id, label: p.label, demo: p.demo, configured: isConfigured(p) })),
  });
});

adminRouter.get('/users', (_req, res) => {
  const users = all('SELECT * FROM users ORDER BY created_at DESC LIMIT 500');
  res.json({ users: users.map((u) => ({ ...publicUser(u), lastLoginAt: u.last_login_at, limits: limitsFor(u), customLimits: !!u.limits_json, usage: usageFor(u),
    projects: get('SELECT COUNT(*) AS n FROM projects WHERE user_id = ?', u.id).n })) });
});

adminRouter.patch('/users/:id', (req, res) => {
  const u = get('SELECT * FROM users WHERE id = ?', req.params.id);
  if (!u) throw new HttpError(404, 'not_found');
  const f = {};
  if (['admin', 'user'].includes(req.body?.role)) f.role = req.body.role;
  if (['active', 'disabled'].includes(req.body?.status)) f.status = req.body.status;
  if (u.id === req.user.id && (f.role === 'user' || f.status === 'disabled')) throw new HttpError(400, 'cannot_demote_self');
  if (req.body?.limits === null) f.limits_json = null;
  else if (req.body?.limits) {
    const l = {};
    for (const k of ['dailySeconds', 'maxActiveProjects', 'maxStorageMb']) { const v = Number(req.body.limits[k]); if (Number.isFinite(v) && v >= 0) l[k] = Math.round(v); }
    f.limits_json = JSON.stringify(l);
  }
  update('users', u.id, f);
  if (f.status === 'disabled') destroyUserSessions(u.id);
  log.info('admin.user_updated', JSON.stringify({ role: f.role, status: f.status, limits: f.limits_json }), { userId: req.user.id, target: u.id });
  res.json({ ok: true });
});

/** One-time password reset link the administrator hands to the user (no e-mail service is configured). */
adminRouter.post('/users/:id/reset-link', (req, res) => {
  const u = get('SELECT * FROM users WHERE id = ?', req.params.id);
  if (!u) throw new HttpError(404, 'not_found');
  log.info('admin.reset_link', 'reset link issued by admin', { userId: req.user.id, target: u.id });
  res.json({ path: `/reset?token=${createResetToken(u.id)}`, expiresInMinutes: 60 });
});

adminRouter.get('/jobs', (req, res) => {
  const status = String(req.query.status || '');
  const where = ['queued', 'running', 'succeeded', 'failed', 'canceled'].includes(status) ? 'WHERE j.status = ?' : status === 'active' ? "WHERE j.status IN ('queued','running')" : '';
  const rows = all(`SELECT j.*, p.title AS project_title, u.email AS user_email, s.position AS scene_position
    FROM jobs j LEFT JOIN projects p ON p.id = j.project_id LEFT JOIN users u ON u.id = j.user_id LEFT JOIN scenes s ON s.id = j.scene_id
    ${where} ORDER BY j.updated_at DESC LIMIT 200`, ...(where.includes('?') ? [status] : []));
  res.json({ jobs: rows.map((j) => ({ id: j.id, type: j.type, status: j.status, attempts: j.attempts, maxAttempts: j.max_attempts, providerId: j.provider_id, providerJobId: j.provider_job_id,
    progress: j.progress, error: j.error, projectId: j.project_id, projectTitle: j.project_title, userEmail: j.user_email, scene: j.scene_position != null ? j.scene_position + 1 : null,
    createdAt: j.created_at, updatedAt: j.updated_at, finishedAt: j.finished_at })) });
});

adminRouter.post('/jobs/:id/retry', (req, res) => {
  const j = get('SELECT * FROM jobs WHERE id = ?', req.params.id);
  if (!j) throw new HttpError(404, 'not_found');
  if (!['failed', 'canceled'].includes(j.status)) throw new HttpError(400, 'job_not_retryable');
  update('jobs', j.id, { status: 'queued', attempts: 0, provider_job_id: null, error: null, run_at: now(), finished_at: null, updated_at: now() });
  if (j.scene_id) update('scenes', j.scene_id, { status: 'queued', error: null, progress: 0 });
  update('projects', j.project_id, { status: j.type === 'assemble' ? 'assembling' : 'generating', error: null, updated_at: now() });
  log.info('admin.job_retry', 'job re-queued by admin', { userId: req.user.id, jobId: j.id, projectId: j.project_id });
  res.json({ ok: true });
});

adminRouter.post('/jobs/:id/cancel', async (req, res) => {
  const j = get('SELECT * FROM jobs WHERE id = ?', req.params.id);
  if (!j) throw new HttpError(404, 'not_found');
  if (!['queued', 'running'].includes(j.status)) throw new HttpError(400, 'job_not_active');
  update('jobs', j.id, { status: 'canceled', finished_at: now(), updated_at: now() });
  const p = getProvider(j.provider_id);
  if (j.provider_job_id && p?.cancel) await p.cancel(j.provider_job_id, getCredentials(p)).catch(() => {});
  if (j.scene_id) update('scenes', j.scene_id, { status: 'failed', error: 'canceled: canceled by an administrator' });
  if (j.type === 'assemble') update('projects', j.project_id, { status: 'failed', error: 'assembly: canceled by an administrator', updated_at: now() });
  else maybeFinish(j.project_id);
  res.json({ ok: true });
});

adminRouter.get('/providers', (_req, res) => {
  res.json({
    video: providers.map((p) => describeProvider(p, { admin: true })),
    audio: audioProviders.map((p) => describeProvider(p, { admin: true })),
    publicBaseUrl: config.publicBaseUrl || null,
    aiDirector: { configured: !!config.anthropicKey, model: config.directorModel },
  });
});

adminRouter.put('/providers/:id', (req, res) => {
  const p = allProviders().find((x) => x.id === req.params.id);
  if (!p) throw new HttpError(404, 'not_found');
  saveProviderSettings(p, { enabled: typeof req.body?.enabled === 'boolean' ? req.body.enabled : undefined, credentials: req.body?.credentials });
  log.info('admin.provider_updated', `${p.id} settings changed`, { userId: req.user.id, fields: Object.keys(req.body?.credentials || {}) });
  res.json({ provider: describeProvider(p, { admin: true }) });
});

/** Real authenticated call to the provider — the only way a connection is ever reported as working. */
adminRouter.post('/providers/:id/test', async (req, res) => {
  const p = allProviders().find((x) => x.id === req.params.id);
  if (!p) throw new HttpError(404, 'not_found');
  if (!p.test) return res.json({ ok: false, error: 'no_test_available' });
  if (!isConfigured(p)) return res.json({ ok: false, error: 'not_configured' });
  try { await p.test(getCredentials(p)); log.info('admin.provider_test', `${p.id}: connection ok`, { userId: req.user.id }); res.json({ ok: true }); }
  catch (e) { log.warn('admin.provider_test', `${p.id}: ${e.message}`, { userId: req.user.id }); res.json({ ok: false, error: e.code || 'provider_error', detail: String(e.message).slice(0, 300) }); }
});

adminRouter.get('/logs', (req, res) => {
  const where = [], params = [];
  if (['info', 'warn', 'error'].includes(req.query.level)) { where.push('level = ?'); params.push(req.query.level); }
  if (req.query.q) { where.push('(event LIKE ? OR message LIKE ?)'); const q = `%${String(req.query.q).slice(0, 80)}%`; params.push(q, q); }
  if (req.query.projectId) { where.push('project_id = ?'); params.push(String(req.query.projectId)); }
  const rows = all(`SELECT * FROM logs ${where.length ? 'WHERE ' + where.join(' AND ') : ''} ORDER BY id DESC LIMIT 300`, ...params);
  res.json({ logs: rows.map((l) => ({ id: l.id, ts: l.ts, level: l.level, event: l.event, message: l.message, userId: l.user_id, projectId: l.project_id, jobId: l.job_id, data: l.data_json })) });
});

adminRouter.get('/settings', (_req, res) => res.json({ limits: { ...config.defaultLimits, ...getSetting('limits', {}) }, registrationOpen: getSetting('registrationOpen', true) }));
adminRouter.put('/settings', (req, res) => {
  if (req.body?.limits) {
    const l = {};
    for (const k of ['dailySeconds', 'maxActiveProjects', 'maxStorageMb']) { const v = Number(req.body.limits[k]); if (Number.isFinite(v) && v >= 0) l[k] = Math.round(v); }
    setSetting('limits', l);
  }
  if (typeof req.body?.registrationOpen === 'boolean') setSetting('registrationOpen', req.body.registrationOpen);
  log.info('admin.settings_updated', 'global settings changed', { userId: req.user.id });
  res.json({ ok: true });
});
