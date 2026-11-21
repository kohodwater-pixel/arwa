import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button, Loading, useAction, StatusBadge, DemoBadge, Field, Modal, usePolling, copyText, useToast } from '../ui.jsx';

function useLoad(path, deps = []) {
  const [data, setData] = useState(null);
  const load = useCallback(() => api.get(path).then(setData), [path]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { setData(null); load().catch(() => {}); }, [load, ...deps]); // eslint-disable-line react-hooks/exhaustive-deps
  return [data, load];
}

function Overview() {
  const { L, num } = useI18n(); const [d, load] = useLoad('/admin/overview'); usePolling(load, 5000, true);
  if (!d) return <Loading />;
  const stats = [[L('المستخدمون', 'Users'), d.users], [L('المشاريع', 'Projects'), d.projects], [L('فيديوهات مكتملة', 'Completed videos'), d.completed], [L('مهام جارية', 'Active jobs'), d.activeJobs], [L('مهام فاشلة (24 س)', 'Failed jobs (24h)'), d.failedJobs24h], [L('ثوانٍ مولّدة (24 س)', 'Seconds generated (24h)'), d.secondsToday], [L('ثوانٍ تجريبية (24 س)', 'Demo seconds (24h)'), d.demoSecondsToday], [L('التخزين (م.ب)', 'Storage (MB)'), d.storageMb]];
  return (
    <div className="stack lg">
      <div className="grid c4">{stats.map(([t, v]) => <div key={t} className="card"><div className="muted small">{t}</div><div style={{ fontSize: 30, fontWeight: 700 }} className="ltr">{num(v)}</div></div>)}</div>
      <div className="card stack"><h3>{L('محركات التوليد', 'Generation engines')}</h3><div className="row wrap">{d.providers.map((p) => <span key={p.id} className={`badge ${p.demo ? 'demo' : p.configured ? 'ok' : ''}`}><span className="ltr">{p.label}</span> — {p.demo ? L('تجريبي', 'demo') : p.configured ? L('مهيأ', 'configured') : L('غير مهيأ', 'not configured')}</span>)}</div></div>
    </div>
  );
}

function Users() {
  const { L, num, date } = useI18n(); const { user: me } = useSession(); const toast = useToast();
  const [d, load] = useLoad('/admin/users'); const [busy, run] = useAction(); const [edit, setEdit] = useState(null); const [link, setLink] = useState(null);
  if (!d) return <Loading />;
  const patch = (u, body) => run(u.id, async () => { await api.patch(`/admin/users/${u.id}`, body); await load(); }, L('حُفظ', 'Saved'));
  return (
    <>
      <div className="table-wrap"><table>
        <thead><tr><th>{L('المستخدم', 'User')}</th><th>{L('الدور', 'Role')}</th><th>{L('الحالة', 'Status')}</th><th>{L('المشاريع', 'Projects')}</th><th>{L('توليد 24 س', 'Generated 24h')}</th><th>{L('آخر دخول', 'Last sign-in')}</th><th /></tr></thead>
        <tbody>{d.users.map((u) => (
          <tr key={u.id}>
            <td><b>{u.name}</b><div className="ltr small muted">{u.email}</div></td>
            <td><select className="select" style={{ minHeight: 36, paddingBlock: 4, width: 'auto' }} value={u.role} disabled={u.id === me.id || !!busy} onChange={(e) => patch(u, { role: e.target.value })} aria-label={L('الدور', 'Role')}><option value="user">{L('مستخدم', 'User')}</option><option value="admin">{L('مدير', 'Admin')}</option></select></td>
            <td><span className={`badge ${u.status === 'active' ? 'ok' : 'err'}`}>{u.status === 'active' ? L('نشط', 'Active') : L('موقوف', 'Disabled')}</span></td>
            <td className="ltr">{num(u.projects)}</td>
            <td className="ltr">{num(Math.round(u.usage.secondsToday))} / {num(u.limits.dailySeconds)}{u.customLimits && ' *'}</td>
            <td className="small">{u.lastLoginAt ? date(u.lastLoginAt) : '—'}</td>
            <td><div className="row" style={{ justifyContent: 'flex-end' }}>
              <Button className="sm ghost" onClick={() => setEdit({ ...u, form: { ...u.limits } })}>{L('الحدود', 'Limits')}</Button>
              <Button className="sm ghost" disabled={!!busy} onClick={() => run('link', async () => { const r = await api.post(`/admin/users/${u.id}/reset-link`); setLink({ user: u, url: location.origin + r.path, minutes: r.expiresInMinutes }); })}>{L('رابط استعادة', 'Reset link')}</Button>
              <Button className={`sm ghost ${u.status === 'active' ? 'danger' : ''}`} disabled={u.id === me.id || !!busy} onClick={() => patch(u, { status: u.status === 'active' ? 'disabled' : 'active' })}>{u.status === 'active' ? L('إيقاف', 'Disable') : L('تفعيل', 'Enable')}</Button>
            </div></td>
          </tr>
        ))}</tbody>
      </table></div>
      <p className="hint" style={{ marginTop: 8 }}>{L('* حدود خاصة بهذا المستخدم.', '* Limits set for this user only.')}</p>
      {edit && (
        <Modal title={L(`حدود ${edit.name}`, `Limits for ${edit.name}`)} onClose={() => setEdit(null)}>
          <div className="stack">
            {[['dailySeconds', L('ثواني التوليد اليومية', 'Daily generation seconds')], ['maxActiveProjects', L('مشاريع جارية في وقت واحد', 'Projects generating at once')], ['maxStorageMb', L('التخزين (م.ب)', 'Storage (MB)')]].map(([k, label]) => <Field key={k} label={label}><input className="input ltr" type="number" min="0" value={edit.form[k]} onChange={(e) => setEdit({ ...edit, form: { ...edit.form, [k]: e.target.value } })} /></Field>)}
            <div className="row" style={{ justifyContent: 'flex-end' }}>
              {edit.customLimits && <Button className="ghost" onClick={async () => { await patch(edit, { limits: null }); setEdit(null); }}>{L('العودة للحدود العامة', 'Use global limits')}</Button>}
              <Button className="primary" onClick={async () => { await patch(edit, { limits: edit.form }); setEdit(null); }}>{L('حفظ', 'Save')}</Button>
            </div>
          </div>
        </Modal>
      )}
      {link && (
        <Modal title={L('رابط استعادة كلمة المرور', 'Password reset link')} onClose={() => setLink(null)}>
          <div className="stack">
            <p className="muted small">{L(`سلّم هذا الرابط إلى ${link.user.name} بوسيلة آمنة. صالح ${link.minutes} دقيقة ولمرة واحدة، ولن يظهر مجددًا.`, `Give this link to ${link.user.name} through a secure channel. It is valid for ${link.minutes} minutes, works once, and will not be shown again.`)}</p>
            <input className="input ltr small" readOnly value={link.url} onFocus={(e) => e.target.select()} />
            <Button className="primary" icon="copy" onClick={() => copyText(link.url).then(() => toast(L('نُسخ الرابط', 'Link copied')))}>{L('نسخ الرابط', 'Copy link')}</Button>
          </div>
        </Modal>
      )}
    </>
  );
}

function Jobs() {
  const { L, date } = useI18n(); const [filter, setFilter] = useState('');
  const [d, load] = useLoad(`/admin/jobs?status=${filter}`); const [busy, run] = useAction();
  usePolling(load, 3000, true);
  const filters = [['', L('الكل', 'All')], ['active', L('الجارية', 'Active')], ['failed', L('الفاشلة', 'Failed')], ['succeeded', L('الناجحة', 'Succeeded')], ['canceled', L('الملغاة', 'Canceled')]];
  return (
    <div className="stack">
      <div className="chips">{filters.map(([k, t]) => <button key={k} className={`chip ${filter === k ? 'on' : ''}`} onClick={() => setFilter(k)} aria-pressed={filter === k}>{t}</button>)}</div>
      {!d ? <Loading /> : !d.jobs.length ? <div className="empty">{L('لا توجد مهام.', 'No jobs.')}</div> : (
        <div className="table-wrap"><table>
          <thead><tr><th>{L('المهمة', 'Job')}</th><th>{L('المشروع', 'Project')}</th><th>{L('المحرك', 'Engine')}</th><th>{L('الحالة', 'Status')}</th><th>{L('المحاولات', 'Attempts')}</th><th>{L('آخر تحديث', 'Updated')}</th><th /></tr></thead>
          <tbody>{d.jobs.map((j) => (
            <tr key={j.id}>
              <td>{j.type === 'assemble' ? L('تجميع الفيلم', 'Assemble film') : L(`مشهد ${j.scene ?? ''}`, `Scene ${j.scene ?? ''}`)}{j.providerJobId && <div className="ltr mono faint" style={{ maxWidth: 190, overflow: 'hidden', textOverflow: 'ellipsis' }}>{j.providerJobId}</div>}</td>
              <td><b>{j.projectTitle || '—'}</b><div className="ltr small muted">{j.userEmail}</div></td>
              <td className="ltr">{j.providerId || '—'}</td>
              <td><StatusBadge status={j.status} />{j.status === 'running' && j.progress > 0 && <span className="ltr small faint"> {Math.round(j.progress * 100)}%</span>}{j.error && <div className="ltr small" style={{ color: 'var(--err)', maxWidth: 300 }}>{j.error}</div>}</td>
              <td className="ltr">{j.attempts} / {j.maxAttempts}</td>
              <td className="small">{date(j.updatedAt)}</td>
              <td><div className="row" style={{ justifyContent: 'flex-end' }}>
                {['failed', 'canceled'].includes(j.status) && <Button className="sm ghost" icon="refresh" disabled={!!busy} onClick={() => run(j.id, async () => { await api.post(`/admin/jobs/${j.id}/retry`); await load(); })}>{L('إعادة', 'Retry')}</Button>}
                {['queued', 'running'].includes(j.status) && <Button className="sm ghost danger" icon="x" disabled={!!busy} onClick={() => run(j.id, async () => { await api.post(`/admin/jobs/${j.id}/cancel`); await load(); })}>{L('إلغاء', 'Cancel')}</Button>}
              </div></td>
            </tr>
          ))}</tbody>
        </table></div>
      )}
    </div>
  );
}

function ProviderCard({ p, onSaved }) {
  const { L } = useI18n(); const { loadMeta } = useSession(); const [busy, run] = useAction();
  const [vals, setVals] = useState({}); const [test, setTest] = useState(null);
  const dirty = Object.keys(vals).length > 0;
  const save = (body) => run('save', async () => { await api.put(`/admin/providers/${p.id}`, body); setVals({}); setTest(null); await onSaved(); loadMeta(); }, L('حُفظت الإعدادات', 'Settings saved'));
  const note = { sdk: L('محوّل مبني على SDK المزود الرسمي. لم يُختبر مع الخدمة الحية في هذه النسخة.', 'Adapter written from the provider’s official SDK. Not yet exercised against the live service in this build.'), unverified: L('محوّل تجريبي: تعذّر فتح توثيق المزود وقت كتابته. راجعه قبل الاعتماد عليه.', 'Experimental adapter: the provider’s documentation could not be opened when it was written. Review before relying on it.'), local: L('يعمل محليًا على الخادم ولا يتصل بأي مزود.', 'Runs locally on the server and calls no provider.') }[p.verified];
  return (
    <div className="card stack">
      <div className="row between wrap">
        <div className="row"><h3 className="ltr" style={{ margin: 0 }}>{p.label}</h3>{p.demo ? <DemoBadge /> : <span className={`badge ${p.configured ? 'ok' : ''}`}>{p.configured ? L('مهيأ', 'Configured') : L('غير مهيأ', 'Not configured')}</span>}{!p.enabled && <span className="badge err">{L('معطّل', 'Disabled')}</span>}</div>
        <label className="row small" style={{ cursor: 'pointer' }}><input type="checkbox" checked={p.enabled} disabled={!!busy} onChange={(e) => save({ enabled: e.target.checked })} style={{ accentColor: 'var(--accent)' }} />{L('متاح للمستخدمين', 'Available to users')}</label>
      </div>
      {note && <p className="hint">{note}</p>}
      {p.fields.length > 0 && (
        <div className="grid c2">
          {p.fields.map((f) => (
            <Field key={f.key} label={<><span className="ltr">{f.label}</span>{f.required ? ' *' : ''}</>} hint={f.set ? `${f.source === 'env' ? L('من متغيرات البيئة', 'From environment variables') : L('محفوظ مشفّرًا في قاعدة البيانات', 'Stored encrypted in the database')}: ${f.preview}` : null}>
              <input className="input ltr" type={f.secret ? 'password' : 'text'} autoComplete="off" placeholder={f.set ? L('اتركه فارغًا للإبقاء على القيمة الحالية', 'Leave empty to keep the current value') : f.placeholder} value={vals[f.key] ?? ''} onChange={(e) => { const v = { ...vals, [f.key]: e.target.value }; if (!e.target.value) delete v[f.key]; setVals(v); }} />
            </Field>
          ))}
        </div>
      )}
      {(p.fields.length > 0 || p.canTest) && (
        <div className="row wrap">
          {p.fields.length > 0 && <Button className="primary sm" busy={busy === 'save'} disabled={!dirty} onClick={() => save({ credentials: vals })}>{L('حفظ المفاتيح', 'Save keys')}</Button>}
          {p.canTest && <Button className="sm" icon="link" busy={busy === 'test'} disabled={!p.configured || dirty} onClick={() => run('test', async () => setTest(await api.post(`/admin/providers/${p.id}/test`)))}>{L('اختبار الاتصال', 'Test connection')}</Button>}
          {p.fields.some((f) => f.source === 'panel') && <Button className="sm ghost danger" disabled={!!busy} onClick={() => save({ credentials: Object.fromEntries(p.fields.map((f) => [f.key, ''])) })}>{L('حذف المفاتيح المحفوظة', 'Remove stored keys')}</Button>}
          {p.docsUrl && <a className="btn sm ghost ltr" href={p.docsUrl} target="_blank" rel="noreferrer">API docs</a>}
        </div>
      )}
      {test && <div className={`banner ${test.ok ? 'info' : 'err'}`}><Icon name={test.ok ? 'check' : 'alert'} /><span>{test.ok ? L('نجح الاتصال: ردّ المزود على طلب موثَّق.', 'Connection works: the provider answered an authenticated request.') : <>{L('فشل الاتصال: ', 'Connection failed: ')}<span className="ltr">{test.detail || test.error}</span></>}</span></div>}
      {p.qualities.length > 0 && (
        <details><summary className="small" style={{ color: 'var(--accent)' }}>{L('الإمكانيات المعروضة للمستخدم', 'Capabilities offered to users')}</summary>
          <div className="table-wrap" style={{ marginTop: 10 }}><table className="ltr"><thead><tr><th>Tier</th><th>Aspect</th><th>Clip (s)</th><th>Prompt</th><th>Image→video</th><th>Audio</th></tr></thead>
            <tbody>{p.qualities.map((q) => <tr key={q.id}><td>{q.label}</td><td>{q.aspects.join(', ')}</td><td>{q.clip.values ? q.clip.values.join(' / ') : `${q.clip.min}–${q.clip.max}`}</td><td>{q.maxPromptChars}</td><td>{q.imageToVideo ? 'yes' : q.imageByUrl ? 'needs PUBLIC_BASE_URL' : 'no'}</td><td>{q.nativeAudio ? 'native' : 'no'}</td></tr>)}</tbody></table></div>
        </details>
      )}
    </div>
  );
}

function Providers() {
  const { L } = useI18n(); const [d, load] = useLoad('/admin/providers');
  if (!d) return <Loading />;
  return (
    <div className="stack lg">
      <div className="banner info"><Icon name="shield" /><span>{L('المفاتيح تُحفظ على الخادم فقط (مشفّرة بـAES-256-GCM) ولا تُرسل إلى المتصفح أبدًا؛ الواجهة تعرض آخر 4 خانات فقط.', 'Keys are kept on the server only (encrypted with AES-256-GCM) and are never sent to the browser; the interface shows the last 4 characters only.')}</span></div>
      <h3>{L('مزودو الفيديو', 'Video providers')}</h3>
      {d.video.map((p) => <ProviderCard key={p.id} p={p} onSaved={load} />)}
      <h3>{L('مزودو الصوت', 'Audio providers')}</h3>
      {d.audio.map((p) => <ProviderCard key={p.id} p={p} onSaved={load} />)}
      <div className="card stack">
        <h3>{L('إعدادات تُضبط من متغيرات البيئة', 'Settings read from environment variables')}</h3>
        <dl className="kv">
          <dt>{L('المخرج الذكي (Claude)', 'AI director (Claude)')}</dt><dd>{d.aiDirector.configured ? <><span className="badge ok">{L('مفعّل', 'On')}</span> <span className="ltr small muted">{d.aiDirector.model}</span></> : <><span className="badge">{L('غير مفعّل', 'Off')}</span> <span className="small muted">{L('يُستخدم محرك القواعد المدمج. للتفعيل: ANTHROPIC_API_KEY', 'The built-in rule engine is used. To enable: ANTHROPIC_API_KEY')}</span></>}</dd>
          <dt>{L('العنوان العام للخادم', 'Public server address')}</dt><dd>{d.publicBaseUrl ? <span className="ltr">{d.publicBaseUrl}</span> : <span className="small muted">{L('غير مضبوط (PUBLIC_BASE_URL). لازم لمزودين يقرؤون الصور المرجعية عبر رابط.', 'Not set (PUBLIC_BASE_URL). Needed by providers that read reference images by URL.')}</span>}</dd>
        </dl>
      </div>
    </div>
  );
}

function Logs() {
  const { L, date } = useI18n(); const [level, setLevel] = useState(''); const [q, setQ] = useState('');
  const [d, load] = useLoad(`/admin/logs?level=${level}&q=${encodeURIComponent(q)}`);
  return (
    <div className="stack">
      <div className="row wrap">
        <div className="chips">{[['', L('الكل', 'All')], ['error', L('أخطاء', 'Errors')], ['warn', L('تحذيرات', 'Warnings')], ['info', L('عمليات', 'Operations')]].map(([k, t]) => <button key={k} className={`chip ${level === k ? 'on' : ''}`} onClick={() => setLevel(k)} aria-pressed={level === k}>{t}</button>)}</div>
        <input className="input" style={{ maxWidth: 260 }} type="search" value={q} placeholder={L('بحث…', 'Search…')} onChange={(e) => setQ(e.target.value)} aria-label={L('بحث', 'Search')} />
        <Button className="sm ghost" icon="refresh" onClick={() => load()}>{L('تحديث', 'Refresh')}</Button>
      </div>
      {!d ? <Loading /> : !d.logs.length ? <div className="empty">{L('لا توجد سجلات.', 'No log entries.')}</div> : (
        <div className="table-wrap"><table>
          <thead><tr><th>{L('الوقت', 'Time')}</th><th>{L('المستوى', 'Level')}</th><th>{L('الحدث', 'Event')}</th><th>{L('التفاصيل', 'Details')}</th></tr></thead>
          <tbody>{d.logs.map((l) => <tr key={l.id}><td className="small" style={{ whiteSpace: 'nowrap' }}>{date(l.ts)}</td><td><span className={`badge ${l.level === 'error' ? 'err' : l.level === 'warn' ? 'warn' : ''}`}>{l.level}</span></td><td className="ltr mono">{l.event}</td><td className="ltr small" style={{ wordBreak: 'break-word' }}>{l.message}{l.data && <div className="faint mono">{l.data}</div>}</td></tr>)}</tbody>
        </table></div>
      )}
    </div>
  );
}

function Settings() {
  const { L } = useI18n(); const [d, load] = useLoad('/admin/settings'); const [form, setForm] = useState(null); const [busy, run] = useAction();
  useEffect(() => { if (d) setForm({ ...d.limits, registrationOpen: d.registrationOpen }); }, [d]);
  if (!form) return <Loading />;
  return (
    <form className="card stack" style={{ maxWidth: 620 }} onSubmit={(e) => { e.preventDefault(); run('save', async () => { const { registrationOpen, ...limits } = form; await api.put('/admin/settings', { limits, registrationOpen }); await load(); }, L('حُفظت الإعدادات', 'Settings saved')); }}>
      <h3>{L('حدود الاستخدام العامة لكل مستخدم', 'Default usage limits per user')}</h3>
      {[['dailySeconds', L('ثواني التوليد خلال 24 ساعة', 'Generation seconds per 24 hours')], ['maxActiveProjects', L('مشاريع جارية في وقت واحد', 'Projects generating at once')], ['maxStorageMb', L('التخزين (م.ب)', 'Storage (MB)')]].map(([k, label]) => <Field key={k} label={label}><input className="input ltr" type="number" min="0" value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} /></Field>)}
      <label className="row" style={{ cursor: 'pointer' }}><input type="checkbox" checked={form.registrationOpen} onChange={(e) => setForm({ ...form, registrationOpen: e.target.checked })} style={{ accentColor: 'var(--accent)' }} />{L('التسجيل مفتوح لحسابات جديدة', 'Registration is open to new accounts')}</label>
      <div><Button type="submit" className="primary" busy={busy === 'save'}>{L('حفظ', 'Save')}</Button></div>
    </form>
  );
}

export default function Admin() {
  const { L } = useI18n(); const [sp, setSp] = useSearchParams(); const tab = sp.get('tab') || 'overview';
  const tabs = [['overview', L('نظرة عامة', 'Overview'), Overview], ['users', L('المستخدمون', 'Users'), Users], ['jobs', L('عمليات التوليد', 'Generation jobs'), Jobs], ['providers', L('مزودو الخدمة', 'Providers'), Providers], ['logs', L('سجل العمليات والأخطاء', 'Logs'), Logs], ['settings', L('الإعدادات', 'Settings'), Settings]];
  const Current = (tabs.find((t) => t[0] === tab) || tabs[0])[2];
  return (
    <div className="container">
      <div className="page-head"><div><h2>{L('لوحة تحكم المدير', 'Admin panel')}</h2><p>{L('المستخدمون، عمليات التوليد، مزودو الخدمة والسجلات.', 'Users, generation jobs, providers and logs.')}</p></div></div>
      <div className="tabs" role="tablist">{tabs.map(([k, t]) => <button key={k} role="tab" aria-selected={tab === k} className={`tab ${tab === k ? 'on' : ''}`} onClick={() => setSp(k === 'overview' ? {} : { tab: k })}>{t}</button>)}</div>
      <Current />
    </div>
  );
}
