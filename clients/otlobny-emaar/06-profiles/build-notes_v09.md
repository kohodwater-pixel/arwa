# Build notes — «اطلبني إعمار» / OTLOBNY Emar company profile, draft v09

**Date:** 2026-11-14 · **Author:** corporate-designer · **Status:** DRAFT v09, built from the client's instructions and the agency decisions recorded on 2026-11-14 (brand-context.md and `03-strategy/name-decision_2026-11-14.md`). The name strings are pending the client's confirmation. v08 is untouched. **20 pages.**

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v09.pdf` and `.html`
- `_work/build_profile_v09.py`. Run `_work/v09/fleet_v09.py` first.
- `_work/v09/fleet_v09.py`: prepares the client's fleet image and writes `assets/derived/v09_logistics_fleet-client.jpg` (4376 × 1618 px).
- `_work/v09/check300_*.png`: 300 dpi crops of every vehicle surface, the removed marks and two cut-out edges. `check300_all.png` shows the vehicle surfaces and removed marks at 2×.
- `assets/mockups/mockup_fleet_car-scooter-truck.png`: copy of the client upload. The original in `_originals/` is untouched.
- `assets/logo/otlobny-emaar_logo_lockup-{colour,reversed,white,navy}_ar-en_v02.svg`: copied from `04-identity/02-logo/`.
- `_work/finish_pdf_v09.py`, `_work/contact_v09.py`, `_work/contact_v09_part1/2.png`, `_work/preview_v09/`, `_work/build_v09.log`, `_work/check_v09.log`
- `content-outline.md`: v09 status block added. The earlier text is in `_archive/content-outline_before-v09_2026-11-14.md`.

## 1. Lockup v02 across the profile (minimum 45 mm; version chosen by ground, per system.md 1a)

| Page | Version | Width | Ground |
|---|---|---|---|
| p1 cover | colour | 86 mm (the full text column, as the wordmark was) | white |
| p2 contents | reversed | 58 mm | navy panel |
| p19 contact | reversed | 80 mm | navy |
| p20 back cover | colour | 90 mm | white |

- Clear space: at least one alef width (6.9% of the lockup width) on every page.
- p19: the contact block starts 59 mm from the top, below the 49 mm lockup.
- p20: the otlobny.net / Madinah line sits 9 mm below the descriptor.
- No other page carries the logo.

## 2. Name
- Every English "OTLOBNY Emaar" is now "OTLOBNY Emar". This covers body copy, kickers, footers (which display "OTLOBNY EMAR"), the "Why" title, alt text, the HTML title and the PDF metadata.
- The PDF contains "Emaar" 0 times; the HTML also contains 0. File and folder names keep "emaar", as instructed.
- Arabic running text is unchanged: «اطلبني إعمار».

## 3. Logistics image: the client's own fleet image on p12

**Edges**
- The cut-out was made from a black ground. Semi-transparent edge pixels are un-premultiplied against black.
- Rim pixels darker than the pixels just inside are faded.
- The whole silhouette is choked by 1 px and re-feathered by 0.7 px.
- Checked at 300 dpi on the car front and the truck rear (`check300_edge_*`): no dark fringe.

**Third-party marks:** Suzuki badge, "DZIRE" plate lettering and "ISUZU" lettering are painted out by row-wise interpolation, which keeps the grille bars. The DZIRE and ISUZU plates are now blank dark plates.

**AI logos and garbled descriptors**

Method:
- The AI logos and descriptors are painted out with each panel's own paint. The fill is computed only from the surrounding panel pixels, followed by a second pass that removes faint grey ghosts.
- The real mark is then placed with `cv2.getPerspectiveTransform` and shaded by the panel's local light.
- White versions are used on the blue boxes and colour versions on the white panels.
- The client's livery waves and the vehicles themselves are untouched.

| Surface | Placed | Width in the image | Judgement at 300 dpi (`_work/v09/check300_*.png`) |
|---|---|---|---|
| Truck box side | **white lockup v02**, fitted to the box's four corners; centred where the AI block was | 248 px src, ≈ 34 mm on the page | Reads as printed. Perspective follows the panel and the descriptor runs parallel to it. Real descriptor text, legible on zoom. No halo. |
| Truck cab front | **wordmark alone** (colour) | ≈ 17 mm | Straight and clean. The descriptor below is painted out to a clean white panel. A very faint smoothing of the panel is visible only at 2× of 300 dpi. |
| Truck cab door | **wordmark alone** (colour), slight receding perspective | ≈ 12 mm | Clean. The painted-out area is a hair lighter than the door at 2× of 300 dpi; not visible at page size. |
| Car door | **wordmark alone** (colour), following the door slope | ≈ 20 mm | Good. The descriptor is painted out. At extreme zoom the faint door-seam line is lost inside the painted area. |
| Delivery box | **wordmark alone** (white) | ≈ 16 mm | Crisp, matches the box. Descriptor painted out. |
| Scooter panel | **wordmark alone** (colour), rotated −17° to the panel | ≈ 12 mm | Clean on the curved panel. Only the old logo's own blue/green pixels were filled. |

- **Why the wordmark alone on five surfaces:** the lockup's minimum width is 45 mm. On those surfaces the descriptor would print at 1–2 pt, which the ruling treats as below legible size. Their garbled descriptors are therefore painted out, not replaced.
- No surface needed to be left as a blank panel.
- No garbled text («اطليني», "CONSANY", "COKPANY") survives anywhere. This was checked visually on every crop; text search cannot see inside images.

**On the page:** the image sits on the same pale floor with contact and ambient shadows, runs full width (297 × 109.8 mm), and keeps the «صورة توضيحية» / "Illustrative image" label.
- Effective resolution is 374 ppi on the ×2 working canvas (the client file's native resolution is 187 ppi at this width).
- The v08 agency composite is no longer used.

## 4. Madinah Chamber (p15)
- Body text now reads «تقدم «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة بعقد مستمر منذ عام 2023 حتى الآن.» / "OTLOBNY Emar has provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry under a contract running from 2023 to the present."
- No other fact was added.

## 5. Review r5 minors
- p16: «دار التقوى» and "Dar Al Taqwa Hotel" are joined with non-breaking spaces in the title and in the body text.
- p20: the note now reads "illustrative visuals based on images supplied by the client" / «تصاميم توضيحية مبنية على صور مقدمة من العميل».

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**. 20 pages; Tajawal and IBM Plex Sans with no fallback; 4,568 Arabic characters.
- PDF text search, all 0: Emaar/EMAAR, «شهد», Shahd, «اطليني», CONSANY, COKPANY, Suzuki, ISUZU, DZIRE, «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp. No harakat.
- The Chamber sentence appears once in each language.
- Contents vs folios: contents 03, 04, 06, 13, 14, 17, 19 match the real pages; every folio matches its page.
- Bookmarks point to pages 2, 3, 4, 6, 13, 14, 17, 19 and 20.
- No source image appears on two pages; the build log reports "none".
- Every page viewed on the contact sheets. pp1, 2, 12, 13, 15, 16, 19 and 20 were also viewed at preview size, and every vehicle surface in the 300 dpi crops.
- Image ppi is as in v08 except p12 (above).

## Open
- Client confirmation of the name strings ("Emar", «إعمار», the descriptor) against his commercial registration. Not a trademark clearance.
- Rights to the fleet mockup and the hotel room photo rest with the client.
- Native Arabic proofread, second-viewer check and accessibility tagging are still outstanding, along with the earlier client items (original bus-shelter file, official partner logos, own photographs, the "single contract" line).
