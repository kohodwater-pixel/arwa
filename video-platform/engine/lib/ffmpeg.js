import { spawn } from 'node:child_process';
export function exec(bin, args, timeoutMs = 300000) {
  return new Promise((resolve, reject) => {
    const p = spawn(bin, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    const t = setTimeout(() => { p.kill('SIGKILL'); reject(new Error(`${bin} timed out`)); }, timeoutMs);
    p.stdout.on('data', (d) => (out += d)); p.stderr.on('data', (d) => { err += d; if (err.length > 400000) err = err.slice(-200000); });
    p.on('error', (e) => { clearTimeout(t); reject(e); });
    p.on('close', (code) => { clearTimeout(t); code === 0 ? resolve({ out, err }) : reject(new Error(`${bin} exited ${code}: ${err.slice(-600)}`)); });
  });
}
export async function probe(file) {
  const { out } = await exec('ffprobe', ['-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', file], 30000);
  const j = JSON.parse(out); const v = (j.streams || []).find((s) => s.codec_type === 'video'); const a = (j.streams || []).find((s) => s.codec_type === 'audio');
  const [n, d] = String(v?.avg_frame_rate || '0/1').split('/').map(Number);
  return { duration: Number(j.format?.duration) || null, width: v?.width || null, height: v?.height || null, fps: d ? n / d : null, frames: Number(v?.nb_frames) || null, hasVideo: !!v, hasAudio: !!a, codec: v?.codec_name || null };
}
/** Number of hard cuts inside a clip (a training clip should be one shot). */
export async function sceneCuts(file, threshold = 0.4) {
  const { err } = await exec('ffmpeg', ['-v', 'info', '-i', file, '-vf', `select='gt(scene,${threshold})',showinfo`, '-an', '-f', 'null', '-']);
  return (err.match(/pts_time:/g) || []).length;
}
/** Technical signals measurable without a GPU: frozen and black spans, frame-to-frame change, blur. */
export async function technical(file) {
  const { err } = await exec('ffmpeg', ['-v', 'info', '-i', file, '-vf', 'blackdetect=d=0.2:pix_th=0.10,signalstats,metadata=print:key=lavfi.signalstats.YDIF', '-an', '-f', 'null', '-']);
  const sum = (re) => [...err.matchAll(re)].reduce((n, m) => n + Number(m[1]), 0);
  const p = await probe(file);
  // YDIF = mean luma difference to the previous frame. A frame that barely differs from the one before it is "frozen".
  const ydif = [...err.matchAll(/lavfi\.signalstats\.YDIF=([\d.]+)/g)].map((m) => Number(m[1])).slice(1);
  const mean = ydif.length ? ydif.reduce((a, b) => a + b, 0) / ydif.length : 0;
  const sd = ydif.length ? Math.sqrt(ydif.reduce((a, b) => a + (b - mean) ** 2, 0) / ydif.length) : 0;
  const frozenSeconds = p.fps ? ydif.filter((v) => v < 0.02).length / p.fps : 0;
  let blur = null;
  try { const b = await exec('ffmpeg', ['-v', 'info', '-i', file, '-vf', 'blurdetect', '-an', '-f', 'null', '-']); const m = b.err.match(/blur mean:\s*([\d.]+)/); blur = m ? Number(m[1]) : null; } catch { /* filter missing in this ffmpeg build */ }
  return { frozenSeconds, blackSeconds: sum(/black_duration:\s*([\d.]+)/g), motionMean: mean, motionJitter: mean ? sd / mean : 0, blurMean: blur };
}
