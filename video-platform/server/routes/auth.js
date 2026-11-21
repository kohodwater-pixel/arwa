import { Router } from 'express';
import { get, run, now } from '../db.js';
import { config } from '../config.js';
import * as log from '../log.js';
import {
  HttpError, hashPassword, verifyPassword, validateCredentials, createSession, destroySession, destroyUserSessions,
  publicUser, requireAuth, rateLimit, createResetToken, consumeResetToken, newUserId, countUsers,
} from '../auth.js';
import { limitsFor, usageFor } from '../limits.js';
import { getSetting } from '../db.js';

export const authRouter = Router();
const limiter = rateLimit({ windowMs: 15 * 60e3, max: 20, key: (req) => `${req.ip}:${String(req.body?.email || '').toLowerCase()}` });
const me = (u) => ({ user: publicUser(u), limits: limitsFor(u), usage: usageFor(u) });

authRouter.post('/register', limiter, async (req, res) => {
  if (getSetting('registrationOpen', true) === false && countUsers() > 0) throw new HttpError(403, 'registration_closed');
  const { email, password, name } = validateCredentials(req.body || {}, true);
  if (get('SELECT 1 FROM users WHERE email = ?', email)) throw new HttpError(409, 'email_taken');
  const first = countUsers() === 0;
  const role = (config.adminEmail ? email === config.adminEmail : first) ? 'admin' : 'user';
  const userId = newUserId();
  const locale = req.body.locale === 'en' ? 'en' : 'ar';
  run('INSERT INTO users (id, email, name, password_hash, role, locale, created_at, last_login_at) VALUES (?,?,?,?,?,?,?,?)', userId, email, name, await hashPassword(password), role, locale, now(), now());
  createSession(res, userId);
  log.info('auth.register', `new ${role} account`, { userId });
  res.status(201).json(me(get('SELECT * FROM users WHERE id = ?', userId)));
});

authRouter.post('/login', limiter, async (req, res) => {
  const email = String(req.body?.email || '').trim().toLowerCase();
  const u = get('SELECT * FROM users WHERE email = ?', email);
  const ok = u && (await verifyPassword(String(req.body?.password || ''), u.password_hash));
  if (!ok) { log.warn('auth.login_failed', 'bad credentials', { ip: req.ip }); throw new HttpError(401, 'bad_credentials'); }
  if (u.status !== 'active') throw new HttpError(403, 'account_disabled');
  run('UPDATE users SET last_login_at = ? WHERE id = ?', now(), u.id);
  createSession(res, u.id);
  res.json(me(u));
});

authRouter.post('/logout', (req, res) => { destroySession(req, res); res.json({ ok: true }); });
authRouter.get('/me', (req, res) => { req.user ? res.json(me(req.user)) : res.status(401).json({ error: 'unauthenticated' }); });

/**
 * Password recovery. This server has no e-mail service wired in, so the reset link is written to the
 * operations log for an administrator to pass on; the response says so instead of pretending a
 * message was sent. The response is the same whether or not the address exists.
 */
authRouter.post('/forgot', limiter, (req, res) => {
  const email = String(req.body?.email || '').trim().toLowerCase();
  const u = get('SELECT * FROM users WHERE email = ?', email);
  if (u && u.status === 'active') {
    const token = createResetToken(u.id);
    log.info('auth.reset_requested', `reset link: ${config.publicBaseUrl || ''}/reset?token=${token}`, { userId: u.id });
  }
  res.json({ ok: true, delivery: 'admin' });
});

authRouter.post('/reset', limiter, async (req, res) => {
  const { password } = validateCredentials({ email: 'x@x.xx', password: req.body?.password });
  const userId = consumeResetToken(req.body?.token);
  if (!userId) throw new HttpError(400, 'invalid_reset_token');
  run('UPDATE users SET password_hash = ? WHERE id = ?', await hashPassword(password), userId);
  destroyUserSessions(userId);
  log.info('auth.password_reset', 'password changed with a reset link', { userId });
  res.json({ ok: true });
});

authRouter.patch('/profile', requireAuth, (req, res) => {
  const name = req.body?.name !== undefined ? String(req.body.name).trim().slice(0, 80) : req.user.name;
  if (name.length < 2) throw new HttpError(400, 'invalid_name');
  const locale = ['ar', 'en'].includes(req.body?.locale) ? req.body.locale : req.user.locale;
  run('UPDATE users SET name = ?, locale = ? WHERE id = ?', name, locale, req.user.id);
  res.json(me(get('SELECT * FROM users WHERE id = ?', req.user.id)));
});

authRouter.post('/password', requireAuth, limiter, async (req, res) => {
  if (!(await verifyPassword(String(req.body?.current || ''), req.user.password_hash))) throw new HttpError(400, 'bad_current_password');
  const { password } = validateCredentials({ email: 'x@x.xx', password: req.body?.next });
  run('UPDATE users SET password_hash = ? WHERE id = ?', await hashPassword(password), req.user.id);
  destroyUserSessions(req.user.id);
  createSession(res, req.user.id);
  res.json({ ok: true });
});
