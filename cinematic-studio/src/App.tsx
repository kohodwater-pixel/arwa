import { useEffect, useState, type ReactNode } from 'react';
import { useStudio, isActive, type View } from './lib/store';
import { L, reasonText } from './lib/i18n';
import { cx, Btn, Meter } from './lib/ui';
import { isTauri, rpc } from './lib/rpc';
import Dashboard from './screens/Dashboard';
import NewProject from './screens/NewProject';
import Creator from './screens/Creator';
import PromptEditor from './screens/PromptEditor';
import Storyboard from './screens/Storyboard';
import SceneEditor from './screens/SceneEditor';
import Timeline from './screens/Timeline';
import Preview from './screens/Preview';
import Audio from './screens/Audio';
import Media from './screens/Media';
import Models from './screens/Models';
import Gpu from './screens/Gpu';
import Queue from './screens/Queue';
import ExportCenter from './screens/ExportCenter';
import Settings from './screens/Settings';

type Item = { id: View; ar: string; en: string };
// The film's own pipeline, in the order a film is made.
const FILM: Item[] = [
  { id: 'creator', ar: 'منشئ الفيديو', en: 'AI Video Creator' }, { id: 'prompt', ar: 'محرر البرومبت', en: 'Prompt Editor' },
  { id: 'storyboard', ar: 'الستوري بورد', en: 'Storyboard Studio' }, { id: 'scene', ar: 'محرر المشهد', en: 'Scene Editor' },
  { id: 'timeline', ar: 'الخط الزمني', en: 'Timeline Editor' }, { id: 'audio', ar: 'استوديو الصوت', en: 'Audio Studio' },
  { id: 'preview', ar: 'المعاينة', en: 'Video Preview' }, { id: 'export', ar: 'مركز التصدير', en: 'Export Center' },
];
const HOUSE: Item[] = [
  { id: 'media', ar: 'مكتبة الوسائط', en: 'Media Library' }, { id: 'models', ar: 'النماذج و LoRA', en: 'Model Manager' },
  { id: 'gpu', ar: 'إدارة GPU', en: 'GPU Manager' }, { id: 'queue', ar: 'قائمة التنفيذ', en: 'Render Queue' }, { id: 'settings', ar: 'الإعدادات', en: 'Settings' },
];
const SCREENS: Record<View, () => ReactNode> = {
  dashboard: () => <Dashboard />, new: () => <NewProject />, creator: () => <Creator />, prompt: () => <PromptEditor />, storyboard: () => <Storyboard />, scene: () => <SceneEditor />,
  timeline: () => <Timeline />, preview: () => <Preview />, audio: () => <Audio />, media: () => <Media />, models: () => <Models />, gpu: () => <Gpu />, queue: () => <Queue />, export: () => <ExportCenter />, settings: () => <Settings />,
};
const NEEDS_PROJECT: View[] = ['creator', 'prompt', 'storyboard', 'scene', 'timeline', 'preview', 'audio', 'export'];

function NavButton({ item, n, active, disabled, badge, onClick }: { item: Item; n?: number; active: boolean; disabled?: boolean; badge?: ReactNode; onClick: () => void }) {
  return (
    <button type="button" data-nav={item.id} disabled={disabled} aria-current={active ? 'page' : undefined} onClick={onClick}
      className={cx('group w-full flex items-center gap-3 h-9 ps-4 pe-3 text-[13px] text-start border-s-2 transition-colors disabled:opacity-35 disabled:pointer-events-none', active ? 'border-accent bg-raised text-text' : 'border-transparent text-soft hover:text-text hover:bg-panel')}>
      {n !== undefined && <span className={cx('num text-[10px] w-4', active ? 'text-accent' : 'text-mute')}>{String(n).padStart(2, '0')}</span>}
      <span className="flex-1 truncate">{L(item.ar, item.en)}</span>{badge}
    </button>
  );
}

export default function App() {
  const st = useStudio();
  const { status, view, project, jobs, go, toasts, saving, bootError } = st;
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => { const f = () => setOnline(navigator.onLine); window.addEventListener('online', f); window.addEventListener('offline', f); return () => { window.removeEventListener('online', f); window.removeEventListener('offline', f); }; }, []);
  // Files dropped on the window go to the media library (the desktop shell reports their real paths).
  useEffect(() => {
    if (!isTauri) return;
    let un: (() => void) | undefined;
    import('@tauri-apps/api/webview').then(({ getCurrentWebview }) => getCurrentWebview().onDragDropEvent(async (e) => {
      if (e.payload.type !== 'drop' || !e.payload.paths.length) return;
      const paths = e.payload.paths;
      const r: any[] | undefined = await st.run(() => rpc('media_import', { paths, project_id: project?.id }));
      if (r) { st.toast(L(`أُضيف ${r.filter((x) => x.ok && !x.duplicate).length} ملفًا إلى المكتبة`, `${r.filter((x) => x.ok && !x.duplicate).length} file(s) added to the library`), 'ok'); window.dispatchEvent(new Event('media-changed')); }
    })).then((u) => { un = u; });
    return () => un?.();
  }, [project?.id]); // eslint-disable-line react-hooks/exhaustive-deps

  if (bootError && !status) return <div className="h-full grid place-items-center"><div className="text-center"><p className="text-lg">{bootError}</p><Btn className="mt-4" onClick={() => st.refreshStatus()}>{L('إعادة المحاولة', 'Retry')}</Btn></div></div>;
  if (!status) return <div className="h-full grid place-items-center text-mute">Cinematic Studio</div>;

  const active = jobs.filter(isActive);
  const running = active.find((j) => ['running', 'submitted', 'downloading'].includes(j.status));
  const blocked = active.find((j) => j.status === 'blocked');
  const b = status.budget;
  const needs = NEEDS_PROJECT.includes(view) && !project;

  return (
    <div className="h-full grid grid-cols-[232px_1fr] grid-rows-[1fr_30px]">
      <aside className="row-span-1 bg-stage border-e border-line flex flex-col min-h-0">
        <div className="px-4 pt-5 pb-4">
          <div className="flex items-center gap-2.5"><span className="size-2.5 rounded-full bg-accent" /><span className="ltr font-semibold tracking-[0.14em] text-[12px]">CINEMATIC STUDIO</span></div>
        </div>
        <nav className="flex-1 overflow-y-auto pb-4" aria-label={L('التنقل', 'Navigation')}>
          <NavButton item={{ id: 'dashboard', ar: 'الاستوديو', en: 'Dashboard' }} active={view === 'dashboard'} onClick={() => go('dashboard')} />
          <NavButton item={{ id: 'new', ar: 'مشروع جديد', en: 'New Project' }} active={view === 'new'} onClick={() => go('new')} />
          <div className="mt-5 mb-1.5 px-4">
            <p className="text-[11px] text-mute">{L('الفيلم', 'Film')}</p>
            <p className={cx('text-[13px] truncate mt-0.5', project ? 'text-text' : 'text-mute')} title={project?.name}>{project ? project.name : L('لا يوجد مشروع مفتوح', 'No project open')}</p>
          </div>
          {FILM.map((it, i) => <NavButton key={it.id} item={it} n={i + 1} active={view === it.id} disabled={!project} onClick={() => go(it.id)} />)}
          <p className="mt-5 mb-1.5 px-4 text-[11px] text-mute">{L('الورشة', 'Workshop')}</p>
          {HOUSE.map((it) => <NavButton key={it.id} item={it} active={view === it.id} onClick={() => go(it.id)} badge={it.id === 'queue' && active.length ? <span className="num text-[10px] text-accent">{active.length}</span> : undefined} />)}
        </nav>
        <div className="p-3 border-t border-line flex gap-1.5">
          {(['ar', 'en'] as const).map((l) => <button key={l} type="button" data-lang={l} onClick={() => st.setLanguage(l)} className={cx('flex-1 h-7 rounded text-xs', st.lang === l ? 'bg-raised text-text' : 'text-mute hover:text-soft')}>{l === 'ar' ? 'العربية' : 'English'}</button>)}
        </div>
      </aside>

      <main className="min-h-0 min-w-0 bg-ink" data-view={view}>
        {needs ? <div className="h-full grid place-items-center"><div className="text-center"><p className="text-soft">{L('افتح مشروعًا أو أنشئ مشروعًا جديدًا أولًا.', 'Open a project or create a new one first.')}</p><div className="mt-4 flex gap-2 justify-center"><Btn onClick={() => go('dashboard')}>{L('المشاريع', 'Projects')}</Btn><Btn tone="accent" onClick={() => go('new')}>{L('مشروع جديد', 'New project')}</Btn></div></div></div> : SCREENS[view]()}
      </main>

      {/* status strip: what the machine is doing right now */}
      <footer className="col-span-2 bg-stage border-t border-line flex items-center gap-5 px-4 text-[11px] text-mute overflow-hidden whitespace-nowrap">
        <button type="button" className="flex items-center gap-1.5 hover:text-soft" onClick={() => go('queue')}>
          <i className={cx('size-1.5 rounded-full', running ? 'bg-accent live' : blocked ? 'bg-bad' : 'bg-line-2')} />
          {running ? <>{L('يعمل', 'Working')}: {running.kind === 'export' ? L('تصدير', 'export') : `${L('مشهد', 'scene')} ${(running.scene_position ?? 0) + 1}`} <span className="num">{Math.round((running.progress || 0) * 100)}%</span></> : blocked ? <>{L('متوقف', 'Waiting')}: {reasonText(blocked.blocked_reason)}</> : active.length ? <>{active.length} {L('في الانتظار', 'queued')}</> : L('لا مهام', 'Idle')}
        </button>
        <button type="button" className="flex items-center gap-1.5 hover:text-soft" onClick={() => go('settings')}><i className={cx('size-1.5 rounded-full', status.settings.comfy_url ? 'bg-ok' : 'bg-line-2')} />ComfyUI: {status.settings.comfy_url ? <span className="ltr">{new URL(status.settings.comfy_url).host}</span> : L('غير مضبوط', 'not configured')}</button>
        <button type="button" className="flex items-center gap-2 hover:text-soft" onClick={() => go('gpu')}>
          {L('ميزانية GPU', 'GPU budget')} <span className="w-20"><Meter value={b.percent / 100} tone={b.level === 'blocked' ? 'bad' : 'accent'} /></span>
          <span className={cx('num', b.level !== 'ok' && 'text-accent', b.level === 'blocked' && 'text-bad')}>{b.spent_sar.toFixed(0)} / {b.limit_sar.toFixed(0)} SAR</span>
        </button>
        {!status.ffmpeg && <button type="button" className="text-bad" onClick={() => go('settings')}>{L('FFmpeg غير موجود', 'FFmpeg not found')}</button>}
        <span className="ms-auto flex items-center gap-4">
          {!online && <span className="text-accent">{L('بلا اتصال — العمل المحلي متاح', 'Offline — local work available')}</span>}
          <span data-save-state={saving ? 'saving' : 'saved'}>{saving ? L('يحفظ…', 'Saving…') : L('حُفظ تلقائيًا', 'Auto-saved')}</span>
          <span className="num">v{status.version}</span>
        </span>
      </footer>

      <div className="fixed bottom-12 end-5 z-50 flex flex-col gap-2 w-[380px] max-w-[90vw]" aria-live="polite">
        {toasts.map((t) => <div key={t.id} data-toast={t.kind} className={cx('rounded-md border px-4 py-3 text-sm bg-raised shadow-xl selectable', t.kind === 'bad' ? 'border-bad/60' : t.kind === 'ok' ? 'border-ok/50' : 'border-line-2')}>{t.text}</div>)}
      </div>
    </div>
  );
}
