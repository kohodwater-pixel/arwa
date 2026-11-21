import { useRef, useState } from 'react';
import { api } from '../api.js';
import { useI18n } from '../i18n.jsx';
import { useToast } from '../ui.jsx';
import { Icon } from '../icons.jsx';

/** Drop zone / picker that uploads files one by one and reports each result. */
export default function Uploader({ purpose = 'reference', projectId, onUploaded, compact, label }) {
  const { L, err } = useI18n(); const toast = useToast();
  const input = useRef(null); const [busy, setBusy] = useState(0); const [over, setOver] = useState(false);
  const accept = purpose === 'audio' ? '.mp3,.wav,.m4a,.ogg,audio/*' : '.png,.jpg,.jpeg,.webp,.mp4,.mov,.webm,image/*,video/*';
  const send = async (files) => {
    for (const file of [...files].slice(0, 10)) {
      setBusy((n) => n + 1);
      try { const r = await api.upload(file, { purpose, projectId }); onUploaded(r.asset); }
      catch (e) { toast(`${file.name}: ${err(e)}`, 'err'); }
      finally { setBusy((n) => n - 1); }
    }
  };
  return (
    <>
      <input ref={input} type="file" hidden multiple={purpose !== 'audio'} accept={accept} onChange={(e) => { send(e.target.files); e.target.value = ''; }} />
      {compact ? (
        <button type="button" className="btn sm" onClick={() => input.current.click()} disabled={busy > 0}>{busy > 0 ? <span className="spin" /> : <Icon name="upload" size={16} />}{label || L('رفع ملف', 'Upload')}</button>
      ) : (
        <div className={`drop ${over ? 'over' : ''}`} role="button" tabIndex={0} onClick={() => input.current.click()} onKeyDown={(e) => e.key === 'Enter' && input.current.click()}
          onDragOver={(e) => { e.preventDefault(); setOver(true); }} onDragLeave={() => setOver(false)} onDrop={(e) => { e.preventDefault(); setOver(false); send(e.dataTransfer.files); }}>
          {busy > 0 ? <span className="spin" style={{ display: 'inline-block' }} /> : <Icon name="upload" size={22} />}
          <div style={{ marginTop: 6 }}>{label || L('اسحب الصور أو الفيديوهات المرجعية هنا، أو اضغط للاختيار', 'Drop reference images or videos here, or click to choose')}</div>
          <div className="hint">{purpose === 'audio' ? 'MP3 · WAV · M4A · OGG' : 'PNG · JPG · WEBP · MP4 · MOV · WEBM'}</div>
        </div>
      )}
    </>
  );
}

export function RefThumb({ asset, selected, onClick, onRemove, disabled }) {
  return (
    <span className={`ref ${selected ? 'on' : ''}`} role={onClick ? 'button' : undefined} tabIndex={onClick && !disabled ? 0 : undefined} onClick={disabled ? undefined : onClick} title={asset.filename} aria-pressed={selected}>
      {asset.kind === 'reference_image' ? <img src={asset.url} alt={asset.filename} loading="lazy" /> : asset.kind === 'reference_video' ? <video src={asset.url} muted preload="metadata" /> : <Icon name="music" />}
      {onRemove && <button type="button" className="rm" onClick={(e) => { e.stopPropagation(); onRemove(); }} aria-label="remove"><Icon name="x" size={12} /></button>}
    </span>
  );
}
