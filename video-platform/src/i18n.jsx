import { createContext, useContext, useEffect, useMemo, useState, useCallback } from 'react';

const Ctx = createContext(null);
const initial = () => { try { return localStorage.getItem('locale') || 'ar'; } catch { return 'ar'; } };

export function I18nProvider({ children }) {
  const [locale, setLocaleState] = useState(initial);
  const setLocale = useCallback((l) => { setLocaleState(l); try { localStorage.setItem('locale', l); } catch { /* private mode */ } }, []);
  useEffect(() => { document.documentElement.lang = locale; document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr'; }, [locale]);
  const value = useMemo(() => ({
    locale, setLocale, rtl: locale === 'ar',
    /** L('نص', 'text') — both languages sit side by side at the call site. */
    L: (ar, en) => (locale === 'ar' ? ar : en),
    name: (item) => (item ? (locale === 'ar' ? item.ar : item.en) : ''),
    num: (n) => new Intl.NumberFormat(locale === 'ar' ? 'ar-SA-u-nu-latn' : 'en').format(n),
    date: (ts) => new Intl.DateTimeFormat(locale === 'ar' ? 'ar-SA-u-nu-latn-ca-gregory' : 'en-GB', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(ts)),
    err: (e) => errorText(e, locale),
  }), [locale, setLocale]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
export const useI18n = () => useContext(Ctx);

const ERR = {
  network: ['تعذّر الاتصال بالخادم. تحقق من الشبكة وحاول مجددًا.', 'Could not reach the server. Check your connection and try again.'],
  unauthenticated: ['انتهت الجلسة. سجّل الدخول من جديد.', 'Your session has ended. Please sign in again.'],
  forbidden: ['لا تملك صلاحية لهذا الإجراء.', 'You do not have permission to do this.'],
  csrf: ['طلب غير موثوق.', 'Untrusted request.'],
  rate_limited: ['محاولات كثيرة. انتظر قليلًا ثم حاول.', 'Too many attempts. Wait a little and try again.'],
  invalid_email: ['البريد الإلكتروني غير صحيح.', 'The e-mail address is not valid.'],
  weak_password: ['كلمة المرور يجب ألا تقل عن 8 أحرف.', 'The password must be at least 8 characters.'],
  invalid_name: ['اكتب الاسم (حرفان على الأقل).', 'Enter a name (at least 2 characters).'],
  email_taken: ['هذا البريد مسجّل من قبل.', 'This e-mail is already registered.'],
  bad_credentials: ['البريد أو كلمة المرور غير صحيحة.', 'Wrong e-mail or password.'],
  account_disabled: ['هذا الحساب موقوف. تواصل مع المدير.', 'This account is disabled. Contact the administrator.'],
  registration_closed: ['التسجيل مغلق حاليًا.', 'Registration is currently closed.'],
  invalid_reset_token: ['رابط الاستعادة غير صالح أو منتهي.', 'The reset link is invalid or has expired.'],
  bad_current_password: ['كلمة المرور الحالية غير صحيحة.', 'The current password is wrong.'],
  description_too_short: ['الوصف قصير جدًا. اكتب 10 أحرف على الأقل.', 'The description is too short. Write at least 10 characters.'],
  description_too_long: ['الوصف طويل جدًا (الحد 4000 حرف).', 'The description is too long (limit: 4000 characters).'],
  provider_unavailable: ['محرك التوليد غير متاح.', 'This generation engine is not available.'],
  provider_not_configured: ['محرك التوليد غير مهيأ: لا يوجد مفتاح API له على الخادم.', 'This engine is not configured: the server has no API key for it.'],
  unsupported_option: ['هذا الخيار غير مدعوم في المحرك المختار.', 'This option is not supported by the selected engine.'],
  bad_duration: (d) => [`المدة غير مقبولة (الحد الأقصى ${d.max} ثانية).`, `Duration not accepted (maximum ${d.max} seconds).`],
  bad_scene_duration: (d) => [`مدة المشهد يجب أن تكون بين 1 و${d.max} ثوانٍ في هذا المحرك.`, `A scene must last between 1 and ${d.max} seconds on this engine.`],
  bad_prompt_length: (d) => [`طول البرومبت يجب أن يكون بين 10 و${d.max} حرفًا.`, `The prompt must be between 10 and ${d.max} characters.`],
  project_busy: ['المشروع قيد التوليد الآن. انتظر انتهاءه أو ألغِه أولًا.', 'The project is generating. Wait for it to finish or cancel it first.'],
  project_not_found: ['المشروع غير موجود.', 'Project not found.'],
  no_storyboard: ['لا يوجد مخطط مشاهد بعد.', 'There is no storyboard yet.'],
  last_scene: ['لا يمكن حذف المشهد الوحيد.', 'The only scene cannot be deleted.'],
  too_many_scenes: ['الحد الأقصى 24 مشهدًا.', 'The maximum is 24 scenes.'],
  reference_must_be_image: ['المرجع يجب أن يكون صورة.', 'The reference must be an image.'],
  reference_not_supported: ['المحرك المختار لا يدعم البدء من صورة مرجعية.', 'The selected engine cannot start from a reference image.'],
  scenes_incomplete: ['بعض المشاهد لم يكتمل توليدها.', 'Some scenes have not finished generating.'],
  not_completed: ['الفيديو لم يكتمل بعد.', 'The video is not finished yet.'],
  not_running: ['لا توجد عملية توليد جارية.', 'Nothing is being generated.'],
  audio_not_configured: ['توليد الصوت مطلوب لكن لا توجد خدمة صوت مهيأة. اختر «رفع ملف» أو «بدون».', 'Audio generation was requested but no audio service is configured. Choose "Upload" or "None".'],
  audio_voice_missing: ['اختر صوتًا للتعليق الصوتي.', 'Choose a voice for the voice-over.'],
  limit_active_projects: (d) => [`بلغت حد المشاريع الجارية في وقت واحد (${d.limit}).`, `You reached the limit of projects generating at once (${d.limit}).`],
  limit_daily_seconds: (d) => [`بلغت حد التوليد اليومي (${d.used} من ${d.limit} ثانية).`, `You reached the daily generation limit (${d.used} of ${d.limit} seconds).`],
  limit_storage: (d) => [`امتلأت مساحة التخزين (${d.limit} م.ب). احذف ملفات أو مشاريع.`, `Storage is full (${d.limit} MB). Delete files or projects.`],
  unsupported_file_type: ['نوع الملف غير مدعوم.', 'This file type is not supported.'],
  file_too_large: ['الملف أكبر من الحد المسموح.', 'The file is larger than allowed.'],
  unreadable_file: ['تعذّرت قراءة الملف؛ قد يكون تالفًا.', 'The file could not be read; it may be damaged.'],
  video_too_long: ['الفيديو المرجعي أطول من 5 دقائق.', 'The reference video is longer than 5 minutes.'],
  upload_failed: ['فشل رفع الملف.', 'The upload failed.'],
  cannot_demote_self: ['لا يمكنك إزالة صلاحيتك أو إيقاف حسابك.', 'You cannot demote or disable your own account.'],
  job_not_retryable: ['هذه المهمة لا يمكن إعادتها.', 'This job cannot be retried.'],
  job_not_active: ['المهمة ليست جارية.', 'The job is not active.'],
  not_found: ['غير موجود.', 'Not found.'],
  server_error: ['حدث خطأ في الخادم. سُجّل الخطأ للمراجعة.', 'A server error occurred. It has been logged.'],
};
export function errorText(e, locale) {
  const entry = ERR[e?.code] || ERR.server_error;
  const pair = typeof entry === 'function' ? entry(e.data || {}) : entry;
  return pair[locale === 'ar' ? 0 : 1];
}
