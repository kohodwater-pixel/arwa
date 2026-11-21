import crypto from 'node:crypto';
import { promisify } from 'node:util';
import { config } from './config.js';
import { get, run, now, id, all } from './db.js';
import { sha256, randomToken } from './secrets.js';

const scrypt = promisify(crypto.scrypt);
const COOKIE = 'sid';

export async function hashPassword(pw) {
  const salt = crypto.randomBytes(16);
  const hash = await scrypt(pw, salt, 64, { N: 16384, r: 8, p: 1 });
  return `scrypt$${salt.toString('base64')}$${hash.toString('base64')}`;
}
export async function verifyPassword(pw, stored) {
  const [, s, h] = String(stored).split('$');
  if (!s || !h) return false;
  const expect = Buffer.from(h, 'base64');
  const got = await scrypt(pw, Buffer.from(s, 'base64'), expect.length, { N: 16384, r: 8, p: 1 });
  return crypto.timingSafeEqual(expect, got);
}

export class HttpError extends Error {
  constructor(status, code, message, extra) { super(message || code); this.status = status; this.code = code; this.extra = extra; }
}

export function validateCredentials({ email, password, name }, needName) {
  email = String(email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 200) throw new HttpError(400, 'invalid_email');
  if (typeof password !== 'string' || password.length < 8 || password.length > 200) throw new HttpError(400, 'weak_password');
  name = String(name || '').trim().slice(0, 80);
  if (needName && name.length < 2) throw new HttpError(400, 'invalid_name');
  return { email, password, name };
}

export function createSession(res, userId) {
  const token = randomToken();
  const exp = now() + config.sessionDays * 864e5;
  run('INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?,?,?,?)', sha256(token), userId, now(), exp);
  res.cookie(COOKIE, token, { httpOnly: true, sameSite: 'lax', secure: config.cookieSecure, expires: new Date(exp), path: '/' });
}
export function destroySession(req, res) {
  const t = req.cookies?.[COOKIE];
  if (t) run('DELETE FROM sessions WHERE token_hash = ?', sha256(t));
  res.clearCookie(COOKIE, { path: '/' });
}
export const destroyUserSessions = (userId) => run('DELETE FROM sessions WHERE user_id = ?', userId);

export function publicUser(u) {
  return u && { id: u.id, email: u.email, name: u.name, role: u.role, status: u.status, locale: u.locale, createdAt: u.created_at };
}

/** Attaches req.user when a valid session cookie is present. */
export function loadUser(req, _res, next) {
  const t = req.cookies?.[COOKIE];
  if (t) {
    const s = get('SELECT user_id, expires_at FROM sessions WHERE token_hash = ?', sha256(t));
    if (s && s.expires_at > now()) {
      const u = get('SELECT * FROM users WHERE id = ?', s.user_id);
      if (u && u.status === 'active') req.user = u;
    }
  }
  next();
}
export function requireAuth(req, _res, next) { req.user ? next() : next(new HttpError(401, 'unauthenticated')); }
export function requireAdmin(req, _res, next) {
  if (!req.user) return next(new HttpError(401, 'unauthenticated'));
  req.user.role === 'admin' ? next() : next(new HttpError(403, 'forbidden'));
}

/**
 * CSRF guard: every state-changing API call must carry a custom header. Browsers do not let
 * cross-site forms set it, and no CORS policy is exposed, so only our own front end can send it.
 */
export function csrfGuard(req, _res, next) {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) return next();
  req.get('x-requested-with') === 'studio' ? next() : next(new HttpError(403, 'csrf'));
}

/** Small in-memory rate limiter (per key, sliding window). */
export function rateLimit({ windowMs, max, key }) {
  const hits = new Map();
  setInterval(() => { const t = now(); for (const [k, v] of hits) if (v[v.length - 1] < t - windowMs) hits.delete(k); }, windowMs).unref();
  return (req, _res, next) => {
    const k = key(req), t = now();
    const arr = (hits.get(k) || []).filter((x) => x > t - windowMs);
    arr.push(t); hits.set(k, arr);
    arr.length > max ? next(new HttpError(429, 'rate_limited')) : next();
  };
}

export function createResetToken(userId) {
  const token = randomToken();
  run('INSERT INTO password_resets (token_hash, user_id, expires_at) VALUES (?,?,?)', sha256(token), userId, now() + 3600e3);
  return token;
}
export function consumeResetToken(token) {
  const r = get('SELECT * FROM password_resets WHERE token_hash = ?', sha256(String(token || '')));
  if (!r || r.used_at || r.expires_at < now()) return null;
  run('UPDATE password_resets SET used_at = ? WHERE token_hash = ?', now(), r.token_hash);
  return r.user_id;
}
export const newUserId = id;
export const countUsers = () => get('SELECT COUNT(*) AS n FROM users').n;
export const listAdmins = () => all("SELECT id FROM users WHERE role = 'admin' AND status = 'active'");
