# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v08

**Date:** 2026-11-14 **Author:** corporate-designer **Status:** DRAFT v08, covering review_v07_r4 and the client's confirmation of the Dar Al Taqwa scope. Not approved by the client. v07 is untouched. **20 pages.**

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v08.pdf` and `.html`
- `_work/build_profile_v08.py`. Run `_work/v08/composite_v08.py` first; it uses the v07 GrabCut masks from `_work/v07/`.
- `_work/v08/composite_v08.py`, which writes `assets/derived/v08_logistics_fleet-composite.jpg` (3440 × 1280 px).
- `_work/v08/check300_*.png`: 300 dpi crops of every replaced logo, `check300_all.png` (all crops together) and `check300_reference_wordmark.png`.
- `_work/finish_pdf_v08.py`, `_work/contact_v08.py`, `_work/contact_v08_part1/2.png`, `_work/preview_v08/`, `_work/build_v08.log`, `_work/check_v08.log`
- `content-outline.md`: v08 status block added (Dar Al Taqwa scope confirmed). The previous text is in `_archive/content-outline_before-v08_2026-11-14.md`.

## 1. Dar Al Taqwa text (client confirmed 2026-11-14)
- p16 now matches the Chamber page: number, title, «قدمت «اطلبني إعمار» خدمات الصيانة والنظافة لفندق دار التقوى.» / "OTLOBNY Emaar provided maintenance and cleaning services for Dar Al Taqwa Hotel.", and scope chips صيانة، نظافة / Maintenance, Cleaning.
- The two photos were reduced so the text column is 95 mm wide:
  - entrance 37 × 66 mm, 230 ppi
  - room 99 × 66 mm, 197 ppi
- This resolves r4 m5.

## 2. p12 composite: the real wordmark on every vehicle (r4 M1, m1, m2, m3)
**Method**
- Worked at 2× the source resolution. The composite is 3440 px across 297 mm, about **294 ppi** (147 in v07).
- On each surface:
  - The AI-drawn logo is painted out with the surface's own paint: a membrane fill from the surrounding panel, plus matched grain.
  - The real wordmark (SVG from `04-identity/02-logo/`, rendered with cairosvg) is warped with `cv2.getPerspectiveTransform` onto the surface plane.
  - It is shaded by the local light ratio of the painted-out panel, so it reads as printed rather than pasted.
- Versions follow system.md: reversed (green + white) on the navy truck box and the black delivery box; colour on the white cab and the car door.
- Truck box: the plane was fitted to the box's four corners. The logo is centred where the AI logo was and sized to it, so its baseline runs along the panel's perspective.

**Each surface at 300 dpi, compared with the SVG** (`_work/v08/check300_*.png`)

| Surface | Result | Honest judgement |
|---|---|---|
| Truck box side | real wordmark, reversed | Correct letterforms. Perspective follows the panel and the baseline runs with the top rail. Reads as printed; no halo. |
| Truck cab front | real wordmark, colour | Straight and centred on the grille panel; matches the cab's light. Good. |
| Truck cab door | real wordmark, colour | Fits the door plane between window and handle; slight perspective. Good. |
| Car door | real wordmark, colour | Follows the door's slope; the shading carries the door's soft gradient. Good. A faint lighter patch from the paint-out is visible only at 300 dpi. |
| Delivery box | real wordmark, reversed | Near-frontal, crisp; matches the box's flat black. Good. |
| Scooter side panel | **painted out, no logo** | The curved, glossy panel could not take a flat warp cleanly, so per the ruling it is a clean unbranded panel. The old logo's colour cast was neutralised. |

No surface looked pasted or skewed after placement, so no further logos were painted out.

**Other fixes**
- **m1:** the truck box mask was completed with a polygon on the box's real edges. The rear-corner step is gone, and the silver top rail and the rear trim are restored from the source.
- **m2:**
  - The towers seen through the cab's far window are replaced with dark glass.
  - The truck's under-chassis shadow is softer (0.28 instead of 0.45).
  - The car and scooter have firmer contact shadows plus a soft ambient shadow.
  - Below the bumper line the truck keeps only its two wheels, so there is no asphalt slab.
- The client mockups are still not regraded (m9). The «صورة توضيحية» / "Illustrative image" label stays.

## 3. List wraps (r4 m4)
- p8 and p9 use a wider English column (1.12 / 0.88).
- p9's lift item keeps "lift systems" together.
- Result: no three-line items and no orphan words on pp8–9. p11 keeps the wider Arabic column it needs; the other pages use 0.95 / 1.05.

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**. 20 pages; Tajawal and IBM Plex Sans, no fallback font; 4,535 Arabic characters.
- **Forbidden strings:** «شهد», Shahd, «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp, TAIBA, THERMO, COAST and 157th all appear 0 times. No harakat.
- **Dar Al Taqwa sentence:** present once in each language (checked in the HTML; PDF text extraction splits the line).
- **Contents, folios and bookmarks** checked against the real pages:
  - contents: About 03, Vision 04, Services 06, Why 13, Work 14, Partners 17, Contact 19
  - folios 02–19 match their pages, and every kicker number matches its section
  - bookmarks point to pages 2, 3, 4, 6, 13, 14, 17, 19, 20
- **No image on two pages:** the build log reports "none".
- **Image resolution (ppi):** as in v07, except:
  - p12 composite: about 294
  - p16 entrance: 230
  - p16 room: 197
- **Visual check:** all 20 pages viewed on the contact sheets. pp8, 9, 12 and 16 also viewed at full preview size, and the composite viewed at native size and in the 300 dpi crops.

## Open
- **p11 uniforms:** the logos there are very small and are accepted as supplied (ruling).
- Still waiting on the client:
  - "Single contract" line on p13
  - Bus-shelter original photo
  - Official partner logos (The End cut)
  - Their own photographs
- Also open:
  - Native Arabic proofread
  - Second-viewer check
  - Accessibility tagging
