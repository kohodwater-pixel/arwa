import { useState } from 'react';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Button, Field, useAction } from '../ui.jsx';

export default function Account() {
  const { L, num, date, setLocale } = useI18n(); const { user, limits, usage, signIn } = useSession();
  const [name, setName] = useState(user.name); const [locale, setLoc] = useState(user.locale);
  const [pw, setPw] = useState({ current: '', next: '' }); const [busy, run] = useAction();
  const meter = (used, limit) => <div className="progress"><i style={{ width: `${limit ? Math.min(100, Math.round((used / limit) * 100)) : 0}%` }} /></div>;
  return (
    <div className="container narrow">
      <div className="page-head"><div><h2>{L('إعدادات الحساب', 'Account settings')}</h2><p className="ltr">{user.email}</p></div><span className={`badge ${user.role === 'admin' ? 'warn' : ''}`}>{user.role === 'admin' ? L('مدير', 'Administrator') : L('مستخدم', 'User')}</span></div>
      <div className="stack lg">
        <form className="card stack" onSubmit={(e) => { e.preventDefault(); run('profile', async () => { const r = await api.patch('/auth/profile', { name, locale }); signIn(r); setLocale(locale); }, L('حُفظ الملف الشخصي', 'Profile saved')); }}>
          <h3>{L('الملف الشخصي', 'Profile')}</h3>
          <div className="grid c2">
            <Field label={L('الاسم', 'Name')}><input className="input" value={name} onChange={(e) => setName(e.target.value)} /></Field>
            <Field label={L('لغة الواجهة', 'Interface language')}><select className="select" value={locale} onChange={(e) => setLoc(e.target.value)}><option value="ar">العربية</option><option value="en">English</option></select></Field>
          </div>
          <div className="row"><Button type="submit" className="primary" busy={busy === 'profile'}>{L('حفظ', 'Save')}</Button><span className="hint">{L('عضو منذ ', 'Member since ')}{date(user.createdAt)}</span></div>
        </form>

        <div className="card stack">
          <h3>{L('الاستخدام والحدود', 'Usage and limits')}</h3>
          {user.role === 'admin' && <p className="hint">{L('حساب المدير غير مقيّد بهذه الحدود.', 'Administrator accounts are not bound by these limits.')}</p>}
          <div className="stack sm"><div className="row between small"><span>{L('ثواني التوليد خلال آخر 24 ساعة', 'Seconds generated in the last 24 hours')}</span><span className="ltr">{num(Math.round(usage.secondsToday))} / {num(limits.dailySeconds)}</span></div>{meter(usage.secondsToday, limits.dailySeconds)}</div>
          <div className="stack sm"><div className="row between small"><span>{L('مشاريع قيد التوليد الآن', 'Projects generating now')}</span><span className="ltr">{num(usage.activeProjects)} / {num(limits.maxActiveProjects)}</span></div>{meter(usage.activeProjects, limits.maxActiveProjects)}</div>
          <div className="stack sm"><div className="row between small"><span>{L('التخزين (م.ب)', 'Storage (MB)')}</span><span className="ltr">{num(usage.storageMb)} / {num(limits.maxStorageMb)}</span></div>{meter(usage.storageMb, limits.maxStorageMb)}</div>
          <p className="hint">{L('الوضع التجريبي لا يُحتسب من ثواني التوليد.', 'Demo mode does not count against generation seconds.')}</p>
        </div>

        <form className="card stack" onSubmit={(e) => { e.preventDefault(); run('pw', async () => { await api.post('/auth/password', pw); setPw({ current: '', next: '' }); }, L('تم تغيير كلمة المرور', 'Password changed')); }}>
          <h3>{L('كلمة المرور', 'Password')}</h3>
          <div className="grid c2">
            <Field label={L('الحالية', 'Current')}><input className="input ltr" type="password" autoComplete="current-password" value={pw.current} onChange={(e) => setPw({ ...pw, current: e.target.value })} /></Field>
            <Field label={L('الجديدة', 'New')} hint={L('8 أحرف على الأقل. تُسجَّل خروج الأجهزة الأخرى.', 'At least 8 characters. Other devices are signed out.')}><input className="input ltr" type="password" autoComplete="new-password" value={pw.next} onChange={(e) => setPw({ ...pw, next: e.target.value })} /></Field>
          </div>
          <div><Button type="submit" busy={busy === 'pw'} disabled={!pw.current || pw.next.length < 8}>{L('تغيير كلمة المرور', 'Change password')}</Button></div>
        </form>
      </div>
    </div>
  );
}
