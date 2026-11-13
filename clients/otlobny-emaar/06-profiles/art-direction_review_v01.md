# Art-direction review — company profile, draft v01

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-13  **Author:** art-director
**Reviewed:** `otlobny-emaar_company-profile_screen_ar-en_v01.pdf` through all 20 previews in `_work/preview_v01/`, against `art-direction.md`, `build-notes_v01.md`, the decision log, and the client's original (`_work/original_pages_contact.png`).
**Scope:** concept and craft only. Facts, spelling and copy are the quality-reviewer's. No copy is changed by this review; every instruction uses text already in `content-outline.md`.
**For:** the corporate-designer (build v02) and the Creative Director.

Units are millimetres; origin top-left; columns K1–K12 counted from the right, rows R1–R6, as in `art-direction.md` 2.2.

**Overall verdict: not ready for the client. The system is sound; six pages are good, and the pages that matter most to a buyer (cover, works, partners) are the weakest.** Much of that is my specification, not the designer's execution: the build is accurate, clean and consistent, and where it looks thin it is mostly because it followed the direction faithfully. Where this review changes the direction it says so (section 7).

**Geometry sketches.** The main proposals below were laid out roughly with the real fonts, copy and assets to check that the numbers fit: `_work/ad-sketch_v01/ad-sketch_v01_1.png` (cover), `_2` (mission at statement size), `_3` and `_4` (service list pages 10 and 12), `_5` (project page), `_6` and `_7` (partners). They are proofs of fit, not designs: icons are missing, ordinals are not bidi-isolated, spacing is approximate. Do not copy their code; build from the numbers here.

---

## 0. The Creative Director's four impressions, tested

| Impression | Finding |
|---|---|
| (a) Many pages sparse, lower half empty | **Right for pp4, 5, 9, 10, 13, 15–17; not for p12.** The cause is not the amount of white (the direction asks for half of each white page to stay empty) but that all content hangs from the top and nothing answers it below, exactly as in the original. p12 runs to y 152 and is not sparse; its problem is (c). |
| (b) Partners page weakest | **Right.** The grid is not the fault. The logos are small because of two rules: the 150 ppi cap and levelling to about 400 mm². Twelve marks are 11–26 mm wide inside 52 × 44 cells; seven cannot be read. The title parked in three cells reads as a hole in the grid. |
| (c) Icon-only panels read as unfinished | **Right, and it is my specification that fails.** A 12 mm line icon enlarged to 46 mm with its stroke scaled becomes a 5.75 pt pictogram on an 83 × 132 slab: it reads as a placeholder for a missing photograph. Four pages have it (9, 10, 12, 13), not three. |
| (d) Cover restrained to the point of plain | **Right, but the fault is composition, not restraint.** Five unrelated objects (corner diamond, photo diamond, green diamond, lockup, sparkle band) float with no dominant and no alignment between them, and the right-hand centre is a void. |

---

## 1. Verdict per page

| Page | Verdict | One sentence |
|---|---|---|
| 1 Cover | **Redo** | Five floating objects and no dominant; recompose around one central photo diamond and one corner cut (section 4). |
| 2 Contents | **Keep** | Clear, calm, the paired rows work; no change. |
| 3 About | **Adjust** | Good page, but "2021" at 40 pt collides with the hairline above it and the table's first rule is grey while the others are periwinkle. |
| 4 Vision | **Adjust** | The statement is set too small to carry a page and ends at y 120; set it at statement size (change 5). |
| 5 Mission | **Adjust** | Same as p4; the pair must change together. |
| 6 Goals | **Keep** | The best white page in the file; only equalise the padding under the three-line row 02, whose text touches the next rule. |
| 7 Services overview | **Keep** | The strongest page; the uneven row heights and the 14 mm holders are accepted. |
| 8 General Contracting | **Keep** | The triptych works when the centre is a photograph and the list has five rows. |
| 9 Landscaping | **Redo** | Icon slab reads as a missing image; move to the service list template (section 5). |
| 10 Maintenance | **Redo** | The emptiest page in the file: two short rows beside a slab; same template change. |
| 11 Cleaning | **Adjust** | Layout holds, but the duotone is murky and the figure is hard to find; lift the image (change 7). |
| 12 Manpower Supply | **Redo** | Text is full and fine; only the icon slab fails; same template change. |
| 13 Logistics (draft) | **Redo** | Same template change; draft pill stays. |
| 14 Why OTLOBNY Emaar | **Keep** | Dense but ordered; the content-driven row heights are accepted. |
| 15 Work: bus shelters | **Adjust (major)** | The client's own proof is shown at 83 × 75 with a strip of clutter beneath; enlarge the frame, remove the index (change 2). |
| 16 Work: Chamber | **Adjust (major)** | As p15. |
| 17 Work: Shahd hotel | **Adjust (major)** | As p15. |
| 18 Partners 1 | **Redo** | Logos too small, title sitting in the grid; new layout in section 3. |
| 19 Partners 2 | **Redo** | As p18; the nine new logos already look right, the old 18 do not match them. |
| 20 Contact / back cover | **Adjust** | Narrow block on off-grid edges (x 60 and 237), small values, a stray sparkle band bottom-left. |

Six keep, six adjust, eight redo (four of the eight are one template change).

---

## 2. The ten changes, in priority order

Page count stays at **20** and the contents page does not change. Pairing two services to a page was tested on paper and rejected: at the document's type sizes only Landscaping + Maintenance fit together, which would create a one-off dense template and an odd page count; the list template in change 3 solves the same pages inside the existing system.

### 1. Partners, pp18–19 — full redesign
Section 3. This is the page the client will judge the work by; do it first.

### 2. Project pages 15–17 — make the evidence the page
The three photographs are the only proof of work in the document and are currently the same size as a stock image.

- **Frame:** K4–K9 × R2–R5 = x 85–212, y 53.5–158.5 (**127 × 105**). Full colour, square corners, no effects, as before.
- **Crops** (fractions of the files in `assets/photos/`; check each at 100%, tolerance ± 0.02):
  - `bus-shelter.png`: (0.40, 0.02, 0.989, 1.00) = about 560 × 463 px, 112 ppi. The left edge must stay right of the debris on the pavement (x 0.33–0.40 of the source); if any of it shows, move the left edge to 0.41 and trim the top to keep the ratio.
  - `chamber-building.png`: (0.137, 0.00, 0.99, 1.00) = 549 × 454 px, 110 ppi.
  - `shahd-hotel.png`: (0.20, 0.085, 0.979, 1.00) = 822 × 680 px, 164 ppi. Keep both minarets in frame.
- **Text blocks:** Arabic K1–K3 (x 217–278), English K10–K12 (x 19–80), both from y 53.5. Project name Heading 20 Bold / 17 SemiBold (three lines are fine at 61 mm), 4 mm, sentence in Body. Unchanged copy.
- **Scope chips:** stay, same words, but move into the side blocks, **bottom-aligned to y 158.5** (the frame's bottom edge); they may wrap to two lines, 1.5 mm between lines. **Centre the Arabic word optically in its pill**: in v01 it sits about 0.6 mm high in every Arabic chip (pp15–17).
- **Delete the project index in R6.** It is my specification and it is wrong: the Arabic line runs right to left and the English line left to right, so on pp15 and 17 a project's two names sit at opposite ends, and the English caps break into orphans ("SHELTERS", "INDUSTRY"). The ordinal "01 / 03" above the title already does the job. R6 stays empty.
- Title zone and ordinal unchanged. All three pages identical in structure.

### 3. Service pages without a photograph (9, 10, 12, 13) — list template, no slab
Section 5.

### 4. Cover — recompose
Section 4.

### 5. Vision and Mission (pp4–5) — statement size
Verified for the longer of the two (mission) in sketch `_2`.

- Arabic statement: Tajawal **Bold 24 pt, line height 1.5**, K1–K5 (x 173–278), top y 53.5.
- English statement: IBM Plex Sans **SemiBold 19 pt, line height 1.35**, K8–K12 (x 19–124), top y 55 (so the two first lines align optically).
- Centre hairline x 148.5 extended to y 53.5–186.
- Mission then runs to about y 170 (Arabic, nine lines) and y 143 (English). Vision will be shorter; that is right, and the sparkle band on p4 stays where it is (y 166–178) only if the Arabic ends above y 156; otherwise delete it from p4.
- Both pages use the same sizes. If the Arabic mission exceeds y 186 in the real build, drop **both** pages to 22 / 17.5; never one alone.
- No widow: the last Arabic line must hold at least two words.

### 6. Contact / back cover (p20)
- Move the block onto the grid: rows and hairlines span **K2–K11, x 41–256** (v01 uses x 60–237, which are not column lines; my error). Arabic labels right-aligned at x 256, English labels left-aligned at x 41, values centred on x 148.5.
- Lockup, white: height **40** (width 94.7), centred on x 148.5, y 22–62.
- Title row «تواصل معنا» / "Contact": reduce from Section size to **Page title 26 / 22**, top y 74, on the block edges (x 256 and x 41). At 32 / 27 it competes with the lockup.
- Rows from y 94, pitch 15; values IBM Plex Sans Medium **20 pt** (from 17).
- Address row top y 158, same edges, as built.
- Sparkle band: move from the bottom-left corner to the centre: 3 × 12, white 30%, x 119–178, y 184–196.
- The website row keeps its pill in drafts. In any version sent as final the row carries one confirmed domain or is removed, and the rows re-space.

### 7. Photograph panels (pp8, 11) — lift the duotone
- p11: the cleaner is lost in reflections. Re-derive `p11_office-cleaner_duotone.png` with the midpoint (Royal blue) at 45% instead of 55% and a gamma of about 1.15 before the map, so the figure and the cloth separate from the glass. No retouching.
- p8: apply the same curve so the two panels match; check that the lamp at top right does not blow to a white hole against the page (if it does, move the crop left by 0.02).
- Nothing else changes on these two pages.

### 8. About (p3) — fact table
- "2021": IBM Plex Sans Bold **28 pt** (from 40), centred in its row with at least 3 mm clear of the rule above and below. CR number Bold **22 pt**. The two shared numerals then read as a pair.
- Row pitch stays 16 from y 118 (deviation 4, accepted).

### 9. Hairlines, padding and small type — one sweep
- **One hairline colour.** The first rule of the tables on pp3 and 6 prints grey; every other rule is periwinkle. All hairlines on light grounds: 0.25 pt `#9BABD7`.
- p6: equal padding above and below the text in every row (minimum 5 mm below the last line); row 02 currently touches the next rule.
- Arabic text inside every pill (chips pp15–17, draft pills pp13 and 20): optically centred, see change 2.
- English labels in caps never break into a one-word last line; where one would, the label goes to sentence case at the same size or the measure is widened.

### 10. Before a final, not before v02
The PDF is still untagged (build note 20). Tagging, alternative text and a second-viewer check remain requirements for the final export; they do not block the v02 draft.

---

## 3. Partners, pp18–19 — the redesign

Client instruction and the Creative Director's ruling 3 stand: transparent logos directly on **white**, no tiles; all **27** kept; the existing 18 first in file order (`existing-01` … `existing-18`), then the nine (`new-01` … `new-09`), read right to left, row by row. Files from `assets/partners-transparent/` only; Keeta and ZERO in the plain transparent variants (not `_on-yellow`, not `_on-dark`). Nothing redrawn, recoloured, sharpened or keyed further.

### 3.1 Where the title goes
Out of the grid and into the **title zone, like every other page**: ordinal line at y 26 ("01 / 02" on p18, "02 / 02" on p19, each bidi-isolated), then the title at y 31.5, Arabic right-aligned at x 278, English left-aligned at x 19, at **Section size 32 / 27** (there is now room; deviation 11 falls away). The title appears on both pages, as "Our Work" does on pp15–17. No sparkle marker in the grid.

### 3.2 Grid
White ground on both pages. **Horizontal hairlines only** (0.25 pt periwinkle) at y 56, 98.5, 141 and 183.5, across x 19–278. **No vertical rules**: without them an uneven column count does not show, and the page reads as three calm shelves, the same language as the lists on pp2, 6 and 14.

| | p18 | p19 |
|---|---|---|
| Logos | 15 (existing 01–15) | 12 (existing 16–18, then new 01–09) |
| Rows | 3 of **42.5**, tops y 56, 98.5, 141 | same |
| Columns | 5 cells of **51.8** | 4 cells of **64.75** |
| Cell centres, x (right to left) | 252.1, 200.3, 148.5, 96.7, 44.9 | 245.6, 180.9, 116.1, 51.4 |
| Row centres, y | 77.25, 119.75, 162.25 | same |

15 + 12 = 27, no empty cell, no cell used for text. The seam between old and new falls inside row 1 of p19.
Ownership note, p19 only: Label style, top y 186.5, Arabic at x 278, English at x 19 (strings as ruled).

### 3.3 Logo box and optical sizing
- **Logo box 38 × 24**, centred on the cell centre (measured on the visible mark, i.e. the non-transparent bounding box, not the PNG canvas). Minimum clear margin to any hairline 8.
- Size by **area, then correct by shape and weight**; never by a common height or width:
  - target bounding-box area about **560 mm²** for a mark of ordinary proportion (1.3:1 to 2.2:1);
  - **wide wordmarks** (wider than 2.2:1): full 38 width, height as it falls;
  - **compact and tall marks** (narrower than 1.3:1): height 23–24; tall emblems with lettering under them never above 24;
  - **dense, solid marks** (Tiny House, Keeta, HungerStation, chop & co, Hippo): about 10% under target;
  - **thin-line or pale marks** (WE AR SPA, Harmony, Novotel, ZERO, Rotana): up to the box limit;
  - one exception to the box: Dar Al Taqwa (6.5:1) runs **42 wide**, or it is a hairline.
- Then look at the page at fit-to-window and adjust any single mark by at most ± 8% until no logo is the first or the last thing the eye finds.

### 3.4 Resolution rule for a screen PDF
The 150 ppi floor is a print rule. On a laptop at fit-to-window an A4 landscape page is shown at roughly 110–130 pixels per inch, so an image placed at 100 ppi is displayed at about its native pixels. I tested the twelve low-resolution marks at 150, 100, 75 and 60 ppi (`_work/partners_enlargement-test_v01_part1.png`, `_part2.png`; each row is one logo at 1×, 1.5×, 2× and 2.5× of its 150-ppi size; the Development Authority and Taza rows start from their effective detail, so their columns are 75, 50, 37 and 30 ppi effective):

| Tier | Which | May be placed down to | Meaning |
|---|---|---|---|
| A — sharp | vector or large rasters: existing 04, 06, 12, 13, 14, 16 and all nine new | no limit inside the box | |
| B — low-resolution with lettering | existing 01, 03, 05, 08, 09, 10, 11, 15; existing 02 and 17 by their effective detail (121 px and 143 px wide) | **100 ppi** | up to **1.5×** the size it has at 150 ppi |
| C — low-resolution, bold shape, no small lettering | existing 07 (HSH), 18 (calligraphic mark) | **80 ppi** | up to **1.9×** |

At 100 ppi every mark holds at fit-to-window and at 125% zoom. At 75 ppi bold shapes still hold but lettering breaks up. At 60 ppi everything is visibly soft: never. Cooperative Taibah was tried at 83 ppi in the sketch and looked soft; it stays in tier B. Placed with the browser's default smoothing; no `image-rendering: pixelated`, no sharpening filter.

What no size can fix: the small second lines of existing 01, 02, 03, 08, 09 and 15 are blurred in the client's own PDF and stay unreadable. The marks themselves now read. Official artwork for the twelve tier-B/C logos is still the real fix and is required for print.

### 3.5 Size of each mark (visible mark, width × height in mm)

| # | Logo | v01 | **v02** | ppi at v02 size |
|---|---|---|---|---|
| E1 | green-dome emblem | 10.8 × 16.9 | **14.7 × 23.0** | 110 |
| E2 | Development Authority | 20.6 × 13.0 | **30.0 × 19.0** | 102 effective |
| E3 | Al Maqar | 21.7 × 14.1 | **29.5 × 19.1** | 110 |
| E4 | WE AR SPA | 22.1 × 18.1 | **28.0 × 22.9** | vector |
| E5 | Mawaddah | 25.9 × 15.5 | **33.0 × 19.6** | 122 |
| E6 | Imagine More | 28.7 × 13.9 | **36.0 × 17.5** | vector |
| E7 | HSH | 17.6 × 9.1 | **32.0 × 16.3** | 83 (tier C) |
| E8 | Cooperative Taibah | 13.5 × 12.2 | **20.3 × 18.3** | 100 |
| E9 | Dar Al Taqwa Hotel | 34.0 × 5.2 | **42.0 × 6.5** | 177 |
| E10 | Dallah Taibah Hotel | 16.6 × 16.8 | **24.2 × 24.0** | 103 |
| E11 | Al Madinah Harmony | 29.2 × 13.7 | **38.0 × 17.8** | 124 |
| E12 | Tiny House | 30.2 × 13.3 | **34.0 × 14.9** | sharp |
| E13 | Platinum | 26.3 × 15.2 | **31.0 × 17.9** | vector |
| E14 | Madinah Chamber | 31.5 × 12.7 | **38.0 × 15.3** | vector |
| E15 | column emblem | 14.9 × 17.3 | **19.9 × 23.1** | 112 |
| E16 | Hippo | 14.5 × 21.0 | **16.6 × 24.0** | vector |
| E17 | Taza | 23.8 × 16.8 | **28.0 × 19.8** | 130 effective |
| E18 | calligraphic mark | 18.8 × 10.7 | **30.0 × 17.0** | 94 (tier C) |
| N1 | Manazil Al-Mukhtara | 22.4 × 17.8 | **30.1 × 24.0** | sharp |
| N2 | Novotel | 32.0 × 12.5 | **38.0 × 14.8** | sharp |
| N3 | Keeta | 27.4 × 14.6 | **31.0 × 16.5** | sharp |
| N4 | Jahez | 24.0 × 16.7 | **28.0 × 19.5** | sharp |
| N5 | Medina Festival Dates | 15.3 × 21.0 | **17.4 × 23.9** | sharp |
| N6 | HungerStation | 27.9 × 14.3 | **32.0 × 16.4** | sharp |
| N7 | Rotana | 34.0 × 11.7 | **38.0 × 13.1** | sharp |
| N8 | Chop & Co | 24.9 × 16.1 | **28.0 × 18.0** | sharp |
| N9 | ZERO | 33.9 × 11.8 | **38.0 × 13.3** | sharp |

The smallest marks grow most: HSH, the calligraphic mark, Cooperative Taibah and the Development Authority roughly double in area or more. Sketches `_6` and `_7` show the two pages at these sizes with the real files.

Count check before handing over: 15 + 12 = 27; 18 `existing-`, 9 `new-`; no `_on-` variant; nothing from the rejected folder.

---

## 4. Cover and back cover

Existing assets only: `assets/derived/cover_glass-facade_duotone.png`, the three logo SVGs. No new image, no line of text added.

**The idea, taken literally from the concept:** what the two languages share sits in the centre. One large photograph diamond in the middle of the page, the Arabic title to its right, the English to its left, and the wordmark's 45-degree cut as one large corner. Three objects with a stated relationship instead of five without one. Verified in sketch `_1`.

| Element | v02 specification |
|---|---|
| Corner cut | Triangle with vertices (0, 0), (163.5, 0), (0, 163.5), brand gradient (dark at the left). Replaces diamond D1. Straight edge, no radius. |
| Photo diamond D2 | Bounding box **130**, centre **(148.5, 92)**, radius 16% of the side; same file, same crop (655 px → 128 ppi). Its upper-left edge runs parallel to the triangle's edge with a white channel of 8.5 between them (12 measured horizontally). |
| Green diamond D3 | Bounding box 18, centre **(191.5, 135)**: on the same 45-degree line, the same 8.5 channel from D2. |
| Lockup, colour | Height **36** (width 85.2), right edge x 278, top y 22. Nearest point of D2 is 13 away: more than the clear space. |
| Sparkle band | Delete the periwinkle band under the lockup. One band inside the triangle: 3 × 12, white 30%, x 19–78, y 26–38. |
| Titles | Unchanged sizes (46 / 38), one shared baseline at **y 181**; Arabic right-aligned at x 278, English left-aligned at x 19. D2's lowest point is y 157, so both titles are clear. |
| Activity line | Stays dropped (deviation 1, accepted). |

Fallback if the facade photograph's licence is refused: D2 becomes a solid Royal blue `#3758B0` diamond; everything else unchanged.

**Back cover (p20):** change 6. With the lockup at 40 and the block on the grid it closes the document with the same weight the new cover opens it. No further device is added: the cover's corner is not repeated, so the two full-gradient pages (7 and 20) stay the only ones.

---

## 5. Pages 9, 10, 12, 13 — what replaces the icon slab

Template **T6-G is withdrawn.** A new template, **T6-L (service list)**, built on the zones of T4, which is already the best-working white page (p6):

- Zones: Arabic K1–K5 (x 173–278), centre K6–K7 (x 129–168), English K8–K12 (x 19–124).
- Ordinal line y 26 and Page title 26 / 22 at y 31.5: unchanged.
- **Centre, level with the title:** the service's icon from p7 at its p7 size in an outlined diamond holder (bounding box 18, 0.75 pt Royal blue outline, icon stroke Royal blue), centred on x 148.5, y 28–46. This is the only place the icon appears; it ties the page to its row on p7. No gradient panel, no enlarged icon, no sparkle band.
- **Intro:** Lead 14 / 12.5 from y 53.5 in the two side zones.
- **Sub-services as rows:** start 8 after the lower of the two intros. Hairline above each row across x 19–278 and one closing hairline after the last. Each row: Arabic **Tajawal Bold 17 pt, line height 1.5** | a green diamond 2.6 in the centre on the first line's optical middle | English **IBM Plex Sans SemiBold 14.5 pt, line height 1.35**. Row padding 4 above, 4 below, minimum row height 20; a row may run to two lines and the two languages share the row height.
- **p12 only:** the contract sentence follows the last row after 5, in Body, both sides. It must end above y 186.
- **p13:** draft pill unchanged.

Sketches `_3` (Maintenance) and `_4` (Manpower) were drawn at the heavier Heading size (20 / 17): Manpower then overruns the footer, which is why the rows are specified at 17 / 14.5. **That final size was not re-sketched; measure p12 first.** If its contract sentence still passes y 186, reduce the row padding to 3 on all four pages.

Expected result: p9 and p12 fill to about y 165–180, p13 to about y 140, p10 to about y 125. Maintenance remains the lightest page because the client's material gives it two sub-services; it is not padded, and with its rows at 17 pt it reads as a short, deliberate page rather than an unfinished one.

Rhythm across the section: 8 photo · 9 list | 10 list · 11 photo | 12 list · 13 list. If a suitable team photograph arrives (open question with the client), p12 returns to T6-P.

---

## 6. Corrections, and deviations accepted

### Must be corrected in v02 (breaks the direction or the craft standard)

| Where | What | Fix |
|---|---|---|
| pp15–17, 13, 20 | Arabic text sits high inside every pill | Centre optically |
| p3 | "2021" touches the hairline above | Change 8 |
| pp3, 6 | First table rule grey, the rest periwinkle | Change 9 |
| p6 | Row 02 text touches the next rule | Change 9 |
| pp15–17 | English index labels break into one-word lines | Index removed (change 2) |
| p20 | Block edges at x 60 / 237 are off the grid | Change 6 (the numbers were mine) |
| pp18–19 | Logo sizes | Section 3 |
| pp9, 10, 12, 13 | Enlarged icons with a 5.75 pt stroke | Section 5 (the specification was mine) |

Checked and found correct: no letter-spacing on any Arabic class in the HTML (`.ar` is set to 0; tracking only on Latin labels and the Latin cover title); Arabic right and English left on all 20 pages; no diamonds outside the cover, the p7 holders and the bullets; one sparkle band per spread at most; logo on pp1, 7 and 20 only; project photographs in full colour and illustrative ones in duotone with the caption; no invented figure, chart or badge.

### Deviations in `build-notes_v01.md` that I accept

| # | Deviation | Ruling |
|---|---|---|
| 1 | Cover activity line dropped | Accepted; my own rule removes it. Title position is replaced by section 4 |
| 2 | Mockup crop not used on p12 | Accepted and agreed: the chest logos are recognisably wrong drawings of the mark |
| 3 | Title top at y 31.5 on every inside page | Accepted; better than the direction |
| 4 | p3 fact table from y 118, pitch 16 | Accepted, with change 8 |
| 5, 6 | pp7, 14 rows sized by content; 14 mm holders on p7 | Accepted; the copy may not be cut. T6-L holders are 18 because they stand alone |
| 7 | p14 title and description on two lines, dash dropped | Accepted as layout; the wording is the quality-reviewer's to confirm |
| 8 | List rows grow for two-line items | Accepted |
| 9 | Ordinal only on pp15–17 | Accepted |
| 10 | Scope chip words | Accepted |
| 11 | Partners title at 26 / 22 | Superseded: 32 / 27 in the title zone |
| 12 | Partners on white, hairline grid, no tiles | Accepted (Creative Director's ruling); grid revised in section 3 |
| 13 | 150 ppi cap on logos | **Replaced** by section 3.4 |
| 14, 15 | p20 title row, address aligned to rows, website pill, back-cover lines not repeated | Accepted, with change 6 |
| 16 | Draft pill on p13 and the website row only | Accepted per ruling 6; the logistics mentions on pp3, 7 and 14 remain the Creative Director's open item |
| 17 | Icons with round caps only | Accepted; my sentence contradicted itself |
| 18 | Sparkle drawn, not traced | Accepted; it matches at 2 mm |
| 19 | Line-break balancing | Accepted |
| 20 | PDF not tagged | Accepted for drafts only (change 10) |

---

## 7. Amendments this review makes to `art-direction.md`

So that the designer is not caught between two documents; `art-direction.md` itself is not edited.

1. **4.1, resolution, screen edition only:** photographs may be placed down to **110 ppi**; partner logos as in 3.4 above. The 150 ppi floor returns for any print edition, where the project frame goes back to 83 × 75 and the low-resolution logos need official artwork.
2. **T1 cover:** replaced by section 4.
3. **T6-G:** withdrawn; T6-L in section 5. The chamfered gradient panel no longer appears; the chamfer remains on the two photograph panels.
4. **T7:** frame 127 × 105 on K4–K9; project index removed.
5. **T3, pp4–5:** statement size 24 / 19.
6. **T8 / section 5:** replaced by section 3 of this review, within the Creative Director's ruling 3.
7. **T9:** block on K2–K11; sizes as in change 6.
8. **2.5, colour shares:** the four gradient panels go and the cover gains a gradient corner of about 21% of one page; the gradient's share of the document falls slightly and white rises. No new colour.
