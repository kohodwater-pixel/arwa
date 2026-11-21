import { useState } from 'react';
import { Routes, Route, NavLink, Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useI18n } from './i18n.jsx';
import { useSession } from './session.jsx';
import { Icon } from './icons.jsx';
import { Loading, Button } from './ui.jsx';
import Home from './pages/Home.jsx';
import { Login, Register, Forgot, Reset } from './pages/Auth.jsx';
import Create from './pages/Create.jsx';
import Storyboard from './pages/Storyboard.jsx';
import Generate from './pages/Generate.jsx';
import Library from './pages/Library.jsx';
import Project from './pages/Project.jsx';
import Account from './pages/Account.jsx';
import Admin from './pages/Admin.jsx';
import Share from './pages/Share.jsx';

function Guard({ children, admin }) {
  const { user, loading } = useSession(); const loc = useLocation();
  if (loading) return <Loading />;
  if (!user) return <Navigate to="/login" replace state={{ from: loc.pathname + loc.search }} />;
  if (admin && user.role !== 'admin') return <Navigate to="/library" replace />;
  return children;
}

function Nav() {
  const { L, locale, setLocale } = useI18n(); const { user, signOut, meta } = useSession();
  const [open, setOpen] = useState(false); const nav = useNavigate();
  const close = () => setOpen(false);
  return (
    <header className="nav">
      <div className="container">
        <Link to="/" className="brand"><span className="brand-mark"><Icon name="film" size={17} /></span><span className="ltr">{meta?.appName || 'Mashhad Studio'}</span></Link>
        {user && (
          <nav className={`nav-links ${open ? 'open' : ''}`} onClick={close}>
            <NavLink to="/create">{L('إنشاء فيديو', 'Create')}</NavLink>
            <NavLink to="/library">{L('مكتبة المشاريع', 'Library')}</NavLink>
            <NavLink to="/account">{L('الحساب', 'Account')}</NavLink>
            {user.role === 'admin' && <NavLink to="/admin">{L('لوحة المدير', 'Admin')}</NavLink>}
          </nav>
        )}
        <span className="spacer" />
        <button className="btn ghost sm" onClick={() => setLocale(locale === 'ar' ? 'en' : 'ar')} aria-label="language"><Icon name="globe" size={16} />{locale === 'ar' ? 'English' : 'العربية'}</button>
        {user ? (
          <>
            <Button className="ghost sm hide-sm" icon="logout" flip onClick={async () => { await signOut(); nav('/'); }}>{L('خروج', 'Sign out')}</Button>
            <button className="btn ghost icon nav-toggle" onClick={() => setOpen(!open)} aria-label="menu"><Icon name="menu" /></button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn ghost sm hide-sm">{L('دخول', 'Sign in')}</Link>
            <Link to="/register" className="btn primary sm">{L('حساب جديد', 'Sign up')}</Link>
          </>
        )}
      </div>
    </header>
  );
}

export default function App() {
  const { L } = useI18n(); const { metaError, loadMeta } = useSession(); const loc = useLocation();
  if (loc.pathname.startsWith('/watch/')) return <Routes><Route path="/watch/:token" element={<Share />} /></Routes>;
  return (
    <div className="app">
      <Nav />
      {metaError && <div className="container" style={{ marginTop: 16 }}><div className="banner err"><Icon name="alert" /><span className="grow">{L('تعذّر الاتصال بالخادم.', 'The server cannot be reached.')}</span><Button className="sm" onClick={loadMeta}>{L('إعادة المحاولة', 'Retry')}</Button></div></div>}
      <main key={loc.pathname}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot" element={<Forgot />} />
          <Route path="/reset" element={<Reset />} />
          <Route path="/create" element={<Guard><Create /></Guard>} />
          <Route path="/library" element={<Guard><Library /></Guard>} />
          <Route path="/projects/:id" element={<Guard><Project /></Guard>} />
          <Route path="/projects/:id/storyboard" element={<Guard><Storyboard /></Guard>} />
          <Route path="/projects/:id/generate" element={<Guard><Generate /></Guard>} />
          <Route path="/account" element={<Guard><Account /></Guard>} />
          <Route path="/admin" element={<Guard admin><Admin /></Guard>} />
          <Route path="*" element={<div className="container"><div className="empty"><h3>{L('الصفحة غير موجودة', 'Page not found')}</h3><p style={{ marginTop: 12 }}><Link className="btn" to="/">{L('الرئيسية', 'Home')}</Link></p></div></div>} />
        </Routes>
      </main>
      <footer className="foot"><div className="container row between wrap"><span className="ltr">© {new Date().getFullYear()} Mashhad Studio</span><span>{L('مفاتيح مزودي التوليد محفوظة على الخادم فقط.', 'Provider keys are kept on the server only.')}</span></div></footer>
    </div>
  );
}
