import fsp from 'node:fs/promises';
import multer from 'multer';
import { config } from './config.js';
import { storage } from './storage.js';
import { HttpError } from './auth.js';
import { probe } from './ffmpeg.js';

/** File types accepted from users. Detection is by file signature, never by the name or the browser's MIME. */
const TYPES = [
  { ext: 'png', mime: 'image/png', kind: 'image', test: (b) => b.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) },
  { ext: 'jpg', mime: 'image/jpeg', kind: 'image', test: (b) => b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff },
  { ext: 'webp', mime: 'image/webp', kind: 'image', test: (b) => b.toString('latin1', 0, 4) === 'RIFF' && b.toString('latin1', 8, 12) === 'WEBP' },
  { ext: 'wav', mime: 'audio/wav', kind: 'audio', test: (b) => b.toString('latin1', 0, 4) === 'RIFF' && b.toString('latin1', 8, 12) === 'WAVE' },
  { ext: 'mp3', mime: 'audio/mpeg', kind: 'audio', test: (b) => b.toString('latin1', 0, 3) === 'ID3' || (b[0] === 0xff && (b[1] & 0xe0) === 0xe0 && (b[1] & 0x06) !== 0) },
  { ext: 'ogg', mime: 'audio/ogg', kind: 'audio', test: (b) => b.toString('latin1', 0, 4) === 'OggS' },
  { ext: 'm4a', mime: 'audio/mp4', kind: 'audio', test: (b) => b.toString('latin1', 4, 8) === 'ftyp' && /^M4A |^M4B /.test(b.toString('latin1', 8, 12)) },
  { ext: 'mov', mime: 'video/quicktime', kind: 'video', test: (b) => b.toString('latin1', 4, 8) === 'ftyp' && b.toString('latin1', 8, 12) === 'qt  ' },
  { ext: 'mp4', mime: 'video/mp4', kind: 'video', test: (b) => b.toString('latin1', 4, 8) === 'ftyp' },
  { ext: 'webm', mime: 'video/webm', kind: 'video', test: (b) => b[0] === 0x1a && b[1] === 0x45 && b[2] === 0xdf && b[3] === 0xa3 },
];
const MAX = { image: 20 * 1024 * 1024, audio: 50 * 1024 * 1024, video: config.maxUploadBytes };
export const uploadRules = {
  image: { ext: ['png', 'jpg', 'webp'], maxMb: 20 },
  audio: { ext: ['mp3', 'wav', 'm4a', 'ogg'], maxMb: 50 },
  video: { ext: ['mp4', 'mov', 'webm'], maxMb: Math.round(config.maxUploadBytes / 1048576) },
};

export const uploadMiddleware = multer({
  storage: multer.diskStorage({ destination: storage.tmpDir, filename: (_r, _f, cb) => cb(null, 'up-' + Date.now() + '-' + Math.random().toString(36).slice(2)) }),
  limits: { fileSize: config.maxUploadBytes, files: 1 },
}).single('file');

/** Validates an uploaded temp file. Returns { kind, ext, mime, meta } or throws (and removes the file). */
export async function inspectUpload(file, allowedKinds) {
  const fail = async (code, extra) => { await fsp.unlink(file.path).catch(() => {}); throw new HttpError(400, code, undefined, extra); };
  if (!file) throw new HttpError(400, 'no_file');
  const fh = await fsp.open(file.path, 'r');
  const head = Buffer.alloc(16);
  await fh.read(head, 0, 16, 0);
  await fh.close();
  const type = TYPES.find((t) => t.test(head));
  if (!type || !allowedKinds.includes(type.kind)) return fail('unsupported_file_type');
  if (file.size > MAX[type.kind]) return fail('file_too_large', { maxMb: MAX[type.kind] / 1048576 });
  let meta;
  try { meta = await probe(file.path); } catch { return fail('unreadable_file'); }
  if (type.kind === 'audio' && !meta.hasAudio) return fail('unreadable_file');
  if (type.kind !== 'audio' && !meta.hasVideo) return fail('unreadable_file');
  if (type.kind === 'video' && (meta.duration || 0) > 300) return fail('video_too_long', { maxSeconds: 300 });
  return { ...type, meta };
}
