import { useEffect, useRef, useState, type ReactNode, type ButtonHTMLAttributes, type InputHTMLAttributes, type SelectHTMLAttributes, type TextareaHTMLAttributes } from 'react';
import { L, statusText } from './i18n';

const cx = (...c: (string | false | null | undefined)[]) => c.filter(Boolean).join(' ');
export { cx };

type BtnProps = ButtonHTMLAttributes<HTMLButtonElement> & { tone?: 'accent' | 'plain' | 'ghost' | 'danger'; small?: boolean };
export function Btn({ tone = 'plain', small, className, ...p }: BtnProps) {
  const tones = { accent: 'bg-accent text-accent-ink hover:brightness-110 font-semibold', plain: 'bg-raised text-text border border-line-2 hover:border-mute', ghost: 'text-soft hover:text-text hover:bg-raised', danger: 'border border-bad/50 text-bad hover:bg-bad/10' };
  return <button type="button" {...p} className={cx('inline-flex items-center justify-center gap-2 rounded-md transition-colors disabled:opacity-40 disabled:pointer-events-none whitespace-nowrap', small ? 'h-7 px-2.5 text-xs' : 'h-9 px-4 text-sm', tones[tone], className)} />;
}
export function Field({ label, hint, children, className }: { label: ReactNode; hint?: ReactNode; children: ReactNode; className?: string }) {
  return <label className={cx('block', className)}><span className="block text-xs text-mute mb-1.5">{label}</span>{children}{hint && <span className="block text-xs text-mute mt-1.5">{hint}</span>}</label>;
}
const inputCls = 'w-full bg-ink border border-line-2 rounded-md px-3 text-sm text-text placeholder:text-mute/70 focus:border-accent focus:outline-none disabled:opacity-50';
export const Input = ({ className, ...p }: InputHTMLAttributes<HTMLInputElement>) => <input {...p} className={cx(inputCls, 'h-9', className)} />;
export const Area = ({ className, ...p }: TextareaHTMLAttributes<HTMLTextAreaElement>) => <textarea {...p} className={cx(inputCls, 'py-2 leading-relaxed resize-y', className)} />;
export const Select = ({ className, children, ...p }: SelectHTMLAttributes<HTMLSelectElement>) => <select {...p} className={cx(inputCls, 'h-9', className)}>{children}</select>;

export function Slate({ title, sub, actions, children }: { title: ReactNode; sub?: ReactNode; actions?: ReactNode; children: ReactNode }) {
  return (
    <div className="h-full flex flex-col min-h-0">
      <header className="shrink-0 flex items-end justify-between gap-6 px-8 pt-7 pb-5">
        <div className="min-w-0"><h1 className="text-[22px] font-semibold tracking-tight truncate">{title}</h1>{sub && <p className="text-sm text-mute mt-1 max-w-3xl">{sub}</p>}</div>
        {actions && <div className="flex items-center gap-2 shrink-0">{actions}</div>}
      </header>
      <div className="flex-1 min-h-0 overflow-y-auto px-8 pb-10">{children}</div>
    </div>
  );
}
export function Panel({ title, right, children, className }: { title?: ReactNode; right?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={cx('bg-panel border border-line rounded-lg', className)}>{(title || right) && <div className="flex items-center justify-between gap-3 px-4 h-11 border-b border-line"><h2 className="text-xs font-medium text-soft uppercase tracking-[0.08em] rtl:tracking-normal rtl:text-[13px]">{title}</h2>{right}</div>}<div className="p-4">{children}</div></section>;
}
export function Tag({ status, children }: { status?: string; children?: ReactNode }) {
  const tone = ['succeeded', 'completed', 'ready', 'exported', 'running'].includes(status || '') ? 'text-ok border-ok/40' : ['failed', 'error'].includes(status || '') ? 'text-bad border-bad/40' : ['queued', 'submitted', 'downloading', 'generating', 'starting', 'blocked'].includes(status || '') ? 'text-accent border-accent/40' : 'text-mute border-line-2';
  const live = ['running', 'submitted', 'downloading', 'generating', 'starting'].includes(status || '');
  return <span className={cx('inline-flex items-center gap-1.5 h-[22px] px-2 rounded border text-[11px] whitespace-nowrap', tone)}>{live && <i className="size-1.5 rounded-full bg-current live" />}{children ?? statusText(status)}</span>;
}
export function Meter({ value, tone }: { value: number; tone?: 'accent' | 'bad' | 'ok' }) {
  const v = Math.max(0, Math.min(1, value || 0));
  return <div className="h-1.5 rounded-full bg-line overflow-hidden" role="progressbar" aria-valuenow={Math.round(v * 100)} aria-valuemin={0} aria-valuemax={100}><div className={cx('h-full rounded-full transition-[width] duration-500', tone === 'bad' ? 'bg-bad' : tone === 'ok' ? 'bg-ok' : 'bg-accent')} style={{ width: `${v * 100}%` }} /></div>;
}
export function Empty({ title, text, action }: { title: ReactNode; text?: ReactNode; action?: ReactNode }) {
  return <div className="border border-dashed border-line-2 rounded-lg px-8 py-14 text-center"><p className="text-base text-soft">{title}</p>{text && <p className="text-sm text-mute mt-2 max-w-xl mx-auto">{text}</p>}{action && <div className="mt-5 flex justify-center gap-2">{action}</div>}</div>;
}
export function Note({ tone = 'info', children }: { tone?: 'info' | 'warn' | 'bad'; children: ReactNode }) {
  return <div className={cx('rounded-md border px-3.5 py-2.5 text-[13px] leading-relaxed', tone === 'warn' ? 'border-accent/40 bg-accent/5 text-soft' : tone === 'bad' ? 'border-bad/40 bg-bad/5 text-soft' : 'border-line-2 bg-raised/60 text-soft')}>{children}</div>;
}
export function Modal({ title, children, onClose, footer, wide }: { title: ReactNode; children: ReactNode; onClose: () => void; footer?: ReactNode; wide?: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { const k = (e: KeyboardEvent) => e.key === 'Escape' && onClose(); window.addEventListener('keydown', k); ref.current?.querySelector<HTMLElement>('input,textarea,select,button')?.focus(); return () => window.removeEventListener('keydown', k); }, [onClose]);
  return (
    <div className="fixed inset-0 z-40 bg-black/70 backdrop-blur-[2px] flex items-center justify-center p-6" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div ref={ref} role="dialog" aria-modal="true" className={cx('bg-panel border border-line-2 rounded-lg shadow-2xl w-full max-h-[86vh] flex flex-col', wide ? 'max-w-3xl' : 'max-w-lg')}>
        <div className="px-5 h-12 flex items-center justify-between border-b border-line shrink-0"><h2 className="font-medium">{title}</h2><button type="button" aria-label={L('إغلاق', 'Close')} onClick={onClose} className="text-mute hover:text-text text-lg leading-none px-1">×</button></div>
        <div className="p-5 overflow-y-auto">{children}</div>
        {footer && <div className="px-5 py-3.5 border-t border-line flex justify-end gap-2 shrink-0">{footer}</div>}
      </div>
    </div>
  );
}
/** Asks before a destructive or paid action. `needName` makes the approver type their name. */
export function Confirm({ title, text, confirmLabel, danger, needName, defaultName, onConfirm, onClose }: { title: string; text: ReactNode; confirmLabel: string; danger?: boolean; needName?: boolean; defaultName?: string; onConfirm: (name: string) => void | Promise<void>; onClose: () => void }) {
  const [name, setName] = useState(defaultName || '');
  const [checked, setChecked] = useState(!needName);
  const [busy, setBusy] = useState(false);
  const ok = checked && (!needName || name.trim().length >= 2);
  return (
    <Modal title={title} onClose={onClose} footer={<><Btn tone="ghost" onClick={onClose}>{L('إلغاء', 'Cancel')}</Btn><Btn tone={danger ? 'danger' : 'accent'} disabled={!ok || busy} onClick={async () => { setBusy(true); await onConfirm(name.trim()); setBusy(false); onClose(); }}>{confirmLabel}</Btn></>}>
      <div className="text-sm text-soft leading-relaxed space-y-3">{text}</div>
      {needName && <div className="mt-5 space-y-3">
        <Field label={L('اسم الموافق (يُسجَّل في السجل)', 'Approver name (recorded in the log)')}><Input value={name} onChange={(e) => setName(e.target.value)} /></Field>
        <label className="flex items-start gap-2.5 text-sm text-soft"><input type="checkbox" className="mt-1 accent-[var(--color-accent)]" checked={checked} onChange={(e) => setChecked(e.target.checked)} /><span>{L('أوافق صراحةً على هذا الإجراء المدفوع.', 'I explicitly approve this paid action.')}</span></label>
      </div>}
    </Modal>
  );
}
export const Row = ({ k, v }: { k: ReactNode; v: ReactNode }) => <div className="flex items-baseline justify-between gap-4 py-1.5 text-sm border-b border-line/60 last:border-0"><span className="text-mute shrink-0">{k}</span><span className="text-soft text-end min-w-0 break-words selectable">{v}</span></div>;
