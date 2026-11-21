import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { all, get, run, now, id, parse, sha256File } from './db.js';
import { probe, sceneCuts } from './ffmpeg.js';
import { SPECIALTIES } from './router.js';

/**
 * Dataset management for LoRA training.
 * Rules the code enforces:
 *  - a clip enters only with a rights record (where it came from, who owns it, under what licence);
 *  - every clip is measured (size, length, frame rate, hard cuts) and starts as "pending";
 *  - a person approves or rejects each clip; only approved, captioned clips are exported;
 *  - an export is tied to a snapshot hash of exactly which clips and captions went in, and that hash
 *    is what a LoRA version records, so a trained file can always be traced to its data.
 */
const VIDEO = ['.mp4', '.mov', '.mkv', '.webm'], IMAGE = ['.png', '.jpg', '.jpeg', '.webp'];
const fail = (m) => { throw new Error(m); };
const ds = (slug) => get('SELECT * FROM datasets WHERE slug = ?', slug) || fail(`dataset "${slug}" not found`);

export function create({ slug, name, specialty, target = {} }) {
  if (!/^[a-z0-9][a-z0-9-]{2,60}$/.test(slug || '')) fail('slug: lowercase letters, digits and hyphens');
  if (!SPECIALTIES.includes(specialty)) fail(`specialty must be one of ${SPECIALTIES.join(', ')}`);
  const t = { width: 1280, height: 720, fps: 16, frames: 81, minSeconds: 3, maxSeconds: 12, ...target };
  run('INSERT INTO datasets (id, slug, name, specialty, target_json, created_at) VALUES (?,?,?,?,?,?)', id('ds'), slug, name || slug, specialty, JSON.stringify(t), now());
  return summary(slug);
}

export async function ingest(slug, dir, rights) {
  const d = ds(slug), t = parse(d.target_json, {});
  for (const k of ['source', 'holder', 'license']) if (!rights?.[k]) fail(`rights.${k} is required: clips without a rights record are not accepted`);
  const files = fs.readdirSync(dir).filter((f) => [...VIDEO, ...IMAGE].includes(path.extname(f).toLowerCase())).sort();
  const report = { added: 0, duplicate: 0, unreadable: 0, flagged: 0 };
  for (const f of files) {
    const file = path.resolve(dir, f), kind = VIDEO.includes(path.extname(f).toLowerCase()) ? 'video' : 'image';
    const sha = await sha256File(file);
    if (get('SELECT 1 FROM dataset_items WHERE dataset_id = ? AND sha256 = ?', d.id, sha)) { report.duplicate++; continue; }
    let p; try { p = await probe(file); } catch { report.unreadable++; continue; }
    if (!p.hasVideo) { report.unreadable++; continue; }
    const cuts = kind === 'video' ? await sceneCuts(file) : 0;
    const short = Math.min(p.width, p.height), need = Math.min(t.width, t.height);
    const checks = {
      resolution: { pass: short >= need, value: `${p.width}x${p.height}`, need: `short side >= ${need}` },
      ...(kind === 'video' ? {
        duration: { pass: p.duration >= t.minSeconds && p.duration <= t.maxSeconds, value: p.duration, need: `${t.minSeconds}-${t.maxSeconds} s (split longer clips)` },
        frameRate: { pass: (p.fps || 0) >= t.fps - 0.5, value: p.fps, need: `>= ${t.fps} fps` },
        singleShot: { pass: cuts === 0, value: cuts, need: 'no hard cuts inside a clip' },
        enoughFrames: { pass: (p.duration || 0) * t.fps >= t.frames, value: Math.floor((p.duration || 0) * t.fps), need: `>= ${t.frames} frames at ${t.fps} fps` },
      } : {}),
    };
    const ok = Object.values(checks).every((c) => c.pass);
    if (!ok) report.flagged++;
    const cap = file.replace(/\.[^.]+$/, '.txt');
    run(`INSERT INTO dataset_items (id, dataset_id, file, sha256, kind, duration, width, height, fps, has_audio, scene_cuts, checks_json, caption, caption_source, split,
          rights_source, rights_holder, rights_license, rights_people_consent, rights_doc, added_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`,
      id('di'), d.id, file, sha, kind, p.duration, p.width, p.height, p.fps, p.hasAudio ? 1 : 0, cuts, JSON.stringify({ ok, ...checks }),
      fs.existsSync(cap) ? fs.readFileSync(cap, 'utf8').trim() : null, fs.existsSync(cap) ? 'file' : null, parseInt(sha.slice(0, 4), 16) % 10 === 0 ? 'val' : 'train',
      rights.source, rights.holder, rights.license, rights.peopleConsent || null, rights.doc || null, now());
    report.added++;
  }
  return { ...report, dataset: summary(slug) };
}

export function items(slug, status) {
  const d = ds(slug);
  return all(`SELECT * FROM dataset_items WHERE dataset_id = ? ${status ? 'AND status = ?' : ''} ORDER BY file`, ...[d.id, status].filter(Boolean))
    .map((i) => ({ id: i.id, file: path.basename(i.file), kind: i.kind, status: i.status, split: i.split, seconds: i.duration, size: `${i.width}x${i.height}`, fps: i.fps, cuts: i.scene_cuts, checksOk: parse(i.checks_json, {}).ok, caption: i.caption, reject: i.reject_reason }));
}
export function review(slug, itemId, { status, reason, caption }) {
  const d = ds(slug), i = get('SELECT * FROM dataset_items WHERE id = ? AND dataset_id = ?', itemId, d.id) || fail('item not found');
  if (caption !== undefined) run("UPDATE dataset_items SET caption = ?, caption_source = 'review' WHERE id = ?", String(caption).trim(), i.id);
  if (status) {
    if (!['approved', 'rejected', 'pending'].includes(status)) fail('status: approved | rejected | pending');
    if (status === 'rejected' && !reason) fail('a rejection needs a reason');
    if (status === 'approved' && !parse(i.checks_json, {}).ok && reason !== 'override') fail('this clip failed automatic checks; pass reason "override" to approve it anyway');
    run('UPDATE dataset_items SET status = ?, reject_reason = ? WHERE id = ?', status, status === 'rejected' ? reason : null, i.id);
  }
  return items(slug).find((x) => x.id === i.id);
}

export function snapshot(slug) {
  const d = ds(slug);
  const rows = all("SELECT sha256, caption FROM dataset_items WHERE dataset_id = ? AND status = 'approved' ORDER BY sha256", d.id);
  return { hash: crypto.createHash('sha256').update(JSON.stringify(rows)).digest('hex').slice(0, 16), items: rows.length };
}
export function summary(slug) {
  const d = ds(slug);
  const c = Object.fromEntries(all('SELECT status, COUNT(*) n FROM dataset_items WHERE dataset_id = ? GROUP BY status', d.id).map((r) => [r.status, r.n]));
  const sec = get("SELECT COALESCE(SUM(duration),0) s FROM dataset_items WHERE dataset_id = ? AND status = 'approved'", d.id).s;
  return { slug: d.slug, name: d.name, specialty: d.specialty, target: parse(d.target_json, {}), counts: { pending: 0, approved: 0, rejected: 0, ...c }, approvedSeconds: Math.round(sec), snapshot: snapshot(slug) };
}

/**
 * Writes a training folder: links to the approved clips, one caption .txt per clip, and the dataset config
 * in the trainer's own format. Formats follow the trainers' documentation (musubi-tuner docs/dataset_config.md,
 * diffusion-pipe examples/dataset.toml) as read on 2026-11-21; they have not been run through the trainers here.
 */
export function exportFor(slug, trainer, outDir) {
  const d = ds(slug), t = parse(d.target_json, {});
  const rows = all("SELECT * FROM dataset_items WHERE dataset_id = ? AND status = 'approved' ORDER BY file", d.id);
  if (!rows.length) fail('no approved clips');
  const missing = rows.filter((r) => !r.caption);
  if (missing.length) fail(`${missing.length} approved clip(s) have no caption`);
  const snap = snapshot(slug);
  const root = path.resolve(outDir, `${slug}-${snap.hash}`);
  for (const split of ['train', 'val']) fs.mkdirSync(path.join(root, split), { recursive: true });
  for (const r of rows) {
    const base = `${r.sha256.slice(0, 12)}${path.extname(r.file).toLowerCase()}`;
    const dest = path.join(root, r.split, base);
    if (!fs.existsSync(dest)) fs.symlinkSync(r.file, dest);
    fs.writeFileSync(dest.replace(/\.[^.]+$/, '.txt'), r.caption + '\n');
  }
  let config;
  if (trainer === 'musubi-tuner') {
    config = `# musubi-tuner dataset config — dataset ${slug}, snapshot ${snap.hash}\n[general]\nresolution = [${t.width}, ${t.height}]\ncaption_extension = ".txt"\nbatch_size = 1\nenable_bucket = true\nbucket_no_upscale = true\n\n[[datasets]]\nvideo_directory = "${path.join(root, 'train')}"\ncache_directory = "${path.join(root, 'cache-train')}"\ntarget_frames = [${t.frames}]\nframe_extraction = "head"\nsource_fps = ${Number(t.fps).toFixed(1)}\nnum_repeats = 1\n`;
  } else if (trainer === 'diffusion-pipe') {
    config = `# diffusion-pipe dataset config — dataset ${slug}, snapshot ${snap.hash}\nresolutions = [${Math.min(t.width, t.height)}]\nenable_ar_bucket = true\nmin_ar = 0.5\nmax_ar = 2.0\nnum_ar_buckets = 7\nframe_buckets = [1, ${t.frames}]\n\n[[directory]]\npath = "${path.join(root, 'train')}"\nnum_repeats = 1\n`;
  } else fail('trainer: musubi-tuner | diffusion-pipe');
  fs.writeFileSync(path.join(root, 'dataset.toml'), config);
  fs.writeFileSync(path.join(root, 'MANIFEST.json'), JSON.stringify({ dataset: slug, specialty: d.specialty, snapshot: snap.hash, trainer, target: t, exportedAt: new Date().toISOString(),
    items: rows.map((r) => ({ sha256: r.sha256, split: r.split, seconds: r.duration, caption: r.caption, rights: { source: r.rights_source, holder: r.rights_holder, license: r.rights_license, peopleConsent: r.rights_people_consent, doc: r.rights_doc } })) }, null, 1));
  return { root, snapshot: snap.hash, train: rows.filter((r) => r.split === 'train').length, val: rows.filter((r) => r.split === 'val').length, config: path.join(root, 'dataset.toml') };
}
