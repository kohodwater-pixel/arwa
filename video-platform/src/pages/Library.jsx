import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { Icon } from '../icons.jsx';
import { Button, Loading, useAction, DemoBadge, StatusBadge, Confirm, usePolling, Modal, Player } from '../ui.jsx';
import Uploader from '../components/Uploader.jsx';

const ACTIVE = ['queued', 'generating', 'assembling'];
const target = (p) => (ACTIVE.includes(p.status) ? `/projects/${p.id}/generate` : ['draft', 'storyboard'].includes(p.status) ? `/projects/${p.id}/storyboard` : `/projects/${p.id}`);

function Files() {
  const { L, date } = useI18n(); const [assets, setAssets] = useState(null); const [busy, run] = useAction(); const [del, setDel] = useState(null);
  const load = useCallback(() => api.get('/assets').then((r) => setAssets(r.assets)), []);
  useEffect(() => { load().catch(() => setAssets([])); }, [load]);
  if (!assets) return <Loading />;
  return (
    <div className="stack">
      <div className="row wrap"><Uploader compact label={L('رفع صورة أو فيديو مرجعي', 'Upload a reference image or video')} onUploaded={load} /><Uploader compact purpose="audio" label={L('رفع ملف صوتي', 'Upload an audio file')} onUploaded={load} /></div>
      {!assets.length ? <div className="empty"><Icon name="image" size={30} /><div>{L('لا توجد ملفات مرجعية بعد.', 'No reference files yet.')}</div></div> : (
        <div className="grid cards">
          {assets.map((a) => (
            <div key={a.id} className="pcard">
              <div className="thumb">{a.kind === 'reference_image' ? <img src={a.url} alt={a.filename} loading="lazy" /> : a.kind === 'reference_video' ? <video src={a.url} muted controls preload="metadata" style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : <Icon name="music" size={30} />}</div>
              <div className="body">
                <div className="title ltr">{a.filename}</div>
                <div className="desc">{a.kind === 'audio_upload' ? L('ملف صوتي', 'Audio file') : a.kind === 'reference_image' ? L('صورة مرجعية', 'Reference image') : L('فيديو مرجعي', 'Reference video')} · <span className="ltr">{(a.size / 1048576).toFixed(1)} MB</span> · {date(a.createdAt)}</div>
                {a.kind === 'audio_upload' && <audio src={a.url} controls preload="none" style={{ width: '100%', marginTop: 6 }} />}
              </div>
              <div className="foot"><span className="spacer" /><button className="btn ghost icon danger" disabled={!!busy} onClick={() => setDel(a)} aria-label={L('حذف', 'Delete')}><Icon name="trash" /></button></div>
            </div>
          ))}
        </div>
      )}
      {del && <Confirm title={L('حذف الملف؟', 'Delete this file?')} text={L('يُحذف الملف نهائيًا ويُفك ارتباطه بأي مشهد.', 'The file is deleted permanently and detached from any scene.')} confirmLabel={L('حذف', 'Delete')} danger onClose={() => setDel(null)} onConfirm={() => run('del', async () => { await api.del(`/assets/${del.id}`); await load(); })} />}
    </div>
  );
}

export default function Library() {
  const { L, num, date } = useI18n(); const nav = useNavigate(); const [sp, setSp] = useSearchParams();
  const tab = sp.get('tab') || 'all';
  const [data, setData] = useState(null); const [q, setQ] = useState(''); const [busy, run] = useAction(); const [del, setDel] = useState(null); const [watch, setWatch] = useState(null);
  const load = useCallback(async () => { if (tab === 'files') return; const r = await api.get(`/projects?status=${tab === 'all' ? '' : tab}&q=${encodeURIComponent(q)}`); setData(r); }, [tab, q]);
  useEffect(() => { const t = setTimeout(() => load().catch(() => setData((d) => d || { projects: [], counts: {} })), q ? 250 : 0); return () => clearTimeout(t); }, [load, q]);
  const anyActive = !!data?.projects.some((p) => ACTIVE.includes(p.status));
  const offline = usePolling(load, 3000, anyActive && tab !== 'files');
  const c = data?.counts || {};
  const tabs = [['all', L('مشاريعي', 'My projects'), c.all], ['completed', L('المكتملة', 'Completed'), c.completed], ['active', L('قيد الإنشاء', 'In progress'), c.active], ['failed', L('الفاشلة', 'Failed'), c.failed], ['drafts', L('المسودات', 'Drafts'), c.drafts], ['files', L('الصور والملفات المرجعية', 'Reference files')]];

  return (
    <div className="container">
      <div className="page-head">
        <div><h2>{L('مكتبة المشاريع', 'Project library')}</h2><p>{L('كل مشاريعك ومسوداتك وملفاتك المرجعية.', 'All your projects, drafts and reference files.')}</p></div>
        <Link className="btn primary" to="/create"><Icon name="plus" />{L('مشروع جديد', 'New project')}</Link>
      </div>
      <div className="tabs" role="tablist">{tabs.map(([k, t, n]) => <button key={k} role="tab" aria-selected={tab === k} className={`tab ${tab === k ? 'on' : ''}`} onClick={() => setSp(k === 'all' ? {} : { tab: k })}>{t}{n != null && <span className="count">{num(n)}</span>}</button>)}</div>
      {offline && <div className="banner warn" style={{ marginBottom: 16 }}><Icon name="alert" /><span>{L('انقطع الاتصال بالخادم؛ نعيد المحاولة.', 'Connection lost; retrying.')}</span></div>}
      {tab === 'files' ? <Files /> : !data ? <Loading /> : (
        <div className="stack">
          <input className="input" style={{ maxWidth: 360 }} type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={L('بحث في العنوان أو الوصف…', 'Search title or description…')} aria-label={L('بحث', 'Search')} />
          {!data.projects.length ? (
            <div className="empty"><Icon name="film" size={32} /><h3>{q ? L('لا نتائج', 'No results') : L('لا توجد مشاريع هنا بعد', 'No projects here yet')}</h3>{!q && <p style={{ marginTop: 14 }}><Link className="btn primary" to="/create">{L('إنشاء أول فيديو', 'Create your first video')}</Link></p>}</div>
          ) : (
            <div className="grid cards">
              {data.projects.map((p) => (
                <div key={p.id} className="pcard">
                  <Link to={target(p)} className="thumb" aria-label={p.title}>
                    {p.posterUrl ? <img src={p.posterUrl} alt="" loading="lazy" /> : <Icon name="film" size={30} />}
                    <span className="badges">{p.isDemo && <DemoBadge />}<StatusBadge status={p.status} /></span>
                    {ACTIVE.includes(p.status) && <div className={`progress ${p.status === 'assembling' ? 'indet' : ''}`}><i style={{ width: `${Math.max(4, Math.round(p.progress * 100))}%` }} /></div>}
                  </Link>
                  <div className="body">
                    <Link to={target(p)} className="title">{p.title}</Link>
                    <div className="desc">{p.description}</div>
                    <div className="hint"><span className="ltr">{p.providerLabel} · {p.aspect}</span> · {num(p.duration)}{L('ث', 's')} · {date(p.updatedAt)}</div>
                  </div>
                  <div className="foot">
                    {p.final && p.status === 'completed' && <button className="btn ghost sm" onClick={() => setWatch(p)}><Icon name="play" size={15} />{L('مشاهدة', 'Watch')}</button>}
                    {p.final && p.status === 'completed' && <a className="btn ghost icon" href={`${p.final.url}?download=1`} download aria-label={L('تحميل', 'Download')} title={L('تحميل', 'Download')}><Icon name="download" /></a>}
                    {p.status === 'failed' && <Link className="btn ghost sm" to={`/projects/${p.id}/generate`}><Icon name="refresh" size={15} />{L('إعادة المحاولة', 'Retry')}</Link>}
                    <span className="spacer" />
                    <Link className="btn ghost icon" to={`/projects/${p.id}/storyboard`} aria-label={L('تعديل', 'Edit')} title={L('تعديل', 'Edit')}><Icon name="edit" /></Link>
                    <button className="btn ghost icon" disabled={!!busy} onClick={() => run('dup', async () => { const r = await api.post(`/projects/${p.id}/duplicate`); nav(`/projects/${r.project.id}/storyboard`); })} aria-label={L('نسخ', 'Duplicate')} title={L('نسخ', 'Duplicate')}><Icon name="copy" /></button>
                    <button className="btn ghost icon danger" disabled={!!busy} onClick={() => setDel(p)} aria-label={L('حذف', 'Delete')} title={L('حذف', 'Delete')}><Icon name="trash" /></button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      {watch && <Modal wide title={watch.title} onClose={() => setWatch(null)}><Player src={watch.final.url} aspect={watch.aspect} poster={watch.posterUrl} isDemo={watch.isDemo} downloadUrl={`${watch.final.url}?download=1`} /></Modal>}
      {del && <Confirm title={L('حذف المشروع؟', 'Delete this project?')} text={L(`يُحذف «${del.title}» ومشاهده والفيديو المولَّد نهائيًا.`, `"${del.title}", its scenes and its generated video are deleted permanently.`)} confirmLabel={L('حذف نهائي', 'Delete permanently')} danger onClose={() => setDel(null)} onConfirm={() => run('del', async () => { await api.del(`/projects/${del.id}`); await load(); })} />}
    </div>
  );
}
