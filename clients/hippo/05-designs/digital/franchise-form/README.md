# هيبو — صفحة نموذج الاستفسار عن الامتياز (v03، مسودة)

**الحالة: مسودة غير موصولة.** الصفحة تعمل وتتحقق من الحقول، لكنها لا ترسل شيئًا حتى يوضع رابط الاستقبال في ملف الإعدادات. ما دامت غير موصولة يظهر شريط أسود أعلاها يقول ذلك، ورسالة التأكيد تقول صراحةً إن شيئًا لم يُرسَل.

## ما هي
الصفحة التي يفتحها رمز QR في نهاية إعلان الامتياز: مقدمة قصيرة تحمل «حُطّ ثقلك.»، ثم نموذج من ثلاث خطوات (بياناتك، خبرتك، خطتك)، ثم رسالة التأكيد. عربية `src/index.html` وإنجليزية `src/index-en.html` مع زر تبديل يحفظ ما كُتب. مجلد `src/` مكتفٍ بنفسه: الخطوط والصور داخله، ولا يتصل بأي خدمة خارجية.

**قرارا العميل (2026-11-18):** الاستفسارات تُحفظ في جدول Google Sheet، والصفحة تُنشر على نطاق شركة العميل (اسم النطاق لم يصلنا بعد).

## ربط النموذج بجدول Google — خطوة بخطوة
لا تحتاج مبرمجًا. تحتاج حساب Google الذي سيملك الجدول.

1. **أنشئ الجدول:** افتح Google Sheets وأنشئ جدولًا جديدًا فارغًا وسمِّه (مثلًا: استفسارات امتياز هيبو). **أبقِ مشاركة الجدول خاصة** (لك ولمن يتابع الاستفسارات فقط): فيه بيانات شخصية للمتقدمين.
2. **افتح محرر السكربت:** من القائمة أعلى الجدول: Extensions (الإضافات) › Apps Script.
3. **الصق الكود:** احذف ما في المحرر، ثم افتح الملف `integrations/google-sheet/Code.gs` وانسخ محتواه كله والصقه، واضغط حفظ.
4. **انشره كتطبيق ويب:** Deploy › New deployment › النوع Web app، ثم اختر:
   - Execute as: **Me** (أنا)
   - Who has access: **Anyone** (أي شخص). ليس «Anyone with a Google account»؛ بهذا الخيار لن يصل أي استفسار.

   اضغط Deploy.
5. **شاشة التحذير من Google:** ستظهر شاشة «Google hasn't verified this app» (لم يتحقق Google من هذا التطبيق). هذا متوقع لأن السكربت خاص بك. اضغط **Advanced** ثم **Go to (اسم المشروع)** ثم Allow.
   - إن كان الحساب حساب شركة (Google Workspace) فقد يمنع مسؤول النظام خيار «Anyone». عندها اطلب منه السماح، أو استخدم حساب Google عاديًّا.
6. **انسخ الرابط** الذي ينتهي بـ `/exec`.
7. **فحص سريع:** الصق الرابط في المتصفح. يجب أن يظهر سطر يبدأ بـ `{"ok":true`. إن ظهرت صفحة تسجيل دخول أو خطأ فالنشر غير صحيح (راجع الخطوة 4).
8. **ضعه في الصفحة:** افتح `src/js/config.js` بمحرر نصوص عادي (Notepad في ويندوز أو TextEdit في ماك، وليس Word)، والصق الرابط بين علامتي التنصيص في السطر `FORM_ENDPOINT: ""`، واحفظ. لا تغيّر شيئًا آخر. إن كانت الصفحة مرفوعة على الموقع فأعد رفع هذا الملف.
9. **جرّب:** افتح الصفحة، عبّئ استفسارًا تجريبيًا وأرسله، ثم افتح الجدول: يجب أن يظهر صف جديد في تبويب اسمه `Enquiries` (يُنشأ تلقائيًا مع صف العناوين). إن لم يظهر الصف فالربط لم ينجح؛ لا تنشر الصفحة قبل نجاح هذه التجربة. بعد نجاحها **احذف صف التجربة**.

**رابط إشعار الخصوصية:** في الملف نفسه `src/js/config.js` الصق رابط النسخة العربية في `PRIVACY_URL_AR` والإنجليزية في `PRIVACY_URL_EN`. ما دام السطران فارغين تظهر مكان الرابط خانة منقّطة تقول إنه لم يصل بعد.

**إن عدّلت الكود لاحقًا:** استخدم Deploy › **Manage deployments** › تعديل (القلم) › Version: **New version**. هذا يُبقي الرابط نفسه. أما **New deployment** فيُنشئ رابطًا جديدًا، فيتوقف الرابط الموضوع في الصفحة عن استقبال التعديل، وإن تغيّر رابط الصفحة نفسها يتعطل رمز QR المطبوع.

### ما الذي يظهر في الجدول
- تبويب `Enquiries`: صف لكل استفسار. الأعمدة التي تنتهي بـ `_label` فيها الإجابة كما قرأها المتقدم (بلغة الصفحة)، والعمود الذي قبلها فيه رمز ثابت للفرز.
- تبويب `Spam`: الاستفسارات التي عبّأت حقلًا مخفيًّا لا يراه الزائر (فخ للبرامج الآلية). لا يُحذف شيء: راجعوا هذا التبويب بين حين وآخر، فقد يقع فيه متقدم حقيقي عبّأ متصفحُه الحقل تلقائيًّا.
- إعادة إرسال الاستفسار نفسه بعد خطأ في الاتصال لا تُنشئ صفًّا مكررًا.

### ما الذي تؤكده الصفحة وما الذي لا تؤكده
- تظهر رسالة «وصل استفسارك» **فقط** إذا ردّ السكربت بأنه حفظ الصف.
- إذا لم يصل رد خلال 25 ثانية، أو لم تستطع الصفحة قراءة الرد، تظهر رسالة «تعذّر الإرسال» مع بقاء البيانات في النموذج ليعيد الزائر المحاولة.
- الصفحة لا تعرف هل قرأ أحد الاستفسار، ولا ترسل تنبيهًا بالبريد. من يريد تنبيهًا يفعّله من الجدول نفسه (Tools › Notification settings).
- **لم نجرّب الكود على حساب Google حقيقي.** بيئة العمل لا تصل إلى Google؛ الكود كُتب وروجع بالقراءة، وجُرّب منطقه بخدمات وهمية، وجُرّب جانب الصفحة بخادم محاكاة يردّ بالشكل نفسه. التجربة في الخطوة 9 هي الاختبار الحقيقي. أرقام الجوال تُحفظ نصًّا، وقد تظهر في الخلية مسبوقة بعلامة `'` إن بدأت بـ `+`.

## رفع الصفحة على نطاق الشركة
1. ارفع **محتويات** مجلد `src/` كما هي إلى مجلد على موقع الشركة، مثلًا `/franchise/`، فيصبح الرابط بالشكل: `https://نطاق-الشركة/franchise/`. يلزم أن يعمل الموقع بـ HTTPS.
2. افتح الرابط من جوال وتأكد من ظهور الصفحة بالعربية والإنجليزية، وأن الشريط الأسود «مسودة» اختفى (يختفي تلقائيًا بعد وضع رابط الاستقبال).
3. أرسل استفسارًا تجريبيًا من الرابط الحي وتأكد من وصول الصف، ثم احذفه.
4. **بعدها فقط** يُولَّد رمز QR من الرابط الحي النهائي ويوضع في الإعلان. لا يُولَّد الرمز من رابط مؤقت.

## خيارات استقبال أخرى (إن تغيّر القرار)
كلها من الملف نفسه `src/js/config.js`: خدمة نماذج جاهزة (Formspree أو Basin)؛ جدول في قاعدة بيانات مستضافة (كما في الصفحة المرجعية) عبر رابط يستقبل POST؛ موقع العميل أو نظام CRM عنده؛ أو واتساب (`WHATSAPP_NUMBER`) بديلًا بلا خادم.

## الحقول
**الخطوة 1 — بياناتك:** الاسم الكامل*، المهنة*، العمر* (18 فأكثر)، اسم الشركة، موقع الشركة، الجوال*، البريد الإلكتروني*.
**الخطوة 2 — خبرتك:** الخبرة في المطاعم والمقاهي* (ست إجابات، و«غير ذلك» تفتح حقلًا مطلوبًا)، اسم علامتك، عدد الفروع التي تديرها، لماذا امتياز هيبو*.
**الخطوة 3 — خطتك:** كم فرعًا تنوي افتتاحه* (فرع واحد / من فرعين إلى خمسة / من ستة إلى عشرة / غير ذلك)، مصدر الاستثمار*، المبلغ الذي تنوي استثماره* (رقم يكتبه المتقدم، ر.س، بلا شرائح ولا حد أدنى)، متى تتوقع أن تبدأ* (فورًا / خلال 6 أشهر / خلال 6 إلى 12 شهرًا / خلال سنة إلى سنتين)، المدن التي تستهدفها* (نص حر)، هل لديك موقع، كيف سمعت عنا، ملاحظات، الموافقة*.
لا يوجد في الصفحة أي رقم أو ادعاء عن هيبو (رسوم، عوائد، عدد فروع، رأس مال مطلوب)، ولا قائمة مدن.

## مطلوب من العميل
1. اسم النطاق والمجلد الذي ستُنشر فيه الصفحة، ومن سيرفعها.
2. حساب Google الذي سيملك الجدول، ومن سيتابع الاستفسارات وتبويب `Spam`.
3. نص إشعار الخصوصية أو رابطه، ومراجعة مستشاره القانوني لصياغة الموافقة ولجمع العمر والمبلغ.
4. **سؤال «مدة استرداد رأس المال المتوقعة»** موجود في الصفحة المرجعية ولم نضعه: يدعو المتقدم إلى توقّع عائد لم تعلنه هيبو. هل يريده العميل؟
5. هل الامتياز متاح في مدن أو أسواق محددة؟ الحقل الآن نص حر.
6. اعتماد جملة التأكيد «سيتواصل معك فريق هيبو عبر بيانات التواصل التي كتبتها».
7. قراءة النص العربي من قارئ سعودي قبل النشر.

---

# HIPPO — franchise enquiry form page (v03, draft)

**Status: draft, not connected.** The page validates but sends nothing until the endpoint is pasted into the config. Until then a black strip says so and the confirmation states that nothing was sent.

**What it is:** the page the QR code at the end of the franchise ad opens: a short hero, a three-step form (About you, Your experience, Your plan) and a confirmation. Arabic `src/index.html`, English `src/index-en.html`; the language switch keeps what has been typed. `src/` is self-contained.

**Client decisions (2026-11-18):** enquiries go to a Google Sheet; the page will be hosted on the client's own company domain (name not yet given).

## Connect to a Google Sheet
1. Create a new blank Google Sheet. **Keep its sharing private**: it will hold applicants' personal data.
2. In the Sheet: Extensions › Apps Script.
3. Replace the editor's content with the whole of `integrations/google-sheet/Code.gs`; save.
4. Deploy › New deployment › Web app — Execute as: **Me**; Who has access: **Anyone** (not "Anyone with a Google account").
5. Google shows "Google hasn't verified this app". This is expected for your own script: Advanced › Go to (project name) › Allow. On a company Workspace account the administrator may block "Anyone"; ask them to allow it or use an ordinary Google account.
6. Copy the URL ending in `/exec`.
7. Quick check: open that URL in a browser. It should show a line starting `{"ok":true`. A sign-in or error page means the deployment is wrong.
8. Open `src/js/config.js` in a plain-text editor (Notepad, TextEdit; not Word), paste the URL into `FORM_ENDPOINT`, save, and re-upload that file if the page is already online.
9. Send one test enquiry and check that a row appears in the `Enquiries` tab; then delete the test row. Do not publish before this works.

**Privacy notice link:** paste it into `PRIVACY_URL_AR` and `PRIVACY_URL_EN` in the same file.

**Changing the script later:** use Deploy › **Manage deployments** › edit › Version: **New version**, which keeps the same URL. **New deployment** creates a different URL, so the one in the page stops receiving your change.

**In the Sheet:** `Enquiries` has one row per enquiry; `*_label` columns hold the answer as the applicant read it, the column before each holds a stable code. `Spam` holds enquiries that filled a hidden trap field; nothing is discarded, so look there occasionally in case a real applicant's browser autofilled it. Retrying the same enquiry after a connection error does not create a second row.

**What the page can and cannot confirm.** It shows "Your enquiry is in" only when the script answers that the row was stored. If no reply arrives within 25 seconds, or the reply cannot be read, it shows an error and keeps the answers. It does not send email alerts (set those in the Sheet). **The script has not been run against a real Google account**: it was reviewed by reading, its logic exercised with stubbed services, and the page tested against local servers that answer in the same shape. Step 9 is the real test.

## Host it
Upload the contents of `src/` to a folder on the company site (for example `/franchise/`), over HTTPS. Test both languages and one real enquiry on the live URL, then delete the test row. Only then generate the QR code from that final URL.

## Other destinations
A form service (Formspree, Basin); a hosted database table behind a POST endpoint (what the reference page uses); the client's own site or CRM; or WhatsApp (`WHATSAPP_NUMBER`). All set in `src/js/config.js`.

## Needed from the client
Domain and folder, and who uploads; the Google account that owns the Sheet and who follows up enquiries and the Spam tab; privacy notice text or link, with legal review of the consent wording and of collecting age and investment amount; whether to add the reference's "expected payback period" question (left out: it invites a return expectation HIPPO has not stated); markets offered (the cities field is free text); approval of the confirmation sentence; a Saudi reader's proofread of the Arabic.
