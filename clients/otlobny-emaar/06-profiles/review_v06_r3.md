## Quality review: otlobny-emaar company profile v06 (screen, ar-en), r3, 2026-11-14

**Verdict: PASS WITH MINOR FIXES.** Both r2 majors are fixed, there are no critical issues, and none of the ten points fails.

**Can it go to the client? Yes, as a reviewed draft (v06), on these conditions:**
1. Present it as a draft for the client's review, not as final.
2. In the same message, ask the open client questions (listed under "Conditions" at the end).
3. Before anything is renamed `final` or enters `08-final-delivery/`, three things must still happen: the client approves the piece, a native Arabic reader proofreads it, and the package gets its own delivery-checklist review.

The minor issues below do not block a draft review. Fold them into the next version together with the client's feedback.

**Against the client's bar ("world-class, visual delight, not مشي حالك"):**
- **What works:**
  - The cover is now strong and credible: a steel-frame hero (a literal «إعمار»), a Gulf site workforce, a Gulf tower with palms, rope access on a glass tower, and the Riyadh museum park.
  - The diamond lattice is consistent across the book and the bilingual craft is clean.
  - It no longer reads as "مشي حالك".
- **What still separates it from truly world-class:** photography. The book still relies on small stock tiles and AI mockups, and the works section rests on three low-resolution client images. Only the client's own photographs of his sites, staff and fleet can close that gap; design changes cannot.

### What I checked

Everything is under `/home/user/arwa/clients/otlobny-emaar/`.
- **Arabic check:** I ran `python3 scripts/check_arabic_pdf.py` on `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v06.pdf`. Result: PASS. 20 pages at 297 × 210 mm. Fonts are Tajawal Regular/Medium/Bold/ExtraBold and IBM Plex Sans Regular/Medium/SemiBold/Bold, all embedded, no fallback. 4,494 Arabic characters, no presentation forms.
- **Rendering:** all 20 pages at 150 dpi, viewed one by one or on contact sheets I built myself. p16 again at 300 dpi.
- **Images:** I read the image sources per page in `_work/build_v06.log` myself. No source appears on more than one page. The technician image is gone from both the pages and the credits.
- **Text:** a PDF search finds no Shahd/«شهد», «أطلبني», TAIBA, THERMO, lorem, TBC or "157th".
- **Copy changes:** I diffed every text string in the v05 and v06 HTML. Copy changed only in the kicker separators (· → –), two image alt texts, the version in the title, and the removal of the technician credit. All of it is correct in both languages.

### Round 2 items, verified independently

| r2 item | Status | Evidence |
|---|---|---|
| M1 cover credibility | FIXED | p1: steel erector hero (202 ppi) plus the Gulf workforce tile. The technician is no longer used anywhere. The glass facade moved to p7 as the contracting image (416 ppi). |
| M2 p16 composition | FIXED | Two columns, one per work, image tops aligned. Caption-to-heading gap is about 11 mm (Chamber) and about 12 mm (Dar Al Taqwa). Still no Dar Al Taqwa scope (C1 holds). Dar Al Taqwa photo is 62 mm wide at 137 ppi: soft at 300 dpi but acceptable on screen. |
| m1 kicker separator | FIXED | Now «03 – خدماتنا – 01 / 06» on pp7–12, 17 and 18. No raised dot. |
| m2 diamonds stopping near the edge | FIXED | Outer diamonds on pp7–12 now bleed off the page. |
| m3 list alignment and widows | FIXED, with a small regression | First baselines are aligned and «للمستشفيات» / «أجير» no longer sit alone. But the narrower English column now wraps short English items (see m1 below). |
| m4 bus shelter (p15) | OPEN, source-limited | 105 mm at 133 ppi, as stated. Needs the client's original file. |
| m5 p13 truck logo | FIXED | The front three-quarter truck shows the complete logo on the box. |
| m6 non-Gulf tiles | OPEN, by the maker's statement | p8 San Diego bay planting and p10 red-brick rope-access cleaner remain. |
| m7 faint partner logos | OPEN, needs client files | Unchanged; The End is still cut at its edge. |
| m8 contents numbers | FIXED | Arabic-side section numbers removed. |
| m9 "single contract" line | OPEN, pending the client | Still on p14, point 01. |

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | One idea, "one large image, several small", carried by the diamond lattice from the cover through pp7–12. The cover hero now states «إعمار» directly. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; the brief puts competitors out of scope. |
| 3 | Colour and contrast | PASS | Brand colours only. Footers #5F6573 at 5.84:1 on white and 5.50:1 on the tint; p19 labels white at 82% on navy; p20 credits #525456 at 7.61:1 (unchanged from v05, which I measured in r2). |
| 4 | Arabic and English typography | PASS | check_arabic PASS; letters connected and right to left on every page; no tracking on Arabic; consistent dash separators. |
| 5 | Logo clarity | PASS | Colour wordmark on p1 and p20, white on p2, reversed on p19. Always used alone. Logo now complete on the p13 truck. |
| 6 | Layout | PASS | p16 resolved, edge diamonds bleed, list rules and baselines aligned. Minor points in m1 and m2 below. |
| 7 | Consistency across pages | PASS | One numbering scheme (01–07), one service master, matching stacked captions on p15 and p16, one grade on all stock. |
| 8 | Accuracy | PASS | Every factual line traces to `content-outline.md` or the original profile. Dar Al Taqwa states no scope. Contact details match `brand-context.md`. Every credited photo is in the book and every attributable photo is credited. No spelling errors in either language. |
| 9 | Export quality | PASS | Screen PDF with ICC/sRGB and grey images, fonts embedded, 10.9 MB, file name follows `file-delivery.md`. Not tagged for accessibility (minor, unchanged). |
| 10 | Matches client requirements | PASS | Collage cover; name without hamza; logo alone; nothing from the website; four logistics services; 32 partners in the right order (16 + 16); Dar Al Taqwa replaces Shahd; credited open-licence photos; PDF, HTML and previews. |

### Issues (all minor)

- **m1. pp8, 9, 10, 11: narrower English list column (regression from the m3 fix).** With the columns at 0.86 / 1.14, short English items now wrap where they did not before. Examples: p8 "Landscaping of / planted gardens"; p9 "Operation and / maintenance of central / air-conditioning systems" (three lines); p10 "Pest and insect control / for all government / and private facilities" (three lines). Fix: about 0.95 / 1.05, or keep 0.86 / 1.14 only on p11, where the Arabic needs the room. Corporate-designer.
- **m2. p16, left column (Dar Al Taqwa).**
  - The photo sits at the right edge of its column, leaving an empty block of about 60 × 110 mm at top left.
  - The English title "Dar Al Taqwa Hotel" sits about 11 mm lower than the Arabic title and alone near the footer.

  This is acceptable but slightly loose. Fix: centre the photo in its column, or align the title stack under the photo's own width. Corporate-designer.
- **m3. Cover balance of services.** Three of the five frames are construction (hero, tower, workforce), plus one cleaning and one landscaping. Maintenance and logistics are absent. This is optional; consider swapping the tower tile for the warehouse aisle or the rooftop AC units, keeping the no-repeat rule. Art-director, optional.
- **m4. p15 bus shelter** is soft at 133 ppi. It needs the client's original file. Creative Director to request it.
- **m5. p8 and p10 non-Gulf tiles** (San Diego bay, red-brick building). Replace if a new sourcing round or the client's own photos allow. Art-director.
- **m6. Faint partner logos and the cut The End logo (pp17–18).** Needs official files from the client.
- **m7. p14 point 01, "under a contract with a single company / في عقد مع شركة واحدة"** is still an agency draft [D]. It must be confirmed or removed before final.
- **m8. PDF not tagged for accessibility.** Acceptable for a screen draft; note it for final if the client needs it.

### Spelling and proofreading

- **English:** no errors.
- **Arabic:** no spelling errors. «اطلبني» never takes a hamza, Arabic punctuation is used, numerals are Western, and diacritics are consistent (tanwin only).

### The three changes that would most raise the level (unchanged in substance)

1. **The client's own photographs:** sites, staff in real uniforms, fleet, and finished works (larger Dar Al Taqwa and bus-shelter originals). This is now the single biggest lever by far.
2. **Rebalance the cover across the six services** (m3), and replace the two non-Gulf tiles (m5) as soon as better images exist.
3. **Final craft pass:** the English list column width (m1) and the p16 left-column alignment (m2).

### Conditions for sending v06 to the client as a reviewed draft

Send the PDF with a short note that it is draft v06, and ask the client for:
1. The service scope at Dar Al Taqwa, and a larger photo of it.
2. Confirmation of the "one contract with a single company" line on p14.
3. The original bus-shelter photo.
4. Official partner logo files, especially Dar Al Taqwa, Al Madinah Harmony, the award foundation, Taibah Cooperative, and a complete The End file.
5. His own site, staff and fleet photographs.
6. Confirmation of the name, its Latin spelling and the legal form («شركة اطلبني إعمار» / "OTLOBNY Emaar Co."); still an assumption in `brand-context.md`.
7. Approval of the English copy, which the client has not yet seen.

Also tell him plainly that:
- the service photographs are licensed stock, credited on p20;
- the images labelled «صورة توضيحية» are illustrative and do not show real vehicles or staff.

### Not checked

- No native Arabic proofreading. Required before final, not before a draft review.
- Guillemet direction (standard Chromium rendering) still needs the native proofreader's confirmation.
- The PDF was not opened in a second viewer; I rendered it with poppler only.
- The HTML source was not opened from a copied location.
- Licence terms were not checked against the live source pages; I relied on the stock README and credits and on the build log.
- No competitor comparison, because there is no research in `02-research/`.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 3 of company profile v06 (screen PDF, ar-en) against r2
Status: DONE
Files produced: none in the repo. Scratch renders are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/: the check_arabic previews in review_v06/, 150 dpi pages in v6/, contact sheets s6a.png to s6d.png, and the 300 dpi p16 crop x16c.png.
Tool operations: `check_arabic_pdf.py` on v06 returned PASS (previews in scratchpad/review_v06). pdffonts, pdfinfo, pdftotext and pdftoppm at 150 and 300 dpi were run read-only. I read `_work/build_v06.log` for image sources per page and diffed the v05 and v06 HTML text in scratch only. No Figma or Canva operations.
Decisions needed:
1. Send v06 to the client now as a reviewed draft, with the seven questions above (recommended: yes).
2. Whether to apply minors m1 to m3 before sending or in the next round with the client's feedback (recommended: next round; they do not block a draft).
3. Arrange a native Arabic proofread before any final version.
Assumptions: Tajawal and IBM Plex Sans are treated as the working typefaces (brand-context section 5 is still blank). Contrast values for p19 and p20 are carried over from my r2 measurements, since the colours and backgrounds are unchanged.
Issues / risks: verdict PASS WITH MINOR FIXES — 0 critical, 0 major, 8 minor. Not a final approval. Open: native proofreading, second-viewer check, and the client confirmations listed above.
Suggested next agent: Creative Director, to present v06 to the client with the open questions. Corporate-designer afterwards, for m1 and m2 plus client feedback, as v07. Quality-reviewer again before any final, and for the 08-final-delivery package review.

