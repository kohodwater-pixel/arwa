import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button, Field, Loading, useAction, DemoBadge, fitClip } from '../ui.jsx';
import Treatment from '../components/Treatment.jsx';
import Uploader, { RefThumb } from '../components/Uploader.jsx';
import AudioPanel, { emptyAudio } from '../components/AudioPanel.jsx';

const ASPECTS = [['16:9', 'أفقي', 'Landscape'], ['9:16', 'عمودي', 'Vertical'], ['1:1', 'مربع', 'Square'], ['4:5', 'إنستغرام', 'Instagram']];
const QUALITY = { standard: ['Standard', 'قياسية'], high: ['High Quality', 'عالية'], ultra: ['Ultra Quality', 'فائقة'] };

export default function Create() {
  const { L, name, num } = useI18n(); const { meta, user } = useSession(); const nav = useNavigate(); const [sp] = useSearchParams();
  const editId = sp.get('edit');
  const [busy, run] = useAction();
  const [loaded, setLoaded] = useState(!editId);
  const [orig, setOrig] = useState(null);
  const [f, setF] = useState(() => {
    let d = ''; try { d = sessionStorage.getItem('draft-description') || ''; sessionStorage.removeItem('draft-description'); } catch { /* ignore */ }
    return { description: d, title: '', videoType: 'commercial', style: 'auto', providerId: '', quality: 'standard', aspect: '16:9', duration: 15, custom: false, chainFrames: false };
  });
  const [refs, setRefs] = useState([]); const [audio, setAudio] = useState(emptyAudio()); const [audioFiles, setAudioFiles] = useState([]);
  const [preview, setPreview] = useState(null); const [showAudio, setShowAudio] = useState(false);
  const set = (patch) => setF((x) => ({ ...x, ...patch }));

  useEffect(() => { api.get('/assets?kinds=audio_upload').then((r) => setAudioFiles(r.assets)).catch(() => {}); }, []);
  useEffect(() => {
    if (!editId) return;
    api.get(`/projects/${editId}`).then(({ project: p }) => {
      setOrig(p);
      setF({ description: p.description, title: p.title, videoType: p.videoType, style: p.style, providerId: p.providerId, quality: p.quality, aspect: p.aspect, duration: p.duration, custom: !meta?.durations?.includes(p.duration), chainFrames: p.options.chainFrames });
      setRefs(p.references); setAudio(p.audio); setLoaded(true);
    }).catch(() => nav('/library'));
  }, [editId]); // eslint-disable-line react-hooks/exhaustive-deps

  const providers = meta?.providers || [];
  // default engine: the first real engine that is configured, otherwise demo mode
  useEffect(() => { if (meta && !f.providerId) { const p = providers.find((x) => x.configured && !x.demo) || providers.find((x) => x.configured); if (p) set({ providerId: p.id, quality: p.qualities[0].id }); } }, [meta]); // eslint-disable-line react-hooks/exhaustive-deps
  const provider = providers.find((p) => p.id === f.providerId);
  const quality = provider?.qualities.find((q) => q.id === f.quality) || provider?.qualities[0];
  useEffect(() => { if (quality && !quality.aspects.includes(f.aspect)) set({ aspect: quality.aspects[0] }); if (provider && quality && quality.id !== f.quality) set({ quality: quality.id }); }, [provider, quality]); // eslint-disable-line react-hooks/exhaustive-deps

  const clipNote = useMemo(() => {
    if (!quality) return null;
    const c = quality.clip;
    return c.values ? L(`هذا المحرك يولّد مقاطع بطول ${c.values.join(' أو ')} ثوانٍ؛ الفيديو يُبنى من عدة مشاهد، وكل مشهد يُقص إلى مدته في التجميع.`, `This engine generates clips of ${c.values.join(' or ')} seconds; the video is built from several scenes and each scene is trimmed to its length at assembly.`)
      : L(`هذا المحرك يولّد مقاطع من ${c.min} إلى ${c.max} ثوانٍ؛ المدد الأطول تُبنى من عدة مشاهد.`, `This engine generates clips of ${c.min} to ${c.max} seconds; longer videos are built from several scenes.`);
  }, [quality, L]);

  if (!meta || !loaded) return <Loading />;
  const valid = f.description.trim().length >= 10 && provider?.configured && quality;
  const body = () => ({ description: f.description, title: f.title, videoType: f.videoType, style: f.style, duration: Number(f.duration), aspect: f.aspect, quality: f.quality, providerId: f.providerId, audio, options: { chainFrames: f.chainFrames }, referenceAssetIds: refs.map((r) => r.id) });

  const submit = (draft) => run(draft ? 'draft' : 'create', async () => {
    if (editId) {
      await api.patch(`/projects/${editId}`, body());
      const rebuild = !orig.sceneCount || orig.description !== f.description.trim() || orig.videoType !== f.videoType || orig.style !== f.style || orig.duration !== Number(f.duration);
      if (draft) return nav('/library');
      if (rebuild) await api.post(`/projects/${editId}/storyboard`, { duration: Number(f.duration) });
      return nav(`/projects/${editId}/storyboard`);
    }
    const r = await api.post('/projects', { ...body(), draft });
    nav(draft ? '/library?tab=drafts' : `/projects/${r.project.id}/storyboard`);
  });
  const enhance = () => run('enhance', async () => { const r = await api.post('/engine/enhance', { description: f.description, videoType: f.videoType, style: f.style }); setPreview(r); });
  const real = providers.filter((p) => !p.demo);

  return (
    <div className="container">
      <div className="page-head">
        <div><h2>{editId ? L('تعديل المشروع', 'Edit project') : L('إنشاء فيديو', 'Create a video')}</h2><p>{L('اكتب الفكرة ببساطة. المحرك الإخراجي يحوّلها إلى مشاهد بكاميرا وإضاءة وألوان.', 'Write the idea simply. The cinematic engine turns it into scenes with camera, lighting and colour.')}</p></div>
      </div>
      <div className="split">
        <div className="stack lg">
          <div className="prompt-box">
            <textarea autoFocus value={f.description} maxLength={4000} onChange={(e) => { set({ description: e.target.value }); setPreview(null); }}
              placeholder={L('مثال: مشهد سينمائي لسيارة رياضية سوداء تسير وسط شوارع طوكيو الممطرة ليلًا، انعكاسات النيون على الأرض…', 'Example: a cinematic shot of a black sports car driving through the rainy streets of Tokyo at night, neon reflections on the ground…')} aria-label={L('وصف الفيديو', 'Video description')} />
            <div className="bar">
              <span className="hint">{num(f.description.length)} / 4000</span><span className="spacer" />
              <Button className="sm" icon="spark" busy={busy === 'enhance'} disabled={f.description.trim().length < 10} onClick={enhance}>{L('حوّله إلى برومبت إخراجي', 'Turn into a production prompt')}</Button>
            </div>
          </div>

          {preview && (
            <div className="card stack">
              <div className="row between"><h3>{L('قراءة المخرج للوصف', 'The director’s reading')}</h3><button className="btn ghost icon" onClick={() => setPreview(null)} aria-label="close"><Icon name="x" /></button></div>
              <Treatment t={preview.treatment} />
              {preview.aiDirector && <p className="hint">{L('هذه معاينة فورية من محرك القواعد. عند إنشاء المشروع يعيد المخرج الذكي كتابة المشاهد ويثبّت وصف العناصر.', 'This is an instant preview from the rule engine. When the project is created, the AI director rewrites the scenes and locks the description of the elements.')}</p>}
            </div>
          )}

          <div className="card stack">
            <h3>{L('نوع الفيديو', 'Video type')}</h3>
            <div className="chips">{meta.videoTypes.map((v) => <button key={v.id} className={`chip ${f.videoType === v.id ? 'on' : ''}`} onClick={() => { set({ videoType: v.id }); setPreview(null); }} aria-pressed={f.videoType === v.id}>{name(v)}</button>)}</div>
            <div className="grid c2">
              <Field label={L('الأسلوب السينمائي', 'Cinematic style')}><select className="select" value={f.style} onChange={(e) => { set({ style: e.target.value }); setPreview(null); }}>{meta.styles.map((s) => <option key={s.id} value={s.id}>{name(s)}</option>)}</select></Field>
              <Field label={L('عنوان المشروع (اختياري)', 'Project title (optional)')}><input className="input" value={f.title} maxLength={120} onChange={(e) => set({ title: e.target.value })} /></Field>
            </div>
          </div>

          <div className="card stack">
            <div><h3>{L('صور وفيديوهات مرجعية', 'Reference images and videos')}</h3><p className="hint">{L('الصور يمكن ربطها بمشهد محدد كإطار بداية في صفحة المخطط (إن كان المحرك يدعم ذلك). الفيديوهات تُحفظ كمرجع بصري للمشروع ولا تُرسل إلى المحرك.', 'Images can be attached to a scene as its first frame on the storyboard page (when the engine supports it). Videos are kept as a visual reference for the project and are not sent to the engine.')}</p></div>
            {refs.length > 0 && <div className="refs">{refs.map((r) => <RefThumb key={r.id} asset={r} onRemove={() => setRefs(refs.filter((x) => x.id !== r.id))} />)}</div>}
            <Uploader projectId={editId || undefined} onUploaded={(a) => setRefs((x) => [...x, a])} />
          </div>

          <div className="card stack">
            <button className="row between" style={{ background: 'none', border: 0, padding: 0, cursor: 'pointer', textAlign: 'start' }} onClick={() => setShowAudio(!showAudio)} aria-expanded={showAudio}>
              <div><h3>{L('الصوت والموسيقى (اختياري)', 'Sound and music (optional)')}</h3><p className="hint">{L('موسيقى، مؤثرات، أصوات محيطة وتعليق صوتي.', 'Music, effects, ambience and voice-over.')}</p></div>
              <Icon name={showAudio ? 'up' : 'down'} />
            </button>
            {showAudio && <AudioPanel value={audio} onChange={setAudio} files={audioFiles} onUploaded={(a) => setAudioFiles((x) => [a, ...x])} nativeAudio={quality?.nativeAudio} />}
          </div>
        </div>

        <aside className="stack">
          <div className="card stack">
            <h3>{L('محرك التوليد', 'Generation engine')}</h3>
            <div className="stack sm">
              {providers.map((p) => (
                <button key={p.id} className={`chip ${f.providerId === p.id ? 'on' : ''}`} style={{ justifyContent: 'space-between', borderRadius: 12, textDecoration: 'none' }} disabled={!p.configured} onClick={() => set({ providerId: p.id, quality: p.qualities[0].id })} aria-pressed={f.providerId === p.id}>
                  <span className="ltr">{p.label}</span>
                  {p.demo || p.mockOnly ? <DemoBadge /> : p.configured ? <span className="badge ok">{L('متصل', 'Connected')}</span> : <span className="badge" title={p.statusNote || ''}>{p.statusNote ? L('لا يوجد عامل GPU', 'No GPU worker') : L('غير مهيأ', 'Not configured')}</span>}
                </button>
              ))}
            </div>
            {provider?.mockOnly && <div className="banner demo"><Icon name="alert" /><span>{L('المحرك الخاص متصل بعامل تجريبي (Mock) فقط: لا يوجد نموذج يعمل فعلًا، والمخرجات بطاقات بديلة موسومة.', 'The self-hosted engine has only a mock worker connected: no model actually runs, and outputs are labelled placeholders.')}</span></div>}
            {provider?.demo && <div className="banner demo"><Icon name="alert" /><span>{L('الوضع التجريبي لا يولّد فيديو بالذكاء الاصطناعي. ينتج بطاقات بديلة موسومة «DEMO» لتجربة المسار كاملًا فقط.', 'Demo mode does not generate AI video. It produces placeholder cards stamped "DEMO" so you can try the whole workflow.')}</span></div>}
            {!real.some((p) => p.configured) && <p className="hint">{user.role === 'admin' ? <>{L('لربط محرك حقيقي أضف مفتاح API من ', 'To connect a real engine add an API key in ')}<Link to="/admin?tab=providers" style={{ color: 'var(--accent)' }}>{L('لوحة المدير ← المزودون', 'Admin → Providers')}</Link>.</> : L('لم يربط المدير أي محرك توليد حقيقي بعد.', 'The administrator has not connected a real engine yet.')}</p>}
            {provider?.verified === 'unverified' && <div className="banner warn"><Icon name="alert" /><span>{L('محوّل تجريبي: لم يُتحقق من توثيق هذا المزود ولم يُختبر مع خدمته.', 'Experimental adapter: this provider’s documentation was not verified and it has not been tested against the live service.')}</span></div>}
          </div>

          {quality && (
            <div className="card stack">
              <Field label={L('الجودة', 'Quality')}>
                <div className="chips">{['standard', 'high', 'ultra'].map((id) => { const q = provider.qualities.find((x) => x.id === id); return <button key={id} className={`chip ${f.quality === id ? 'on' : ''}`} disabled={!q} title={q ? q.label : L('غير مدعومة في هذا المحرك', 'Not supported by this engine')} onClick={() => set({ quality: id })} aria-pressed={f.quality === id}><span className="ltr">{QUALITY[id][0]}</span></button>; })}</div>
                <span className="hint ltr">{quality.label}</span>
              </Field>
              <Field label={L('أبعاد الفيديو', 'Aspect ratio')} hint={ASPECTS.some(([a]) => !quality.aspects.includes(a)) ? L('الأبعاد المشطوبة غير مدعومة في هذا المحرك بهذه الجودة.', 'Struck-through ratios are not supported by this engine at this quality.') : null}>
                <div className="chips">{ASPECTS.map(([a, ar, en]) => <button key={a} className={`chip ${f.aspect === a ? 'on' : ''}`} disabled={!quality.aspects.includes(a)} onClick={() => set({ aspect: a })} aria-pressed={f.aspect === a}><span className="ltr">{a}</span> {L(ar, en)}</button>)}</div>
              </Field>
              <Field label={L('مدة الفيديو', 'Duration')} hint={clipNote}>
                <div className="chips">
                  {meta.durations.map((d) => <button key={d} className={`chip ${!f.custom && Number(f.duration) === d ? 'on' : ''}`} onClick={() => set({ duration: d, custom: false })} aria-pressed={!f.custom && Number(f.duration) === d}>{num(d)} {L('ث', 's')}</button>)}
                  <button className={`chip ${f.custom ? 'on' : ''}`} onClick={() => set({ custom: true })} aria-pressed={f.custom}>{L('مخصصة', 'Custom')}</button>
                </div>
                {f.custom && <input className="input ltr" type="number" min="2" max={meta.maxProjectSeconds} value={f.duration} onChange={(e) => set({ duration: e.target.value })} aria-label={L('المدة بالثواني', 'Duration in seconds')} />}
                {f.custom && <span className="hint">{L(`من 2 إلى ${meta.maxProjectSeconds} ثانية.`, `From 2 to ${meta.maxProjectSeconds} seconds.`)}</span>}
              </Field>
              {quality.imageToVideo && !quality.imageByUrl && (
                <label className="row top small" style={{ cursor: 'pointer' }}>
                  <input type="checkbox" checked={f.chainFrames} onChange={(e) => set({ chainFrames: e.target.checked })} style={{ marginTop: 5, accentColor: 'var(--accent)' }} />
                  <span><b>{L('ربط المشاهد بالإطار الأخير', 'Chain scenes by last frame')}</b><br /><span className="muted">{L('يبدأ كل مشهد من آخر إطار في المشهد السابق لاستمرارية أقوى. التوليد يصبح متتابعًا وأبطأ.', 'Each scene starts from the last frame of the previous one for stronger continuity. Generation becomes sequential and slower.')}</span></span>
                </label>
              )}
            </div>
          )}

          <Button className="primary lg block" icon="spark" busy={busy === 'create'} disabled={!valid || !!busy} onClick={() => submit(false)}>{editId ? L('حفظ وبناء المخطط', 'Save and build storyboard') : L('إنشاء فيديو', 'Create video')}</Button>
          <Button className="block" busy={busy === 'draft'} disabled={!valid || !!busy} onClick={() => submit(true)}>{L('حفظ كمسودة', 'Save as draft')}</Button>
          <p className="hint center">{L('الخطوة التالية: مراجعة مخطط المشاهد قبل أي توليد.', 'Next step: review the storyboard before anything is generated.')}</p>
          {quality && Number(f.duration) > 0 && fitClip(quality.clip, 1) > Number(f.duration) && <p className="hint center">{L('المدة أقصر من أقصر مقطع يولّده المحرك؛ سيُقص المقطع.', 'The duration is shorter than the engine’s shortest clip; the clip will be trimmed.')}</p>}
        </aside>
      </div>
    </div>
  );
}
