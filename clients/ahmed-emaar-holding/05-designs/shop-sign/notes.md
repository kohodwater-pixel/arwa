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

---

# v03 — raised letters directly on the wall, no panel (2026-11-23)

**Status:** v03 is a new version for the client's change: "no background panel". The v02 files stay in place as the alternative with a panel. Nothing was archived this round.

## What changed
- Content is option A only: the mark, «أحمد إعمار القابضة» and AHMED EMAAR HOLDING.
- There is no tagline and there are no corner accent lines.
- The lettering is **250 cm wide overall, mark included**, by **44.6 cm** high. That leaves about 15–25 cm of clearance on each side to the exposed rebar and the column stubs (an estimate from the photo, pending site measurement).

## Placement
- The **whole lockup sits on the wall above the crack line**:
  - letter bottoms are about 60 cm above the slab's lower front edge, which is about 35 cm above the crack (the crack is about 25 cm above that edge);
  - letter tops are about 105 cm above that edge, which leaves about 30 cm below the top of the wall.
- Why I chose this:
  - the slab-edge face (about 30–40 cm) is the damaged strip, with cracks, spalling and exposed rebar;
  - splitting the lockup across the crack would put letters on that strip or straddling it;
  - the wall above is flush with the slab edge and has about 1 m of height. It is not fully sound: there is a vertical crack near the mark and the «أ», and there are pock holes under HOLDING.
- All heights are estimates from one photo. The three site measurements are listed on the drawing.

## Sizes and strokes (cm, real size)
- **Mark:** 44.4 high × 41.9 wide (re-measured from the artwork after the swoosh tip was cut). Bars are 4.2–4.7 wide and the thinnest part of the arch is 3.3.
  - The swoosh tip is **blunted** where it would be thinner than about 1.5. This is a fabrication change to the provisional trace.
- **Arabic name:**
  - alef 17.0; letter-body height 12.0; full extent 31.2; width 196.5;
  - stem 3.2; horizontal stroke 2.8.
  - There are 8 small separate pieces, each pinned separately: 2 hamzas (5.8 × 5.2) and 6 dots (3.1 × 2.7).
- **English name:**
  - cap height 8.5; width 196.5; tracking 0.26 em (exactly 0.256);
  - **Inter ExtraBold (800)** instead of 600, so that the horizontal bars reach about 1.5 cm;
  - stem 2.1.
- **Spacing:** Arabic baseline to English cap top 11.9 (lowest hamza to English cap top 4.5); mark to lettering 11.6.
- **Every stroke is at least 1.5 cm.** Sharp corners are to be radiused by the fabricator. The small dots (about 3 cm) could be made as solid or shallower pieces.
- **Piece count:** mark 3, Arabic 16, English 17.
- **Suggested depth:** mark and Arabic 5 cm, English 3 cm.
- **Stand-off from the wall:** 15–20 mm.
- **Fixing:** threaded studs with chemical anchors into sound concrete only, positioned with a 1:1 drilling template from the fabricator. The wall above the slab may be blockwork, so the substrate has to be identified on site and the anchor chosen to suit.

## Weld checks (same as v02)
- Each element is one outline: 3 paths in total.
- The file has no stroke, no clipPath and no live text.
- The nonzero and evenodd fill rules give 0 differing pixels.
- Each text line, and the blunted mark, matches the raw overlapping parts at 0 differing pixels.

## Contrast on the real wall
- The wall was sampled from the site photo:
  - sunlit plaster ground: about #F2F0EC;
  - rose motif: about #B6AAA8;
  - shaded soffit: about #605146.
- WCAG ratios, comparing the swatch colour with the photo pixels (an indicator only):

| Letter colour | Sunlit ground | Rose motif | Shaded soffit |
|---|---|---|---|
| Gold #D4A95F | **1.9** | **1.0** | 3.5 |
| Navy #102232 | **14.2** | 7.2 | 2.1 |
| Dark bronze #4A3A28 | 9.6 | 4.8 | 1.4 |
| Gold face on a navy edge | edge vs wall 14.2; gold vs navy 7.4 | | |

- The letters sit on the **sunlit** wall, so the sunlit columns are the ones that matter.
- The shaded-soffit figures only show that the soffit is much darker than the wall. They are not where the letters will be.

## Which variant reads (honest view)
- **V1, all gold:**
  - The ratio is 1.9 against the plaster and about 1.0 against the rose motif. Gold almost disappears into the pattern.
  - In the mockup it reads mainly because of the dark returns and the cast shadows. These vanish in flat light (overcast, dusk, midday sun straight on).
  - It does not meet even the 3:1 large-text threshold.
- **V2, navy names with a gold mark:** best legibility (14:1). It keeps gold in the mark, but the lettering is no longer gold.
- **V3, gold faces with navy returns and a navy backer edge:**
  - It keeps the gold identity.
  - The navy edge outlines every letter against the wall (14:1), and gold on navy is 7.4:1.
  - It reads close to V2 at street distance, at a higher fabrication cost (backer plates).
- **Recommendation:**
  - V3 if the client wants the letters to stay gold.
  - V2 if legibility comes first.
  - Do not use V1 on this wall.

## Viewing distance (rule of thumb: about 3 m per 1 cm of letter height)
- **Arabic:** about 36 m, measured on the 12.0 cm letter-body height, not on the alef.
- **English:** about 26 m.
- **Intended viewing distance:** 20–30 m.

## v02 minors from review r2
- **Range order:** in the v02 Arabic note, "2.5–3.0 م" displays reversed, as 3.0–2.5. Fixing it would mean re-issuing v02, so I did not.
  - The v03 drawing isolates every range and number as left-to-right text, so the order is correct there.
  - v02 still carries the reversed range.
- **Python cache folders:** `__pycache__/` is now ignored via `.gitignore` in both `_work` folders.

## v04 (review r3): drawing and V1 mockup only
- New files:
  - `letters-on-wall-technical-drawing_ar-en_v04.pdf`
  - `letters-on-wall-mockup-site-v1-gold_ar-en_v04.png`
- Their v03 versions are in `_archive/`. The artwork, V2 and V3 are unchanged at v03.
- **Drawing corrections:**
  - The mark is 44.4 × 41.9 cm, not 44.7 wide.
  - The [8] mark-to-lettering gap is 11.6 cm, not 8.8. Both values were re-measured from the v03 artwork paths.
  - English tracking is 0.26 em.
  - The crack is given everywhere as about 25 cm above the slab edge, with the letters about 35 cm above it.
  - The minimum-stroke row now says sharp corners are to be radiused.
  - The fixing row now covers the substrate (the wall may be blockwork).
  - The placement note now lists the vertical crack and the pock holes on the wall above.
  - Side clearance is given as about 15–25 cm, pending measurement.
  - The small dots are suggested as solid or shallower pieces.
- **V1 caption:** now says, in Arabic first, then English, that gold measures about 1.9:1 against the sunlit plaster, reads mainly through its shadows, and is not recommended.
- **Still open:** the V2 and V3 mockups were built with the old mark-width figure, which only enters the depth-offset estimate. The shift this causes is under 0.1 cm and is not visible.
