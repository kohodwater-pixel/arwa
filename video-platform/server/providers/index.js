import runway from './runway.js';
import luma from './luma.js';
import veo from './veo.js';
import kling from './kling.js';
import demo from './demo.js';
import selfhosted from './selfhosted.js';
import { get, run, now } from '../db.js';
import { encrypt, decrypt } from '../secrets.js';
import { config } from '../config.js';

/**
 * Provider registry. To add a provider: write an adapter with the same shape as the ones in this
 * folder (qualities(), submit(), poll(), optional cancel()/test()) and add it to this list.
 * Nothing else in the platform refers to a provider by name.
 */
export const providers = [selfhosted, runway, veo, luma, kling, demo];
export const getProvider = (id) => providers.find((p) => p.id === id);

function row(id) { return get('SELECT * FROM provider_settings WHERE provider_id = ?', id); }

/** Credentials: values saved from the admin panel (encrypted) override environment variables. */
export function getCredentials(p) {
  const stored = row(p.id)?.credentials_enc ? decrypt(row(p.id).credentials_enc) || {} : {};
  const creds = {};
  for (const f of p.credentialFields) {
    const v = stored[f.key] || (f.env && process.env[f.env]) || '';
    if (v) creds[f.key] = v;
  }
  return creds;
}
export const isConfigured = (p) => p.credentialFields.filter((f) => f.required).every((f) => !!getCredentials(p)[f.key]);
export const isEnabled = (p) => (row(p.id)?.enabled ?? 1) === 1;

export function saveProviderSettings(p, { enabled, credentials }) {
  const cur = row(p.id);
  let stored = cur?.credentials_enc ? decrypt(cur.credentials_enc) || {} : {};
  if (credentials) {
    for (const f of p.credentialFields) {
      if (!(f.key in credentials)) continue;
      const v = String(credentials[f.key] ?? '').trim();
      if (v) stored[f.key] = v.slice(0, 500); else delete stored[f.key];
    }
  }
  run(`INSERT INTO provider_settings (provider_id, enabled, credentials_enc, updated_at) VALUES (?,?,?,?)
       ON CONFLICT(provider_id) DO UPDATE SET enabled = excluded.enabled, credentials_enc = excluded.credentials_enc, updated_at = excluded.updated_at`,
    p.id, (enabled ?? (cur?.enabled ?? 1)) ? 1 : 0, Object.keys(stored).length ? encrypt(stored) : null, now());
  p.refresh?.(getCredentials(p));
}

/** Providers whose capabilities change at run time (the self-hosted engine) are re-read on a timer. */
export function startCapabilityRefresh(everyMs = 15000) {
  const tick = () => { for (const p of providers) if (p.refresh && isEnabled(p)) p.refresh(getCredentials(p)).catch(() => {}); };
  tick();
  setInterval(tick, everyMs).unref();
}

/** What a quality tier can really do on this server (image-to-video by URL needs a public base URL). */
function effective(q) {
  const i2v = q.imageToVideo === 'url' ? !!config.publicBaseUrl : !!q.imageToVideo;
  return { id: q.id, label: q.label, resolution: q.resolution, aspects: Object.keys(q.aspects), clip: q.clip, maxPromptChars: q.maxPromptChars, negativePrompt: !!q.negativePrompt, imageToVideo: i2v, imageByUrl: q.imageToVideo === 'url', nativeAudio: !!q.nativeAudio };
}
export const getQuality = (p, qualityId) => { const q = p.qualities().find((x) => x.id === qualityId); return q ? effective(q) : null; };

/** Safe description for the browser: never contains credential values. */
export function describeProvider(p, { admin = false } = {}) {
  const creds = admin ? getCredentials(p) : null;
  const stored = admin && row(p.id)?.credentials_enc ? decrypt(row(p.id).credentials_enc) || {} : {};
  return {
    id: p.id, label: p.label, demo: p.demo, verified: p.verified, docsUrl: p.docsUrl || null,
    enabled: isEnabled(p), configured: isConfigured(p) && (!p.refresh || p.qualities().length > 0),
    statusNote: p.status ? (isConfigured(p) ? p.status().error : null) : null, mockOnly: p.status ? p.status().mockOnly : false,
    qualities: p.qualities().map(effective),
    ...(admin ? {
      fields: p.credentialFields.map((f) => ({
        key: f.key, label: f.label, secret: f.secret, required: f.required, placeholder: f.placeholder || '',
        set: !!creds[f.key], source: stored[f.key] ? 'panel' : creds[f.key] ? 'env' : null,
        preview: creds[f.key] ? (f.secret ? '••••' + creds[f.key].slice(-4) : creds[f.key]) : '',
      })),
      canTest: typeof p.test === 'function',
    } : {}),
  };
}
/** Providers a user may pick: enabled and configured (the demo provider is always configured). */
export const usableProviders = () => providers.filter((p) => isEnabled(p) && isConfigured(p));
