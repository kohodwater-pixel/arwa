## Quality review: otlobny-emaar company profile v07 (screen, ar-en), r4, 2026-11-14

**Verdict: FAIL, on one major issue.** You were right about the logo on the truck's side. At 300 dpi it is malformed, and so is the logo on every vehicle in the logistics image. The composite did not cause this: the shapes come unchanged from the client's AI-generated mockups. I should have caught it in r1–r3, because the same truck images were on p13 in v04–v06 and the car/scooter image was on p6 and p12. I flagged only the logo colours then (m9), not the shapes. That was my miss.

Everything else in v07 is at PASS WITH MINOR FIXES level:
- both of the client's instructions are carried out correctly;
- the contents page numbers are right;
- no image is used on two pages;
- the Arabic check passes and the changed text is correct.

**Can v07 go to the client as a reviewed draft?** Not yet. Two ways to clear the major issue:
- **(a) Recommended, a small job:** replace the logos on the vehicles in the p12 composite with the real wordmark, warped to each surface's perspective. Then re-review only p12.
- **(b) A Creative Director ruling,** recorded in `brand-context.md`, that extends m9 from logo colours to logo shapes inside the client's illustrative mockups, and tells the client plainly that these are AI approximations of his logo. Once that ruling is recorded, v07 may go to the client as a reviewed draft.

### What I checked

Everything is under `/home/user/arwa/clients/otlobny-emaar/`.
- **Arabic check:** I ran `python3 scripts/check_arabic_pdf.py` on `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v07.pdf`. Result: PASS. 20 pages at 297 × 210 mm. Fonts are Tajawal and IBM Plex Sans, all weights embedded, no fallback. 4,467 Arabic characters, no presentation forms.
- **Rendering:** all 20 pages at 150 dpi, viewed one by one or on contact sheets I built myself. p12 and p16 again at 300 dpi.
- **Logo comparison:** I set the truck-box logo, isolated by colour from the client's source image, beside `04-identity/02-logo/_work/otlobny-emaar_logo_wordmark-colour_ar_v01_on-white.png`. I also compared it with the original mockup in `_originals/mockup_logistics-trucks.png`.
- **Contents and folios:** I checked the contents page against the real page folios. Images per page come from `_work/build_v07.log`.
- **Text:** I diffed every text string in the v06 and v07 HTML.

### Logo on the p12 composite: findings

- **Truck box side** (the largest logo on the page, about 40 mm wide). Compared with the identity wordmark:
  - the two short teeth are unequal, and the second rises almost to the tall stem;
  - the green upper stroke and bowl of «ط» are reshaped and overlap differently;
  - the squeegee is a small zigzag rather than the drawn squeegee;
  - the green dot has no white ring;
  - the pill-shaped dot under «ي» is a rounded square;
  - the star dot is oval.

  It reads as «اطلبني», but it is visibly not the client's logo. The aspect ratio is the same in the source (1.37) and in the composite (1.39), so the compositing did not stretch it.
- **Truck cab front and door, car door, delivery box and scooter side panel:** the same AI approximation at smaller sizes. The scooter's logo is also skewed along the body panel. All are complete (nothing cropped) and legible as «اطلبني», but none matches the identity drawing.
- **Severity:** I rate this major, not critical, because the client supplied these images, asked for them, and they are labelled «صورة توضيحية». But an incorrect logo at this size on the client's own logistics page breaks `quality-standards.md` (only approved logos). Addendum 4 also committed to compositing the real lockup into these mockups.

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Diamond lattice system intact; logistics is now one strong full-width image page. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; competitors are out of scope. |
| 3 | Colour and contrast | PASS | Brand colours only; text colours and backgrounds unchanged from v06 (measured in r2). |
| 4 | Arabic and English typography | PASS | check_arabic PASS; letters connected and right to left on every page; the new caption «صور مقدمة من العميل» is correct. |
| 5 | Logo clarity | FAIL | p12: the logos on the truck box, cab, car, delivery box and scooter are AI-malformed versions of «اطلبني». The real logo on pp1, 2, 19 and 20 is correct. |
| 6 | Layout | PASS | p12 and pp14–16 work as a family; minor points below. |
| 7 | Consistency across pages | PASS | The works master is shared on pp14–16; the panel side alternates as intended. |
| 8 | Accuracy | PASS | Dar Al Taqwa states no scope. The tower credit (ianmunroe) is removed with its image. Contact details unchanged. No spelling errors. |
| 9 | Export quality | PASS | Screen PDF, sRGB, fonts embedded, 11.3 MB, file name follows `file-delivery.md`. |
| 10 | Matches client requirements | PASS | Dar Al Taqwa has its own page with both photos (p16). Logistics is one combined image of the car, scooter and truck (p12). The book is 20 pages. All earlier rulings are kept. |

### Other checks against what you asked

- **Contents page numbers** against the real footer folios: About 03, Vision/Mission/Goals 04, Services 06, Why Us 13, Our Work 14, Partners 17, Contact 19. All correct.
  - The p6 overview's "PAGE 07…12" references are correct.
  - The PDF bookmarks were not checked separately.
- **No image on two pages:** confirmed from the build log ("sources on more than one page: none") and by eye.
  - The racking aisle is now only on the cover.
  - The tower image is gone from the pages and the credits.
- **Changed text** (v06 → v07 diff): only the removal of the old p13 strings, the new p16 caption «صور مقدمة من العميل» / "Photographs supplied by the client", the version in the title, and the credits minus the tower photo. All correct.
- **p16, Dar Al Taqwa:** both photos are sharp enough for screen (entrance 194 ppi, room 167 ppi), with matching heights. The room photo has no watermark or overlay at 300 dpi. Rights for the room photo stay with the client, as recorded in `brand-context.md`.

### Issues

**Major**

**M1. p12 composite: logos on the vehicles are malformed (details above).**
- **Fix:** the composite already has masks for each vehicle. Recolour away the AI logo on each surface with that surface's paint colour, then place `04-identity/02-logo/otlobny-emaar_logo_wordmark-colour_ar_v01.svg` (white or reversed version where the ground is dark, as `system.md` requires) with a perspective transform matching each surface:
  - truck box side;
  - cab front and door;
  - car door;
  - delivery box;
  - scooter side panel (or simply remove the scooter-panel logo).

  Do this at the composite's native size, then check it at 300 dpi against the SVG.
- **Who fixes it:** corporate-designer. Alternatively, the Creative Director rules (option b above).
- **Related:** the same malformed logo is on the cleaning-team mockup (p11, uniforms, small) and the car/scooter image. Whatever the CD decides for p12 should apply there too.

**Minor**

- **m1. p12 truck, rear end of the box.** The cut-out leaves a small step in the right-hand edge of the box at about mid-height. The silver top rail and the rear corner trims of the box were removed with the background, so the box reads as a flat dark slab. Clean the mask at the rear corner and restore the rail from the source. Corporate-designer.
- **m2. p12, light does not match.** The car and scooter come from an overcast scene with flat light; the truck is in harder sun with a dark under-chassis shadow. The contact shadows are generic. Soften the truck's under-chassis shadow, or give the car and scooter a slightly firmer shadow. Faint towers still show in the truck's windscreen. Corporate-designer.
- **m3. p12 composite sharpness.** It runs at 147 ppi across 297 mm, so the logos on it are soft at zoom. This is acceptable for screen; fold it into the M1 rebuild.
- **m4. List wrapping (r3 m1) only partly fixed.** p8 "Maintenance of parks / and street trees" and "Maintenance of / irrigation equipment" still wrap, as does p9 "Operation and / maintenance of lift systems". Minor; fine-tune the column widths. Corporate-designer.
- **m5. p16 text column.** The column holds only the number and the two titles; below them is about 120 mm of white space. With the scope unconfirmed this is acceptable. Optionally lower the title block to the photos' vertical centre so the page reads as one composition.
- **m6. Still open from earlier rounds:**
  - bus-shelter original file (p14);
  - two non-Gulf tiles (p8, p10);
  - faint partner logos and the cut The End logo;
  - the "single contract" line (p13 point 01);
  - Dar Al Taqwa scope;
  - native Arabic proofread;
  - PDF not tagged for accessibility.

### Overall view against the client's bar

v07 delivers what the client asked for. The single logistics image is a real improvement over six separate pictures, and Dar Al Taqwa now has a proper page. Once the vehicle logos are corrected, p12 will be one of the strongest pages in the book. With the logos as they are, it puts a wrong version of the client's own mark at the largest size it appears on any inside page.

### The three changes that would most raise the level

1. Put the real wordmark on every vehicle in the p12 composite (M1) and clean the truck's rear edge (m1).
2. Get the client's own photographs and files: site, staff and fleet photos, the bus-shelter original, and official partner logos.
3. Final craft pass on the list wrapping (m4) and the p16 title placement (m5).

### Not checked

- No native Arabic proofreading.
- The PDF was not opened in a second viewer; I rendered it with poppler only.
- PDF bookmarks were not checked against the new page map.
- The HTML source was not opened from a copied location.
- I did not inspect the maker's GrabCut masks or `_work/v07/composite_200pct.png` separately; I judged the composite from the PDF at 300 dpi and from `assets/derived/v07_logistics_fleet-composite.png`.
- Licence terms were not checked against the live source pages.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 4 of company profile v07 (screen PDF, ar-en)
Status: DONE
Files produced: none in the repo. Scratch files are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/:
- check_arabic previews in review_v07/ and 150 dpi pages in v7/
- contact sheets s7a.png, s7b.png, s7c.png
- 300 dpi p12 crops z12_*.png and p16 crop z16room.png
- logo comparison logo_compare.png (client mockup truck logo above, identity wordmark below)
Tool operations: `check_arabic_pdf.py` on v07 returned PASS. pdfinfo, pdftotext and pdftoppm at 150 and 300 dpi were run read-only. A Pillow/numpy colour isolation of the truck logo from `06-profiles/assets/derived/mockup_logistics-trucks_retouched_v03.png` was saved to scratch only. HTML text diff v06 → v07. No Figma or Canva operations.
Decisions needed:
1. M1: fix the vehicle logos with the real wordmark (recommended), or record an explicit ruling extending m9 to logo shapes inside the client's illustrative mockups and tell the client they are AI approximations.
2. Apply the same decision to the other mockups (p11 cleaning team).
Assumptions: the identity wordmark in `04-identity/02-logo/` is treated as the reference drawing of the logo; it was extracted from the client's original profile and has been in use since 2026-11-13.
Issues / risks: verdict FAIL — 0 critical, 1 major (vehicle logos on p12), 6 minor. I missed the logo-shape issue in r1–r3, and the earlier m9 ruling covered colours only.
Suggested next agent: corporate-designer, to rebuild the p12 composite with the real wordmark perspective-placed on the truck box, cab, car door and delivery box (inputs: `assets/derived/v07_logistics_fleet-composite.png` sources and masks in `_work/v07/`, `04-identity/02-logo/*.svg`, `04-identity/03-system/system.md` colour-on-ground rules), and to fix m1 and m4. Then quality-reviewer for r5, limited to p12 and any changed pages.

