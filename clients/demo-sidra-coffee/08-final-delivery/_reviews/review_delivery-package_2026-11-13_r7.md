> Saved by the Creative Director from the quality-reviewer's handoff. SYSTEM TEST — fictional client.

# Review round 7: demo-sidra-coffee held delivery package (2026-11-13)

## Verdicts

| Item | Verdict |
|---|---|
| Guidelines v05 (`02-brand-guidelines/…_mini_ar-en_v05.pdf` and source) | **PASS WITH MINOR FIXES** (G1 and G2 closed; one cosmetic line break, one wording consistency point) |
| Strategy summary v04 (`00-brand-strategy/…_v04.pdf` and `.md`) | **PASS WITH MINOR FIXES** (N1, N2, N4 closed; the new status line is itself inaccurate) |
| Package as an internal HELD package | **PASS WITH MINOR FIXES**. No critical or major issue open. It stays HELD. |

Standing conditions, reported once: no native Arabic proofread; the animation has not been watched played back; no client approval. These and the other README holds keep the package HELD.

The cross-document sweep found no conflict with the decision log in any text-bearing deliverable.

## Ten-point table (guidelines v05 / strategy v04)

| # | Point | Guidelines v05 | Strategy v04 |
|---|---|---|---|
| 1 | Creative idea | PASS: p1 "Weekly Beat", the idea sentence stands under ruling (al) | PASS: Direction A, section 1 |
| 2 | Distinctiveness | PASS: unchanged since r3/r6; p6 states the comparison and its limits | N/A |
| 3 | Colour | PASS: p4 values match `brand-context.md` section 5 exactly | PASS: Paper, Ink, Ember, Crema only |
| 4 | Typography | PASS: `check_arabic_pdf.py` PASS, 9 IBM Plex faces, 0 presentation forms; all six pages viewed, letters connected, RTL correct | PASS: script PASS, 7 IBM Plex faces; p1, 3, 4, 6 viewed |
| 5 | Logo | PASS: p2 lockups, clear space and the د caption render correctly | PASS: bilingual logo on p1 |
| 6 | Layout | PASS: one stranded «و» on p5 (minor R7-5) | PASS: blank last page accepted by ruling (ak) |
| 7 | Consistency | PASS: footers all read v05; personality Arabic differs from the strategy (minor R7-4) | PASS |
| 8 | Accuracy | PASS: no fact outside the brief; Say lists clean | PASS, with minor R7-1 (status line) |
| 9 | Export | PASS: A4, 6 pages, fonts embedded by name, naming correct | PASS: A4, 8 pages, naming correct |
| 10 | Brief | PASS: mini guidelines with two applications as previews (ruling s) | PASS: short strategy, section 10 A |

## Check 1: guidelines v05

- **G1 closed.** The p6 Say lists read "roastery, roasted to order, every week, fresh" / «محمصة، يُحمَّص لطلبك، كل أسبوع، طازجة». The p1 value reads "On schedule (an internal commitment: not used in public copy until roast and delivery days can be published)", with the Arabic equivalent.
- **G2 closed.** p1 reads "Promise, wholesale material only." / «الوعد، لمواد الجملة فقط». The p6 tagline is scoped the same way.
- **p5 body sample** is rescoped to cafés in both languages ("roasts each café's order in that week's roast").
- **p6 files table** names real package folders (`01-logo/svg`, `png`, `pdf`, `02-brand-guidelines`, `07-fonts-and-licences`), and all exist.
- **p2 د caption** renders correctly in both languages.
- **Sweep against the decision log:** no delivery-day, roast-date or home roast-to-order wording. The name rule on p3 and p6 matches `brand-context.md` section 5. The bag label preview carries no roast date and uses the tagline on a wholesale bag only.
- **Source and PDF agree.** The packaged source differs from the stage HTML only in asset paths.

## Check 2: strategy v04

- **N1 closed.** Section 4 (p3) ends "a supplier that roasts each café's order in that week's roast", identical to `brand-context.md` section 3.
- **N2 closed.** Section 6 (p4) reads "Promise [D] (wholesale-facing material only)"; `brand-context.md` matches.
- **N4 closed.** Section 9 (p6) reads "V60 stays in Latin script; espresso is written إسبريسو in Arabic text", matching `brand-context.md` section 4.
- **N6 partly closed.** The stale "for quality review" wording is gone and the blank p8 is accepted by ruling (ak), but the new status line is inaccurate (R7-1).
- **`.md`, source HTML and PDF carry the same text.** Arabic word sets are identical between `.md` and HTML; the English differences are table-header capitalisation only.

## Check 3: cross-document sweep

Swept: strategy `.md`, PDF text and source HTML; guidelines PDF text and source; profile PDF text and source; deck PPTX text and PDF text; landing page `index.html` and `styles.css`; social post and animation source HTML; the three READMEs; `FONTS.md`; `licences.md`; `mark-check.md`; `tokens.json`.

| Search | Result |
|---|---|
| «على الموعد» / "on schedule" | Only in the strategy (section 7, labelled internal) and guidelines p1 (labelled internal). None in the profile, deck, landing page, post, README or tokens. **No conflict.** |
| Home orders roasted to order | None. Every roast-to-order line is addressed to cafés. Home lines are subscription or product only, which the brief verifies. **No conflict.** |
| Delivery-day or roast-date promise | None. No weekday, hour count or roast date anywhere. "Monthly delivery to homes" is the brief's subscription fact. |
| Standalone «سدرة» / "Sidra" in running text | None in visible copy. Hits are quoted forbidden forms, the third-party Alshaya complex and variety name, and logo alt text (minor R7-3). |
| Phone numbers | None. Only statements that there is none. |
| "sample" / «عيّنة», placeholder, lorem | None. The landing page's call to action is a wholesale enquiry (ruling j). |
| Facts not in the brief | None. 2023, Riyadh, 250 g / 1 kg, weekly roast-to-order wholesale, monthly subscription, barista courses and the email all trace to the brief. No clients, counts, awards or certifications. |

## Check 4: package integrity

- **Hashes:** 312 package files are byte-identical to a current, non-archived stage file. None matches an archived file only.
- **Collected sources:** the five source HTMLs and two CSS files differ from stage by path rewriting, plus two unused `@font-face` lines dropped by the collector. Neither affected face is used in the PDFs.
- **Not in the stage folders:** the OFL texts, the hashed post font and `IBMPlexSansArabic-Light.ttf`, which is identical to the repo's `assets/fonts` copy.
- **Superseded versions:** none. No guidelines v04, strategy v03, `_work`, `_archive` or stray files in the package.
- **Playwright:** all six HTML files opened from a scratchpad copy with 0 failed requests, 0 requests outside their own folder, 0 console errors and every font face loaded.
- **Versions present:** strategy v04, guidelines v05, profile v04, presentation v03, post v02, landing v03 (per the decision log; the folder carries no version label), animation v01.

## Check 5: README and brand-context.md

- **N3 closed.** Hold 3 reads "was announced for Riyadh in 2018 (it is not known whether it still trades under that name)" in both languages and in the `brand-context.md` log row.
- **N5 closed.** The small points now mention the comments and the hashed font name.
- **N7 closed.** The Arabic README uses «الملف التعريفي»; the logo line uses `<lockup>` and defines it.
- The eight holds are accurate, and "v01 to v05" is correct.
- `brand-context.md` sections 3, 4 and 5 and the last two log rows agree with the package. One stale row in section 7 (R7-2).

## Check 6: status of round 6 issues

| r6 issue | Status |
|---|---|
| G1 (major) | **Closed** |
| G2 | **Closed** |
| N1 | **Closed** (ruling ah applied in the strategy and `brand-context.md`) |
| N2 | **Closed** |
| N3 | **Closed** |
| N4 | **Closed** (ruling aj) |
| N5 | **Closed** by README disclosure; the comments and hashed file name remain for client clean-up (hold 8) |
| N6 | **Partly closed**: blank page accepted (ak); status line replaced but inaccurate (R7-1) |
| N7 | **Closed** |

## New issues (all minor; none blocks the internal held package)

| ID | Severity | Location | What | Rule | Fix | Agent |
|---|---|---|---|---|---|---|
| R7-1 | Minor | Strategy v04 p1 header; `.md` line 11; source HTML | Status reads "v04; passed internal quality review (rounds 5 and 6)". Round 5 failed strategy v02, round 6 passed v03 with minor fixes, and v04 had not been reviewed when this was written. | Accuracy; honesty rules | At the next version write "v04; reviewed in round 7 (pass with minor fixes); test approvals only, no client approval", or drop the review claim and point to `_reviews/`. | brand-strategist (text), corporate-designer (export) |
| R7-2 | Minor | `brand-context.md` section 7, deliveries row | "rebuilt after rounds 4 and 5" is stale; the package was rebuilt again after round 6. | `file-management.md`, brand-context kept current | Update the row to include round 6 and this review. | Creative Director |
| R7-3 | Minor | `08-source-files/instagram-post/…_v02.html` line 41 (`alt="سدرة"`); the same label in the animation source HTML | Logo alternative text gives the name alone. The profile source uses «شعار سدرة للقهوة». Source only; the PNG and MP4 are unaffected. | Name rule, `brand-context.md` section 5; consistency | Use «شعار سدرة للقهوة» at the next version of each source. | graphic-designer |
| R7-4 | Minor | Guidelines v05 p1 «الشخصية» against strategy v04 section 5 | The Arabic for "Rooted" is «أصيلة وعربية أولًا» in the guidelines and «بنت الرياض» in the strategy. The two reference documents use different Arabic for the same approved trait. | Brand consistency | Choose one rendering, preferably at the native proofread, and align both at their next versions. | brand-strategist decides; identity-designer applies |
| R7-5 | Minor | Guidelines v05 p5, Arabic font paragraph, line 2 | The line ends on a stranded «و», with "Helvetica Neue" starting the next line. | `quality-standards.md`, awkward line breaks | Bind «و» to the following word with a no-break space at the next version. | identity-designer |

## Not checked

- Strategy pages 2, 5, 7 and 8 were not viewed as images; their text was read and matched to the `.md`.
- Profile v04, presentation v03, landing page v03, post v02 and animation v01 were not re-rendered or re-viewed visually. They are byte-identical to the stage files; this round only swept their text. Whether they changed since round 6 was not verified against r6 hashes.
- The 225 logo files were hash-compared only.
- `tokens.json` values were not re-verified beyond a text search.
- No second PDF viewer, no PowerPoint, no MP4 playback.
- Contrast ratios and print minimum sizes were not re-measured.
- URLs in `mark-check.md` were not opened.
- Arabic was read by me, not by a native proofreader.
- The Figma and Canva files are out of scope and were not opened.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — review round 7 (final gate) of guidelines v05, strategy summary v04 and the rebuilt held delivery package
Status: DONE
Files produced: none in the repo. Previews and a scratch copy only, under /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc7/
Tool operations: `bash scripts/setup.sh` succeeded (12 Arabic font faces). `check_arabic_pdf.py` on guidelines v05: PASS, previews viewed for all six pages. `check_arabic_pdf.py` on strategy v04: PASS, pages 1, 3, 4 and 6 viewed. Text extracted with pdftotext and python-pptx. Hash comparison by Python: 312 identical. Playwright opened six HTML files from a scratchpad copy: 0 failed, 0 outside requests. No Figma or Canva operation. One Bash command included a stray `cp` into a non-existent `node_modules` path; it failed, nothing was written, and `git status` is clean.
Decisions needed: (1) Accept R7-1 to R7-5 as known minor points for the held package, or issue strategy v05 and guidelines v06. I recommend accepting them, fixing R7-2 now and batching the rest with the native proofread. (2) Which Arabic rendering of "Rooted" is canonical (R7-4). I recommend leaving this to the native proofreader.
Assumptions: the Creative Director saves this report as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_delivery-package_2026-11-13_r7.md`. Test rulings (ag) to (al) are treated as valid closures. The landing page is taken as v03 on the decision log's word.
Issues / risks: no critical or major issue open. The package stays HELD on the README's eight conditions. The strategy status line overstates its review history (R7-1). Five deliverables were text-swept only this round, not re-viewed visually.
Suggested next agent: Creative Director (save this report; update `brand-context.md` section 7 for R7-2; record the ruling on R7-1, R7-3, R7-4 and R7-5). No further review round is needed unless a new version is issued. If one is: brand-strategist with corporate-designer for R7-1, identity-designer for R7-4 and R7-5, graphic-designer for R7-3, then quality-reviewer on the changed files only.
