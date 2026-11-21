import { useEffect, useRef, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDuration, fmtDate, fmtSize } from '../lib/i18n';
import { fileUrl, inLibrary } from '../lib/rpc';
import { Btn, Slate, Empty, cx, Note } from '../lib/ui';
import { useTimeline } from '../lib/timeline';
import { sceneVideo } from '../lib/project';

export default function Preview() {
  const st = useStudio();
  const p = st.project;
  const { tl, sceneOf, clipLen, starts, total } = useTimeline();
  const root = st.status.library_root;
  const exports = (p.exports || []).filter((e: any) => e.status === 'completed');
  const [mode, setMode] = useState<'cut' | 'export'>(exports.length ? 'export' : 'cut');
  const [idx, setIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [pos, setPos] = useState(0);
  const v = useRef<HTMLVideoElement>(null);
  const clips = tl?.clips || [];
  const clip = clips[idx];
  const scene = clip && sceneOf(clip.scene_id);
  useEffect(() => { const el = v.current; if (!el || mode !== 'cut' || !clip) return; const start = () => { el.currentTime = clip.trim_in || 0; if (playing) el.play().catch(() => {}); }; if (el.readyState >= 1) start(); else el.addEventListener('loadedmetadata', start, { once: true }); }, [idx, mode, scene?.video_path]); // eslint-disable-line react-hooks/exhaustive-deps
  if (!tl) return <Slate title={L('المعاينة', 'Video Preview')}><p className="text-mute">…</p></Slate>;
  if (!clips.length && !exports.length) return <Slate title={L('المعاينة', 'Video Preview')}><Empty title={L('لا شيء للمعاينة بعد', 'Nothing to preview yet')} text={L('ولّد مشهدًا واحدًا على الأقل.', 'Generate at least one scene.')} action={<Btn tone="accent" onClick={() => st.go('storyboard')}>{L('الستوري بورد', 'Storyboard')}</Btn>} /></Slate>;
  const onTime = () => { const el = v.current; if (!el || !clip) return; const end = clip.trim_out ?? el.duration; setPos(starts[idx] + Math.max(0, el.currentTime - (clip.trim_in || 0))); if (el.currentTime >= end - 0.04) next(); };
  const next = () => { if (idx < clips.length - 1) setIdx(idx + 1); else { setPlaying(false); v.current?.pause(); setIdx(0); setPos(0); } };
  const toggle = () => { const el = v.current; if (!el) return; if (playing) { el.pause(); setPlaying(false); } else { el.play().catch(() => {}); setPlaying(true); } };
  const latest = exports[0];

  return (
    <Slate title={L('المعاينة', 'Video Preview')} actions={<div className="flex bg-panel border border-line rounded-md p-0.5">{([['cut', L('مونتاج أولي', 'Rough cut')], ['export', L('الفيلم المُصدَّر', 'Exported film')]] as const).map(([m, label]) => <button key={m} type="button" disabled={m === 'export' ? !exports.length : !clips.length} onClick={() => { setMode(m); setPlaying(false); }} className={cx('h-8 px-3 rounded text-sm disabled:opacity-40', mode === m ? 'bg-raised text-text' : 'text-mute')}>{label}</button>)}</div>}>
      <div className="max-w-5xl mx-auto">
        <div className="frame rounded-sm overflow-hidden" style={{ aspectRatio: p.aspect.replace(':', ' / '), maxHeight: '62vh', marginInline: 'auto' }}>
          {mode === 'cut' && scene && <video ref={v} data-preview="cut" key={scene.video_path} src={fileUrl(sceneVideo(root, scene))} className="w-full h-full" onTimeUpdate={onTime} onEnded={next} onClick={toggle} />}
          {mode === 'export' && latest && <video data-preview="export" key={latest.path} src={fileUrl(inLibrary(root, latest.path))} controls className="w-full h-full" />}
        </div>
        {mode === 'cut' && <>
          <div className="flex items-center gap-4 mt-4"><Btn tone="accent" data-action="play" onClick={toggle}>{playing ? L('إيقاف مؤقت', 'Pause') : L('تشغيل', 'Play')}</Btn><span className="num text-sm text-soft">{fmtDuration(pos)} / {fmtDuration(total)}</span><span className="text-sm text-mute">{L('مشهد', 'Scene')} <span className="num">{(scene?.position ?? 0) + 1}</span> — {scene?.title}</span></div>
          <div className="relative h-8 mt-3 ltr bg-stage border border-line rounded-sm overflow-hidden">{clips.map((c, i) => <button key={c.scene_id} type="button" onClick={() => setIdx(i)} className={cx('absolute top-0 bottom-0 border-e border-ink text-[10px] num', i === idx ? 'bg-accent/30 text-text' : 'bg-raised text-mute hover:text-soft')} style={{ left: `${(starts[i] / Math.max(total, 0.1)) * 100}%`, width: `${(clipLen(c) / Math.max(total, 0.1)) * 100}%` }}>{String((sceneOf(c.scene_id)?.position ?? i) + 1).padStart(2, '0')}</button>)}<span className="absolute top-0 bottom-0 w-px bg-accent pointer-events-none" style={{ left: `${(pos / Math.max(total, 0.1)) * 100}%` }} /></div>
          <div className="mt-4"><Note>{L('المونتاج الأولي يشغّل المقاطع بترتيبها وقصّها فقط. الانتقالات وتصحيح اللون ومسارات الصوت تظهر في الفيلم المُصدَّر.', 'The rough cut plays the clips in order with their trims only. Transitions, colour correction and audio tracks appear in the exported film.')}</Note></div>
        </>}
        {mode === 'export' && latest && <p className="text-sm text-mute mt-4"><span className="num">{latest.width}×{latest.height}</span> · <span className="num">{fmtDuration(latest.duration)}</span> · <span className="num">{fmtSize(latest.size)}</span> · {fmtDate(latest.created_at)}</p>}
      </div>
    </Slate>
  );
}
