import { spawn } from 'node:child_process';
import fsp from 'node:fs/promises';
import { config } from './config.js';
import { storage } from './storage.js';

function exec(bin, args, { timeoutMs = 10 * 60e3 } = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(bin, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    const timer = setTimeout(() => { p.kill('SIGKILL'); reject(new Error(`${bin} timed out`)); }, timeoutMs);
    p.stdout.on('data', (d) => (out += d));
    p.stderr.on('data', (d) => { err += d; if (err.length > 20000) err = err.slice(-10000); });
    p.on('error', (e) => { clearTimeout(timer); reject(e); });
    p.on('close', (code) => { clearTimeout(timer); code === 0 ? resolve(out) : reject(new Error(`${bin} exited ${code}: ${err.slice(-1500)}`)); });
  });
}

export async function ffmpegAvailable() {
  try { await exec('ffmpeg', ['-version'], { timeoutMs: 5000 }); return true; } catch { return false; }
}

export async function probe(file) {
  const out = await exec('ffprobe', ['-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', file], { timeoutMs: 30e3 });
  const j = JSON.parse(out);
  const v = (j.streams || []).find((s) => s.codec_type === 'video');
  const a = (j.streams || []).find((s) => s.codec_type === 'audio');
  const duration = Number(j.format?.duration) || Number(v?.duration) || Number(a?.duration) || null;
  return { duration, width: v?.width || null, height: v?.height || null, hasVideo: !!v, hasAudio: !!a, format: j.format?.format_name || '', videoCodec: v?.codec_name, audioCodec: a?.codec_name };
}

const even = (n) => Math.max(2, Math.round(n / 2) * 2);
const ASPECT = { '16:9': 16 / 9, '9:16': 9 / 16, '1:1': 1, '4:5': 4 / 5 };
export function frameSize(aspect, shortSide = 480) {
  const r = ASPECT[aspect] || 16 / 9;
  return r >= 1 ? { w: even(shortSide * r), h: even(shortSide) } : { w: even(shortSide), h: even(shortSide / r) };
}

/**
 * Demo-mode placeholder clip: an animated gradient card that states plainly that it is NOT an
 * AI-generated video. Used only by the demo provider.
 */
export async function renderDemoClip({ out, duration, aspect, lines }) {
  const { w, h } = frameSize(aspect, 480);
  const files = [];
  const textFile = async (t) => { const f = storage.tmpPath('txt'); await fsp.writeFile(f, t); files.push(f); return f.replace(/\\/g, '/').replace(/:/g, '\\:'); };
  const font = config.fontFile.replace(/\\/g, '/').replace(/:/g, '\\:');
  const fs1 = Math.round(Math.min(w, h) / 9), fs2 = Math.round(Math.min(w, h) / 22);
  const draw = [
    `drawtext=fontfile='${font}':textfile='${await textFile('DEMO')}':fontcolor=white@0.16:fontsize=${fs1 * 2.4}:x=(w-text_w)/2:y=(h-text_h)/2`,
    `drawbox=x=0:y=0:w=iw:h=${fs2 * 2.2}:color=0xE5484D@0.92:t=fill`,
    `drawtext=fontfile='${font}':textfile='${await textFile('DEMO MODE - NOT AN AI-GENERATED VIDEO')}':fontcolor=white:fontsize=${Math.round(fs2 * 0.9)}:x=(w-text_w)/2:y=${Math.round(fs2 * 0.6)}`,
  ];
  let y = h - fs2 * 1.6 * (lines.length + 0.6);
  for (const l of lines) {
    draw.push(`drawtext=fontfile='${font}':textfile='${await textFile(l)}':fontcolor=white@0.9:fontsize=${fs2}:x=${fs2}:y=${Math.round(y)}`);
    y += fs2 * 1.6;
  }
  draw.push(`drawtext=fontfile='${font}':text='%{pts\\:hms}':fontcolor=white@0.6:fontsize=${fs2}:x=w-text_w-${fs2}:y=h-${fs2 * 2}`);
  try {
    await exec('ffmpeg', ['-y', '-v', 'error',
      '-f', 'lavfi', '-i', `gradients=s=${w}x${h}:d=${duration}:r=24:c0=0x0B0F1A:c1=0x1B2A4A:c2=0x43226B:nb_colors=3:speed=0.015`,
      '-vf', draw.join(','), '-t', String(duration), '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  } finally { await Promise.all(files.map((f) => fsp.unlink(f).catch(() => {}))); }
}

/** Saves the last frame of a clip (used for frame-chaining continuity between scenes). */
export async function lastFrame(video, outPng) {
  await exec('ffmpeg', ['-y', '-v', 'error', '-sseof', '-0.15', '-i', video, '-frames:v', '1', '-update', '1', outPng]);
}

/**
 * Joins scene clips into the final film: each clip is trimmed to its scene duration, scaled/cropped to one
 * frame size and frame rate, concatenated, then mixed with optional audio tracks.
 * clips:  [{ path, duration, hasAudio, sourceDuration }]
 * tracks: [{ path, volume (0..1), offset (s), loop (bool) }]
 */
export async function assemble({ clips, tracks = [], out, width, height, fps = 30, clipAudioVolume = 1 }) {
  const args = ['-y', '-v', 'error'];
  const fc = [];
  const total = clips.reduce((s, c) => s + c.duration, 0);
  clips.forEach((c) => args.push('-i', c.path));
  tracks.forEach((t) => { if (t.loop) args.push('-stream_loop', '-1'); args.push('-i', t.path); });

  const useClipAudio = clipAudioVolume > 0 && clips.some((c) => c.hasAudio);
  const withAudio = useClipAudio || tracks.length > 0;
  clips.forEach((c, i) => {
    const d = c.duration.toFixed(3);
    fc.push(`[${i}:v]trim=0:${d},setpts=PTS-STARTPTS,scale=${width}:${height}:force_original_aspect_ratio=increase,crop=${width}:${height},fps=${fps},format=yuv420p,setsar=1,tpad=stop_mode=clone:stop_duration=${Math.max(0, c.duration - (c.sourceDuration ?? c.duration)).toFixed(3)}[v${i}]`);
    if (withAudio) {
      fc.push(useClipAudio && c.hasAudio
        ? `[${i}:a]atrim=0:${d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=${clipAudioVolume},apad=whole_dur=${d}[a${i}]`
        : `anullsrc=r=48000:cl=stereo,atrim=0:${d}[a${i}]`);
    }
  });
  fc.push(`${clips.map((_, i) => `[v${i}]${withAudio ? `[a${i}]` : ''}`).join('')}concat=n=${clips.length}:v=1:a=${withAudio ? 1 : 0}[vout]${withAudio ? '[abase]' : ''}`);
  if (withAudio) {
    const mix = ['[abase]'];
    tracks.forEach((t, k) => {
      const idx = clips.length + k, ms = Math.round((t.offset || 0) * 1000);
      fc.push(`[${idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume=${t.volume ?? 1}${ms ? `,adelay=${ms}:all=1` : ''},atrim=0:${total.toFixed(3)}[t${k}]`);
      mix.push(`[t${k}]`);
    });
    fc.push(mix.length > 1
      ? `${mix.join('')}amix=inputs=${mix.length}:normalize=0:duration=first,alimiter=limit=0.95[aout]`
      : `[abase]anull[aout]`);
  }
  args.push('-filter_complex', fc.join(';'), '-map', '[vout]');
  if (withAudio) args.push('-map', '[aout]', '-c:a', 'aac', '-b:a', '192k');
  args.push('-t', total.toFixed(3), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  await exec('ffmpeg', args, { timeoutMs: 30 * 60e3 });
  return { duration: total, hasAudio: withAudio };
}

/** Poster frame for library thumbnails. */
export async function poster(video, outJpg, at = 0.5) {
  await exec('ffmpeg', ['-y', '-v', 'error', '-ss', String(at), '-i', video, '-frames:v', '1', '-vf', 'scale=640:-2', '-q:v', '4', '-update', '1', outJpg]);
}
