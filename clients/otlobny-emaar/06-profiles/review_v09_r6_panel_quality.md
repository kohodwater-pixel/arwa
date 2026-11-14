## Quality review: otlobny-emaar company profile v09 (screen, ar-en), r6, 2026-11-14 — panel member: ten-point quality and technical

**Verdict: PASS WITH MINOR FIXES.** No critical or major issues; none of the ten points fails.

**v09 may be presented to the client as a reviewed draft.** It is not final. Three conditions:
1. The name strings must be confirmed by the client against his CR certificate. They are still an agency decision pending confirmation (name-decision §3).
2. Arabic needs a native proofread.
3. The 08 package needs its own review.

I recommend fixing m1–m3 before sending; each is a small change. If they go out unfixed, say so in the cover note.

### What I checked

Everything is under `/home/user/arwa/clients/otlobny-emaar/`.
- **Arabic check:** I ran `python3 scripts/check_arabic_pdf.py` on `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v09.pdf`. Result: PASS. 20 pages. Tajawal and IBM Plex Sans, all weights embedded, no fallback. 4,568 Arabic characters, no presentation forms.
- **Pages:** all 20 rendered at 150 dpi and viewed. pp1, 2, 12, 15, 19 and 20 viewed full-size; the rest on contact sheets. p12 also at 300 dpi.
- **Vehicle logos:** each one on p12 compared at 300 dpi with the wordmark and lockup v02 in `04-identity/02-logo/`.
- **Clear space:** measured on p1 from pixels.
- **Metadata and bookmarks:** read with pypdf.
- **Text:** HTML text diff from v08 to v09, with the name change normalised so only real copy changes show.
- **Name sweep:** PDF text and HTML for Emaar/EMAAR.
- **Images:** build log checked for repeated images.

### Lockup v02 on the four pages (against system.md §1a)

| Page | Version | Ground | Size | Clear space | Result |
|---|---|---|---|---|---|
| p1 cover | colour, grey descriptor | white | about 86 mm, above the 45 mm minimum | **Measured gap to the rope-access photo diamond: 4.2 mm. X = 6.9% × 86 mm ≈ 5.9 mm, so about 1.7 mm short (m1).** Top and left margins are fine. | Renders correctly; Arabic connected, English line crisp |
| p2 contents | reversed: green wordmark, white descriptor | navy panel | 58 mm | Margins fine. The background diamond hairlines run behind the lockup; this is texture of the ground, but see m4. | Correct |
| p19 contact | reversed | navy | about 80 mm | Generous; the kicker is about 12 mm below | Correct |
| p20 back cover | colour | white | about 90 mm | Generous; otlobny.net / المدينة المنورة sits about 9 mm below | Correct |

The descriptor reads «شركة اطلبني إعمار المحدودة» / "OTLOBNY EMAR COMPANY LTD." on all four pages, with the hamza on إ, matching name-decision §3. It is outlined (not live text) and the Arabic is untracked.

### p12, the client's fleet image, at 300 dpi

| Surface | Placed | Shape against the SVG | Perspective | Halo or patch | Result |
|---|---|---|---|---|---|
| Truck box side | White lockup on royal blue (correct per system.md; the reversed green would only reach 3.06:1) | Correct wordmark and descriptor; both lines readable on zoom | Follows the box plane; descriptor parallel to it | No halo; the livery wave below is intact | Good. But at about 34 mm on the page the lockup is under the 45 mm minimum (m2). |
| Cab front | Colour wordmark | Correct | Straight | Clean | Good |
| Cab door | Colour wordmark | Correct | Slight perspective | **The paint-out patch cuts a white notch into the base of the mirror bracket, just above-left of the logo, and leaves a tiny dark speck below-left of the door handle (m3)** | Logo good; patch needs fixing |
| Car door | Colour wordmark | Correct | Follows the door | Clean at normal view | Good |
| Delivery box | White wordmark on blue | Correct | Near-frontal | Clean | Good |
| Scooter panel | Colour wordmark, rotated | Correct | Fits the curved panel | Clean | Good |

- **Third-party marks:** the Suzuki badge and the DZIRE plate on the car are blank, with the grille bars kept. The ISUZU marks on the truck grille and bumper are gone.
- **Garbled AI text:** none survives anywhere on the vehicles. The 0-count for «اطليني», CONSANY, COKPANY, ISUZU, DZIRE and Suzuki applies to the PDF text; the visual check covered the image itself.
- **Cut-out edges:** no dark fringe on the car front, wheels or truck rear. The floor shadows are consistent.

This is now the client's own scene with the real identity applied. It is clearly the best logistics image the book has had.

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Diamond lattice system intact; the cover and the service masters are unchanged. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; competitors are out of scope. The name risk ("Emar" still sounds like Emaar) is noted in the name decision and is not a design issue. |
| 3 | Colour and contrast | PASS | Lockup versions match the ground on all four pages and on the vehicles (white on royal blue, colour on white). Descriptor contrast is as in system.md (7.61:1 grey on white, 12.55:1 white on navy). |
| 4 | Arabic and English typography | PASS | check_arabic PASS. The new Arabic text on p15 and p20 is connected and reads right to left. The descriptor is shaped and untracked. |
| 5 | Logo clarity | PASS | The real lockup or wordmark is used everywhere, with the correct version per ground. The two clear-space and minimum-size deviations are minor (m1, m2). |
| 6 | Layout | PASS | No regressions on any page. The p16 name stays together («دار التقوى» / "Dar Al Taqwa Hotel"). |
| 7 | Consistency across pages | PASS | "OTLOBNY Emar" / "OTLOBNY EMAR" in every kicker, footer and title. |
| 8 | Accuracy | PASS | The p15 contract "from 2023 to the present" is the client-confirmed fact in brand-context.md. The p16 scope is client-confirmed. No other copy changed. No spelling errors in either language. |
| 9 | Export quality | PASS | Screen PDF, sRGB, fonts embedded, 11.1 MB. File name follows `file-delivery.md`; the slug keeps "emaar" by ruling. Metadata Title reads "OTLOBNY Emar". |
| 10 | Matches client requirements | PASS | Lockup with descriptor across the profile, as the client instructed. His fleet image is on p12. The Chamber contract period is stated. 20 pages. All earlier rulings are kept. |

### Contents, bookmarks, repeats, name sweep

- **Contents:** 03, 04, 06, 13, 14, 17 and 19 match the real footer folios on pages 3–19.
- **Bookmarks:** Contents 2, About 3, Vision 4, Services 6, Why 13, Work 14, Partners 17, Contact 19, Photo credits 20. All correct.
- **Repeated images:** none, per the build log.
- **"Emaar":** 0 in the PDF text and 0 in the PDF metadata. In the HTML it appears only inside four asset file paths (`otlobny-emaar_logo_lockup-*_v02.svg`), which the ruling permits and which are never displayed.
- **Removed strings:** Shahd/«شهد», «أطلبني», lorem and TBC all appear 0 times.

### Changed text, proofread

- **p15 (Arabic):** «تقدم «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة بعقد مستمر منذ عام 2023 حتى الآن.» Correct.
- **p15 (English):** "OTLOBNY Emar has provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry under a contract running from 2023 to the present." Correct, and it matches the Arabic.
- **p20 provenance note:** «تصاميم توضيحية مبنية على صور مقدمة من العميل» / "illustrative visuals based on images supplied by the client". Correct.

### Issues (all minor)

- **m1. p1 cover: lockup clear space is infringed.**
  - Where: the left tip of the rope-access photo diamond comes within 4.2 mm of the lockup's right edge; the rule is about 5.9 mm.
  - Fix (either):
    - reduce the lockup to about 80 mm (it stays above the 45 mm minimum);
    - or shift the collage about 2 mm right / the lockup about 2 mm left.
  - Who: corporate-designer.
- **m2. p12 truck box: the lockup is about 34 mm on the page, under system.md's 45 mm minimum.**
  - The descriptor is about 1 mm tall: legible only when zoomed.
  - Two ways to resolve it:
    - **(a)** the Creative Director rules that livery depicted inside a photograph is exempt, because it represents a full-size vehicle;
    - **(b)** use the white wordmark alone, as on the other five surfaces.
  - Recommendation: (a), recorded in brand-context.md, because a lettered truck box is exactly where a real lockup would sit.
  - Who: Creative Director.
- **m3. p12 cab door: paint-out patch.**
  - Where: a white notch cuts into the lower mirror-bracket corner above-left of the logo, and a small dark speck sits below-left of the door handle.
  - At page size it is about 1 mm and visible to a careful eye.
  - Fix: restore the bracket from the source, limit the paint-out to the door panel, and remove the speck.
  - Who: corporate-designer.
- **m4. p2 contents: background hairlines run behind the lockup.**
  - The diamond pattern lines pass through the lockup's clear-space zone.
  - This is acceptable as ground texture, but a cleaner result would mask the pattern (solid navy) within X of the lockup.
  - Optional.
- **m5. Still open from earlier rounds:**
  - client confirmation of the name strings against his CR;
  - native Arabic proofread;
  - second-viewer check;
  - accessibility tagging;
  - original bus-shelter photo;
  - official partner logo files (The End still cut);
  - the client's own site, staff and fleet photographs;
  - the "single contract" line on p13;
  - rights to the fleet mockup and the room photo (the client's responsibility, as recorded).

### Overall view against the client's bar

v09 is the most complete and credible version so far:
- the client's chosen lockup, rendered correctly on every page;
- his own fleet image, now carrying the real identity;
- one consistent name throughout;
- factual work pages.

As before, the gap to truly world-class is the photography, which only the client's own material can close. From a quality and technical standpoint the piece is ready for the client's review.

### Not checked

- No native Arabic proofreading.
- The PDF was not opened in a second viewer; I rendered it with poppler only.
- The HTML source was not opened from a copied location.
- I did not open the maker's `_work/v09/check300_*.png`; I made my own crops from the PDF.
- I did not check the vector paths of the lockup SVGs beyond their rendered output.
- The legal and registered name was not verified; it cannot be until the client sends his CR.
- Licence terms were not checked against the live source pages.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 6, full book, company profile v09 (screen PDF, ar-en); quality and technical member of a three-expert panel
Status: DONE
Files produced: none in the repo. Scratch files are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/:
- check_arabic previews in review_v09/
- 150 dpi pages and the 300 dpi p12 render in v9/
- p12 crops j_*.png (j_box, j_cab, j_door, j_fleck, j_car, j_deliv, j_scoot, j_carfront, j_grille, j_tgrille)
- contact sheets s9a.png and s9b.png
Tool operations: `check_arabic_pdf.py` on v09 returned PASS. pdfinfo, pypdf (metadata and bookmarks), pdftotext, pdftoppm at 150 and 300 dpi, a numpy clear-space measurement on p1, and an HTML text diff v08 → v09. All read-only. No Figma or Canva operations.
Decisions needed:
1. Present v09 to the client as a reviewed draft (recommended: yes, ideally after the m1 and m3 fixes).
2. m2: rule that livery depicted in a photograph is exempt from the 45 mm lockup minimum (recommended), or use the wordmark alone on the truck box.
3. In the same message, ask the client to confirm the name strings against his CR.
Assumptions: the descriptor strings and "Emar" are taken as the agency decision recorded on 2026-11-14 (pending client confirmation). The p15 "2023 to the present" is taken as client-confirmed per brand-context.md.
Issues / risks: verdict PASS WITH MINOR FIXES — 0 critical, 0 major, 5 minor. Not a final approval: the name confirmation, native proofread and package review are still to come.
Suggested next agent: corporate-designer, for m1, m3 and optionally m4 (and m2 if the Creative Director chooses option b), as v10 or a patch. Quality-reviewer then only needs to recheck p1, p2 and p12. Creative Director to reconcile this report with the art-director's and brand-strategist's panel reviews.

