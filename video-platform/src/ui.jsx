import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { Icon } from './icons.jsx';
import { useI18n } from './i18n.jsx';

// ── toasts ──
const ToastCtx = createContext(() => {});
export function ToastProvider({ children }) {
  const [items, setItems] = useState([]);
  const push = useCallback((text, kind = 'ok') => {
    const id = Math.random();
    setItems((x) => [...x.slice(-3), { id, text, kind }]);
    setTimeout(() => setItems((x) => x.filter((i) => i.id !== id)), kind === 'err' ? 7000 : 3500);
  }, []);
  return (
    <ToastCtx.Provider value={push}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        {items.map((i) => <div key={i.id} className={`toast ${i.kind}`}><Icon name={i.kind === 'err' ? 'alert' : 'check'} /><span>{i.text}</span></div>)}
      </div>
    </ToastCtx.Provider>
  );
}
export const useToast = () => useContext(ToastCtx);

/** Runs an async action with a busy flag and shows API errors as toasts. */
export function useAction() {
  const toast = useToast(); const { err } = useI18n();
  const [busy, setBusy] = useState(null);
  const run = useCallback(async (key, fn, okText) => {
    if (busy) return undefined;
    setBusy(key);
    try { const r = await fn(); if (okText) toast(okText); return r; }
    catch (e) { toast(err(e), 'err'); return undefined; }
    finally { setBusy(null); }
  }, [busy, toast, err]);
  return [busy, run];
}

export function Button({ busy, icon, flip, children, className = '', ...rest }) {
  return (
    <button type="button" className={`btn ${className}`} disabled={busy || rest.disabled} {...rest}>
      {busy ? <span className="spin" /> : icon ? <Icon name={icon} flip={flip} /> : null}{children}
    </button>
  );
}

export function Modal({ title, onClose, children, wide }) {
  useEffect(() => { const h = (e) => e.key === 'Escape' && onClose(); window.addEventListener('keydown', h); return () => window.removeEventListener('keydown', h); }, [onClose]);
  return (
    <div className="modal-back" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className={`modal ${wide ? 'wide' : ''}`} role="dialog" aria-modal="true" aria-label={title}>
        <div className="row between" style={{ marginBottom: 16 }}><h3>{title}</h3><button className="btn ghost icon" onClick={onClose} aria-label="close"><Icon name="x" /></button></div>
        {children}
      </div>
    </div>
  );
}

export function Confirm({ title, text, confirmLabel, danger, onConfirm, onClose }) {
  const { L } = useI18n(); const [busy, setBusy] = useState(false);
  return (
    <Modal title={title} onClose={onClose}>
      <p className="muted" style={{ marginBottom: 22 }}>{text}</p>
      <div className="row" style={{ justifyContent: 'flex-end' }}>
        <Button className="ghost" onClick={onClose}>{L('تراجع', 'Cancel')}</Button>
        <Button className={danger ? 'danger' : 'primary'} busy={busy} onClick={async () => { setBusy(true); await onConfirm(); setBusy(false); onClose(); }}>{confirmLabel}</Button>
      </div>
    </Modal>
  );
}

export function Field({ label, hint, children }) {
  return <div className="field">{label && <label>{label}</label>}{children}{hint && <span className="hint">{hint}</span>}</div>;
}

export const Loading = () => <div className="center" style={{ padding: 80 }}><span className="spin" style={{ width: 26, height: 26, display: 'inline-block', color: 'var(--accent)' }} /></div>;

export function DemoBadge() { const { L } = useI18n(); return <span className="badge demo">{L('وضع تجريبي', 'DEMO')}</span>; }

export function StatusBadge({ status }) {
  const { L } = useI18n();
  const map = {
    draft: ['', L('مسودة', 'Draft')], storyboard: ['info', L('مخطط جاهز', 'Storyboard')], queued: ['warn', L('في الانتظار', 'Queued')],
    generating: ['warn', L('قيد التوليد', 'Generating')], assembling: ['warn', L('قيد التجميع', 'Assembling')], completed: ['ok', L('مكتمل', 'Completed')],
    failed: ['err', L('فشل', 'Failed')], canceled: ['', L('أُلغي', 'Canceled')], pending: ['', L('لم يُولَّد', 'Not generated')],
    running: ['warn', L('جارٍ', 'Running')], succeeded: ['ok', L('نجح', 'Succeeded')],
  };
  const [cls, text] = map[status] || ['', status];
  const live = ['queued', 'generating', 'assembling', 'running'].includes(status);
  return <span className={`badge ${cls}`}>{live && <i className="dot pulse" />}{text}</span>;
}

export const arClass = (aspect) => `ar-${String(aspect || '16:9').replace(':', 'x')}`;
const fmt = (s) => { s = Math.max(0, Math.floor(s || 0)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };

/** Video player with its own controls (play, seek, time, mute, fullscreen, download). */
export function Player({ src, aspect, poster, isDemo, downloadUrl }) {
  const v = useRef(null), box = useRef(null);
  const [st, setSt] = useState({ playing: false, t: 0, d: 0, muted: false, started: false });
  useEffect(() => { setSt((s) => ({ ...s, playing: false, t: 0, started: false })); }, [src]);
  const toggle = () => { const el = v.current; if (!el) return; el.paused ? el.play().catch(() => {}) : el.pause(); };
  const seek = (e) => { const r = e.currentTarget.getBoundingClientRect(); const el = v.current; if (el && st.d) el.currentTime = ((e.clientX - r.left) / r.width) * st.d; };
  return (
    <div ref={box} className={`player ${arClass(aspect)} ${st.playing ? '' : 'paused'}`}>
      {isDemo && <span className="demo-tag"><DemoBadge /></span>}
      <video ref={v} src={src} poster={poster || undefined} playsInline preload="metadata" onClick={toggle}
        onPlay={() => setSt((s) => ({ ...s, playing: true, started: true }))} onPause={() => setSt((s) => ({ ...s, playing: false }))}
        onTimeUpdate={(e) => setSt((s) => ({ ...s, t: e.target.currentTime }))} onLoadedMetadata={(e) => setSt((s) => ({ ...s, d: e.target.duration }))} />
      {!st.started && <button className="big" onClick={toggle} aria-label="play"><span><Icon name="play" size={30} /></span></button>}
      <div className="controls">
        <button onClick={toggle} aria-label={st.playing ? 'pause' : 'play'}><Icon name={st.playing ? 'pause' : 'play'} /></button>
        <span className="time">{fmt(st.t)}</span>
        <div className="seek" onClick={seek} role="slider" aria-valuemin={0} aria-valuemax={Math.round(st.d)} aria-valuenow={Math.round(st.t)} tabIndex={0}
          onKeyDown={(e) => { const el = v.current; if (!el) return; if (e.key === 'ArrowRight') el.currentTime += 2; if (e.key === 'ArrowLeft') el.currentTime -= 2; }}>
          <i style={{ width: st.d ? `${(st.t / st.d) * 100}%` : 0 }} />
        </div>
        <span className="time">{fmt(st.d)}</span>
        <button onClick={() => { v.current.muted = !v.current.muted; setSt((s) => ({ ...s, muted: v.current.muted })); }} aria-label="mute"><Icon name={st.muted ? 'mute' : 'volume'} /></button>
        {downloadUrl && <a href={downloadUrl} download aria-label="download"><button tabIndex={-1}><Icon name="download" /></button></a>}
        <button onClick={() => (document.fullscreenElement ? document.exitFullscreen() : box.current?.requestFullscreen?.())} aria-label="fullscreen"><Icon name="full" /></button>
      </div>
    </div>
  );
}

/** Polls `fn` every `ms` while `active`; reports connection loss instead of failing silently. */
export function usePolling(fn, ms, active) {
  const [offline, setOffline] = useState(false);
  const ref = useRef(fn); ref.current = fn;
  useEffect(() => {
    if (!active) return undefined;
    let stop = false, timer;
    const tick = async () => {
      try { await ref.current(); if (!stop) setOffline(false); } catch (e) { if (!stop && e?.code === 'network') setOffline(true); }
      if (!stop) timer = setTimeout(tick, ms);
    };
    timer = setTimeout(tick, ms);
    return () => { stop = true; clearTimeout(timer); };
  }, [ms, active]);
  return offline;
}

export function copyText(text) {
  if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(text);
  const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
  return Promise.resolve();
}
export const fitClip = (clip, s) => (clip?.values ? clip.values.find((v) => v >= s) ?? clip.values[clip.values.length - 1] : Math.min(clip?.max ?? s, Math.max(clip?.min ?? 1, Math.ceil(s))));
