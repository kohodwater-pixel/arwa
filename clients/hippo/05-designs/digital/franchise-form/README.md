# هيبو — صفحة نموذج الاستفسار عن الامتياز (v02، مسودة)

**الحالة: مسودة غير موصولة.** الصفحة تعمل وتتحقق من الحقول، لكنها لا ترسل شيئًا حتى يوضع رابط الاستقبال في ملف الإعدادات. ما دامت غير موصولة يظهر شريط أسود أعلاها يقول ذلك، ورسالة التأكيد تقول صراحةً إن شيئًا لم يُرسَل.

## ما هي
الصفحة التي يفتحها رمز QR في نهاية إعلان الامتياز: مقدمة قصيرة تحمل «حُطّ ثقلك.»، ثم نموذج من خطوتين (بياناتك، ثم طلبك)، ثم رسالة التأكيد. عربية `src/index.html` وإنجليزية `src/index-en.html` مع زر تبديل. مجلد `src/` مكتفٍ بنفسه (الخطوط والصور داخله، ولا يتصل بأي خدمة خارجية).

**قرارا العميل (2026-11-18):** الاستفسارات تُحفظ في جدول Google Sheet، والصفحة تُنشر على نطاق شركة العميل (اسم النطاق لم يصلنا بعد).

## ربط النموذج بجدول Google — خطوة بخطوة
لا تحتاج مبرمجًا. تحتاج حساب Google الذي سيملك الجدول.

1. **أنشئ الجدول:** افتح Google Sheets وأنشئ جدولًا جديدًا فارغًا وسمِّه (مثلًا: استفسارات امتياز هيبو).
2. **افتح محرر السكربت:** من القائمة أعلى الجدول: Extensions (الإضافات) › Apps Script.
3. **الصق الكود:** احذف ما في المحرر، ثم افتح الملف `integrations/google-sheet/Code.gs` وانسخ محتواه كله والصقه، واضغط حفظ.
4. **انشره كتطبيق ويب:** Deploy › New deployment › النوع Web app، ثم اختر:
   - Execute as: **Me** (أنا)
   - Who has access: **Anyone** (أي شخص)

   اضغط Deploy ووافق على الأذونات التي يطلبها Google.
5. **انسخ الرابط** الذي ينتهي بـ `/exec`.
6. **ضعه في الصفحة:** افتح `src/js/config.js` والصق الرابط بين علامتي التنصيص في السطر `FORM_ENDPOINT: ""`. لا تغيّر شيئًا آخر.
7. **جرّب:** افتح الصفحة، عبّئ استفسارًا تجريبيًا وأرسله، ثم افتح الجدول: يجب أن يظهر صف جديد في تبويب اسمه `Enquiries` (يُنشأ تلقائيًا مع صف العناوين). إن لم يظهر الصف فالربط لم ينجح؛ لا تنشر الصفحة قبل نجاح هذه التجربة.

إذا عدّلت الكود لاحقًا: Deploy › Manage deployments › تعديل › Version: New version، حتى يبقى الرابط نفسه.

### ما الذي تؤكده الصفحة وما الذي لا تؤكده
- تظهر رسالة «وصل استفسارك» **فقط** إذا ردّ السكربت بأنه حفظ الصف.
- إذا لم تستطع الصفحة قراءة الرد (انقطاع الاتصال في لحظة الرد، أو إعداد نشر خاطئ) تظهر رسالة «تعذّر الإرسال» مع بقاء البيانات في النموذج. في حالات نادرة قد يكون الصف قد حُفظ فعلًا فيعيد الزائر الإرسال ويتكرر الصف؛ راجعوا التكرار في الجدول.
- الصفحة لا تعرف هل قرأ أحد الاستفسار، ولا ترسل تنبيهًا بالبريد. من يريد تنبيهًا يفعّله من الجدول نفسه (Tools › Notification settings).
- **لم نجرّب الكود على حساب Google حقيقي.** هذه البيئة لا تصل إلى Google؛ الكود كُتب وروجع بالقراءة، وجُرّب منطقه بخدمات وهمية، وجُرّب جانب الصفحة بخادم محاكاة يردّ بالشكل نفسه (إعادة توجيه ثم رد JSON). التجربة في الخطوة 7 هي الاختبار الحقيقي. أرقام الجوال تُحفظ نصًّا، وقد تظهر في الخلية مسبوقة بعلامة `'` إن بدأت بـ `+`.

## رفع الصفحة على نطاق الشركة
1. ارفع **محتويات** مجلد `src/` كما هي إلى مجلد على موقع الشركة، مثلًا `/franchise/`، فيصبح الرابط بالشكل: `https://نطاق-الشركة/franchise/`. يلزم أن يعمل الموقع بـ HTTPS.
2. افتح الرابط من جوال وتأكد من ظهور الصفحة بالعربية والإنجليزية، وأن الشريط الأسود «مسودة» اختفى (يختفي تلقائيًا بعد وضع رابط الاستقبال).
3. أرسل استفسارًا تجريبيًا من الرابط الحي وتأكد من وصول الصف.
4. **بعدها فقط** يُولَّد رمز QR من الرابط الحي النهائي ويوضع في الإعلان. لا يُولَّد الرمز من رابط مؤقت.

## خيارات استقبال أخرى (إن تغيّر القرار)
كلها من الملف نفسه `src/js/config.js`: خدمة نماذج جاهزة (Formspree أو Basin)؛ **جدول في قاعدة بيانات مستضافة** (كما في الصفحة المرجعية) عبر رابط يستقبل POST؛ موقع العميل أو نظام CRM عنده؛ أو واتساب (`WHATSAPP_NUMBER`) بديلًا بلا خادم.

## الحقول
**الخطوة 1 — بياناتك:** الاسم الكامل*، المهنة*، العمر* (18 فأكثر)، اسم الشركة، موقع الشركة، الجوال*، البريد الإلكتروني*.
**الخطوة 2 — طلبك:** الخبرة في المطاعم والمقاهي* (ست إجابات، و«غير ذلك» تفتح حقلًا مطلوبًا)، اسم علامتك، عدد الفروع التي تديرها، لماذا امتياز هيبو*، كم فرعًا تنوي افتتاحه*، مصدر الاستثمار*، المبلغ الذي تنوي استثماره* (رقم يكتبه المتقدم، ر.س، بلا شرائح ولا حد أدنى)، متى تتوقع أن تبدأ*، المدن التي تستهدفها* (نص حر)، هل لديك موقع، كيف سمعت عنا، ملاحظات، الموافقة*.
لا يوجد في الصفحة أي رقم أو ادعاء عن هيبو (رسوم، عوائد، عدد فروع، رأس مال مطلوب)، ولا قائمة مدن.

## مطلوب من العميل
1. اسم النطاق والمجلد الذي ستُنشر فيه الصفحة، ومن سيرفعها.
2. حساب Google الذي سيملك الجدول، ومن سيتابع الاستفسارات.
3. نص إشعار الخصوصية أو رابطه (مكانه خانة منقّطة واضحة)، ومراجعة مستشاره القانوني لصياغة الموافقة ولجمع العمر والمبلغ.
4. **سؤال «مدة استرداد رأس المال المتوقعة»** موجود في الصفحة المرجعية ولم نضعه: يدعو المتقدم إلى توقّع عائد لم تعلنه هيبو. هل يريده العميل؟
5. هل الامتياز متاح في مدن أو أسواق محددة؟ الحقل الآن نص حر.
6. اعتماد جملة التأكيد «سيتواصل معك فريق هيبو».
7. قراءة النص العربي من قارئ سعودي قبل النشر.

## ملاحظات للمطوّر
- الملفان `index.html` و`index-en.html` يُولَّدان من `_work/build_html.py` حتى لا يختلف النصّان؛ يمكن تعديلهما باليد، لكن إعادة تشغيل السكربت تمحو التعديل اليدوي.
- إعادة الفحص: `node _work/verify.cjs`. اللقطات في `hippo_franchise-form_screens_ar-en_v02/`. النسخة الأولى (خطوة واحدة) محفوظة في `_archive/`.

---

# HIPPO — franchise enquiry form page (v02, draft)

**Status: draft, not connected.** The page validates but sends nothing until the endpoint is pasted into the config. Until then a black strip says so and the confirmation states that nothing was sent.

**Client decisions (2026-11-18):** enquiries go to a Google Sheet; the page will be hosted on the client's own company domain (name not yet given).

## Connect to a Google Sheet
1. Create a new blank Google Sheet.
2. In the Sheet: Extensions › Apps Script.
3. Replace the editor's content with the whole of `integrations/google-sheet/Code.gs`; save.
4. Deploy › New deployment › Web app — Execute as: **Me**; Who has access: **Anyone**; authorise.
5. Copy the URL ending in `/exec`.
6. Paste it into `FORM_ENDPOINT` in `src/js/config.js`. Change nothing else.
7. Send one test enquiry and check that a row appears in the `Enquiries` tab. Do not publish before this works.

**What the page can and cannot confirm.** It shows "Your enquiry is in" only when the script answers that the row was stored. If the reply cannot be read, it shows an error and keeps the answers; in rare cases the row may already have been stored and a retry creates a duplicate. It does not send email alerts (set those in the Sheet). **The script has not been run against a real Google account**: it was reviewed by reading, its logic exercised with stubbed services, and the page tested against a local server that answers in the same shape (redirect, then JSON). Step 7 is the real test.

## Host it
Upload the contents of `src/` to a folder on the company site (for example `/franchise/`), over HTTPS. Test both languages and one real enquiry on the live URL. Only then generate the QR code from that final URL.

## Other destinations
A form service (Formspree, Basin); a hosted database table behind a POST endpoint (what the reference page uses); the client's own site or CRM; or WhatsApp (`WHATSAPP_NUMBER`). All set in `src/js/config.js`.

## Needed from the client
Domain and folder, and who uploads; the Google account that owns the Sheet and who follows up; privacy notice text or link, with legal review of the consent wording and of collecting age and investment amount; whether to add the reference's "expected payback period" question (left out: it invites a return expectation HIPPO has not stated); markets offered (cities field is free text); approval of the confirmation sentence; a Saudi reader's proofread of the Arabic.
