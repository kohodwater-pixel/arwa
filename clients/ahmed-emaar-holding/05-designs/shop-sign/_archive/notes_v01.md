# Shop sign v01 — Ahmed Emaar Holding (2026-11-23)

**Status:** v01 for internal review. Nothing here is approved yet.

## Size
- Width 250 cm (from the client). Height 60 cm is an estimate; the client must measure on site.
- From the site photo:
  - The concrete slab edge face (from the long crack down to the front edge of the underside) is about 80 px tall. At the wall plane the shutter is about 780 px wide. A typical shutter is 2.5–3.0 m wide (assumed; no real dimension is known). On that basis the slab edge is about **25–35 cm** high. That is clearly less than 80 cm.
  - The wall above the crack sits in the same plane as the slab edge. The 60 cm panel therefore covers the slab edge plus about 30 cm of wall above it, between the two column stubs. This also covers the crack line, which must be repaired first.
  - If the panel has to fit on the slab edge alone, it would be about 250 × 30 cm. That needs a different layout on a single line (see the handoff).
- The layout scales with the height. All sizes come from `H` in `_work/build_sign.py`. Change `W`/`H`, then re-run `build_sign.py`, `export_artwork.py`, `build_drawing.py` and `build_mockup.py` from `_work/`.

## Content (no invented content)
- **Option A:** logo mark on the right, «أحمد إعمار القابضة», and "AHMED EMAAR HOLDING" below it.
- **Option B:** the same, plus the tagline «حلول متكاملة للبنية التحتية والخدمات» from the client's board.
- There are no phone numbers, URLs, CR numbers or client logos.

## Letter heights (real size)
| | Option A | Option B |
|---|---|---|
| Mark (h × w) | 32.0 × 32.2 cm | 27.0 × 27.2 cm |
| Arabic name: alef height / full extent incl. hamzas | 12.3 / 22.7 cm | 10.2 / 18.8 cm |
| Latin caps | 6.0 cm (tracking 0.27 em) | 5.3 cm (tracking 0.21 em) |
| Tagline alef height | — | 5.0 cm |
| Margins to lettering, top/bottom/sides | 14 / 14 / 34 cm | 7 / 7 / 49.6 cm |

- The gold accent lines are 1.2 cm wide and run at 41°, the same angle as the cut on the mark. They are the only elements that reach the edge.
- Numerals are Western (0–9) throughout.

## Fonts and colours
- **Fonts:** Cairo 700 for the Arabic name and Cairo 600 for the tagline, both outlined. Inter 600 for the Latin, outlined. IBM Plex Sans Arabic for the labels in the technical drawing (live text, checked with `check_arabic_pdf.py`: PASS).
- **Colours (suggestions, to confirm with the sign maker):**
  - Navy #102232, about CMYK 100/78/45/55, RAL 5011 or 5004.
  - Gold #D4A95F, about CMYK 12/32/72/2, Pantone 7562 C or 871 C metallic.
- The artwork PDFs are RGB vector files (cairosvg). They are not PDF/X or CMYK; the CMYK values above are approximate.

## Mockups
- Each mockup is the client's site photo with the sign added using a four-corner perspective warp. Nothing else in the photo was changed.
- The caption strip sits below the photo and labels the image as a visualisation.
- I did not make a dusk or LED version.
