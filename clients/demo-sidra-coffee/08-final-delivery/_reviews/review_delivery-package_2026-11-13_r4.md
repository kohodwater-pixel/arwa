> Saved by the Creative Director from the quality-reviewer's handoff. SYSTEM TEST — fictional client.

# Final gate review: demo-sidra-coffee delivery package, round 4 (2026-11-13)

Scope: `/home/user/arwa/clients/demo-sidra-coffee/08-final-delivery/` as an internal, HELD package. SYSTEM TEST, fictional client. I modified nothing; `git status` was clean after the run.

## Verdict: FAIL (narrow)

Everything in the package is sound, but the package is not complete against the brief and its README does not say so.

- **What holds up:** all 268 deliverable and support files are byte-identical to the latest version in the stage folders, every file opens cleanly from the package alone, and both late fix passes (landing page v03, guidelines v04) are confirmed fixed with nothing broken.
- **Why it fails:**
  - **P1 (critical):** deliverable A of the brief, Brand Strategy, is not in the package, is not mentioned in the README, and has never been through quality review.
  - **P2 (major):** editable sources for four pieces are outside the package.
- **Path to pass:** P1 and P2 can each be closed by adding the files or by a recorded ruling plus a README hold line. After that the package is PASS WITH MINOR FIXES as a held package.

**Version numbers instead of `final`:** this is the honest choice and I endorse it. `file-delivery.md` reserves `final` for "the approved file", and no client has approved anything. Renaming would assert an approval that did not happen. The checklist item "marked `final`" is therefore correctly unmet. Two gaps: the README does not explain why names carry `v01`–`v04`, and the decision is not in the `brand-context.md` decision log.

## Ten-point table (package level)

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Seven bars with the fourth lit is consistent across logo, guidelines, post, deck, landing page and film. |
| 2 | Distinctiveness | PASS, risk on record | HIGH name risk stated in the README (hold 3), `mark-check.md` and guidelines p6. |
| 3 | Colour | PASS | 45 SVGs use only the five HEX values plus black and white; landing page computed colours are the five only. |
| 4 | Typography | PASS | `check_arabic_pdf.py` PASS on all three PDFs with 0 presentation forms and Plex faces only; previews viewed, letters connected; no letter-spacing on the landing page. |
| 5 | Logo clarity | PASS | Favicon is now `icon-small`, legible at 16 px; lockups I rendered are complete and unclipped. |
| 6 | Layout | PASS | Landing page has no horizontal overflow at 1440, 390 or 320 px, including the error state. |
| 7 | Consistency | PASS with minors | The full-name rule in the README and guidelines v04 is broken in the profile and the deck (P3). |
| 8 | Accuracy | PASS with minors | No invented fact found; README and `brand-context.md` have small inaccuracies (P4, P9). |
| 9 | Export quality | PASS | MP4 is H.264 High, 1080 × 1080, 30 fps, 90 frames, 3.0 s; PNGs are at exact sizes; PDFs have fonts embedded. |
| 10 | Client requirements | **FAIL** | Brief deliverable A is absent (P1); sources are not collected (P2). |

## Delivery checklist

| Item | Result | Evidence |
|---|---|---|
| Every file has passed quality review | PARTIAL | Six deliverables passed r1–r3; landing v03 and guidelines v04 are confirmed in this round. The strategy was never reviewed. |
| Client approved final versions | FAIL, by design | Disclosed as HELD; only test approvals exist. |
| Every deliverable in the brief present | **FAIL** | A (strategy) is absent. B's "2 applications" exist only as thumbnails on guidelines p6. C, D, E and F are present. The logo animation is extra, added by ruling (k). |
| Every language version present | PASS | Logo AR, EN and bilingual; guidelines and profile AR-EN; post, deck and landing page AR, as briefed. |
| Every required format present | PASS | PDF, PPTX, SVG, PNG and HTML, plus MP4. |
| Folder structure | PASS | `01-logo` to `08-source-files` plus `README.md`. Extras are `_reviews/` and two `.gitkeep` files. |
| Naming convention, marked `final` | PARTIAL | All 262 deliverable files match `<client>_<deliverable>_<variant>_<lang>_vNN`. None is `final`, which is correct (see above). |
| No drafts, rejected options, duplicates, system files | PASS with minor | No `_work`, `_archive`, v01 leftovers, `.DS_Store` or `Thumbs.db`. Two 0-byte `.gitkeep` files (root and `_reviews/`). No archive-only file was packaged. |
| Logo: SVG, PDF, PNG 1x/2x/4x per lockup | PASS | 45 SVG, 45 PDF, 135 PNG; the set equals `04-identity/02-logo/` exactly. |
| Logo: colour, black, white | PASS | Colour, colour-reversed, colour-on-ember, black and white. |
| Logo: RGB and CMYK separated | N/A, disclosed | RGB only; README hold 5 says nothing is print-ready. |
| Sources included, assets collected | **FAIL** | `08-source-files/README.md` only points to stage folders outside the package (P2). |
| Fonts included | PASS | Ten static TTFs and two OFL texts, hash-identical to `assets/fonts/`. |
| Licences documented | PASS with minor | `licences.md` and the OFL texts are present; `licences.md` and `FONTS.md` cite repo paths (P5). |
| README in plain language | PASS with minors | See P4. |
| Guidelines PDF included | PASS | v04, 6 pages, A4. |
| Opens from a fresh copy | PASS | See the technical results below. |
| `brand-context.md` updated | PARTIAL | Section 7 has the HELD entry; header and details are stale (P9). |

## Technical results

- **Hashes:** 274 files in the package. The 6 without a stage twin are the three READMEs and three review reports, as expected. Everything else matches its source.
- **PDFs** (`check_arabic_pdf.py`, all PASS):
  - Guidelines v04: 6 pages, 9 static Plex faces, 4,489 Arabic characters.
  - Profile v02: 4 pages, 8 faces.
  - Deck v02: 5 pages, with a Type 3 note on bold Latin; fine for screen and already known.
- **Landing page:** copied alone to the scratchpad and opened in Chromium at 1440, 390 and 320 px. Nine faces loaded; 13 requests, 0 outside the folder, 0 failed. `dir="rtl" lang="ar"`; no text under 15 px. There are two Ember buttons, about 2,400 px apart.
- **PPTX:** python-pptx reads 5 slides at 16:9. LibreOffice converts it with IBM Plex Sans Arabic and IBM Plex Sans.
- **Logos:** 3 PDFs (vector, 0 fonts, 0 rasters), 2 SVGs rendered, 5 PNGs (RGBA, exact 1x/2x/4x multiples). All 45 SVGs parse, with no `<text>` and no external references.

## Late fix passes

**Landing page v03**

| Issue | Status | Evidence |
|---|---|---|
| L1 full name | FIXED | Meta description and hero lead read «سدرة للقهوة محمصة…»; no standalone «سدرة» remains in the page text. |
| L2 favicon | FIXED | Points to `icon-small-colour_v01.svg`; a 16 px render shows a solid rule with the centre lit. Not seen in a real browser tab. |
| L3 bar row | FIXED per ruling (o) | The row is the last element of `#how` at all three widths. At 1440 the lit bar still falls in the centre column, 64 px below step 2; nothing sits over a step. |
| L5 overhang | FIXED | The ك of «كل» now ends on the text edge. Trade-off: line 1 «تُحمَّص» sits about 13 px inside the edge shared by the caption and lead. No art-director acceptance is recorded. |
| L6 line breaks | FIXED | Step 2 breaks 4 + 4 words; the email error wraps to two lines at 390 and 320 px without overflow. |
| L7 token refs | FIXED | `styles.css` lines 2 and 164 and `handoff-notes.md` say v03. |

Broken by the pass: nothing. One new nit at 320 px: the hero caption breaks as «… · تأسّست / عام 2023».

**Guidelines v04**

| Issue | Status | Evidence |
|---|---|---|
| I3 web Ember rule | FIXED | p4, both languages. |
| I3 motion block | FIXED | p2 "Logo in motion / الشعار في الحركة", both languages; it fits above the footer. |
| Name rule | FIXED | p3 "Also" list in both languages; p6 Arabic voice line. |
| Arabic "waived" | FIXED | p6 now reads «أُعفي هذا الاختبار من مراجع بانتون…». |
| I2 `system.md` stale lines | Appears FIXED | Header and section 13 say corrected; I did not read the whole file. It was edited in place with no version change. |

Broken by the pass: nothing on p2, p3, p4 or p6, which I viewed. Pages 1 and 5 were read as text only.

Other r3 items: I4 is fixed (log line in `02-logo/_archive/README.md`), I5 is fixed, A1 is fixed (v01 brief and storyboard are in `_archive/`). I1 was not verified.

## Issues

| # | Severity | Location | What is wrong | Rule | Fix | Agent |
|---|---|---|---|---|---|---|
| P1 | Critical | Package root; `README.md` | Brief section 10 item A, Brand Strategy, is not in the package and not mentioned. `03-strategy/brand-strategy.md` exists but was never quality-reviewed. | Delivery checklist, completeness; CLAUDE.md responsibility 7 | Review the strategy, export it and add it; or rule that it is handed over separately and say so in the README. | Creative Director, then brand-strategist and quality-reviewer |
| P2 | Major | `08-source-files/README.md` | Sources for the guidelines, profile, social post and animation are HTML files in stage folders a client would not receive. The top README does not list this as a hold. | `file-delivery.md`, "ships with an editable source… linked assets collected" | Collect self-contained sources, as the landing page already is; or add it as a README hold condition. | Creative Director, with the makers |
| P3 | Minor | Profile PDF p2, Arabic "About us" line 1; deck slide 2, right-hand card label | «سدرة محمصة قهوة مختصة من الرياض…» and «ما تفعله سدرة» use «سدرة» alone. This breaks the name rule the README and guidelines v04 now state, and README hold 7 does not list it. | `brand-context.md` section 5, name rule | Change to «سدرة للقهوة» in new versions; until then add to hold 7. | corporate-designer, presentation-designer |
| P4 | Minor | `README.md` | See the README findings below. | Checklist, handover; honesty rules | Correct in a new README version. | Creative Director |
| P5 | Minor | `06-presentations/FONTS.md` | It points to `assets/fonts/…`, `bash scripts/setup.sh` and `04-identity/licences.md`, none of which are in the package. "Known limits" says the fonts are "not done here; this is a working folder" and that the static files are unverified, which `licences.md` has since partly answered. | `file-delivery.md`, README for a non-designer | Issue a package version pointing to `07-fonts-and-licences/`. | presentation-designer |
| P6 | Minor | Guidelines v04 p6, "Files in 04-identity" table | It lists stage folders (`02-logo`, `03-system`, `brand-v02.css`, `04-applications`) that do not exist in the package. | Accuracy | Describe the package folders in the next version. | identity-designer |
| P7 | Minor | Package root and `_reviews/` | Two `.gitkeep` files; `_reviews/` and `landing-page/handoff-notes.md` are internal working records. | Checklist, organisation | Exclude them from any client copy. | Creative Director |
| P8 | Minor | Brief item B; `03-stationery-print/README.md` | The two applications appear only as small previews on guidelines p6; v02 was never fully reviewed. | Completeness | Decide whether the previews satisfy "2 applications" or add reviewed screen PDFs. | Creative Director, identity-designer |
| P9 | Minor | `brand-context.md` | See the `brand-context.md` findings below. | `file-management.md` | Update. | Creative Director |
| P10 | Minor | Landing page hero caption at 320 px | The line breaks leaving «عام 2023» alone. | `quality-standards.md`, craft | Balance or shorten the caption. | ui-ux-designer |

**README findings (P4).** Every factual claim I checked is true: page and slide counts, pixel sizes, lockup and colour names, HEX values, fonts, the logo size ladder and the name rule. The holds are honest. The gaps:
- "Passed… rounds 1 to 3" was written before landing v03 and guidelines v04 were reviewed; it should cite this round.
- Hold 7 omits P3, and omits that the guidelines footers and p6 still carry "SYSTEM TEST" markers and internal open points (r2 N13).
- There is no word on the missing strategy or the uncollected sources.
- It does not explain why file names carry version numbers.
- The body is English only for an Arabic-primary client.
- "master", "lockup" and "tokens" are unexplained for a non-designer.
- Colours are given as HEX only; RGB and approximate CMYK are in the guidelines.

**`brand-context.md` findings (P9).** The colours, fonts, name rule, guidelines v04 reference and HELD entry are consistent with the package. The gaps:
- The header still says "Current stage: quality review round 3".
- Section 7 says "six conditions"; the README lists seven.
- The decision log has no entry for landing v03, guidelines v04, the package assembly or the decision to keep version numbers.
- Section 2 "Timeline" and "Mandatory elements" are blank, though the brief gives constraints (no people, avoid green and white).

## Before a real client could receive it

1. A native reader proofreads all Arabic.
2. A person watches the animation played back.
3. A trademark attorney advises on the name and the bar device.
4. The wordmark is redrawn.
5. Pantone and calibrated CMYK are set, and print-ready files made if print is wanted.
6. A real email and phone number are supplied.
7. The strategy deliverable is added and reviewed (P1).
8. Sources are collected into the package (P2).
9. The name rule is fixed in the profile and the deck (P3), and N8, N9 and N11 are closed.
10. "SYSTEM TEST" markers and internal open points are stripped from client copies; `_reviews/`, `.gitkeep` and the handoff notes are removed.
11. `FONTS.md`, guidelines p6 and the README are corrected, with an Arabic README.
12. The client approves; only then are files re-exported as `final` and the date logged in `brand-context.md`.

## Not checked

- Native Arabic proofread; I read the texts and found no error beyond P3.
- Animation playback; I viewed five frames and the ffprobe data only.
- Guidelines p1 and p5, profile p1, p3 and p4, and deck slides 1, 4 and 5 as images.
- PPTX paragraph RTL flags, the raster-logo part of N11 and the 32 px spacing part of N8.
- 40 of 45 logo PDFs, and most SVGs and PNGs visually.
- The landing page with keyboard or screen reader, in other browsers, at tablet widths, or its favicon in a real tab.
- I1 (stale "still open" lines in the direction documents) and the full text of `system.md`.
- Figma and Canva files, which are not part of the package.
- The content of `03-strategy/` — not reviewed, and that gap is P1.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — final gate review of the held delivery package `08-final-delivery/` (round 4), including the unreviewed landing page v03 and guidelines v04
Status: DONE
Files produced: none in the repo. Temporary previews only, in /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc4/ (subfolders `pdf`, `lp`, `logo`, `fresh`, `pptx_conv`, plus `shot.cjs`, `sheet.png`, `anim.png`, `bil.png`, `g3.txt`, `g4.txt`)
Tool operations: `bash scripts/setup.sh` (12 Arabic font faces). SHA-256 comparison of all 274 package files against the stage folders and `assets/fonts/`. `python3 scripts/check_arabic_pdf.py` on guidelines v04, profile v02 and deck v02 PDFs: all RESULT PASS; guidelines p2, p3, p4, p6, profile p2 and deck p2, p3 viewed. Playwright Chromium on a standalone copy of `landing-page/` at 1440, 390 and 320 px: screenshots, computed-style and network audit, error state; hero, "how it works", 390 error state and 320 fold viewed. `diff` of landing v02 against v03 and of guidelines v03 against v04 text. `ffprobe` and a five-frame strip of the MP4. python-pptx read and LibreOffice conversion of the PPTX. Pillow, CairoSVG and `pdftoppm` checks on logo files. No Figma, Canva or export operations. No project file was modified.
Decisions needed: (1) P1: add a reviewed strategy document to the package, or rule that it is handed over separately and say so in the README; I recommend adding it as a PDF after review. (2) P2: collect sources into `08-source-files/`, or list it as a hold; I recommend the hold line now and collection before release. (3) P8: whether the guidelines previews satisfy "2 applications"; I recommend recording that they do for the test and requiring reviewed files for a real client. (4) L5: art-director acceptance of the 13 px inset on headline line 1; I recommend accepting. (5) Record the keep-version-numbers decision in the decision log; I recommend yes.
Assumptions: the Creative Director saves this report as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_delivery-package_2026-11-13_r4.md`. Test rulings by the Creative Director acting as client are treated as valid closures. "Latest reviewed version" was judged against the stage folders' current non-archived files.
Issues / risks: one critical (P1) and one major (P2) at package level; eight minor. Landing page v03 and guidelines v04 are confirmed fixed with nothing broken. All seven README holds remain open. `system.md` was corrected in place without a version change.
Suggested next agent: Creative Director (P1 and P2 rulings, README and `brand-context.md` corrections P4, P7, P9); brand-strategist then quality-reviewer if the strategy is to be packaged (input: `03-strategy/brand-strategy.md`); corporate-designer and presentation-designer (P3, P5, plus N9 and N11; input: name rule in `brand-context.md` section 5); identity-designer (P6); ui-ux-designer (P10). Then a short re-review of the package.
