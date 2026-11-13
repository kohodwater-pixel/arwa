> Saved by the Creative Director from the quality-reviewer's handoff. SYSTEM TEST — fictional client.

# Review round 5: demo-sidra-coffee delivery package (2026-11-13)

Scope: `/home/user/arwa/clients/demo-sidra-coffee/08-final-delivery/` as an internal HELD package, plus the first review of the strategy deliverable. SYSTEM TEST, fictional client. I modified nothing in the repo; `git status` was clean after the run. Previews are in `/tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc5/`.

## Verdicts

**Strategy document (`00-brand-strategy/…_brand-strategy_summary_en_v02.pdf` and `.md`): FAIL.** The content is sound: no invented fact, and it follows the decision log. It fails on three major issues: a corrupted duplicate title on page 1 (S1), broken Arabic direction and punctuation in mixed lines (S2), and a value proposition that makes the claim the document itself says must never be implied (S3).

**Package as an internal held package: FAIL (narrow).** P2 and P3 are fixed and everything else holds up. It fails because one packaged deliverable (the strategy) has open major issues, and the README states that every piece passed review "rounds 1 to 5" before round 5 existed (R1). Once S1–S3 are fixed and re-reviewed, and R1 and C1 are corrected or ruled, the package is PASS WITH MINOR FIXES as a held package.

**Standing conditions (reported once):** no native Arabic proofread, the animation has not been watched played back, and there is no client approval. These keep the package HELD and are disclosed in the README.

## Ten-point table: strategy document

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | "The weekly roast" is one clear idea, tied to the one verified differentiating fact. |
| 2 | Distinctiveness | PASS, limits stated | The competitor test and its "honest limit" are written out; the HIGH name risk is in section 11. |
| 3 | Colour | PASS | Only Ink, Ember, Paper and white are used. |
| 4 | Typography | **FAIL** | `check_arabic_pdf.py` PASS (6 pages, six Plex faces, 931 Arabic characters, 0 presentation forms) and letters are connected. But direction and punctuation are wrong in mixed lines (S2), and Arabic is not scaled up against the Latin (S6). |
| 5 | Logo clarity | N/A | No logo is used; acceptable for a text document. |
| 6 | Layout | **FAIL** | p1 carries two titles, the first with three replacement characters (S1). The header fields run together, and the Values table splits across p3 and p4. |
| 7 | Consistency | **FAIL** | The value proposition and mission extend roast-to-order to home brewers, against section 6 of the same document and ruling (u) (S3). |
| 8 | Accuracy | PASS with minors | Every factual statement traces to the brief, `competitor-audit_v02.md`, `mark-check.md`, `naming.md` or `distinctiveness-check_v02.md`. Two wordings are slightly stronger than their source (S5). |
| 9 | Export quality | **FAIL** | The PDF Title metadata and the HTML `<title>` contain U+FFFD (S1). Fonts are embedded, A4. |
| 10 | Client requirements | PASS | "Brand Strategy (short)": 6 pages, in English with Arabic for name, tagline, values and voice. |

**Decision-log compliance of the strategy:**
- Arabic-first is not claimed as a differentiator (section 3, labelled [D]).
- The no-cafés clause is not claimed: the "Reading limits" note is explicit and the "we do not compete" line is held.
- Tagline scope is stated correctly for the tagline itself, but see S3.
- The name rule matches `brand-context.md` section 5. The four standalone «سدرة» in the text are mentions inside the rule, not uses.

**Fact cross-check, all confirmed:**
- Brief: founded 2023, Riyadh, weekly roast to order, the four products, both audiences, the 20-account goal, Western numerals, the constraints and the must-not-invent list.
- Competitor audit: Camel Step since 2013; Elixir Bunn's disputed 2014/2018 date, with no year stated; Brew92 founded 2016 with its four cities; all three run cafés and sell wholesale.
- Mark check: Alshaya "Sidra" (Riyadh, announced 2018; Kuwait); the variety risk; classes 30, 43 and 35; "not a legal clearance".

## Issues

| # | Severity | Location | What is wrong | Rule | Fix | Agent |
|---|---|---|---|---|---|---|
| S1 | Major | Strategy PDF p1, first line; PDF Title metadata; `08-source-files/brand-strategy/…v02.html` `<title>` and `<h1 class="title">` | A pandoc title block prints "Sidra Coffee ��� Brand strategy summary" (three U+FFFD where an em dash was) above the real H1. The page has two titles, one corrupted. The `.md` is clean. | `quality-standards.md`, accuracy and "opens cleanly" | Rebuild without the title block or with a correctly encoded title; re-export as v03. | brand-strategist |
| S2 | Major | Strategy PDF: p1 tagline line; p3 "Promise"; p4 "Tagline (confirmed)", "Value proposition" and "Held until confirmed"; p5 Arabic do/don't table | (a) Arabic quoted inside English lines has no direction isolation, so the full stop sits at the start of the Arabic sentence (right end, beside the first word) and the guillemets are split from the sentence. (b) The value proposition runs Arabic and English in one paragraph; the Arabic wraps over two lines in an LTR paragraph and the English follows on the same line. (c) The Arabic table «اكتب هكذا / لا تكتب هكذا / السبب» has its row-label column on the left and reads left to right. The standalone Arabic blockquote on p2 and the key-messages table are correct. | `arabic-design.md`: direction and layout, "do not interleave", "tables read from the right-hand column" | Wrap each Arabic quotation in `<bdi dir="rtl">` or put it on its own RTL line; give the value proposition separate Arabic and English blocks; set `dir="rtl"` on the Arabic table. | brand-strategist |
| S3 | Major | Strategy section 8 "Value proposition" (AR and EN), section 7 Mission, section 4 Arabic positioning | "…roasts your order in the weekly roast, for independent cafés and for people who brew at home" asserts roast-to-order for home orders. Section 6 lists that as "not confirmed and never implied", and ruling (u) limits the tagline for the same reason. The value proposition carries no hold or scope label, so a writer will lift it as-is. The same sentence is in the profile mission (p2), which is wholesale material. | Decision log ruling (u); `brand-context.md` section 3 TBC list | Scope the value proposition to wholesale, reword it so the home clause does not depend on "your order", or mark it held pending question 3. Record a ruling on the mission wording. | brand-strategist; Creative Director |
| S4 | Minor | Strategy p1 header | "Status: … Awaiting quality review" and "Replaces… `brand-strategy.md` and `messaging.md`" are internal and name files not in the package. Version, Date, Prepared by, Language, Status and Replaces run together as one paragraph. | Accuracy; craft | Update the status and put each field on its own line. | brand-strategist |
| S5 | Minor | Strategy section 3 bullet 4; section 11 table | "Has no awards or certifications to publish [V]": the brief says "not available", not "none exist". "With a Starbucks among its tenants": `mark-check.md` 1.1 says "probably the same complex. Not confirmed". | Accuracy | Soften both wordings. | brand-strategist |
| S6 | Minor | Strategy PDF throughout; p1 H1 | Arabic is set at the same size as the Latin, not 15–20% larger as the brand's own rule requires. The H1 breaks the name as "(سدرة / للقهوة)" across two lines. The Values table splits two rows on p3 and two on p4. | `arabic-design.md`, optical size; craft | Scale the Arabic up, keep the name unbroken and keep the table together. | brand-strategist |
| S7 | Minor | Strategy section 10, rule 4 | The «سدرة المنتهى» rule is labelled [D] with the others, but it comes from `naming.md` and is not in the decision log or `brand-context.md` section 5. | `branding.md`, decisions recorded | Add it to `brand-context.md` or relabel it. | Creative Director |
| R1 | Major | `README.md` lines 7 and 20 | "Every piece here passed… no critical or major issue open (reports in `_reviews/`, rounds 1 to 5)". `_reviews/` holds r1–r4 only. The strategy had never been reviewed when this was written, and it now fails. The Arabic status line makes the same claim. | Honesty rules; delivery checklist | Rewrite after the strategy is re-reviewed; cite only rounds that exist. | Creative Director |
| C1 | Major unless ruled | Profile v03 p2, Values line (AR and EN), against `brand-context.md` section 4 | `brand-context.md` says "On schedule / على الموعد" "is not used in public copy until roast and delivery days can be published". The profile prints it as a value. The strategy section 7 states a softer rule ("must not be worded as a delivery promise"). The three sources disagree, and ruling (i) says no piece may imply delivery timing. This predates v03. | `brand-context.md` section 4; ruling (i) | Rule which wording governs, then align `brand-context.md`, the strategy and the profile. I recommend keeping the value in the strategy only and dropping it from the profile until days are published. | Creative Director, then corporate-designer |
| R2 | Minor | `README.md` | The Arabic section covers only the status and the eight holds. The "known small points" paragraph, folder guide, logo guide and name rule are English only for an Arabic-primary client. Hold 8 names only the guidelines, but SYSTEM TEST markers are also in the strategy PDF, `FONTS.md`, HTML titles and `tokens.json`. | Checklist, README for a non-designer | Add the missing Arabic sections and widen hold 8. | Creative Director |
| K1 | Minor | `08-source-files/instagram-post/assets/` | Eight font files are never loaded by the page. Six are instances cut from the variable font (v3.201, one named `LightCondensed` with internal name "IBM Plex Sans Regular"), which `licences.md` describes as work files not referenced by deliverables. Redistributing modified instances under the reserved name "Plex" is a licence question. One file has a hashed name, `IBMPlexSans-Regular-f0cfd6.ttf`. | `file-delivery.md`, no working files; `branding.md`, rights | Keep only the four files the post loads (Arabic Regular, Medium and Bold; static Latin Regular) and confirm the render is still pixel-identical. | graphic-designer |
| K2 | Minor | `08-source-files/logo-animation/assets/`; `company-profile/…v03.html` line 3 | The animation's `assets/` folder is empty. The profile source comment says "licence texts beside them", but no OFL text is in its `assets/`. | Accuracy; organisation | Remove the empty folder; add the OFL texts or correct the comment. | Creative Director |
| K3 | Minor | `02-brand-guidelines/mark-check.md` lines 55 and 145, `licences.md`, `tokens.json`; CSS and HTML comments in sources | `mark-check.md` gives the full name as "Sidra Coffee Roastery", against the name rule "Sidra Coffee". These files cite `assets/fonts/…`, `04-identity/…`, `naming.md`, `_archive/` and `scripts/html2pdf.cjs`, none of which is in the package. This is the remaining part of r4 P5. | Accuracy; name rule | Issue package versions, or add the point to the README's small-points list. | identity-designer |
| K4 | Minor | Deck slide 5 against slides 2–4 | The seven-bar band sits about 3% of slide height lower on the closing slide than on slides 2–4, where it is identical. | Craft, consistency | Align it, or confirm the closing layout is intentionally different. | presentation-designer |
| K5 | Minor | `brand-context.md` sections 7 and 3 | Section 7 still reads "assembled after review round 3"; the package was rebuilt after round 4. Section 3 does not name the strategy summary v02 file. | `file-management.md` | Update. | Creative Director |

## Checks 2 to 6

**Sources (P2): FIXED.** I copied the package to the scratchpad and opened all five sources and the landing page in Chromium.

| Source | Requests | Outside folder | Failed | Match with deliverable |
|---|---|---|---|---|
| brand-strategy | 8 | 0 | 0 | Re-exported PDF text identical, 6 pages (it reproduces S1) |
| brand-guidelines | 24 | 0 | 0 | Re-exported PDF text identical, 6 pages; 21 images, none broken |
| company-profile | 12 | 0 | 0 | Re-exported PDF text identical, 4 pages |
| instagram-post | 7 | 0 | 0 | Screenshot at 1080 × 1350 is pixel-identical to the PNG |
| logo-animation | 1 | 0 | 0 | Plays and loops; self-contained; not compared frame by frame with the MP4 |
| landing-page | 13 | 0 | 0 | Nine faces loaded, 2 images, RTL |

There were no console errors and no broken images. Fonts are not all loaded: the guidelines leave one declared face unloaded and the Instagram post leaves eight (K1), because nothing on the page uses them.

**Profile v03 and deck v03 (P3): FIXED, nothing broken.**
- `check_arabic_pdf.py` is PASS on both (profile: 4 pages, 8 faces; deck: 5 pages, with the known Type 3 note). I viewed all 4 pages and all 5 slides; letters are connected and RTL.
- Profile p2 now reads «سدرة للقهوة محمصة قهوة مختصة من الرياض…» and "Sidra Coffee roastery…". The only other text change from v02 is the Values line losing its trailing dot; it now wraps cleanly in two balanced English lines.
- Deck slide 2's left card label is «ما تفعله سدرة للقهوة»; the two cards are equal and the band matches slides 3 and 4.
- No standalone «سدرة» remains in the profile, deck, post or landing page text.
- All deck paragraphs carry `rtl="1"`.
- `FONTS.md` now points to `07-fonts-and-licences/` and has no repo path.

**Hashes and contents.**
- The package has 335 files, and 321 are byte-identical to a current stage or `assets/fonts/` file.
- The 14 without a twin are expected: three READMEs, four review reports, and seven source HTML and CSS files rewritten for relative paths, whose output I verified above.
- Nine source assets match only files under `_work/`. Three preview PNGs are legitimately used by the guidelines; the six cut font instances are K1.
- There are no superseded versions, drafts, `_work`, `_archive`, `.gitkeep`, `.DS_Store` or handoff notes in the package. Profile and deck v02 are in the stage `_archive/` folders.

**README.**
- These claims check out: page and slide counts, 1080 × 1350, 3.0 s H.264 MP4, 45 SVG / 45 PDF / 135 PNG, every logo name pattern, HEX and RGB values, fonts, the name rule and the `v01`–`v04` explanation.
- The Arabic and English hold lists agree: eight each, with the same content.
- It is understandable by a non-designer; "lockup", "tokens" and "master artwork" are now explained.
- The faults are R1 and R2.

**`brand-context.md`.** The header, the "eight conditions" count, rulings (r)–(u), the colours, the fonts and the name rule are consistent with the package. The faults are K5 and the wording conflict in C1.

## Status of round 4 issues

| # | Status | Note |
|---|---|---|
| P1 | STILL OPEN | The strategy is now in the package, mentioned in the README and reviewed, but it fails (S1–S3). |
| P2 | FIXED | Sources are self-contained, with zero outside or failed requests. |
| P3 | FIXED | Full name in the profile and the deck, both languages. |
| P4 | PARTLY FIXED | Version names explained, Arabic status added, terms explained, RGB added. Still open: R1 and R2. |
| P5 | FIXED for `FONTS.md`; STILL OPEN for `licences.md` | See K3. |
| P6 | DISCLOSED AS HOLD | README "known small points". |
| P7 | FIXED and DISCLOSED AS HOLD | `.gitkeep` and the handoff notes are gone; `_reviews/` is covered by hold 8. |
| P8 | CLOSED BY RULING (s) | Also disclosed in the README and in `03-stationery-print/README.md`. |
| P9 | FIXED, one line left | See K5. |
| P10 | DISCLOSED AS HOLD | README "known small points". |

## Delivery checklist

| Item | Result | Evidence |
|---|---|---|
| Every file has passed quality review | **FAIL** | The strategy fails its first review; everything else has passed. |
| Client approved final versions | FAIL, by design | Disclosed as hold 7. |
| Every deliverable in the brief present | PASS | A to F are present; B's two applications are previews by ruling (s). |
| Every language version present | PASS | As briefed. |
| Every required format present | PASS | PDF, PPTX, SVG, PNG and HTML, plus MP4. |
| Folder structure | PASS | `00` to `08`, `README.md` and `_reviews/`; `00-brand-strategy/` is a sensible addition. |
| Naming convention | PASS | All deliverables follow the pattern; none is `final`, by ruling (r). One hashed font file name (K1). |
| No drafts, duplicates or system files | PASS with minor | K1 and K2. |
| Logo set | PASS | Unchanged from r4 and hash-identical. |
| RGB and CMYK separated | N/A, disclosed | Hold 5. |
| Sources included, assets collected | PASS | Verified in a fresh copy. |
| Fonts and licences | PASS with minor | K1 and K3. |
| README in plain language | **FAIL** | R1 (untrue review claim); R2. |
| Opens from a fresh copy | PASS | Six HTML files, three PDFs and the PPTX text were all read from the copy. |
| `brand-context.md` updated | PASS with minor | K5 and C1. |

## Before a real client receives it

1. Fix S1, S2 and S3 in a strategy v03, then re-review it.
2. Correct the README (R1, R2) and rule on C1.
3. A native reader proofreads all Arabic, including the strategy.
4. A person watches the animation played back.
5. A trademark attorney advises on the name and the bar device.
6. The wordmark is redrawn.
7. Pantone and calibrated CMYK are set, and print files made if print is wanted.
8. A real email and phone number are supplied.
9. The client answers the four questions in strategy section 11.
10. The two applications are produced as reviewed files (ruling s).
11. SYSTEM TEST markers and internal notes are stripped everywhere, `_reviews/` is removed, and K1–K3 are cleaned up.
12. The deck is opened in PowerPoint.
13. The client approves; only then are files re-exported as `final` and logged.

## Not checked

- Native Arabic proofread. I read all the Arabic in the strategy, profile and deck and found no spelling error.
- Animation playback, and a frame-by-frame comparison of the animation source against the MP4.
- Guidelines v04 pages as images this round; I checked text identity with its source only. I noted one tracked Latin caption on the clear-space tile that contains a single Arabic letter د.
- The deck in PowerPoint or Keynote.
- The landing page at 390 and 320 px this round (1440 only), and with keyboard or screen reader.
- Logo files visually; I relied on hash identity with the set reviewed in r4.
- Whether competitor facts are still true on the live sites; I checked the strategy against the audit, not against the web.
- Figma and Canva files, which are not part of the package.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — review round 5: first review of the strategy summary v02 and re-review of the rebuilt held delivery package `08-final-delivery/`
Status: DONE
Files produced: none in the repo. Temporary previews only, in /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc5/ (`pdf/`, `fresh/pkg/`, `src/`, `audit.cjs`, `strat_1.png` to `strat_3.png`, `prof_1.png`, `prof_2.png`, `deck_1.png` to `deck_3.png`, `anim.png`)
Tool operations: `bash scripts/setup.sh` (12 Arabic font faces). `python3 scripts/check_arabic_pdf.py` on the strategy v02, profile v03 and deck v03 PDFs: all RESULT PASS; all 15 pages and slides viewed as images. SHA-256 comparison of all 335 package files against the stage folders and `assets/fonts/`. Playwright Chromium on a scratchpad copy of the package: five sources and the landing page opened with a request, font and image audit; three sources re-exported to PDF and text-diffed against the deliverables (0 differing lines each); the Instagram source screenshot compared with the PNG (0 differing pixels). python-pptx read of deck v03 and diff against v02. Text diff of profile v02 against v03. fontTools name check of the Instagram source fonts. `ffprobe` on the MP4. No Figma, Canva or export operations. No project file was modified.
Decisions needed: (1) C1: is "On schedule / على الموعد" allowed as a printed value in public pieces? I recommend removing it from the profile until days are published and aligning the wording in `brand-context.md` and the strategy. (2) S3: scope of the value proposition and mission towards home brewers; I recommend a wholesale-scoped value proposition and a recorded ruling on the mission. (3) S7: add the «سدرة المنتهى» rule to `brand-context.md` section 5; I recommend yes. (4) K4: is the lower band on the closing slide intentional? I recommend aligning it.
Assumptions: the Creative Director saves this report as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_delivery-package_2026-11-13_r5.md`. Test rulings by the Creative Director acting as client are treated as valid closures. S1 and S2 are rated major, not critical, because the letters are shaped and connected and no fact is wrong; a stricter reading of "broken Arabic" would make S2 critical.
Issues / risks: the strategy document FAILS with three major issues (S1, S2, S3). The package FAILS narrowly because of that, the untrue README review claim (R1) and the open conflict C1. P2 and P3 are fixed with nothing broken. All eight README holds remain open.
Suggested next agent: brand-strategist (strategy v03 fixing S1–S6; input: this report, `arabic-design.md`, decision log ruling (u)); Creative Director (rulings C1, S3, S7; README R1, R2; `brand-context.md` K5; K2); graphic-designer (K1); identity-designer (K3); presentation-designer (K4); corporate-designer if C1 removes the value from the profile. Then quality-reviewer for a short round 6 on strategy v03, the README and any changed files.
