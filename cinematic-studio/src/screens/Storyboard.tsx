import { useState } from 'react';
import { useStudio, isActive } from '../lib/store';
import { L, pick, statusText, reasonText } from '../lib/i18n';
import { rpc, fileUrl } from '../lib/rpc';
import { Btn, Slate, Tag, Empty, Confirm, Meter, cx, Note } from '../lib/ui';
import { alternate, cameraMoves, shotSizes, compileOne, type Director } from '../director';
import { toDraft, scenePreview, sceneVideo } from '../lib/project';

export default function Storyboard() {
  const st = useStudio();
  const p = st.project;
  const d: Director | null = p.director;
  const [del, setDel] = useState<any | null>(null);
  const [regenAll, setRegenAll] = useState(false);
  const [drag, setDrag] = useState<string | null>(null);
  const root = st.status.library_root;
  const jobs = st.jobs.filter((j) => j.project_id === p.id && j.kind === 'generate' && isActive(j));
  const jobOf = (sid: string) => jobs.find((j) => j.scene_id === sid);
  const pending = p.scenes.filter((s: any) => s.status !== 'completed' && !jobOf(s.id)).length;

  const generate = async (scene_ids?: string[], all = false) => {
    const r: any = await st.run(() => rpc('generate', { project_id: p.id, scene_ids, all }));
    if (r) { st.toast(r.queued ? L(`أُضيفت ${r.queued} مهمة إلى قائمة التنفيذ`, `${r.queued} job(s) added to the queue`) : L('لا مشاهد تحتاج توليدًا', 'No scenes need generating'), r.queued ? 'ok' : 'info'); st.refreshProject(); }
  };
  const reorder = (ids: string[]) => st.save(() => rpc('scenes_reorder', { project_id: p.id, order: ids }));
  const move = (i: number, by: number) => { const ids = p.scenes.map((s: any) => s.id); const j = i + by; if (j < 0 || j >= ids.length) return; [ids[i], ids[j]] = [ids[j], ids[i]]; reorder(ids); };
  const drop = (target: string) => { if (!drag || drag === target) return; const ids: string[] = p.scenes.map((s: any) => s.id).filter((x: string) => x !== drag); ids.splice(ids.indexOf(target), 0, drag); setDrag(null); reorder(ids); };
  // A new take: another description and camera move for this scene, with its prompt rewritten for the model.
  const newTake = (s: any) => {
    if (!d) return;
    const neighbours = [p.scenes[s.position - 1]?.camera_move, p.scenes[s.position + 1]?.camera_move].filter(Boolean);
    const alt = alternate({ ...toDraft(s, d, p.scenes), variant: (s.seed_variant || 0) + Math.floor(Math.random() * 3) }, d, neighbours);
    const c = compileOne(alt, d, p.model_id, s.position, p.scenes.length);
    return st.save(() => rpc('scene_update', { id: s.id, patch: { title: alt.title, description: alt.description, camera_move: alt.camera_move, shot_size: alt.shot_size, camera_angle: alt.camera_angle, ...c, prompt_edited: false } }));
  };
  const add = () => st.save(() => rpc('scene_add', { project_id: p.id, scene: { title: L('مشهد جديد', 'New scene'), duration: 3, description: '', prompt: '', camera_move: 'static', shot_size: 'medium', role: 'action' } })).then(() => st.toast(L('أُضيف مشهد. اكتب وصفه وبرومبته من «محرر المشهد».', 'Scene added. Write its description and prompt in the Scene Editor.')));

  if (!p.scenes.length) return <Slate title={L('الستوري بورد', 'Storyboard Studio')}><Empty title={L('لا مشاهد بعد', 'No scenes yet')} text={L('اطلب من المخرج تقسيم الفيلم، أو أضف المشاهد يدويًا.', 'Ask the director to split the film, or add scenes by hand.')} action={<><Btn tone="accent" onClick={() => st.go('creator')}>{L('منشئ الفيديو', 'AI Video Creator')}</Btn><Btn data-action="add-scene" onClick={add}>{L('أضف مشهدًا', 'Add scene')}</Btn></>} /></Slate>;
  const total = p.scenes.reduce((n: number, s: any) => n + s.duration, 0);

  return (
    <Slate title={L('الستوري بورد', 'Storyboard Studio')} sub={<><span className="num">{p.scenes.length}</span> {L('مشاهد', 'scenes')} · <span className="num">{total}s</span> · <span className="ltr">{p.model_id}</span> · <span className="num">{p.aspect}</span></>}
      actions={<><Btn data-action="add-scene" onClick={add}>{L('أضف مشهدًا', 'Add scene')}</Btn><Btn onClick={() => setRegenAll(true)}>{L('أعد توليد الكل', 'Regenerate all')}</Btn><Btn tone="accent" data-action="generate-missing" disabled={!pending} onClick={() => generate()}>{pending ? L(`ولّد ${pending} مشاهد`, `Generate ${pending} scene(s)`) : L('كل المشاهد مولَّدة', 'All scenes generated')}</Btn></>}>
      {!st.status.settings.comfy_url && <div className="mb-5"><Note tone="warn">{L('خادم ComfyUI غير مضبوط: مهام التوليد ستنتظر في القائمة حتى تضبطه من «الإعدادات». التطبيق لا يصنع مقاطع وهمية.', 'No ComfyUI server is configured: generation jobs will wait in the queue until you set one in Settings. The app does not produce placeholder clips.')}</Note></div>}
      <div className="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-5" data-storyboard>
        {p.scenes.map((s: any, i: number) => {
          const job = jobOf(s.id);
          return (
            <article key={s.id} data-scene={s.id} draggable onDragStart={() => setDrag(s.id)} onDragOver={(e) => e.preventDefault()} onDrop={() => drop(s.id)} className={cx('bg-panel border rounded-lg overflow-hidden flex flex-col', drag === s.id ? 'border-accent opacity-60' : 'border-line')}>
              <div className="sprockets h-1.5" />
              <button type="button" className="relative aspect-video bg-black block" onClick={() => st.go('scene', s.id)} aria-label={L('افتح المشهد', 'Open scene')}>
                {s.video_path ? <video src={fileUrl(sceneVideo(root, s))} poster={fileUrl(scenePreview(root, s))} muted loop preload="none" className="w-full h-full object-contain" onMouseEnter={(e) => e.currentTarget.play().catch(() => {})} onMouseLeave={(e) => { e.currentTarget.pause(); e.currentTarget.currentTime = 0; }} />
                  : <span className="absolute inset-0 grid place-items-center text-xs text-mute">{job ? statusText(job.status) : L('لم يُولَّد بعد', 'Not generated yet')}</span>}
                <span className="absolute top-2 start-2 num text-[11px] bg-black/70 px-1.5 rounded text-accent">{String(i + 1).padStart(2, '0')}</span>
                <span className="absolute top-2 end-2 num text-[11px] bg-black/70 px-1.5 rounded">{s.duration}s</span>
              </button>
              {job && <div className="px-3 pt-2"><Meter value={job.progress || 0} /><p className="text-[11px] text-mute mt-1">{job.status === 'blocked' ? reasonText(job.blocked_reason) : job.stage || statusText(job.status)}</p></div>}
              <div className="p-3 flex-1 flex flex-col gap-2">
                <div className="flex items-start justify-between gap-2"><h3 className="text-sm font-medium truncate">{s.title}</h3><Tag status={job ? job.status : s.status} /></div>
                <p className="text-[13px] text-mute line-clamp-2 min-h-[2.6em]">{s.description || <span className="ltr">{s.prompt}</span>}</p>
                <p className="text-[11px] text-mute">{pick(shotSizes.find((x) => x.id === s.shot_size))} · {pick(cameraMoves.find((x) => x.id === s.camera_move))}{s.reference_media_id ? ` · ${L('مرجع بصري', 'visual reference')}` : ''}</p>
                {s.error && <p className="text-[12px] text-bad selectable line-clamp-3">{s.error}</p>}
                <div className="mt-auto pt-2 flex flex-wrap gap-1 border-t border-line">
                  <Btn small tone="ghost" data-action="edit" onClick={() => st.go('scene', s.id)}>{L('تعديل', 'Edit')}</Btn>
                  <Btn small tone="ghost" data-action="generate" disabled={!!job} onClick={() => generate([s.id])}>{s.video_path ? L('أعد التوليد', 'Regenerate') : L('ولّد', 'Generate')}</Btn>
                  {d && <Btn small tone="ghost" data-action="new-take" disabled={!!job} onClick={() => newTake(s)} title={L('وصف وحركة كاميرا مختلفان لهذا المشهد', 'A different description and camera move for this scene')}>{L('لقطة بديلة', 'New take')}</Btn>}
                  <span className="ms-auto flex">
                    <Btn small tone="ghost" aria-label={L('قدّم المشهد', 'Move earlier')} disabled={i === 0} onClick={() => move(i, -1)}>↑</Btn>
                    <Btn small tone="ghost" aria-label={L('أخّر المشهد', 'Move later')} disabled={i === p.scenes.length - 1} onClick={() => move(i, 1)}>↓</Btn>
                    <Btn small tone="ghost" data-action="delete" aria-label={L('احذف المشهد', 'Delete scene')} disabled={!!job || p.scenes.length === 1} className="hover:!text-bad" onClick={() => setDel(s)}>×</Btn>
                  </span>
                </div>
              </div>
            </article>
          );
        })}
      </div>
      {del && <Confirm danger title={L('حذف المشهد', 'Delete scene')} confirmLabel={L('حذف', 'Delete')} onClose={() => setDel(null)} text={<p>{L(`سيُحذف «${del.title}» من الستوري بورد.${del.video_path ? ' مقطعه المولَّد يُنقل إلى مجلد ‎_replaced‎ ولا يُمحى.' : ''}`, `"${del.title}" will be removed from the storyboard.${del.video_path ? ' Its generated clip is moved to _replaced, not erased.' : ''}`)}</p>} onConfirm={() => st.save(() => rpc('scene_delete', { id: del.id }))} />}
      {regenAll && <Confirm title={L('إعادة توليد كل المشاهد', 'Regenerate all scenes')} confirmLabel={L('أعد التوليد', 'Regenerate')} onClose={() => setRegenAll(false)} text={<p>{L(`ستُضاف ${p.scenes.length} مهمة توليد. المقاطع الحالية تبقى حتى يكتمل البديل ثم تُنقل إلى ‎_replaced‎. التوليد يستهلك وقت GPU.`, `${p.scenes.length} generation job(s) will be queued. Current clips stay until their replacement is finished, then move to _replaced. Generation uses GPU time.`)}</p>} onConfirm={() => generate(undefined, true)} />}
    </Slate>
  );
}
