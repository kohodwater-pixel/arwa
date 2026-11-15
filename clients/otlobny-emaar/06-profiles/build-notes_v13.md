# Build notes — «اطلبني إعمار» / OTLOBNY Emar company profile v13

**Date:** 2026-11-15 · **Author:** corporate-designer
**Input:** client feedback on v12 (brand-context.md, 2026-11-15; files in `_originals/client-uploads_2026-11-15/`). These rules still apply: no captions, no credits, no "draft". v12 is untouched. 20 pages.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v13.pdf` and `.html`
- `_work/build_profile_v13.py` (run `_work/v13/garments_v13.py` first)
- `_work/v13/garments_v13.py`: logo fixes on garments; writes `assets/derived/v13_client_*.png`
- `_work/v13/check_*.png`: before/after at 4×
- `_work/v13/check300_page_*.png`: crops from the 300 dpi render of the PDF
- `_work/v13/rejected_padded-square_palm-team.png`: rejected attempt, kept for the record
- `assets/mockups/`: copies of the three client photos (originals untouched)
- `_work/finish_pdf_v13.py`, `_work/contact_v13.py`, `_work/contact_v13_part1/2.png`, `_work/preview_v13/`, `_work/build_v13.log`, `_work/check_v13.log`
- `content-outline.md`: v13 block added (earlier text in `_archive/`)

## Changes by point

**1. Landscaping, p8**
- **Double diamond:** the client's palm-planting team, cropped square at 1024 px, centred on the palm. It shows all three workers; the outer two are trimmed at the diamond edges. Effective resolution 178 ppi.
- **Normal diamond:** the client's street-planting photo at 338 ppi. The remaining cells are tint and navy fills.
- Both images are full colour, ungraded.
- The Doha and San Diego stock images are gone from the book.
- I tried padding the photo to a square by extending sky and grass. It smeared the palm fronds and mirrored the workers, so I rejected it.

**2. Cover, p1**
- The triptych is split at its white gutters (x 715–727 and 1444–1455).
- **Hero:** the two engineers in full colour, 94 ppi. Each panel is only 716 px wide, so the hero is soft when zoomed in; it looks fine at page size on screen.
- **Small diamonds:**
  - the window cleaner, 229 ppi, framed so his whole back lockup sits inside the diamond;
  - the landscaping panel, cropped close on the tree and flowers so it differs from the wide street view on p8, 220 ppi.
- No other client image was free to use. The old AI mockups still carry malformed logos and the fleet image is already used. The remaining cells are brand colours: tint, two navy gradients and royal blue, plus the green accent.
- The blue duotone is removed from the cover.
- The steel erector is removed from the book; p7 already uses the glass facade.
- **Title:** «الملف التعريفي» is removed. "Company Profile" now sits just above the bottom green rule, at 170 mm, on the text column. The lockup stays at the top with open space below it.
- **Clear space:** the collage geometry and lockup are unchanged, so the nearest collage edge is still 9.6 mm from the lockup box; X is 5.5 mm.
- The p2 kicker «الملف التعريفي» / "Company Profile" is also removed, so the phrase appears on no visible page. It remains only in the PDF title metadata, as allowed.

**3. Logos on garments** (checked at 4× and in the 300 dpi page render)
- **Engineers' vests:** malformed descriptor (garbled Latin, «اطليني»). Painted out and replaced with the white lockup v02 in perspective. These logos fall outside the cover's diamond crop, so they do not show on the page.
- **Window cleaner's back:** malformed «اطليني». Replaced with the white lockup v02. Shows on the cover; reads as printed.
- **Palm team, left worker's back:** wordmark replaced with the real white wordmark, rotated 24° to the slope of the back.
- **Palm team, right worker's shoulder:** the logo sits over the shoulder curve, so it is painted out only (clean garment).
  - Residue: a few specks of about 3 px remain at the shoulder edge, roughly 0.5 mm on the page.
  - That spot falls outside the p8 diamond crop.
- **Left alone:** cap and glove marks on the palm team. They are tiny AI marks, roughly legible at 300 dpi but not readable at page size.

**4. Madinah Chamber, p15, and Why #03, p13**
- New body text and four chips, exactly as instructed: نظافة المرافق · الضيافة · التشغيل · الصيانة / Facility cleaning · Hospitality · Operation · Maintenance.
- The chips now wrap onto two rows in each language.
- Why #03 uses the new text.
- The Arabic column on p13 was widened to 119 mm with slightly smaller type (12 pt title, 10 pt description), so the two-line #03 fits its row.

## Checks
- **Arabic check:** `check_arabic_pdf.py --expect "اطلبني إعمار"` PASS.
- **PDF text search, all 0:**
  - «الملف التعريفي» (no visible page; PDF title only)
  - Emaar, «شهد», Shahd, "single company", «في عقد مع شركة واحدة»
  - «اطليني», CONSANY, Suzuki, ISUZU, DZIRE
  - «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp
  - draft, Illustrative, «توضيحية», «مقدمة من العميل»
  - Photo credits, CC BY, Flickr, Wikimedia, «حقوق الصور»
- **New Chamber strings:** present on p15 and p13 (twice in the HTML).
- **Contents and bookmarks:** contents 03/04/06/13/14/17/19 match the folios, with no mismatches. Bookmarks: 2, 3, 4, 6, 13, 14, 17, 19.
- **No image on two pages:** confirmed by the build. Removed images: Doha, San Diego and the steel erector, each 0 occurrences in the HTML.
- **Viewed:** the contact sheets; pp1, 8, 13 and 15 at full preview size; the replaced logos at 300 dpi.
