import fs from 'node:fs';
import path from 'node:path';

/**
 * Model providers. One file per model family in engine/models/. Each exports a manifest: licence,
 * variants, what a variant can generate, and plan() which turns a platform request into the exact
 * job spec a worker runs. Adding a model = adding one file here plus one runner on the worker.
 */
const dir = path.join(import.meta.dirname, '..', 'models');
export const models = [];
for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.js') && !x.startsWith('_')).sort()) models.push((await import(path.join(dir, f))).default);
export const getModel = (id) => models.find((m) => m.id === id);
export const getVariant = (modelId, variantId) => getModel(modelId)?.variants.find((v) => v.id === variantId);

export { framesFor, maxSeconds, minSeconds } from './frames.js';

/** Licence gate. policy 'commercial' admits only models whose weights licence was read and allows paid hosted use. */
export function licenceAllows(model, policy = process.env.ENGINE_LICENSE_POLICY || 'commercial') {
  if (policy === 'any') return true;
  const accepted = (process.env.ENGINE_ACCEPTED_LICENCES || '').split(',').map((s) => s.trim()).filter(Boolean);
  if (model.license.commercial === 'yes') return true;
  if (model.license.commercial === 'conditions') return accepted.includes(model.id); // an owner has read and accepted the conditions
  return false;
}
