# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v14

**Date:** 2026-11-15
**Author:** corporate-designer
**Input:** client feedback on v13 (brand-context.md, last 2026-11-15 entry)
**Standing rules (unchanged):** no captions, no credits, no "draft".
v13 is untouched. 20 pages.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v14.pdf` and `.html`
- `_work/build_profile_v14.py`: use `COVER_TRIAL=A|B|C` to rebuild a cover trial and `VEIL=` to change the tint strength.
- `_work/finish_pdf_v14.py`, `_work/contact_v14.py`, `_work/contact_v14_part1.png`, `_work/contact_v14_part2.png`, `_work/preview_v14/`, `_work/build_v14.log`, `_work/check_v14.log`
- `_work/v14/`: cover trials (described below).
- `assets/mockups/photo_manpower-hospitality-waiter.png`: copy of the client's upload. The original is untouched.

## 1. Manpower Supply (p11)
- **Double diamond:** the client's hospitality-waiter image, in full colour, crop centre x = 0.54. Face, apron and tray all sit inside the diamond. 163 ppi.
- **Cluster:**
  - catering stock tile (245 ppi)
  - the client's cleaning-team mockup (368 ppi)
  - one navy diamond
- The cluster uses the same structure as the contracting and maintenance pages.
- The tea-pouring photo is removed from the book (0 occurrences in the HTML).

## 2. Cover (p1)
**Light blue veil.** Every cover photo gets a soft wash of #2B458A (between navy and royal) at **18%**:
- It is weighted to mid-tones and shadows, so it is lighter on highlights.
- A small contrast lift compensates for the wash.
- I chose 18% by eye after comparing 15% and 20%. At 20% the photos started to look blue-cast; at 15% the tint was barely visible.
- Faces and skies stay clean.
- Hero and small frames get the identical treatment.

**Layout trials:**

| Trial | Layout | Result |
|---|---|---|
| **A (chosen)** | A 2×2 hero (127 mm) centred in the right area. Two small diamonds on its left: window cleaner on top, landscaping below. Two on its right: navy gradient and royal blue, both bleeding off the right edge. | Symmetric "two and two". The hero is now 143 ppi, sharper than v13's 94. The green accent diamond is removed. |
| B (rejected) | v13's large 3×3 hero, with two diamonds on each of its left edges (cleaner, navy, landscaping, royal). | Still reads as one-sided, and the hero stays at 94 ppi. File: `rejected_cover_trial_B_large-hero-left-pairs.png` |
| C (rejected) | As A, but the two right-hand frames hold unused library stock (Gulf site workforce, racking aisle). | Busier, and brings stock photos back to the cover after the client replaced them with his own. Kept as an alternative to show the client if asked. File: `rejected_cover_trial_C_four-photos.png` |

`superseded_cover_trial_A_first-geometry.png` shows the first A attempt, with the right pair misaligned. That geometry was fixed.

**Frames:**
- Left side: window cleaner (229 ppi) and the landscaping panel (220 ppi).
- Right side: navy gradient and royal blue. No other client image is free to use without repeating one.

**Clear space:** the left diamonds start at x = 113.3 mm and the lockup ends at x = 98 mm, so the gap is 15.3 mm (X = 5.5 mm). "Company Profile" stays at the bottom rule.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**.
- Forbidden strings: all 0, the same list as v13.
- Bookmarks point to pages 2, 3, 4, 6, 13, 14, 17 and 19.
- No image appears on more than one page (build log reports "none").
- p1 and p11 viewed at full preview size; all pages viewed on the contact sheets.
