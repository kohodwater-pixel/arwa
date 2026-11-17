# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v19

**Date:** 2026-11-17 · **Author:** corporate-designer
v18 is untouched. 20 pages. This version changes only p1 and p6.

## p1 Cover: the client's original arrangement, measured and reproduced
**How it was measured.** Shape edges were read from `01-brief/assets-received/pages/p-01.png` (1287 × 910 px) by scanning rows for the white/non-white boundary, then converted at 297/1287 mm per px. Fractions below are of page width (w) and height (h).

| Shape | Original (measured) | v19 |
|---|---|---|
| Large diamond, left vertex | (0.537 w, 0.337 h). Edges at 45°; right and top vertices off the page | Same vertex and edges (159.5 mm, 70.8 mm); half-diagonal 160 mm, so it bleeds right, top and bottom |
| Top partial, centre on the top edge | (0.568 w, 0), half-diagonal 0.155 w | Same: centre (168.7, 0), half-diagonal 45.9 mm |
| Small diamond | centre (0.618 w, 0.734 h), half-diagonal 0.127 w | Same: centre (183.5, 154.2), half-diagonal 37.6 mm |
| Bottom-right partial, centre on the bottom edge | (0.789 w, 1.0 h), half-diagonal 0.173 w | Same: centre (234.2, 210), half-diagonal 51.5 mm |
| Gutters | 9–14 mm, uneven as in the original | Same, because the positions are copied |
| Corner radius | about 18–21 mm on the large shape; smaller on the others | 18 mm on the large shape; 7.5 mm on the others |

- **Overlay:** `_work/v19/overlay_cover_v19-on-original-p01_50pct.png` is my render over p-01 at 50%. The edges of all four shapes coincide. `compare_original-vs-v19_p01.png` shows the two side by side.

**Content of each shape**
- **Large diamond:** the two engineers in full colour, 88 ppi.
  - The visible part of the diamond is a tall narrow area (137.5 × 210 mm). Each triptych panel is only 716 px wide.
  - The crop starts at the panel's left edge, so the pointing engineer, his gesture and the crane read well. The second engineer is only partly in frame at the right.
  - The pointing engineer's face is partly behind the diamond's lower-left edge. Only the helmet and the gesture read fully. This is a consequence of the original geometry.
- **Small diamond:** the window cleaner, with his back logo inside the shape. 186 ppi.
- **Top partial:** the landscaping panel. 198 ppi.
- **Bottom-right partial:** navy→royal gradient fill. Every client image is already used on another page.
- **Overlay strength:** the three side shapes carry the navy overlay at 86%, the same strength as v16.

**Left column**
- Lockup v02 (colour), 80 mm wide.
- Clear space: the top partial's nearest edge is about 33 mm from the lockup box, far above the 5.5 mm minimum, so the lockup did not need reducing.
- "Company Profile" sits at the bottom rule, followed by otlobny.net · «المملكة العربية السعودية».

## p6 Services banner
- **Frame:** fixed at **297 × 85 mm (3.5:1)**, full bleed. An image made at 3.5:1 drops in edge to edge with no crop.
- **Current image:** the client's wide Riyadh image, copied as a PNG to `assets/mockups/`. The original .webp is untouched.
  - Cover-cropped to source rows y 15–504 of 1708 × 921, at 146 ppi, with no distortion.
  - The Kingdom Centre crown sits inside the frame with sky above; the buildings sit at the lower edge.
- **Malformed green wordmark:** painted out into the sky. 300 dpi check: `_work/v19/check300_p06_top-right.png`.
- **Vision 2030 logo:** built in white from the **official file**. I did not use the copy baked into the image.
  - Reason: at full resolution, the baked-in «رؤية» is misdrawn (its final ta marbuta reads as a lam, «رؤيل») and the emblem's squares are blurred. Evidence: `_work/v19/check_baked-in-vision-logo_not-used.png`.
  - Recolour method: only the neutral grey parts were turned white (lettering, palm, swords). The emblem's colours are kept, as in the client's image.
  - File: `assets/derived/v19_vision2030_white.png`.
  - Placement: directly on the photo with no plate, 44 mm wide, clear space 6.6 mm (15%) from the right and bottom edges.
  - A soft navy radial shade sits behind that corner only, for legibility over the lit buildings.
  - 300 dpi check: `_work/v19/check300_p06_vision2030.png`.
- **White tab:** the v17/v18 white tab with the grey logo is removed.
- **Cards:** text sizes are unchanged. The last card ends at 189.8 mm and the footer starts at 197 mm, a gap of 7.2 mm.

## Checks
- **Arabic check:** `check_arabic_pdf.py --expect "اطلبني إعمار"` PASS.
- **Forbidden strings:** 0.
- **Bookmarks:** 2, 3, 4, 6, 13, 14, 17, 19.
- **Images:** none is used on two pages.
- **Pages viewed:** p1 and p6 at full size, plus both 300 dpi crops and the overlay.
