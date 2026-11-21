import { run, now } from './db.js';

/** Operation + error log: written to stdout (JSON lines) and to the logs table (admin panel). */
export function log(level, event, message, ctx = {}) {
  const { userId = null, projectId = null, jobId = null, ...data } = ctx;
  const line = { ts: new Date().toISOString(), level, event, message, userId, projectId, jobId, ...data };
  if (process.env.NODE_ENV !== 'test') (level === 'error' ? console.error : console.log)(JSON.stringify(line));
  try {
    run('INSERT INTO logs (ts, level, event, user_id, project_id, job_id, message, data_json) VALUES (?,?,?,?,?,?,?,?)',
      now(), level, event, userId, projectId, jobId, String(message ?? '').slice(0, 2000), Object.keys(data).length ? JSON.stringify(data).slice(0, 4000) : null);
  } catch { /* logging must never break the request */ }
}
export const info = (event, message, ctx) => log('info', event, message, ctx);
export const warn = (event, message, ctx) => log('warn', event, message, ctx);
export const error = (event, message, ctx) => log('error', event, message, ctx);
