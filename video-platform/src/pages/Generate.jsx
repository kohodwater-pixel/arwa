import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { Icon } from '../icons.jsx';
import { Button, Loading, useAction, DemoBadge, StatusBadge, Player, usePolling, Confirm, useToast } from '../ui.jsx';

const ACTIVE = ['queued', 'generating', 'assembling'];

export default function Generate() {
  const { id } = useParams(); const nav = useNavigate(); const toast = useToast();
  const { L, num, err } = useI18n();
  const [project, setProject] = useState(null); const [busy, run] = useAction(); const [confirm, setConfirm] = useState(false);
  const load = useCallback(async () => { const r = await api.get(`/projects/${id}`); setProject(r.project); }, [id]);
  useEffect(() => { load().catch((e) => { toast(err(e), 'err'); nav('/library'); }); }, [load]); // eslint-disable-line react-hooks/exhaustive-deps
  const active = !!project && ACTIVE.includes(project.status);
  const offline = usePolling(load, 1500, active);
  const act = (key, fn) => run(key, async () => { const r = await fn(); if (r?.project) setProject(r.project); });

  if (!project) return <Loading />;
  const pct = Math.round(project.progress * 100);
  const failed = project.scenes.filter((s) => s.status === 'failed');
  const headline = {
    generating: L('جارٍ توليد المشاهد…', 'Generating the scenes…'), queued: L('في قائمة الانتظار…', 'Waiting in the queue…'), assembling: L('جارٍ تجميع الفيلم والصوت…', 'Assembling the film and sound…'),
    completed: L('اكتمل الفيديو', 'The video is ready'), failed: L('لم يكتمل التوليد', 'Generation did not finish'), canceled: L('أُلغي التوليد', 'Generation was canceled'),
    storyboard: L('لم يبدأ التوليد بعد', 'Generation has not started'), draft: L('لم يبدأ التوليد بعد', 'Generation has not started'),
  }[project.status];

  return (
    <div className="container">
      <div className="page-head">
        <div className="grow">
          <div className="row wrap small muted" style={{ marginBottom: 6 }}><Link to="/library">{L('المكتبة', 'Library')}</Link><Icon name="arrow" size={13} flip /><Link to={`/projects/${id}`}>{project.title}</Link></div>
          <h2>{headline}</h2>
          <div className="row wrap" style={{ marginTop: 10 }}>{project.isDemo && <DemoBadge />}<StatusBadge status={project.status} /><span className="badge ltr">{project.providerLabel}</span></div>
        </div>
        <div className="row wrap">
          {active && <Button className="danger" icon="x" disabled={!!busy} onClick={() => setConfirm(true)}>{L('إلغاء التوليد', 'Cancel generation')}</Button>}
          {!active && <Link className="btn" to={`/projects/${id}/storyboard`}><Icon name="edit" />{L('العودة للمخطط', 'Back to storyboard')}</Link>}
        </div>
      </div>

      <div className="stack lg">
        {offline && <div className="banner warn" role="status"><Icon name="alert" /><span>{L('انقطع الاتصال بالخادم. التوليد مستمر في الخلفية، وسنعيد المحاولة تلقائيًا.', 'Connection to the server was lost. Generation continues in the background; retrying automatically.')}</span></div>}
        {project.isDemo && <div className="banner demo"><Icon name="alert" /><span>{L('وضع تجريبي: ما تراه بطاقات بديلة ينتجها الخادم لتجربة المسار، وليست فيديو مولّدًا بالذكاء الاصطناعي.', 'Demo mode: what you see are placeholder cards rendered by the server to try the workflow, not AI-generated video.')}</span></div>}

        {project.status === 'completed' && project.final && (
          <div className="stack">
            <Player src={project.final.url} aspect={project.aspect} poster={project.posterUrl} isDemo={project.isDemo} downloadUrl={`${project.final.url}?download=1`} />
            <div className="row wrap" style={{ justifyContent: 'center' }}>
              <Link className="btn primary" to={`/projects/${id}`}><Icon name="film" />{L('صفحة المشروع', 'Open project')}</Link>
              <a className="btn" href={`${project.final.url}?download=1`} download><Icon name="download" />{L('تحميل الفيديو', 'Download video')}</a>
            </div>
          </div>
        )}

        {active && (
          <div className="card pad-lg stack">
            <div className="row between"><b>{project.status === 'assembling' ? L('التجميع النهائي', 'Final assembly') : L(`${project.scenesCompleted} من ${project.sceneCount} مشاهد`, `${project.scenesCompleted} of ${project.sceneCount} scenes`)}</b><span className="ltr muted">{num(pct)}%</span></div>
            <div className={`progress ${project.status === 'assembling' ? 'indet' : ''}`}><i style={{ width: `${Math.max(3, pct)}%` }} /></div>
            <p className="hint">{L('يعمل التوليد في الخلفية على الخادم. يمكنك إغلاق الصفحة والعودة لاحقًا من المكتبة.', 'Generation runs in the background on the server. You can close this page and come back later from the library.')}</p>
          </div>
        )}

        {project.status === 'failed' && (
          <div className="banner err"><Icon name="alert" />
            <div className="grow">
              <b>{project.error?.startsWith('assembly') ? L('فشل تجميع الفيلم.', 'Assembling the film failed.') : L(`فشل توليد ${failed.length} من ${project.sceneCount} مشاهد. المشاهد الناجحة محفوظة.`, `${failed.length} of ${project.sceneCount} scenes failed. The finished scenes are kept.`)}</b>
              {project.error?.startsWith('assembly') && <div className="ltr small" style={{ marginTop: 4 }}>{project.error}</div>}
            </div>
            <Button className="sm primary" icon="refresh" busy={busy === 'retry'} onClick={() => act('retry', () => (project.error?.startsWith('assembly') ? api.post(`/projects/${id}/assemble`) : api.post(`/projects/${id}/generate`)))}>{L('إعادة المحاولة', 'Retry')}</Button>
          </div>
        )}
        {['canceled', 'storyboard', 'draft'].includes(project.status) && <div className="banner info"><Icon name="info" /><span className="grow">{L('لا توجد عملية توليد جارية لهذا المشروع.', 'Nothing is being generated for this project.')}</span><Link className="btn sm primary" to={`/projects/${id}/storyboard`}>{L('فتح المخطط', 'Open storyboard')}</Link></div>}

        <div className="tiles">
          {project.scenes.map((s, i) => (
            <div key={s.id} className="tile">
              <div className="view">
                {s.clip ? <video src={s.clip.url} controls muted playsInline preload="metadata" /> : s.status === 'generating' || s.status === 'queued' ? <span className="spin" style={{ width: 24, height: 24, color: 'var(--accent)' }} /> : <Icon name={s.status === 'failed' ? 'alert' : 'film'} size={26} />}
              </div>
              <div className="meta">
                <div className="row between"><b>{num(i + 1)}. {s.title}</b><span className="faint">{num(s.duration)}{L('ث', 's')}</span></div>
                <div className="row between"><StatusBadge status={s.status} />{s.status === 'generating' && s.progress > 0 && <span className="ltr faint">{Math.round(s.progress * 100)}%</span>}</div>
                {s.status === 'generating' && <div className={`progress ${s.progress ? '' : 'indet'}`}><i style={{ width: `${Math.round((s.progress || 0) * 100)}%` }} /></div>}
                {s.error && <div className="ltr small" style={{ color: 'var(--err)' }}>{s.error}</div>}
              </div>
            </div>
          ))}
        </div>
      </div>
      {confirm && <Confirm title={L('إلغاء التوليد؟', 'Cancel generation?')} text={L('تتوقف المهام الجارية، وتبقى المشاهد المكتملة محفوظة.', 'Running jobs stop; finished scenes are kept.')} confirmLabel={L('إلغاء التوليد', 'Cancel generation')} danger onClose={() => setConfirm(false)} onConfirm={() => act('cancel', () => api.post(`/projects/${id}/cancel`))} />}
    </div>
  );
}
