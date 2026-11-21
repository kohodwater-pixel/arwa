import { useEffect, useRef, useState } from 'react';
import { useStudio, useDebounced, isActive } from '../lib/store';
import { L, pick, reasonText, statusText } from '../lib/i18n';
import { rpc, fileUrl, inLibrary } from '../lib/rpc';
import { Btn, Slate, Field, Input, Area, Select, Tag, Note, Meter, cx, Empty } from '../lib/ui';
import { cameraMoves, shotSizes, compileOne, profileFor, type Director } from '../director';
import { toDraft, scenePreview, sceneVideo } from '../lib/project';
import { MediaPicker } from '../lib/MediaPicker';

export default function SceneEditor() {
  const st = useStudio();
  const p = st.project;
  const d: Director | null = p.director;
  const scene = p.scenes.find((s: any) => s.id === st.sceneId) || p.scenes[0];
  const [f, setF] = useState<any>(scene);
  const [picker, setPicker] = useState(false);
  const [ref, setRef] = useState<any | null>(null);
  useEffect(() => { setF(scene); }, [scene?.id, scene?.status, scene?.video_path]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (scene?.reference_media_id) rpc('media_list', { kind: 'image' }).then((r: any) => setRef(r.items.find((m: any) => m.id === scene.reference_media_id) || null)).catch(() => {}); else setRef(null); }, [scene?.reference_media_id]);
  // Edits made in quick succession are merged into one save, so a later field never cancels an earlier one.
  const queued = useRef<{ id: string; patch: any } | null>(null);
  const flush = useDebounced(() => { const q = queued.current; queued.current = null; if (q) st.save(() => rpc('scene_update', q)); }, 600);
  const persist = (id: string, patch: any) => { if (queued.current && queued.current.id !== id) { const q = queued.current; st.save(() => rpc('scene_update', q)); queued.current = null; } queued.current = { id, patch: { ...(queued.current?.patch || {}), ...patch } }; flush(); };
  if (!scene) return <Slate title={L('محرر المشهد', 'Scene Editor')}><Empty title={L('لا مشاهد في هذا المشروع', 'This project has no scenes')} action={<Btn onClick={() => st.go('storyboard')}>{L('الستوري بورد', 'Storyboard')}</Btn>} /></Slate>;
  const root = st.status.library_root;
  const job = st.jobs.find((j) => j.scene_id === scene.id && isActive(j));
  const busy = !!job;
  const profile = profileFor(p.model_id);
  const set = (k: string, v: any, extra: any = {}) => { setF((x: any) => ({ ...x, [k]: v, ...extra })); persist(scene.id, { [k]: v, ...extra }); };
  // Changing a directing choice of the scene rewrites its prompt, unless the user took over the prompt by hand.
  const setVisual = (k: string, v: any) => {
    const next = { ...f, [k]: v };
    if (d && !f.prompt_edited) { const c = compileOne(toDraft(next, d, p.scenes), d, p.model_id, scene.position, p.scenes.length); setF({ ...next, ...c }); persist(scene.id, { [k]: v, ...c }); }
    else set(k, v);
  };
  const rewrite = () => { if (!d) return; const c = compileOne(toDraft(f, d, p.scenes), d, p.model_id, scene.position, p.scenes.length); setF({ ...f, ...c, prompt_edited: 0 }); st.save(() => rpc('scene_update', { id: scene.id, patch: { ...c, prompt_edited: false } })); };
  const generate = async () => { const r: any = await st.run(() => rpc('generate', { project_id: p.id, scene_ids: [scene.id] })); if (r?.queued) { st.toast(L('أُضيفت المهمة إلى قائمة التنفيذ', 'Job added to the queue'), 'ok'); st.refreshProject(); } };
  const stale = scene.status === 'completed';

  return (
    <Slate title={<>{L('محرر المشهد', 'Scene Editor')} <span className="num text-accent ms-2">{String(scene.position + 1).padStart(2, '0')}</span></>} sub={stale ? L('تعديل ما يظهر في المشهد يُلغي مقطعه الحالي (يُحفظ جانبًا) ويحتاج توليدًا جديدًا.', 'Changing what the scene shows retires its current clip (kept aside) and needs a new generation.') : undefined}
      actions={<><Btn onClick={() => st.go('storyboard')}>{L('الستوري بورد', 'Storyboard')}</Btn><Btn tone="accent" data-action="generate-scene" disabled={busy} onClick={generate}>{scene.video_path ? L('أعد توليد المشهد', 'Regenerate scene') : L('ولّد المشهد', 'Generate scene')}</Btn></>}>
      <div className="grid grid-cols-[150px_minmax(0,1fr)_minmax(0,1fr)] gap-6 items-start">
        <nav className="space-y-1" aria-label={L('المشاهد', 'Scenes')}>
          {p.scenes.map((s: any) => <button key={s.id} type="button" onClick={() => st.go('scene', s.id)} className={cx('w-full text-start px-2.5 py-2 rounded text-[13px] flex gap-2', s.id === scene.id ? 'bg-raised text-text' : 'text-mute hover:text-soft')}><span className="num text-accent">{String(s.position + 1).padStart(2, '0')}</span><span className="truncate">{s.title}</span></button>)}
        </nav>

        <fieldset disabled={busy} className="space-y-4 min-w-0">
          <div className="grid grid-cols-[1fr_110px] gap-4">
            <Field label={L('عنوان المشهد', 'Scene title')}><Input data-field="title" value={f.title || ''} onChange={(e) => set('title', e.target.value)} /></Field>
            <Field label={L('المدة (ث)', 'Duration (s)')}><Input data-field="duration" type="number" min={1} max={30} value={f.duration} onChange={(e) => setVisual('duration', Math.max(1, Math.min(30, Number(e.target.value) || 1)))} /></Field>
          </div>
          <Field label={L('وصف المشهد', 'Scene description')} hint={L('الوصف لك أنت. ما يقرؤه النموذج هو البرومبت أدناه.', 'The description is for you. What the model reads is the prompt below.')}><Area data-field="description" rows={3} value={f.description || ''} onChange={(e) => setVisual('description', e.target.value)} /></Field>
          <div className="grid grid-cols-2 gap-4">
            <Field label={L('حجم اللقطة', 'Shot size')}><Select value={f.shot_size || 'medium'} onChange={(e) => setVisual('shot_size', e.target.value)}>{shotSizes.map((x) => <option key={x.id} value={x.id}>{pick(x)}</option>)}</Select></Field>
            <Field label={L('حركة الكاميرا', 'Camera movement')}><Select data-field="camera_move" value={f.camera_move || 'static'} onChange={(e) => setVisual('camera_move', e.target.value)}>{cameraMoves.map((x) => <option key={x.id} value={x.id}>{pick(x)}</option>)}</Select></Field>
            <Field label={L('زاوية الكاميرا', 'Camera angle')}><Input className="ltr" value={f.camera_angle || ''} onChange={(e) => setVisual('camera_angle', e.target.value)} /></Field>
            <Field label={L('الإضاءة', 'Lighting')}><Input className="ltr" value={f.lighting || ''} onChange={(e) => setVisual('lighting', e.target.value)} /></Field>
          </div>
          <Field label={<span className="flex justify-between"><span>{L('البرومبت', 'Prompt')} {f.prompt_edited ? `· ${L('معدَّل يدويًا', 'hand-edited')}` : ''}</span><span className={cx('num', (f.prompt || '').length > profile.maxChars && 'text-bad')}>{(f.prompt || '').length}/{profile.maxChars}</span></span>}>
            <Area data-field="prompt" rows={7} className="ltr" value={f.prompt || ''} onChange={(e) => { setF((x: any) => ({ ...x, prompt: e.target.value, prompt_edited: 1 })); persist(scene.id, { prompt: e.target.value, prompt_edited: true }); }} />
          </Field>
          {d && !!f.prompt_edited && <Btn small onClick={rewrite}>{L('أعد كتابة البرومبت من قرارات المخرج', 'Rewrite the prompt from the director\'s decisions')}</Btn>}
          <Field label={L('برومبت الاستبعاد', 'Negative prompt')} hint={profile.negative === 'ignored' ? L('لا أثر له مع هذا النموذج (CFG = 1).', 'Has no effect with this model (CFG 1).') : L('يُضاف إليه برومبت الاستبعاد الافتراضي لنموذج Wan تلقائيًا.', 'The default Wan negative prompt is appended automatically.')}><Area rows={2} className="ltr" value={f.negative_prompt || ''} onChange={(e) => set('negative_prompt', e.target.value)} /></Field>
          <Field label="Seed" hint={L('اتركه فارغًا لقيمة عشوائية في كل توليد.', 'Leave empty for a random value on each generation.')}><Input className="ltr w-48" type="number" min={0} value={f.seed ?? ''} onChange={(e) => set('seed', e.target.value === '' ? null : Math.max(0, Math.floor(Number(e.target.value))))} /></Field>
        </fieldset>

        <div className="space-y-4 min-w-0">
          <div className="frame aspect-video rounded-sm overflow-hidden grid place-items-center">
            {scene.video_path ? <video key={scene.video_path} data-scene-video src={fileUrl(sceneVideo(root, scene))} poster={fileUrl(scenePreview(root, scene))} controls className="w-full h-full" /> : <span className="text-sm text-mute">{L('لا يوجد مقطع مولَّد لهذا المشهد', 'No generated clip for this scene')}</span>}
          </div>
          <div className="flex items-center justify-between text-xs text-mute"><Tag status={job ? job.status : scene.status} />{scene.video_duration ? <span className="num">{scene.video_duration.toFixed(2)}s</span> : null}</div>
          {job && <div><Meter value={job.progress || 0} /><p className="text-xs text-mute mt-1.5">{job.status === 'blocked' ? reasonText(job.blocked_reason) : job.stage || statusText(job.status)}</p></div>}
          {scene.error && <Note tone="bad"><span className="selectable">{scene.error}</span></Note>}
          <div className="bg-panel border border-line rounded-lg p-4">
            <p className="text-xs text-mute mb-3">{L('المرجع البصري (الإطار الأول)', 'Visual reference (first frame)')}</p>
            {ref ? <div className="flex gap-3 items-center"><img src={fileUrl(inLibrary(root, ref.thumb_path))} alt="" className="w-28 aspect-video object-cover rounded-sm bg-black" /><div className="min-w-0 flex-1"><p className="text-sm truncate">{ref.name}</p>{!!ref.missing && <p className="text-xs text-bad">{L('الملف الأصلي مفقود', 'The original file is missing')}</p>}</div><Btn small disabled={busy} onClick={() => st.save(() => rpc('scene_update', { id: scene.id, patch: { reference_media_id: null } }))}>{L('إزالة', 'Remove')}</Btn></div>
              : <p className="text-[13px] text-mute">{L('بلا مرجع: يُولَّد المشهد من النص فقط.', 'No reference: the scene is generated from text only.')}</p>}
            <Btn small className="mt-3" data-action="pick-reference" disabled={busy} onClick={() => setPicker(true)}>{L('اختر من مكتبة الوسائط', 'Choose from the media library')}</Btn>
          </div>
        </div>
      </div>
      {picker && <MediaPicker kind="image" onClose={() => setPicker(false)} onPick={(m) => st.save(() => rpc('scene_update', { id: scene.id, patch: { reference_media_id: m.id } }))} />}
    </Slate>
  );
}
