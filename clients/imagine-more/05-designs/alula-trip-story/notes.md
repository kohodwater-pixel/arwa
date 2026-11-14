# AlUla trip story — notes (v01)

**What:** the client's existing 9:16 story rebuilt at 1080×1920 px, sRGB PNG, in three options that differ only in the background photo. Client picks one.

| Option | Background | Files |
|---|---|---|
| A | Elephant Rock (Jabal AlFil) | `imagine-more_alula-trip-story_option-a_ar_v01.png` / `.html` |
| B | Hegra, Qasr al-Bint necropolis, Tomb 21 | `imagine-more_alula-trip-story_option-b_ar_v01.png` / `.html` |
| C | AlUla Old Town under the cliffs | `imagine-more_alula-trip-story_option-c_ar_v01.png` / `.html` |

Shared source: `story.css`, `assets/` (fonts, lifted logos and footer icons, photos). Photo licences: `photo-credits.md`.

**Changes from the reference (only these):**
1. Background photo.
2. Date chip now reads `كل يوم جمعة` / `من 20 نوفمبر حتى 5 فبراير` on two lines; the chip row is 104 px tall instead of 82 px and 24 px wider.
3. Old price `320` (45 px, medium, white at 80%) with a small riyal sign to its left, one 3 px strike line across the digits only, placed above the main riyal sign beside `299`. To make room, `299` is 118 px instead of 124 px (about 5% smaller) and sits 32 px further right, the price label moved 20 px right, and the divider and group note moved 16–18 px left.

**Copy used:** exactly as in `01-brief/brief.md`. One point differs from the reference pixels: the reference spells `للحجـز والأستفسار` (with a hamza); the brief gives the correct `والاستفسار`, which is what is set here.

**Assumptions / gaps:**
- Typeface: Alexandria (SIL OFL) for everything except the phone line, which uses Cairo. Chosen by comparing against crops of the reference; not confirmed by the client.
- HIPPO and Imagine More logos, the four social icons and the WhatsApp icon are lifted from the 720 px reference (luminance mask, 4× Lanczos); no vector files were supplied.
- Include-row icons, the group icon, the sparkle stars and the riyal sign are redrawn as SVG.
- All three photos need a photographer credit when published; see `photo-credits.md`.

**Rebuild:** `python3 _work/build.py` regenerates the three HTML files from `_work/options.json`; `node _work/render.cjs a b c` exports the PNGs; `python3 _work/compose_bg.py` makes the background canvases.
