# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v03

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-14  **Author:** corporate-designer
**Status:** DRAFT v03 for the Creative Director and the quality-reviewer. Not approved by the client. All v01/v02 files untouched.

## 1. Files

| File | What it is |
|---|---|
| `otlobny-emaar_company-profile_screen_ar-en_v03.pdf` | 20 pages, 297 × 210 mm, screen PDF (sRGB), 6.9 MB |
| `otlobny-emaar_company-profile_screen_ar-en_v03.html` | Editable source (assets linked from `assets/`) |
| `_work/build_profile_v03.py` | Generator = v02 code unchanged + a "v03" section at the end; writes `assets/derived/v03_*.jpg` |
| `_work/retouch_mockups_v03.py` | New retouch (imports v02's patch list, adds/adjusts three); writes `assets/derived/mockup_*_retouched_v03.png` (+5 truck crops) and 4× before/after sheets in `_work/retouch_v03/` |
| `_work/prepare_partners_v03.py` | Prepares the three new partner logos; log and check sheets in `_work/partners_v03/` |
| `_work/finish_pdf_v03.py` | Title, `/Lang ar`, R2L, bookmarks |
| `_work/preview_v03/`, `_work/contact_v03_part1-2.png`, `_work/contact_v03_full_a-c.png` | 110 dpi previews of the final export; contact sheets; full-size stacks of pp1/10, 12/13, 20/7 |

## 2. Changes from v02

1. **Partners = 30, 15 + 15.** Added `new-10_shawarma-laila`, `new-11_loomi`, `new-12_the-end` (in `assets/partners-transparent/`, recorded in `assets/partners/README.md`). Order: existing-01…18, new-01…09, new-10…12, right to left, row by row. Both pages: 5 columns × 3 rows, row centres y 77.25 / 119.75 / 162.25 mm, hairlines at y 56 / 98.5 / 141 / 183.5, title in the normal title zone, ownership line under the p19 grid at y 186.5. p19 changed from 4 to 5 columns.
2. **New logos prepared:** cropped to the artwork with an even 8 % transparent margin; The End downsampled from 3000 to 1400 px artwork width (premultiplied Lanczos, no sharpening). **Loomi:** at 4× on white the outer edge carried a 1–2 px opaque blue-grey fringe (alpha in the supplied file is hard 0/255, so there was no semi-transparent fringe to threshold). Only edge pixels touching transparency and coloured blue-grey (not the logo yellow) were removed — 9,380 px over 3 passes; the 6,808 remaining off-colour boundary pixels were set to 50 % alpha, colour unchanged. Letterforms, blue counters and inner edges untouched (sheet: `_work/partners_v03/new-11_loomi_zoom4x_on-white.png`). **The End:** the client's file is cut at its right and bottom edges (the «D» and check band touch the canvas) — not redrawn; complete file requested.
3. **Optical sizing.** Rule: logo box 38 × 24 mm, about 560 mm² of mark, corrected for shape and weight. New: Laila ×1.15 (wide, light outline) → 34.6 × 18.6 mm; Loomi ×0.80 (heavy wide wordmark) → 31.5 × 14.3; The End ×1.20 (fine BURGERS / FRIES detail) → 31.0 × 21.7. The six faint marks were taken to the floor or the cell limit (box widened to 46 × 25 mm for them): Dar Al Taqwa 42 → 46 mm wide (cell limit; still only 7.1 mm tall — the asset is a thin pale lockup), Al Madinah Harmony 38 → 44 mm, Development Authority 30.0 → 30.9 mm (100 ppi effective floor), Dallah Taibah 24.2 → 24.7 mm (floor / 25 mm height), dome mark 14.7 → 16.0 mm (25 mm tall, 102 ppi), Manarat Taba 19.9 → 21.6 mm (104 ppi). No logo below its floor. Other existing and new-01…09 sizes unchanged from v02.
4. **Optical centring:** every logo is centred on the point halfway between its bounding-box centre and its ink centroid (shift limited to 12 % of its size; largest shifts 2.2 mm, Madinah Chamber, and 2.0 mm, Tiny House).
5. **Mockup retouch v03** (section 5).
6. **pp7 and 11 rebalanced:** photo bands 100 → 116 mm (General Contracting, Manpower Supply); text block starts 16 mm lower; the bottom gap above the footer is now about 9 mm on p7 and similar on p11. Crops: electrical-panel 1240 × 484 px (106 ppi, as before), waiter 980 × 512 px (112 ppi).
7. `content-outline.md` and `content-gaps.md` updated minimally (status block at the top + website rows / closed rows); previous text in `_archive/`.

Unchanged: client's four images used large, logo alone (nothing under it), image-led pages, nothing from the website, no WhatsApp row, no invented facts.

## 3. Partner logos — sizes and effective resolution (as built)

| # | Page | File | Mark size (mm) | Area (mm²) | Effective ppi | Floor tier | Optical shift x / y (mm) |
|---|---|---|---|---|---|---|---|
| 1 | p18 | existing-01_madinah-award-foundation | 16.0 × 25.0 | 400 | 102 | B (≥100) | -1.1 / +1.8 |
| 2 | p18 | existing-02_al-madinah-region-development-authority | 30.9 × 19.6 | 604 | 100 | B (≥100) | -0.1 / +0.8 |
| 3 | p18 | existing-03_al-maqar | 29.5 × 19.1 | 564 | 110 | B (≥100) | +0.1 / -0.2 |
| 4 | p18 | existing-04_we-ar-spa | 28.0 × 22.8 | 639 | 777 | — | -0.1 / -0.9 |
| 5 | p18 | existing-05_mawaddah | 33.0 × 19.7 | 651 | 122 | B (≥100) | -0.1 / +0.3 |
| 6 | p18 | existing-06_imagine-more | 36.0 × 17.4 | 628 | 718 | — | +0.7 / +0.3 |
| 7 | p18 | existing-07_hsh | 32.0 × 16.6 | 532 | 83 | C (≥80) | -0.1 / +0.0 |
| 8 | p18 | existing-08_taibah-cooperative | 20.3 × 18.3 | 371 | 100 | B (≥100) | -0.0 / -0.1 |
| 9 | p18 | existing-09_dar-al-taqwa-hotel | 46.0 × 7.1 | 326 | 161 | B (≥100) | +0.2 / -0.1 |
| 10 | p18 | existing-10_dallah-taibah-hotel | 24.7 × 25.0 | 619 | 101 | B (≥100) | +0.0 / -0.3 |
| 11 | p18 | existing-11_al-madinah-harmony | 44.0 × 20.6 | 906 | 107 | B (≥100) | +0.8 / -0.5 |
| 12 | p18 | existing-12_tiny-house | 34.0 × 14.9 | 507 | 545 | — | -2.0 / +0.7 |
| 13 | p18 | existing-13_platinum | 31.0 × 17.9 | 554 | 788 | — | -0.1 / -0.8 |
| 14 | p18 | existing-14_madinah-chamber | 38.0 × 15.3 | 582 | 1271 | — | +2.2 / +0.2 |
| 15 | p18 | existing-15_manarat-taba-hotel | 21.6 × 25.0 | 539 | 104 | B (≥100) | -0.1 / -0.5 |
| 16 | p19 | existing-16_hippo | 16.6 × 24.0 | 398 | 781 | — | -0.0 / +0.3 |
| 17 | p19 | existing-17_taza | 28.0 × 19.7 | 553 | 130 | B (≥100) | -0.0 / +0.6 |
| 18 | p19 | existing-18_arabic-calligraphic-mark | 30.0 × 17.0 | 511 | 94 | C (≥80) | +0.1 / +1.2 |
| 19 | p19 | new-01_manazil-al-mukhtara | 30.1 × 23.9 | 720 | 878 | — | +0.5 / -1.0 |
| 20 | p19 | new-02_novotel | 38.0 × 14.8 | 564 | 837 | — | -0.4 / +0.5 |
| 21 | p19 | new-03_keeta | 31.0 × 16.5 | 512 | 610 | — | -0.4 / -0.1 |
| 22 | p19 | new-04_jahez | 28.0 × 19.5 | 546 | 725 | — | -0.2 / +0.1 |
| 23 | p19 | new-05_medina-dates-festival | 17.4 × 24.0 | 417 | 1108 | — | -0.6 / -0.4 |
| 24 | p19 | new-06_hungerstation | 32.0 × 16.4 | 525 | 928 | — | -0.0 / -0.0 |
| 25 | p19 | new-07_rotana | 38.0 × 13.1 | 496 | 765 | — | +0.1 / +0.9 |
| 26 | p19 | new-08_chop-and-co | 28.0 × 18.1 | 508 | 1053 | — | +1.1 / -0.3 |
| 27 | p19 | new-09_zero | 38.0 × 13.3 | 504 | 676 | — | -0.3 / -0.3 |
| 28 | p19 | new-10_shawarma-laila | 34.6 × 18.6 | 645 | 1046 | — | -0.1 / +0.4 |
| 29 | p19 | new-11_loomi | 31.5 × 14.3 | 449 | 748 | — | -0.3 / -0.5 |
| 30 | p19 | new-12_the-end | 31.0 × 21.7 | 674 | 1147 | — | +1.1 / +0.5 |

Counted on the final previews: 15 on p18 + 15 on p19 = 30, no duplicates, none clipped (viewed at full size).

## 4. Images
As v02 except p7 and p11 (above) and that all mockup-derived JPEGs come from the v03 retouches. Full log: `_work/build_v03.log`.

## 5. Mockup retouch v03

**Method.** v02 refilled only the old stroke pixels by diffusion, which carried stroke fringes inward and left mottled patches (car door) and a smudge (facade). v03 rebuilds each whole patch area (grown 2 px; 3 px on the raised facade letters; 1 px on the car door so the sill crease is spared): (1) the wordmark is detected and protected (blue/green saturated pixels; on the facade also the dark-blue letter extrusion; on the cart the large white shapes); (2) the hole is filled with a smooth membrane (Laplace) surface whose boundary values are a masked Gaussian average of clean surrounding panel only (robust: grille edges, logo halos and remnants excluded; disabled on the glossy helmet and scooter), initialised from a quadratic fit; (3) sharp vertical structure (door gaps, hinges, panel seams) is carried through, constant per column, only where the panel above and below agree; (4) fine grain matched to the surrounding noise (robust MAD level; reduced on the glossy scooter) is added; 2 px feather. Isolated remnant specks (the white dots left on the truck box sides in v02, etc.) inside the patch areas (+6 px) on even surfaces were filled from the local median.

**Changes to the patch list:** added the facade shadow line of the old Latin letters just below the v02 area (quad 236,238 / 318,244 / 318,253 / 236,247); truck view 4 cab-front area ends at y 848 (clear of the grille); **cleaning cart narrowed to 1406,660–1468,670** — v02's area (1384,656–1470,671) had also removed the lower bowl and dots of the white «اطلبني» on the cart (found at 6×; this is in v02 as sent to the client); v03 restores the wordmark exactly as supplied.

**Verification.** Differencing each result against the original: pixels changed outside the patch masks (+6 px) = **0** in all four images; wordmark pixels changed outside the masks = 0 (trucks: 25 bluish-classified pixels inside the masks changed — anti-aliased edges of the old text, not the wordmark). 4× sheets for all four images viewed: `_work/retouch_v03/zoom_mockup_*.png`. No trace of the old descriptor lines remains in any mockup at 4× or on the pages.

Residual (minor, visible only at 4×): on the two rear-door patches (truck views 2 and 5) the carried door-gap lines are slightly uneven in tone where they cross the patch; the view-4 cab front patch has a faint lighter haze at its left end. Neither is visible at page size (viewed on pp12–13 at full preview size).

## 6. Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**, 20 pages 297 × 210 mm; fonts Tajawal Regular/Medium/Bold/ExtraBold, IBM Plex Sans Regular/Medium/SemiBold/Bold; no fallback; 4,146 Arabic characters, no presentation forms; webfonts_failed: none.
- Viewed: pp1, 7, 10, 12, 13, 18, 19, 20 at full preview size (1287 px wide); all 20 in contact sheets at about 560 px. Arabic connected and right to left; titles readable over every image; nothing clipped; no descriptor remnants.
- pypdf prints "Object count 289 exceeds defined trailer size 245" when finishing the PDF (also seen in v02); the file opens and checks normally.

## 7. Open points
1. Name and lockup (cover, back cover) still a proposal awaiting the client.
2. Banner slogan «خدمتك بجودة تهمنا» in the cover image: not approved copy; client to confirm or have removed.
3. The End: client's file is cut at its right and bottom edges — complete file requested. Loomi: fringe cleaned by us; an official file would be better.
4. Low-resolution old logos (Dar Al Taqwa, Development Authority, Dallah Taibah, dome mark, Manarat Taba, Al Madinah Harmony, HSH, calligraphic mark) are at the agreed floor and still look smaller/fainter than the new vector-quality marks; only official files will fix this. Dar Al Taqwa is the weakest (thin pale lockup, 7 mm tall).
5. v02 (already with the client) shows the cleaning-cart wordmark without its lower part; v03 corrects it — worth mentioning when v03 is sent.
6. Phone, email, address not reconfirmed; photo licences unknown; partner-logo permissions are the client's responsibility.
7. No native Arabic proofread yet; PDF not tagged; screen PDF only (no print version).
