# هيبو — صفحة نموذج الاستفسار عن الامتياز (v01، مسودة)

**الحالة: مسودة غير موصولة.** الصفحة تعمل وتتحقق من الحقول، لكنها لا ترسل شيئًا إلى أي جهة حتى تُربط. ما دامت غير موصولة يظهر شريط أسود أعلاها يقول ذلك، ورسالة التأكيد تقول صراحةً إن شيئًا لم يُرسَل.

## ما هي
الصفحة التي يفتحها رمز QR في نهاية إعلان الامتياز: مقدمة قصيرة تحمل «حُطّ ثقلك.»، ثم النموذج، ثم رسالة التأكيد. عربية (`src/index.html`) وإنجليزية (`src/index-en.html`) مع زر تبديل. مجلد `src/` مكتفٍ بنفسه: الخطوط والصور داخله، ولا يتصل بأي خدمة خارجية (لا تحليلات ولا خطوط من الإنترنت). يُفتح بالنقر على `index.html` من أي مكان.

## الحقول
مطلوبة: الاسم الكامل، رقم الجوال، المدينة أو المنطقة (نص حر)، هل لديك موقع (ثلاث إجابات)، الموافقة.
اختيارية: البريد الإلكتروني، الخبرة، كيف سمعت عن الامتياز، الرسالة.
لا يوجد في الصفحة أي رقم أو مبلغ أو عدد فروع أو قائمة مدن.

## الربط — القرار للعميل
الربط كله في ملف واحد: `src/js/config.js`. الخيارات:

| الخيار | ما يلزم | ملاحظة |
|---|---|---|
| خدمة نماذج جاهزة (مثل Formspree أو Basin) | حساب في الخدمة، ثم لصق رابطها في `FORM_ENDPOINT` | الأسرع؛ الاستفسارات تصل بالبريد. بيانات المتقدمين تمر بطرف ثالث |
| Google Apps Script إلى جدول Google Sheet | سكربت صغير في حساب Google للعميل، ورابطه في `FORM_ENDPOINT` مع `FORM_FORMAT: "form"` | مجاني والبيانات في جدول العميل |
| موقع العميل أو نظام CRM عنده | رابط يستقبل POST من مطوّر العميل | الأنسب إن كان لديه نظام قائم |
| واتساب (بديل بسيط بلا خادم) | رقم الواتساب في `WHATSAPP_NUMBER` | يفتح واتساب الزائر والاستفسار مكتوب، والزائر يضغط «إرسال» بنفسه؛ لا يُحفظ شيء تلقائيًا |

البيانات المرسلة: `full_name, mobile, email, city, has_location, experience, heard_from, message, consent, lang, form, submitted_at`. يعدّ النموذج الإرسال ناجحًا إذا ردّ الخادم برمز نجاح (2xx)، وإلا تظهر رسالة خطأ وتبقى البيانات في الحقول.
**لم يُجرَّب الربط مع أي خدمة حقيقية.** جُرّبت مسارات النجاح والفشل وواتساب بمحاكاة داخل المتصفح فقط؛ بعد الربط الفعلي يجب إرسال استفسار تجريبي والتأكد من وصوله.

## الاستضافة
ارفع محتويات `src/` كما هي على أي استضافة ملفات ثابتة تعمل بـ HTTPS (موقع العميل الحالي، أو Netlify أو Cloudflare Pages أو GitHub Pages)، ثم يُولَّد رمز QR من الرابط النهائي. لا يُطبع الرمز قبل تثبيت الرابط.

## مطلوب من العميل
1. جهة استقبال الاستفسارات (أحد الخيارات أعلاه).
2. النطاق أو الرابط الذي ستُنشر عليه الصفحة.
3. نص إشعار الخصوصية أو رابطه (مكانه في الصفحة خانة منقّطة واضحة). صياغة الموافقة تحتاج مراجعة مستشاره القانوني.
4. هل يريد سؤالًا عن القدرة الاستثمارية؟ لم نضعه لأن شرائحه أرقام لا نملكها.
5. هل الامتياز متاح في أسواق أو مدن محددة؟ الحقل الآن نص حر.
6. هل البريد الإلكتروني مطلوب أم اختياري (الآن اختياري)؟
7. اعتماد جملة التأكيد «سيتواصل معك فريق هيبو»، ومن سيتابع الاستفسارات.
8. قراءة النص العربي من قارئ سعودي قبل النشر.

## ملاحظات
- الصفحة المرجعية التي أرسلها العميل لم تُفتح من بيئة العمل (النطاق محجوب بسياسة الشبكة)، فبُنيت الحقول على الممارسة المعتادة في نماذج الامتياز. التفاصيل في `ux-brief.md`.
- لقطات المراجعة في `hippo_franchise-form_screens_ar-en_v01/`. إعادة الفحص: `node _work/verify.cjs`.

---

# HIPPO — franchise enquiry form page (v01, draft)

**Status: draft, not connected.** The page works and validates, but sends nothing anywhere until it is connected. Until then a black strip at the top says so, and the confirmation states plainly that nothing was sent.

- **What it is:** the page the QR code at the end of the franchise ad opens. Arabic `src/index.html`, English `src/index-en.html`. `src/` is self-contained (fonts and images inside, no external requests) and opens from any folder.
- **Connect it:** edit `src/js/config.js` only. Options for the client to choose from: a form service (Formspree, Basin); Google Apps Script writing to a Google Sheet (`FORM_FORMAT: "form"`); the client's own website or CRM endpoint; or a WhatsApp link (`WHATSAPP_NUMBER`) as a no-server alternative. No real service has been tested; success, failure and WhatsApp paths were exercised by browser simulation only.
- **Host it:** upload the contents of `src/` to any HTTPS static host, then generate the QR from the final URL.
- **Needed from the client:** submission destination; domain or URL; privacy notice text or link, with legal review of the consent wording; whether to add an investment-capacity question (left out: its ranges are figures we do not have); markets offered (the city field is free text); whether email is required; approval of the confirmation sentence; a Saudi reader's proofread of the Arabic.
