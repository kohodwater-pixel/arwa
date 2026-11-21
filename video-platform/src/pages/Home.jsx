import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button } from '../ui.jsx';

export default function Home() {
  const { L } = useI18n(); const { user, meta } = useSession(); const nav = useNavigate();
  const [text, setText] = useState('');
  const example = L('مشهد سينمائي لسيارة رياضية سوداء تسير وسط شوارع طوكيو الممطرة ليلًا، انعكاسات النيون على الأرض، حركة كاميرا احترافية، إضاءة درامية، واقعية فائقة.',
    'A cinematic shot of a black sports car driving through the rainy streets of Tokyo at night, neon reflections on the ground, professional camera movement, dramatic lighting, hyper-realistic.');
  const go = () => { try { sessionStorage.setItem('draft-description', text || example); } catch { /* ignore */ } nav(user ? '/create' : '/register'); };
  const real = (meta?.providers || []).filter((p) => !p.demo);
  const connected = real.filter((p) => p.configured);

  const features = [
    ['camera', L('محرك إخراج سينمائي', 'Cinematic engine'), L('لا يُرسل وصفك كما هو. يُحلَّل أولًا ويُحوَّل إلى قرارات تصوير: حركة الكاميرا، العدسة، الإضاءة، تدريج الألوان وقواعد الاستمرارية.', 'Your description is never sent as is. It is analysed and turned into shooting decisions: camera movement, lens, lighting, colour grade and continuity rules.')],
    ['layers', L('مخطط مشاهد قابل للتعديل', 'Editable storyboard'), L('شاهد خطة المشاهد قبل التوليد: عدّل الوصف والمدة وحركة الكاميرا، أعد ترتيب المشاهد، أو اطلب صياغة بديلة لمشهد واحد.', 'See the scene plan before anything is generated: edit descriptions, durations and camera moves, reorder scenes, or ask for another take on one scene.')],
    ['link', L('استمرارية بين المشاهد', 'Continuity between scenes'), L('كل مشهد يحمل الوصف نفسه للشخصيات والموقع والألوان، ويمكن بدء كل مشهد من آخر إطار في المشهد الذي قبله عندما يدعم المحرك ذلك.', 'Every scene carries the same description of characters, location and colour, and each scene can start from the last frame of the previous one when the engine supports it.')],
    ['cog', L('محركات توليد متعددة', 'Several generation engines'), L('بنية محوّلات مستقلة لكل مزود. الخيارات المعروضة (المدة، الأبعاد، الجودة) هي ما يدعمه المحرك المتصل فعلًا.', 'A separate adapter per provider. The options you see (duration, aspect ratio, quality) are the ones the connected engine really supports.')],
    ['music', L('صوت وموسيقى', 'Sound and music'), L('موسيقى ومؤثرات وتعليق صوتي بملفاتك، أو عبر خدمة صوت مرخّصة عند ربطها، مع مزامنة التعليق مع بداية كل مشهد.', 'Music, effects and voice-over from your own files, or through a licensed audio service once connected, with voice-over synced to the start of each scene.')],
    ['grid', L('مكتبة مشاريع', 'Project library'), L('مشاريعك ومسوداتك وملفاتك المرجعية في مكان واحد: مشاهدة، تحميل، نسخ، إعادة توليد ومشاركة برابط.', 'Projects, drafts and reference files in one place: watch, download, duplicate, regenerate and share by link.')],
  ];
  const steps = [
    [L('اكتب الفكرة', 'Write the idea'), L('وصف بسيط بلغتك، مع نوع الفيديو والمدة والأبعاد.', 'A simple description in your language, with the video type, duration and aspect ratio.')],
    [L('راجع الإخراج', 'Review the direction'), L('المنصة تبني التصور الإخراجي وتقسّمه إلى مشاهد تعدّلها أو تعتمدها.', 'The platform builds the treatment and splits it into scenes you edit or approve.')],
    [L('ولّد وتابع', 'Generate and follow'), L('تُرسل المشاهد إلى المحرك في الخلفية وتتابع تقدم كل مشهد.', 'Scenes go to the engine in the background and you follow each one.')],
    [L('استلم الفيلم', 'Receive the film'), L('تُجمع المشاهد مع الصوت في فيديو واحد للمشاهدة والتحميل.', 'Scenes and sound are assembled into one video to watch and download.')],
  ];

  return (
    <div className="container stack lg">
      <section className="hero">
        <div className="eyebrow"><Icon name="spark" size={16} />{L('من الوصف إلى فيلم بمشاهد', 'From a description to a film in scenes')}</div>
        <h1>{L('اكتب الفكرة. نحوّلها إلى إخراج سينمائي.', 'Write the idea. We turn it into cinema.')}</h1>
        <p className="lead">{L('منصة تحوّل الوصف النصي إلى تصور إخراجي ومخطط مشاهد، ثم تولّد الفيديو عبر محرك التوليد المتصل وتجمعه مع الصوت.', 'A platform that turns a text description into a director’s treatment and a storyboard, then generates the video through the connected engine and assembles it with sound.')}</p>
        <div className="prompt-box">
          <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder={example} aria-label={L('وصف الفيديو', 'Video description')} />
          <div className="bar">
            <span className="hint grow">{L('اتركه فارغًا لتجربة المثال.', 'Leave it empty to try the example.')}</span>
            <Button className="primary lg" icon="spark" onClick={go}>{L('إنشاء فيديو', 'Create video')}</Button>
          </div>
        </div>
      </section>

      {meta && (
        <div className={`banner ${connected.length ? 'info' : 'warn'}`}>
          <Icon name={connected.length ? 'check' : 'alert'} />
          <div>
            {connected.length
              ? <>{L('محركات التوليد المتصلة: ', 'Connected generation engines: ')}<b className="ltr">{connected.map((p) => p.label).join(' · ')}</b></>
              : <>{L('لا يوجد محرك توليد حقيقي متصل بهذا الخادم بعد. المتاح الآن هو الوضع التجريبي فقط: يُظهر مسار العمل كاملًا ببطاقات بديلة موسومة بوضوح، ولا يولّد فيديو بالذكاء الاصطناعي.', 'No real generation engine is connected to this server yet. Only demo mode is available: it shows the whole workflow with clearly labelled placeholder cards and does not generate AI video.')}</>}
            {!!real.length && <div className="hint" style={{ marginTop: 4 }}>{L('المحوّلات الجاهزة للربط: ', 'Adapters ready to connect: ')}<span className="ltr">{real.map((p) => p.label).join(' · ')}</span></div>}
          </div>
        </div>
      )}

      <section className="grid c3">
        {features.map(([icon, title, body]) => <div key={title} className="card feature"><Icon name={icon} size={24} /><h3>{title}</h3><p>{body}</p></div>)}
      </section>

      <section className="stack">
        <h2>{L('كيف تعمل', 'How it works')}</h2>
        <div className="grid c4 steps">{steps.map(([t, b]) => <div key={t} className="card"><h3>{t}</h3><p className="muted small" style={{ marginTop: 6 }}>{b}</p></div>)}</div>
      </section>

      <section className="card pad-lg row between wrap">
        <div><h2>{L('ابدأ مشروعك الأول', 'Start your first project')}</h2><p className="muted">{L('من الفكرة إلى مخطط المشاهد في أقل من دقيقة.', 'From the idea to a storyboard in under a minute.')}</p></div>
        <Link className="btn primary lg" to={user ? '/create' : '/register'}>{user ? L('إنشاء فيديو', 'Create video') : L('إنشاء حساب', 'Create an account')}<Icon name="arrow" flip /></Link>
      </section>
    </div>
  );
}
