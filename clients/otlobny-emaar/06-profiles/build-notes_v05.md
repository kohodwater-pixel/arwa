# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v05

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-14  **Author:** corporate-designer
**Status:** DRAFT v05, the answer to `review_v04_r1.md` and the Creative Director rulings of 2026-11-14. Not approved by the client. Every v01–v04 file is untouched.

## 1. Files

| File | What it is |
|---|---|
| `otlobny-emaar_company-profile_screen_ar-en_v05.pdf` | 20 pages, 297 × 210 mm, screen PDF (sRGB), 11.3 MB; title, `/Lang ar`, R2L, 9 bookmarks |
| `otlobny-emaar_company-profile_screen_ar-en_v05.html` | Editable source (assets linked from `assets/`) |
| `_work/build_profile_v05.py` | Generator: retouches, grade recipe, crops (`assets/derived/v05_*.jpg`, 32 files, all used), HTML |
| `_work/finish_pdf_v05.py` | Metadata and bookmarks |
| `_work/contact_v05.py`, `_work/contact_v05_part1.png`, `_part2.png` | Contact sheets |
| `_work/preview_v05/` | 110 dpi previews of the final PDF |
| `_work/build_v05.log`, `_work/check_v05.log` | Image and logo log (crop, size, ppi; repeat check), Arabic check |

## 2. Page map (20)

1 cover · 2 contents · 3 about · 4 vision + mission · 5 goals · 6 services overview · 7–12 services (one master) · 13 logistics in pictures (pictorial only) · 14 why us · 15 work 01 bus shelters · 16 works 02 Madinah Chamber + 03 Dar Al Taqwa · 17–18 partners (16 + 16) · 19 contact · 20 back cover with photo credits.

Numbering (one scheme, same format in both languages, in kickers, contents and footers): 01 About Us · 02 Vision, Mission and Goals · 03 Our Services · 04 Why Us · 05 Our Work · 06 Partners in Success · 07 Contact.

## 3. Service master (pp7–12), built for tile-size images

A diamond cluster on the image half, the same 45° lattice as the cover: diamonds of 50 mm side with 3.6 mm gutters. Pages with a sharp large photo (contracting: steel erector, 2048 px; maintenance: HVAC gauges, 3600 px) use one double diamond plus two small ones. Pages with only ~1024 px images (landscaping, cleaning, manpower, logistics) use two to four small photo diamonds combined with brand-colour diamonds (navy gradient, green, blue, pale tint). Every small diamond is about 71 mm across, so every 1024 px image sits at 244–276 ppi. The cluster alternates left and right. The text half is a 117 mm column: kicker, Arabic title, English title, green rule, intro paragraphs in two columns, and then the bilingual list.

**M2 — lists:** each item is one CSS grid row (English cell left, Arabic cell right). The row height is set by the taller cell and one rule runs across both columns, so the rules cannot drift.

## 4. Images: page, source, effective ppi (no source on two pages; checked in code — "sources on more than one page: none")

| Page | Derived file | Source | ppi | Grade |
|---|---|---|---|---|
| 1 | v05_p01_hero_glass-facade | cover-hero_blue-glass-facade (CC0) | 315 | recipe |
| 1 | v05_p01_t_tower | contracting_tower-construction-with-palms | 281 | recipe |
| 1 | v05_p01_t_rope-access | cleaning_rope-access-blue-glass-tower | 284 | recipe |
| 1 | v05_p01_t_palm-park | landscaping_palm-park-riyadh-museum | 319 | recipe |
| 1 | v05_p01_t_technician | maintenance_technician-headlamp-tools | 284 | recipe |
| 3 | v05_p03_madinah-plaza | opener_madinah-haram-plaza-umbrellas | 327 | recipe |
| 6 | v05_p06_madinah-panorama | opener_madinah-haram-panorama (cropped above the "TAIBA FRONT HOTEL" sign and left of the toilets sign) | 227 | recipe |
| 7 | v05_p07_contracting_hero / _12 / _21 | steel erector / concrete screeding crew / surveyor | 266 / 245 / 246 | recipe |
| 8 | v05_p08_landscaping_00 / _11 | date-palm walkway Doha / palms dry planting | 276 / 276 | recipe |
| 9 | v05_p09_maintenance_hero / _12 / _21 | HVAC gauges / rooftop AC units / distribution board | 333 / 245 / 460 | recipe |
| 10 | v05_p10_cleaning_00 / _11 | rope-access window cleaner / mop and trolley | 244 / 245 | recipe |
| 11 | v05_p11_manpower_00 / _10 / _01 | Gulf site workforce / waiter pouring tea / catering table (banner cropped) | 276 / 245 / 245 | recipe (warm −5 on tea and catering) |
| 11 | v05_p11_manpower_11 | client mockup: cleaning team (illustrative) | 368 | none (client image) |
| 12 | v05_p12_logistics_00 | warehouse racking aisle | 244 | recipe |
| 12 | v05_p12_logistics_11 | client mockup: car and scooter (illustrative) | 368 | none |
| 13 | truck-rear34 / truck-side / truck-front34 / truck-front / truck-rear / rider | client mockups (illustrative) | 184 / 138 / 184 / 152 / 151 / 276 | none |
| 15 | v05_p15_bus-shelter | client photo, cropped to x 400–950 px (litter out) | 133 | recipe |
| 16 | v05_p16_chamber | client rendering | 195 | recipe |
| 16 | v05_p16_dar-al-taqwa_entrance | client photo (335 × 597 px), 50 mm wide | 170 | recipe |

Not used (DEMOTED list): rebar worker, palm promenade, gardener, date palm (Commons), floor scrubbers, white box truck, forklift, site at blue hour. The p2 image from v04 is gone: p2 is type and pattern only.

**Grade recipe (README round 3), applied identically in code to every stock and client works photo:** saturation −20; curves 64→56 and 192→200 with black output 10; navy #1F3162 soft light at 15 %; temperature −5 on the two warm interiors. The client's AI mockups are not graded, so their brand colours stay as supplied (CD ruling m9).

**Retouches** (in memory; no source written): the gauge-label maker name (as in v04); "COAST" on the technician's head strap (filled with the strap colour); the banner slogan in the car/scooter mockup (as in v04). Rooftop AC image: the red lettering on the parapet is cropped out, not retouched (crop centre 0.33).

## 5. Checks

- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**. 20 pages at 297 × 210 mm. Fonts: Tajawal 400/500/700/800 and IBM Plex Sans 400/500/600/700, no fallback. 4,494 Arabic characters, no presentation forms.
- PDF text search, all 0: «شهد», "Shahd", «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp/واتساب, «خدمات الصيانة والنظافة لفندق», TAIBA, THERMO, COAST, and the demoted authors (Torquay, Jamain, nenad53, Z22, Lav Ulv, seier, Srianix).
- Diacritics: harakat 0 (all stripped in the build). The only mark kept is tanwin fath in «ـاً» (7 instances), as written in the outline. Numerals: Western only, Arabic-Indic 0.
- Contact strings match `brand-context.md`.
- Contrast (WCAG ratio, computed from the CSS colours):
  - p19 labels, white 82 % on flat navy: 8.96.
  - p19 values: 12.55.
  - p20 credits, grey #525456 on white: 7.61; bold, navy: 12.55. English 7 pt, Arabic 8.5 pt.
  - Footers, #5F6573: 5.84 on white, 5.50 on the tint.
  - Captions on the tint panel: 7.17.
  - Green kicker on navy: 5.83.
- Every page was viewed at full preview size during iteration, and all 20 again on the final contact sheets.

## 6. Open points

1. Dar Al Taqwa: no scope is stated (C1). The scope and a larger photograph are needed from the client.
2. The "one company / in a single contract" line (m12) is kept pending the client.
3. No Gulf-credible large hero exists for landscaping, cleaning, manpower or logistics. The master is built so this does not show, but the client's own photographs would still be stronger.
4. Faint partner logos: they are at their resolution floor, and only official files will fix them. The End's file is still cut at its edge.
5. No native Arabic proofread. Screen PDF only. Not tagged for accessibility. Not opened in a second viewer.
