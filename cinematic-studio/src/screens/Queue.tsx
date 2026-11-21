import { useStudio, isActive } from '../lib/store';
import { L, fmtDate, statusText, reasonText } from '../lib/i18n';
import { rpc } from '../lib/rpc';
import { Btn, Slate, Tag, Meter, Empty, Note } from '../lib/ui';

export default function Queue() {
  const st = useStudio();
  const jobs = st.jobs;
  const active = jobs.filter(isActive);
  const blocked = [...new Set(active.filter((j) => j.status === 'blocked').map((j) => j.blocked_reason))];
  const act = (cmd: string, id: string) => st.run(() => rpc(cmd, { id }));
  return (
    <Slate title={L('قائمة التنفيذ', 'Render Queue')} sub={L('مهام التوليد والتصدير بالترتيب. مهمة توليد واحدة تعمل في كل مرة على خادم ComfyUI.', 'Generation and export jobs in order. One generation job runs at a time on the ComfyUI server.')}
      actions={<Btn disabled={!jobs.some((j) => !isActive(j))} onClick={() => st.run(() => rpc('jobs_clear_finished'))}>{L('امسح المنتهية', 'Clear finished')}</Btn>}>
      {blocked.map((r) => <div key={r} className="mb-4"><Note tone="warn">{reasonText(r)} {r?.startsWith('comfy') && <button type="button" className="underline text-accent" onClick={() => st.go('settings')}>{L('الإعدادات', 'Settings')}</button>}{(r === 'gpu_stopped' || r === 'budget_exceeded') && <button type="button" className="underline text-accent" onClick={() => st.go('gpu')}>{L('إدارة GPU', 'GPU Manager')}</button>}<span className="block text-xs text-mute mt-1">{L('المهام المتوقفة تُعاد محاولتها تلقائيًا عند زوال السبب.', 'Waiting jobs are retried automatically once the cause is gone.')}</span></Note></div>)}
      {!jobs.length && <Empty title={L('القائمة فارغة', 'The queue is empty')} text={L('تظهر هنا المهام عند طلب توليد مشهد أو تصدير فيلم.', 'Jobs appear here when you generate a scene or export a film.')} />}
      <div className="border border-line rounded-lg overflow-hidden divide-y divide-line" data-queue>
        {jobs.map((j) => (
          <div key={j.id} data-job={j.status} className="bg-panel px-4 py-3 grid grid-cols-[110px_minmax(0,1.4fr)_minmax(0,1fr)_150px_auto] gap-4 items-center text-sm">
            <Tag status={j.status} />
            <div className="min-w-0"><p className="truncate">{j.kind === 'export' ? L('تصدير الفيلم', 'Film export') : <>{L('مشهد', 'Scene')} <span className="num">{(j.scene_position ?? 0) + 1}</span> — {j.scene_title || L('(حُذف)', '(deleted)')}</>}</p><p className="text-xs text-mute truncate">{j.project_name} · <span className="ltr">{j.kind === 'export' ? 'FFmpeg' : j.model_id}</span>{j.attempts > 1 ? ` · ${L('محاولة', 'attempt')} ${j.attempts}` : ''}</p></div>
            <div className="min-w-0">{isActive(j) && j.status !== 'blocked' && j.status !== 'queued' ? <><Meter value={j.progress || 0} /><p className="text-[11px] text-mute mt-1 truncate">{j.stage || statusText(j.status)} <span className="num">{Math.round((j.progress || 0) * 100)}%</span></p></> : j.status === 'blocked' ? <p className="text-xs text-accent truncate">{reasonText(j.blocked_reason)}</p> : j.error ? <p className="text-xs text-bad line-clamp-2 selectable" title={j.error}>{j.error}</p> : null}</div>
            <span className="text-xs text-mute">{fmtDate(j.finished_at || j.started_at || j.created_at)}</span>
            <span className="flex gap-1 justify-end">
              {isActive(j) && <Btn small data-action="cancel" onClick={() => act('job_cancel', j.id)}>{L('إلغاء', 'Cancel')}</Btn>}
              {['failed', 'canceled'].includes(j.status) && <Btn small data-action="retry" onClick={() => act('job_retry', j.id)}>{L('أعد المحاولة', 'Retry')}</Btn>}
              {j.kind === 'generate' && j.status === 'succeeded' && <Btn small tone="ghost" onClick={async () => { await st.openProject(j.project_id); st.go('scene', j.scene_id); }}>{L('افتح', 'Open')}</Btn>}
            </span>
          </div>
        ))}
      </div>
    </Slate>
  );
}
