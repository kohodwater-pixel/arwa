# AlUla trip story — notes (A/B/C v04, D/E/F v01)

**What:** the client's existing 9:16 story rebuilt at 1080×1920 px, sRGB PNG, in three options that differ only in the background photo. Client picks one.

| Option | Background | Files |
|---|---|---|
| A | Maraya with the Ashar valley cliffs | `imagine-more_alula-trip-story_option-a_ar_v04.png` / `.html` |
| B | Hot-air balloon over the AlUla rock field, golden hour | `imagine-more_alula-trip-story_option-b_ar_v04.png` / `.html` |
| C | Sunburst seen from inside a cave, AlUla | `imagine-more_alula-trip-story_option-c_ar_v04.png` / `.html` |

Shared source: `story.css`, `assets/` (fonts, lifted logos and footer icons, photos). Photo licences: `photo-credits.md`.

**Changes from the reference (only these):**
1. Background photo.
2. Date chip now reads `كل يوم جمعة` / `من 20 نوفمبر حتى 5 فبراير` on two lines; the chip row is 104 px tall instead of 82 px and 24 px wider.
3. Old price `320` (44 px, medium, 100% white) with a 26×29 px riyal sign to its left, one 3 px strike line across the digits only, placed above the main riyal sign beside `299`. To make room, `299` is 118 px instead of 124 px (about 5% smaller) and sits 32 px further right, the price label moved 20 px right, and the divider and group note moved 16–18 px left.

**Copy used:** exactly as in `01-brief/brief.md`. One point differs from the reference pixels: the reference spells `للحجـز والأستفسار` (with a hamza); the brief gives the correct `والاستفسار`, which is what is set here.

**Assumptions / gaps:**
- Typeface: Alexandria (SIL OFL) for everything except the phone line, which uses Cairo. Chosen by comparing against crops of the reference; not confirmed by the client.
- HIPPO and Imagine More logos, the four social icons and the WhatsApp icon are lifted from the 720 px reference (luminance mask, 4× Lanczos); no vector files were supplied.
- Include-row icons, the group icon, the sparkle stars and the riyal sign are redrawn as SVG.
- All three photos need a photographer credit when published; see `photo-credits.md`.

**Rebuild:** `python3 _work/build.py` regenerates the three HTML files from `_work/options.json`; `node _work/render.cjs a b c` exports the PNGs; `python3 _work/compose_bg.py` makes the background canvases.

**v02 (after quality review r1; v01 is in `_archive/`):**
- Frosted panels (price panel, "تشمل الرحلة" tag, chip row) now have a dark warm-brown underlay beneath the glass so white text passes contrast. Underlay strength is set per option in `_work/options.json` (`under`, `chip`). Layout unchanged.
- Measured contrast of white text against the rendered background behind it, median (worst 5% of pixels), from `_work/contrast_v02.txt`:
  - A: price label 6.7 (6.5), 299 6.9 (6.2), 320 6.8 (6.5), group note 8.8 (6.6), include tag 11.4 (9.1), chips 5.7–6.0 (5.4)
  - B: price label 9.2 (7.9), 299 7.9 (6.1), 320 6.6 (5.9), group note 6.8 (5.9), include tag 11.6 (10.2), chips 6.6 (6.4)
  - C: price label 9.7 (7.3), 299 11.0 (9.2), 320 9.9 (6.4), group note 5.3 (4.7), include tag 11.1 (8.9), chips 4.9 (4.7); headline 5.0, sub-headline 4.2 (large text) after strengthening C's top gradient
- `320` is 100% white; its riyal sign is larger.
- Option B: photo moved up 77 px and the bottom gradient strengthened so the include row sits on calmer ground (the carved pediment is now behind the price panel).
- Breakfast icon redrawn after zooming on the reference: solid cup with handle and three steam lines, croissant in front.
- Headline weight: 500 and 600 were compared against a reference crop at the same scale; 600 is closer in stroke thickness and keeps the width match, so it stays.
- PNGs carry an embedded sRGB ICC profile.

**v03 (client rejected the v02 photos on 2026-11-14; v02 is in `_archive/`):**
- Only the backgrounds and their overlays changed. Layout, copy, logos, dates, prices and panels are as v02.
- New photos chosen for depth after reviewing 247 Commons candidates (`_work/contact_v03_*.jpg`, shortlist `_work/shortlist_v03.jpg`, Maraya set `_work/maraya_options.jpg`). Details and licences in `photo-credits.md`.
- Photos are colour-graded (`_work/grade.py`); the top gradient colour is now configurable per option (dark brown on C). Settings in `_work/options.json`; v02 settings kept in `_work/options_v02.json`.
- Measured contrast, median (worst 5%), from `_work/contrast_v03.txt`:
  - A: headline 6.0 (5.6), sub 5.2 (4.9), chips 4.8–4.9 (4.5), price label 10.5 (6.9), 299 10.5 (5.3), 320 6.4 (5.2), group note 10.1 (5.8), include tag 11.7, include labels 13.4 (11.9), phone 18.6
  - B: headline 7.0 (6.3), sub 6.1 (5.4), chips 5.3–5.6 (5.0), price label 8.8 (8.2), 299 8.1 (7.3), 320 7.8 (7.7), group note 7.9 (7.6), include tag 12.1, include labels 16.2 (10.1), phone 18.9
  - C: headline 19.2 (7.5), sub 19.2 (5.5), chips 13.7–14.0 (5.8), price label 12.5 (9.7), 299 8.9 (7.4), 320 9.8 (8.8), group note 14.5, include tag 13.5, include labels 18.1 (7.1), phone 19.1
- Comparison with the client's mood reference: `_work/side-by-side_mood-reference-vs-v03-abc.png`.

**2026-11-15 — copy change and three more options:**
- Copy change from the client, all options: `وجبة عشاء لذيذة` became `وجبة غداء لذيذة` (lunch instead of dinner); same icon, same two-line break. A/B/C re-exported as v04 with only this change; v03 is in `_archive/`. Checked: `وجبة غداء` present and `عشاء` absent in all six HTML files; include row inspected in `_work/zoom_include-row_abcdef.png`. Note: `01-brief/brief.md` still lists the dinner wording under fixed content.
- New options, first versions: D `imagine-more_alula-trip-story_option-d_ar_v01` (Elephant Rock at dusk with camel riders), E `..._option-e_ar_v01` (Qasr al-Farid at golden hour), F `..._option-f_ar_v01` (Sharaan rock field under sun rays). Same layout, copy, logos and panels. D uses a dark brown top gradient because the headline sits on red rock; E and F keep the blue one.
- Candidates reviewed for this round: 357 more Commons thumbnails (`_work/contact_def_0..6.jpg`), shortlist `_work/shortlist_def.jpg`.
- Contrast for all six: `_work/contrast_v04_def.txt`. Comparison with the mood reference and option B: `_work/side-by-side_mood-reference-vs-b-d-e-f.png`.
