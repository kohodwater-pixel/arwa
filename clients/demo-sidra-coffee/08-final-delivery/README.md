# Sidra Coffee — delivery package / حزمة التسليم

> **SYSTEM TEST — FICTIONAL CLIENT.** "Sidra Coffee" does not exist; this package was produced to test Creative Agency OS.

## Status: HELD — not released to a client · الحالة: محجوزة، لم تُسلَّم لعميل

Every piece here passed the agency's quality review with no critical or major issue open (rounds 1 to 3, reports in `_reviews/`). It is **not** cleared for a real client until all of these are done:

1. **Arabic proofread by a native reader.** No person has proofread any Arabic text. / لم يدقّق قارئ بشري أي نص عربي بعد.
2. **Someone watches the logo animation played back.** It was checked frame by frame only.
3. **Trademark advice.** A preliminary search found a high name risk: a "Sidra" dining complex operates in Riyadh. See `02-brand-guidelines/mark-check.md`. A trademark attorney must advise before the name or mark is used.
4. **Wordmark redraw.** The Arabic wordmark is set in IBM Plex Sans Arabic Bold, not custom-drawn.
5. **Print colour.** No Pantone references and no calibrated CMYK values exist. Nothing here is print-ready.
6. **Real contact details.** The email `hello@sidra-coffee.example` is a test address; there is no phone number.
7. **Minor review notes** still open on the profile, deck and social post are listed in `_reviews/review_all-deliverables_2026-11-13_r2.md` (N8, N9, N11).

## What is in each folder · محتوى المجلدات

| Folder | Contents | Use it for |
|---|---|---|
| `01-logo/` | The logo as SVG (master), PNG at 1x/2x/4x with transparent background, and vector PDF. Lockups: `primary` (Arabic), `bilingual`, `latin`, `icon`, `wordmark`; each also as `-small`. Colours: `colour`, `colour-reversed`, `colour-on-ember`, `black`, `white` | Websites and documents: PNG or SVG. Printers and sign makers: PDF or SVG |
| `02-brand-guidelines/` | Brand guidelines PDF (6 pages, Arabic and English), `tokens.json` (colours, type sizes, spacing), font and licence notes, the name and mark check | How to use the logo, colours and fonts |
| `03-stationery-print/` | Empty; see its README | — |
| `04-digital-social/` | Instagram post (1080 × 1350 PNG), logo animation (3 s MP4) with its poster image, and the landing page prototype (open `landing-page/index.html` in a browser) | Social media and web |
| `05-profile/` | Company profile, 4 pages, Arabic and English, screen PDF | Sending to café owners by email |
| `06-presentations/` | Presentation for café owners, 5 slides, Arabic: editable PowerPoint and PDF. Read `FONTS.md` first | Presenting or sending |
| `07-fonts-and-licences/` | IBM Plex Sans Arabic and IBM Plex Sans, with their SIL Open Font Licence texts | Install these before opening the PowerPoint |
| `08-source-files/` | Where the editable sources are | Future changes |
| `_reviews/` | The three quality review reports | Record |

## Which logo file? · أي ملف شعار أستخدم؟

- **Normal use:** `primary-colour` on light backgrounds; `primary-colour-reversed` on dark ones.
- **With the English name:** `bilingual-…`. Not smaller than 48 px high on screen.
- **Small sizes (16 to 31 px high):** the `-small` versions. Below that, `wordmark-…` alone.
- **App icon or avatar:** `icon-…_v02` at 48 px and above; `icon-small-…` below.
- **One-colour printing or stamps:** `…-black` or `…-white`.

## Colours · الألوان

| Name | HEX |
|---|---|
| Ember — جمر | #C23A20 |
| Ink — حبر | #1F1B18 |
| Paper — ورق | #F3ECE0 |
| Crema — كريما | #E3C9A0 |
| Ash — رماد | #6F6861 |

## Fonts · الخطوط

Arabic: IBM Plex Sans Arabic. English: IBM Plex Sans. Both are free to use commercially under the SIL Open Font Licence (texts in `07-fonts-and-licences/`).

## Name rule · قاعدة الاسم

Always write the full name: «سدرة للقهوة» / "Sidra Coffee". Never «سدرة» or "Sidra" alone in text.
