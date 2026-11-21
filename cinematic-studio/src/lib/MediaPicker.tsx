import { useEffect, useState } from 'react';
import { L, fmtDuration } from './i18n';
import { rpc, fileUrl, inLibrary, pickFiles, MEDIA_FILTERS } from './rpc';
import { Btn, Modal, Input, Empty } from './ui';
import { useStudio } from './store';

/** Choose one item of the media library (or import a new file first). */
export function MediaPicker({ kind, onPick, onClose }: { kind: 'image' | 'audio' | 'video'; onPick: (m: any) => void; onClose: () => void }) {
  const st = useStudio();
  const [items, setItems] = useState<any[]>([]);
  const [q, setQ] = useState('');
  const load = () => rpc('media_list', { kind, q }).then((r: any) => setItems(r.items)).catch(() => {});
  useEffect(() => { load(); }, [q]); // eslint-disable-line react-hooks/exhaustive-deps
  const add = async () => {
    const paths = await pickFiles({ multiple: true, filters: MEDIA_FILTERS[kind] || MEDIA_FILTERS.any, title: L('اختر ملفات', 'Choose files') });
    if (!paths.length) return;
    const r: any[] | undefined = await st.run(() => rpc('media_import', { paths, project_id: st.project?.id }));
    r?.filter((x) => !x.ok).forEach((x) => st.toast(`${x.path}: ${x.detail}`, 'bad'));
    load();
  };
  const root = st.status.library_root;
  return (
    <Modal wide title={kind === 'image' ? L('اختر صورة مرجعية', 'Choose a reference image') : L('اختر ملفًا صوتيًا', 'Choose an audio file')} onClose={onClose} footer={<Btn onClick={add}>{L('استيراد من الجهاز', 'Import from this computer')}</Btn>}>
      <Input placeholder={L('بحث بالاسم', 'Search by name')} value={q} onChange={(e) => setQ(e.target.value)} className="mb-4" />
      {!items.length && <Empty title={L('لا توجد ملفات من هذا النوع في المكتبة', 'No files of this kind in the library')} />}
      <div className={kind === 'image' ? 'grid grid-cols-4 gap-3' : 'divide-y divide-line'}>
        {items.map((m) => kind === 'image'
          ? <button key={m.id} type="button" data-media={m.id} disabled={!!m.missing} onClick={() => { onPick(m); onClose(); }} className="text-start group disabled:opacity-40"><span className="block aspect-video bg-black rounded-sm overflow-hidden border border-line group-hover:border-accent">{m.thumb_path && <img src={fileUrl(inLibrary(root, m.thumb_path))} alt="" className="w-full h-full object-cover" />}</span><span className="block text-xs text-soft truncate mt-1">{m.name}</span></button>
          : <button key={m.id} type="button" data-media={m.id} disabled={!!m.missing} onClick={() => { onPick(m); onClose(); }} className="w-full flex justify-between py-2.5 text-sm text-start hover:text-accent disabled:opacity-40"><span className="truncate">{m.name}</span><span className="num text-mute">{fmtDuration(m.duration)}</span></button>)}
      </div>
    </Modal>
  );
}
