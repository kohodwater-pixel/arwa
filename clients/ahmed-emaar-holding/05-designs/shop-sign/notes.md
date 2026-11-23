# Shop sign v02: Ahmed Emaar Holding (2026-11-23)

**Status:** v02. These are the fixes from quality review r1. The client has not approved anything yet. The v01 files are in `_archive/`, together with the v01 notes.

## Size
- **Width:** 250 cm, as given by the client.
- **Height:** 60 cm, an assumption that still has to be measured on site.
- **Estimate from the site photo:**
  - The slab-edge face (from the crack line to the edge of the underside) is about 80 px tall.
  - The shutter is about 780 px wide at the wall plane.
  - I assumed a typical shutter width of 2.5–3.0 m. That gives a slab-edge face of about **30–40 cm**. The range is wide because the camera points steeply upward.
- The wall above the crack is flush with the slab edge. So the 60 cm panel covers the slab edge plus about 20–30 cm of wall above it, and it crosses the crack line.
- **Measurements to ask for on site** (also listed on the drawing):
  1. Height of the slab-edge face.
  2. Usable wall height above the crack.
  3. Clear width between the two column stubs.
- **To re-scale the layout:** every size is derived from `H`. Edit `W`/`H` in `_work/build_sign_v02.py`, then re-run these four scripts:
  - `build_sign_v02.py`
  - `export_v02.py`
  - `build_drawing_v02.py`
  - `build_mockup_v02.py ..`

## Fabrication outlines
- Each gold element is a single welded compound outline. There are 4 elements in option A and 6 in option B:
  - mark
  - Arabic name
  - English name
  - tagline (option B only)
  - rules (option B only)
  - corner accents, expanded into filled bands and trimmed at the panel edge
- **Checks run on the files:**
  - The files contain no live text, no strokes and no clip paths.
  - The nonzero and evenodd fill rules render identically (0 different pixels).
  - Each welded text line and the mark were rendered against the original overlapping glyphs to confirm nothing was lost: 0 different pixels.
- The artwork is a cut file in RGB at 1:10. It is not print-ready.

## Sizes at real scale (cm)
| | Option A | Option B |
|---|---|---|
| Mark h × w | 38.0 × 38.3 | 28.6 × 28.8 |
| Arabic name: alef height / full extent / width | 14.7 / 27.2 / 170.8 | 10.8 / 19.9 / 125.3 |
| English: cap height / width (tracking) | 7.0 / 170.8 (0.30 em) | 5.6 / 125.3 (0.20 em) |
| Tagline: alef height / width | — | 8.0 / 171.9 |
| Margins to lettering T/B/R/L | 11.0 / 11.0 / 16.7 / 16.7 | 8.0 / 8.0 / 39.0 / 39.0 |

In option A the name is about 20% larger than in v01, which had an alef of 12.3 and a full extent of 22.7.

## Stroke widths at real scale (cm)
| | Option A | Option B |
|---|---|---|
| Mark: bars / thinnest arch / swoosh | 3.6–4.0 / 2.8 / ≤ 3.2, tapering to a point | 2.7–3.0 / 2.1 / ≤ 2.4, tapering |
| Arabic name: stem / horizontal | 2.8 / 2.4 | 2.0 / 1.8 |
| English: stem / horizontal bar | 1.3 / ≈ 1.0 | 1.0 / ≈ 0.8 |
| Tagline: stem / horizontal | — | 1.0 / 0.9 |
| Gold lines and rules | 1.2 | 1.2 |

**How each part can be made** (suggestions for the sign maker to confirm):
- **Halo-lit channel letters, 5–8 cm deep:** the mark and the Arabic name. The swoosh tip should be blunted slightly.
- **Flat-cut, 5–10 mm, unlit:** the English name, the tagline and the gold lines.
- These replace the single "3–5 cm raised, face- or halo-lit" wording used in v01.

## Viewing distance
- The sign is meant to be read from 20–30 m away (from the street or a passing car).
- **Rule of thumb only:** each 1 cm of letter height (alef or capital) gives about 3 m of reading distance.

| Line | Option A | Option B |
|---|---|---|
| Arabic name | ≈ 44 m | ≈ 32 m |
| English name | ≈ 21 m | ≈ 17 m |
| Tagline | — | ≈ 24 m |

- In option B the English line reads only at close range, below 20 m.
- Option B's tagline reaches about 24 m. Its name is slightly larger than in v01 B; it was not made smaller.

## Fonts and colours
- **Lettering on the sign:** Cairo 700 for the name and Cairo 600 for the tagline; Inter 600 for the English name. All are outlined.
- **Drawings and captions:** IBM Plex Sans Arabic. All fonts are SIL OFL.
- **Drawing check:** `check_arabic_pdf.py` returned PASS for both drawings, each on one A3 page.
- **Navy:** #102232, CMYK about 100/78/45/55, RAL 5011 or 5004.
- **Gold:** #D4A95F, CMYK about 12/32/72/2, Pantone 7562 C or 871 C.
- All colour references are suggestions.

## Mockups
- Each mockup is the client's photo with the sign warped onto the face. The rest of the photo is unchanged.
- Channel letters are shown with more depth than flat-cut ones.
- The caption is below the photo: the Arabic block comes first, then the English block. It covers three points:
  - this is a visualisation and the 250 × 60 cm size is assumed;
  - the logo is provisional;
  - the slab must be repaired before installation, and the cracks behind the sign are hidden in the image.
- I did not make a dusk or LED version.
