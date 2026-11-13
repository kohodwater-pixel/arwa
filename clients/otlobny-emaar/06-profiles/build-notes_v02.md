# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v02

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-13  **Author:** corporate-designer
**Status:** DRAFT v02 for the Creative Director and the quality-reviewer. Not approved by the client. v01 files are untouched.

## 1. Files

| File | What it is |
|---|---|
| `otlobny-emaar_company-profile_screen_ar-en_v02.pdf` | 20 pages, 297 × 210 mm, screen PDF (sRGB), 6.7 MB |
| `otlobny-emaar_company-profile_screen_ar-en_v02.html` | Editable source (assets linked from `assets/`) |
| `_work/build_profile_v02.py` | Generator: v01 code plus a "v02" section that redefines the changed pages and writes the JPEG crops |
| `_work/retouch_mockups_v02.py` | Removes the wrong descriptor lines from the client's four mockups; writes `assets/derived/mockup_*_retouched_v02.png`, the five truck crops, and before/after 4× sheets in `_work/retouch_v02/` |
| `_work/finish_pdf_v02.py` | Title, `/Lang ar`, R2L reading direction, 7 bookmarks |
| `_work/preview_v02/`, `_work/contact_v02_part1-3.png` | 110 dpi previews of the final export and contact sheets |
| `assets/derived/v02_*.jpg` | 17 JPEG crops placed in the PDF (native pixels, never upscaled) |

## 2. What changed from v01

- **Image-led.** Full-bleed cover (the client's car / scooter / building mockup under a navy gradient, colour lockup on a white chamfered panel); contents with a full-height photo panel; vision + mission on one page around a full-height centre photograph; every service page has a full-width photo band (96–128 mm tall) with the title over a navy gradient; a new logistics picture page (three truck views full-bleed plus the delivery rider); works frames enlarged to 127 × 105 mm; partners enlarged.
- **All four client images used, large:** cover (car/scooter/facade), cleaning (team), logistics (two truck views on p12; front/side/rear trucks and the rider on p13).
- **Page map (20):** 1 cover · 2 contents · 3 about · 4 vision & mission · 5 goals · 6 services overview · 7–12 six services · 13 logistics in pictures · 14 why · 15–17 works · 18–19 partners · 20 contact / back cover. Contents page and folios updated; services start on p6.
- **Client answers applied:** logistics confirmed — new intro, four sub-services (Delivery, Goods transport, Storage, Vehicle rental), overview summary «التوصيل ونقل البضائع والتخزين وتأجير المركبات» / "Delivery, goods transport, storage and vehicle rental."; draft pill removed. Website `otlobny.net` as a normal linked row; the pill and otlobny.co/.com options removed. No WhatsApp row; nothing taken from the website. Same wordmark.
- **Mockups:** wordmark alone, nothing written under it (client decision). The interim composited descriptors were withdrawn; the code is kept as `COMPOSITES_WITHDRAWN` for the record.

## 3. Art-director review of v01 — what was adopted

Adopted: partners grid (title in the title zone at 32/27 with "01 / 02"; horizontal hairlines at y 56, 98.5, 141, 183.5; 15 logos in 5 columns, 12 in 4; per-logo sizes from section 3.5; tier B ≥ 100 ppi, tier C ≥ 80 ppi); works pages (127 × 105 frame, the review's crops with the bus-shelter left edge moved to 0.41 to exclude the pavement debris, project index deleted, chips bottom-aligned at y 158.5 inside the side blocks); "2021" at 28 pt and CR at 22 pt; first table rule periwinkle; Arabic optically centred in pills; contact block on x 41–256, lockup 40 high, title 26/22, rows pitch 15 with 20 pt values, sparkle band centred; photographs down to 110 ppi.

Set aside because of the client's instruction ("visual pleasure", use my images): the list-only service template and the withdrawal of imagery from service pages; the restrained diamond cover; the vision/mission statement pages at 24/19 pt (vision and mission are paired on one page with a photograph instead, at 16.5 / 13.5 pt); duotone — all photographs are now full colour, so the "lifted duotone" fix does not apply.

## 4. Images and effective resolution

| Page | Placed file | Source | Crop px (l,t,r,b) | Placed width | ppi |
|---|---|---|---|---|---|
| 1 | v02_cover_car-scooter-facade.jpg | mockup car/scooter/facade (retouched) | 29,0,1477,1024 | 297 mm | 124 |
| 2 | v02_contents_glass-facade.jpg | photos/glass-facade-cleaners | 296,0,743,876 | 107 mm | 106 |
| 4 | v02_vismis_office-cleaner.jpg | photos/office-cleaner | 1150,0,1495,873 | 83 mm | 106 |
| 7 | v02_svc_electrical-panel.jpg | photos/electrical-panel | 0,158,1240,575 | 297 mm | 106 |
| 8 | v02_svc_nursery-worker.jpg | photos/nursery-worker | 0,248,961,732 | 222 mm | 110 |
| 9 | v02_svc_glass-facade.jpg | photos/glass-facade-cleaners | 0,128,1237,661 | 297 mm | 106 |
| 10 | v02_svc_cleaning-team.jpg | mockup cleaning team (retouched) | 0,135,1536,787 | 297 mm | 131 |
| 11 | v02_svc_waiter.jpg | photos/waiter | 0,146,980,588 | 222 mm | 112 |
| 12 | v02_svc_truck-front34 / -rear34.jpg | truck collage views 1 and 2 (retouched) | 14,0,686,582 / 13,0,685,582 | 148 mm each | 115 |
| 13 | v02_gal_truck-front / -side / -rear.jpg | truck collage views 4, 3, 5 | full views | 83 / 128.5 / 82 mm | 132 |
| 13 | v02_gal_rider.jpg | mockup delivery rider (retouched) | 300,10,770,1010 | 52.6 mm | 227 |
| 15 | v02_work_15.jpg | photos/bus-shelter | 390,16,940,471 | 127 mm | 110 |
| 16 | v02_work_16.jpg | photos/chamber-building | 88,0,637,454 | 127 mm | 110 |
| 17 | v02_work_17.jpg | photos/shahd-hotel | 211,64,1033,743 | 127 mm | 164 |

Five placements are at 106 ppi, below the 110 aim (pp2, 4, 7, 9): the sources are 873–876 px tall / 1237–1240 px wide and full-bleed needs that. Viewed at fit-to-window they hold; on p8 and p11 the photo stops at 222 mm and a brand panel with the service icon fills the rest rather than enlarging further. riyadh-skyline not used; no Vision 2030 or Ajeer logo.

Truck view 1 is cropped at x ≤ 700 px of the collage so the Riyadh tower (from x 703) is excluded.

## 5. Mockup retouch — every patch

Method (final): inside each measured area only the old text strokes are replaced (pixels > 16 levels from the local 13 px median, grown 2 px; 9 levels / 3 px on the raised facade letters to include their shadows); wordmark pixels are detected (saturated blue/green, or bright white on the cart) and protected; the hole is filled by masked diffusion from the surrounding surface (vertical-weighted where seams or hinges run through), smoothed, given matching grain and feathered 2 px. Check: pixels changed outside the patch areas (+6 px) = **0** in all four images.

| Image | Area (source px) | Reason |
|---|---|---|
| cleaning-team | 323,329–356,339 / 532,314–579,325 / 752,313–804,325 / 958,318–1004,332 / 1197,324–1250,336 | Garbled descriptor under each of the five chest logos |
| cleaning-team | 1384,656–1470,671 | Garbled Arabic line on the cart panel |
| delivery-rider | 453,57–496,68 | Helmet logo descriptor |
| delivery-rider | 499,251–540,265 | Jacket chest descriptor |
| delivery-rider | 661,297–710,320 | Delivery bag: garbled Arabic and misspelt "OTLOBY … Co." |
| car-scooter-facade | quad 160,185 / 352,200 / 354,248 / 160,232 and 316,234–358,252 | Facade sign: «شركة لطليني اللصابة والنظافة» and "OTLOBIY Maintenance & Cleaning Co." (sloping with the perspective) |
| car-scooter-facade | 1253,144–1325,159 | Street banner descriptor. The slogan «خدمتك بجودة تهمنا» is correct Arabic and is kept (see open points) |
| car-scooter-facade | polygon 528,655 → 682,683 → 645,691 → 528,692 | Car door: old Arabic line and "OTLOBHY Maintenance & Cleaning Co."; shaped to spare the door crease |
| car-scooter-facade | 1361,514–1459,537 | Scooter top box descriptor |
| car-scooter-facade | quad 1222,683 / 1286,663 / 1288,675 / 1224,696 | Scooter side panel, slanted descriptor |
| logistics-trucks | 143,355–223,378 / 357,352–402,370 | View 1 cab front and cab door |
| logistics-trucks | 580,292–696,335 | View 1 box side: «شركة اطلبني الخدمات اللوجستية» / "OTLOBY Logistics Services Co." |
| logistics-trucks | 986,315–1089,364 and 1040,344–1066,362 | View 2 box side (and two leftover dots) |
| logistics-trucks | 1228,293–1383,336 | View 2 rear doors |
| logistics-trucks | 321,795–462,831 / 64,840–111,855 | View 3 box side and cab door |
| logistics-trucks | 850,826–933,851 / 1234,760–1392,798 | View 4 cab front, view 5 rear doors |

Not touched: the tiny licence plate on the car (not legible at any page size). These images are illustrative brand visualisations, not photographs, and are captioned «صورة توضيحية» / "Illustrative image".

## 6. Checks

- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**, 20 pages 297 × 210 mm; fonts Tajawal Regular/Medium/Bold/ExtraBold and IBM Plex Sans Regular/Medium/SemiBold/Bold embedded; no fallback; 4,146 Arabic characters, no presentation forms. Webfonts all loaded.
- All 20 previews viewed in contact sheets at about 800 px per page (service pages re-checked after the final band change): Arabic connected and right to left, nothing clipped, titles over images on a navy gradient (white on ≥ 78% navy), partner logos clearly visible.
- Car / facade retouch checked at 3× after the final run. The final 4× sheets for the cleaning, rider and truck images (`_work/retouch_v02/zoom_*.png`) were generated but only checked at page scale after the switch to stroke-only masks: **the quality-reviewer should open them**.

## 7. Open points

1. Name and lockup (cover, back cover) remain a proposal awaiting the client.
2. The banner slogan «خدمتك بجودة تهمنا» in the cover image is not approved copy; it is cropped mostly out of view behind the lockup panel on p1 but exists in the derived image. Client to confirm or have it removed.
3. `content-outline.md` and `content-gaps.md` were not updated with the client's logistics and website answers; the copy used is the Creative Director's message of 2026-11-13.
4. Phone, email and address from the old profile, not reconfirmed.
5. Photo licences unknown (from the old profile). Partner-logo permissions are the client's responsibility; 12 old logos are low-resolution (tier B/C sizes).
6. No native Arabic proofread of the layout yet. PDF not tagged. Screen PDF only (no print version).
7. Service pages use per-service band heights (100–128 mm) so no page has an empty lower half; pp7 and 11 still end about 25 mm above the footer.
