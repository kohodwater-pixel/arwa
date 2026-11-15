# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v12

**Date:** 2026-11-15 · **Author:** corporate-designer

**Input:** client instruction of 2026-11-15 (brand-context.md): remove the photo sources and credits from the profile. v11 is untouched. The profile still has 20 pages.

## What changed
- **p20 is now a full-page back cover.** The navy→royal gradient fills the whole page, with the white lockup v02 (100 mm wide) and otlobny.net · «المدينة المنورة» in white beneath it, centred.
- **Credits band removed, in both languages:** photo credits, the no-attribution list and the rights note are gone.
- **"Photo credits" PDF bookmark removed.** Bookmarks now point to pages 2, 3, 4, 6, 13, 14, 17 and 19.
- **Unused credit CSS removed** from the HTML.
- **Nothing else changed.** The other 19 pages are identical to v11.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v12.pdf`
- `otlobny-emaar_company-profile_screen_ar-en_v12.html`
- `_work/build_profile_v12.py`
- `_work/finish_pdf_v12.py`
- `_work/contact_v12.py`
- `_work/contact_v12_part1/2.png`
- `_work/preview_v12/`
- `_work/build_v12.log`
- `_work/check_v12.log`

## Checks
- **`check_arabic_pdf.py --expect "اطلبني إعمار"`:** PASS.
- **PDF text search, all 0:** "Photo credits", "CC BY", "Flickr", "Wikimedia", "licence", «حقوق الصور», «المشاع»; also "Emaar", «شهد» and "draft".
- **HTML search:** 0 for credit, licen, flickr, wikimedia, CC BY, «حقوق الصور» and «المشاع».
- **p20:** viewed at full preview size.

## Licensing record
`assets/stock/CREDITS.md` and `README.md` are unchanged and kept on file. The profile no longer carries the attributions that the CC BY / CC BY-SA licences require. That decision is the client's and needs to be recorded with the CD.
