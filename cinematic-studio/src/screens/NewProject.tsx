import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, pick } from '../lib/i18n';
import { rpc } from '../lib/rpc';
import { Btn, Slate, Field, Input, Area, Select, Note } from '../lib/ui';
import { videoTypes } from '../director';

export default function NewProject() {
  const st = useStudio();
  const [models, setModels] = useState<any[]>([]);
  const [f, setF] = useState({ name: '', description: '', video_type: 'commercial', aspect: '16:9', duration: 15, model_id: 'wan22-ti2v-5b' });
  const [busy, setBusy] = useState(false);
  useEffect(() => { rpc('models_list').then(setModels).catch(() => {}); }, []);
  const model = models.find((m) => m.id === f.model_id);
  const aspects: string[] = model ? model.sizes.map((s: any) => s[0]) : ['16:9', '9:16'];
  useEffect(() => { if (model && !aspects.includes(f.aspect)) setF((x) => ({ ...x, aspect: aspects[0] })); }, [f.model_id, models.length]); // eslint-disable-line react-hooks/exhaustive-deps
  const create = async () => {
    setBusy(true);
    const p: any = await st.run(() => rpc('project_create', f));
    setBusy(false);
    if (p) { st.setProject(p); st.go('creator'); st.refreshStatus(); }
  };
  return (
    <Slate title={L('مشروع جديد', 'New project')} sub={L('يُنشأ للمشروع مجلد خاص داخل مكتبتك، وتُحفظ بياناته في قاعدة بيانات محلية.', 'The project gets its own folder inside your library, and its data is kept in a local database.')}>
      <div className="max-w-2xl space-y-5">
        <Field label={L('اسم المشروع', 'Project name')}><Input data-field="name" value={f.name} maxLength={120} onChange={(e) => setF({ ...f, name: e.target.value })} placeholder={L('مثال: إعلان عطر الصحراء', 'e.g. Desert perfume commercial')} /></Field>
        <Field label={L('فكرة الفيلم', 'Film idea')} hint={L('اكتبها بالعربية أو الإنجليزية. يمكنك تعديلها لاحقًا.', 'Write it in Arabic or English. You can change it later.')}><Area data-field="description" rows={5} value={f.description} maxLength={4000} onChange={(e) => setF({ ...f, description: e.target.value })} /></Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label={L('نوع الفيديو', 'Video type')}><Select value={f.video_type} onChange={(e) => setF({ ...f, video_type: e.target.value })}>{videoTypes.map((t) => <option key={t.id} value={t.id}>{pick(t)}</option>)}</Select></Field>
          <Field label={L('النموذج', 'Model')}><Select value={f.model_id} onChange={(e) => setF({ ...f, model_id: e.target.value })}>{models.map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}</Select></Field>
          <Field label={L('المقاس', 'Aspect ratio')} hint={L('تظهر المقاسات التي يولّدها النموذج المختار فقط.', 'Only the ratios the chosen model generates are listed.')}><Select value={f.aspect} onChange={(e) => setF({ ...f, aspect: e.target.value })}>{aspects.map((a) => <option key={a}>{a}</option>)}</Select></Field>
          <Field label={L('المدة (ثانية)', 'Duration (seconds)')}><Input type="number" min={2} max={600} value={f.duration} onChange={(e) => setF({ ...f, duration: Math.max(2, Math.min(600, Number(e.target.value) || 2)) })} /></Field>
        </div>
        {model && !model.tasks.includes('t2v') && <Note tone="warn">{L('هذا النموذج يحوّل الصورة إلى فيديو: كل مشهد سيحتاج صورة مرجعية من مكتبة الوسائط.', 'This model is image-to-video: every scene will need a reference image from the media library.')}</Note>}
        <div className="flex gap-2 pt-2"><Btn tone="accent" data-action="create-project" disabled={busy || f.name.trim().length < 2} onClick={create}>{L('إنشاء المشروع', 'Create project')}</Btn><Btn tone="ghost" onClick={() => st.go('dashboard')}>{L('إلغاء', 'Cancel')}</Btn></div>
      </div>
    </Slate>
  );
}
