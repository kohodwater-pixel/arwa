# سدرة للقهوة — حزمة التسليم · Sidra Coffee — delivery package

> **اختبار نظام — عميل وهمي · SYSTEM TEST — FICTIONAL CLIENT.** «سدرة للقهوة» شركة غير موجودة؛ أُنتجت هذه الحزمة لاختبار Creative Agency OS.

# القسم العربي

## الحالة: محجوزة — لم تُسلَّم لعميل

مرّت الأعمال في هذه الحزمة بمراجعة الجودة الداخلية للوكالة على عدة جولات؛ تقارير كل الجولات ونتائجها في مجلد `_reviews/`، وآخر تقرير فيه هو المرجع لحالة كل عمل. الحزمة **غير صالحة للتسليم لعميل حقيقي** قبل استيفاء الشروط التالية:

1. **تدقيق لغوي بشري.** لم يدقّق أي نص عربي قارئٌ متمكّن بعد.
2. **مشاهدة تحريك الشعار مُشغَّلاً.** فُحص إطاراً بإطار فقط.
3. **رأي محامي علامات تجارية.** البحث الأولي وجد مخاطرة عالية في الاسم: مجمّع مطاعم باسم «Sidra» في الرياض. انظر `02-brand-guidelines/mark-check.md`.
4. **إعادة رسم الشعار اللفظي.** هو حالياً بخط IBM Plex Sans Arabic العريض دون رسم خاص.
5. **ألوان الطباعة.** لا توجد مراجع Pantone ولا قيم CMYK معايَرة ولا ملفات جاهزة للطباعة.
6. **بيانات تواصل حقيقية.** البريد `hello@sidra-coffee.example` تجريبي، ولا يوجد رقم هاتف.
7. **اعتماد العميل.** لم يعتمد أي عميل شيئاً؛ لذلك تحمل أسماء الملفات أرقام إصدارات (`v01` إلى `v04`) وليس كلمة `final`، ولا تُسمّى `final` إلا بعد الاعتماد.
8. **تنظيف نسخة العميل.** تُحذف عبارة «SYSTEM TEST» أينما وردت (دليل الهوية، وثيقة الاستراتيجية، `FONTS.md`، عناوين ملفات HTML، `tokens.json`)، وتُحذف النقاط الداخلية «ما زال مفتوحاً» من دليل الهوية، ويُحذف مجلد `_reviews/`.

نقاط صغيرة معروفة (لا تمنع الاستخدام الداخلي): الصفحة الأخيرة من دليل الهوية وملفات `licences.md` و`mark-check.md` و`tokens.json` تذكر مجلدات عمل الوكالة لا مجلدات هذه الحزمة، ويرد في `mark-check.md` الاسم «Sidra Coffee Roastery» بدل «Sidra Coffee»؛ شعارات العرض التقديمي صور وليست متجهات؛ العرض جُرّب على LibreOffice فقط لا PowerPoint؛ عند عرض 320 بكسل ينكسر سطر التعريف في أعلى صفحة الهبوط بشكل غير متوازن؛ تطبيقا الهوية (بطاقة العمل وملصق الكيس) معاينتان داخل دليل الهوية فقط.

## محتوى المجلدات

| المجلد | المحتوى | الاستخدام |
|---|---|---|
| `00-brand-strategy/` | ملخص استراتيجية العلامة: الجمهور، المكانة، الشخصية، الرسائل، نبرة التواصل، قاعدة الاسم، المخاطر والأسئلة المفتوحة. PDF من 8 صفحات مع نصّه | مرجع لكل من يكتب أو يصمّم للعلامة |
| `01-logo/` | الشعار بصيغة SVG (الملف الأصلي)، وPNG بثلاثة مقاسات بخلفية شفافة، وPDF متجه | المواقع والمستندات: PNG أو SVG. المطابع واللوحات: PDF أو SVG |
| `02-brand-guidelines/` | دليل الهوية PDF (6 صفحات، عربي وإنجليزي)؛ `tokens.json` (الألوان ومقاسات الخط والمسافات كبيانات للمطوّرين)؛ ملاحظات الخطوط والتراخيص؛ فحص الاسم والعلامة | طريقة استخدام الشعار والألوان والخطوط |
| `03-stationery-print/` | فارغ؛ انظر ملف README داخله | — |
| `04-digital-social/` | منشور إنستغرام (PNG بمقاس 1080 × 1350)؛ تحريك الشعار (MP4 مدته 3 ثوانٍ) مع صورة غلافه؛ نموذج صفحة الهبوط (افتح `landing-page/index.html` في المتصفح؛ النموذج لا يرسل شيئاً) | وسائل التواصل والويب |
| `05-profile/` | بروفايل الشركة، 4 صفحات، عربي وإنجليزي، PDF للشاشة | الإرسال لأصحاب المقاهي |
| `06-presentations/` | عرض لأصحاب المقاهي، 5 شرائح، عربي: PowerPoint قابل للتحرير وPDF. اقرأ `FONTS.md` أولاً | العرض أو الإرسال |
| `07-fonts-and-licences/` | خطّا IBM Plex Sans Arabic وIBM Plex Sans مع نص ترخيص SIL Open Font | ثبّتها قبل فتح ملف PowerPoint |
| `08-source-files/` | الملفات المصدرية القابلة للتحرير، كلٌّ في مجلد مكتفٍ بذاته | التعديلات لاحقاً |
| `_reviews/` | تقارير مراجعة الجودة (داخلية) | للتوثيق |

خارج نطاق هذا المشروع، فلا توجد هنا: ملفات الطباعة، نسخ إنجليزية من العرض والمنشور وصفحة الهبوط، وأكثر من منشور واحد.

## أي ملف شعار أستخدم؟

أسماء الملفات على هيئة `…_logo_<التركيب>-<اللون>_…`. «التركيب» (lockup) هو طريقة ترتيب أجزاء الشعار.

- **الاستخدام العادي:** `primary-colour` على الخلفيات الفاتحة، و`primary-colour-reversed` على الداكنة.
- **مع الاسم الإنجليزي:** `bilingual-…`، ولا يصغر عن 48 بكسل ارتفاعاً على الشاشة.
- **المقاسات الصغيرة (16 إلى 31 بكسل ارتفاعاً):** النسخ المنتهية بـ `-small`. وأصغر من ذلك: `wordmark-…` وحده.
- **أيقونة تطبيق أو صورة حساب:** `icon-…_v02` من 48 بكسل فأكبر، و`icon-small-…` لما دون ذلك.
- **طباعة بلون واحد أو ختم:** `…-black` أو `…-white`.

## الألوان

| الاسم | HEX | RGB |
|---|---|---|
| جمر — Ember | #C23A20 | 194, 58, 32 |
| حبر — Ink | #1F1B18 | 31, 27, 24 |
| ورق — Paper | #F3ECE0 | 243, 236, 224 |
| كريما — Crema | #E3C9A0 | 227, 201, 160 |
| رماد — Ash | #6F6861 | 111, 104, 97 |

قيم الطباعة (CMYK وPantone) غير محدّدة؛ انظر الشرط 5.

## الخطوط

العربية: IBM Plex Sans Arabic. الإنجليزية: IBM Plex Sans. كلاهما مجاني للاستخدام التجاري بترخيص SIL Open Font (النصوص في `07-fonts-and-licences/`).

## قاعدة الاسم

يُكتب الاسم كاملاً دائماً: «سدرة للقهوة» / "Sidra Coffee". لا تُكتب «سدرة» أو "Sidra" وحدها في أي نص. الاستثناء الوحيد كلمة «سدرة» داخل الشعار نفسه.

---

# English section

## Status: HELD — not released to a client

The pieces in this package went through the agency's internal quality review over several rounds; every round's report and verdicts are in `_reviews/`, and the latest report there is the reference for each piece's status. The package is **not** cleared for a real client until:

1. **Arabic proofread by a native reader.** No person has proofread any Arabic text.
2. **Someone watches the logo animation played back.** It was checked frame by frame only.
3. **Trademark advice.** A preliminary search found a high name risk: a "Sidra" dining complex operates in Riyadh. See `02-brand-guidelines/mark-check.md`.
4. **Wordmark redraw.** The Arabic wordmark is set in IBM Plex Sans Arabic Bold, not custom-drawn.
5. **Print colour.** No Pantone references, no calibrated CMYK values, no print-ready files.
6. **Real contact details.** The email `hello@sidra-coffee.example` is a test address; there is no phone number.
7. **Client approval.** No client has approved anything. That is why file names carry version numbers (`v01` to `v04`) and not the word `final`; files are renamed `final` only after approval.
8. **Client copy clean-up.** Remove "SYSTEM TEST" wherever it appears (guidelines, strategy document, `FONTS.md`, HTML titles, `tokens.json`), remove the internal "still open" points from the guidelines, and delete the `_reviews/` folder.

Known small points (none blocks internal use): the guidelines' last page and the files `licences.md`, `mark-check.md` and `tokens.json` refer to the agency's working folders, not this package's folders, and `mark-check.md` writes "Sidra Coffee Roastery" where the name rule says "Sidra Coffee"; the presentation's logos are images, not vector; the presentation was rendered in LibreOffice only, never opened in PowerPoint; at a 320 px phone width the landing page's hero caption breaks awkwardly; the two identity applications (business card, bag label) appear only as previews inside the guidelines.

## What is in each folder

| Folder | Contents | Use it for |
|---|---|---|
| `00-brand-strategy/` | Brand strategy summary: audience, positioning, personality, messages, tone of voice, name rule, risks and open questions. PDF (8 pages) and its text file | Briefing anyone who writes or designs for the brand |
| `01-logo/` | The logo as SVG (the master artwork), PNG at three sizes with transparent background, and vector PDF | Websites and documents: PNG or SVG. Printers and sign makers: PDF or SVG |
| `02-brand-guidelines/` | Brand guidelines PDF (6 pages, Arabic and English); `tokens.json` (the colours, type sizes and spacing as data for developers); font and licence notes; the name and mark check | How to use the logo, colours and fonts |
| `03-stationery-print/` | Empty; see its README | — |
| `04-digital-social/` | Instagram post (1080 × 1350 PNG); logo animation (3-second MP4) with its poster image; landing page prototype (open `landing-page/index.html` in a browser; its form does not send anything) | Social media and web |
| `05-profile/` | Company profile, 4 pages, Arabic and English, screen PDF | Sending to café owners by email |
| `06-presentations/` | Presentation for café owners, 5 slides, Arabic: editable PowerPoint and PDF. Read `FONTS.md` first | Presenting or sending |
| `07-fonts-and-licences/` | IBM Plex Sans Arabic and IBM Plex Sans with their SIL Open Font Licence texts | Install before opening the PowerPoint |
| `08-source-files/` | Editable sources, each self-contained | Future changes |
| `_reviews/` | The agency's quality review reports (internal) | Record |

Out of scope, so not here: print files, an English version of the presentation, post and landing page, and more than one social post.

## Which logo file?

File names follow `…_logo_<layout>-<colour>_…`. A "lockup" is one arrangement of the logo's parts.

- **Normal use:** `primary-colour` on light backgrounds; `primary-colour-reversed` on dark ones.
- **With the English name:** `bilingual-…`. Not smaller than 48 px high on screen.
- **Small sizes (16 to 31 px high):** the `-small` versions. Below that, `wordmark-…` alone.
- **App icon or avatar:** `icon-…_v02` at 48 px and above; `icon-small-…` below.
- **One-colour printing or stamps:** `…-black` or `…-white`.

## Colours

| Name | HEX | RGB |
|---|---|---|
| Ember | #C23A20 | 194, 58, 32 |
| Ink | #1F1B18 | 31, 27, 24 |
| Paper | #F3ECE0 | 243, 236, 224 |
| Crema | #E3C9A0 | 227, 201, 160 |
| Ash | #6F6861 | 111, 104, 97 |

Print (CMYK, Pantone) values are not set; see hold 5.

## Fonts

Arabic: IBM Plex Sans Arabic. English: IBM Plex Sans. Both are free to use commercially under the SIL Open Font Licence (texts in `07-fonts-and-licences/`).

## Name rule

Always write the full name: «سدرة للقهوة» / "Sidra Coffee". Never «سدرة» or "Sidra" alone in text. The word «سدرة» inside the logo is the only exception.
