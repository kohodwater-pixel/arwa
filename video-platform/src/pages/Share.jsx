import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { Icon } from '../icons.jsx';
import { Loading, Player } from '../ui.jsx';

/** Public watch page for a shared project (no account needed). */
export default function Share() {
  const { token } = useParams(); const { L, num } = useI18n();
  const [data, setData] = useState(null); const [missing, setMissing] = useState(false);
  useEffect(() => { api.get(`/share/${token}`).then(setData).catch(() => setMissing(true)); }, [token]);
  return (
    <div className="app">
      <header className="nav"><div className="container"><Link to="/" className="brand"><span className="brand-mark"><Icon name="film" size={17} /></span><span className="ltr">{data?.appName || 'Mashhad Studio'}</span></Link></div></header>
      <main><div className="container narrow stack lg">
        {missing ? <div className="empty"><Icon name="link" size={30} /><h3>{L('هذا الرابط غير متاح', 'This link is not available')}</h3><p className="small">{L('ربما أوقف صاحب المشروع المشاركة.', 'The owner may have turned sharing off.')}</p></div> : !data ? <Loading /> : (
          <>
            <Player src={data.videoUrl} aspect={data.aspect} isDemo={data.isDemo} downloadUrl={`${data.videoUrl}?download=1`} />
            <div><h2>{data.title}</h2><p className="muted">{num(data.duration)} {L('ثانية', 'seconds')} · <span className="ltr">{data.aspect}</span></p></div>
            {data.isDemo && <div className="banner demo"><Icon name="alert" /><span>{L('فيديو من الوضع التجريبي: بطاقات بديلة وليست فيديو مولّدًا بالذكاء الاصطناعي.', 'A demo-mode video: placeholder cards, not AI-generated video.')}</span></div>}
          </>
        )}
      </div></main>
    </div>
  );
}
