# Build notes — «اطلبني إعمار» / OTLOBNY Emar company profile, draft v10

**Date:** 2026-11-14 · **Author:** corporate-designer · **Status:** DRAFT v10, built from the three expert-panel reviews of v09 (quality r6, art direction, content) and the CD's reconciling rulings (brand-context.md). Not approved by the client. v09 is untouched. **20 pages.**

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v10.pdf` and `.html`
- `_work/build_profile_v10.py` (run `_work/v10/fleet_v10.py` first), `_work/v10/fleet_v10.py`
- `_work/v10/check300_*.png` (300 dpi surface crops, including the repaired cab door)
- `_work/finish_pdf_v10.py`, `_work/contact_v10.py`, `_work/contact_v10_part1/2.png`, `_work/preview_v10/`, `_work/build_v10.log`, `_work/check_v10.log`
- `content-outline.md` and `content-gaps.md`: v10 blocks added; earlier text in `_archive/*_before-v10_2026-11-14.md`

## Must-fixes

| Item | Status | How / where |
|---|---|---|
| MF1 p2 clear zone | Done | Solid navy `#1F3162` box covering the lockup bounds plus X = 4.0 mm on every side (6.9% of 58 mm). The lattice no longer runs through the lockup. Only one filled green diamond is kept (the other two fills were removed). |
| MF2 cover images | Done | The four small tiles (racking aisle, rope-access tower, palm park, workforce) are in one navy→royal duotone (`#1F3162` → `#3758B0`, light top end). The hero (steel erector) stays in colour with the standard grade. |
| MF3 p16 on the works master | Done | One works master for pp14–16. Panel 142 mm wide (left on p14 and p16, mirrored on p15). Every photo starts at the same top line, 52 mm. Titles use the same `t1 tw` size on all three pages. Dar Al Taqwa photos: entrance 32.5 × 58 mm (261 ppi) and room 87 × 58 mm (224 ppi), centred in the panel. |
| MF4 p20 back cover | Done | Top 60% is the navy→royal gradient, with the reversed lockup centred at 90 mm and otlobny.net · «المدينة المنورة» in white. Bottom 40% is a white band with the complete credits (English 7 pt, Arabic 8 pt, grey #525456 = 7.61:1). I used 60% instead of the specified 62% so the credits fit at a legible size. |
| MF5 p13 on navy | Done | Same treatment as p5: white titles, green numerals, periwinkle secondary text, 25% white hairlines. **Flat navy** rather than a gradient: periwinkle on the gradient's light end measures 3.96:1 (fail), while flat navy gives 5.50:1. |
| M1 why #01 | Done | «… تقدمها شركة واحدة.» / "… all from one company." |
| M2 p20 Arabic rights note | Done | Exact string from the content review. |
| M3 p11 contract line | Done | «تكون العقود شهرية أو سنوية على نظام «أجير».» |
| M4 p6 card 02 | Done | «… وأجهزة الري.» |
| M5 p14 bus shelters | Done | Exact replacement string. |
| N14 why #03 | Done | #03 is now the Madinah Chamber proof point (exact text, §5). The contract-term line is folded into #02's description. |
| M7 record | Done | "WE DO THE BEST" recorded in content-gaps.md and content-outline.md (unsupported superlative, unconfirmed tagline, question for the client). |
| r6 m1 cover clear space | Done | Lockup reduced from 86 to 80 mm; X = 5.5 mm. Nearest collage edge is 9.6 mm from the lockup box (measured with sharp-corner geometry, which errs on the safe side). Lockup top is 22 mm from the trim and left is 18 mm. |
| r6 m3 cab door | Done | The mirror-bracket corner and the door handle are kept out of the patch. The patch is limited to the door panel; the speck is gone. 300 dpi crop: `_work/v10/check300_cab-door.png`. |
| r6 m2 | Ruling | The truck box keeps the full lockup. |
| r6 m4 | Done | Covered by MF1. |

## Art-direction extras

**Applied**
- **Cover:**
  - green diamond moved into the lattice notch between hero and tiles;
  - the repeated name line «اطلبني إعمار» / "OTLOBNY EMAR" removed above the title;
  - title moved up to two rows (22 mm) under the lockup;
  - Arabic title 36 pt.
- **p19:** lockup at the 20 mm top margin, 64 mm wide.
- **Works pages:**
  - large royal-blue work number (40 pt) at the head of the text column; the small English "0N / 03" stays as the kicker;
  - **navy panel** behind the photos instead of the tint. Navy tests better: the small photos sit like framed prints, and with p13 and p19–20 it gives the book dark beats. Captions on navy are white at 82% (8.96:1).
- **p6 banner:** re-cropped to the umbrella crown and the minarets with the dome out of frame, set in duotone.
- **p3 photo:** re-crop at 118%, anchored to the top. The umbrellas and minaret are now the subject; less empty marble.
- **pp8, 10, 11:** green filler diamonds changed to tint, so green stays an accent.
- **p8 and p10 tiles:**
  - San Diego tile cropped tighter on the palm group;
  - rope-access tile cropped tighter (the brick is reduced; a little remains at the edge).
- **p12:** fleet image at 96% and centred, so the vehicles clear the trim by more than 8 mm. The floor tint now fades out at its sides and bottom instead of ending in a hard edge.

**Not applied**
- **p17–18 optical re-sizing of partner logos:** a separate pass; not in the must list. Faint originals still need official files.
- **p8 Arabic list column widening:** the landscaping page keeps the English-wide columns from v08, which fixed the r4 English wraps. The Arabic item wraps to two lines, as it did before.

## Content nice-to-haves

**Applied** (pure language, no new fact)
- N1: sector order on p10 in both languages
- N2: comma instead of a full stop before «وتخدم» on p3
- N3: «بموجب السجل التجاري»
- N4: «تتولى … لجميع أنواع» on p7
- N5: p6 card 01, both languages
- N6: «من عام 2023»
- N7: «وفي غيرها من المجالات»
- N9: «ثلاثة قطاعات نخدمها»
- N10: "innovate and excel"
- N11: "to a high standard … valued clients'"
- N12: p20 "Images labelled 'Illustrative image' are visuals created from images supplied by the client"
- N13: "Al Madinah Al Munawwarah" kept on one line on p19
- N15: page reference in both languages on p6 («صفحة 07» / "PAGE 07")

**Declined**
- N8: it rewrites the client's own goal wording; the reviewer said to offer it, not impose it. Left for the client.
- N16: an art-direction question about non-Madinah images; no text change.

## Images
- No image appears on two pages (build log: "none").
- ppi values match v09, except:
  - p3 plaza 277
  - p6 band (duotone) 250
  - p16 entrance 261, room 224
  - p12 fleet 390 at 285 mm
- Full table in `_work/build_v10.log`.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**. 20 pages; Tajawal and IBM Plex Sans, no fallback; 4,695 Arabic characters.
- **Forbidden strings, all 0:** Emaar, EMAAR, «شهد», Shahd, "single company", «في عقد مع شركة واحدة», «اطليني», CONSANY, Suzuki, ISUZU, DZIRE, «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp, "WE DO THE BEST", «تبرم العقود», «وأنظمة الري». No harakat.
- **New strings present once each:** M1 (both languages), N14 (both), M3, M4, M5, M2.
- **Contents, folios, bookmarks:** contents 03/04/06/13/14/17/19 match the pages; no folio mismatches; bookmarks point to 2, 3, 4, 6, 13, 14, 17, 19, 20.
- **Contrast (WCAG):**

  | Page | Pair | Ratio |
  |---|---|---|
  | p13 (flat navy) | white | 12.55 |
  | p13 | periwinkle | 5.50 |
  | p13 | green numerals | 5.83 |
  | p20 | white lockup line on the gradient (navy to royal end) | 12.55 → 6.59 |
  | p20 | credits grey on white | 7.61 |
  | p20 | bold navy on white | 12.55 |
  | works panels | captions | 8.96 |

- **Fit:** p20 credits end at 186 mm (page is 210 mm). p3 text ends at 127.6 mm; the fact table runs 135–189 mm; the footer is at 197 mm.
- **Visual check:** all 20 pages viewed on the contact sheets; pp1, 3, 14 and 16 also at full preview size; cab door at 300 dpi.

## Open
- Client confirmation of the name strings, the Dar Al Taqwa work status, and a tagline.
- His own photographs, the original bus-shelter file, official partner logo files.
- Native Arabic proofread, second-viewer check, accessibility tagging.
