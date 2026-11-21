import elevenlabs from './elevenlabs.js';
import { getCredentials, isConfigured, isEnabled } from '../providers/index.js';

/** Audio provider registry (same idea as the video registry; one adapter today). */
export const audioProviders = [elevenlabs];
export const getAudioProvider = () => audioProviders.find((p) => isEnabled(p) && isConfigured(p)) || null;
export const audioCreds = (p) => getCredentials(p);
export const TRACKS = ['music', 'voiceover', 'sfx', 'ambience'];

export function defaultAudio() {
  const t = () => ({ mode: 'none', assetId: null, prompt: '', volume: 0.8 });
  return { music: { ...t(), volume: 0.5 }, voiceover: { ...t(), volume: 1, language: 'ar', dialect: '', voiceId: '' }, sfx: { ...t(), volume: 0.7 }, ambience: { ...t(), volume: 0.4 }, clipAudioVolume: 1 };
}

/** Validates and normalises the audio settings sent by the browser. */
export function sanitizeAudio(input, base = defaultAudio()) {
  const out = structuredClone(base);
  const vol = (v, d) => (Number.isFinite(Number(v)) ? Math.min(1, Math.max(0, Number(v))) : d);
  for (const k of TRACKS) {
    const src = input?.[k]; if (!src) continue;
    if (['none', 'upload', 'generate'].includes(src.mode)) out[k].mode = src.mode;
    if (src.assetId === null || typeof src.assetId === 'string') out[k].assetId = src.assetId;
    if (typeof src.prompt === 'string') out[k].prompt = src.prompt.slice(0, 2000);
    out[k].volume = vol(src.volume, out[k].volume);
  }
  const vo = input?.voiceover || {};
  if (['ar', 'en'].includes(vo.language)) out.voiceover.language = vo.language;
  if (typeof vo.dialect === 'string') out.voiceover.dialect = vo.dialect.slice(0, 60);
  if (typeof vo.voiceId === 'string') out.voiceover.voiceId = vo.voiceId.slice(0, 80);
  out.clipAudioVolume = vol(input?.clipAudioVolume, out.clipAudioVolume);
  return out;
}

/** Audio direction appended to prompts of models that generate their own sound (e.g. Veo 3). */
export function audioDirection(a) {
  if (!a) return '';
  const parts = [];
  if (a.music.mode !== 'none' && a.music.prompt) parts.push(`music: ${a.music.prompt}`);
  if (a.sfx.prompt) parts.push(`sound effects: ${a.sfx.prompt}`);
  if (a.ambience.prompt) parts.push(`ambience: ${a.ambience.prompt}`);
  return parts.length ? ` Audio: ${parts.join('; ')}. No spoken dialogue.` : '';
}
