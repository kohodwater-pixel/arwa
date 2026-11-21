import { useCallback, useEffect, useRef, useState } from 'react';
import { rpc } from './rpc';
import { useStudio } from './store';

export type Clip = { scene_id: string; trim_in: number; trim_out: number | null; transition: { kind: string; duration: number } };
export type AudioItem = { id: string; media_id: string; track: 'audio' | 'voiceover' | 'music'; start: number; volume: number; fade_in: number; fade_out: number; trim_in: number };
export type TimelineDoc = { clips: Clip[]; audio: AudioItem[]; color: { brightness: number; contrast: number; saturation: number }; clip_audio_volume: number; output: { preset: string; fps: number; crf: number } };

/** Loads the project's timeline and saves every change (debounced) back to the project. */
export function useTimeline() {
  const st = useStudio();
  const p = st.project;
  const [tl, setTl] = useState<TimelineDoc | null>(null);
  const [transitions, setTransitions] = useState<string[]>(['cut']);
  const [media, setMedia] = useState<any[]>([]);
  const timer = useRef<any>(null);
  const done = p.scenes.filter((s: any) => s.status === 'completed').map((s: any) => s.id).join(',');
  const load = useCallback(async () => {
    const r: any = await st.run(() => rpc('timeline_get', { project_id: p.id }));
    if (r) { setTl({ audio: [], color: { brightness: 0, contrast: 1, saturation: 1 }, clip_audio_volume: 1, output: { preset: 'source', fps: 24, crf: 18 }, ...r.timeline }); setTransitions(r.transitions); }
  }, [p.id]); // eslint-disable-line react-hooks/exhaustive-deps
  const reloadMedia = useCallback(() => { rpc('media_list', { kind: 'audio' }).then((m: any) => setMedia(m.items)).catch(() => {}); }, []);
  // An edit that is still waiting for its save is written before the timeline is read again or the screen is left.
  const unsaved = useRef<TimelineDoc | null>(null);
  const flush = useCallback(async () => { clearTimeout(timer.current); const next = unsaved.current; unsaved.current = null; if (next) await st.save(() => rpc('project_update', { id: p.id, patch: { timeline: next } })); }, [p.id]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { flush().then(load); reloadMedia(); return () => { flush(); }; }, [load, done, flush, reloadMedia]);
  const update = useCallback((fn: (t: TimelineDoc) => TimelineDoc) => {
    setTl((cur) => {
      if (!cur) return cur;
      const next = fn(structuredClone(cur));
      unsaved.current = next;
      clearTimeout(timer.current);
      timer.current = setTimeout(flush, 500);
      return next;
    });
  }, [p.id]); // eslint-disable-line react-hooks/exhaustive-deps
  const sceneOf = (id: string) => p.scenes.find((s: any) => s.id === id);
  const clipLen = (c: Clip) => { const s = sceneOf(c.scene_id); const full = s?.video_duration || s?.duration || 0; return Math.max(0.1, (c.trim_out ?? full) - (c.trim_in || 0)); };
  // same arithmetic as the exporter: a transition overlaps the two clips it joins
  const starts: number[] = []; let t = 0;
  (tl?.clips || []).forEach((c, i) => { if (i > 0 && c.transition?.kind !== 'cut') t -= Math.min(c.transition.duration || 0, clipLen(c), clipLen(tl!.clips[i - 1])); starts.push(Math.max(0, t)); t = Math.max(0, t) + clipLen(c); });
  return { tl, update, transitions, media, reloadMedia, sceneOf, clipLen, starts, total: t };
}
export const TRACK_LABEL: Record<string, [string, string]> = { video: ['الفيديو', 'Video'], audio: ['الصوت', 'Audio'], voiceover: ['التعليق الصوتي', 'Voiceover'], music: ['الموسيقى', 'Music'] };
