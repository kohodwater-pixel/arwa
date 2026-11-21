import { request } from '../providers/http.js';

/**
 * ElevenLabs audio adapter (voice-over, sound effects, music).
 * Source: official SDK elevenlabs/elevenlabs-js v2.79.0, read 2026-11-21:
 *   POST /v1/text-to-speech/{voice_id}, POST /v1/sound-generation, POST /v1/music, GET /v1/voices
 * Assumption: eleven_multilingual_v2 is used for Arabic and English (language is detected from the text;
 * that model does not accept language_code). Music availability depends on the ElevenLabs plan.
 * Not exercised against the live API in this build.
 */
const BASE = 'https://api.elevenlabs.io';
const headers = (c) => ({ 'xi-api-key': c.apiKey });
const audio = async (path, creds, json) => {
  const res = await request(`${BASE}${path}?output_format=mp3_44100_128`, { method: 'POST', headers: headers(creds), json, raw: true, timeoutMs: 180_000 });
  return Buffer.from(await res.arrayBuffer());
};

export default {
  id: 'elevenlabs', label: 'ElevenLabs',
  credentialFields: [{ key: 'apiKey', label: 'API key', env: 'ELEVENLABS_API_KEY', secret: true, required: true }],
  capabilities: { voiceover: true, sfx: true, ambience: true, music: true },
  qualities: () => [],
  voiceover: ({ text, voiceId }, creds) => audio(`/v1/text-to-speech/${encodeURIComponent(voiceId)}`, creds, { text, model_id: 'eleven_multilingual_v2' }),
  effect: ({ prompt, seconds, loop }, creds) => audio('/v1/sound-generation', creds, { text: prompt, duration_seconds: Math.min(30, Math.max(0.5, seconds)), loop: !!loop }),
  music: ({ prompt, seconds }, creds) => audio('/v1/music', creds, { prompt, music_length_ms: Math.min(600000, Math.max(3000, Math.round(seconds * 1000))), force_instrumental: true }),
  async voices(creds) {
    const r = await request(`${BASE}/v1/voices`, { headers: headers(creds), timeoutMs: 20000 });
    return (r.voices || []).map((v) => ({ id: v.voice_id, name: v.name, labels: v.labels || {}, previewUrl: v.preview_url || null }));
  },
  test: (creds) => request(`${BASE}/v1/voices`, { headers: headers(creds), timeoutMs: 15000 }),
};
