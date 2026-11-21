import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button, Loading, useAction, DemoBadge, StatusBadge, Player, Confirm, usePolling, copyText, useToast, arClass } from '../ui.jsx';
import Treatment from '../components/Treatment.jsx';
import AudioPanel from '../components/AudioPanel.jsx';
import { RefThumb } from '../components/Uploader.jsx';

const ACTIVE = ['queued', 'generating', 'assembling'];

export default function Project() {
  const { id } = useParams(); const nav = useNavigate(); const toast = useToast();
  const { L, num, name, date, err } = useI18n(); const { meta } = useSession();
  const [project, setProject] = useState(null); const [busy, run] = useAction(); const [confirm, setConfirm] = useState(null);
  const [audio, setAudio] = useState(null); const [tab, setTab] = useState('scenes');
  const load = useCallback(async () => { const r = await api.get(`/projects/${id}`); setProject(r.project); setAudio((a) => a || r.project.audio); }, [id]);
  useEffect(() => { load().catch((e) => { toast(err(e), 'err'); nav('/library'); }); }, [load]); // eslint-disable-line react-hooks/exhaustive-deps
  const active = !!project && ACTIVE.includes(project.status);
  usePolling(load, 2500, active);
  const act = (key, fn, ok) => run(key, async () => { const r = await fn(); if (r?.project) setProject(r.project); return r; }, ok);

  if (!project || !meta) return <Loading />;
  const type = meta.videoTypes.find((v) => v.id === project.videoType); const style = meta.styles.find((v) => v.id === project.style);
  const shareUrl = project.shareToken ? `${location.origin}/watch/${project.shareToken}` : null;
  const audioDirty = audio && JSON.stringify(audio) !== JSON.stringify(project.audio);
  const allDone = project.scenes.length > 0 && project.scenes.every((s) => s.status === 'completed');
  const go = (fn) => run('gen', async () => { await fn(); nav(`/projects/${id}/generate`); });

  return (
    <div className="container">
      <div className="page-head">
        <div className="grow">
          <div className="row wrap small muted" style={{ marginBottom: 6 }}><Link to="/library">{L('المكتبة', 'Library')}</Link><Icon name="arrow" size={13} flip /><span>{L('تفاصيل المشروع', 'Project details')}</span></div>
          <h2>{project.title}</h2>
          <div className="row wrap" style={{ marginTop: 10 }}>{project.isDemo && <DemoBadge />}<StatusBadge status={project.status} /><span className="badge ltr">{project.providerLabel} · {project.capabilities?.label || project.quality}</span><span className="badge ltr">{project.aspect}</span><span className="badge">{num(project.duration)} {L('ثانية', 'seconds')}</span></div>
        </div>
        <div className="row wrap">
          {active ? <Link className="btn primary" to={`/projects/${id}/generate`}><Icon name="play" />{L('متابعة التوليد', 'Follow generation')}</Link> : <Link className="btn" to={`/projects/${id}/storyboard`}><Icon name="edit" />{L('تعديل المشاهد', 'Edit scenes')}</Link>}
          <Button icon="copy" disabled={!!busy} onClick={() => run('dup', async () => { const r = await api.post(`/projects/${id}/duplicate`); nav(`/projects/${r.project.id}/storyboard`); })}>{L('نسخ المشروع', 'Duplicate')}</Button>
          <Button className="danger" icon="trash" disabled={!!busy} onClick={() => setConfirm('delete')}>{L('حذف', 'Delete')}</Button>
        </div>
      </div>

      <div className="split">
        <div className="stack lg">
          {project.final ? (
            <>
              {project.status !== 'completed' && <div className="banner warn"><Icon name="alert" /><span>{L('هذا آخر فيديو مكتمل. المشروع عُدّل بعده ولم يُعَد توليده أو تجميعه بعد.', 'This is the last finished video. The project was edited afterwards and has not been regenerated or re-assembled yet.')}</span></div>}
              <Player src={`${project.final.url}?v=${project.final.id}`} aspect={project.aspect} poster={project.posterUrl} isDemo={project.final.isDemo} downloadUrl={`${project.final.url}?download=1`} />
              <div className="row wrap">
                <a className="btn primary" href={`${project.final.url}?download=1`} download><Icon name="download" />{L('تحميل الفيديو', 'Download video')}</a>
                <Button icon="refresh" disabled={!!busy || active || !project.providerUsable} onClick={() => setConfirm('regen')}>{L('إعادة التوليد', 'Regenerate')}</Button>
                <span className="hint ltr">{project.final.width}×{project.final.height} · {project.final.duration?.toFixed(1)}s · {(project.final.size / 1048576).toFixed(1)} MB</span>
              </div>
            </>
          ) : (
            <div className={`player ${arClass(project.aspect)}`} style={{ display: 'grid', placeItems: 'center', background: 'var(--surface)' }}>
              <div className="center muted stack sm" style={{ padding: 24, alignItems: 'center' }}>
                <Icon name="film" size={34} />
                <span>{active ? L('الفيديو قيد الإنشاء…', 'The video is being created…') : project.status === 'failed' ? L('لم يكتمل التوليد.', 'Generation did not finish.') : L('لم يُولَّد فيديو لهذا المشروع بعد.', 'No video has been generated for this project yet.')}</span>
                {!active && project.scenes.length > 0 && <Link className="btn primary" to={project.status === 'failed' ? `/projects/${id}/generate` : `/projects/${id}/storyboard`}>{project.status === 'failed' ? L('عرض الأخطاء وإعادة المحاولة', 'See errors and retry') : L('فتح المخطط', 'Open storyboard')}</Link>}
                {!project.scenes.length && <Link className="btn primary" to={`/projects/${id}/storyboard`}>{L('بناء المخطط', 'Build storyboard')}</Link>}
              </div>
            </div>
          )}

          <div>
            <div className="tabs" role="tablist">
              {[['scenes', L('المشاهد', 'Scenes')], ['treatment', L('التصور الإخراجي', 'Treatment')], ['audio', L('الصوت', 'Sound')]].map(([k, t]) => <button key={k} role="tab" aria-selected={tab === k} className={`tab ${tab === k ? 'on' : ''}`} onClick={() => setTab(k)}>{t}</button>)}
            </div>
            {tab === 'scenes' && (project.scenes.length ? (
              <div className="tiles">
                {project.scenes.map((s, i) => (
                  <div key={s.id} className="tile">
                    <div className="view">{s.clip ? <video src={s.clip.url} controls muted playsInline preload="metadata" /> : <Icon name="film" size={26} />}</div>
                    <div className="meta">
                      <div className="row between"><b>{num(i + 1)}. {s.title}</b><span className="faint">{num(s.duration)}{L('ث', 's')}</span></div>
                      <p className="muted small">{s.description}</p>
                      <div className="row between"><StatusBadge status={s.status} />
                        {s.clip && !active && <Button className="sm ghost" icon="refresh" disabled={!!busy || !project.providerUsable} onClick={() => go(() => api.post(`/projects/${id}/scenes/${s.id}/generate`))}>{L('إعادة توليده', 'Regenerate')}</Button>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : <div className="empty">{L('لا توجد مشاهد بعد.', 'No scenes yet.')}</div>)}
            {tab === 'treatment' && (project.treatment ? <Treatment t={project.treatment} /> : <div className="empty">{L('لم يُبنَ التصور الإخراجي بعد.', 'The treatment has not been built yet.')}</div>)}
            {tab === 'audio' && audio && (
              <div className="stack">
                <AudioPanel value={audio} onChange={setAudio} files={project.audioFiles} onUploaded={() => load()} nativeAudio={project.capabilities?.nativeAudio} />
                <div className="row wrap">
                  <Button disabled={!audioDirty || !!busy || active} busy={busy === 'audio'} onClick={() => act('audio', () => api.patch(`/projects/${id}`, { audio }), L('حُفظت إعدادات الصوت', 'Sound settings saved'))}>{L('حفظ إعدادات الصوت', 'Save sound settings')}</Button>
                  <Button className="primary" icon="film" disabled={!allDone || !!busy || active} onClick={() => go(async () => { if (audioDirty) await api.patch(`/projects/${id}`, { audio }); await api.post(`/projects/${id}/assemble`); })}>{L('إعادة تجميع الفيلم بالصوت', 'Re-assemble the film with sound')}</Button>
                </div>
                {!allDone && <p className="hint">{L('إعادة التجميع متاحة بعد اكتمال توليد كل المشاهد.', 'Re-assembly is available once every scene has been generated.')}</p>}
              </div>
            )}
          </div>
        </div>

        <aside className="stack">
          <div className="card stack">
            <h3>{L('الوصف', 'Description')}</h3>
            <p className="muted" style={{ whiteSpace: 'pre-wrap' }}>{project.description}</p>
            <dl className="kv">
              <dt>{L('النوع', 'Type')}</dt><dd>{name(type)}</dd>
              <dt>{L('الأسلوب', 'Style')}</dt><dd>{name(style)}</dd>
              <dt>{L('المحرك', 'Engine')}</dt><dd className="ltr">{project.providerLabel}</dd>
              <dt>{L('المشاهد', 'Scenes')}</dt><dd>{num(project.scenesCompleted)} / {num(project.sceneCount)}</dd>
              <dt>{L('أُنشئ', 'Created')}</dt><dd>{date(project.createdAt)}</dd>
              <dt>{L('آخر تحديث', 'Updated')}</dt><dd>{date(project.updatedAt)}</dd>
            </dl>
            <Link className="btn sm" to={`/create?edit=${id}`}><Icon name="cog" size={16} />{L('تعديل الإعدادات', 'Edit settings')}</Link>
          </div>

          <div className="card stack">
            <h3>{L('مشاركة برابط', 'Share by link')}</h3>
            {project.status !== 'completed' ? <p className="hint">{L('المشاركة متاحة بعد اكتمال الفيديو.', 'Sharing is available once the video is finished.')}</p> : shareUrl ? (
              <>
                <input className="input ltr small" readOnly value={shareUrl} onFocus={(e) => e.target.select()} aria-label={L('رابط المشاهدة', 'Watch link')} />
                <div className="row wrap">
                  <Button className="sm primary" icon="copy" onClick={() => copyText(shareUrl).then(() => toast(L('نُسخ الرابط', 'Link copied')))}>{L('نسخ الرابط', 'Copy link')}</Button>
                  <Button className="sm ghost danger" disabled={!!busy} onClick={() => act('share', () => api.post(`/projects/${id}/share`, { enabled: false }), L('أُوقفت المشاركة', 'Sharing turned off'))}>{L('إيقاف المشاركة', 'Stop sharing')}</Button>
                </div>
                <p className="hint">{L('أي شخص لديه الرابط يستطيع مشاهدة الفيديو دون حساب.', 'Anyone with the link can watch the video without an account.')}</p>
              </>
            ) : <Button icon="share" busy={busy === 'share'} onClick={() => act('share', () => api.post(`/projects/${id}/share`, { enabled: true }))}>{L('إنشاء رابط مشاهدة', 'Create a watch link')}</Button>}
          </div>

          {project.references.length > 0 && <div className="card stack"><h3>{L('الملفات المرجعية', 'Reference files')}</h3><div className="refs">{project.references.map((r) => <a key={r.id} href={r.url} target="_blank" rel="noreferrer"><RefThumb asset={r} /></a>)}</div></div>}
        </aside>
      </div>

      {confirm === 'delete' && <Confirm title={L('حذف المشروع؟', 'Delete this project?')} text={L('يُحذف المشروع ومشاهده والفيديو المولَّد نهائيًا. الملفات المرجعية التي رفعتها تبقى في مكتبتك.', 'The project, its scenes and the generated video are deleted permanently. Reference files you uploaded stay in your library.')} confirmLabel={L('حذف نهائي', 'Delete permanently')} danger onClose={() => setConfirm(null)} onConfirm={async () => { try { await api.del(`/projects/${id}`); nav('/library'); } catch (e) { toast(err(e), 'err'); } }} />}
      {confirm === 'regen' && <Confirm title={L('إعادة توليد كل المشاهد؟', 'Regenerate every scene?')} text={L('تُولَّد كل المشاهد من جديد بالإعدادات الحالية وتُستبدل المقاطع الحالية. يُحتسب ذلك من حد التوليد.', 'Every scene is generated again with the current settings and the current clips are replaced. This counts against your generation limit.')} confirmLabel={L('إعادة التوليد', 'Regenerate')} onClose={() => setConfirm(null)} onConfirm={() => go(() => api.post(`/projects/${id}/generate`, { all: true }))} />}
    </div>
  );
}
