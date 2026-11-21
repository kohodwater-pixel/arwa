export type Lang = 'ar' | 'en';
let current: Lang = 'ar';
export const setLang = (l: Lang) => { current = l; document.documentElement.lang = l; document.documentElement.dir = l === 'ar' ? 'rtl' : 'ltr'; };
export const lang = () => current;
/** Inline bilingual text: L('عربي', 'English'). */
export const L = (ar: string, en: string) => (current === 'ar' ? ar : en);
export const pick = (o: { ar: string; en: string } | undefined | null) => (o ? (current === 'ar' ? o.ar : o.en) : '');

const ERR: Record<string, [string, string]> = {
  core_unreachable: ['نواة التطبيق لا تعمل.', 'The application core is not running.'],
  comfy_not_configured: ['لم يُضبط خادم ComfyUI بعد. أضف عنوانه من «الإعدادات».', 'No ComfyUI server is configured yet. Add its address in Settings.'],
  comfy_unreachable: ['تعذّر الوصول إلى خادم ComfyUI. تحقق من أن الخادم يعمل ومن العنوان.', 'The ComfyUI server cannot be reached. Check that it is running and the address is right.'],
  comfy_auth: ['رفض خادم ComfyUI رمز الدخول.', 'The ComfyUI server refused the access token.'],
  insecure_url: ['العنوان يجب أن يبدأ بـ https://. يُسمح بـ http فقط لخادم على هذا الجهاز (localhost).', 'The address must start with https://. Plain http is allowed only for a server on this computer (localhost).'],
  budget_exceeded: ['بلغت ميزانية GPU الشهرية حدّها. لا تُقبل مهام توليد جديدة حتى يرفع المدير الحد.', 'The monthly GPU budget is used up. No new generation jobs are accepted until the manager raises the limit.'],
  approval_required: ['هذا الإجراء يحتاج موافقة صريحة واسم الموافق.', 'This action needs an explicit approval and the approver\'s name.'],
  gpu_stopped: ['GPU السحابي متوقف. شغّله من «إدارة GPU» (بموافقة).', 'The cloud GPU is stopped. Start it from the GPU Manager (approval required).'],
  gpu_auth: ['رفض مزود GPU المفتاح.', 'The GPU provider refused the key.'],
  gpu_not_configured: ['لم يُضبط مزود GPU.', 'No GPU provider is configured.'],
  scene_too_long: ['مدة أحد المشاهد أطول مما يولّده هذا النموذج في مقطع واحد.', 'A scene is longer than this model generates in one clip.'],
  aspect_not_supported: ['هذا النموذج لا يولّد المقاس المختار.', 'This model does not generate the chosen aspect ratio.'],
  reference_required: ['هذا النموذج يحوّل الصورة إلى فيديو: كل مشهد يحتاج صورة مرجعية.', 'This model is image-to-video: every scene needs a reference image.'],
  empty_prompt: ['أحد المشاهد بلا برومبت.', 'A scene has no prompt.'],
  project_busy: ['ألغِ المهام الجارية لهذا المشروع أولًا.', 'Cancel this project\'s running jobs first.'],
  scene_busy: ['هذا المشهد قيد التوليد الآن.', 'This scene is being generated.'],
  export_running: ['يوجد تصدير لهذا المشروع في القائمة.', 'An export of this project is already queued.'],
  ffmpeg_missing: ['لم يُعثر على FFmpeg. حدّد مجلده من «الإعدادات».', 'FFmpeg was not found. Set its folder in Settings.'],
  not_safetensors: ['يُقبل ملف .safetensors صحيح فقط؛ صيغ pickle مرفوضة لأنها قد تنفّذ شيفرة.', 'Only a valid .safetensors file is accepted; pickle formats are refused because they can run code.'],
  version_exists: ['هذا الإصدار موجود. استخدم رقم إصدار جديدًا.', 'This version already exists. Use a new version number.'],
  rights_required: ['اكتب مصدر المقاطع وما يجيز التدريب عليها.', 'Say where the clips come from and what permits training on them.'],
  unsafe_archive: ['الملف المضغوط غير آمن ولم يُستورد.', 'The archive is unsafe and was not imported.'],
  archive: ['هذا ليس ملف مشروع صالحًا.', 'This is not a valid project file.'],
  unsupported_type: ['نوع الملف غير مدعوم.', 'Unsupported file type.'],
  file_missing: ['الملف غير موجود.', 'The file does not exist.'],
  forbidden: ['غير مسموح.', 'Not allowed.'],
  empty_timeline: ['لا توجد مشاهد مكتملة للتصدير.', 'There are no finished scenes to export.'],
};
export function errText(e: unknown): string {
  const code = (e as any)?.code as string | undefined;
  const msg = (e as any)?.message as string | undefined;
  if (code && ERR[code]) return L(ERR[code][0], ERR[code][1]);
  return msg || String(e);
}
export const reasonText = (code: string | null | undefined) => (code && ERR[code] ? L(ERR[code][0], ERR[code][1]) : code || '');

const STATUS: Record<string, [string, string]> = {
  draft: ['مسودة', 'Draft'], storyboard: ['ستوري بورد', 'Storyboard'], generating: ['قيد التوليد', 'Generating'], ready: ['جاهز', 'Ready'], exported: ['مُصدَّر', 'Exported'],
  pending: ['لم يُولَّد', 'Not generated'], queued: ['في الانتظار', 'Queued'], blocked: ['متوقف مؤقتًا', 'Waiting'], submitted: ['أُرسل', 'Submitted'], running: ['يعمل', 'Running'],
  downloading: ['تنزيل', 'Downloading'], succeeded: ['اكتمل', 'Done'], completed: ['مكتمل', 'Done'], failed: ['فشل', 'Failed'], canceled: ['أُلغي', 'Canceled'],
  stopped: ['متوقف', 'Stopped'], starting: ['يبدأ', 'Starting'], stopping: ['يتوقف', 'Stopping'], error: ['خطأ', 'Error'], unknown: ['غير معروف', 'Unknown'],
};
export const statusText = (s: string | null | undefined) => (s && STATUS[s] ? L(STATUS[s][0], STATUS[s][1]) : s || '');

export const fmtDuration = (sec: number | null | undefined) => { const s = Math.max(0, Math.round(sec || 0)); return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; };
export const fmtSize = (b: number | null | undefined) => { const n = b || 0; return n > 1e9 ? `${(n / 1e9).toFixed(2)} GB` : n > 1e6 ? `${(n / 1e6).toFixed(1)} MB` : `${Math.ceil(n / 1e3)} KB`; };
export const fmtDate = (iso: string | null | undefined) => (iso ? new Date(iso).toLocaleString(current === 'ar' ? 'ar-SA-u-nu-latn-ca-gregory' : 'en-GB', { dateStyle: 'medium', timeStyle: 'short' }) : '');
