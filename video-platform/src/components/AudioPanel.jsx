import { useEffect, useState } from 'react';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useSession } from '../session.jsx';
import { Field } from '../ui.jsx';
import { Icon } from '../icons.jsx';
import Uploader from './Uploader.jsx';

export const emptyAudio = () => {
  const t = (volume) => ({ mode: 'none', assetId: null, prompt: '', volume });
  return { music: t(0.5), voiceover: { ...t(1), language: 'ar', dialect: '', voiceId: '' }, sfx: t(0.7), ambience: t(0.4), clipAudioVolume: 1 };
};

/** Optional audio stage: music, effects, ambience and voice-over, each from a file, a service, or off. */
export default function AudioPanel({ value, onChange, files, onUploaded, nativeAudio }) {
  const { L } = useI18n(); const { meta } = useSession();
  const service = meta?.audio?.provider;
  const [voices, setVoices] = useState(null);
  const a = value || emptyAudio();
  const set = (k, patch) => onChange({ ...a, [k]: { ...a[k], ...patch } });
  useEffect(() => { if (service && a.voiceover.mode === 'generate' && !voices) api.get('/audio/voices').then((r) => setVoices(r.voices || [])).catch(() => setVoices([])); }, [service, a.voiceover.mode, voices]);

  const tracks = [
    ['music', 'music', L('الموسيقى التصويرية', 'Music'), L('مثال: موسيقى إلكترونية هادئة بإيقاع متصاعد', 'e.g. calm electronic score that builds')],
    ['sfx', 'volume', L('المؤثرات الصوتية', 'Sound effects'), L('مثال: هدير محرك، عجلات على أسفلت مبلل', 'e.g. engine roar, tyres on wet asphalt')],
    ['ambience', 'globe', L('أصوات البيئة المحيطة', 'Ambience'), L('مثال: مطر خفيف وضجيج مدينة بعيد', 'e.g. light rain and distant city hum')],
    ['voiceover', 'user', L('التعليق الصوتي', 'Voice-over'), L('نص التعليق كاملًا (أو اكتب سطرًا لكل مشهد في صفحة المخطط)', 'The full narration (or write a line per scene on the storyboard page)')],
  ];
  return (
    <div className="stack">
      {!service && <div className="banner info"><Icon name="info" /><span>{L('لا توجد خدمة صوت خارجية مهيأة على الخادم، لذلك المتاح هو رفع ملفاتك الصوتية. يمكن للمدير ربط خدمة صوت من لوحة التحكم.', 'No external audio service is configured on the server, so you can upload your own audio files. An administrator can connect an audio service from the admin panel.')}</span></div>}
      {nativeAudio && <div className="banner info"><Icon name="info" /><span>{L('المحرك المختار يولّد صوتًا مع الفيديو. وصف الموسيقى والمؤثرات والأجواء يُضاف إلى تعليمات كل مشهد.', 'The selected engine generates sound with the video. The music, effects and ambience descriptions are added to each scene’s instructions.')}</span></div>}
      {tracks.map(([k, icon, title, ph]) => {
        const t = a[k];
        return (
          <div key={k} className="card flat stack sm" style={{ padding: 16 }}>
            <div className="row wrap">
              <Icon name={icon} size={17} style={{ color: 'var(--accent)' }} /><b className="grow">{title}</b>
              <select className="select" style={{ width: 'auto', minHeight: 38, paddingBlock: 4 }} value={t.mode} onChange={(e) => set(k, { mode: e.target.value })} aria-label={title}>
                <option value="none">{L('بدون', 'None')}</option>
                <option value="upload">{L('ملف أرفعه', 'My own file')}</option>
                {service && service[k] && <option value="generate">{L('توليد عبر ', 'Generate with ')}{service.label}</option>}
              </select>
            </div>
            {t.mode === 'upload' && (
              <div className="row wrap">
                <select className="select grow" value={t.assetId || ''} onChange={(e) => set(k, { assetId: e.target.value || null })} aria-label={L('الملف الصوتي', 'Audio file')}>
                  <option value="">{L('اختر ملفًا من ملفاتك…', 'Choose one of your files…')}</option>
                  {(files || []).map((f) => <option key={f.id} value={f.id}>{f.filename}{f.duration ? ` (${Math.round(f.duration)}s)` : ''}</option>)}
                </select>
                <Uploader purpose="audio" compact onUploaded={(asset) => { onUploaded?.(asset); set(k, { assetId: asset.id }); }} />
              </div>
            )}
            {(k === 'voiceover' ? t.mode === 'generate' : t.mode !== 'upload') && (
              <textarea className="textarea" style={{ minHeight: 64 }} value={t.prompt} placeholder={ph} onChange={(e) => set(k, { prompt: e.target.value })} aria-label={title} />
            )}
            {k !== 'voiceover' && t.mode === 'none' && !nativeAudio && <span className="hint">{L('الوصف يُحفظ مع المشروع، ولا يُنتج صوتًا إلا إذا كان المحرك يولّد الصوت أو رُبطت خدمة صوت.', 'The description is saved with the project; it only produces sound when the engine generates audio or an audio service is connected.')}</span>}
            {k === 'voiceover' && t.mode !== 'none' && (
              <div className="grid c3">
                <Field label={L('اللغة', 'Language')}><select className="select" value={t.language} onChange={(e) => set(k, { language: e.target.value })}><option value="ar">{L('العربية', 'Arabic')}</option><option value="en">{L('الإنجليزية', 'English')}</option></select></Field>
                <Field label={L('اللهجة', 'Dialect')} hint={t.mode === 'generate' ? L('تُحفظ كملاحظة؛ اللهجة الفعلية يحددها النص والصوت المختار.', 'Saved as a note; the actual dialect comes from the text and the chosen voice.') : null}><input className="input" value={t.dialect} placeholder={L('مثال: فصحى، سعودية، مصرية', 'e.g. MSA, Saudi, Egyptian')} onChange={(e) => set(k, { dialect: e.target.value })} /></Field>
                {t.mode === 'generate' && <Field label={L('الصوت', 'Voice')}><select className="select" value={t.voiceId} onChange={(e) => set(k, { voiceId: e.target.value })}><option value="">{voices ? L('اختر صوتًا…', 'Choose a voice…') : L('جارٍ التحميل…', 'Loading…')}</option>{(voices || []).map((v) => <option key={v.id} value={v.id}>{v.name}{v.labels?.accent ? ` — ${v.labels.accent}` : ''}</option>)}</select></Field>}
              </div>
            )}
            {t.mode !== 'none' && <label className="row small muted"><span style={{ minWidth: 92 }}>{L('مستوى الصوت', 'Volume')} {Math.round(t.volume * 100)}%</span><input type="range" min="0" max="1" step="0.05" value={t.volume} onChange={(e) => set(k, { volume: Number(e.target.value) })} /></label>}
          </div>
        );
      })}
      {nativeAudio && <label className="row small muted"><span style={{ minWidth: 150 }}>{L('صوت المقاطع المولّدة', 'Generated clip audio')} {Math.round(a.clipAudioVolume * 100)}%</span><input type="range" min="0" max="1" step="0.05" value={a.clipAudioVolume} onChange={(e) => onChange({ ...a, clipAudioVolume: Number(e.target.value) })} /></label>}
    </div>
  );
}
