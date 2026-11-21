import { get, getSetting } from './db.js';
import { config } from './config.js';
import { HttpError } from './auth.js';

export function limitsFor(user) {
  const global = getSetting('limits', {});
  let own = {}; try { own = user.limits_json ? JSON.parse(user.limits_json) : {}; } catch { /* ignore */ }
  return { ...config.defaultLimits, ...global, ...own };
}
export function usageFor(user) {
  const since = Date.now() - 864e5;
  return {
    secondsToday: get('SELECT COALESCE(SUM(seconds),0) AS s FROM usage WHERE user_id = ? AND is_demo = 0 AND created_at > ?', user.id, since).s,
    activeProjects: get("SELECT COUNT(*) AS n FROM projects WHERE user_id = ? AND status IN ('queued','generating','assembling')", user.id).n,
    storageMb: Math.round(get('SELECT COALESCE(SUM(size),0) AS s FROM assets WHERE user_id = ?', user.id).s / 1048576),
  };
}
/** Throws 429 when starting `seconds` of generation would exceed the user's limits. Admins are not limited. */
export function assertCanGenerate(user, { seconds, isDemo, alreadyActive = false }) {
  if (user.role === 'admin') return;
  const l = limitsFor(user), u = usageFor(user);
  if (!alreadyActive && u.activeProjects >= l.maxActiveProjects) throw new HttpError(429, 'limit_active_projects', undefined, { limit: l.maxActiveProjects });
  if (!isDemo && u.secondsToday + seconds > l.dailySeconds) throw new HttpError(429, 'limit_daily_seconds', undefined, { limit: l.dailySeconds, used: Math.round(u.secondsToday) });
  if (u.storageMb >= l.maxStorageMb) throw new HttpError(429, 'limit_storage', undefined, { limit: l.maxStorageMb });
}
export function assertStorage(user) {
  if (user.role === 'admin') return;
  const l = limitsFor(user), u = usageFor(user);
  if (u.storageMb >= l.maxStorageMb) throw new HttpError(429, 'limit_storage', undefined, { limit: l.maxStorageMb });
}
