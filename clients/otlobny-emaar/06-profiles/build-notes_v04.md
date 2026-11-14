# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v04

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-14  **Author:** corporate-designer
**Status:** DRAFT v04 for the Creative Director and the quality-reviewer. A new design, not a patch of v03. Not approved by the client. No v01–v03 file was changed.

## 1. Files

| File | What it is |
|---|---|
| `otlobny-emaar_company-profile_screen_ar-en_v04.pdf` | 20 pages, 297 × 210 mm, screen PDF (sRGB), about 12.9 MB, title / `/Lang ar` / R2L / 9 bookmarks |
| `otlobny-emaar_company-profile_screen_ar-en_v04.html` | Editable source; assets linked from `assets/` (fonts, logo, derived photos, partner logos) |
| `_work/build_profile_v04.py` | Generator: retouches, brand grade, crops (writes `assets/derived/v04_*.jpg`, 39 files) and the HTML |
| `_work/finish_pdf_v04.py` | Metadata, language, reading direction, bookmarks |
| `_work/contact_v04.py` | Contact sheets `_work/contact_v04_part1.png` (pp1–10) and `_part2.png` (pp11–20) |
| `_work/preview_v04/` | 110 dpi previews of the final PDF (from `check_arabic_pdf.py`) |
| `_work/build_v04.log`, `_work/check_v04.log` | Image log (crop, size, effective ppi; logo sizes) and the Arabic check output |
| `assets/photos/dar-al-taqwa-hotel-entrance.jpg` | Byte-identical copy of the client's upload (original untouched in `_originals/`) |
| `assets/logo/otlobny-emaar_logo_wordmark-{colour,reversed}_ar_v01.svg` | Copies of the approved-as-captured wordmarks from `04-identity/02-logo/` (logo alone, nothing under it) |

Also updated (previous text archived in `_archive/*_before-v04_2026-11-14.md`): a v04 status block at the top of `content-outline.md` and `content-gaps.md`; one line added to `assets/photos/README.md`.

## 2. Design idea

**"One large image, several small" as the system, not only the cover.** The client asked for the cover to work like the original (one big image, small images around it). v04 takes that structure and makes it the grid of the whole book:

- **Cover:** a diamond lattice. One large rounded diamond (steel frame under construction, a direct reading of «إعمار») and four small diamonds on the same 45° lattice with a constant 3.6 mm gutter (maintenance, landscaping, cleaning, logistics), two brand-colour diamonds and one small green accent in the notch. Corner radius 12 % of the side, the same rounding as the wordmark's diamond device. Logo (colour wordmark, alone) top left; Arabic title block right-aligned, English block left-aligned below, separated from the logo by more than 60 mm of white.
- **Service master (pp7–12):** a photo panel of one large square and two small tiles (3.6 mm white gutters, bleeding off three edges), alternating left and right for rhythm; a 117 mm text area on the other side.
- **Works master (pp15–17):** a light-tint panel on the image side with the photograph, caption and scope chips centred in it; on p17 the tint becomes a narrow band behind a small portrait photo so the small image reads as intentional.
- **Typographic pages** (contents, goals on navy, why on tint, partners, contact on navy) give breathing space between photographic pages.

**Bilingual structure, one rule kept throughout:** in every text area English sits on the left, Arabic on the right, in separate aligned blocks. Full-width pages put the two titles on one baseline; half-page text areas stack the Arabic title (right) above the English title (left) because the long Arabic service names do not fit beside their English pair in 117 mm. Arabic is the primary language: larger (titles 31 pt vs 21 pt, body 11 pt vs 9 pt, lead 12–13 pt vs 10–10.5 pt), never tracked, line height 1.55–1.8, Arabic punctuation, Western numerals as recorded in `brand-context.md`.

**Grid and type scale:** margins 18 mm left/right; kicker at 20 mm; footer at 197 mm (section name in each language, folio beside the Arabic). Type: Tajawal 400/500/700/800, IBM Plex Sans 400/500/600/700 (static files from `assets/fonts/`).

## 3. Photography

- **One brand grade for every photograph** (`grade()` in the script): 18 % desaturation, shadows drawn towards brand navy #1F3162, highlights towards the light tint, a whisper of cool in the mid-tones, slight contrast. Strength 1.15 on stock; 0.8 on the Madinah images; 0.55–0.7 on the client's mockups and works photos (so their brand colours and the works stay truthful); none on the studio cut-out of the rider.
- **Retouches (done on copies in memory; no source file written):** white box truck — Danish number plate and the operator's name on the sun visor replaced by local colour; rebar worker — white maker logo on the cap filled with the cap colour; HVAC gauges — maker name and logo on the blue manifold label removed (lettering only; label shape and shading kept); car/scooter mockup — the banner slogan «خدمتك بجودة تهمنا» (unapproved copy) filled with the banner navy, logo on the banner kept; catering image cropped to remove the red event banner; floor-scrubber image cropped to its right 60 % (no "T5" mark); forklift badge checked: not legible, no retouch.
- **Resolution (effective ppi at placed size, screen):** large frames 197–433 ppi (cover hero 202, about 327, contracting hero 398, maintenance 401, cleaning 307, manpower/logistics heroes = client mockups 197); every 1024 px Flickr file is used only as a tile ≤ 72 mm (≥ 203 ppi) or a cover diamond (≥ 283 ppi). Lowest: truck side view 120 ppi and truck front/rear 161 ppi (client's own crops, 97 mm wide), Madinah Chamber 139 ppi (client file 644 px, 118 mm), bus shelter 204 ppi, Dar Al Taqwa entrance 213 ppi (40 mm wide). Full log: `_work/build_v04.log`.
- **Image map:** cover — steel erector (hero), HVAC, palm promenade, mop and trolley, warehouse aisle · p2 glass facade · p3 Madinah plaza · p4 Madinah panorama (cropped to exclude a toilet sign at the right) · p6 the six service heroes, cropped differently · p7 rebar worker, surveyor, distribution board · p8 date palm, palm promenade, gardener · p9 HVAC wide, HVAC detail, building at blue hour · p10 floor scrubber, mop and trolley, rope-access window cleaner · p11 client's team image, waiter pouring tea, catering table · p12 client's car/scooter image, box truck, forklift · p13 client's three truck views and delivery rider · p15 bus shelter (client) · p16 Madinah Chamber image (client) · p17 Dar Al Taqwa entrance (client).
- **Credits (p20):** generated from the images actually used: 15 attributed photos (CC BY 2.0, CC BY-SA 2.0/3.0/4.0, CC BY 3.0 PL), all marked "modified", plus the four CC0 / public-domain files named as not requiring attribution. Arabic note: service photographs are illustrative; works, vehicle and team images are the client's.

## 4. Partners (pp18–19)

32 logos, 16 + 16, 4 × 4 cells of 65.3 × 33 mm, right to left and row by row: existing-01…16 on p18; existing-17, 18, new-01…14 on p19 (new-13 Le Méridien from the client's SVG, black wordmark; new-14 Al Esra Cabin). Transparent files on white, hairline grid. Sizing: v03 optical widths × 0.86, height cap 19.5 mm, ppi floors kept (tier B 100, tier C 80); optical centring between bounding-box centre and ink centroid. Dar Al Taqwa and Al Madinah Harmony widened (still above floor). Nothing from `_originals/partner-logos_2026-11-13` used. Line «جميع الشعارات ملك لأصحابها.» / "All logos are the property of their respective owners." under the p19 grid.

## 5. Checks run

- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS** — 20 pages 297 × 210 mm; fonts Tajawal Regular/Medium/Bold/ExtraBold and IBM Plex Sans Regular/Medium/SemiBold/Bold, no fallback; 4,057 Arabic characters, no presentation forms; webfonts failed: none.
- Text scan of the PDF: «شهد» 0, "Shahd" 0 (also 0 in the HTML); «الشركة المختارة» 0; «رائدة» 0; «أطلبني» 0; Arabic-Indic digits 0; "lorem"/"TBC" 0; «اطلبني إعمار» 34; contact strings as in brand-context (054 955 5514, info@otlobny.co, otlobny.net, CR 4650245200).
- Every page viewed at full preview size (1287 px wide) during iteration and again on the final contact sheets. Fixed during iteration: cover title wrapping into the English block; service titles wrapping and colliding (moved to stacked titles, wider text area); p17 title over the photo; p4 toilet sign; soft bus-shelter detail tile (removed); legible maker name on the gauge label; rider's grey box; nested list styles on p13; footer grey raised to #5F6573 for AA contrast.
- Letter-spacing: only on English labels; every Arabic class has letter-spacing 0.
- pypdf prints "Object count … exceeds defined trailer size" when finishing (seen in v02/v03 too); the file opens and checks normally.

## 6. Open points / honest assessment

1. **Dar Al Taqwa scope is an assumption** (maintenance and cleaning, same pattern as the hotel it replaces) — to confirm with the client.
2. The p17 photo is small by necessity (335 × 597 px); the page is typography-led and works, but a larger original from the client would make it stronger. The room photo was not used (rights).
3. Weakest pages in my judgement: **p17** (much white space, by design) and **p8** (the only sharp large landscaping image, a date palm under a flat sky, is the dullest hero in the book). p13 relies on the client's AI-generated truck images, which remain illustrative.
4. Service photographs are open-licence stock, not the company's work; captions say so on the credits page only, not under each image. If the CD wants per-image «صورة توضيحية» labels, they can be added to the service master.
5. Faint/low-resolution partner logos (Al Madinah Harmony, Dar Al Taqwa, the dome mark, Dallah Taibah, HSH, the calligraphic mark) still read lighter than the vector-quality marks; only official files fix this. The End file is still cut at its edge (client file).
6. Name and lockup remain proposals; the logo is used alone throughout (cover colour wordmark, p2 white wordmark, p20 reversed wordmark).
7. No native Arabic proofread yet; screen PDF only (no print/CMYK version); PDF not tagged for accessibility.
