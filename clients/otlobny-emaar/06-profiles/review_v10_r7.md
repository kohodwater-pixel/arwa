## Quality review: otlobny-emaar company profile v10 (screen, ar-en), r7, 2026-11-14 — final gate before the client

**Verdict: PASS WITH MINOR FIXES. No critical or major issues; none of the ten points fails.**

**v10 may be presented to the client tomorrow as a reviewed draft.** It is not final. Four things are still needed before final:
- the client confirms the name strings against his CR certificate (still an agency decision pending his confirmation);
- a native Arabic speaker proofreads it;
- a second viewer checks it;
- the 08 delivery package gets its own review.

None of the minor issues below needs to be fixed before tomorrow.

### What I checked

All files are under `/home/user/arwa/clients/otlobny-emaar/06-profiles/`.

- **Arabic check:** I ran `check_arabic_pdf.py` on `otlobny-emaar_company-profile_screen_ar-en_v10.pdf` myself. Result: PASS. 20 pages. Tajawal and IBM Plex Sans, all weights embedded, no fallback. 4,695 Arabic characters, no presentation forms.
- **Pages:** all 20 rendered at 150 dpi and viewed. pp1, 2, 12, 13, 14, 16 and 20 at full size; the rest on contact sheets. p12 also at 300 dpi.
- **Contrast:** measured from pixels on p13, the works panels (pp14–16) and p20.
- **Clear space:** measured from pixels on p1.
- **Copy:** I diffed the v09 and v10 HTML text and compared each changed string with `review_v09_panel_content.md`.
- **Bookmarks:** read with pypdf.
- **Images:** checked the build log for repeated images.

### Content must-fixes, string by string

Every one matches the content review exactly.

| Item | Page | Result |
|---|---|---|
| M1 | p13 #01 | Arabic «… والخدمات اللوجستية، تقدمها شركة واحدة.» and English "… manpower supply and logistics, all from one company." Exact. The old "single contract" wording appears 0 times in the PDF and HTML. |
| M2 | p20 | The Arabic rights note matches the specified string exactly, including «وأزيلت منها علامات تجارية صغيرة لأطراف أخرى حيث وجدت». |
| M3 | p11 | «تكون العقود شهرية أو سنوية على نظام «أجير».» Exact. «تبرم العقود» appears 0 times. |
| M4 | p6 | «التشجير وتنسيق الحدائق وصيانة المنتزهات وأجهزة الري.» Exact. «وأنظمة الري» appears 0 times. |
| M5 | p14 | «صممت «اطلبني إعمار» محطات انتظار الحافلات وركبتها بجودة عالية واحترافية في التنفيذ، وهي محطات تسهم في تنظيم حركة الركاب وسير الحافلات.» Exact. |
| N14 | p13 | #03 is now «عقد مستمر مع الغرفة التجارية والصناعية في المدينة المنورة» / «نقدم للغرفة خدمات التشغيل والصيانة والنظافة من عام 2023 حتى الآن.», with English "An ongoing Madinah Chamber contract" / "Operation, maintenance and cleaning for the Madinah Chamber of Commerce and Industry, from 2023 to the present." #02 now reads «نوفر كوادر نظامية مؤهلة، بعقود شهرية أو سنوية على نظام «أجير».» / "Qualified, legally compliant staff, on monthly or annual contracts through the Ajeer system." All as specified. The English description starts with a capital, which is correct after the title. |

The nice-to-haves that were applied (N1–N7, N9–N13, N15) match the review's wording. I checked each one in the diff:
- sector order on p10;
- comma before «وتخدم» and «بموجب» on p3;
- «تتولى … لجميع» on p7;
- the p6 card 01 text in both languages;
- «من عام 2023» on p15;
- «وفي غيرها من المجالات» on p5;
- «ثلاثة قطاعات نخدمها»;
- "innovate", "to a high standard … valued clients'";
- the "labelled … visuals created from" wording on p20;
- «صفحة 07» etc. on p6.

N8 was declined, correctly, because it is client wording. No new facts were introduced. I found no spelling or grammar errors in the changed text in either language.

### Forbidden strings, contents, bookmarks, repeats

- **Forbidden strings:** none found in the PDF text: Emaar, Shahd/«شهد», «أطلبني», «اطليني», CONSANY, ISUZU, DZIRE, Suzuki, "single company", WE DO THE BEST, «تبرم العقود», WhatsApp, lorem, TBC.
- **Metadata Title:** "OTLOBNY Emar … (draft v10)".
- **Contents:** 03, 04, 06, 13, 14, 17 and 19 match the real footer folios.
- **Bookmarks:** Contents 2, About 3, Vision 4, Services 6, Why 13, Work 14, Partners 17, Contact 19, Photo credits 20. All correct.
- **Repeated images:** the build log reports "sources on more than one page: none". Visually, no image repeats either; the p3 and p6 Madinah images are two different source photographs.

### Contrast (measured from pixels)

| Page | Ground | Text | Ratio | Result |
|---|---|---|---|---|
| p13 | flat navy #1F3162 | white | 12.55 | pass |
| p13 | flat navy | periwinkle secondary text | 5.50 | pass |
| p13 | flat navy | green numerals | 5.83 | pass |
| pp14–16 | navy panels | captions in white at 82% | 8.98 | pass |
| p20 top | gradient, samples from 11.25 down to 6.81 | white text and descriptor | at least 6.81 | pass |
| p20 top | gradient behind the wordmark | green reversed wordmark | 3.9–4.7 | above the 3:1 needed for non-text graphics; see m1 |
| p20 bottom | white | credits #525456 | 7.61 | pass (as before) |
| p20 bottom | white | bold navy | 12.55 | pass |

### Lockup clear space and sizes (system.md §1a: minimum 45 mm; X = 6.9% of the width)

| Page | Version | Width | Clear space |
|---|---|---|---|
| p1 | colour | measured 79.8 mm | Nearest collage edge measured at 11.9 mm, against X ≈ 5.5 mm. **r6 m1 fixed.** |
| p2 | reversed | 58 mm | A solid navy zone around the lockup clears the lattice, so nothing crosses it. |
| p19 | reversed | 64 mm | Clear. |
| p20 | reversed | 90 mm | Clear. |

### p12 cab door at 300 dpi

Fixed:
- the mirror bracket is intact;
- the paint-out patch stays inside the door panel;
- the speck below the handle is gone;
- the wordmark is correct and slightly in perspective.

All other vehicle surfaces are unchanged from v09 and stay correct. The fleet image now sits clear of the trim, and its floor fades out softly.

### Ten-point table

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | The diamond lattice is now stronger: duotone tiles on the cover and dark beats on pp5, 13, 14–16, 19 and 20. |
| 2 | Distinctiveness | N/A | `02-research/` is empty; competitors are out of scope. |
| 3 | Colour and contrast | PASS | All text pairs pass AA (table above). Green is now an accent only on pp8, 10 and 11. |
| 4 | Arabic and English typography | PASS | check_arabic PASS. The new Arabic text on p13, p6 and p20 is connected and reads right to left. No tracking on Arabic. |
| 5 | Logo clarity | PASS | Correct versions, sizes ≥ 58 mm, and clear space respected on all four pages. Vehicle logos are correct. |
| 6 | Layout | PASS | The works master is consistent across pp14–16 (same photo top line, title size and number). The p3 and p6 re-crops work. No overflow; p20 credits end at about 186 mm. |
| 7 | Consistency across pages | PASS | One running name, one kicker and footer system, one works master. |
| 8 | Accuracy | PASS | M1 removes the unsupported claim. The new #03 restates a client-confirmed fact. No invented content. No spelling errors. |
| 9 | Export quality | PASS | Screen PDF, sRGB, fonts embedded. File name follows `file-delivery.md`. 9 bookmarks. |
| 10 | Matches client requirements | PASS | Lockup with descriptor throughout, his fleet image, the Chamber contract period, the Dar Al Taqwa page with its confirmed scope, 32 partners, 20 pages. |

### Issues (all minor; none blocks tomorrow's presentation)

- **m1. p20, lockup on the gradient.**
  - The green reversed wordmark sits at the middle of the navy→royal gradient. Its right half is on the lighter end, at 3.9:1.
  - That is above the 3:1 needed for graphics. But system.md assigns the reversed version to "navy, dark half of the gradient" and the white version to royal blue and gradients.
  - Fix (one of):
    - use `lockup-white`;
    - or shift the gradient so it is darkest behind the lockup.
  - Who: corporate-designer.
- **m2. p2, the clear zone shows as a visible rectangle.**
  - The lattice stops abruptly along a straight-edged box around the lockup.
  - Fix (optional):
    - end the lattice on whole diamond cells;
    - or fade it out near the lockup.
- **m3. pp14–16, duplicated work number.**
  - The large "01 / 02 / 03" and the small English kicker "01 / 03" say the same thing.
  - Fix (optional): drop the small fraction, or change it to the section label.
- **m4. Still open:**
  - name strings to be confirmed against the client's CR;
  - native Arabic proofread;
  - second-viewer check;
  - accessibility tagging;
  - official partner logo files (faint logos; The End is still cut);
  - the original bus-shelter photo;
  - the client's own photographs;
  - rights to the fleet mockup and the room photo, which rest with the client.

### Overall view against the client's bar

v10 is the best version to date. It has:
- a confident cover, with one colour hero and a quiet duotone set of tiles;
- a clear structure, with dark, rhythmic pages for "why us" and the works section;
- a factual, stronger "why" page built on the Chamber contract;
- correct use of the identity everywhere, including on his fleet.

From a quality and technical standpoint it is ready for the client's review. The remaining gap to truly world-class is still the client's own photography.

### Not checked

- No native Arabic proofreading.
- No second-viewer check; I rendered the PDF with poppler only.
- The HTML source was not opened from a copied location.
- The maker's `_work/v10/check300_cab-door.png` was not opened; I made my own 300 dpi crop from the PDF.
- Licence terms were not checked against the live source pages.

## HANDOFF
Agent: quality-reviewer
Client / task: otlobny-emaar — review round 7, final gate for company profile v10 (screen PDF, ar-en) before the client presentation
Status: DONE
Files produced: none in the repo. Scratch files are under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/:
- check_arabic previews in review_v10/
- 150 dpi pages and the 300 dpi p12 render in v10/
- v10_door.png (cab door crop) and v10p12_small.png
- contact sheets s10a.png and s10b.png
Tool operations: `check_arabic_pdf.py` on v10 returned PASS. Also run, read-only: pdftotext, pdfinfo, pypdf bookmarks, pdftoppm at 150 and 300 dpi, pixel contrast and clear-space measurements with Pillow and numpy, and an HTML text diff v09 → v10. No Figma or Canva operations.
Decisions needed:
1. Present v10 to the client as a reviewed draft (recommended: yes), and ask him in the same message to confirm the name strings against his CR.
2. m1: switch to the white lockup on p20, or darken the gradient behind it. This can wait for the next round.
Assumptions:
- The p15 contract period and the Dar Al Taqwa scope are taken as client-confirmed, per brand-context.md.
- The descriptor strings and "Emar" are taken as the agency decision pending the client.
Issues / risks: verdict PASS WITH MINOR FIXES — 0 critical, 0 major, 3 minor plus open items. Not a final approval.
Suggested next agent: Creative Director, to present v10 to the client. Corporate-designer afterwards, for m1–m3 and the client's feedback. Quality-reviewer before any final version and for the 08-final-delivery package review.

