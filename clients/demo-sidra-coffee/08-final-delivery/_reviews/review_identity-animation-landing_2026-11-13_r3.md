> Saved by the Creative Director from the quality-reviewer's handoff. SYSTEM TEST — fictional client.

# Quality review: demo-sidra-coffee, round 3 (2026-11-13)

Scope: the three deliverables that failed round 2. SYSTEM TEST, fictional client.

## Verdicts

| Deliverable | Verdict | Why |
|---|---|---|
| 1. Identity v03 | **PASS WITH MINOR FIXES** | Issue 16 is met as the rule requires: a preliminary check was run and recorded with its limits. N4, N8, N10 and N13 are fixed. Five minor documentation issues remain. |
| 2. Logo animation v01 | **PASS WITH MINOR FIXES** | The art-director approved the concept, storyboard and film, and wrote motion rules. I checked all 90 frames against those rules and found no breach. The poster frame exists. |
| 3. Landing page v02 | **PASS WITH MINOR FIXES** | The sample offer is gone, fonts are local and static, and Ember follows ruling (l). I opened it in Chromium at 1440 and 390 px. Seven minor issues, two of which need a ruling. |
| **Overall** | **PASS WITH MINOR FIXES** | No critical or major issue is open on these three pieces, and none of the ten points fails. |

Standing conditions, reported once and not counted against any verdict:
- **No native Arabic proofread.** This blocks client delivery of every Arabic piece.
- **Nobody has watched the animation played back.** Maker, art-director and both reviewers judged it from frames and numbers only.
- **For a real client the identity is not ready for use.** It still needs a trademark attorney's opinion (a HIGH name risk is on record), the wordmark redraw, and Pantone with calibrated CMYK. All three are logged as required before real use.

## Status of the listed issues

| Issue | Status | Evidence |
|---|---|---|
| r1 16: no conflict check on the mark | **FIXED** (as a preliminary check) | `04-identity/mark-check.md` logs 14 dated searches in Arabic and English, with a "what this is not" section. It states that no register was searched, no linked page was opened, and the bar device is "unknown, not clear". It reports a HIGH risk (the Alshaya "Sidra" dining complex in Riyadh) and marks recall-only items as unverified. `licences.md` v03, `system.md` section 5, guidelines v03 p6 (both languages) and the decision log say the same. I did not re-run the searches. |
| r2 N4: four documents contradicting the log | **FIXED** | `distinctiveness-check_v02.md` replaces the v01 body and addendum. Amendment 02 section 6 closes the pending verdicts. `licences.md` v03 withdraws the three wrong sentences by name. Guidelines p6 carries the agreed verdict line. One leftover: see I1. |
| r2 N8: A4 ladder not recorded (identity part) | **FIXED** | `system.md` section 3.1 and `tokens.json` `font.ladder_a4_document_pt` hold 28/32 pt and 40/46 pt. The profile's 32 px spacing was outside this round. |
| r2 N10: icon v01 beside v02; PNG multiples | **FIXED** | Five icon v01 SVGs are in `02-logo/_archive/` with a reason. I measured all 45 PNG sets: 2x and 4x are exact multiples of 1x, all 135 are RGBA, and none is missing. All 45 PDFs are present; the one I opened has no fonts and no raster. |
| r2 N13: misuse page and test markers | **FIXED** (misuse); markers accepted for the test | Guidelines v03 p3 carries the "Stacked pattern and icon" paragraph in both languages. Footers still read "SYSTEM TEST, FICTIONAL CLIENT" and p6 still lists internal open points; strip these in any client copy. |
| r2 N2: animation without art-director approval; partial bar count | **CLOSED BY RULING** | `art-director-review.md` approves it, and amendment 02 section 1 sets the motion rules. Bars build from frame 4 to 31 (0.13 to 1.03 s), with no two identical frames on a partial count. Ember appears only from frame 35, after seven bars, and only on the fourth. Both pauses show seven bars. The wordmark fades in whole. The film is static from frame 57 to 89, a 1.1 s end hold. |
| r2 N3: empty first frame, not watched, out of scope | **FIXED / CLOSED BY RULING (k)**, except playback | The poster is 1080 × 1080, RGB, with an ICC profile, and matches the last frame within encoder noise. Its file name is accepted in the decision log. Scope is added by ruling (k). Playback is the standing condition above. |
| r2 N1: sample offer (critical) | **FIXED** | No "sample" / «عيّنة» anywhere in the source or rendered text. Every call to action is a wholesale enquiry, per ruling (j). The radio group and phone field are gone. |
| r2 N7: variable font, Ember on two buttons, 100 px display, external fonts | **FIXED / CLOSED BY RULING (l)** | Nine static faces load, and all 13 requests stay inside the page folder. Step figures are Light 300 at normal width. The header button is an Ink outline. There is one Ember button per screenful at 1440 × 900 and 390 × 844 (hero and submit are about 2,400 px apart). The headline is 115 px at 1440. |

## New issues (all minor)

| # | File and location | What is wrong | Rule | Fix required | Agent |
|---|---|---|---|---|---|
| I1 | `01-direction/distinctiveness-check_v02.md` "Limits", last bullet; `creative-direction-amendment-02.md` section 6, last bullet | Both still say the preliminary conflict check (issue 16) is "still open". It has since been run. | `file-management.md`, single source of truth | Add a dated note or new version pointing to `mark-check.md`. | art-director |
| I2 | `03-system/system.md` header, section 3, section 7 points 2 and 3, section 8 | Stale lines under "status after round 3". Header says "not yet approved" while `brand-context.md` says v03 is accepted for the test. Section 7 says bars on Ember "need the art-director's confirmation", though the log accepted it. Section 8 says the per-row wording is outstanding in `brand-context.md`; it is there. | Same | Correct in the next version. | identity-designer |
| I3 | Guidelines v03 PDF p4, Ember bullet; whole document | The guide says Ember appears "once per layout as a field or a headline, plus the lit bar". It omits the web button rule (l) and all motion rules, which now exist only in `system.md` and the tokens. | `branding.md`, decisions recorded; review point 7 | Add one line for each in the next version. | identity-designer |
| I4 | `02-logo/png/`, all 135 files | The PNGs were re-exported at new pixel sizes under the same `v01` / `v02` names, overwriting files the round-2 reviewer saw. | `file-management.md`, versions | Log the overwrite in `02-logo/_archive/README.md`, or bump the PNG version. | identity-designer |
| I5 | `brand-context.md` section 3 (Competitors) and section 5 | Section 3 cites `distinctiveness-check.md`, not `_v02`. The rule "always «سدرة للقهوة» / never 'Sidra' alone" exists only in `licences.md`, `mark-check.md` and `naming.md`, though it is the mitigation for the HIGH name risk. | `file-management.md`, brand-context | Update the reference and record the full-name rule for both languages. | Creative Director |
| A1 | `05-designs/logo-animation/motion-brief.md`, `storyboard.md` | The superseded v01 documents sit beside v02, not in `_archive/`. | Ruling (m); `file-management.md` | Move both with a one-line reason. | Creative Director |
| L1 | `landing-page/index.html`: `<meta name="description">` and hero lead | Both read «سدرة محمصة قهوة مختصة من الرياض…», with «سدرة» alone. This breaks the full-name rule (see I5). | `licences.md` Status; `mark-check.md` section 4 | Change to «سدرة للقهوة محمصة قهوة مختصة…» or «محمصة سدرة للقهوة…». | ui-ux-designer |
| L2 | `index.html` line 10, favicon | The favicon uses barred icon v02, which the ladder allows from 48 px only; at 16 px the bars merge. The maker flagged this as "as instructed". | `system.md` section 5 switch sizes; review point 5 | Use `icon-small-colour` for the favicon; keep v02 for sizes of 48 px and above. | ui-ux-designer |
| L3 | `index.html` section `#how`, both widths | The seven-bar rule sits directly above the three numbered steps, and its lit bar falls over step 2, "we roast it". Nothing is labelled by a bar, so ruling (f) is not broken to the letter, but it reads close to "the lit bar is the roast". The deck fixed the same closeness in round 2. | Ruling (f) | Art-director rules. I recommend moving the rule above the section heading or to the section foot. | art-director, then ui-ux-designer |
| L4 | `index.html`: contact intro, email hint, success panel | «ونردّ عليك على بريدك» and «سنردّ عليك…» promise a reply by email. The brief verifies the email address, not the reply. `ux-brief.md` marks this as an assumption. I rate it minor because it is a service behaviour, not a claimed fact or achievement. | Review point 8; honesty rules | Confirm and log it, or soften to «راسلنا على…». | Creative Director |
| L5 | Hero `h1` at 1440 px, line 2 | The top stroke of the ك in «كل» overhangs the right text edge by about 12 px; the caption and lead align at 1376 px. | `quality-standards.md`, grid | Accept as optical overhang, or pull the headline in. Art-director's call. | ui-ux-designer |
| L6 | Step 2 at 1440 px; email error line at 390 px | Step 2 ends on the short line «لك أنت.». At 390 px the email error line fills the full width edge to edge. | `quality-standards.md`, craft | Rebalance the step text. Let the example address wrap, and test at 360 and 320 px. | ui-ux-designer |
| L7 | `styles.css` lines 2 and 163; `handoff-notes.md` "Tokens" heading | Both still say "tokens.json v02". The values are unchanged in v03. | `file-management.md` | Update the references. | ui-ux-designer |

## Ten-point table

| # | Point | Identity v03 | Animation v01 | Landing page v02 |
|---|---|---|---|---|
| 1 | Creative idea | PASS: seven bars with the fourth lit, across logo, pattern, icon and guide | PASS: seven beats, one lights, then the name | PASS: tagline headline with the stacked pattern |
| 2 | Distinctiveness | PASS on home-page evidence, countersigned by the art-director; HIGH name risk on record | PASS: uses only the identity | PASS: no borrowed layout seen |
| 3 | Colour | PASS: only the five HEX values plus black and white in 45 SVGs | PASS: Paper, Ink and Ember within 2 levels | PASS: only the five colours computed; Ash on Paper only |
| 4 | Typography | PASS: `check_arabic_pdf.py` PASS on guidelines v03, nine static Plex faces, 4,074 Arabic characters, no presentation forms; p3 and p6 viewed, letters connected | PASS: outlined wordmark whole in every frame it appears | PASS: nine faces loaded, no letter-spacing, no text under 15 px |
| 5 | Logo clarity | PASS: ladder defined, exports complete | PASS: clear space 270 px against 146 px required | PASS: header 48/56 px, footer 64 px; minor L2 |
| 6 | Layout | PASS: p3 and p6 viewed | PASS | PASS: no horizontal overflow in default, error or success states; minors L3, L5, L6 |
| 7 | Consistency | PASS: tokens, system and guide agree on values; minors I2, I3 | PASS: film, poster and storyboard agree | PASS |
| 8 | Accuracy | PASS: limits and risks stated; no invented fact | PASS: no claims | PASS: every statement traces to the brief (2023, Riyadh, weekly to order, 250 g and 1 kg, four services, email); minors L1, L4 |
| 9 | Export quality | PASS: A4 screen PDF with fonts embedded; names follow the convention; no print file in scope | PASS: H.264 High, 1080 × 1080, 30 fps, 90 frames, bt709, no audio | PASS: self-contained folder with fonts and OFL texts |
| 10 | Client requirements | PASS: logo AR/EN, colours, fonts, tokens, 2 applications, mini guide | PASS: scope added by ruling (k) | PASS: Arabic RTL HTML prototype |

## Not checked

- **Native Arabic proofread.** I read the landing page copy and guidelines p3 and p6 and found no error. One item for the proofreader: guidelines p6 says «أُجّلت» ("postponed") where the English says "waived".
- **Mark-check searches.** I did not re-run them or open the cited URLs. I judged whether the check was run and honestly recorded, not whether its findings are complete.
- **Animation playback.** I analysed every frame but did not play the film. The v02 candidate in `_archive/` was not reviewed.
- **Guidelines pages 1, 2, 4 and 5.** Read as extracted text only, not viewed as images. The HTML source and a second PDF viewer were not checked.
- **Logo files.** One of 45 PDFs opened. No 16 px or 10 mm re-test; I relied on the maker's bar-count files. Applications v02 were not re-reviewed.
- **Landing page.** Not tested with keyboard or screen reader, on real devices, at tablet widths or below 390 px, or in other browsers. Hover and focus states and the favicon in a real tab were not viewed. Contrast figures were taken from `system.md`, not recomputed.
- **Figma and Canva files.** Not opened.
- **Other deliverables.** Profile, deck and social post were outside this round, so the profile half of N8 and N9, N11, N12 and N14 were not re-checked.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — round 3 re-review of identity v03, logo animation v01 and landing page v02
Status: DONE
Files produced: none in the repo. Temporary previews only, in /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc3/ (subfolders `gl`, `anim`, `lp`, plus `shot.cjs`)
Tool operations: `bash scripts/setup.sh` (12 Arabic font faces). `python3 scripts/check_arabic_pdf.py` on guidelines v03: RESULT PASS; previews of p3 and p6 viewed. `pdfinfo`, `pdffonts`, `pdftotext` on the guidelines; `pdffonts` and `pdfimages` on one logo PDF. Pillow audit of all 135 PNGs and 45 SVGs. `ffprobe` and `ffmpeg` extraction of all 90 frames, per-frame bar and Ember analysis, contact sheet and poster viewed. Playwright Chromium on `index.html` at 1440 × 900 and 390 × 844: fold, full-page, error-state and success-state screenshots, computed-style and network audit. Viewed: desktop full page and fold, mobile full page and fold, mobile error state, desktop success state. No Figma, Canva or export operations. No project file was modified.
Decisions needed: (1) L3, bar row above the three steps: art-director ruling; I recommend moving it. (2) L4, reply-by-email promise: confirm and log, or soften; I recommend confirming, as email is the only channel. (3) I5 / L1: record the full-name rule for Arabic and English in `brand-context.md`; I recommend yes, given the HIGH name risk. (4) I4: accept the in-place PNG re-export with a log line, or require a version bump; I recommend the log line. (5) Whether the three pieces enter `08-final-delivery/` before the proofread and a played viewing; I recommend holding client delivery until both are done.
Assumptions: the Creative Director saves this report as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_identity-animation-landing_2026-11-13_r3.md`. Test rulings by the Creative Director acting as client are treated as valid closures. Issue 16 was judged against "a preliminary check run and honestly recorded", as instructed, not against legal clearance.
Issues / risks: no critical or major issue open on the three pieces; 13 minor issues listed. Native Arabic proofread still blocks all client delivery. The animation has not been watched in motion by anyone. For any real use: HIGH name risk (Alshaya "Sidra", Riyadh) needs a trademark attorney's opinion, the bar device is unchecked, the wordmark must be redrawn, and Pantone with calibrated CMYK is required before print.
Suggested next agent: ui-ux-designer (L1, L2, L5, L6, L7, and L3 after the ruling; needs the full-name rule and `icon-small` SVG); identity-designer (I2, I3, I4; needs amendment 02 and this report); art-director (I1 and the L3 ruling); Creative Director (I5, A1, L4, then packaging into `08-final-delivery/` and the delivery checklist once the proofread and a played viewing are done).
