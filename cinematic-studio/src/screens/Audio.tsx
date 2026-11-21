import { useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDuration } from '../lib/i18n';
import { fileUrl } from '../lib/rpc';
import { Btn, Slate, Panel, Note } from '../lib/ui';
import { useTimeline, TRACK_LABEL, type AudioItem } from '../lib/timeline';
import { MediaPicker } from '../lib/MediaPicker';

const HINT: Record<string, [string, string]> = {
  audio: ['مؤثرات وأصوات المكان', 'Effects and ambience'], voiceover: ['تسجيل تعليق صوتي جاهز', 'A recorded voiceover file'], music: ['الموسيقى التصويرية', 'The score'],
};
export default function Audio() {
  const st = useStudio();
  const { tl, update, media, reloadMedia, total } = useTimeline();
  const [pick, setPick] = useState<AudioItem['track'] | null>(null);
  if (!tl) return <Slate title={L('استوديو الصوت', 'Audio Studio')}><p className="text-mute">…</p></Slate>;
  const set = (id: string, patch: Partial<AudioItem>) => update((t) => { Object.assign(t.audio.find((a) => a.id === id)!, patch); return t; });
  const num = (v: string, min: number, max: number) => Math.max(min, Math.min(max, Number(v) || 0));
  const tracks: AudioItem['track'][] = ['voiceover', 'music', 'audio'];
  return (
    <Slate title={L('استوديو الصوت', 'Audio Studio')} sub={<>{L('أضف ملفات صوتية من جهازك إلى المسارات الثلاثة واضبط توقيتها ومستواها. طول الفيلم', 'Add audio files from your computer to the three tracks and set their timing and level. Film length')} <span className="num">{fmtDuration(total)}</span></>} actions={<Btn onClick={() => st.go('timeline')}>{L('الخط الزمني', 'Timeline')}</Btn>}>
      <div className="mb-5"><Note>{L('هذه الشاشة تمزج ملفات صوتية موجودة لديك. توليد الصوت أو التعليق بالذكاء الاصطناعي غير مضمَّن في هذا الإصدار.', 'This screen mixes audio files you already have. AI generation of sound or voiceover is not part of this version.')}</Note></div>
      <div className="space-y-5">
        {tracks.map((track) => (
          <Panel key={track} title={<>{L(...TRACK_LABEL[track])} <span className="normal-case tracking-normal text-mute ms-2">{L(...HINT[track])}</span></>} right={<Btn small data-add-audio={track} onClick={() => setPick(track)}>{L('أضف ملفًا', 'Add file')}</Btn>}>
            {!tl.audio.some((a) => a.track === track) && <p className="text-sm text-mute">{L('المسار فارغ.', 'This track is empty.')}</p>}
            <div className="space-y-4">
              {tl.audio.filter((a) => a.track === track).map((a) => { const m = media.find((x) => x.id === a.media_id); return (
                <div key={a.id} data-audio-item={a.id} className="grid grid-cols-[minmax(0,1.3fr)_repeat(4,88px)_minmax(0,1fr)_auto] gap-3 items-end">
                  <div className="min-w-0"><p className="text-sm truncate">{m ? m.name : <span className="text-bad">{L('الملف غير موجود في المكتبة', 'File not in the library')}</span>}</p>{m && <audio src={fileUrl(m.path)} controls preload="none" className="h-7 w-full mt-1.5" />}{m?.missing ? <p className="text-xs text-bad mt-1">{L('الملف الأصلي مفقود من القرص', 'The original file is missing from disk')}</p> : null}</div>
                  {([['start', L('يبدأ عند (ث)', 'Starts at (s)'), 0, Math.max(0, total)], ['trim_in', L('تخطَّ من أوله (ث)', 'Skip from start (s)'), 0, m?.duration || 0], ['fade_in', L('دخول تدريجي', 'Fade in'), 0, 10], ['fade_out', L('خروج تدريجي', 'Fade out'), 0, 10]] as const).map(([k, label, min, max]) => <label key={k} className="block"><span className="block text-[11px] text-mute mb-1">{label}</span><input type="number" step={0.1} min={min} max={max} value={a[k] || 0} onChange={(e) => set(a.id, { [k]: num(e.target.value, min, max) })} className="w-full h-8 bg-ink border border-line-2 rounded px-2 text-sm num" /></label>)}
                  <label className="block"><span className="flex justify-between text-[11px] text-mute mb-1"><span>{L('المستوى', 'Level')}</span><span className="num">{Math.round(a.volume * 100)}%</span></span><input type="range" min={0} max={2} step={0.05} value={a.volume} onChange={(e) => set(a.id, { volume: Number(e.target.value) })} className="w-full" /></label>
                  <Btn small tone="ghost" className="hover:!text-bad" onClick={() => update((t) => ({ ...t, audio: t.audio.filter((x) => x.id !== a.id) }))}>{L('إزالة', 'Remove')}</Btn>
                </div>); })}
            </div>
          </Panel>
        ))}
      </div>
      {pick && <MediaPicker kind="audio" onClose={() => { setPick(null); reloadMedia(); }} onPick={(m) => { update((t) => { t.audio.push({ id: crypto.randomUUID(), media_id: m.id, track: pick, start: 0, volume: pick === 'music' ? 0.5 : 1, fade_in: 0, fade_out: pick === 'music' ? 1.5 : 0, trim_in: 0 }); return t; }); reloadMedia(); }} />}
    </Slate>
  );
}
