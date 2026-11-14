# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v07

**Date:** 2026-11-14  **Author:** corporate-designer  **Status:** DRAFT v07. It covers the client's feedback on v06 (brief addendum 7) and the minors from review_v06_r3. Not approved. Every v06 file is untouched. **20 pages.**

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v07.pdf` (11.3 MB) and `.html`.
- `_work/build_profile_v07.py`: the generator. Run `_work/v07/cutouts_v07.py` and then `_work/v07/composite_v07.py` first.
- `_work/v07/cutouts_v07.py`: cuts the vehicles out of the client mockups with OpenCV GrabCut (opencv-python-headless, installed for this). It uses rectangle and hint boxes plus zone clean-ups, and keeps only the two wheels below the truck's chassis line. Check images are `_work/v07/*_check.jpg`; the masks are `*_mask.npy`.
- `_work/v07/composite_v07.py`: builds `assets/derived/v07_logistics_fleet-composite.png` (1720 × 640 px). There is a 200% view at `_work/v07/composite_200pct.png`.
- `assets/photos/dar-al-taqwa-hotel-room.png`: lossless PNG converted from the client's AVIF (768 × 512) with Pillow. The original in `_originals/` is untouched.
- `_work/finish_pdf_v07.py`, `_work/contact_v07.py`, `_work/contact_v07_part1/2.png`, `_work/preview_v07/`, `_work/build_v07.log`, `_work/check_v07.log`.

## Page map (20)
1 cover · 2 contents · 3 about · 4 vision + mission · 5 goals · 6 services overview · 7–11 services · **12 logistics (with the composite)** · 13 why us · **14 work 01 bus shelters · 15 work 02 Madinah Chamber · 16 work 03 Dar Al Taqwa** · 17–18 partners · 19 contact · 20 back cover and credits.

Contents now reads: Why Us 13, Our Work 14, Partners 17, Contact 19. Bookmarks match.

## 1. Dar Al Taqwa page and the works family
- **Works layout, used on all three pages:** a tint panel holds the image(s), vertically centred. On the other side is a text column with the kicker, number, Arabic and English titles, then text and scope where confirmed. The panel side alternates: left on p14, right on p15, left on p16.
- **p16 Dar Al Taqwa:**
  - Entrance photo at 43.8 × 78 mm (194 ppi) and room photo at 117 × 78 mm (167 ppi), side by side at the same height.
  - Caption «صور مقدمة من العميل» / "Photographs supplied by the client".
  - Title «فندق دار التقوى» / "Dar Al Taqwa Hotel".
  - No text and no scope chips: the scope is unconfirmed.
- **p15 Madinah Chamber:** the rendering at 110 mm (149 ppi), with text and scope.
- **p14 Bus shelters:** unchanged (133 ppi).

## 2. Logistics: one composed image, folded into p12
- **The composite** uses the client's own mockups:
  - The car, scooter and rider are cut out as one group from the car/scooter scene, keeping their original relative positions, at 62%.
  - The box truck is cut out of the front three-quarter view at 100%. Only the truck is used; the Riyadh tower and the street behind it are removed with the background.
  - Both stand on one shared floor (white fading to a pale brand tint) with soft contact shadows. The truck sits slightly further back.
  - Every logo is complete. The client images are not regraded (ruling m9).
- **Checked at 200%:** no seams or halos. Remaining at that zoom:
  - The truck's windscreen still shows faint towers through the glass, from the source image.
  - A few tiny grey flecks at the scooter's tail.
  - Neither is visible at page size.
- **Why fold it into p12:** logistics becomes one strong page instead of two, the book stays at 20 pages, and the second work can have a page of its own.
  - p12 layout: title and intro on top, the composite as a full-width band (297 mm, 147 ppi), the «صورة توضيحية» / "Illustrative image" label on the floor, and the four services as one bilingual strip below (English left, Arabic right).
  - The racking aisle, which used to be on p12, moved to the cover.

## 3. Review r3 minors
- **m1:** bilingual list columns are now 0.95 / 1.05. Only manpower keeps 0.86 / 1.14, where the Arabic needs the room.
- **m2:** superseded by the new p16.
- **m3:** the cover's tower tile is replaced by the warehouse racking aisle (logistics). The cover now shows contracting (hero), logistics, cleaning, landscaping and manpower. The tower image is no longer used and has dropped out of the credits automatically.

## Images (no source on more than one page; confirmed by the build log)
| Page | Images and ppi |
|---|---|
| p1 | steel erector 202 · racking aisle 283 · rope-access glass tower 284 · Riyadh palm park 319 · Gulf workforce 319 |
| p3 | Madinah plaza 327 |
| p6 | Madinah panorama 227 |
| p7 | glass facade 416 · screeding 245 · surveyor 246 |
| p8 | Doha walkway 276 · dry planting 276 |
| p9 | HVAC 333 · rooftop AC 245 · distribution board 460 |
| p10 | rope-access window cleaner 244 · mop and trolley 245 |
| p11 | waiter 245 · catering 245 · client team mockup 368 |
| p12 | logistics composite 147 at 297 mm |
| p14 | bus shelter 133 |
| p15 | Chamber rendering 149 |
| p16 | Dar Al Taqwa entrance 194 · room 167 |

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: PASS, 20 pages, Tajawal and IBM Plex Sans, no fallback, 4,467 Arabic characters.
- Forbidden strings all 0, including «شهد», Shahd, «الشركة المختارة», the old Dar Al Taqwa scope sentence, the demoted authors and ianmunroe. No short-vowel marks, no Arabic-Indic digits.
- Labels: «صورة توضيحية» on pp11, 12 and in the p20 note; client-photo captions on pp14–16.
- Contrast unchanged from v05/v06.
- All 20 pages viewed on the contact sheets; pp12, 14, 15 and 16 also at full preview size; the composite at 200%.

## Open
- Rights for the room photo (from a booking site) are the client's responsibility, as he instructed; it is recorded in brand-context.
- Dar Al Taqwa scope, the "single contract" line, the original bus-shelter file, official partner logos, the client's own photographs, a native Arabic proofread, and a second-viewer check are all still open.
