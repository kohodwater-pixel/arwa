import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { config } from './config.js';

/**
 * Storage driver. The rest of the code only uses this interface, so an object store (S3, GCS, R2)
 * can replace the local disk by implementing the same five functions (localPath() would download
 * to a temp file, because ffmpeg needs a real path).
 */
const base = path.join(config.dataDir, 'storage');
const tmp = path.join(config.dataDir, 'tmp');
fs.mkdirSync(base, { recursive: true });
fs.mkdirSync(tmp, { recursive: true });

const resolve = (key) => {
  const p = path.resolve(base, key);
  if (!p.startsWith(base + path.sep)) throw new Error('bad storage key');
  return p;
};

export const storage = {
  newKey(userId, ext) {
    const name = crypto.randomBytes(16).toString('hex');
    return `${userId}/${name.slice(0, 2)}/${name}${ext ? '.' + ext.replace(/[^a-z0-9]/gi, '') : ''}`;
  },
  async putFile(key, srcPath) {
    const dest = resolve(key);
    await fsp.mkdir(path.dirname(dest), { recursive: true });
    await fsp.rename(srcPath, dest).catch(async () => { await fsp.copyFile(srcPath, dest); await fsp.unlink(srcPath); });
    return (await fsp.stat(dest)).size;
  },
  localPath: (key) => resolve(key),
  read: (key) => fsp.readFile(resolve(key)),
  async remove(key) { await fsp.unlink(resolve(key)).catch(() => {}); },
  tmpPath(ext = '') { return path.join(tmp, crypto.randomBytes(12).toString('hex') + (ext ? '.' + ext : '')); },
  tmpDir: tmp,
};
