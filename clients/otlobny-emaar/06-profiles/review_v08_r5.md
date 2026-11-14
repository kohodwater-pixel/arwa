## Quality review: otlobny-emaar company profile v08 (screen, ar-en), r5, 2026-11-14

**Verdict: PASS WITH MINOR FIXES.** There are no critical or major issues, and none of the ten points fails. The r4 major (the AI-drawn logos on the vehicles) is properly fixed.

**v08 may go to the client as a reviewed draft.** These are still needed before anything is called final or enters `08-final-delivery/`:
- the client's approval;
- a native Arabic proofread;
- a separate review of the delivery package.

The minor issues below can go into the next version together with the client's feedback.

### What I checked

Everything is under `/home/user/arwa/clients/otlobny-emaar/`.
- **Arabic check:** I ran `python3 scripts/check_arabic_pdf.py` on `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v08.pdf`. Result: PASS. 20 pages. Tajawal and IBM Plex Sans, all weights embedded, no fallback. 4,535 Arabic characters, no presentation forms.
- **Rendering:** all 20 pages at 150 dpi, viewed one by one (pp8, 9, 12 and 16) or on contact sheets I built myself (the rest). p12 again at 300 dpi.
- **Logo comparison:** I set every logo placed on p12 beside `04-identity/02-logo/_work/otlobny-emaar_logo_wordmark-colour_ar_v01_on-white.png` and `…wordmark-reversed_ar_v01_on-navy.png`.
- **Paint-out check:** I stretched the contrast on the truck box and the car door to look for patches left by painting out the old logos, and measured the tone inside and outside each patch.
- **Bookmarks:** read with pypdf.
- **Images:** `_work/build_v08.log` reports no source on more than one page.
- **Text:** I diffed every text string in the v07 and v08 HTML. PDF search finds no «شهد»/Shahd, «أطلبني», lorem or TBC.

### p12 in depth: each replaced logo at 300 dpi

| Surface | Version | Shape against the SVG | Perspective and baseline | Halo, patch and light | Judgement |
|---|---|---|---|---|---|
| Truck box side | Reversed (green with white dot and squeegee) on navy, correct per `system.md` | Letterforms match the reversed wordmark: two equal short teeth, tall stem, «ط» drawn correctly, ringed dot, squeegee, star dot, pill dot | Right side shorter than the left, matching how the panel recedes; the squash fits the box's foreshortening (about 0.43); baseline follows the panel | No halo. The paint-out patch shows only under heavy contrast stretch (measured 2–6 levels of 255): invisible at normal view | Good |
| Cab front | Colour on white | Correct | Straight, centred on the grille panel | Clean | Good |
| Cab door | Colour on white | Correct | Slight perspective, fits between window and handle | Clean | Good |
| Car door | Colour on white | Correct, white ring round the dot intact | Follows the door plane | Faint flatter patch visible only under stretch | Good |
| Delivery box | Reversed on black | Correct | Near-frontal, crisp | Clean | Good |
| Scooter side panel | Painted out | Not applicable | Not applicable | Clean unbranded panel | Acceptable |

Other p12 points:
- **Rear of the truck box (r4 m1):** fixed. Clean edge, silver top rail and rear trim restored.
- **Windscreen (r4 m2):** the towers seen through the glass are gone.
- **Shadows (r4 m2):** consistent across the three vehicles, and the light now reads as one scene.
- **Sharpness (r4 m3):** the composite is now about 294 ppi and crisp at 300 dpi.
- The tiny AI logo on the rider's jacket remains. It is about 2 mm and unreadable, and accepted under the m9 ruling.

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Diamond lattice system unchanged and intact. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; competitors are out of scope. |
| 3 | Colour and contrast | PASS | Brand colours only. Logo versions match `system.md` on every ground. Text colours unchanged from v06, where I measured them. |
| 4 | Arabic and English typography | PASS | check_arabic PASS; the new Arabic sentence on p16 is connected and reads right to left. |
| 5 | Logo clarity | PASS | The real wordmark is used on every page and on every vehicle surface on p12. |
| 6 | Layout | PASS | p16 now matches the works master; the p8 and p9 lists no longer wrap awkwardly. Small points below. |
| 7 | Consistency across pages | PASS | pp14–16 share one master: number, titles, rule, text, scope chips. |
| 8 | Accuracy | PASS | The Dar Al Taqwa sentence and scope (maintenance and cleaning) are the client's confirmation recorded in `brand-context.md` on 2026-11-14, worded exactly as in the content outline. No spelling errors. |
| 9 | Export quality | PASS | Screen PDF, sRGB, fonts embedded, 10.8 MB, file name follows `file-delivery.md`, 9 bookmarks. |
| 10 | Matches client requirements | PASS | Dar Al Taqwa has its own page with both photos and the confirmed scope. Logistics is one combined image of the car, scooter and truck. 20 pages. All earlier rulings are kept. |

### Other items you asked for

- **p16:** both photos are sharp at their size (entrance 230 ppi, room 197 ppi), with matching heights and stacked captions as on p14 and p15. The new sentence reads «قدمت «اطلبني إعمار» خدمات الصيانة والنظافة لفندق دار التقوى.» / "OTLOBNY Emaar provided maintenance and cleaning services for Dar Al Taqwa Hotel." It is correct in both languages, with chips صيانة، نظافة / Maintenance, Cleaning.
- **p8 and p9:** "Maintenance of parks and street trees", "Maintenance of irrigation equipment" and "Landscaping of planted gardens" now sit on one line each. On p9 the items wrap as two balanced lines, with no orphan words and no three-line items.
- **Contents against real folios:** About 03, Vision 04, Services 06, Why Us 13, Work 14, Partners 17, Contact 19. All correct. Footer folios 02–19 match their pages.
- **Bookmarks** match: Contents 2, About 3, Vision 4, Services 6, Why 13, Work 14, Partners 17, Contact 19, Photo credits 20.
- **Regression pass over all 20 pages:** nothing has regressed. Text changed only on p16 and in the version in the title.

### Issues (all minor)

- **m1. p12, under the truck chassis between the wheels.** The cut-out edge is ragged, with light fringes along it, and a small stray grey dash floats about 4 mm below the chassis. It is faintly visible at page size. Fix: smooth the mask along the chassis underside and delete the dash. Corporate-designer.
- **m2. p12, scooter.** Thin pale slivers of the original background remain beside the front and rear wheels. They are visible only on zoom. Clean the mask. Corporate-designer.
- **m3. p16 line breaks split the hotel's name.** The Arabic breaks between «لفندق» and «دار التقوى»; the English between "Dar Al" and "Taqwa Hotel". Fix: keep each name on one line with non-breaking spaces. Corporate-designer.
- **m4. p20 "Client images" note.** It says the illustrative images were "supplied by the client". The p12 image is now an agency montage of the client's mockups with the logos re-applied by the agency. Suggested English: "illustrative visuals based on images supplied by the client". Arabic to match: «تصاميم توضيحية مبنية على صور مقدمة من العميل». Corporate-designer; the Creative Director approves the wording.
- **m5. Still open from earlier rounds:**
  - "single contract" line (p13, point 01);
  - original bus-shelter photo;
  - official partner logo files (The End still cut);
  - the client's own site, staff and fleet photographs;
  - two non-Gulf tiles (p8, p10);
  - native Arabic proofread;
  - PDF not tagged for accessibility.

### Overall view against the client's bar

v08 is the strongest version so far:
- a credible collage cover;
- a coherent diamond system;
- p12 now shows the client's real logo on a convincing three-vehicle fleet;
- the works section reads as three matching, factual case pages.

What still keeps it short of genuinely world-class is the source photography: stock tiles and client mockups instead of the company's own work. Only the client can supply that.

### The three changes that would most raise the level

1. The client's own photographs of his sites, staff, fleet and finished works. This is still the single biggest lever.
2. Clean-up of the p12 cut-out edges (m1, m2).
3. Keep the hotel name together on p16 (m3) and correct the provenance note on p20 (m4).

### Not checked

- No native Arabic proofreading.
- The PDF was not opened in a second viewer; I rendered it with poppler only.
- The HTML source was not opened from a copied location.
- I did not inspect the maker's `_work/v08/check300_*.png` crops; I made my own from the PDF.
- Licence terms were not checked against the live source pages.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 5 of company profile v08 (screen PDF, ar-en)
Status: DONE
Files produced: none in the repo. Scratch files are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/:
- check_arabic previews in review_v08/
- 150 dpi pages and the 300 dpi p12 render in v8/
- p12 crops k_*.png (k_box, k_cab, k_car, k_deliv, k_under, k_scoot, k_*_stretch)
- contact sheets s8a.png, s8b.png, s8c.png
Tool operations: `check_arabic_pdf.py` on v08 returned PASS. pdftoppm at 150 and 300 dpi, pdftotext, a pypdf bookmark read, and a numpy tone measurement of the paint-out patches, all read-only. HTML text diff v07 → v08. No Figma or Canva operations.
Decisions needed:
1. Send v08 to the client as a reviewed draft (recommended: yes), stating that it is not final.
2. Approve the p20 provenance wording in m4.
3. Arrange the native Arabic proofread before any final version.
Assumptions: the Dar Al Taqwa scope is taken as confirmed on the strength of the 2026-11-14 `brand-context.md` entry. The identity wordmark SVGs in `04-identity/02-logo/` are the reference drawing of the logo.
Issues / risks: verdict PASS WITH MINOR FIXES — 0 critical, 0 major, 5 minor. Not a final approval: the client's approval, a native proofread and the package review are still to come.
Suggested next agent: Creative Director, to send v08 to the client as a reviewed draft. Corporate-designer afterwards, for m1–m4 plus the client's feedback, as v09. Quality-reviewer before any final version and for the 08-final-delivery package review.

