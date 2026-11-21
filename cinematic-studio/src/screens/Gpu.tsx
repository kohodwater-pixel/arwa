import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDate, statusText, errText } from '../lib/i18n';
import { rpc } from '../lib/rpc';
import { Btn, Slate, Panel, Meter, Note, Row, Confirm, Field, Input, Tag, Select } from '../lib/ui';

export default function Gpu() {
  const st = useStudio();
  const [g, setG] = useState<any | null>(null);
  const [comfy, setComfy] = useState<any | null>(null);
  const [ask, setAsk] = useState(false);
  const [key, setKey] = useState('');
  const [budgetAsk, setBudgetAsk] = useState<string | null>(null);
  const s = st.status.settings;
  const [f, setF] = useState({ gpu_instance_id: s.gpu_instance_id || '', gpu_budget_sar: s.gpu_budget_sar || '1000', usd_to_sar: s.usd_to_sar || '3.75', gpu_idle_minutes: s.gpu_idle_minutes || '10', gpu_rate_usd: s.gpu_rate_usd || '' });
  const load = () => { rpc('gpu_status').then(setG).catch((e) => st.toast(errText(e), 'bad')); rpc('comfy_status').then(setComfy).catch(() => {}); };
  useEffect(() => { load(); const t = setInterval(load, 15000); return () => clearInterval(t); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const setting = async (key: string, value: string) => { const r = await st.run(() => rpc('setting_set', { key, value })); if (r) { await st.refreshStatus(); load(); } return r; };
  if (!g) return <Slate title={L('إدارة GPU', 'GPU Manager')}><p className="text-mute">…</p></Slate>;
  const b = g.budget, inst = g.instance, state = inst?.state as string | undefined;
  const running = state === 'running' || state === 'starting';
  const rate = inst?.rate_usd_per_hour ?? g.session?.rate_usd_per_hour ?? (Number(f.gpu_rate_usd) || 0);
  return (
    <Slate title={L('إدارة GPU', 'GPU Manager')} sub={L('GPU السحابي يعمل عند الطلب فقط. لا يبدأ إلا بموافقتك الصريحة، ويتوقف تلقائيًا عند الخمول، والتكلفة محسوبة مقابل ميزانية شهرية.', 'The cloud GPU runs on demand only. It starts only with your explicit approval, stops by itself when idle, and its cost is counted against a monthly budget.')}>
      <div className="grid grid-cols-2 gap-6 items-start">
        <div className="space-y-6">
          <Panel title={L('الميزانية الشهرية', 'Monthly budget')} right={<span className="num text-xs text-mute">{b.month}</span>}>
            <div className="flex items-baseline justify-between"><p className="num text-2xl font-semibold" data-budget-spent>{b.spent_sar.toFixed(2)} <span className="text-sm text-mute font-normal">/ {b.limit_sar.toFixed(0)} SAR</span></p><p className="num text-sm text-soft" data-budget-level={b.level}>{b.percent.toFixed(1)}%</p></div>
            <div className="relative mt-3"><Meter value={b.percent / 100} tone={b.level === 'blocked' ? 'bad' : 'accent'} /><i className="absolute -top-1 h-3.5 w-px bg-mute" style={{ insetInlineStart: '70%' }} /><i className="absolute -top-1 h-3.5 w-px bg-mute" style={{ insetInlineStart: '90%' }} /></div>
            <p className="text-xs text-mute mt-2">{L('تحذير عند 70% و90%، وإيقاف قبول مهام التوليد الجديدة عند 100%.', 'Warnings at 70% and 90%; new generation jobs are refused at 100%.')}</p>
            {b.level === 'warn70' && <div className="mt-3"><Note tone="warn">{L('تجاوز الإنفاق 70% من ميزانية هذا الشهر.', 'Spending has passed 70% of this month\'s budget.')}</Note></div>}
            {b.level === 'warn90' && <div className="mt-3"><Note tone="warn">{L('تجاوز الإنفاق 90% من ميزانية هذا الشهر. اقترب الإيقاف.', 'Spending has passed 90% of this month\'s budget. The stop is close.')}</Note></div>}
            {b.level === 'blocked' && <div className="mt-3"><Note tone="bad">{L('بلغ الإنفاق حد الميزانية. لا تُقبل مهام توليد جديدة ولا يُشغَّل GPU حتى يرفع المدير الحد.', 'Spending reached the budget limit. No new generation jobs are accepted and the GPU will not start until the manager raises the limit.')}</Note></div>}
            <div className="mt-4"><Row k={L('ساعات التشغيل هذا الشهر', 'Hours this month')} v={<span className="num">{b.hours.toFixed(2)}</span>} /><Row k={L('المتبقي', 'Remaining')} v={<span className="num">{b.remaining_sar.toFixed(2)} SAR</span>} /><Row k={L('سعر الصرف', 'Exchange rate')} v={<span className="num">1 USD = {b.usd_to_sar} SAR</span>} /></div>
          </Panel>
          <Panel title={L('سياسة التكلفة', 'Cost policy')}>
            <div className="grid grid-cols-2 gap-4">
              <Field label={L('الميزانية الشهرية (SAR)', 'Monthly budget (SAR)')}><div className="flex gap-2"><Input data-field="budget" type="number" min={0} value={f.gpu_budget_sar} onChange={(e) => setF({ ...f, gpu_budget_sar: e.target.value })} /><Btn disabled={f.gpu_budget_sar === String(s.gpu_budget_sar || '1000')} onClick={() => (Number(f.gpu_budget_sar) > b.limit_sar ? setBudgetAsk(f.gpu_budget_sar) : setting('gpu_budget_sar', f.gpu_budget_sar))}>{L('حفظ', 'Save')}</Btn></div></Field>
              <Field label={L('إيقاف تلقائي بعد خمول (دقيقة)', 'Auto-stop after idle (minutes)')}><div className="flex gap-2"><Input type="number" min={1} max={240} value={f.gpu_idle_minutes} onChange={(e) => setF({ ...f, gpu_idle_minutes: e.target.value })} /><Btn onClick={() => setting('gpu_idle_minutes', f.gpu_idle_minutes)}>{L('حفظ', 'Save')}</Btn></div></Field>
              <Field label={L('سعر صرف الدولار', 'USD to SAR')}><div className="flex gap-2"><Input type="number" step={0.01} value={f.usd_to_sar} onChange={(e) => setF({ ...f, usd_to_sar: e.target.value })} /><Btn onClick={() => setting('usd_to_sar', f.usd_to_sar)}>{L('حفظ', 'Save')}</Btn></div></Field>
              <Field label={L('سعر الساعة الاحتياطي (USD)', 'Fallback hourly rate (USD)')} hint={L('يُستخدم فقط إذا لم يُرجع المزود السعر.', 'Used only when the provider does not report a price.')}><div className="flex gap-2"><Input type="number" step={0.01} min={0} value={f.gpu_rate_usd} onChange={(e) => setF({ ...f, gpu_rate_usd: e.target.value })} /><Btn onClick={() => setting('gpu_rate_usd', f.gpu_rate_usd || '0')}>{L('حفظ', 'Save')}</Btn></div></Field>
            </div>
          </Panel>
        </div>

        <div className="space-y-6">
          <Panel title={L('الجهاز السحابي', 'Cloud instance')} right={state ? <Tag status={state} /> : <Tag>{L('غير مضبوط', 'Not configured')}</Tag>}>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <Field label={L('المزود', 'Provider')}><Select data-field="provider" value={s.gpu_provider || 'none'} onChange={(e) => setting('gpu_provider', e.target.value)}><option value="none">{L('بلا مزود (خادمي الخاص)', 'None (my own server)')}</option><option value="runpod">RunPod</option></Select></Field>
              <Field label="Pod ID"><div className="flex gap-2"><Input className="ltr" value={f.gpu_instance_id} onChange={(e) => setF({ ...f, gpu_instance_id: e.target.value })} /><Btn onClick={() => setting('gpu_instance_id', f.gpu_instance_id)}>{L('حفظ', 'Save')}</Btn></div></Field>
            </div>
            <Field label={L('مفتاح API للمزود', 'Provider API key')} hint={g.key_stored ? L(`مفتاح محفوظ في ${g.secret_backend}. لا يُعرض ولا يُكتب في قاعدة البيانات أو السجلات.`, `A key is stored in ${g.secret_backend}. It is never shown, nor written to the database or logs.`) : L(`يُحفظ في ${g.secret_backend} عبر النواة، لا في الواجهة.`, `Stored in ${g.secret_backend} by the core, not in the interface.`)}>
              <div className="flex gap-2"><Input className="ltr" type="password" autoComplete="off" value={key} placeholder={g.key_stored ? '••••••••••••' : ''} onChange={(e) => setKey(e.target.value)} /><Btn disabled={key.length < 8} onClick={async () => { await st.run(() => rpc('secret_set', { name: 'gpu_api_key', value: key }), L('حُفظ المفتاح', 'Key stored')); setKey(''); st.refreshStatus(); load(); }}>{L('حفظ', 'Save')}</Btn>{g.key_stored && <Btn tone="ghost" onClick={async () => { await st.run(() => rpc('secret_delete', { name: 'gpu_api_key' })); st.refreshStatus(); load(); }}>{L('حذف', 'Delete')}</Btn>}</div>
            </Field>
            {s.gpu_provider === 'runpod' && !g.configured && <div className="mt-4"><Note>{L('غير مضبوط بعد: أدخل Pod ID والمفتاح. لا يُجرى أي اتصال بالمزود قبل ذلك.', 'Not configured yet: enter the Pod ID and the key. No call is made to the provider before that.')}</Note></div>}
            {g.error && <div className="mt-4"><Note tone="bad"><span className="selectable">{errText(g.error)}</span></Note></div>}
            {inst && <div className="mt-4">
              <Row k={L('الحالة', 'State')} v={statusText(state)} />
              <Row k="GPU" v={<span className="ltr">{inst.gpu || '—'}</span>} />
              <Row k={L('السعر', 'Rate')} v={<span className="num">{rate ? `${rate.toFixed(3)} USD/h ≈ ${(rate * b.usd_to_sar).toFixed(2)} SAR/h` : '—'}</span>} />
              <Row k={L('مدة التشغيل الحالية', 'Current runtime')} v={<span className="num">{g.runtime_minutes != null ? `${g.runtime_minutes.toFixed(1)} min` : '—'}</span>} />
              <Row k={L('تكلفة هذه الجلسة', 'Cost of this session')} v={<span className="num">{g.runtime_minutes != null && rate ? `${((g.runtime_minutes / 60) * rate * b.usd_to_sar).toFixed(2)} SAR` : '—'}</span>} />
              <Row k={L('إيقاف تلقائي بعد خمول', 'Auto-stop after idle')} v={<span className="num">{g.idle_minutes} min</span>} />
              <Row k="VRAM" v={comfy?.connected ? <span className="num">{((comfy.system.vram_total - comfy.system.vram_free) / 2 ** 30).toFixed(1)} / {(comfy.system.vram_total / 2 ** 30).toFixed(1)} GB</span> : <span className="text-mute">{L('يظهر عند اتصال ComfyUI', 'Shown when ComfyUI is connected')}</span>} />
            </div>}
            {g.configured && <div className="mt-5 flex gap-2">
              <Btn tone="accent" data-action="gpu-start" disabled={running || b.level === 'blocked' || !inst} onClick={() => setAsk(true)}>{L('شغّل GPU', 'Start GPU')}</Btn>
              <Btn data-action="gpu-stop" disabled={!running} onClick={async () => { await st.run(() => rpc('gpu_stop'), L('أُرسل أمر الإيقاف', 'Stop requested')); load(); st.refreshStatus(); }}>{L('أوقف GPU', 'Stop GPU')}</Btn>
              <Btn tone="ghost" onClick={load}>{L('تحديث', 'Refresh')}</Btn>
            </div>}
          </Panel>
          <Panel title={L('سجل الجلسات', 'Session log')}>
            {!g.sessions.length && <p className="text-sm text-mute">{L('لم يُشغَّل GPU من هذا التطبيق بعد.', 'The GPU has not been run from this app yet.')}</p>}
            <div className="divide-y divide-line text-[13px] max-h-72 overflow-y-auto">{g.sessions.map((x: any) => { const hrs = ((x.stopped_at ? new Date(x.stopped_at).getTime() : Date.now()) - new Date(x.started_at).getTime()) / 3.6e6; return <div key={x.id} className="py-2 grid grid-cols-[1fr_auto] gap-x-4"><span>{fmtDate(x.started_at)} <span className="text-mute">· {x.approved_by}</span></span><span className="num text-soft">{hrs.toFixed(2)} h · {(hrs * x.rate_usd_per_hour * x.usd_to_sar).toFixed(2)} SAR</span><span className="text-xs text-mute col-span-2">{x.stopped_at ? x.stop_reason : L('تعمل الآن', 'running now')}</span></div>; })}</div>
          </Panel>
        </div>
      </div>
      {ask && <Confirm needName defaultName={s.operator_name || ''} title={L('تشغيل GPU مدفوع', 'Start a paid GPU')} confirmLabel={L('أوافق، شغّل', 'I approve, start')} onClose={() => setAsk(false)}
        text={<><p>{L('سيبدأ احتساب التكلفة فور التشغيل وحتى الإيقاف.', 'Billing starts as soon as it runs and continues until it stops.')}</p><p className="num">{rate ? `${rate.toFixed(3)} USD/h ≈ ${(rate * b.usd_to_sar).toFixed(2)} SAR/h` : L('السعر غير معروف من المزود', 'The provider did not report a price')} · {L('المتبقي من الميزانية', 'Budget remaining')}: {b.remaining_sar.toFixed(2)} SAR</p><p>{L(`يتوقف تلقائيًا بعد ${g.idle_minutes} دقيقة بلا مهام.`, `It stops by itself after ${g.idle_minutes} minutes without jobs.`)}</p></>}
        onConfirm={async (name) => { await st.run(() => rpc('gpu_start', { approved: true, approved_by: name }), L('أُرسل أمر التشغيل', 'Start requested')); await rpc('setting_set', { key: 'operator_name', value: name }).catch(() => {}); load(); st.refreshStatus(); }} />}
      {budgetAsk && <Confirm needName defaultName={s.operator_name || ''} title={L('رفع حد الميزانية', 'Raise the budget limit')} confirmLabel={L('أوافق على الرفع', 'I approve the increase')} onClose={() => setBudgetAsk(null)}
        text={<p className="num">{b.limit_sar.toFixed(0)} SAR → {Number(budgetAsk).toFixed(0)} SAR</p>} onConfirm={async (name) => { await rpc('setting_set', { key: 'operator_name', value: name }).catch(() => {}); await setting('gpu_budget_sar', budgetAsk); }} />}
    </Slate>
  );
}
