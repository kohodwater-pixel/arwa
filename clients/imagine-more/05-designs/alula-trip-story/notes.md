# AlUla trip story — notes (v02)

**What:** the client's existing 9:16 story rebuilt at 1080×1920 px, sRGB PNG, in three options that differ only in the background photo. Client picks one.

| Option | Background | Files |
|---|---|---|
| A | Elephant Rock (Jabal AlFil) | `imagine-more_alula-trip-story_option-a_ar_v02.png` / `.html` |
| B | Hegra, Qasr al-Bint necropolis, Tomb 21 | `imagine-more_alula-trip-story_option-b_ar_v02.png` / `.html` |
| C | AlUla Old Town under the cliffs | `imagine-more_alula-trip-story_option-c_ar_v02.png` / `.html` |

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
