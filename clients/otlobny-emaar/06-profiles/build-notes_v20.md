# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v20

**Date:** 2026-11-17
**Author:** corporate-designer

v19 is untouched. Only p1 and p6 change. The book stays at 20 pages.

## p6 banner
**Image and frame**
- The client's 3:1 banner image (2172 × 724 px) is shown whole in a 297 × 99 mm frame.
- **Nothing is cropped and nothing is distorted.** It runs full bleed at 186 ppi.
- The copy is in `assets/mockups/`; the client's original file is untouched.

**Vision 2030 logo**
- The logo baked into the image misdraws «رؤية»: the final ta marbuta reads as a lam. Its emblem is also blurred, as in the earlier images.
- I painted it out into the dark palms. The clean image is `assets/derived/v20_client_riyadh-banner_clean.png`, made by `_work/v20/riyadh_banner_v20.py`.
- In its place is the official white version (`v19_vision2030_white.png`), at the same position and size as the baked-in logo: source box x 1891–2118 px, about 31 mm wide.
- It sits directly on the photo with no plate and no extra shading. The dark palms give enough contrast on their own.
- 300 dpi check: `_work/v20/check300_p06_vision2030.png`. Before and paint-out views: `_work/v20/check_logo-corner_*.png`.

**Content below the banner (re-fitted)**
- Space from the banner to the title: 3 mm (was 6).
- Page title one small step down: Arabic 31 → 25 pt, English 21 → 17.5 pt.
- Kicker gap reduced.
- Card spacing: card padding 2 → 1.6 mm, card row pitch 38 → 33.8 mm, gap between cards 8 → 6 mm.
- English card description line spacing 1.45 → 1.36.
- Card text sizes are unchanged. The Arabic card descriptions keep line spacing 1.6.
- The last card ends at 191.1 mm. The footer is at 197 mm, so the gap is 5.9 mm.

## p1 cover hero
- The client's rebar worker photo replaces the two engineers. The copy is in `assets/mockups/`.
- The engineers image is no longer used anywhere in the book.
- **Framing:** it sits in the v19 geometry, which reproduces the original cover. The crop is source x 449–1205 at full height.
  - Inside the diamond: helmet, face, the reaching arm and glove, and the rebar verticals and cage.
  - The vest and lower body are cut by the diamond's lower-left edge, as on his original cover.
- **Effective resolution: 140 ppi.**
- **Light blue tint:** a royal-blue tone (navy shadows, royal #3758B0 mid-tones, cool white highlights) blended over the photo at **30%**.
  - I tried 25%, 30% and 35% (`_work/v20/cover_hero-tint_*.png`). At 25% the sepia still showed. At 35% the photo went grey-cold. At 30% it reads cool and natural, clearly lighter than the 86% navy on the side shapes.
- Geometry, side shapes, their overlay and the left text column are unchanged from v19.
- Comparison with his original cover: `_work/v20/compare_original-vs-v20_p01.png`.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: PASS.
- Forbidden strings: 0.
- Bookmarks: 2, 3, 4, 6, 13, 14, 17, 19.
- No image appears on two pages.
- p1 and p6 viewed at full size; the logo corner checked at 300 dpi.
