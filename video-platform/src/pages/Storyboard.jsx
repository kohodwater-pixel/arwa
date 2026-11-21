import { useCallback, useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button, Loading, useAction, DemoBadge, StatusBadge, Confirm, Field, fitClip, useToast } from '../ui.jsx';
import Treatment from '../components/Treatment.jsx';
import Uploader, { RefThumb } from '../components/Uploader.jsx';

function SceneCard({ scene, index, total, project, meta, act, busy, drag }) {
  const { L, name, num } = useI18n();
  const caps = project.capabilities;
  const [desc, setDesc] = useState(scene.description); const [title, setTitle] = useState(scene.title);
  const [vo, setVo] = useState(scene.voiceover); const [prompt, setPrompt] = useState(scene.prompt); const [open, setOpen] = useState(false);
  useEffect(() => { setDesc(scene.description); setTitle(scene.title); setVo(scene.voiceover); setPrompt(scene.prompt); }, [scene.description, scene.title, scene.voiceover, scene.prompt]);
  const patch = (body) => act(`scene-${scene.id}`, () => api.patch(`/projects/${project.id}/scenes/${scene.id}`, body));
  const clip = fitClip(caps.clip, scene.duration);
  const images = project.references.filter((r) => r.kind === 'reference_image');
  const working = busy === `scene-${scene.id}` || busy === `regen-${scene.id}`;
  return (
    <div id={`scene-${scene.id}`} className={`scene ${drag.dragging === scene.id ? 'dragging' : ''} ${drag.over === scene.id ? 'over' : ''}`}
      onDragOver={(e) => { if (drag.dragging) { e.preventDefault(); drag.setOver(scene.id); } }} onDrop={(e) => { e.preventDefault(); drag.drop(scene.id); }}>
      <div className="rail">
        <span className="num">{num(index + 1)}</span>
        <span className="grip" draggable onDragStart={(e) => { e.dataTransfer.effectAllowed = 'move'; drag.start(scene.id); }} onDragEnd={drag.end} title={L('اسحب لإعادة الترتيب', 'Drag to reorder')}><Icon name="drag" /></span>
        <button className="btn ghost icon" disabled={index === 0 || !!busy} onClick={() => drag.move(index, -1)} aria-label={L('تحريك لأعلى', 'Move up')}><Icon name="up" /></button>
        <button className="btn ghost icon" disabled={index === total - 1 || !!busy} onClick={() => drag.move(index, 1)} aria-label={L('تحريك لأسفل', 'Move down')}><Icon name="down" /></button>
      </div>
      <div className="content">
        <div className="head">
          <input className="title" value={title} maxLength={80} onChange={(e) => setTitle(e.target.value)} onBlur={() => title.trim() && title !== scene.title && patch({ title })} aria-label={L('عنوان المشهد', 'Scene title')} />
          {scene.status === 'completed' && <span className="badge ok"><Icon name="check" size={13} />{L('مولَّد', 'Generated')}</span>}
          {scene.status === 'failed' && <StatusBadge status="failed" />}
          {working && <span className="spin" style={{ color: 'var(--accent)' }} />}
          <Button className="sm ghost" icon="refresh" disabled={!!busy} onClick={() => act(`regen-${scene.id}`, () => api.post(`/projects/${project.id}/scenes/${scene.id}/regenerate`))}>{L('صياغة بديلة', 'New take')}</Button>
          <button className="btn ghost icon danger" disabled={total <= 1 || !!busy} onClick={() => act(`scene-${scene.id}`, () => api.del(`/projects/${project.id}/scenes/${scene.id}`))} aria-label={L('حذف المشهد', 'Delete scene')}><Icon name="trash" /></button>
        </div>
        <textarea className="textarea" value={desc} maxLength={1500} onChange={(e) => setDesc(e.target.value)} onBlur={() => desc.trim().length >= 3 && desc.trim() !== scene.description && patch({ description: desc })} aria-label={L('وصف المشهد', 'Scene description')} />
        <div className="controls3">
          <Field label={L('المدة', 'Duration')}>
            <div className="stepper">
              <button disabled={scene.duration <= 1 || !!busy} onClick={() => patch({ duration: scene.duration - 1 })} aria-label="-">−</button>
              <span>{num(scene.duration)} {L('ث', 's')}</span>
              <button disabled={scene.duration >= caps.clip.max || !!busy} onClick={() => patch({ duration: scene.duration + 1 })} aria-label="+">+</button>
            </div>
          </Field>
          <Field label={L('حركة الكاميرا', 'Camera movement')}><select className="select" value={scene.cameraMove} disabled={!!busy} onChange={(e) => patch({ cameraMove: e.target.value })}>{meta.cameraMoves.map((m) => <option key={m.id} value={m.id}>{name(m)}</option>)}</select></Field>
          <Field label={L('حجم اللقطة', 'Shot size')}><select className="select" value={scene.shotSize} disabled={!!busy} onChange={(e) => patch({ shotSize: e.target.value })}>{meta.shotSizes.map((m) => <option key={m.id} value={m.id}>{name(m)}</option>)}</select></Field>
        </div>
        {clip > scene.duration && <span className="hint">{L(`المحرك يولّد هذا المشهد بطول ${clip} ث ثم يُقص إلى ${scene.duration} ث في التجميع.`, `The engine generates this scene at ${clip}s; it is trimmed to ${scene.duration}s at assembly.`)}</span>}
        {scene.error && <div className="banner err"><Icon name="alert" /><span className="ltr small">{scene.error}</span></div>}

        <div className="row wrap small">
          <button className="btn ghost sm" onClick={() => setOpen(!open)} aria-expanded={open}><Icon name={open ? 'up' : 'down'} size={15} />{L('الصورة المرجعية، التعليق، والبرومبت', 'Reference image, voice-over and prompt')}</button>
          {scene.referenceAssetId && <span className="badge info"><Icon name="image" size={13} />{L('يبدأ من صورة مرجعية', 'Starts from a reference image')}</span>}
          {scene.promptEdited && <span className="badge warn">{L('برومبت معدّل يدويًا', 'Prompt edited by hand')}</span>}
        </div>
        {open && (
          <div className="stack">
            <Field label={L('صورة مرجعية لهذا المشهد (إطار البداية)', 'Reference image for this scene (first frame)')}
              hint={!caps.imageToVideo ? (caps.imageByUrl ? L('هذا المحرك يقرأ الصور عبر رابط عام، والخادم بلا عنوان عام (PUBLIC_BASE_URL)، لذلك الميزة غير متاحة.', 'This engine reads images by public URL and the server has no public address (PUBLIC_BASE_URL), so this is unavailable.') : L('المحرك المختار بهذه الجودة لا يدعم البدء من صورة.', 'The selected engine at this quality cannot start from an image.')) : images.length ? L('اضغط صورة لاختيارها، واضغطها مجددًا لإلغائها.', 'Click an image to select it, click again to clear.') : L('لا توجد صور مرجعية في المشروع بعد.', 'The project has no reference images yet.')}>
              <div className="refs">{images.map((r) => <RefThumb key={r.id} asset={r} disabled={!caps.imageToVideo || !!busy} selected={scene.referenceAssetId === r.id} onClick={() => patch({ referenceAssetId: scene.referenceAssetId === r.id ? null : r.id })} />)}</div>
            </Field>
            <Field label={L('سطر التعليق الصوتي لهذا المشهد', 'Voice-over line for this scene')} hint={L('يُستخدم عند توليد التعليق عبر خدمة صوت، ويبدأ مع بداية المشهد.', 'Used when voice-over is generated by an audio service; it starts when the scene starts.')}>
              <input className="input" value={vo} maxLength={1000} onChange={(e) => setVo(e.target.value)} onBlur={() => vo !== scene.voiceover && patch({ voiceover: vo })} />
            </Field>
            <Field label={L('البرومبت الإنتاجي المرسل إلى المحرك', 'Production prompt sent to the engine')} hint={L(`يُبنى تلقائيًا من حقول المشهد وقرارات المخرج (حد المحرك: ${caps.maxPromptChars} حرفًا). تعديله يدويًا يوقف التحديث التلقائي لهذا المشهد.`, `Built automatically from the scene fields and the director’s decisions (engine limit: ${caps.maxPromptChars} characters). Editing it by hand stops automatic updates for this scene.`)}>
              <textarea className="textarea mono ltr" style={{ minHeight: 150 }} value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            </Field>
            <div className="row wrap">
              <Button className="sm" disabled={prompt.trim() === scene.prompt || !!busy} onClick={() => patch({ prompt })}>{L('حفظ البرومبت', 'Save prompt')}</Button>
              {scene.promptEdited && <Button className="sm ghost" icon="refresh" disabled={!!busy} onClick={() => patch({ resetPrompt: true })}>{L('العودة للبرومبت التلقائي', 'Back to automatic prompt')}</Button>}
              <span className="hint ltr">{prompt.length} / {caps.maxPromptChars}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Storyboard() {
  const { id } = useParams(); const nav = useNavigate(); const toast = useToast();
  const { L, num, name, err } = useI18n(); const { meta } = useSession();
  const [project, setProject] = useState(null); const [busy, run] = useAction();
  const [confirm, setConfirm] = useState(null); const [showT, setShowT] = useState(false);
  const [dragging, setDragging] = useState(null); const [over, setOver] = useState(null);
  const ref = useRef(null); ref.current = project;

  const load = useCallback(() => api.get(`/projects/${id}`).then((r) => setProject(r.project)).catch((e) => { toast(err(e), 'err'); nav('/library'); }), [id]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [load]);
  useEffect(() => { if (project && ['queued', 'generating', 'assembling'].includes(project.status)) nav(`/projects/${id}/generate`, { replace: true }); }, [project?.status]); // eslint-disable-line react-hooks/exhaustive-deps

  const act = (key, fn) => run(key, async () => { const r = await fn(); if (r?.project) setProject(r.project); return r; });
  const reorder = (order) => act('order', () => api.post(`/projects/${id}/scenes/reorder`, { order }));
  const drag = {
    dragging, over, setOver,
    start: setDragging, end: () => { setDragging(null); setOver(null); },
    drop: (targetId) => { const ids = ref.current.scenes.map((s) => s.id); const from = ids.indexOf(dragging), to = ids.indexOf(targetId); setDragging(null); setOver(null); if (from < 0 || to < 0 || from === to) return; ids.splice(to, 0, ids.splice(from, 1)[0]); reorder(ids); },
    move: (index, dir) => { const ids = ref.current.scenes.map((s) => s.id); const [x] = ids.splice(index, 1); ids.splice(index + dir, 0, x); reorder(ids); },
  };

  if (!project || !meta) return <Loading />;
  if (!project.scenes.length) {
    return <div className="container narrow"><div className="empty"><Icon name="layers" size={30} /><h3>{L('هذا المشروع مسودة بلا مخطط مشاهد', 'This project is a draft with no storyboard')}</h3>
      <div className="row" style={{ justifyContent: 'center', marginTop: 16 }}><Button className="primary" icon="spark" busy={busy === 'build'} onClick={() => act('build', () => api.post(`/projects/${id}/storyboard`))}>{L('بناء مخطط المشاهد', 'Build the storyboard')}</Button><Link className="btn" to={`/create?edit=${id}`}>{L('تعديل الإعدادات', 'Edit settings')}</Link></div></div></div>;
  }
  const pending = project.scenes.filter((s) => s.status !== 'completed');
  const total = project.scenes.reduce((n, s) => n + s.duration, 0);
  const type = meta.videoTypes.find((v) => v.id === project.videoType);
  const start = () => run('generate', async () => { await api.post(`/projects/${id}/generate`); nav(`/projects/${id}/generate`); });
  const remix = () => run('generate', async () => { await api.post(`/projects/${id}/assemble`); nav(`/projects/${id}/generate`); });

  return (
    <div className="container">
      <div className="page-head">
        <div className="grow">
          <div className="row wrap small muted" style={{ marginBottom: 6 }}><Link to="/library">{L('المكتبة', 'Library')}</Link><Icon name="arrow" size={13} flip /><span>{L('مخطط المشاهد', 'Storyboard')}</span></div>
          <h2>{project.title}</h2>
          <div className="row wrap" style={{ marginTop: 10 }}>
            {project.isDemo && <DemoBadge />}
            <span className="badge ltr">{project.providerLabel} · {project.capabilities?.label}</span>
            <span className="badge">{name(type)}</span>
            <span className="badge ltr">{project.aspect}</span>
            <span className="badge"><Icon name="clock" size={13} />{num(total)} {L('ثانية', 'seconds')} · {num(project.scenes.length)} {L('مشاهد', 'scenes')}</span>
          </div>
        </div>
        <div className="row wrap">
          <Link className="btn" to={`/create?edit=${id}`}><Icon name="edit" />{L('تعديل الإعدادات', 'Edit settings')}</Link>
          <Button icon="refresh" disabled={!!busy} onClick={() => setConfirm('rebuild')}>{L('إعادة بناء المخطط', 'Rebuild storyboard')}</Button>
        </div>
      </div>

      <div className="stack lg">
        {!project.providerUsable && <div className="banner err"><Icon name="alert" /><span>{L('محرك التوليد لهذا المشروع غير مهيأ الآن. اختر محركًا آخر من «تعديل الإعدادات».', 'This project’s generation engine is not configured right now. Choose another engine in "Edit settings".')}</span></div>}
        {project.isDemo && <div className="banner demo"><Icon name="alert" /><span>{L('وضع تجريبي: التوليد سينتج بطاقات بديلة موسومة «DEMO» وليس فيديو مولّدًا بالذكاء الاصطناعي.', 'Demo mode: generation will produce placeholder cards stamped "DEMO", not AI-generated video.')}</span></div>}

        <div className="card stack">
          <button className="row between" style={{ background: 'none', border: 0, padding: 0, cursor: 'pointer', textAlign: 'start' }} onClick={() => setShowT(!showT)} aria-expanded={showT}>
            <div><h3>{L('التصور الإخراجي', 'Director’s treatment')}</h3><p className="hint ltr">{project.treatment?.lighting?.scheme} · {project.treatment?.camera?.lens} · {project.treatment?.color?.grade?.split(',')[0]}</p></div><Icon name={showT ? 'up' : 'down'} />
          </button>
          {showT && <Treatment t={project.treatment} />}
        </div>

        <div className="timeline" aria-label={L('الخط الزمني', 'Timeline')}>
          {project.scenes.map((s, i) => <button key={s.id} className={s.status === 'completed' ? 'done' : ''} style={{ flex: s.duration }} onClick={() => document.getElementById(`scene-${s.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })} title={s.title}>{num(i + 1)}<span className="faint">{num(s.duration)}{L('ث', 's')}</span></button>)}
        </div>

        <div className="stack">
          {project.scenes.map((s, i) => <SceneCard key={s.id} scene={s} index={i} total={project.scenes.length} project={project} meta={meta} act={act} busy={busy} drag={drag} />)}
          <Button className="add-scene" icon="plus" disabled={!!busy || project.scenes.length >= 24} onClick={() => act('add', () => api.post(`/projects/${id}/scenes`, {}))}>{L('إضافة مشهد', 'Add scene')}</Button>
        </div>

        <div className="card stack">
          <div><h3>{L('صور المشروع المرجعية', 'Project reference images')}</h3><p className="hint">{L('ارفع صورًا ثم اربط كل صورة بالمشهد المناسب من داخل بطاقة المشهد.', 'Upload images, then attach each one to the right scene from inside the scene card.')}</p></div>
          {project.references.length > 0 && <div className="refs">{project.references.map((r) => <RefThumb key={r.id} asset={r} />)}</div>}
          <div><Uploader projectId={id} compact label={L('رفع مرجع', 'Upload reference')} onUploaded={() => load()} /></div>
        </div>

        <div className="card row between wrap" style={{ position: 'sticky', bottom: 16, boxShadow: 'var(--shadow)', borderColor: 'var(--line-2)' }}>
          <div>
            <b>{pending.length ? L(`${pending.length} مشهد بانتظار التوليد`, `${pending.length} scene(s) to generate`) : L('كل المشاهد مولّدة', 'All scenes are generated')}</b>
            <div className="hint">{pending.length ? L('التعديلات تُحفظ تلقائيًا. التوليد يعمل في الخلفية ويمكنك مغادرة الصفحة.', 'Edits are saved automatically. Generation runs in the background; you can leave the page.') : L('تغيّر الترتيب أو الصوت؟ أعد تجميع الفيلم من المقاطع الحالية.', 'Changed the order or the sound? Assemble the film again from the current clips.')}</div>
          </div>
          {pending.length
            ? <Button className="primary lg" icon="play" busy={busy === 'generate'} disabled={!!busy || !project.providerUsable} onClick={start}>{L('اعتماد المخطط وبدء التوليد', 'Approve and generate')}</Button>
            : <Button className="primary lg" icon="film" busy={busy === 'generate'} disabled={!!busy} onClick={remix}>{L('تجميع الفيلم', 'Assemble the film')}</Button>}
        </div>
      </div>
      {confirm === 'rebuild' && <Confirm title={L('إعادة بناء المخطط؟', 'Rebuild the storyboard?')} text={L('سيُعاد تحليل الوصف وبناء المشاهد من جديد، وتُحذف تعديلاتك على المشاهد وأي مقاطع مولّدة لها.', 'The description will be analysed again and the scenes rebuilt. Your scene edits and any generated clips will be removed.')} confirmLabel={L('إعادة البناء', 'Rebuild')} danger onClose={() => setConfirm(null)} onConfirm={() => act('build', () => api.post(`/projects/${id}/storyboard`))} />}
    </div>
  );
}
