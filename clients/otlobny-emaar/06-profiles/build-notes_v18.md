# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v18

**Date:** 2026-11-17 · **Author:** corporate-designer

v17 is untouched. Only p6 changes. 20 pages.

## p6 banner
- **New image.** The client's Riyadh night skyline replaces the Prophet's Mosque umbrella photo, which leaves the book and is not moved to another page.
  - The client file is copied to `assets/mockups/photo_riyadh-night-skyline_with-logos.png`; the original is untouched.
  - Full colour, no grade or tint.
- **Malformed green wordmark (top right).** Painted out into the sky with `_work/v18/riyadh_v18.py`. The fill comes only from the surrounding sky pixels, with grain added to match.
  - Before and after: `_work/v18/check_top-right_before.png` and `_after.png`.
  - At 300 dpi on the page the corner shows only clean sky: `_work/v18/check300_p06_top-right.png`.
- **Vision 2030: option (a).**
  - The baked-in white logo sits in the bottom 25% of the image. Any crop that keeps the Kingdom Centre's arch at the top leaves it out, so I could not use option (b).
  - The official file is used unaltered on the white tab, exactly as in v17: 36 mm wide, clear space 5.4 mm, at the banner's lower-right corner.
  - 300 dpi check: `_work/v18/check300_p06_vision2030.png`.
- **Banner size.** Raised from 68 mm to **82 mm** (39% of the page height). Image runs full bleed at 297 mm, **127 ppi**. Crop is source y 30–441.
  - **What shows:** the tower top to bottom, the lit street light, the purple dusk sky, the crane and the buildings on each side.
  - **What does not:** the lit road. At full width, even a 45% banner shows only 47% of the image height, so the tower's arch and the road cannot both fit. I kept the tower and the sky.
  - The 86 mm trial pushed the Manpower card to 1 mm from the footer, so I rejected it (`_work/v18/p6_trial_86.png`).
- **Spacing below the banner.** Tightened; card text sizes are unchanged.
  - Title gap: 10 → 7 mm.
  - Cards: start 22 mm under the title; row pitch 41 → 38 mm; padding slightly reduced.
  - Last card ends at 188.8 mm. The footer is at 197 mm.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**.
- Forbidden strings: 0.
- Bookmarks: 2, 3, 4, 6, 13, 14, 17, 19.
- No image used on two pages.
- The umbrella panorama is no longer in the HTML.
- p6 viewed at size; both 300 dpi crops viewed.
