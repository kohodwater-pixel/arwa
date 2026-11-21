// The only door between the UI and the system. In the desktop app every call is a Tauri command handled
// in Rust; in a plain browser (development and browser tests) the same calls go to the local dev bridge.
// No key, token or file-system access lives on this side.
export class RpcError extends Error {
  code: string;
  constructor(code: string, message: string) { super(message); this.code = code; }
}
type Reply = { ok: true; data: unknown } | { ok: false; error: { code: string; message: string } };

export const isTauri = typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window;

export async function rpc<T = any>(cmd: string, args: Record<string, unknown> = {}): Promise<T> {
  let reply: Reply;
  if (isTauri) {
    const { invoke } = await import('@tauri-apps/api/core');
    reply = await invoke<Reply>('rpc', { cmd, args });
  } else {
    const r = await fetch('/rpc', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cmd, args }) }).catch(() => null);
    if (!r || !r.ok) throw new RpcError('core_unreachable', 'The application core is not running.');
    reply = await r.json();
  }
  if (!reply.ok) throw new RpcError(reply.error.code, reply.error.message);
  return reply.data as T;
}

/** URL the web view can use to show a file the core allows (library files and registered media). */
export function fileUrl(absolutePath: string | null | undefined): string {
  if (!absolutePath) return '';
  const q = `path=${encodeURIComponent(absolutePath)}`;
  if (!isTauri) return `/file?${q}`;
  // Tauri serves custom schemes as http://<scheme>.localhost on Windows and <scheme>://localhost elsewhere.
  return navigator.userAgent.includes('Windows') ? `http://studio.localhost/file?${q}` : `studio://localhost/file?${q}`;
}

/** Library-relative path → absolute path (the core checks it again before serving). */
export const inLibrary = (root: string, rel: string | null | undefined) => (rel ? `${root.replace(/[\\/]+$/, '')}/${rel}` : '');

type Filter = { name: string; extensions: string[] };
/** Native file picker. In the browser build there is no native picker, so the path is typed (development only). */
export async function pickFiles(opts: { multiple?: boolean; directory?: boolean; filters?: Filter[]; title?: string } = {}): Promise<string[]> {
  if (isTauri) {
    const { open } = await import('@tauri-apps/plugin-dialog');
    const r = await open({ multiple: !!opts.multiple, directory: !!opts.directory, filters: opts.filters, title: opts.title });
    return !r ? [] : Array.isArray(r) ? r : [r];
  }
  const typed = window.prompt(`${opts.title || 'Path'} (development: type an absolute path; separate several with ;)`);
  return typed ? typed.split(';').map((s) => s.trim()).filter(Boolean) : [];
}
export async function pickSavePath(defaultName: string, filters?: Filter[]): Promise<string | null> {
  if (isTauri) {
    const { save } = await import('@tauri-apps/plugin-dialog');
    return (await save({ defaultPath: defaultName, filters })) || null;
  }
  return window.prompt('Save to (development: absolute path)', defaultName);
}

export const MEDIA_FILTERS: Record<string, Filter[]> = {
  any: [{ name: 'Media', extensions: ['png', 'jpg', 'jpeg', 'webp', 'mp4', 'mov', 'webm', 'm4v', 'mp3', 'wav', 'm4a', 'ogg', 'flac'] }],
  image: [{ name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'webp'] }],
  audio: [{ name: 'Audio', extensions: ['mp3', 'wav', 'm4a', 'ogg', 'flac'] }],
};
