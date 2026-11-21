import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDate, fmtSize, errText } from '../lib/i18n';
import { rpc, pickFiles } from '../lib/rpc';
import { Btn, Slate, Panel, Note, Tag, Field, Input, Select, Modal, Confirm, Area, cx } from '../lib/ui';

const SPEC: Record<string, [string, string]> = {
  gulf_commercial_advertising: ['الإعلانات التجارية الخليجية', 'Gulf Commercial Advertising'], luxury_real_estate: ['العقارات الفاخرة', 'Luxury Real Estate'],
  saudi_tourism: ['السياحة السعودية', 'Saudi Tourism'], luxury_product_cinematography: ['تصوير المنتجات الفاخرة', 'Luxury Product Cinematography'],
};
const spec = (id: string) => (SPEC[id] ? L(...SPEC[id]) : id);

export default function Models() {
  const st = useStudio();
  const [models, setModels] = useState<any[]>([]);
  const [comfy, setComfy] = useState<any | null>(null);
  const [lo, setLo] = useState<any>({ loras: [], families: [], specialties: [], datasets: [], runs: [] });
  const [imp, setImp] = useState<any | null>(null);
  const [ds, setDs] = useState<any | null>(null);
  const [plan, setPlan] = useState<any | null>(null);
  const [approve, setApprove] = useState<any | null>(null);
  const [del, setDel] = useState<any | null>(null);
  const [checking, setChecking] = useState(false);
  const loadL = () => rpc('lora_list').then(setLo).catch((e) => st.toast(errText(e), 'bad'));
  const check = () => { setChecking(true); rpc('comfy_status').then(setComfy).catch(() => {}).finally(() => setChecking(false)); };
  useEffect(() => { rpc('models_list').then(setModels).catch(() => {}); loadL(); check(); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const pre = (id: string) => comfy?.models?.find((m: any) => m.model === id);
  const up = async (id: string, patch: any) => { await st.run(() => rpc('lora_update', { id, ...patch })); loadL(); };

  return (
    <Slate title={L('النماذج و LoRA', 'Model Manager')} sub={L('النماذج تعمل على خادم ComfyUI وليست على هذا الجهاز. هنا ترى ما يحتاجه كل نموذج وما ينقص الخادم، وتدير ملفات LoRA.', 'Models run on the ComfyUI server, not on this computer. Here you see what each model needs and what the server is missing, and manage LoRA files.')}
      actions={<Btn onClick={check} disabled={checking}>{checking ? L('يفحص…', 'Checking…') : L('افحص الخادم', 'Check the server')}</Btn>}>
      {comfy && !comfy.configured && <div className="mb-5"><Note tone="warn">{L('خادم ComfyUI غير مضبوط، لذلك لا يمكن معرفة الملفات الموجودة عليه.', 'No ComfyUI server is configured, so the files on it cannot be checked.')} <button type="button" className="underline text-accent" onClick={() => st.go('settings')}>{L('الإعدادات', 'Settings')}</button></Note></div>}
      {comfy?.configured && !comfy.connected && <div className="mb-5"><Note tone="bad">{errText(comfy.error)}</Note></div>}
      <div className="grid grid-cols-2 gap-6 items-start mb-8" data-models>
        {models.map((m) => { const p = pre(m.id); return (
          <Panel key={m.id} title={<span className="ltr normal-case tracking-normal text-sm text-text">{m.label}</span>} right={p ? <Tag status={p.ready ? 'ready' : 'failed'}>{p.ready ? L('جاهز على الخادم', 'Ready on the server') : L('ينقصه ملفات', 'Files missing')}</Tag> : <Tag>{L('لم يُفحص', 'Not checked')}</Tag>}>
            <p className="text-[13px] text-soft">{m.tasks.includes('t2v') ? L('نص ← فيديو، وصورة ← فيديو', 'Text-to-video and image-to-video') : L('صورة ← فيديو فقط', 'Image-to-video only')} · <span className="num">{m.fps} fps</span> · {L('حتى', 'up to')} <span className="num">{m.max_seconds.toFixed(1)}s</span> · <span className="num">{m.sizes.map((s: any) => `${s[0]} (${s[1]}×${s[2]})`).join(', ')}</span></p>
            <p className="text-xs text-mute mt-1.5">{L('الترخيص', 'Licence')}: <span className="ltr">{m.licence}</span> · {L('VRAM أدنى', 'Min VRAM')}: <span className="num">{m.min_vram_gb} GB</span> · LoRA: <span className="ltr">{m.lora_family}</span></p>
            <p className="text-xs text-mute mt-1">{m.status}</p>
            <ul className="mt-3 space-y-1 text-xs">{m.files.map((f: any) => { const on = p?.files?.find((x: any) => x.name === f.name); return <li key={f.name} className="flex justify-between gap-3"><span className="ltr text-soft truncate selectable">models/{f.folder}/{f.name}</span><span className={cx('shrink-0', on ? (on.present ? 'text-ok' : 'text-bad') : 'text-mute')}>{on ? (on.present ? L('موجود', 'present') : L('غير موجود', 'missing')) : '—'}</span></li>; })}</ul>
            {!!p?.missing_nodes?.length && <p className="text-xs text-bad mt-2">{L('عُقد ناقصة في ComfyUI', 'Nodes missing in ComfyUI')}: <span className="ltr">{p.missing_nodes.join(', ')}</span></p>}
            <p className="text-[11px] text-mute mt-3 ltr truncate selectable">{m.source}</p>
          </Panel>); })}
      </div>
      <div className="mb-8"><Note>{L('HunyuanVideo 1.5 و LTX و CogVideoX غير مضافة بعد. بنية المحوّلات تسمح بإضافتها: كل نموذج له محوّل وملف برومبت وعائلة LoRA خاصة به.', 'HunyuanVideo 1.5, LTX and CogVideoX are not added yet. The adapter structure allows it: each model has its own adapter, prompt profile and LoRA family.')}</Note></div>

      <Panel title="LoRA" right={<Btn small data-action="import-lora" onClick={async () => { const [path] = await pickFiles({ filters: [{ name: 'safetensors', extensions: ['safetensors'] }], title: 'LoRA (.safetensors)' }); if (path) setImp({ path, name: path.split(/[\\/]/).pop()!.replace(/\.safetensors$/i, ''), family: lo.families[0], specialty: lo.specialties[0], version: '1.0.0', trigger: '' }); }}>{L('استيراد LoRA', 'Import LoRA')}</Btn>}>
        <p className="text-xs text-mute mb-3">{L('كل ملف LoRA يخص عائلة نموذج واحدة ولا يُطبَّق على غيرها. يُفعَّل إصدار واحد لكل اسم. الملف المفعَّل يجب أن يكون أيضًا في مجلد loras على الخادم.', 'Each LoRA file belongs to one model family and is never applied to another. One version per name can be enabled. An enabled file must also be in the server\'s loras folder.')}</p>
        {!lo.loras.length && <p className="text-sm text-mute">{L('لا ملفات LoRA بعد.', 'No LoRA files yet.')}</p>}
        <div className="divide-y divide-line" data-loras>
          {lo.loras.map((l: any) => (
            <div key={l.id} data-lora={l.id} className="py-3 grid grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)_150px_auto] gap-4 items-center text-sm">
              <div className="min-w-0"><p className="truncate"><span className="ltr">{l.name}</span> <span className="num text-mute">v{l.version}</span></p><p className="text-xs text-mute truncate"><span className="ltr">{l.family}</span> · {spec(l.specialty)} · <span className="num">{fmtSize(l.size)}</span>{l.trigger ? <> · trigger: <span className="ltr">{l.trigger}</span></> : null}</p></div>
              <p className="text-xs text-mute truncate">{fmtDate(l.created_at)}</p>
              <label className="flex items-center gap-2 text-xs text-mute"><input type="range" min={0} max={1.5} step={0.05} defaultValue={l.strength} onMouseUp={(e) => up(l.id, { strength: Number(e.currentTarget.value) })} onKeyUp={(e) => up(l.id, { strength: Number(e.currentTarget.value) })} className="w-24" /><span className="num">{l.strength.toFixed(2)}</span></label>
              <span className="flex gap-1 justify-end"><Btn small tone={l.enabled ? 'accent' : 'plain'} data-action="toggle-lora" onClick={() => up(l.id, { enabled: !l.enabled })}>{l.enabled ? L('مفعَّل', 'Enabled') : L('فعِّل', 'Enable')}</Btn><Btn small tone="ghost" className="hover:!text-bad" onClick={() => setDel(l)}>{L('حذف', 'Delete')}</Btn></span>
            </div>
          ))}
        </div>
      </Panel>

      <div className="grid grid-cols-2 gap-6 items-start mt-6">
        <Panel title={L('مجموعات بيانات التدريب', 'Training datasets')} right={<Btn small onClick={async () => { const [folder] = await pickFiles({ directory: true, title: L('مجلد المقاطع', 'Clips folder') }); if (folder) setDs({ folder, name: folder.split(/[\\/]/).pop(), specialty: lo.specialties[0], rights_note: '' }); }}>{L('سجّل مجلدًا', 'Register a folder')}</Btn>}>
          {!lo.datasets.length && <p className="text-sm text-mute">{L('لا مجموعات بعد. المجلد يبقى في مكانه؛ يُسجَّل مساره وعدد مقاطعه ومصدر حقوقه فقط.', 'No datasets yet. The folder stays where it is; only its path, clip count and rights note are recorded.')}</p>}
          <div className="divide-y divide-line">{lo.datasets.map((x: any) => <div key={x.id} className="py-2.5 text-sm"><div className="flex justify-between gap-3"><span className="truncate">{x.name} <span className="text-mute text-xs">· {spec(x.specialty)} · <span className="num">{x.clip_count}</span> {L('مقطعًا', 'clips')}</span></span><Btn small tone="ghost" onClick={async () => { await st.run(() => rpc('lora_dataset_remove', { id: x.id })); loadL(); }}>{L('إزالة', 'Remove')}</Btn></div><p className="text-xs text-mute mt-1">{L('الحقوق', 'Rights')}: {x.rights_note}</p></div>)}</div>
        </Panel>
        <Panel title={L('سجل التدريب', 'Training history')} right={<Btn small onClick={() => setPlan({ family: 'wan22-a14b-i2v', dataset_id: lo.datasets[0]?.id || '', estimated_cost_sar: '', notes: '' })}>{L('خطّط لتدريب', 'Plan a run')}</Btn>}>
          <Note>{L('التطبيق لا يبدأ أي تدريب. التدريب يُجرى خارج التطبيق عبر Musubi Tuner بعد موافقة المدير، ثم تُستورد النتيجة هنا كإصدار جديد.', 'The app never starts training. Training is done outside the app with Musubi Tuner after the manager approves, and the result is imported here as a new version.')}</Note>
          <div className="divide-y divide-line mt-3">{lo.runs.map((r: any) => <div key={r.id} className="py-2.5 text-sm"><div className="flex items-center gap-3"><Tag status={r.status === 'recorded' ? 'completed' : r.status === 'approved' ? 'queued' : 'pending'}>{r.status === 'planned' ? L('مخطَّط', 'Planned') : r.status === 'approved' ? L('موافَق عليه', 'Approved') : L('مسجَّل', 'Recorded')}</Tag><span className="flex-1 truncate"><span className="ltr">{r.family}</span> <span className="text-mute text-xs">· {r.dataset_name || '—'} · <span className="ltr">{r.tool}</span></span></span>
            {r.status === 'planned' && <Btn small onClick={() => setApprove(r)}>{L('موافقة', 'Approve')}</Btn>}{r.status === 'approved' && <Btn small onClick={async () => { await st.run(() => rpc('lora_run_update', { id: r.id, status: 'recorded' })); loadL(); }}>{L('سجّل كمنتهٍ', 'Mark as done')}</Btn>}</div>
            <p className="text-xs text-mute mt-1">{fmtDate(r.created_at)}{r.estimated_cost_sar != null ? <> · <span className="num">≈ {r.estimated_cost_sar} SAR</span></> : null}{r.approved_by ? ` · ${L('وافق', 'approved by')} ${r.approved_by}` : ''}{r.notes ? ` · ${r.notes}` : ''}</p></div>)}</div>
        </Panel>
      </div>

      {imp && <Modal title={L('استيراد LoRA', 'Import LoRA')} onClose={() => setImp(null)} footer={<><Btn tone="ghost" onClick={() => setImp(null)}>{L('إلغاء', 'Cancel')}</Btn><Btn tone="accent" data-action="confirm-import-lora" onClick={async () => { const r = await st.run(() => rpc('lora_import', imp), L('استُورد الملف (غير مفعَّل)', 'File imported (not enabled)')); if (r) { setImp(null); loadL(); } }}>{L('استيراد', 'Import')}</Btn></>}>
        <div className="space-y-4">
          <p className="ltr text-xs text-mute break-all">{imp.path}</p>
          <div className="grid grid-cols-2 gap-4">
            <Field label={L('الاسم', 'Name')}><Input className="ltr" value={imp.name} onChange={(e) => setImp({ ...imp, name: e.target.value })} /></Field>
            <Field label={L('الإصدار', 'Version')}><Input className="ltr" value={imp.version} onChange={(e) => setImp({ ...imp, version: e.target.value })} /></Field>
            <Field label={L('عائلة النموذج', 'Model family')}><Select value={imp.family} onChange={(e) => setImp({ ...imp, family: e.target.value })}>{lo.families.map((f: string) => <option key={f}>{f}</option>)}</Select></Field>
            <Field label={L('التخصص', 'Specialty')}><Select value={imp.specialty} onChange={(e) => setImp({ ...imp, specialty: e.target.value })}>{lo.specialties.map((s: string) => <option key={s} value={s}>{spec(s)}</option>)}</Select></Field>
          </div>
          <Field label={L('كلمة التفعيل (اختياري)', 'Trigger word (optional)')} hint={L('تُضاف إلى أول البرومبت عند تفعيل الملف.', 'Added to the start of the prompt while the file is enabled.')}><Input className="ltr" value={imp.trigger} onChange={(e) => setImp({ ...imp, trigger: e.target.value })} /></Field>
          <Note>{L('يُقبل ‎.safetensors‎ فقط ويُفحص ترويسه. يُنسخ الملف إلى مجلد Models داخل مكتبتك.', 'Only .safetensors is accepted and its header is checked. The file is copied into the Models folder of your library.')}</Note>
        </div>
      </Modal>}
      {ds && <Modal title={L('تسجيل مجموعة بيانات', 'Register a dataset')} onClose={() => setDs(null)} footer={<><Btn tone="ghost" onClick={() => setDs(null)}>{L('إلغاء', 'Cancel')}</Btn><Btn tone="accent" onClick={async () => { const r = await st.run(() => rpc('lora_dataset_add', ds)); if (r) { setDs(null); loadL(); } }}>{L('تسجيل', 'Register')}</Btn></>}>
        <div className="space-y-4"><p className="ltr text-xs text-mute break-all">{ds.folder}</p>
          <Field label={L('الاسم', 'Name')}><Input value={ds.name} onChange={(e) => setDs({ ...ds, name: e.target.value })} /></Field>
          <Field label={L('التخصص', 'Specialty')}><Select value={ds.specialty} onChange={(e) => setDs({ ...ds, specialty: e.target.value })}>{lo.specialties.map((s: string) => <option key={s} value={s}>{spec(s)}</option>)}</Select></Field>
          <Field label={L('مصدر المقاطع وما يجيز التدريب عليها (إلزامي)', 'Where the clips come from and what permits training on them (required)')}><Area rows={3} value={ds.rights_note} onChange={(e) => setDs({ ...ds, rights_note: e.target.value })} /></Field></div>
      </Modal>}
      {plan && <Modal title={L('خطة تدريب', 'Training plan')} onClose={() => setPlan(null)} footer={<><Btn tone="ghost" onClick={() => setPlan(null)}>{L('إلغاء', 'Cancel')}</Btn><Btn tone="accent" onClick={async () => { const r = await st.run(() => rpc('lora_run_plan', { ...plan, dataset_id: plan.dataset_id || undefined, estimated_cost_sar: plan.estimated_cost_sar === '' ? undefined : Number(plan.estimated_cost_sar) })); if (r) { setPlan(null); loadL(); } }}>{L('احفظ الخطة', 'Save plan')}</Btn></>}>
        <div className="space-y-4">
          <Field label={L('عائلة النموذج', 'Model family')}><Select value={plan.family} onChange={(e) => setPlan({ ...plan, family: e.target.value })}>{lo.families.map((f: string) => <option key={f}>{f}</option>)}</Select></Field>
          <Field label={L('مجموعة البيانات', 'Dataset')}><Select value={plan.dataset_id} onChange={(e) => setPlan({ ...plan, dataset_id: e.target.value })}><option value="">—</option>{lo.datasets.map((d: any) => <option key={d.id} value={d.id}>{d.name}</option>)}</Select></Field>
          <Field label={L('التكلفة التقديرية (SAR)', 'Estimated cost (SAR)')}><Input type="number" min={0} value={plan.estimated_cost_sar} onChange={(e) => setPlan({ ...plan, estimated_cost_sar: e.target.value })} /></Field>
          <Field label={L('ملاحظات', 'Notes')}><Area rows={2} value={plan.notes} onChange={(e) => setPlan({ ...plan, notes: e.target.value })} /></Field>
          <Note>{L('حفظ الخطة لا يشغّل شيئًا ولا يكلّف شيئًا.', 'Saving a plan runs nothing and costs nothing.')}</Note></div>
      </Modal>}
      {approve && <Confirm needName defaultName={st.status.settings.operator_name || ''} title={L('الموافقة على تدريب LoRA', 'Approve a LoRA training run')} confirmLabel={L('أوافق', 'I approve')} onClose={() => setApprove(null)} text={<p>{L('الموافقة تُسجَّل باسمك. التدريب نفسه لا يبدأ من التطبيق.', 'The approval is recorded under your name. The training itself is not started by the app.')}{approve.estimated_cost_sar != null ? <span className="num block mt-1">≈ {approve.estimated_cost_sar} SAR</span> : null}</p>} onConfirm={async (name) => { await st.run(() => rpc('lora_run_update', { id: approve.id, status: 'approved', approved_by: name })); loadL(); }} />}
      {del && <Confirm danger title={L('حذف LoRA', 'Delete LoRA')} confirmLabel={L('حذف', 'Delete')} onClose={() => setDel(null)} text={<p>{L('يُزال من القائمة ويُنقل ملفه إلى Backups/Deleted.', 'It is removed from the list and its file is moved to Backups/Deleted.')}</p>} onConfirm={async () => { await st.run(() => rpc('lora_remove', { id: del.id })); loadL(); }} />}
    </Slate>
  );
}
