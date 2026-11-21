import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

// Minimal .env loader (no dependency). Real environment variables win.
const envFile = path.join(root, '.env');
if (fs.existsSync(envFile)) {
  for (const line of fs.readFileSync(envFile, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

const env = process.env;
const dataDir = path.resolve(root, env.DATA_DIR || './data');
fs.mkdirSync(dataDir, { recursive: true });

const isProd = env.NODE_ENV === 'production';
let appSecret = env.APP_SECRET;
if (!appSecret) {
  if (isProd) throw new Error('APP_SECRET is required in production');
  const f = path.join(dataDir, '.dev-secret');
  if (!fs.existsSync(f)) fs.writeFileSync(f, crypto.randomBytes(32).toString('hex'), { mode: 0o600 });
  appSecret = fs.readFileSync(f, 'utf8').trim();
}

const num = (v, d) => (Number.isFinite(Number(v)) && v !== '' && v != null ? Number(v) : d);

export const config = {
  root,
  dataDir,
  isProd,
  port: num(env.PORT, 4000),
  appName: env.APP_NAME || 'Mashhad Studio',
  appSecret,
  publicBaseUrl: (env.PUBLIC_BASE_URL || '').replace(/\/$/, ''),
  cookieSecure: env.COOKIE_SECURE === 'true',
  adminEmail: (env.ADMIN_EMAIL || '').toLowerCase(),
  maxUploadBytes: num(env.MAX_UPLOAD_MB, 200) * 1024 * 1024,
  maxProjectSeconds: num(env.MAX_PROJECT_SECONDS, 120),
  queueConcurrency: num(env.QUEUE_CONCURRENCY, 4),
  queueTickMs: num(env.QUEUE_TICK_MS, 1000),
  pollIntervalMs: num(env.PROVIDER_POLL_MS, 5000),
  sessionDays: 30,
  directorModel: env.DIRECTOR_MODEL || 'claude-opus-5-5',
  anthropicKey: env.ANTHROPIC_API_KEY || '',
  anthropicBaseUrl: env.DIRECTOR_API_BASE_URL || 'https://api.anthropic.com',
  fontFile: path.join(root, 'public/fonts/Inter-Variable.ttf'),
  // Default per-user limits; admins can override globally or per user.
  defaultLimits: { dailySeconds: 300, maxActiveProjects: 3, maxStorageMb: 5000 },
};
