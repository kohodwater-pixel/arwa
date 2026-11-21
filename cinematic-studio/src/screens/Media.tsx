import { useEffect, useState } from 'react';
import { useStudio } from '../lib/store';
import { L, fmtDuration, fmtDate, fmtSize } from '../lib/i18n';
import { rpc, fileUrl, inLibrary, pickFiles, MEDIA_FILTERS, isTauri } from '../lib/rpc';
import { Btn, Slate, Input, Empty, Row, cx, Confirm, Field } from '../lib/ui';

const KINDS: [string, string, string][] = [['', 'الكل', 'All'], ['image', 'صور', 'Images'], ['video', 'فيديو', 'Video'], ['audio', 'صوت', 'Audio']];
export default function Media() {
  const st = useStudio();
  const [data, setData] = useState<{ items: any[]; folders: any[] }>({ items: [], folders: [] });
  const [kind, setKind] = useState('');
  const [folder, setFolder] = useState<string | null>(null);
  const [q, setQ] = useState('');
  const [sel, setSel] = useState<any | null>(null);
  const [del, setDel] = useState<any | null>(null);
  const [newFolder, setNewFolder] = useState('');
  const root = st.status.library_root;
  const load = () => rpc('media_list', { kind: kind || undefined, folder: folder ?? undefined, q }).then((r: any) => { setData(r); setSel((s: any) => (s ? r.items.find((m: any) => m.id === s.id) || null : null)); }).catch(() => {});
  useEffect(() => { load(); }, [kind, folder, q]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { window.addEventListener('media-changed', load); return () => window.removeEventListener('media-changed', load); });
  const add = async () => {
    const paths = await pickFiles({ multiple: true, filters: MEDIA_FILTERS.any, title: L('اختر ملفات', 'Choose files') });
    if (!paths.length) return;
    const r: any[] | undefined = await st.run(() => rpc('media_import', { paths, folder: folder || '' }));
    if (!r) return;
    const ok = r.filter((x) => x.ok && !x.duplicate).length, dup = r.filter((x) => x.duplicate).length, bad = r.filter((x) => !x.ok);
    st.toast([ok ? L(`أُضيف ${ok}`, `${ok} added`) : '', dup ? L(`${dup} مكرر موجود مسبقًا`, `${dup} duplicate(s) already in the library`) : ''].filter(Boolean).join(' · ') || L('لم يُضف شيء', 'Nothing added'), ok ? 'ok' : 'info');
    bad.forEach((x) => st.toast(`${x.path.split(/[\\/]/).pop()}: ${x.detail}`, 'bad'));
    load(); st.refreshStatus();
  };
  const verify = async () => { const r: any = await st.run(() => rpc('media_verify')); if (r) { st.toast(r.missing + r.corrupted ? L(`${r.missing} مفقود، ${r.corrupted} تالف من ${r.checked}`, `${r.missing} missing, ${r.corrupted} corrupted of ${r.checked}`) : L(`كل الملفات (${r.checked}) سليمة`, `All ${r.checked} files are intact`), r.missing + r.corrupted ? 'bad' : 'ok'); load(); } };
  return (
    <Slate title={L('مكتبة الوسائط', 'Media Library')} sub={L('المكتبة تسجّل مكان ملفاتك ولا تنقلها ولا تعدّلها: الأصل يبقى حيث وضعته.', 'The library records where your files are; it does not move or change them. The original stays where you put it.')}
      actions={<><Btn onClick={verify}>{L('افحص الملفات', 'Check files')}</Btn><Btn tone="accent" data-action="import-media" onClick={add}>{L('استيراد ملفات', 'Import files')}</Btn></>}>
      <div className="grid grid-cols-[180px_minmax(0,1fr)_300px] gap-6 items-start">
        <div>
          <p className="text-xs text-mute mb-2">{L('المجلدات', 'Folders')}</p>
          <button type="button" onClick={() => setFolder(null)} className={cx('w-full text-start px-2.5 py-1.5 rounded text-[13px]', folder === null ? 'bg-raised' : 'text-soft hover:text-text')}>{L('كل الملفات', 'All files')}</button>
          {data.folders.map((f) => <button key={f.folder} type="button" onClick={() => setFolder(f.folder)} className={cx('w-full flex justify-between px-2.5 py-1.5 rounded text-[13px]', folder === f.folder ? 'bg-raised' : 'text-soft hover:text-text')}><span className="truncate">{f.folder || L('بلا مجلد', 'Unfiled')}</span><span className="num text-mute">{f.count}</span></button>)}
        </div>
        <div>
          <div className="flex gap-3 mb-4"><Input data-field="search" placeholder={L('بحث بالاسم', 'Search by name')} value={q} onChange={(e) => setQ(e.target.value)} /><div className="flex bg-panel border border-line rounded-md p-0.5 shrink-0">{KINDS.map(([k, ar, en]) => <button key={k} type="button" data-kind={k || 'all'} onClick={() => setKind(k)} className={cx('h-8 px-3 rounded text-[13px]', kind === k ? 'bg-raised text-text' : 'text-mute')}>{L(ar, en)}</button>)}</div></div>
          {!data.items.length && <Empty title={L('لا ملفات هنا', 'No files here')} text={isTauri ? L('استورد صورًا أو فيديو أو صوتًا، أو اسحب الملفات وأفلتها على نافذة التطبيق.', 'Import images, video or audio, or drag files onto the app window.') : L('استورد صورًا أو فيديو أو صوتًا.', 'Import images, video or audio.')} />}
          <div className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3" data-media-grid>
            {data.items.map((m) => (
              <button key={m.id} type="button" data-media={m.id} onClick={() => setSel(m)} className={cx('text-start rounded-sm border overflow-hidden bg-panel', sel?.id === m.id ? 'border-accent' : 'border-line hover:border-line-2')}>
                <span className="relative block aspect-video bg-black">{m.thumb_path ? <img src={fileUrl(inLibrary(root, m.thumb_path))} alt="" loading="lazy" className="w-full h-full object-cover" /> : <span className="absolute inset-0 grid place-items-center text-[11px] text-mute">{m.kind === 'audio' ? L('صوت', 'Audio') : ''}</span>}
                  {(m.missing || m.corrupted) ? <span className="absolute inset-0 bg-black/70 grid place-items-center text-[11px] text-bad">{m.missing ? L('مفقود', 'Missing') : L('تالف', 'Corrupted')}</span> : null}
                  {m.duration ? <span className="absolute bottom-1 end-1 num text-[10px] bg-black/70 px-1 rounded">{fmtDuration(m.duration)}</span> : null}</span>
                <span className="block px-2 py-1.5 text-xs text-soft truncate">{m.name}</span>
              </button>
            ))}
          </div>
        </div>
        <aside className="bg-panel border border-line rounded-lg p-4 sticky top-0">
          {!sel && <p className="text-sm text-mute">{L('اختر ملفًا لعرض تفاصيله.', 'Select a file to see its details.')}</p>}
          {sel && <>
            <div className="frame aspect-video rounded-sm overflow-hidden grid place-items-center mb-3">
              {sel.missing ? <span className="text-xs text-bad">{L('الملف الأصلي مفقود', 'The original file is missing')}</span> : sel.kind === 'image' ? <img src={fileUrl(sel.path)} alt="" className="w-full h-full object-contain" /> : sel.kind === 'video' ? <video src={fileUrl(sel.path)} controls className="w-full h-full" /> : <audio src={fileUrl(sel.path)} controls className="w-[92%]" />}
            </div>
            <p className="text-sm break-words selectable">{sel.name}</p>
            <div className="mt-3">
              {sel.width ? <Row k={L('الأبعاد', 'Dimensions')} v={<span className="num">{sel.width}×{sel.height}</span>} /> : null}
              {sel.duration ? <Row k={L('المدة', 'Duration')} v={<span className="num">{sel.duration.toFixed(2)}s{sel.fps ? ` · ${sel.fps.toFixed(2)} fps` : ''}</span>} /> : null}
              <Row k={L('الحجم', 'Size')} v={<span className="num">{fmtSize(sel.size)}</span>} />
              <Row k={L('أُضيف', 'Imported')} v={fmtDate(sel.imported_at)} />
              <Row k="SHA-256" v={<span className="ltr text-xs">{sel.sha256.slice(0, 16)}…</span>} />
              <Row k={L('المسار', 'Path')} v={<span className="ltr text-xs">{sel.path}</span>} />
            </div>
            <Field label={L('انقل إلى مجلد', 'Move to folder')} className="mt-4"><div className="flex gap-2"><Input list="folders" value={newFolder} placeholder={sel.folder || L('اسم المجلد', 'Folder name')} onChange={(e) => setNewFolder(e.target.value)} /><Btn onClick={async () => { await st.run(() => rpc('media_update', { id: sel.id, folder: newFolder })); setNewFolder(''); load(); }}>{L('انقل', 'Move')}</Btn></div><datalist id="folders">{data.folders.filter((f) => f.folder).map((f) => <option key={f.folder} value={f.folder} />)}</datalist></Field>
            <Btn small tone="danger" className="mt-4" data-action="remove-media" onClick={() => setDel(sel)}>{L('أزل من المكتبة', 'Remove from library')}</Btn>
          </>}
        </aside>
      </div>
      {del && <Confirm danger title={L('إزالة من المكتبة', 'Remove from library')} confirmLabel={L('إزالة', 'Remove')} onClose={() => setDel(null)} text={<p>{L('يُزال السجل والصورة المصغّرة فقط. ملفك الأصلي يبقى في مكانه دون تغيير.', 'Only the record and its thumbnail are removed. Your original file stays where it is, unchanged.')}</p>} onConfirm={async () => { await st.run(() => rpc('media_remove', { id: del.id })); setSel(null); load(); st.refreshStatus(); }} />}
    </Slate>
  );
}
