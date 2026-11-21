import crypto from 'node:crypto';
import { config } from './config.js';

const key = crypto.createHash('sha256').update('enc:' + config.appSecret).digest();

/** AES-256-GCM encryption for provider credentials stored in the database. */
export function encrypt(obj) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv('aes-256-gcm', key, iv);
  const data = Buffer.concat([c.update(JSON.stringify(obj), 'utf8'), c.final()]);
  return [iv, c.getAuthTag(), data].map((b) => b.toString('base64')).join('.');
}
export function decrypt(text) {
  try {
    const [iv, tag, data] = text.split('.').map((s) => Buffer.from(s, 'base64'));
    const d = crypto.createDecipheriv('aes-256-gcm', key, iv);
    d.setAuthTag(tag);
    return JSON.parse(Buffer.concat([d.update(data), d.final()]).toString('utf8'));
  } catch { return null; }
}
export const sign = (text) => crypto.createHmac('sha256', config.appSecret).update(text).digest('base64url');
export const safeEqual = (a, b) => {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
};
export const sha256 = (t) => crypto.createHash('sha256').update(t).digest('hex');
export const randomToken = (n = 32) => crypto.randomBytes(n).toString('base64url');
