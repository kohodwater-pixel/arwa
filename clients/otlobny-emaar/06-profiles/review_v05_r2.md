## Quality review: otlobny-emaar company profile v05 (screen, ar-en), r2, 2026-11-14

**Verdict: FAIL, but close.** There are no critical issues and two major ones, both narrow and quick to fix:
- **M1:** one cover photo undercuts regional credibility.
- **M2:** the Madinah Chamber / Dar Al Taqwa works page (p16) is unresolved.

With those two fixed, I expect a PASS WITH MINOR FIXES on round 3.

**Overall view:** v05 is a clear lift over v04 and much closer to the client's "world-class, visual delight" bar.
- The diamond lattice now carries the whole book.
- Bilingual lists are clean, numbering is consistent, and no image appears on two pages.
- Contrast passes everywhere I measured.
- The work no longer looks "مشي حالك".
- What keeps it short of world-class: the photography is still mostly small, generic stock, and the works section is thin. Only the client's own site, staff and fleet photographs can fix the latter.

**Process note for the CD:** the 2026-11-14 entry in `brand-context.md` says v04 was "sent to the client as a draft", which sounds like before r1. If so, it broke the rule that every deliverable is reviewed before the client sees it.

### What I checked

Everything is under `/home/user/arwa/clients/otlobny-emaar/`.
- **Arabic check:** I ran `python3 scripts/check_arabic_pdf.py` on `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v05.pdf` myself. Result: PASS. 20 pages at 297 × 210 mm. Fonts are Tajawal Regular/Medium/Bold/ExtraBold and IBM Plex Sans Regular/Medium/SemiBold/Bold, all embedded, no fallback. 4,494 Arabic characters, no presentation forms.
- **Rendering:** all 20 pages at 150 dpi, viewed one by one. Pages 1, 7, 15 and 16 again at 300 dpi for detail.
- **Text:** proofread every unique string from the v05 HTML in both languages. A PDF text search finds no "Shahd", «شهد», «أطلبني», TAIBA, THERMO, lorem or TBC.
- **Images:** every image source per page from `_work/build_v05.log`, checked by me. No source appears on more than one page. Every 1024 px stock file sits at 70.7 mm or less, at 244 ppi or more.
- **Credits:** every image that needs attribution is credited on p20, and the public-domain/CC0 files are listed separately.

### Round 1 items, verified independently

| r1 item | Status | Evidence |
|---|---|---|
| C1 Dar Al Taqwa scope | FIXED | p16: hotel name and photo only. No sentence, no scope chips. |
| M1 contrast on the credits and contact page | FIXED | p19 is flat navy with labels in white at 82%. Credits moved to the white p20, in grey #525456 at 7.61:1. English credits 7 pt, Arabic 8.5 pt. |
| M2 bilingual list alignment | FIXED | pp7–12: one rule runs across both columns. See m3 for a small residue. |
| M3 p13 duplicating p12 | FIXED | p13 is now pictures only, with «صور توضيحية» / "Illustrative images". |
| M4 repeated photo and off-topic tile on p9 | FIXED | p9: HVAC hero, rooftop AC units, distribution board. HVAC appears only here. |
| M5 regional credibility and image quality | PARTLY FIXED | **Gone:** Torquay lawn, European gardener, beanie rebar worker, Danish reefer truck (THERMO KING), blurred forklift, hazy scrubber, dull date palm, blue-hour site, and the TAIBA FRONT HOTEL sign (cropped out). **Added, Gulf-credible:** Riyadh museum park, Doha palm walkway, tower with palms, Gulf site workforce. **Still weak:** see M1 below and m6. |
| M6 works pages | PARTLY FIXED | Chips no longer wrap and captions are consistent. p16 has a new problem (M2 below). The p15 photo is smaller than in v04, not larger (105 mm, 133 ppi). |
| m1 section numbering | FIXED | 01–07 are consistent across kickers, contents and footers. |
| m2 work captions | FIXED | Same wording on each works page; the Chamber image is honestly labelled «تصور معماري مقدم من العميل» / "Architectural rendering supplied by the client". |
| m3 "illustrative" labels | FIXED | pp11, 12 and 13 are labelled; the p20 note says the illustrative images do not show real vehicles or staff. |
| m4 widows | FIXED in headings | p15 and p16 headings now fit on one line. Small residue in lists (m3 below). |
| m5 cover alignment | FIXED | The logo's right edge lines up with the Arabic title column. |
| m6 fact-strip baselines | FIXED | p3 values sit on the same baseline. |
| m7 overview numbers | FIXED | p6 now says "PAGE 07" and so on. |
| m8 partner logos | PARTLY FIXED | The grid is closed and the heavy marks are slightly reduced. Faint low-resolution logos and The End's cut edge depend on the client's files. |
| m9 logo colours inside mockups | ACCEPTED | CD ruling. |
| m10 bus-shelter litter | FIXED | Cropped out; I verified at 300 dpi. |
| m11 credits detail | FIXED | Correct Commons title, separate toolstop entry, share-alike wording added. |
| m12 "single contract" line | OPEN BY RULING | Still on p14, pending the client (see m9 below). |
| m13 shadda | FIXED | No harakat; only tanwin «ـاً» remains, consistently. |
| m14 English polish | FIXED | All four suggested rewrites are in. |

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | "One large image, several small" now runs as one diamond lattice: cover, p2 and p4 patterns, and the service clusters on pp7–12. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; the brief says competitors are out of scope. |
| 3 | Colour and contrast | PASS | Brand colours only. Footers #5F6573 at 5.84:1 on white and 5.50:1 on the tint; p19 labels about 9:1; p20 credits 7.61:1; green kicker on navy 5.83:1. |
| 4 | Arabic and English typography | PASS | check_arabic PASS; letters connected and right to left on every page; no tracking on Arabic. Small middle-dot issue in the kickers (m1). |
| 5 | Logo clarity | PASS | Colour wordmark on the cover and p20, white on p2, reversed on p19. Always used alone. |
| 6 | Layout | FAIL | p16 is crowded and unbalanced (M2). Smaller points in m2 and m3. |
| 7 | Consistency across pages | PASS | One numbering scheme, one service master, consistent captions and grade. |
| 8 | Accuracy | PASS | Every factual line traces to `content-outline.md` or the original profile. Dar Al Taqwa states no scope. Contact details match `brand-context.md`. No spelling errors found in either language. |
| 9 | Export quality | PASS | Screen PDF with ICC/sRGB and grey images, fonts embedded, 11.3 MB, file name follows `file-delivery.md`. Not tagged for accessibility (minor, as before). |
| 10 | Matches client requirements | PASS | Collage cover; name without hamza; logo alone; nothing from the website; four logistics services; 32 partners in the right order (16 + 16); Dar Al Taqwa replaces Shahd; open-licence photos credited; PDF, HTML and previews. |

### Issues

**Major**

**M1. p1 cover, bottom-right photo diamond: regional credibility.**
- **What is wrong:** the only face on the cover is a fair-skinned U.S. Air National Guard technician ("157th Airmen", public domain) in safety glasses and earplugs. For a Madinah company addressing Saudi buyers, the most prominent person on the cover reads as a foreign military technician. The other cover tiles work (Gulf tower with palms, rope-access team on a glass tower, Riyadh park). The hero (an abstract blue glass facade) is neutral but says nothing about the services or the place.
- **Fix:** swap the technician for a Gulf-credible image already in the library and not used elsewhere, or move one between pages so nothing repeats. Options: the rooftop AC units with a technician (currently p9), or the Gulf site workforce (currently p11), replacing it on that page with an unused tile. Optionally reconsider the hero; the steel erector (now on p7) said «إعمار» more directly.
- **Who fixes it:** art-director to choose, corporate-designer to place.

**M2. p16, works 02 and 03 sharing one page: composition and hierarchy.**
- **What is wrong:**
  - The right column is packed from top to bottom: image, a two-line caption, then the "02 / 03" heading only about 3 mm below the caption, so the caption reads as belonging to the next heading.
  - The left column, Dar Al Taqwa, holds a title and a photo, and its lower half is empty (from about 135 mm down to the footer).
  - The page looks unresolved rather than designed.
- **Fix (either):**
  - Give each work equal weight: two matching columns, each with image, caption, title and text, and at least 8 mm between a caption and the next heading. Dar Al Taqwa's lack of body text is then balanced by a larger photo.
  - Or move the Chamber caption under the image with the same spacing as p15, and set Dar Al Taqwa's title block and photo so the column fills deliberately.
- **Who fixes it:** corporate-designer.

**Minor**

- **m1. Arabic kickers, pp7–12, 17, 18.** The «·» between «خدماتنا» (or «شركاء النجاح») and the page fraction renders raised, almost superscript, in Tajawal next to the larger digits. Use the same separator and size as the footers, or a short dash.
- **m2. Diamond near-misses at the page edge.** The lower-left diamond on p7 and p9 stops about 3.4 mm from the left edge, and the right-hand diamonds on pp8, 10 and 12 stop about 3.6 mm from the right edge. They neither bleed nor respect the 18 mm margin, so they look accidental. Either bleed them or pull them inside the margin.
- **m3. Bilingual list cells are vertically centred, so first lines do not share a baseline.** Examples: p10 row 2, p11 row 1, p8 rows 3–4. The narrow Arabic column also breaks «للمستشفيات» onto a line of its own (p11). Top-align both cells, and widen the Arabic column slightly or shorten the line.
- **m4. p15 bus-shelter photo is soft and small.** It is 133 ppi at 105 × 90 mm, with JPEG artefacts visible on zoom. The left half of p15 is still about 35% empty. Ask the client for the original photo file; meanwhile consider a slightly larger frame with the image at its native sharpness.
- **m5. p13 top-right truck.** The «اطلبني» logo on the truck box is cut by the frame edge. Reframe so the client's logo is complete.
- **m6. Remaining non-Gulf stock.**
  - p10: the rope-access cleaner on a red-brick building.
  - p8: the San Diego bay planting with yachts.

  Neither is wrong, but each could be replaced if round-3 sourcing finds better. The client's own photographs remain the real fix.
- **m7. Partner logos (pp17–18).** Dar Al Taqwa, Harmony, the award foundation and Taibah Cooperative are still faint, and The End is still cut. This depends on the client's files.
- **m8. p2 contents.** Each row shows two section numbers plus a page number; this is busy but readable. Consider dropping the Arabic-side section number.
- **m9. p14 point 01, "under a contract with a single company / في عقد مع شركة واحدة".** Still an agency draft [D] awaiting the client (CD ruling). It must be confirmed or removed before final.

**Who fixes the minor issues:** corporate-designer, except m4 and m7 (client files, via the Creative Director), m6 (art-director, if sourcing finds better) and m9 (client confirmation).

### Spelling and proofreading

- **English:** no errors. The phrasing fixes from r1 are in.
- **Arabic:** no spelling errors found. «اطلبني» never takes a hamza. Arabic punctuation is used, numerals are Western throughout, and the shadda/harakat treatment is consistent.

### The three changes that would most raise the level

1. **Real photographs from the client:** his own sites, team, uniforms and fleet. Nothing else would move the book from very good stock design to a profile that proves the company. Meanwhile, swap the cover technician (M1).
2. **Fix the works section into a confident proof spread.** Balance p16 (M2), enlarge the work photos at their native sharpness, and get a larger Dar Al Taqwa photo and its confirmed scope from the client.
3. **Finish the lattice craft:** bleed or inset the edge diamonds (m2), top-align the bilingual list cells (m3), and fix the kicker separator (m1). These are small things a world-class reader notices.

### Not checked

- No native Arabic proofreading; one is still required by `arabic-design.md`.
- Guillemet direction (Chromium standard rendering, see r1) still needs the native proofreader's confirmation.
- The PDF was not opened in a second viewer; I rendered it with poppler only.
- The HTML source was not opened from a copied location.
- Licence terms were not checked against the live source pages; I relied on the stock README and credits and on the build log.
- No competitor comparison, because there is no research in `02-research/`.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 2 of company profile v05 (screen PDF, ar-en) against r1
Status: DONE
Files produced: none in the repo. Scratch renders are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/: the check_arabic previews in review_v05/, 150 dpi pages in v5/, and 300 dpi pages and crops (w1-01.png, w7-07.png, w15-15.png, w16-16.png, y_*.png).
Tool operations: `check_arabic_pdf.py` on v05 returned PASS (previews in scratchpad/review_v05). pdfinfo, pdffonts, pdfimages -list, pdftotext and pdftoppm at 150 and 300 dpi were run read-only. I read `_work/build_v05.log` to check image sources per page. No Figma or Canva operations.
Decisions needed:
1. M1: which Gulf-credible image replaces the cover technician. Recommendation: the rooftop AC technician or the Gulf site workforce, back-filling that page with an unused image.
2. Whether to ask the client now for his own site, staff and fleet photos and the original bus-shelter file (recommended).
3. m9: the "single contract" line on p14 needs the client's confirmation before final.
4. Process: confirm whether v04 reached the client before r1, and keep the review-before-client order from now on.
Assumptions: Tajawal and IBM Plex Sans are treated as the working typefaces (brand-context section 5 is still blank). Contrast ratios for p19 and p20 come from the CSS colours and the flat backgrounds I saw in the renders.
Issues / risks: verdict FAIL — 0 critical, 2 major, 9 minor. No native Arabic proofreading and no second-viewer check yet.
Suggested next agent: corporate-designer, to fix M2 and m1–m3 and m5 as v06. Art-director first, for M1 (cover image swap, keeping the no-repeat rule). Then quality-reviewer for r3.

