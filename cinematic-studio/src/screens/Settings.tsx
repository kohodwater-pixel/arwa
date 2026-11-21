import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDate, errText } from '../lib/i18n';
import { rpc, pickFiles } from '../lib/rpc';
import { Btn, Slate, Panel, Note, Field, Input, Row, Confirm, Tag } from '../lib/ui';

export default function Settings() {
  const st = useStudio();
  const s = st.status.settings;
  const [url, setUrl] = useState(s.comfy_url || '');
  const [token, setToken] = useState('');
  const [name, setName] = useState(s.operator_name || '');
  const [comfy, setComfy] = useState<any | null>(null);
  const [testing, setTesting] = useState(false);
  const [log, setLog] = useState<any[] | null>(null);
  const [move, setMove] = useState<string | null>(null);
  const setting = async (key: string, value: string, ok?: string) => { const r = await st.run(() => rpc('setting_set', { key, value }), ok); if (r) await st.refreshStatus(); return r; };
  const test = async () => { setTesting(true); setComfy(await rpc('comfy_status').catch((e) => ({ configured: true, connected: false, error: e }))); setTesting(false); };
  useEffect(() => { if (s.comfy_url) test(); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const insecure = /^http:\/\//i.test(url) && !/^http:\/\/(localhost|127\.0\.0\.1|\[::1\])(:|\/|$)/i.test(url);

  return (
    <Slate title={L('الإعدادات', 'Settings')}>
      <div className="grid grid-cols-2 gap-6 items-start">
        <div className="space-y-6">
          <Panel title={L('خادم ComfyUI', 'ComfyUI server')} right={comfy ? <Tag status={comfy.connected ? 'ready' : comfy.configured ? 'failed' : undefined}>{comfy.connected ? L('متصل', 'Connected') : comfy.configured ? L('غير متصل', 'Not connected') : L('غير مضبوط', 'Not configured')}</Tag> : undefined}>
            <Field label={L('عنوان الخادم', 'Server address')} hint={L('يجب أن يكون https://. يُسمح بـ http فقط لخادم على هذا الجهاز.', 'Must be https://. Plain http is allowed only for a server on this computer.')}><div className="flex gap-2"><Input data-field="comfy_url" className="ltr" value={url} placeholder="https://your-pod-8188.proxy.example" onChange={(e) => setUrl(e.target.value)} /><Btn data-action="save-comfy" disabled={insecure} onClick={async () => { if (await setting('comfy_url', url.trim(), L('حُفظ العنوان', 'Address saved'))) test(); }}>{L('حفظ', 'Save')}</Btn></div></Field>
            {insecure && <div className="mt-3"><Note tone="bad">{L('لن يُحفظ عنوان http لخادم بعيد: الاتصال غير مشفَّر.', 'An http address for a remote server will not be saved: the connection is not encrypted.')}</Note></div>}
            <Field className="mt-4" label={L('رمز الدخول (Bearer token)', 'Access token (Bearer)')} hint={st.status.comfy_token_stored ? L(`رمز محفوظ في ${st.status.secret_backend}.`, `A token is stored in ${st.status.secret_backend}.`) : L('ضع أمام ComfyUI وكيلًا يطلب هذا الرمز. لا تفتح ComfyUI للعامة بلا مصادقة.', 'Put a proxy in front of ComfyUI that requires this token. Never expose ComfyUI publicly without authentication.')}>
              <div className="flex gap-2"><Input className="ltr" type="password" autoComplete="off" value={token} placeholder={st.status.comfy_token_stored ? '••••••••••••' : ''} onChange={(e) => setToken(e.target.value)} /><Btn disabled={token.length < 8} onClick={async () => { await st.run(() => rpc('secret_set', { name: 'comfy_token', value: token }), L('حُفظ الرمز', 'Token stored')); setToken(''); await st.refreshStatus(); test(); }}>{L('حفظ', 'Save')}</Btn>{st.status.comfy_token_stored && <Btn tone="ghost" onClick={async () => { await st.run(() => rpc('secret_delete', { name: 'comfy_token' })); st.refreshStatus(); }}>{L('حذف', 'Delete')}</Btn>}</div>
            </Field>
            <div className="mt-4 flex gap-2"><Btn data-action="test-comfy" onClick={test} disabled={testing || !s.comfy_url}>{testing ? L('يختبر…', 'Testing…') : L('اختبر الاتصال', 'Test connection')}</Btn></div>
            {comfy && !comfy.connected && comfy.configured && <div className="mt-3"><Note tone="bad"><span data-comfy-error className="selectable">{errText(comfy.error)}</span></Note></div>}
            {comfy?.connected && <div className="mt-3" data-comfy-ok><Row k="ComfyUI" v={<span className="ltr">{comfy.system.comfyui_version || '—'}</span>} /><Row k={L('الجهاز', 'Device')} v={<span className="ltr">{comfy.system.device}</span>} /><Row k="VRAM" v={<span className="num">{(comfy.system.vram_free / 2 ** 30).toFixed(1)} / {(comfy.system.vram_total / 2 ** 30).toFixed(1)} GB</span>} /><Row k={L('النماذج الجاهزة', 'Models ready')} v={<span className="num">{comfy.models.filter((m: any) => m.ready).length} / {comfy.models.length}</span>} /></div>}
          </Panel>
          <Panel title={L('المشغّل', 'Operator')}>
            <Field label={L('اسمك (يظهر في سجل الموافقات)', 'Your name (shown in the approvals log)')}><div className="flex gap-2"><Input value={name} onChange={(e) => setName(e.target.value)} /><Btn onClick={() => setting('operator_name', name, L('حُفظ', 'Saved'))}>{L('حفظ', 'Save')}</Btn></div></Field>
          </Panel>
        </div>
        <div className="space-y-6">
          <Panel title={L('مكتبة المشاريع', 'Project library')}>
            <Row k={L('الموقع الحالي', 'Current location')} v={<span className="ltr text-xs" data-library-root>{st.status.library_root}</span>} />
            <Row k={L('المحتوى', 'Contains')} v={<span className="ltr text-xs">Projects · Assets · Models · Cache · Logs · Backups</span>} />
            <Row k={L('المشاريع', 'Projects')} v={<span className="num">{st.status.counts.projects}</span>} />
            <div className="mt-4 flex gap-2 flex-wrap"><Btn onClick={() => st.run(() => rpc('reveal', { path: st.status.library_root }))}>{L('افتح المجلد', 'Open folder')}</Btn><Btn data-action="change-library" onClick={async () => { const [p] = await pickFiles({ directory: true, title: L('مجلد المكتبة', 'Library folder') }); if (p) setMove(p); }}>{L('غيّر الموقع', 'Change location')}</Btn></div>
            <p className="text-xs text-mute mt-3">{L('الفيديوهات تُحفظ ملفات داخل مجلدات المشاريع. قاعدة البيانات تحفظ المسارات والبيانات الوصفية فقط.', 'Videos are stored as files in the project folders. The database holds only paths and metadata.')}</p>
          </Panel>
          <Panel title="FFmpeg">
            {st.status.ffmpeg ? <><Row k="ffmpeg" v={<span className="ltr text-xs">{st.status.ffmpeg.ffmpeg}</span>} /><Row k="ffprobe" v={<span className="ltr text-xs">{st.status.ffmpeg.ffprobe}</span>} /></> : <Note tone="bad">{L('لم يُعثر على FFmpeg. المعاينات والتصدير والتحقق من الملفات تحتاجه.', 'FFmpeg was not found. Thumbnails, export and file checks need it.')}</Note>}
            <Btn className="mt-4" onClick={async () => { const [p] = await pickFiles({ directory: true, title: L('مجلد يحوي ffmpeg و ffprobe', 'Folder containing ffmpeg and ffprobe') }); if (p) setting('ffmpeg_dir', p, L('حُفظ', 'Saved')); }}>{L('حدّد مجلد FFmpeg', 'Choose FFmpeg folder')}</Btn>
          </Panel>
          <Panel title={L('السجل', 'Activity log')} right={<Btn small tone="ghost" data-action="load-log" onClick={() => rpc('audit_log').then(setLog).catch((e) => st.toast(errText(e), 'bad'))}>{log ? L('تحديث', 'Refresh') : L('اعرض', 'Show')}</Btn>}>
            {!log && <p className="text-sm text-mute">{L('تشغيل GPU وإيقافه، الموافقات، تغييرات الميزانية والأسرار (بلا قيمها).', 'GPU starts and stops, approvals, budget changes and secret changes (never their values).')}</p>}
            {log && <div className="max-h-72 overflow-y-auto divide-y divide-line text-xs" data-log>{log.map((l) => <div key={l.id} className="py-1.5 grid grid-cols-[130px_150px_1fr] gap-3"><span className="text-mute">{fmtDate(l.ts)}</span><span className="ltr text-soft">{l.event}</span><span className="text-mute selectable break-words">{l.message}</span></div>)}{!log.length && <p className="py-2 text-mute">—</p>}</div>}
          </Panel>
        </div>
      </div>
      {move && <Confirm title={L('تغيير موقع المكتبة', 'Change library location')} confirmLabel={L('استخدم هذا المجلد', 'Use this folder')} onClose={() => setMove(null)}
        text={<><p className="ltr text-xs break-all">{move}</p><p>{L('سيستخدم التطبيق هذا المجلد من الآن ويُنشئ فيه المجلدات الستة وقاعدة بيانات جديدة إن لم توجد. المكتبة الحالية تبقى في مكانها دون تغيير ولا تُنقل تلقائيًا.', 'The app will use this folder from now on and create the six folders and a new database in it if they do not exist. The current library stays where it is, unchanged, and is not moved automatically.')}</p></>}
        onConfirm={async () => { const r = await st.run(() => rpc('library_set', { path: move }), L('تغيّر موقع المكتبة', 'Library location changed')); if (r) { st.closeProject(); await st.refreshStatus(); } }} />}
    </Slate>
  );
}
