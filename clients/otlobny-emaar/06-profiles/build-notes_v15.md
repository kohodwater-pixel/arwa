# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v15

**Date:** 2026-11-15
**Author:** corporate-designer
**Scope:** cover only. The client rejected the v14 cover shape. Every other page is identical to v14, including the waiter on p11.

## Cover (p1)

**Arrangement.** The v13 arrangement is back, unchanged:
- Same lattice and the same 3×3 hero (the two engineers), bleeding off the right edge.
- Hero is the same size and position as in v13.
- Lockup top-left; "Company Profile" at the bottom rule.

**Frames removed.** Three of v13's frames are gone:
- the partial top diamond, C(-1,0);
- the pale tint diamond, C(-1,2);
- the small green accent.

**Frames kept:**
- window cleaner, C(-1,1);
- landscaping, C(0,3);
- navy gradient, C(1,3);
- royal blue, C(2,3).

**Side images.** Both side photos get a brand-blue overlay: a navy → royal → periwinkle tone blended over each photo at **70%**.
- At 45–55% they only looked slightly cool. At 80–100% they turned into a duotone.
- At 70% they read clearly as blue-toned and are still easy to read.
- Comparison renders are in `_work/v15/`.

**Hero.** Full colour, with no veil and no tint.
- I kept v13's hero size. The smaller hero would have changed the look, which this round was told not to do. The hero therefore stays at 94 ppi (soft when zoomed).

**Clear space.** The geometry matches v13, so the nearest diamond is still 9.6 mm from the lockup, against an X of 5.5 mm.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v15.pdf` and `.html`
- `_work/build_profile_v15.py` (environment variables: `COVER_TRIAL=D` default, `SIDE_BLUE=0.70`)
- `_work/finish_pdf_v15.py`, `_work/contact_v15.py`, `_work/contact_v15_part1/2.png`, `_work/preview_v15/`
- `_work/v15/`: overlay comparison renders and `compare_v13-vs-v15_p01.png`
- `_work/build_v15.log`, `_work/check_v15.log`

## Checks
- `check_arabic_pdf.py`: PASS
- Forbidden strings: 0
- Bookmarks: correct
- No image appears on two pages
- p1 viewed side by side with v13 p1: arrangement matches
