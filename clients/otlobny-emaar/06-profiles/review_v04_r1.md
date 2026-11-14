## Quality review: otlobny-emaar company profile v04 (screen, ar-en), r1, 2026-11-14

**Verdict: FAIL.** There is one critical issue and six major ones. The critical one is quick to fix. The majors are mostly craft and photography, not structure.

**Overall view:** v04 is a real step up from v03. The diamond collage cover does what the client asked for (one large image with several small ones). The type system is clean and the Arabic is well set. The client's binding rulings are almost all met. It is not yet world-class. What holds it back:
- The photography: many images look European rather than Gulf, several are repeated, and some are dull or soft.
- Bilingual lists whose dividing lines do not line up.
- A duplicated logistics page.
- Weak, empty pages in the works section.

All the files I checked are in `/home/user/arwa/clients/otlobny-emaar/`: the v04 PDF and HTML, `brand-context.md`, `01-brief/brief.md` (addenda 1–6), the original pages p01, p17, p19 and p20, `06-profiles/content-outline.md`, `content-gaps.md`, `build-notes_v04.md`, `_work/build_v04.log`, and `assets/stock/CREDITS.md` and `README.md`. I rendered every page at 150 dpi and pages 1, 4, 10, 12–16 at 300 dpi, and looked at each one.

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | One idea ("one large image, several small") runs from the cover diamond lattice through every service page. It is shallowed by the photography (issues M5, M6). |
| 2 | Distinctiveness | N/A | `02-research/` is empty and the brief says competitors are not needed for this scope. The cover follows the client's old cover by request. No borrowed marks. |
| 3 | Colour and contrast | FAIL | Only brand colours are used. But on p20 the Arabic credits (#9BABD7, 7 pt) measure 4.1:1 against the sampled background #2a4386. AA needs 4.5:1. |
| 4 | Arabic and English typography | PASS | `check_arabic_pdf.py`: PASS. Fonts are Tajawal 400/500/700/800 and IBM Plex Sans 400/500/600/700, all embedded, no fallback. 4,057 Arabic characters, no presentation forms. Letters connected and right to left on all 20 pages. No tracking on Arabic. |
| 5 | Logo clarity | PASS | Colour wordmark alone on the cover, white on p2, reversed (green) on navy on p20, with nothing written under it. Usage matches `04-identity/03-system/system.md`. |
| 6 | Layout | FAIL | Arabic and English list rules do not align on pp7–12 (drift of up to 6 mm). p13 repeats p12's title and list. Large dead areas on p9 and pp15–17. Widowed words in the headings on p15 and p16. |
| 7 | Consistency across pages | PASS (minor issues) | Grid, type scale, footers and colours are consistent. The section numbering and caption wording are not (issues m1, m2). |
| 8 | Accuracy | FAIL | p17 states as fact that Dar Al Taqwa received maintenance and cleaning. `brand-context.md` and `content-outline.md` mark this as an ASSUMPTION. Every other factual line traces to the content outline (tags [V]/[E]) or to the original pages. No «شهد»/Shahd, «أطلبني», «الشركة المختارة», «رائدة», lorem or TBC anywhere (count 0). |
| 9 | Export quality | PASS | 20 pages at 297 × 210 mm. Images are ICC/sRGB or grey. All fonts embedded. 12.9 MB. The file name follows `file-delivery.md`. Not tagged for accessibility (minor). |
| 10 | Matches client requirements | PASS | All of these are present and correct: the collage cover; the name «اطلبني إعمار» without hamza; the logo alone; nothing from the website (no WhatsApp); logistics with exactly four services; 32 partners in order (original 18 in their original sequence, then 9, then 3, then Le Méridien and Al Esra Cabin); Dar Al Taqwa replaces Shahd; open-licence photos credited; PDF, HTML source and PNG previews. |

### Issues

**Critical**

**C1. p17, body text and scope chips.**
- **What is wrong:** «قدمت «اطلبني إعمار» خدمات الصيانة والنظافة لفندق دار التقوى» / "provided maintenance and cleaning services for Dar Al Taqwa Hotel", plus the «صيانة / نظافة» and Maintenance / Cleaning chips. The scope is an assumption carried over from Shahd (brand-context 2026-11-14; content-gaps item f), but it is shown as fact.
- **Rule broken:** honesty rules; quality-standards (Accuracy).
- **Fix:** before the client sees the page, either get the client to confirm the scope (one question), or remove the scope sentence and chips and keep only the hotel as a work, which the client stated.
- **Who fixes it:** Creative Director to ask the client; corporate-designer to edit.

**Major**

**M1. p20, photo credits and contact labels: contrast.**
- **What is wrong:**
  - Arabic credits are #9BABD7 at 7 pt on the lighter bottom-right of the gradient: 4.1:1 at the sampled #2a4386. This fails AA.
  - The English credits are 6 pt and reach only 4.55:1 at their right end, which is barely legible on screen.
  - The Arabic contact labels (الهاتف, البريد الإلكتروني…, 9 pt) measure 4.38–4.53:1, which is borderline.
- **Rule broken:** quality-standards (WCAG AA).
- **Fix:** set credit text and labels to white at 70–85% opacity (5.3:1 or better everywhere), or end the gradient darker behind the credits. Raise the English credits to at least 7 pt and the Arabic to at least 8 pt; split them into two columns if needed.
- **Who fixes it:** corporate-designer.

**M2. pp7, 8, 9, 10, 11, 12: paired Arabic and English bullet lists.**
- **What is wrong:** the Arabic rows are taller (11 pt / 1.55) than the English rows (8.8 pt / 1.5), so the hairlines side by side do not line up. On p7 the drift reaches about 6 mm by row 5 (English rule at about 160 mm from the top, Arabic at about 169 mm). On pp9–11 two-line items make it worse. Two parallel ruled lists that are out of step read as a mistake.
- **Rule broken:** design-checklist (consistent grid); project-review point 6.
- **Fix:** put each Arabic and English item in one shared grid row (one row per item, the height set by the taller cell), so every rule runs across both columns at the same height. Alternatively, use one bilingual table per service.
- **Who fixes it:** corporate-designer.

**M3. p13 (Logistics "in pictures") duplicates p12.**
- **What is wrong:** the same title «الخدمات اللوجستية» / Logistics Services, the same kicker "06 / 06", and the same four-item list in both languages appear on two consecutive pages. The reader sees the same content twice.
- **Fix:** make p13 a purely pictorial fleet page: three truck views plus the rider, the «صور توضيحية» / "Illustrative images" label, and at most a one-line caption. Drop the repeated title and list, or change the kicker to something like «أسطولنا في صور» (wording for the CD to approve, as a caption only; no fleet claims).
- **Who fixes it:** corporate-designer.

**M4. p9 (Maintenance) photo panel.**
- **What is wrong:**
  - Tile 1 is a tighter crop of the same HVAC photo used as the hero beside it.
  - The same photo also appears on the cover and on p6, so it is used four times in the book.
  - Tile 2 (a building under construction at blue hour, with a crane) shows construction, not maintenance.
- **Fix:** replace both tiles with different maintenance subjects (lift or plant room, technician with tools, AC unit service). If the library has nothing suitable, source them in a new art-director round.
- **Who fixes it:** art-director (sourcing), then corporate-designer.

**M5. Photography: regional credibility and quality (cover, pp6, 7, 8, 10, 12).**
- **What is wrong:** for a Madinah company selling to Saudi government and corporate buyers, many images read as northern Europe:
  - cover palm tile and p8 tile 1: a lush English lawn ("Torquay Palms");
  - p8 tile 2: a European gardener in dense green woodland;
  - p7 hero: a worker in a beanie and camouflage trousers in winter;
  - p12 tile 1: a Danish Mercedes reefer truck with "THERMO KING", the Mercedes star and an operator name on the door still legible at 300 dpi;
  - p4: "TAIBA FRONT HOTEL" signage legible in the hero.

  Weak frames:
  - p8 hero: a date palm under a flat white sky (the maker notes this too);
  - p10 hero: a floor scrubber shot through glass, hazy and low in contrast;
  - p12 tile 2: the forklift is mostly motion blur.

  The "one brand grade" is not visibly consistent: the cover palm tile is saturated green next to graded tiles.
- **Rule broken:** quality-standards ("right for the audience"); the client's "choose images carefully" instruction.
- **Fix:** run a second sourcing round aimed at arid, Gulf-looking settings (Wikimedia Commons Saudi and GCC landscaping, street palms, municipal works, cleaning). Replace the European-looking frames above. Retouch or crop out third-party marks (THERMO KING, the door lettering, the p4 hotel sign). Apply one visibly uniform grade. Above all, ask the client for real photographs of his own sites, staff and fleet.
- **Who fixes it:** art-director (sourcing and grade), then corporate-designer; Creative Director to ask the client for his own photos.

**M6. Works pages p15, p16, p17: composition.**
- **What is wrong:**
  - The lower 40–50% of each page is empty (p15 below y ≈ 150 mm; p16 below y ≈ 160 mm).
  - p17 is a 40 mm photo in a tint band with three blocks floating around it.
  - p17's title structure ("Our Work" + hotel name) differs from p15 and p16, where the project name is the title.
  - On p16 the English chips wrap onto two lines while the Arabic chips stay on one.

  This is the proof section and it reads as the weakest part of the book.
- **Fix:**
  - Use one works master on all three pages, with the project name as the title.
  - Enlarge the images. The bus shelter photo (950 px) can run at about 150 mm on screen.
  - Consider a two-page works spread (bus shelter large, Chamber and Dar Al Taqwa as a pair) instead of three thin pages, with the freed page given to stronger imagery.
  - Stop the chips from wrapping.
- **Who fixes it:** corporate-designer.

**Minor**

- **m1. Section numbering is inconsistent.** p3 = 01, p4 = 02, p5 = 02 again, p6 = 03, p14 = 04, the works pages have no number, partners = 05. The English kickers on pp3–5 show only the number, while p6 and p14 show a label plus the number. The p18–19 English kicker leaves out the "05" that the Arabic shows. Fix: one numbering scheme (for example 01 About, 02 Vision/Mission/Goals, 03 Services, 04 Why, 05 Work, 06 Partners) in the same format in both languages.
- **m2. Caption wording differs across the works pages.** p15 "PROJECT PHOTOGRAPH / صورة من أعمال الشركة", p16 "IMAGE SUPPLIED BY THE CLIENT / صورة من العميل", p17 "HOTEL ENTRANCE / مدخل الفندق". Also «صورة من العميل» is clumsy; prefer «صورة مقدّمة من العميل». p16's image is an architectural rendering, so its caption should say so honestly.
- **m3. "Illustrative" labelling is uneven.** p13 marks the client's AI-generated vehicle images as «صور توضيحية», but the same family of images (p6, p11 team hero, p12 car/scooter hero) is unlabelled, and the p20 credits call them "team images: the client". Fix: label consistently, or the CD decides and records why not.
- **m4. Widowed words in headings and lists.**
  - Headings: p15 "Design and installation of bus waiting / shelters"; p16 "Madinah Chamber of Commerce and / Industry".
  - Lists: p9 "…lift / systems" and «…التكييف / المركزية»; p11 "…hotels and / airports".
  - p10: "high- / standard" is broken at the hyphen.

  Fix: rebalance with set widths or manual breaks.
- **m5. p1 cover alignment.** The logo's right edge (about 94 mm from the left) does not line up with the Arabic title block and green rule (about 104 mm from the left), a 10 mm offset. Fix: align the logo's right edge to the text column, or deliberately centre the logo over the column.
- **m6. p3 fact strip.** The Arabic and English values sit about 1 mm off each other's baseline (2021, 4650245200).
- **m7. p6 overview captions.** Each tile shows two unexplained numbers (for example "09" and "03 / 06"). Fix: label the page reference ("p. 09") or drop one.
- **m8. Partner logos on pp18–19.**
  - Optical imbalance: faint, low-resolution marks next to heavy black ones. Faint: existing-01 award foundation, existing-09 Dar Al Taqwa (7.7 mm tall; "DAR AL TAQWA HOTEL" is illegible), existing-11 Harmony, existing-08 Taibah Cooperative. Heavy: Tiny House, Keeta, HungerStation, The End, Loomi.
  - The vertical hairlines stop short of the top and bottom rules, so the grid looks unfinished.
  - The End file is still cut at its edge.

  Fix: reduce the heavy black marks by about 10–15%, close or deliberately open the grid consistently, and ask the client for official files (especially Dar Al Taqwa, which is also a featured work).
- **m9. Logo misuse inside the client's mockups.** p13 trucks and the p12 box show the blue wordmark on navy, which system.md lists as a "do not" (1.9:1). This comes from the client's images. CD decision: accept as supplied, or recomposite with the reversed wordmark.
- **m10. p15 bus shelter photo has visible litter** (cardboard and rubbish by the wall), in a cleaning company's project photo. CD decision: crop it out (preferred over retouching a works photo) or ask the client for a cleaner shot.
- **m11. Credits detail.**
  - The two toolstop photos (racking aisle on the cover, forklift on p12) share one "Sealey Warehouse" entry; credit each separately as `CREDITS.md` does.
  - "Prophet's Mosque, Medina (DD 01)" is a translated title; the Commons title is "Mezquita del Profeta, Medina, Arabia Saudita, 2025-05-22, DD 01".
  - For BY-SA images, the modified versions carry the same licence; consider saying so.

  This is not legal advice.
- **m12. "under a contract with a single company / في عقد مع شركة واحدة" (p14, point 01)** is tagged [D] (agency draft) in content-outline. It is low-risk but unconfirmed; include it in the client's confirmation questions.
- **m13. Mixed diacritics.** p12 has «تقدّم» with shadda; pp9–10 have «تقدم» without. Pick one.
- **m14. English polish.**
  - p4 mission: "to the latest standards applied in the Kingdom" → "in line with the latest standards in the Kingdom".
  - p5 goal 3: "follow up the company's projects closely" → "monitor the company's projects closely".
  - p15: "which help organise passengers and bus movement, to a high standard of execution" → "Built to a high standard, they help organise passenger flow and bus movement."
  - p14 footer: "WHY OTLOBNY EMAAR · OTLOBNY EMAAR" repeats the name.

**Who fixes the minor issues:** corporate-designer, except m2 and m3 wording and m9, m10, m12 decisions (Creative Director) and m8 official files (client, via the Creative Director).

### Spelling and proofreading

- **English:** I read every line in the PDF text extract. No spelling errors; the phrasing points are in m14.
- **Arabic:** I read every Arabic string from the HTML source and checked the rendered pages. No spelling errors found. The name «اطلبني» never takes a hamza. Arabic commas are used, numerals are Western throughout, and «أجير» is in guillemets.

### The three changes that would most raise the level

1. **Photography.** Replace the European-looking and weak frames with a coherent, Gulf-credible set, stop the repeats (especially p9), and apply one visible grade. Ask the client for real photos of his own sites, staff and fleet; nothing else lifts a profile as much.
2. **Bilingual grid craft.** Lock the Arabic and English list rows to one shared grid on pp7–12, and turn p13 into a purely pictorial fleet page rather than a repeat of p12.
3. **The works section and the closing page.** Rebuild pp15–17 on one strong master with larger images and no dead half-pages (or make it a works spread). Fix the p20 credits contrast and size.

### Not checked

- No native Arabic proofreading. I am not a native reader; one is still required by `arabic-design.md`.
- Guillemet direction: Chromium renders «…» in RTL with the marks pointing inward. My own test page shows this is standard Chromium output with both Tajawal and Noto Sans Arabic. The native proofreader should confirm it is acceptable.
- The PDF was not opened in a second viewer (Acrobat). I rendered it with poppler only.
- The HTML source was not opened from a copied location to test its asset links.
- Licence terms were not checked against the live source pages; I relied on `CREDITS.md` and `README.md`.
- No competitor comparison, because there is no research in `02-research/`.
- The logo lockup proposal (the brief's second deliverable) was not part of this review.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — independent review of company profile v04 (screen PDF, ar-en) before the client sees it
Status: DONE
Files produced: none in the repo. Scratch renders are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/: the check_arabic previews in review_v04/, 150 dpi pages in hi/, plus 300 dpi pages and crops, and the guillemet test files.
Tool operations: `python3 scripts/check_arabic_pdf.py` on the v04 PDF returned PASS (previews in scratchpad/review_v04). pdfinfo, pdffonts, pdfimages -list, pdftotext and pdftoppm at 150 and 300 dpi were run read-only. `node scripts/html2pdf.cjs` rendered a scratch test page (scratchpad/q.html, q2.html) to check how Chromium mirrors guillemets. No Figma or Canva operations.
Decisions needed:
1. C1, Dar Al Taqwa scope: ask the client now (recommended), or remove the scope sentence and chips.
2. m3: label all of the client's AI mockups «صور توضيحية» consistently (recommended).
3. m9: accept the blue-on-navy logo in the client's mockups, or recomposite.
4. m10: crop the litter out of the bus shelter photo (recommended).
5. Ask the client for his own site, staff and fleet photos and for official partner logo files.
Assumptions: Tajawal and IBM Plex Sans are treated as the working typefaces from `04-identity/03-system/system.md`; brand-context section 5 is still blank. Contrast was measured against pixels sampled from the 150 dpi render of the gradient.
Issues / risks: verdict FAIL — 1 critical, 6 major, 14 minor. No native Arabic proofreading and no second-viewer check yet.
Suggested next agent: corporate-designer, to fix C1 (after the CD's ruling), M1, M2, M3, M6 and the minor items, as v05. Art-director first, for M4 and M5 (a second photo sourcing round aimed at Gulf-credible maintenance, landscaping, cleaning and logistics images, and one consistent grade), with this review and `06-profiles/assets/stock/README.md` as input. Then back to quality-reviewer for r2.

