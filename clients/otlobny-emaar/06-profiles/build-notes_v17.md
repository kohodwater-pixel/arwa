# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v17

**Date:** 2026-11-16
**Author:** corporate-designer
v16 is untouched. 20 pages.

## p6 Services overview
- **Banner:** now full colour. The blue duotone is removed. The crop is unchanged (umbrella crown and minarets), with the standard light grade used on the other colour photos.
- **Saudi Vision 2030 logo:** the client's file, copied to `assets/logo/logo_saudi-vision-2030.png` and used unaltered (no recolouring, no stretching, no effects).
  - **Width:** 36 mm.
  - **Placement:** a white tab with rounded top corners rising from the white page into the banner's lower-right corner. That is the Arabic reading-start side, above the Arabic title.
  - **Clear space:** 5.4 mm on every side (15% of the logo width).
  - **Spacing:** nothing overlaps the logo, and it is far from the OTLOBNY lockup, which is not on this page.
  - **Option (b) not chosen:** the sky behind the banner is too pale and grey for the grey logo to read reliably, and it would sit against the umbrella detail.
- **300 dpi check:** `_work/v17/check300_p06_vision2030.png`.

## Service area (client 2026-11-16)
- **p1 cover, p20 back cover:** city tag «المدينة المنورة» changed to «المملكة العربية السعودية».
- **p3 About body:**
  - Arabic: «… تأسست عام 2021 وتعمل بموجب السجل التجاري رقم 4650245200، وتخدم جميع مناطق المملكة العربية السعودية.»
  - English: "… founded in 2021, operating under Commercial Registration No. 4650245200 and serving all regions of the Kingdom of Saudi Arabia."
- **p3 fact strip:** «المقر / Based in — المدينة المنورة» changed to «نطاق الخدمة / Service area — جميع مناطق المملكة / All regions of the Kingdom».
- **Alt text:** "Al Madinah Al Munawwarah" removed from the alt text of the two Prophet's Mosque photos.
- **Why-us:** unchanged. A line about serving all regions would repeat p3 and would need rewording one of the six points.

**Where «المدينة المنورة» / "Madinah" still appears in the PDF, and why:**
- **p13 why-us #03:** the Chamber's name, «الغرفة التجارية والصناعية في المدينة المنورة» / "Madinah Chamber". Proper name.
- **p15 Chamber work page:** the Chamber's name in the title and body. Proper name.
- **p19 contact:** the postal address «طريق الأمير عبدالمجيد بن عبدالعزيز، المدينة المنورة، …». Legal and contact data.
- **Partner logos:** names inside the logo artwork, for example "Madinah Chamber" and the Medina Dates Festival. These are images, not text, and are the partners' own marks.
- **PDF metadata:** the title has no Madinah.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: PASS.
- Forbidden strings: 0.
- Bookmarks: 2, 3, 4, 6, 13, 14, 17, 19.
- No image is used on two pages.
- Viewed: p6 at full size, the logo at 300 dpi, and pp1–10 on the contact sheet.
