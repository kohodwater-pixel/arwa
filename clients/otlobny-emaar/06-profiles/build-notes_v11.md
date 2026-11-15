# Build notes — «اطلبني إعمار» / OTLOBNY Emar company profile v11

**Date:** 2026-11-15 · **Author:** corporate-designer
**Inputs:** client instruction on v10 (brand-context.md, 2026-11-15: no captions under images, no draft wording) and the minors of review_v10_r7.
v10 is untouched. 20 pages.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v11.pdf` and `.html`
- `_work/build_profile_v11.py`: uses `assets/derived/v10_logistics_fleet-client.jpg` unchanged
- `_work/finish_pdf_v11.py`, `_work/contact_v11.py`, `_work/contact_v11_part1.png`, `_work/contact_v11_part2.png`
- `_work/preview_v11/`, `_work/build_v11.log`, `_work/check_v11.log`
- `assets/derived/v11_*.jpg`

## Changes
| # | Change | Done how / where |
|---|---|---|
| 1 | All image captions and labels removed | Removed in both languages on p11 (team mockup label), p12 (fleet label), and pp14–16 (client-photo and rendering captions). "illustrative" also removed from the alt texts and the SVG aria-label. |
| 1 | Pages rebalanced after the captions came out | pp14–16: photos are re-centred vertically on the page middle (105 mm), the same line on all three pages. p12: the fleet image moved down 2 mm and its floor runs freely with no label. |
| 2 | Back cover credits trimmed | The "Client images" note and the sentence about illustrative visuals are removed in both languages. Kept: every CC BY / BY-SA attribution (with "modified" and the share-alike wording), the no-attribution list, and the stock-photo rights note. Arabic note reworded so it covers the licensed stock photos only: «الصور الفوتوغرافية المرخصة بتراخيص المشاع الإبداعي أو من الملكية العامة منسوبة إلى أصحابها …». The credits band is now the lower 34% (was 40%); English is 6.8 pt in #5F6573 (5.84:1), Arabic 8 pt. |
| 3 | "draft" removed | PDF title is now "اطلبني إعمار — الملف التعريفي \| OTLOBNY Emar — Company Profile"; the subject line and the HTML title are changed to match. The file keeps its _v11 name. |
| r7 m1 | p20 lockup version | Now the **white** lockup v02 on the gradient (system.md: white on royal blue and gradients). White on the light end of the gradient is 6.59:1. |
| r7 m2 | p2 clear zone | The lattice now fades into solid navy from 118 mm down; it is fully navy above the lockup's clear zone (158 mm), so there is no hard rectangle. |
| r7 m3 | pp14–16 duplicate number | The small "0N / 03" fraction is dropped; only the large work number remains. |

## Checks
- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS** (Tajawal and IBM Plex Sans, no fallback font).
- PDF text search, all 0:
  - «مقدمة من العميل», "supplied by the client", «توضيحية», "illustrative" (any case), "draft" (any case), "Client images", «صور العميل»
  - the earlier forbidden list: Emaar/EMAAR, «شهد», Shahd, "single company", «في عقد مع شركة واحدة», «اطليني», CONSANY, Suzuki, ISUZU, DZIRE, «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp, "WE DO THE BEST"
- HTML search for illustrative/draft/caption strings: 0.
- Contents, folios and bookmarks: contents 03/04/06/13/14/17/19 match the pages; no folio mismatches; bookmarks 2, 3, 4, 6, 13, 14, 17, 19, 20.
- No image on two pages (build log: "none").
- Credits still present: 15 "CC BY" entries plus the no-attribution list.
- All 20 pages viewed on the contact sheets.

## Note
The profile no longer tells the reader that the service photos are stock and that the vehicle and team images are AI-generated mockups. This follows the client's instruction. The open-licence credits on p20 still name every stock photo.
