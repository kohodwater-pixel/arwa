import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { rpc, fileUrl, isTauri } from './rpc';
import { errText, setLang, L, type Lang } from './i18n';

export type View = 'dashboard' | 'new' | 'creator' | 'prompt' | 'storyboard' | 'scene' | 'timeline' | 'preview' | 'audio' | 'media' | 'models' | 'gpu' | 'queue' | 'export' | 'settings';
export type Toast = { id: number; kind: 'ok' | 'bad' | 'info'; text: string };
type Ctx = {
  status: any; lang: Lang; view: View; project: any | null; jobs: any[]; sceneId: string | null; toasts: Toast[]; saving: boolean; bootError: string | null;
  go: (v: View, sceneId?: string) => void; setLanguage: (l: Lang) => void;
  refreshStatus: () => Promise<void>; openProject: (id: string, view?: View) => Promise<void>; closeProject: () => void; refreshProject: () => Promise<void>; setProject: (p: any) => void;
  /** Runs a core call; shows the error as a toast and returns undefined when it fails. */
  run: <T>(fn: () => Promise<T>, okText?: string) => Promise<T | undefined>;
  /** Saves an edit to the core (this is the auto-save: every edit is written to SQLite as it is made). */
  save: (fn: () => Promise<any>) => Promise<void>;
  toast: (text: string, kind?: Toast['kind']) => void;
};
const C = createContext<Ctx>(null as any);
export const useStudio = () => useContext(C);
const ACTIVE = ['queued', 'blocked', 'submitted', 'running', 'downloading'];
export const isActive = (j: any) => ACTIVE.includes(j.status);

export function StudioProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<any>(null);
  const [lang, setL] = useState<Lang>('ar');
  const [view, setView] = useState<View>('dashboard');
  const [project, setProject] = useState<any | null>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [sceneId, setSceneId] = useState<string | null>(null);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [saving, setSaving] = useState(false);
  const [bootError, setBootError] = useState<string | null>(null);
  const projectRef = useRef<any>(null); projectRef.current = project;
  const pending = useRef(0);
  // Bumped whenever an edit is written. A background re-read that started before the latest write is thrown
  // away, so a slow refresh can never put an older copy of the project back on screen.
  const epoch = useRef(0);

  const toast = useCallback((text: string, kind: Toast['kind'] = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t.slice(-3), { id, kind, text }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), kind === 'bad' ? 9000 : 4000);
  }, []);
  const run = useCallback(async <T,>(fn: () => Promise<T>, okText?: string) => {
    try { const r = await fn(); if (okText) toast(okText, 'ok'); return r; } catch (e) { toast(errText(e), 'bad'); return undefined; }
  }, [toast]);
  const save = useCallback(async (fn: () => Promise<any>) => {
    pending.current++; setSaving(true); epoch.current++;
    try { const p = await fn(); epoch.current++; if (p && p.scenes) setProject(p); } catch (e) { epoch.current++; toast(errText(e), 'bad'); } finally { if (--pending.current === 0) setSaving(false); }
  }, [toast]);

  const refreshStatus = useCallback(async () => {
    try { const s = await rpc('app_status'); setStatus(s); setBootError(null); return s; } catch (e) { setBootError(errText(e)); }
  }, []);
  const refreshProject = useCallback(async () => { const id = projectRef.current?.id; if (!id) return; const at = epoch.current; try { const p = await rpc('project_get', { id }); if (at === epoch.current && projectRef.current?.id === id) setProject(p); } catch { /* deleted elsewhere */ } }, []);
  const openProject = useCallback(async (id: string, v: View = 'storyboard') => {
    const p = await run(() => rpc('project_get', { id }));
    if (p) { setProject(p); setView(p.scenes.length ? v : 'creator'); }
  }, [run]);
  const setLanguage = useCallback((l: Lang) => { setLang(l); setL(l); rpc('setting_set', { key: 'language', value: l }).then(setStatus).catch(() => {}); }, []);

  useEffect(() => { (async () => { const s: any = await refreshStatus(); const l = (s?.settings?.language as Lang) || 'ar'; setLang(l); setL(l); })(); }, [refreshStatus]);
  // Once per start: can this machine's FFmpeg render, and can this web view show the result? (see rpc self_check)
  useEffect(() => {
    let done = false;
    (async () => {
      const c: any = await rpc('self_check').catch(() => null);
      if (!c || done) return;
      let why = '';
      const image_ok = c.image ? await new Promise<boolean>((resolve) => { const i = new Image(); const t = setTimeout(() => resolve(false), 10000); i.onload = () => { clearTimeout(t); resolve(i.naturalWidth > 0); }; i.onerror = () => { clearTimeout(t); resolve(false); }; i.src = fileUrl(c.image); }) : false;
      const video_ok = c.path ? await new Promise<boolean>((resolve) => { const v = document.createElement('video'); const t = setTimeout(() => { why = 'timeout'; resolve(false); }, 15000); v.preload = 'auto'; v.muted = true; v.onloadeddata = () => { clearTimeout(t); resolve(v.videoWidth > 0 && v.duration > 0.5); }; v.onerror = () => { clearTimeout(t); why = `media error ${v.error?.code ?? ''} ${v.error?.message ?? ''}`; resolve(false); }; v.src = fileUrl(c.path); }) : false;
      await rpc('self_check_report', { ffmpeg_ok: !!c.ffmpeg_ok, video_ok, image_ok, detail: `${why ? why + ' | ' : ''}${navigator.userAgent}` }).catch(() => {});
      if (isTauri && c.ffmpeg_ok && !video_ok) toast(L('تعذّر عرض مقطع اختباري داخل التطبيق. قد لا تعمل المعاينة على هذا الجهاز.', 'A test clip could not be shown inside the app. Preview may not work on this computer.'), 'bad');
    })();
    return () => { done = true; };
  }, [toast]);

  // The queue is polled (the core has no push channel to the web view): fast while something is running.
  const lastSig = useRef('');
  useEffect(() => {
    let stop = false, timer: any;
    const tick = async () => {
      try {
        const list: any[] = await rpc('jobs_list');
        if (stop) return;
        setJobs(list);
        const sig = list.map((j) => j.id + j.status).join('|');
        if (sig !== lastSig.current) { lastSig.current = sig; refreshProject(); refreshStatus(); }
        timer = setTimeout(tick, list.some(isActive) ? 1200 : 4000);
      } catch { timer = setTimeout(tick, 5000); }
    };
    tick();
    return () => { stop = true; clearTimeout(timer); };
  }, [refreshProject, refreshStatus]);

  const go = useCallback((v: View, sid?: string) => { if (sid !== undefined) setSceneId(sid); setView(v); }, []);
  const closeProject = useCallback(() => { setProject(null); setView('dashboard'); }, []);
  const value = useMemo(() => ({ status, lang, view, project, jobs, sceneId, toasts, saving, bootError, go, setLanguage, refreshStatus: async () => { await refreshStatus(); }, openProject, closeProject, refreshProject, setProject, run, save, toast }),
    [status, lang, view, project, jobs, sceneId, toasts, saving, bootError, go, setLanguage, refreshStatus, openProject, closeProject, refreshProject, run, save, toast]);
  return <C.Provider value={value}>{children}</C.Provider>;
}

/** Calls `fn` a short while after the last change (typing in a field saves once, not per key). */
export function useDebounced<T extends (...a: any[]) => void>(fn: T, ms = 500): T {
  const t = useRef<any>(null); const f = useRef(fn); f.current = fn;
  useEffect(() => () => clearTimeout(t.current), []);
  return useCallback(((...a: any[]) => { clearTimeout(t.current); t.current = setTimeout(() => f.current(...a), ms); }) as T, [ms]);
}
