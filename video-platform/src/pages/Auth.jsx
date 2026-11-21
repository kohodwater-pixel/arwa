import { useState } from 'react';
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Button, Field } from '../ui.jsx';
import { Icon } from '../icons.jsx';

function Shell({ title, sub, children, onSubmit, error }) {
  return (
    <div className="container">
      <form className="card pad-lg auth stack" onSubmit={(e) => { e.preventDefault(); onSubmit(); }} noValidate>
        <div><h2>{title}</h2>{sub && <p className="muted small">{sub}</p>}</div>
        {error && <div className="banner err" role="alert"><Icon name="alert" /><span>{error}</span></div>}
        {children}
      </form>
    </div>
  );
}

function useForm(fn) {
  const { err } = useI18n(); const [busy, setBusy] = useState(false); const [error, setError] = useState('');
  const submit = async () => { setBusy(true); setError(''); try { await fn(); } catch (e) { setError(err(e)); } finally { setBusy(false); } };
  return { busy, error, submit };
}

export function Login() {
  const { L } = useI18n(); const { signIn } = useSession(); const nav = useNavigate(); const loc = useLocation();
  const [f, setF] = useState({ email: '', password: '' });
  const form = useForm(async () => { signIn(await api.post('/auth/login', f)); nav(loc.state?.from || '/create', { replace: true }); });
  return (
    <Shell title={L('تسجيل الدخول', 'Sign in')} onSubmit={form.submit} error={form.error}>
      <Field label={L('البريد الإلكتروني', 'E-mail')}><input className="input ltr" type="email" autoComplete="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} required /></Field>
      <Field label={L('كلمة المرور', 'Password')}><input className="input ltr" type="password" autoComplete="current-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required /></Field>
      <Button type="submit" className="primary block" busy={form.busy}>{L('دخول', 'Sign in')}</Button>
      <div className="row between small"><Link to="/forgot" className="muted">{L('نسيت كلمة المرور؟', 'Forgot your password?')}</Link><Link to="/register" style={{ color: 'var(--accent)' }}>{L('حساب جديد', 'Create an account')}</Link></div>
    </Shell>
  );
}

export function Register() {
  const { L, locale } = useI18n(); const { signIn } = useSession(); const nav = useNavigate();
  const [f, setF] = useState({ name: '', email: '', password: '' });
  const form = useForm(async () => { signIn(await api.post('/auth/register', { ...f, locale })); nav('/create', { replace: true }); });
  return (
    <Shell title={L('حساب جديد', 'Create an account')} sub={L('مشاريعك وملفاتك محفوظة في حسابك وحدك.', 'Your projects and files stay in your own account.')} onSubmit={form.submit} error={form.error}>
      <Field label={L('الاسم', 'Name')}><input className="input" autoComplete="name" value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} required /></Field>
      <Field label={L('البريد الإلكتروني', 'E-mail')}><input className="input ltr" type="email" autoComplete="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} required /></Field>
      <Field label={L('كلمة المرور', 'Password')} hint={L('8 أحرف على الأقل.', 'At least 8 characters.')}><input className="input ltr" type="password" autoComplete="new-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required /></Field>
      <Button type="submit" className="primary block" busy={form.busy}>{L('إنشاء الحساب', 'Create account')}</Button>
      <div className="small center muted">{L('لديك حساب؟ ', 'Already have an account? ')}<Link to="/login" style={{ color: 'var(--accent)' }}>{L('سجّل الدخول', 'Sign in')}</Link></div>
    </Shell>
  );
}

export function Forgot() {
  const { L } = useI18n(); const [email, setEmail] = useState(''); const [sent, setSent] = useState(false);
  const form = useForm(async () => { await api.post('/auth/forgot', { email }); setSent(true); });
  return (
    <Shell title={L('استعادة كلمة المرور', 'Reset your password')} onSubmit={form.submit} error={form.error}>
      {sent ? (
        <div className="banner info"><Icon name="info" /><span>{L('سُجّل طلبك. هذا الخادم غير مربوط بخدمة بريد، لذلك لن تصلك رسالة: تواصل مع مدير المنصة ليعطيك رابط الاستعادة (صالح لساعة واحدة).', 'Your request was recorded. This server is not connected to an e-mail service, so no message will arrive: ask the platform administrator for your reset link (valid for one hour).')}</span></div>
      ) : (
        <>
          <Field label={L('البريد الإلكتروني', 'E-mail')}><input className="input ltr" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></Field>
          <Button type="submit" className="primary block" busy={form.busy}>{L('طلب رابط الاستعادة', 'Request a reset link')}</Button>
        </>
      )}
      <Link to="/login" className="small muted center">{L('العودة لتسجيل الدخول', 'Back to sign in')}</Link>
    </Shell>
  );
}

export function Reset() {
  const { L } = useI18n(); const [sp] = useSearchParams(); const nav = useNavigate();
  const [password, setPassword] = useState(''); const [done, setDone] = useState(false);
  const form = useForm(async () => { await api.post('/auth/reset', { token: sp.get('token'), password }); setDone(true); setTimeout(() => nav('/login'), 1800); });
  return (
    <Shell title={L('كلمة مرور جديدة', 'New password')} onSubmit={form.submit} error={form.error}>
      {done ? <div className="banner info"><Icon name="check" /><span>{L('تم تغيير كلمة المرور. جارٍ تحويلك لتسجيل الدخول…', 'Password changed. Taking you to sign in…')}</span></div> : (
        <>
          <Field label={L('كلمة المرور الجديدة', 'New password')} hint={L('8 أحرف على الأقل.', 'At least 8 characters.')}><input className="input ltr" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} required /></Field>
          <Button type="submit" className="primary block" busy={form.busy}>{L('حفظ', 'Save')}</Button>
        </>
      )}
    </Shell>
  );
}
