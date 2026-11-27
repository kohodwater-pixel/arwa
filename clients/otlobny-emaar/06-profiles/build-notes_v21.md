# Build notes: «اطلبني اعمار» / OTLOBNY Emar company profile v21

**Date:** 2026-11-27
**Author:** corporate-designer
**Status:** v21 = v20 with the company name corrected to the registered name (client approval 2026-11-27, brand-context.md decision log). Not yet reviewed by the quality-reviewer.

v20 is untouched. 20 pages, 297 × 210 mm. No redesign, no other copy, image or layout change.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v21.html` and `.pdf`
- `_work/build_profile_v21.py` (run `_work/v21/fleet_v21.py` and `_work/v21/garments_v21.py` first), `_work/finish_pdf_v21.py`, `_work/contact_v21.py`
- `_work/build_v21.log`, `_work/check_v21.log`, `_work/preview_v21/` (20 page PNGs), `_work/contact_v21_part1.png`, `_work/contact_v21_part2.png`
- `_work/v21/`: the two composite scripts, v20/v21 side-by-side crops (`compare_*`), 300 dpi checks (`check300_*`, `check_cleaner.png`)
- `assets/logo/otlobny-emaar_logo_lockup-{colour,reversed,white,navy}_ar-en_v03.svg`: copied from `04-identity/02-logo/` (byte-identical; the v02 copies are kept)
- `assets/derived/v21_*`: 21 page images written by the build (20 are byte-identical to their `v20_*` counterparts; `v21_p01_small_cleaner.jpg` differs), plus `v21_logistics_fleet-client.jpg` and `v21_client_triptych-cleaner.png`

Build route, same as v20: build script → `node scripts/html2pdf.cjs … --size 297x210mm` → `finish_pdf_v21.py` (title, language, R2L, bookmarks) → `scripts/check_arabic_pdf.py`.

## 1. Strings changed

Only one visible string changes in running text: «اطلبني إعمار» → «اطلبني اعمار» (31 places in the PDF text). English running text "OTLOBNY Emar" is unchanged.

| Page | Where | Before → after |
|---|---|---|
| pp2–19 (18 pages) | Arabic footer, «<section> · اطلبني إعمار» | → «<section> · اطلبني اعمار» |
| p3 | About, Arabic body, first words | «اطلبني إعمار» شركة ذات مسؤولية محدودة… → «اطلبني اعمار» شركة ذات مسؤولية محدودة… |
| p4 | Vision lead; Mission body (Arabic) | «…في «اطلبني إعمار»…» → «…في «اطلبني اعمار»…» (2 places) |
| pp7–12 | Service intro, Arabic (one per page) | «تتولى / تنفذ / تقدم / توفر «اطلبني إعمار»…» → «… «اطلبني اعمار»…» (6 places) |
| p13 | Page title, Arabic | لماذا «اطلبني إعمار» → لماذا «اطلبني اعمار» |
| pp14–16 | Work description, Arabic (one per page) | «صممت / تقدم / قدمت «اطلبني إعمار»…» → «… «اطلبني اعمار»…» (3 places) |
| HTML `<title>` and PDF title | Document title | «اطلبني إعمار — الملف التعريفي \| OTLOBNY Emar — Company Profile» → «اطلبني اعمار — …» |
| pp1, 2, 19, 20 | `alt` text of the lockup image | «اطلبني — شركة اطلبني إعمار المحدودة — OTLOBNY EMAR COMPANY LTD.» → «اطلبني — شركة اطلبني اعمار — OTLOBNY EMAR COMPANY» |

Not changed, on purpose:
- p3 legal form: «شركة ذات مسؤولية محدودة» / "limited liability company" (body) and the fact row «الشكل القانوني: شركة ذات مسؤولية محدودة» / "Limited liability company". This is the legal form stated as a separate descriptor, not part of the name, as the ruling allows.
- «اطلبني» stays without hamza. No unified number, address or other new fact was added. p19 contact details are as in v20.

## 2. Lockups swapped (v02 → v03)

All four placements are by width with the top edge kept; only the box height grows (v03 viewBox 307.711 × 141.848 against 138.25).

| Page | Version | Left, top, width | Height v20 → v21 | Below the lockup |
|---|---|---|---|---|
| p1 cover | colour | 18, 22, 80 mm | 35.94 → 36.88 mm | Box ends at 58.9 mm; next element is "Company Profile" at about 170 mm. Nearest collage edge unchanged (lockup width unchanged). |
| p2 contents | reversed | 18, 162, 58 mm | 26.06 → 26.74 mm | Box ends at 188.7 mm; page edge at 210 mm (21.3 mm; X = 4.0 mm). The navy clear zone above is unchanged. |
| p19 contact | reversed | 116.5, 20, 64 mm | 28.75 → 29.50 mm | Box ends at 49.5 mm; contact block starts at 59 mm (9.5 mm; X = 4.4 mm). |
| p20 back cover | white | 98.5, 71.54, 100 mm | 44.93 → 46.10 mm | The top stays at 71.54 mm (v20 position), so the wordmark does not move. The otlobny.net · «المملكة العربية السعودية» line keeps its 10 mm gap under the lockup and therefore moves down 1.17 mm (126.46 → 127.63 mm). This is the only moved element in the book. |

Wordmark check, measured on the PDFs at 1200 dpi: the wordmark's top-left corner and width are the same in v20 and v21 on all four pages to within 0.02 mm. The wordmark did not shrink or move.

## 3. Lockups baked into images

Every image in the book was viewed at 150–400 dpi for a baked descriptor. Two carry the full lockup; both were legible at print size, so both were re-composited. None is accepted as-is.

| Page | Image | Lockup width on the page | Descriptor size on the page | Action |
|---|---|---|---|---|
| p12 | Fleet image, truck box side | 32.3 mm | Latin capitals 0.95 mm high, Arabic line 2.3 mm; clearly readable («إعمار المحدودة», "LTD." could be read in v20) | Re-composited: `_work/v21/fleet_v21.py` = the v10 script with the white lockup v03. New file `assets/derived/v21_logistics_fleet-client.jpg`. |
| p1 | Small diamond, window cleaner's back (under the 86% navy overlay) | 30.9 mm | Latin capitals 0.90 mm high; readable in v20 | Re-composited: `_work/v21/garments_v21.py` = the v13 script with the white lockup v03. New file `assets/derived/v21_client_triptych-cleaner.png`. |

Method and proof:
- Same method as before: paint-out of the AI mark from the surrounding surface, then the real SVG warped onto the surface (`cv2.getPerspectiveTransform`) and shaded by the surface light. Both start again from the client's untouched copies in `assets/mockups/`.
- Placed by width, top edge anchored (the truck quad is built from its top edge; the garment rectangle's centre is moved down by half the height difference along its own axis).
- Reproduction test: each script was first run with the v02 lockup (`REPRO=1`). Both outputs are pixel-identical to the existing `v10_logistics_fleet-client.jpg` and `v13_client_triptych-cleaner.png` (maximum difference 0). So the method reproduces the old images exactly, and the only variable in v21 is the lockup file.
- Difference v21 against the old image, in source pixels: fleet image, all differences inside x 3711–4208, y 504–784 (the lockup block; the upper rows are JPEG block rounding only, the wordmark is the same); cleaner image, all differences inside x 98–330, y 447–548 (the lockup block).
- Side-by-side crops: `_work/v21/compare_src_*`, `compare_p12_truck-box_*`, `compare_p01_cleaner_*`; 300 dpi: `_work/v21/check300_truck-box.png`, `check_cleaner.png`.

Other baked marks, unchanged because they are the wordmark alone with no descriptor: p12 cab front, cab door, car door, delivery box, scooter panel; p8 palm team (cap and garments); p11 cleaning team (chest marks). The engineers' vests from the same triptych (v13, lockup v02) are not in the book since v20 and were not rebuilt.

`python3 -m pip install scipy opencv-python-headless` was needed in this session: the two composite scripts use them and they are not installed by `scripts/setup.sh`.

## 4. Checks and results

1. **HTML strings (v21):** «إعمار» 0; «المحدودة» 0; "LTD" / "Ltd" / "ltd" 0; "Emaar" / "EMAAR" 0; `_v02` references 0.
   - Remaining "emaar" (4): only inside the four lockup file paths (`assets/logo/otlobny-emaar_logo_lockup-…_v03.svg`); file names keep the slug.
   - Remaining «محدودة» (2): the legal form «شركة ذات مسؤولية محدودة» on p3 (body and fact row), a separate descriptor, not part of the name.
   - New strings: «اطلبني اعمار» 36 (31 visible, 4 alt texts, 1 title); «شركة اطلبني اعمار» 4 and "OTLOBNY EMAR COMPANY" 4 (alt texts); "OTLOBNY Emar" 33, as in v20.
2. **`check_arabic_pdf.py --expect "اطلبني اعمار" --expect "شركة ذات مسؤولية محدودة"`: PASS.** 20 pages, 297 × 210 mm. Fonts: IBMPlexSans (Regular, Medium, SemiBold, Bold) and Tajawal (Regular, Medium, Bold, ExtraBold), all embedded subsets; no fallback font. 4,329 Arabic characters, 0 presentation forms (v20: the same count). Log: `_work/check_v21.log`.
3. **Page count and size:** 20 and 297 × 210 mm, as v20. Bookmarks 2, 3, 4, 6, 13, 14, 17, 19, as v20.
4. **PDF text:** «إعمار» 0 (v20: 31); «اطلبني اعمار» 31; «المحدودة», "LTD", "Emaar" 0; "OTLOBNY Emar" 13 and "OTLOBNY EMAR" 18 (footers in capitals), as v20. The lockup descriptor «شركة اطلبني اعمار» / "OTLOBNY EMAR COMPANY" is outlined artwork (paths), so it is not in the extracted text; it was checked by eye.
5. **Reflow:** every text line in the PDF has the same position and the same line content in v20 and v21 (line boxes compared to 0.1 pt on all 20 pages). The single exception is the intended 1.17 mm move of the p20 line. No line break changed, so no new widow or orphan.
6. **Page images, v20 against v21 at 150 dpi:**

   | Pages | What differs |
   |---|---|
   | p1 | Lockup (descriptor; hairline anti-alias pixels on the wordmark edge); the lockup on the cleaner's back |
   | p2 | Lockup descriptor; hamza in the footer |
   | p3–p11, p13–p18 | Only the hamza under the alef, at each place listed in section 1 (7 to 124 pixels per page) |
   | p12 | Hamza in the intro and the footer; truck-box descriptor |
   | p19 | Lockup descriptor; hamza in the footer |
   | p20 | Lockup descriptor; the line below it, 1.17 mm lower |

   All 20 pages differ, each only in the places intended. Nothing else changed.
7. **Visual check:** all 20 pages on the contact sheets; lockups on pp1, 2, 19, 20, the truck box and the cleaner's back as v20/v21 pairs at 200–400 dpi; the name in running text at 300 dpi (p3, p4, p12, p13, footers of p3 and p19: `_work/v21/check300_name-in-text_*.png`). Letters are connected and in order, «اعمار» has a plain alef, no lockup is clipped.

## 5. Noted, not changed (outside this task)

- **Truck box, space under the lockup (p12):** the descriptor's last line is 0.96 mm from the green wave on the page (v20: 1.08 mm). Both are under the lockup's clear-space unit (6.9% of 32.3 mm = 2.2 mm). The shortfall exists since v09; v03 makes it 0.12 mm tighter because the top edge is anchored. Fix, if wanted: move the lockup up about 1.5 mm on the panel, or reduce it; either changes the wordmark's position, which this task rules out.
- **p3 legal form** («شركة ذات مسؤولية محدودة») is kept from v20. It is not checked against the registration certificate, which is not on file.
- **p19 address and email** are as in v20 (Prince Abdulmajeed bin Abdulaziz Road; info@otlobny.co). brand-context.md now records a different National Address; the task says not to add it.
- `content-outline.md` (25 places) and `content-gaps.md` (3 places) still carry «إعمار» / «المحدودة». brand-context.md section 1 "Brand name" row still reads "OTLOBNY Emaar / اطلبني إعمار".
- The engineers' triptych panel (`v13_client_triptych-engineers.png`, not used in the book) still carries lockup v02.
- Still open from earlier versions: native Arabic proofread, check in a second PDF viewer, accessibility tagging.
