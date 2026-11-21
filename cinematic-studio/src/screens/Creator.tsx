import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, pick } from '../lib/i18n';
import { rpc } from '../lib/rpc';
import { Btn, Slate, Field, Input, Area, Select, Note, Panel, Confirm } from '../lib/ui';
import { direct, videoTypes, styles, DIRECTOR_FIELDS, cameraMoves, type DirectOutput } from '../director';

export default function Creator() {
  const st = useStudio();
  const p = st.project;
  const [models, setModels] = useState<any[]>([]);
  const [f, setF] = useState({ description: p.description || '', video_type: p.video_type, style: p.style || 'auto', duration: p.duration, model_id: p.model_id });
  const [draft, setDraft] = useState<DirectOutput | null>(null);
  const [confirm, setConfirm] = useState(false);
  useEffect(() => { rpc('models_list').then(setModels).catch(() => {}); }, []);
  const model = models.find((m) => m.id === f.model_id);
  const hasVideos = p.scenes.some((s: any) => s.video_path);

  const runDirector = () => {
    if (f.description.trim().length < 8) { st.toast(L('اكتب وصفًا أوضح للفيلم (8 أحرف على الأقل).', 'Write a clearer description of the film (at least 8 characters).'), 'bad'); return; }
    setDraft(direct({ description: f.description, videoType: f.video_type, style: f.style, duration: f.duration, modelId: f.model_id, maxClipSeconds: model?.max_seconds || 5 }));
  };
  const apply = async () => {
    if (!draft) return;
    await st.save(async () => {
      await rpc('project_update', { id: p.id, patch: { description: f.description, video_type: f.video_type, style: f.style, duration: f.duration, model_id: f.model_id, director: draft.director, status: 'storyboard' } });
      return rpc('storyboard_replace', { project_id: p.id, scenes: draft.scenes });
    });
    st.toast(L('حُفظ الستوري بورد', 'Storyboard saved'), 'ok');
    st.go('storyboard');
  };

  return (
    <Slate title={L('منشئ الفيديو', 'AI Video Creator')} sub={L('صف الفيلم. المخرج الآلي يقرأ الوصف ويتخذ القرارات الإخراجية ويقسّمه إلى مشاهد ويكتب برومبت كل مشهد للنموذج المختار. لا شيء يُرسل إلى أي خادم في هذه الخطوة.', 'Describe the film. The director reads it, takes the directing decisions, splits it into scenes and writes each scene\'s prompt for the chosen model. Nothing is sent to any server at this step.')}>
      <div className="grid grid-cols-[minmax(0,5fr)_minmax(0,6fr)] gap-6 items-start">
        <div className="space-y-4">
          <Field label={L('وصف الفيلم', 'Film description')}><Area data-field="description" rows={8} value={f.description} maxLength={4000} onChange={(e) => setF({ ...f, description: e.target.value })} placeholder={L('مثال: سيارة رياضية سوداء تسير بسرعة في شوارع الرياض ليلًا تحت المطر مع أضواء نيون', 'e.g. A black sports car speeding through rainy Riyadh streets at night with neon lights')} /></Field>
          <div className="grid grid-cols-2 gap-4">
            <Field label={L('نوع الفيديو', 'Video type')}><Select value={f.video_type} onChange={(e) => setF({ ...f, video_type: e.target.value })}>{videoTypes.map((t) => <option key={t.id} value={t.id}>{pick(t)}</option>)}</Select></Field>
            <Field label={L('الأسلوب', 'Style')}><Select value={f.style} onChange={(e) => setF({ ...f, style: e.target.value })}>{styles.map((t) => <option key={t.id} value={t.id}>{pick(t)}</option>)}</Select></Field>
            <Field label={L('المدة (ثانية)', 'Duration (seconds)')}><Input type="number" min={2} max={600} value={f.duration} onChange={(e) => setF({ ...f, duration: Math.max(2, Math.min(600, Number(e.target.value) || 2)) })} /></Field>
            <Field label={L('النموذج', 'Model')} hint={model ? L(`أطول مقطع واحد: ${model.max_seconds.toFixed(1)} ث`, `Longest single clip: ${model.max_seconds.toFixed(1)} s`) : ''}><Select value={f.model_id} onChange={(e) => setF({ ...f, model_id: e.target.value })}>{models.map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}</Select></Field>
          </div>
          <Btn tone="accent" data-action="direct" onClick={runDirector}>{draft ? L('أعد الإخراج', 'Direct again') : L('أخرِج الفيلم', 'Direct the film')}</Btn>
          {!!p.scenes.length && !draft && <Note>{L(`لهذا المشروع ستوري بورد من ${p.scenes.length} مشاهد. إعادة الإخراج تستبدله.`, `This project already has a storyboard of ${p.scenes.length} scenes. Directing again replaces it.`)}</Note>}
        </div>

        <div className="space-y-4">
          {!draft && <div className="border border-dashed border-line-2 rounded-lg p-10 text-center text-mute text-sm">{L('ستظهر هنا القرارات الإخراجية والمشاهد قبل حفظها.', 'The directing decisions and scenes appear here before they are saved.')}</div>}
          {draft && <>
            {draft.director.warnings.map((w, i) => <Note key={i} tone="warn">{pick(w)}</Note>)}
            <Panel title={L('القرارات الإخراجية', 'Directing decisions')} right={<span className="text-xs text-mute">{L(`${draft.director.detected.length} مفهومًا من الوصف`, `${draft.director.detected.length} concepts recognised`)}</span>}>
              <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-[13px]" data-director>
                {DIRECTOR_FIELDS.map((d) => <div key={d.key} className="contents"><dt className="text-mute whitespace-nowrap">{L(d.ar, d.en)}</dt><dd className="ltr text-soft selectable">{String(draft.director[d.key]) || '—'}</dd></div>)}
              </dl>
              {!!draft.director.rationale.length && <ul className="mt-4 pt-3 border-t border-line text-xs text-mute space-y-1 list-disc ps-4">{draft.director.rationale.map((r, i) => <li key={i}>{pick(r)}</li>)}</ul>}
            </Panel>
            <Panel title={L(`المشاهد (${draft.scenes.length})`, `Scenes (${draft.scenes.length})`)}>
              <ol className="space-y-3" data-draft-scenes>
                {draft.scenes.map((s, i) => <li key={i} className="grid grid-cols-[28px_1fr_auto] gap-3 text-[13px]"><span className="num text-accent">{String(i + 1).padStart(2, '0')}</span><span><span className="text-text">{s.title}</span><span className="block text-mute">{s.description}</span><span className="block ltr text-xs text-mute/80 mt-1 line-clamp-2">{s.prompt}</span></span><span className="text-mute text-xs text-end"><span className="num">{s.duration}s</span><br />{pick(cameraMoves.find((m) => m.id === s.camera_move))}</span></li>)}
              </ol>
            </Panel>
            <div className="flex gap-2"><Btn tone="accent" data-action="save-storyboard" onClick={() => (hasVideos ? setConfirm(true) : apply())}>{L('احفظ الستوري بورد', 'Save storyboard')}</Btn><Btn tone="ghost" onClick={() => setDraft(null)}>{L('تجاهل', 'Discard')}</Btn></div>
          </>}
        </div>
      </div>
      {confirm && <Confirm title={L('استبدال الستوري بورد', 'Replace storyboard')} confirmLabel={L('استبدال', 'Replace')} onClose={() => setConfirm(false)} onConfirm={apply}
        text={<p>{L('توجد مقاطع مولَّدة لهذا المشروع. ستُنقل إلى مجلد ‎_replaced‎ داخل المشروع (لا تُحذف) وتبدأ المشاهد الجديدة بلا مقاطع.', 'This project has generated clips. They will be moved to the project\'s _replaced folder (not deleted) and the new scenes start without clips.')}</p>} />}
    </Slate>
  );
}
