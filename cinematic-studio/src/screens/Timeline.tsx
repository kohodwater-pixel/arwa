import { useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDuration } from '../lib/i18n';
import { fileUrl } from '../lib/rpc';
import { Btn, Slate, Field, Input, Select, Empty, Panel, cx } from '../lib/ui';
import { useTimeline, TRACK_LABEL, type AudioItem } from '../lib/timeline';
import { scenePreview } from '../lib/project';

const TR: Record<string, [string, string]> = { cut: ['قطع', 'Cut'], fade: ['تلاشٍ', 'Fade'], dissolve: ['مزج', 'Dissolve'], wipeleft: ['مسح', 'Wipe'], slideleft: ['انزلاق', 'Slide'] };

export default function Timeline() {
  const st = useStudio();
  const { tl, update, transitions, media, sceneOf, clipLen, starts, total } = useTimeline();
  const [sel, setSel] = useState(0);
  const root = st.status.library_root;
  if (!tl) return <Slate title={L('الخط الزمني', 'Timeline Editor')}><p className="text-mute">…</p></Slate>;
  if (!tl.clips.length) return <Slate title={L('الخط الزمني', 'Timeline Editor')}><Empty title={L('لا مقاطع على الخط الزمني', 'No clips on the timeline')} text={L('يظهر هنا كل مشهد بعد اكتمال توليده.', 'Each scene appears here once its generation is finished.')} action={<Btn tone="accent" onClick={() => st.go('storyboard')}>{L('الستوري بورد', 'Storyboard')}</Btn>} /></Slate>;
  const audioEnd = Math.max(0, ...tl.audio.map((a) => a.start + Math.max(0, (media.find((m) => m.id === a.media_id)?.duration || 0) - (a.trim_in || 0))));
  const span = Math.max(total, 1);
  const pct = (v: number) => `${Math.min(100, (v / span) * 100)}%`;
  const c = tl.clips[Math.min(sel, tl.clips.length - 1)];
  const cs = sceneOf(c.scene_id);
  const full = cs?.video_duration || cs?.duration || 0;
  const swap = (i: number, by: number) => update((t) => { const j = i + by; if (j < 0 || j >= t.clips.length) return t; [t.clips[i], t.clips[j]] = [t.clips[j], t.clips[i]]; setSel(j); return t; });
  const setClip = (patch: any) => update((t) => { Object.assign(t.clips[sel], patch); return t; });
  const tracks: AudioItem['track'][] = ['audio', 'voiceover', 'music'];

  return (
    <Slate title={L('الخط الزمني', 'Timeline Editor')} sub={<>{L('المدة النهائية', 'Final length')} <span className="num">{fmtDuration(total)}</span> (<span className="num">{total.toFixed(2)}s</span>) · {L('أربعة مسارات: الفيديو، الصوت، التعليق، الموسيقى', 'Four tracks: video, audio, voiceover, music')}</>}
      actions={<><Btn onClick={() => st.go('audio')}>{L('استوديو الصوت', 'Audio Studio')}</Btn><Btn tone="accent" onClick={() => st.go('export')}>{L('التصدير', 'Export')}</Btn></>}>
      <div className="bg-stage border border-line rounded-lg overflow-hidden" data-timeline>
        <div className="grid grid-cols-[110px_1fr] border-b border-line text-[11px] text-mute"><div className="px-3 py-1.5 border-e border-line" /><div className="relative h-6 ltr">{Array.from({ length: Math.floor(span) + 1 }, (_, i) => i).filter((i) => i % Math.max(1, Math.ceil(span / 12)) === 0).map((i) => <span key={i} className="absolute top-1 num" style={{ left: pct(i) }}>{i}s</span>)}</div></div>
        <div className="grid grid-cols-[110px_1fr] border-b border-line">
          <div className="px-3 py-2 text-xs text-soft border-e border-line flex items-center">{L(...TRACK_LABEL.video)}</div>
          <div className="relative h-[76px] ltr">
            {tl.clips.map((clip, i) => { const s = sceneOf(clip.scene_id); return (
              <button key={clip.scene_id} type="button" data-clip={i} onClick={() => setSel(i)} className={cx('absolute top-1.5 bottom-1.5 rounded-sm overflow-hidden border text-start', i === sel ? 'border-accent z-10' : 'border-line-2')} style={{ left: pct(starts[i]), width: pct(clipLen(clip)) }}>
                {s?.preview_path && <img src={fileUrl(scenePreview(root, s))} alt="" className="absolute inset-0 w-full h-full object-cover opacity-60" />}
                <span className="absolute inset-x-0 bottom-0 bg-black/75 px-1.5 py-0.5 text-[10px] truncate"><span className="num text-accent">{String((s?.position ?? i) + 1).padStart(2, '0')}</span> <span className="num">{clipLen(clip).toFixed(1)}s</span></span>
                {i > 0 && clip.transition.kind !== 'cut' && <span className="absolute top-0 left-0 bottom-0 w-2 bg-accent/70" title={clip.transition.kind} />}
              </button>); })}
          </div>
        </div>
        {tracks.map((track) => (
          <div key={track} className="grid grid-cols-[110px_1fr] border-b border-line last:border-0">
            <div className="px-3 py-2 text-xs text-soft border-e border-line flex items-center">{L(...TRACK_LABEL[track])}</div>
            <div className="relative h-9 ltr">
              {tl.audio.filter((a) => a.track === track).map((a) => { const m = media.find((x) => x.id === a.media_id); const len = Math.max(0.2, Math.min((m?.duration || 0) - (a.trim_in || 0), span - a.start)); return <button key={a.id} type="button" onClick={() => st.go('audio')} className="absolute top-1.5 bottom-1.5 rounded-sm bg-raised border border-line-2 px-1.5 text-[10px] text-soft truncate text-start hover:border-accent" style={{ left: pct(a.start), width: pct(len) }} title={m?.name}>{m ? m.name : L('ملف مفقود', 'missing file')}</button>; })}
            </div>
          </div>
        ))}
      </div>
      {audioEnd > total + 0.05 && <p className="text-xs text-mute mt-2">{L('الصوت الأطول من الفيديو يُقصّ عند نهاية الفيديو في التصدير.', 'Audio longer than the picture is cut at the end of the picture on export.')}</p>}

      <div className="grid grid-cols-2 gap-6 mt-6 items-start">
        <Panel title={<>{L('المقطع المحدد', 'Selected clip')} <span className="num text-accent ms-1">{String((cs?.position ?? sel) + 1).padStart(2, '0')}</span> {cs?.title}</>} right={<span className="flex gap-1"><Btn small tone="ghost" disabled={sel === 0} onClick={() => swap(sel, -1)}>{L('قدّم', 'Earlier')}</Btn><Btn small tone="ghost" disabled={sel === tl.clips.length - 1} onClick={() => swap(sel, 1)}>{L('أخّر', 'Later')}</Btn></span>}>
          <div className="grid grid-cols-2 gap-4">
            <Field label={L('بداية القص (ث)', 'Trim in (s)')}><Input data-field="trim_in" type="number" step={0.1} min={0} max={full} value={c.trim_in || 0} onChange={(e) => setClip({ trim_in: Math.max(0, Math.min(Number(e.target.value) || 0, (c.trim_out ?? full) - 0.2)) })} /></Field>
            <Field label={L('نهاية القص (ث)', 'Trim out (s)')} hint={<span className="num">{L('طول المقطع', 'Clip length')} {full.toFixed(2)}s</span>}><Input data-field="trim_out" type="number" step={0.1} min={0.2} max={full} value={c.trim_out ?? Number(full.toFixed(2))} onChange={(e) => setClip({ trim_out: Math.max((c.trim_in || 0) + 0.2, Math.min(Number(e.target.value) || full, full)) })} /></Field>
            <Field label={L('الانتقال من المقطع السابق', 'Transition from the previous clip')}><Select data-field="transition" disabled={sel === 0} value={c.transition?.kind || 'cut'} onChange={(e) => setClip({ transition: { kind: e.target.value, duration: e.target.value === 'cut' ? 0 : c.transition?.duration || 0.5 } })}>{transitions.map((k) => <option key={k} value={k}>{L(...(TR[k] || [k, k]))}</option>)}</Select></Field>
            <Field label={L('مدة الانتقال (ث)', 'Transition length (s)')}><Input type="number" step={0.1} min={0.1} max={2} disabled={sel === 0 || (c.transition?.kind || 'cut') === 'cut'} value={c.transition?.duration || 0} onChange={(e) => setClip({ transition: { ...c.transition, duration: Math.max(0.1, Math.min(2, Number(e.target.value) || 0.5)) } })} /></Field>
          </div>
        </Panel>
        <Panel title={L('اللون والصوت الأصلي (على الفيلم كله)', 'Colour and clip sound (whole film)')} right={<Btn small tone="ghost" onClick={() => update((t) => ({ ...t, color: { brightness: 0, contrast: 1, saturation: 1 }, clip_audio_volume: 1 }))}>{L('إعادة الضبط', 'Reset')}</Btn>}>
          {([['brightness', L('السطوع', 'Brightness'), -0.3, 0.3], ['contrast', L('التباين', 'Contrast'), 0.6, 1.6], ['saturation', L('التشبع', 'Saturation'), 0, 2]] as const).map(([k, label, min, max]) => <label key={k} className="grid grid-cols-[90px_1fr_48px] items-center gap-3 text-sm py-1.5"><span className="text-mute text-xs">{label}</span><input type="range" min={min} max={max} step={0.01} value={tl.color[k]} onChange={(e) => update((t) => { t.color[k] = Number(e.target.value); return t; })} /><span className="num text-xs text-soft text-end">{tl.color[k].toFixed(2)}</span></label>)}
          <label className="grid grid-cols-[90px_1fr_48px] items-center gap-3 text-sm py-1.5"><span className="text-mute text-xs">{L('صوت المقاطع', 'Clip sound')}</span><input type="range" min={0} max={2} step={0.05} value={tl.clip_audio_volume} onChange={(e) => update((t) => ({ ...t, clip_audio_volume: Number(e.target.value) }))} /><span className="num text-xs text-soft text-end">{Math.round(tl.clip_audio_volume * 100)}%</span></label>
          <p className="text-xs text-mute mt-2">{L('تصحيح اللون والانتقالات ومزج الصوت تُطبَّق عند التصدير عبر FFmpeg.', 'Colour correction, transitions and the audio mix are applied on export by FFmpeg.')}</p>
        </Panel>
      </div>
    </Slate>
  );
}
