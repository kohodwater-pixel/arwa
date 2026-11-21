import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Icon } from '../icons.jsx';
import { Button, copyText, useToast } from '../ui.jsx';

/** The director's reading of the brief: camera, lighting, colour, quality, continuity, and why. */
export default function Treatment({ t, compact }) {
  const { L, locale } = useI18n(); const { meta } = useSession(); const toast = useToast();
  if (!t) return null;
  const moves = (meta?.cameraMoves || []).filter((m) => t.camera.preferred.includes(m.id)).map((m) => m.en);
  const style = (meta?.styles || []).find((s) => s.id === t.styleId);
  const rows = [
    ['camera', L('التصوير والكاميرا', 'Camera'), [t.camera.lens, t.camera.angle, t.camera.depthOfField, t.camera.slowMotion && 'Slow Motion', ...moves].filter(Boolean)],
    ['sun', L('الإضاءة', 'Lighting'), [t.lighting.scheme, ...t.lighting.details]],
    ['palette', L('الألوان والمظهر', 'Colour and look'), [t.color.grade, t.color.filmLook, t.color.grain && 'Film Grain'].filter(Boolean)],
    ['spark', L('جودة الصورة', 'Image quality'), t.quality],
    ['link', L('الاستمرارية بين المشاهد', 'Continuity'), t.continuity],
  ];
  return (
    <div className="stack">
      <div className="row wrap">
        <span className={`badge ${t.engine === 'ai' ? 'ok' : 'info'}`}>{t.engine === 'ai' ? L('المخرج: ذكاء اصطناعي (Claude)', 'Director: AI (Claude)') : L('المخرج: محرك القواعد المدمج', 'Director: built-in rule engine')}</span>
        {style && <span className="badge">{L('الأسلوب: ', 'Style: ')}{locale === 'ar' ? style.ar : style.en}</span>}
        {t.elements?.length > 0 && <span className="badge ltr">{t.elements.slice(0, 4).join(' · ')}</span>}
      </div>
      {t.aiError && <div className="banner warn"><Icon name="alert" /><span>{L('تعذّر استخدام المخرج الذكي لهذا المشروع، فاستُخدم محرك القواعد المدمج.', 'The AI director could not be used for this project, so the built-in rule engine was used.')}</span></div>}
      <div className={compact ? 'stack sm' : 'grid c2'}>
        {rows.map(([icon, title, items]) => (
          <div key={title} className="card flat" style={{ padding: 16 }}>
            <div className="row" style={{ marginBottom: 8, color: 'var(--accent)' }}><Icon name={icon} size={17} /><b style={{ color: 'var(--text)', fontSize: 14.5 }}>{title}</b></div>
            <ul className="ltr small muted" style={{ margin: 0, paddingInlineStart: 18 }}>{items.map((x, i) => <li key={i}>{x}</li>)}</ul>
          </div>
        ))}
      </div>
      {t.rationale?.length > 0 && (
        <div className="small muted">
          <b style={{ color: 'var(--text)' }}>{L('لماذا هذه القرارات؟', 'Why these decisions?')}</b>
          <ul style={{ margin: '6px 0 0', paddingInlineStart: 20 }}>{t.rationale.map((r, i) => <li key={i}>{locale === 'ar' ? r.ar : r.en}</li>)}</ul>
        </div>
      )}
      {t.masterPrompt && (
        <details>
          <summary className="row" style={{ color: 'var(--accent)', fontWeight: 600, fontSize: 14.5 }}><Icon name="film" size={16} />Cinematic Production Prompt</summary>
          <div className="pre mono ltr" style={{ marginTop: 10 }}>{t.masterPrompt}</div>
          <Button className="sm ghost" icon="copy" onClick={() => copyText(t.masterPrompt).then(() => toast(L('نُسخ البرومبت', 'Prompt copied')))} style={{ marginTop: 8 }}>{L('نسخ', 'Copy')}</Button>
        </details>
      )}
    </div>
  );
}
