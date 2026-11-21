import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, statusText, fmtDate, fmtDuration } from '../lib/i18n';
import { rpc, fileUrl, inLibrary, pickFiles, pickSavePath } from '../lib/rpc';
import { Btn, Slate, Tag, Empty, Note, Confirm, Meter } from '../lib/ui';

export default function Dashboard() {
  const st = useStudio();
  const { status, go, run } = st;
  const [projects, setProjects] = useState<any[] | null>(null);
  const [del, setDel] = useState<any | null>(null);
  const load = () => rpc('projects_list').then(setProjects).catch(() => setProjects([]));
  useEffect(() => { load(); }, [st.jobs.length]);
  const root = status.library_root;
  const last = projects?.find((p) => p.id === status.last_project) || projects?.[0];

  const importProject = async () => {
    const [path] = await pickFiles({ filters: [{ name: 'Cinematic Studio project', extensions: ['zip'] }], title: L('ملف المشروع', 'Project file') });
    if (!path) return;
    const p: any = await run(() => rpc('project_import_archive', { path }), L('تم استيراد المشروع', 'Project imported'));
    if (p) { load(); st.openProject(p.id); }
  };
  const act = async (kind: string, p: any) => {
    if (kind === 'duplicate') { await run(() => rpc('project_duplicate', { id: p.id }), L('أُنشئت نسخة من المشروع', 'Project duplicated')); load(); }
    if (kind === 'backup') { const b: any = await run(() => rpc('project_backup', { id: p.id })); if (b) st.toast(`${L('نسخة احتياطية في', 'Backup saved to')} ${b.path}`, 'ok'); }
    if (kind === 'export') { const dest = await pickSavePath(`${p.name}.zip`, [{ name: 'Zip', extensions: ['zip'] }]); if (dest) await run(() => rpc('project_export_archive', { id: p.id, dest }), L('تم تصدير المشروع', 'Project exported')); }
    if (kind === 'check') { const r: any = await run(() => rpc('project_integrity', { id: p.id })); if (r) { const n = r.missing_videos.length + r.corrupted_videos.length + r.missing_media.length; st.toast(n ? L(`وُجدت ${n} ملفات مفقودة أو تالفة. المشاهد المتأثرة أُعيدت إلى «لم يُولَّد».`, `${n} missing or corrupted file(s) found. Affected scenes were reset to "not generated".`) : L('كل ملفات المشروع سليمة', 'All project files are intact'), n ? 'bad' : 'ok'); load(); } }
  };

  return (
    <Slate title={L('الاستوديو', 'Studio')} sub={L('مشاريعك محفوظة على هذا الجهاز. التوليد يعمل على خادم ComfyUI الذي تضبطه أنت.', 'Your projects are stored on this computer. Generation runs on the ComfyUI server you configure.')}
      actions={<><Btn onClick={importProject}>{L('استيراد مشروع', 'Import project')}</Btn><Btn tone="accent" data-action="new-project" onClick={() => go('new')}>{L('مشروع جديد', 'New project')}</Btn></>}>
      {status.recovered && <div className="mb-5"><Note tone="warn">{L(`أُغلق التطبيق آخر مرة بشكل غير طبيعي. مشاريعك سليمة لأنها تُحفظ مع كل تعديل${status.recovered_jobs ? `، و${status.recovered_jobs} مهمة كانت تعمل أُعيدت إلى قائمة التنفيذ.` : '.'}`, `The app did not close normally last time. Your projects are intact because every edit is saved${status.recovered_jobs ? `, and ${status.recovered_jobs} job(s) that were running are back in the queue.` : '.'}`)}</Note></div>}

      <div className="grid grid-cols-3 gap-px bg-line border border-line rounded-lg overflow-hidden mb-8 text-sm">
        <button type="button" className="bg-panel p-4 text-start hover:bg-raised" onClick={() => go('settings')}>
          <p className="text-xs text-mute">{L('خادم التوليد', 'Generation server')}</p>
          <p className="mt-1.5">{status.settings.comfy_url ? <span className="ltr">{status.settings.comfy_url}</span> : L('غير مضبوط', 'Not configured')}</p>
          <p className="text-xs text-mute mt-1">{status.settings.comfy_url ? 'ComfyUI · Wan 2.2' : L('أضف عنوان ComfyUI لتفعيل التوليد', 'Add a ComfyUI address to enable generation')}</p>
        </button>
        <button type="button" className="bg-panel p-4 text-start hover:bg-raised" onClick={() => go('gpu')}>
          <p className="text-xs text-mute">{L('ميزانية GPU لهذا الشهر', 'GPU budget this month')}</p>
          <p className="mt-1.5 num">{status.budget.spent_sar.toFixed(2)} / {status.budget.limit_sar.toFixed(0)} SAR</p>
          <div className="mt-2.5"><Meter value={status.budget.percent / 100} tone={status.budget.level === 'blocked' ? 'bad' : 'accent'} /></div>
        </button>
        <button type="button" className="bg-panel p-4 text-start hover:bg-raised" onClick={() => go('queue')}>
          <p className="text-xs text-mute">{L('قائمة التنفيذ', 'Render queue')}</p>
          <p className="mt-1.5">{status.counts.active_jobs ? L(`${status.counts.active_jobs} مهمة نشطة`, `${status.counts.active_jobs} active job(s)`) : L('لا مهام نشطة', 'No active jobs')}</p>
          <p className="text-xs text-mute mt-1">{status.ffmpeg ? 'FFmpeg ✓' : L('FFmpeg غير موجود', 'FFmpeg not found')}</p>
        </button>
      </div>

      {projects && !projects.length && <Empty title={L('لا توجد مشاريع بعد', 'No projects yet')} text={L('ابدأ بوصف الفيلم بالعربية أو الإنجليزية؛ المخرج الآلي يحوّله إلى قرارات إخراجية وستوري بورد قابل للتعديل.', 'Start by describing the film in Arabic or English; the director turns it into directing decisions and an editable storyboard.')} action={<Btn tone="accent" onClick={() => go('new')}>{L('مشروع جديد', 'New project')}</Btn>} />}

      {last && <button type="button" data-open-last onClick={() => st.openProject(last.id)} className="w-full text-start mb-8 grid grid-cols-[320px_1fr] bg-panel border border-line rounded-lg overflow-hidden hover:border-line-2">
        <div className="aspect-video bg-black">{last.preview_path && <img src={fileUrl(inLibrary(root, last.preview_path))} alt="" className="w-full h-full object-cover" />}</div>
        <div className="p-6 flex flex-col justify-center min-w-0">
          <p className="text-xs text-accent">{L('تابع العمل', 'Continue')}</p>
          <p className="text-xl font-semibold mt-1 truncate">{last.name}</p>
          <p className="text-sm text-mute mt-2 line-clamp-2">{last.description}</p>
          <div className="mt-4 flex items-center gap-3 text-xs text-mute"><Tag status={last.status} /><span className="num">{last.scenes_done}/{last.scene_count}</span>{L('مشاهد', 'scenes')}<span className="num">{fmtDuration(last.duration)}</span><span>{fmtDate(last.updated_at)}</span></div>
        </div>
      </button>}

      {!!projects?.length && <>
        <h2 className="text-xs text-mute mb-3">{L('كل المشاريع', 'All projects')} <span className="num">({projects.length})</span></h2>
        <div className="border border-line rounded-lg overflow-hidden divide-y divide-line">
          {projects.map((p) => (
            <div key={p.id} data-project={p.id} className="flex items-center gap-4 px-4 py-3 bg-panel hover:bg-raised/70">
              <button type="button" className="flex-1 min-w-0 flex items-center gap-4 text-start" onClick={() => st.openProject(p.id)}>
                <span className="w-24 aspect-video bg-black rounded-sm overflow-hidden shrink-0">{p.preview_path && <img src={fileUrl(inLibrary(root, p.preview_path))} alt="" className="w-full h-full object-cover" />}</span>
                <span className="min-w-0 flex-1"><span className="block truncate">{p.name}</span><span className="block text-xs text-mute">{fmtDate(p.updated_at)} · <span className="num">{p.scenes_done}/{p.scene_count}</span> · <span className="num">{p.aspect}</span></span></span>
                <Tag status={p.status}>{statusText(p.status)}</Tag>
              </button>
              <div className="flex gap-1 shrink-0">
                <Btn small tone="ghost" onClick={() => act('duplicate', p)}>{L('نسخ', 'Duplicate')}</Btn>
                <Btn small tone="ghost" onClick={() => act('backup', p)}>{L('نسخة احتياطية', 'Back up')}</Btn>
                <Btn small tone="ghost" onClick={() => act('export', p)}>{L('تصدير', 'Export')}</Btn>
                <Btn small tone="ghost" onClick={() => act('check', p)}>{L('فحص الملفات', 'Check files')}</Btn>
                <Btn small tone="ghost" className="hover:!text-bad" data-delete={p.id} onClick={() => setDel(p)}>{L('حذف', 'Delete')}</Btn>
              </div>
            </div>
          ))}
        </div>
      </>}
      {del && <Confirm danger title={L('حذف المشروع', 'Delete project')} confirmLabel={L('حذف', 'Delete')} onClose={() => setDel(null)}
        text={<p>{L(`سيُزال «${del.name}» من القائمة. ملفاته تُنقل إلى مجلد Backups/Deleted داخل مكتبتك ولا تُمحى نهائيًا.`, `"${del.name}" will be removed from the list. Its files are moved to Backups/Deleted inside your library, not erased.`)}</p>}
        onConfirm={async () => { await run(() => rpc('project_delete', { id: del.id })); if (st.project?.id === del.id) st.closeProject(); load(); st.refreshStatus(); }} />}
    </Slate>
  );
}
