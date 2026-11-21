import { useState } from 'react';
import { useStudio, useDebounced } from '../lib/store';
import { L, pick } from '../lib/i18n';
import { rpc } from '../lib/rpc';
import { Btn, Slate, Field, Area, Note, Panel, Empty } from '../lib/ui';
import { DIRECTOR_FIELDS, profileFor, compileOne, type Director } from '../director';
import { recompileProject, toDraft } from '../lib/project';

export default function PromptEditor() {
  const st = useStudio();
  const p = st.project;
  const [d, setD] = useState<Director | null>(p.director || null);
  const persist = useDebounced((next: Director) => st.save(() => rpc('project_update', { id: p.id, patch: { director: next } })), 600);
  if (!d) return <Slate title={L('محرر البرومبت السينمائي', 'Cinematic Prompt Editor')}><Empty title={L('لم يُخرَج هذا المشروع بعد', 'This project has not been directed yet')} text={L('ابدأ من «منشئ الفيديو» ليتخذ المخرج القرارات، ثم عدّلها هنا.', 'Start in the AI Video Creator so the director takes its decisions, then adjust them here.')} action={<Btn tone="accent" onClick={() => st.go('creator')}>{L('منشئ الفيديو', 'AI Video Creator')}</Btn>} /></Slate>;
  const profile = profileFor(p.model_id);
  const set = (k: keyof Director, v: string) => { const next = { ...d, [k]: v }; setD(next); persist(next); };
  const stale = p.scenes.filter((s: any) => !s.prompt_edited && compileOne(toDraft(s, d, p.scenes), d, p.model_id, s.position, p.scenes.length).prompt !== s.prompt).length;
  const edited = p.scenes.filter((s: any) => s.prompt_edited).length;
  const apply = async (force: boolean) => { await st.save(async () => { await rpc('project_update', { id: p.id, patch: { director: d } }); return recompileProject(p, d, p.model_id, undefined, force); }); st.toast(L('حُدّثت برومبتات المشاهد', 'Scene prompts updated'), 'ok'); };

  return (
    <Slate title={L('محرر البرومبت السينمائي', 'Cinematic Prompt Editor')} sub={L('هذه قرارات المخرج الاثنا عشر. عدّل أي قرار ثم طبّقه على المشاهد. القيم بالإنجليزية لأنها ما يقرؤه النموذج.', 'These are the director\'s twelve decisions. Change any of them, then apply to the scenes. Values are in English because that is what the model reads.')}
      actions={<><Btn data-action="apply-prompts" tone="accent" disabled={!stale} onClick={() => apply(false)}>{stale ? L(`طبّق على ${stale} مشاهد`, `Apply to ${stale} scene(s)`) : L('المشاهد محدَّثة', 'Scenes up to date')}</Btn></>}>
      <div className="grid grid-cols-[minmax(0,3fr)_minmax(0,2fr)] gap-6 items-start">
        <div className="grid grid-cols-2 gap-4">
          {DIRECTOR_FIELDS.map((f) => <Field key={f.key} label={<>{L(f.ar, f.en)}{st.lang === 'ar' && <span className="ltr ms-2 text-mute/60">{f.en}</span>}</>} className={f.key === 'negative_instructions' ? 'col-span-2' : ''}><Area data-director-field={f.key} rows={f.key === 'negative_instructions' ? 3 : 2} className="ltr" value={String(d[f.key] || '')} onChange={(e) => set(f.key, e.target.value)} /></Field>)}
        </div>
        <div className="space-y-4">
          <Panel title={L('ملف البرومبت للنموذج', 'Model prompt profile')}>
            <p className="ltr text-sm mb-2">{profile.label}</p>
            <ul className="text-[13px] text-soft space-y-1.5 list-disc ps-4">{profile.notes.map((n, i) => <li key={i}>{pick(n)}</li>)}<li>{L(`الحد الأقصى ${profile.maxChars} حرفًا لكل برومبت.`, `At most ${profile.maxChars} characters per prompt.`)}</li></ul>
            {profile.negative === 'ignored' && <div className="mt-3"><Note tone="warn">{L('حقل «تعليمات الاستبعاد» لا يؤثر مع هذا النموذج.', 'The "Negative Instructions" field has no effect with this model.')}</Note></div>}
          </Panel>
          {!!d.warnings?.length && d.warnings.map((w, i) => <Note key={i} tone="warn">{pick(w)}</Note>)}
          {!!edited && <Note>{L(`${edited} مشاهد عُدّل برومبتها يدويًا ولن تتغير.`, `${edited} scene(s) have a hand-edited prompt and will not change.`)} <button type="button" className="underline text-accent" onClick={() => apply(true)}>{L('أعد كتابتها من القرارات', 'Rewrite them from the decisions')}</button></Note>}
          <Panel title={L('معاينة برومبت كل مشهد', 'Prompt preview per scene')}>
            <ol className="space-y-3">{p.scenes.map((s: any) => { const c = compileOne(toDraft(s, d, p.scenes), d, p.model_id, s.position, p.scenes.length); const text = s.prompt_edited ? s.prompt : c.prompt; return <li key={s.id} className="text-[13px]"><div className="flex justify-between text-xs text-mute mb-1"><span><span className="num text-accent">{String(s.position + 1).padStart(2, '0')}</span> {s.title}{s.prompt_edited ? ` · ${L('يدوي', 'hand-edited')}` : ''}</span><span className="num">{text.length}/{profile.maxChars}</span></div><p className="ltr text-soft selectable leading-relaxed">{text}</p></li>; })}</ol>
          </Panel>
          {!!d.rationale?.length && <Panel title={L('لماذا هذه القرارات', 'Why these decisions')}><ul className="text-[13px] text-soft space-y-1.5 list-disc ps-4">{d.rationale.map((r, i) => <li key={i}>{pick(r)}</li>)}</ul></Panel>}
        </div>
      </div>
    </Slate>
  );
}
