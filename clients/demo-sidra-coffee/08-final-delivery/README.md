# Sidra Coffee — delivery package · سدرة للقهوة — حزمة التسليم

> **SYSTEM TEST — FICTIONAL CLIENT · اختبار نظام — عميل وهمي.** "Sidra Coffee" does not exist; this package was produced to test Creative Agency OS.

## الحالة: محجوزة — لم تُسلَّم لعميل

كل عمل في هذه الحزمة اجتاز مراجعة الجودة الداخلية دون ملاحظات حرجة أو رئيسية (التقارير في `_reviews/`). لكنها **غير صالحة للتسليم لعميل حقيقي** قبل استيفاء الشروط التالية:

1. تدقيق لغوي لكل النصوص العربية يقوم به قارئ بشري متمكّن.
2. مشاهدة تحريك الشعار مُشغَّلاً (فُحص إطاراً بإطار فقط).
3. رأي محامي علامات تجارية: البحث الأولي وجد مخاطرة عالية في الاسم (مجمّع مطاعم باسم «Sidra» في الرياض). انظر `02-brand-guidelines/mark-check.md`.
4. إعادة رسم الشعار اللفظي (حالياً بخط IBM Plex Sans Arabic دون رسم خاص).
5. ألوان الطباعة: لا توجد مراجع Pantone ولا قيم CMYK معايَرة، ولا ملفات جاهزة للطباعة.
6. بيانات تواصل حقيقية: البريد `hello@sidra-coffee.example` تجريبي، ولا يوجد رقم هاتف.
7. اعتماد العميل. لم يعتمد أي عميل شيئاً؛ لذلك تحمل أسماء الملفات أرقام إصدارات (`v01`–`v04`) وليس كلمة `final`.
8. نسخة العميل تُنزع منها عبارة «SYSTEM TEST» والنقاط الداخلية في دليل الهوية، ويُحذف مجلد `_reviews/`.

## Status: HELD — not released to a client

Every piece here passed the agency's internal quality review with no critical or major issue open (reports in `_reviews/`, rounds 1 to 5). It is **not** cleared for a real client until:

1. **Arabic proofread by a native reader.** No person has proofread any Arabic text.
2. **Someone watches the logo animation played back.** It was checked frame by frame only.
3. **Trademark advice.** A preliminary search found a high name risk: a "Sidra" dining complex operates in Riyadh. See `02-brand-guidelines/mark-check.md`.
4. **Wordmark redraw.** The Arabic wordmark is set in IBM Plex Sans Arabic Bold, not custom-drawn.
5. **Print colour.** No Pantone references, no calibrated CMYK values, no print-ready files.
6. **Real contact details.** The email `hello@sidra-coffee.example` is a test address; there is no phone number.
7. **Client approval.** No client has approved anything. That is why file names carry version numbers (`v01` to `v04`) and not the word `final`; files are renamed `final` only after approval.
8. **Client copy clean-up.** Remove the "SYSTEM TEST" footers and the internal "still open" points from the guidelines, and delete the `_reviews/` folder.

Known small points still open (none blocks internal use): the guidelines' last page lists the agency's working folders, not this package's folders; the presentation's logos are images, not vector; the presentation was rendered in LibreOffice only, never opened in PowerPoint; at a 320 px phone width the landing page's hero caption breaks awkwardly; the two identity applications (business card, bag label) appear only as previews inside the guidelines.

## What is in each folder · محتوى المجلدات

| Folder | Contents | Use it for |
|---|---|---|
| `00-brand-strategy/` | Brand strategy summary: audience, positioning, personality, messages, tone of voice, name rule, risks and open questions. PDF (6 pages) and its text file | Briefing anyone who writes or designs for the brand |
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

## Which logo file? · أي ملف شعار أستخدم؟

File names follow `…_logo_<layout>-<colour>_…`. A "lockup" is one arrangement of the logo's parts.

- **Normal use:** `primary-colour` on light backgrounds; `primary-colour-reversed` on dark ones.
- **With the English name:** `bilingual-…`. Not smaller than 48 px high on screen.
- **Small sizes (16 to 31 px high):** the `-small` versions. Below that, `wordmark-…` alone.
- **App icon or avatar:** `icon-…_v02` at 48 px and above; `icon-small-…` below.
- **One-colour printing or stamps:** `…-black` or `…-white`.

## Colours · الألوان

| Name | HEX | RGB |
|---|---|---|
| Ember — جمر | #C23A20 | 194, 58, 32 |
| Ink — حبر | #1F1B18 | 31, 27, 24 |
| Paper — ورق | #F3ECE0 | 243, 236, 224 |
| Crema — كريما | #E3C9A0 | 227, 201, 160 |
| Ash — رماد | #6F6861 | 111, 104, 97 |

Print (CMYK, Pantone) values are not set; see hold 5.

## Fonts · الخطوط

Arabic: IBM Plex Sans Arabic. English: IBM Plex Sans. Both are free to use commercially under the SIL Open Font Licence (texts in `07-fonts-and-licences/`).

## Name rule · قاعدة الاسم

Always write the full name: «سدرة للقهوة» / "Sidra Coffee". Never «سدرة» or "Sidra" alone in text. The word «سدرة» inside the logo is the only exception.
