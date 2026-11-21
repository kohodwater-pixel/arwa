import { useState } from 'react';
import { useStudio, isActive } from '../lib/store';
import { L, fmtDuration, fmtDate, fmtSize, statusText } from '../lib/i18n';
import { rpc, fileUrl, inLibrary } from '../lib/rpc';
import { Btn, Slate, Field, Select, Panel, Meter, Tag, Note, Row } from '../lib/ui';
import { useTimeline } from '../lib/timeline';

export default function ExportCenter() {
  const st = useStudio();
  const p = st.project;
  const { tl, update, total } = useTimeline();
  const [play, setPlay] = useState<string | null>(null);
  const root = st.status.library_root;
  const job = st.jobs.find((j) => j.project_id === p.id && j.kind === 'export' && isActive(j));
  const failed = st.jobs.find((j) => j.project_id === p.id && j.kind === 'export' && j.status === 'failed');
  const done = p.scenes.filter((s: any) => s.status === 'completed').length;
  if (!tl) return <Slate title={L('مركز التصدير', 'Export Center')}><p className="text-mute">…</p></Slate>;
  const o = tl.output;
  const start = async () => { const r = await st.run(() => rpc('export', { project_id: p.id, options: { output: o } })); if (r) st.toast(L('بدأ التصدير', 'Export started'), 'ok'); };
  return (
    <Slate title={L('مركز التصدير', 'Export Center')} sub={L('يُجمع الفيلم على جهازك عبر FFmpeg: المقاطع بقصّها وانتقالاتها، تصحيح اللون، ومسارات الصوت، ثم يُفحص الناتج قبل اعتماده.', 'The film is assembled on your computer by FFmpeg: clips with their trims and transitions, colour correction and the audio tracks; the result is checked before it is accepted.')}>
      <div className="grid grid-cols-[360px_1fr] gap-6 items-start">
        <Panel title={L('إعدادات التصدير', 'Export settings')}>
          <div className="space-y-4">
            <Field label={L('الدقة', 'Resolution')}><Select data-field="preset" value={o.preset} onChange={(e) => update((t) => { t.output.preset = e.target.value; return t; })}><option value="source">{L('دقة المقاطع الأصلية', 'Source resolution')}</option><option value="1080p">1080p</option><option value="720p">720p</option></Select></Field>
            <Field label={L('الإطارات في الثانية', 'Frames per second')}><Select value={o.fps} onChange={(e) => update((t) => { t.output.fps = Number(e.target.value); return t; })}>{[24, 25, 30].map((f) => <option key={f}>{f}</option>)}</Select></Field>
            <Field label={L('الجودة', 'Quality')} hint={<span className="num">H.264 · CRF {o.crf} · AAC</span>}><Select value={o.crf} onChange={(e) => update((t) => { t.output.crf = Number(e.target.value); return t; })}><option value={16}>{L('عالية جدًا (ملف أكبر)', 'Very high (larger file)')}</option><option value={18}>{L('عالية', 'High')}</option><option value={23}>{L('متوسطة (ملف أصغر)', 'Medium (smaller file)')}</option></Select></Field>
          </div>
          <div className="mt-5 pt-4 border-t border-line">
            <Row k={L('المشاهد الجاهزة', 'Finished scenes')} v={<span className="num">{done} / {p.scenes.length}</span>} />
            <Row k={L('المقاطع على الخط الزمني', 'Clips on the timeline')} v={<span className="num">{tl.clips.length}</span>} />
            <Row k={L('المدة', 'Length')} v={<span className="num">{fmtDuration(total)}</span>} />
            <Row k={L('مسارات صوت مضافة', 'Added audio items')} v={<span className="num">{tl.audio.length}</span>} />
          </div>
          {done < p.scenes.length && tl.clips.length > 0 && <div className="mt-4"><Note tone="warn">{L(`${p.scenes.length - done} مشاهد لم تُولَّد بعد ولن تدخل في الفيلم.`, `${p.scenes.length - done} scene(s) are not generated yet and will not be in the film.`)}</Note></div>}
          {!st.status.ffmpeg && <div className="mt-4"><Note tone="bad">{L('FFmpeg غير موجود. حدّد مجلده من «الإعدادات».', 'FFmpeg was not found. Set its folder in Settings.')}</Note></div>}
          <Btn tone="accent" className="w-full mt-5" data-action="export" disabled={!!job || !tl.clips.length || !st.status.ffmpeg} onClick={start}>{job ? L('يصدّر…', 'Exporting…') : L('صدّر MP4', 'Export MP4')}</Btn>
          {job && <div className="mt-4"><Meter value={job.progress || 0} /><div className="flex justify-between text-xs text-mute mt-1.5"><span>{job.stage || statusText(job.status)}</span><span className="num">{Math.round((job.progress || 0) * 100)}%</span></div><Btn small tone="ghost" className="mt-2" onClick={() => st.run(() => rpc('job_cancel', { id: job.id }))}>{L('إلغاء التصدير', 'Cancel export')}</Btn></div>}
          {!job && failed && !p.exports?.some((e: any) => e.created_at > failed.created_at && e.status === 'completed') && <div className="mt-4"><Note tone="bad"><span className="selectable">{failed.error}</span></Note></div>}
        </Panel>
        <Panel title={L('الملفات المُصدَّرة', 'Exported files')} right={<Btn small tone="ghost" onClick={() => st.run(() => rpc('reveal', { path: `${p.absolute_folder}/exports` }))}>{L('افتح المجلد', 'Open folder')}</Btn>}>
          {!p.exports?.length && <p className="text-sm text-mute">{L('لا ملفات مُصدَّرة بعد.', 'No exported files yet.')}</p>}
          <div className="divide-y divide-line" data-exports>
            {(p.exports || []).map((e: any) => (
              <div key={e.id} data-export={e.status} className="py-3 first:pt-0">
                <div className="flex items-center gap-3"><Tag status={e.status} /><span className="ltr text-sm truncate flex-1 selectable">{e.path.split('/').pop()}</span>{e.status === 'completed' && <Btn small onClick={() => setPlay(play === e.id ? null : e.id)}>{play === e.id ? L('إغلاق', 'Close') : L('تشغيل', 'Play')}</Btn>}</div>
                <p className="text-xs text-mute mt-1.5">{e.status === 'completed' ? <><span className="num">{e.width}×{e.height}</span> · <span className="num">{fmtDuration(e.duration)}</span> · <span className="num">{fmtSize(e.size)}</span> · </> : null}{fmtDate(e.created_at)}{e.status === 'completed' ? ` · ${L('مع ملف بيانات ‎.json', 'with a .json metadata file')}` : ''}</p>
                {e.error && <p className="text-xs text-bad mt-1 selectable">{e.error}</p>}
                {play === e.id && <video src={fileUrl(inLibrary(root, e.path))} controls autoPlay className="w-full mt-3 rounded-sm max-h-[50vh]" />}
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </Slate>
  );
}
