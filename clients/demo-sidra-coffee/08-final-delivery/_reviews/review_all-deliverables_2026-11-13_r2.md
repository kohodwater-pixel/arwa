> Saved by the Creative Director from the quality-reviewer's handoff. SYSTEM TEST — fictional client.

# Quality review: demo-sidra-coffee, round 2 (2026-11-13)

## Verdicts

Standing condition, reported once: no native Arabic proofread has been done, and none can be done inside this system. It blocks client delivery of every Arabic piece. The verdicts below say what each piece gets apart from that condition.

| Deliverable | Verdict | Why |
|---|---|---|
| 1. Company profile v02 | **PASS WITH MINOR FIXES** (subject to the proofread) | Every r1 critical and major issue is fixed or closed by ruling. No invented fact, no placeholder, no draft marker. Three minor items remain. |
| 2. Identity v02 | **FAIL** (one major still open) | r1 issue 16, the preliminary conflict check on the mark, was not run and no ruling waived it. Everything else is fixed or closed by ruling; several documents are now out of date. |
| 3. Presentation v02 | **PASS WITH MINOR FIXES** (subject to the proofread) | All r1 majors are fixed. The PPTX re-rendered by me matches the supplied PDF on all five slides. Logos are still raster. |
| 4. Social post v02 | **PASS WITH MINOR FIXES** (subject to the proofread) | The invented direct-message channel is gone and the verified email is used; sRGB is embedded. One size deviation has no ruling. |
| 5. Logo animation v01 (new) | **FAIL** (one major, process and brand rule) | The file is technically clean, but the art-director never approved a concept or storyboard, and the build-up shows fewer than seven bars with no ruling on that. |
| 6. Landing page v01 (new) | **FAIL** (one critical) | The whole page is built on "request a sample", an offer that is not in the brief, `brand-context.md` or the strategy. |
| **Overall** | **FAIL** | Three of six pieces carry an open critical or major issue. Nothing enters `08-final-delivery/` yet. |

What held up in every piece I viewed:
- **PDF checks:** `check_arabic_pdf.py` reports PASS on all three v02 PDFs, with IBM Plex Sans Arabic and IBM Plex Sans only and no fallback.
- **Arabic shaping:** letters are connected and right to left throughout; no tracking on Arabic.
- **Colour:** only the five approved HEX values appear in the SVGs, PPTX, CSS and the social PNG.
- **Contact details:** no phone number, social handle or direct-message channel anywhere; the email is the only channel.
- **Timing:** no delivery-day or roast-date promise in any piece.

## r1 issue status

| # | r1 issue | Status | Evidence |
|---|---|---|---|
| 1 | Distinctiveness never checked (critical) | FIXED, within home-page evidence | I viewed `captures-r3/camelstep.png`, `elixirbunn.png` and `captures/brew92.png`: a teal line-drawn camel symbol, a black calligraphic and serif wordmark with green imagery, and a thin blue Latin wordmark. None resembles the bars, Ember or the heavy wordmark. Only home pages were checked. See N4 and N5. |
| 2 | Social post invented a direct-message channel (critical) | FIXED | v02 reads «لطلبات المقاهي بالجملة:» with `hello@sidra-coffee.example`. |
| 3 | Profile placeholder and draft markers | FIXED | No phone row and no "DRAFT" in the footers or PDF title. |
| 4 | Profile p2 Arabic "online" attached to brewing | FIXED | «ونبيعها للمقاهي، وعبر الإنترنت لمن يحضّر قهوته في بيته». |
| 5 | No native Arabic proofread | STILL OPEN | Standing condition. |
| 6 | Tagline unconfirmed | CLOSED BY RULING (a) | `brand-context.md` section 3 is updated; the profile counts as wholesale material. |
| 7 | "Sidra" alone in English | FIXED | "Sidra Coffee roastery is based in Riyadh…". |
| 8 | Deck slide 2 implied a timing promise | FIXED | The two questions and the answering line are gone. |
| 9 | Deck slide 3 steps tied to bars | FIXED, with ruling (f) | Three equal columns; the band sits apart at the foot of the slide. |
| 10 | PPTX fonts, master, Latin runs | FIXED | `FONTS.md` added; one master with four named "Sidra" layouts; Latin runs are set in IBM Plex Sans. Fonts are listed, not embedded, which the rule allows. |
| 11 | Profile widows | FIXED | The three widows are gone. One trailing "·" remains (N9). |
| 12 | Profile p3 Arabic item numbers low | FIXED | Numbers sit on the heading line on both sides. |
| 13 | Profile sizes and paddings off scale | PARTLY FIXED | The A4 ladder is defined in amendment-01 section 9, but not copied into `system.md` or `tokens.json` as that amendment instructs. 32 px is still used three times and is not a spacing step (N8). |
| 14 | Profile HTML fonts from `_work/fonts/` | FIXED | Now `assets/fonts/ibmplexsans-static/`. |
| 15 | Wordmark is typed Plex Bold | CLOSED BY RULING (d) | Redraw is required before real use, and is now a distinctiveness requirement because Camel Step sets its site in the same typeface. |
| 16 | No conflict check on the mark | **STILL OPEN (major)** | `licences.md` states that no search of any kind was run for the mark. The competitor comparison covers three home pages only. The record is honest, but the check was not done and no ruling waives it. |
| 17 | Pantone and calibrated CMYK | CLOSED BY RULING (e) | `tokens.json`, `system.md` and guidelines p4 say "waived for system test; required before print". |
| 18 | Logo PNG and PDF missing | FIXED | 135 transparent RGBA PNGs at 1x/2x/4x and 45 vector PDFs, one set for each of the 45 current lockups. Sample PDF has no fonts and no raster. See N10. |
| 19 | Fallback ladder and icon | CLOSED BY RULING (g); icon FIXED | Icon v02 is three stacked rows; its test file counts seven bars from 41 px, and the switch size is 48 px. |
| 20 | `brand-context.md` section 5 empty | FIXED, but now stale | The section is filled; several lines no longer match later rulings (N6). |
| 21 | Ink on Ember given as 3.9:1 | FIXED | Corrected to 3.19:1 in amendment-01 section 1; the approved file was rightly left untouched. |
| 22 | Guidelines cover pattern in wide bars | FIXED | The cover is now three band rows, taller than wide. |
| 23 | Variable font in guidelines; dummy number on card | FIXED | Guidelines v02 embeds static faces only; card v02 has no phone number. |
| 24 | Deck `sldSz`, raster logos, counter, caption | PARTLY FIXED | `sldSz` is untyped, the counter is 18 pt and the caption is rewritten. The three logos are still PNG (N11). |
| 25 | Social sRGB and three deviations | FIXED / CLOSED BY RULING (h) | "sRGB built-in" profile embedded; full-width headline and bottom bleed are approved. Headline size is not ruled (N12). |
| 26 | Canva link listed without warning | FIXED | Annotated "OFF-BRAND, not for use". |

## New issues

| # | Severity | File and location | What is wrong | Rule | Fix required | Agent |
|---|---|---|---|---|---|---|
| N1 | **Critical** | `05-designs/landing-page/index.html`: header button, hero button, contact heading «اطلب عيّنة، أو اسألنا.», radio option «عيّنة من القهوة» | The page offers café owners a coffee sample. No sample offer exists in the brief, `brand-context.md` or the strategy. `ux-brief.md` line 49 lists it as an assumption to confirm, yet it is the primary call to action. | Review point 8; honesty rules. | Get the sample offer confirmed and logged, or rebuild the call to action around the verified facts (ask about wholesale supply by email or form). | ui-ux-designer (Creative Director gets the confirmation) |
| N2 | Major | `05-designs/logo-animation/…_v01.mp4`; `notes.md` items 6 and 8 | The art-director never reviewed the concept, and the storyboard was not approved before animating. At 0.5 s the frame shows four and a half bars, against the do-not "change the count", with no ruling for motion. | CLAUDE.md routing G (art-director concept, then production); `brand-context.md` section 5 do-nots. | Art-director reviews the storyboard and the fade, and rules whether a partial bar count is allowed during a build. Re-export only if the ruling requires it. | art-director, then graphic-designer |
| N3 | Minor | Logo animation, `notes.md` items 5 and 7; `01-brief/brief.md` section 10 | The first frame is empty Paper, so it cannot serve as a thumbnail. The maker never watched it in motion. A logo animation is not among the brief's deliverables. | Motion skill checks; review point 10. | Supply a poster frame or state the cover frame; watch it played; record the scope addition in the decision log. | graphic-designer, Creative Director |
| N4 | Minor | `04-identity/01-direction/distinctiveness-check.md`; `creative-direction-amendment-01.md` "Still open"; `licences.md` "not checked" list; guidelines v02 p6 "Still open", first bullet | The main body still says Camel Step and Elixir Bunn are "NOT YET VERIFIED", while the addendum and decision log say all three are distinct. The amendment still lists the verdicts as pending. `licences.md` says both "no look at the real identities" and "compared". The guidelines say the mark "has not been compared with other marks". | `file-management.md` single source of truth; `branding.md` decisions recorded. | Bring the four documents into line with the decision-log row as new versions. | art-director, identity-designer |
| N5 | Minor | `distinctiveness-check.md` addendum | The final verdicts were written by the Creative Director, not by the art-director who owns the check. | CLAUDE.md "you do not do a specialist's job". | Art-director confirms or countersigns the addendum. | art-director |
| N6 | Minor | `brand-context.md` header, section 3 and section 5 | Stale: "Last updated 2026-11-12, current stage 04-identity". Section 3 still says competitor details are "unverified" and the positioning still claims "an Arabic-first supplier", which the last ruling withdrew. Section 5 says "v01 accepted", "icon = seven bars in a square" and Pantone "to be matched by printer". | `file-management.md` brand-context. | Update from `system.md` section 8 and the last two log rows. | Creative Director |
| N7 | Minor | `05-designs/landing-page/styles.css` lines 11 and 153; `handoff-notes.md` deviations 1 to 3 | Step numbers use the variable font at 85% width, Light, which tokens v02 dropped. Ember is used on two buttons against "once per layout". Display is 100 px. The fonts load from `../../../../assets/fonts/`, so the page will not open correctly once moved out of the repo. | `system.md` section 3; `file-delivery.md` sources. | Rebuild on tokens v02 and static fonts; Creative Director or art-director rules on Ember for buttons; collect the fonts with the page at packaging. | ui-ux-designer, art-director |
| N8 | Minor | `04-identity/03-system/system.md`, `tokens.json`; profile v02 HTML | The A4 ladder (28/32 pt and 40/46 pt) is not recorded in the system or tokens. The profile uses 32 px three times, off the spacing steps. | Amendment-01 section 9; `system.md` section 4. | Record the ladder; move 32 px to 24 or 40. | identity-designer, corporate-designer |
| N9 | Minor | Profile PDF p2, Values, English line 1 | The line ends on a dangling "·" ("On schedule · Plain facts ·"). | `quality-standards.md` craft. | Break before the separator or set one value per line. | corporate-designer |
| N10 | Minor | `04-identity/02-logo/` and `02-logo/png/` | The five superseded icon v01 SVGs sit beside v02 instead of in `_archive/`. Lockup PNGs are 204, 407 and 814 px wide, so 2x is not exactly double 1x. | `file-management.md` versions. | Archive icon v01 with a one-line reason; export 1x at a whole-pixel size. | identity-designer |
| N11 | Minor | Deck v02: `.pptx` media; slides 2 and 4; `FONTS.md` "Known limits" | Logos are still three PNG rasters. Slides 2 and 4 have no bar band and slide 2 leaves the lower third empty, while 1, 3 and 5 carry the band. `FONTS.md` says the static IBM Plex Sans files are unverified as IBM's own release, while `licences.md` calls them official. | Design checklist presentations; review point 7. | Use vector logos if the tool allows, or record the limit; balance slide 2; settle the provenance of the static font files. | presentation-designer, identity-designer |
| N12 | Minor | Social post v02 headline; `…_v02.html` line 21 | The headline is 132 px. Ruling (h) approves the seven-column span, not a size above the display step. | `tokens.json` type scale. | Art-director approves 132 px for this format or the size is reduced. | art-director, graphic-designer |
| N13 | Minor | Guidelines v02 PDF, all footers and p6 "Still open"; guidelines p3 against icon v02 | Footers read "SYSTEM TEST, FICTIONAL CLIENT" and p6 carries internal open points; acceptable for the test, not for a client copy. The misuse page says "do not light more than one bar" and "always seven", while icon v02 lights three of twenty-one; the pattern rule on p5 explains it but the misuse page does not. | `quality-standards.md`; brand checklist. | Add one line on the misuse page exempting the stacked pattern and icon; strip test markers in any client version. | identity-designer |
| N14 | Minor | `06-profiles/`, `07-presentations/`, `05-designs/social-launch/` | Superseded v01 PDF, HTML, PPTX and PNG files remain beside v02 rather than in `_archive/`. | `file-management.md` versions. | Move v01 to each stage's `_archive/` with a reason; nothing is deleted. | Creative Director |

## Ten-point table: company profile v02

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Seven bars with the fourth lit carry the cover, the header logo and the closing Ember field on p4. |
| 2 | Distinctiveness | PASS | Viewed the three competitor home-page captures; no shared mark, palette or layout. Limited to home pages. |
| 3 | Colour consistency | PASS | Only the five approved colours; Ash captions sit on Paper only; Paper on Ember (p4 tagline) is 4.56:1. |
| 4 | Arabic and English typography | PASS, subject to the proofread | Script PASS: 928 Arabic characters, no presentation forms, eight static Plex faces embedded. Letters are connected on all four pages. Arabic is 11.5 pt against 10 pt Latin. |
| 5 | Logo clarity | PASS | Bilingual lockup on the cover; primary at header size on p2 to p4; on-Ember version with Ink bars and Paper lit bar on p4. |
| 6 | Layout | PASS | Arabic right and English left on the 4 + 3 split throughout; item numbers aligned. Minor: N9. |
| 7 | Consistency across pages | PASS | Same header, footer, hairlines and type ladder on p2 to p4. Minor: N8. |
| 8 | Accuracy | PASS | Every statement traces to the brief: 2023, Riyadh, weekly to order, 250 g and 1 kg, the four services, the email. No placeholder or draft marker. Vision, mission and values match `brand-context.md` section 3. |
| 9 | Export quality | PASS | A4, 4 pages, fonts embedded and subset, screen PDF, correct file name, HTML source alongside with static fonts. |
| 10 | Matches client requirements | PASS | 4 pages, bilingual, PDF, as brief section 10 C asks. |

No point fails, so the profile is PASS WITH MINOR FIXES, held only by the proofread.

## Not checked

- **Native Arabic proofread:** I read all Arabic in the profile, deck, post and landing page and found no error, which does not replace a native reader. I did not proofread every line of the six guidelines pages; I viewed them two pages to a sheet.
- **Trademark and mark search:** none exists to review.
- **Competitors beyond home pages:** packaging, social accounts and other Saudi roasters were not seen.
- **Guidelines p4 colour-blindness figures (2.4:1, 3.9:1):** not recomputed.
- **Landing page:** not opened in a browser by me. I read the source and viewed the maker's 1440 and 390 px default-state screenshots; the error and success screenshots, keyboard and screen-reader behaviour, and real devices were not checked.
- **Animation:** judged from ffprobe and four extracted frames (0, 0.5, 1.4 and 2.9 s); not watched in motion.
- **PPTX:** re-rendered in LibreOffice only, not opened in PowerPoint or Keynote.
- **Logo files:** all 50 SVGs audited by colour and element; PNG sizes and modes checked for all 135, colours for two; one of the 45 PDFs opened. Not re-tested at 16 px or 10 mm; I relied on the maker's bar-count file.
- **Applications v02 (card and bag label):** viewed as small previews and scanned in source for phone numbers, dates and Ash on Crema; small text not proofread.
- **Print:** no print file is in scope, so CMYK, bleed and crop marks do not apply.
- **Figma and Canva files:** not opened.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — round 2 re-review of profile, identity, presentation and social post, plus first review of the logo animation and landing page
Status: DONE
Files produced: none in the repo. Temporary previews only, in /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc2/
Tool operations: `bash scripts/setup.sh` (exit 0, 12 Arabic font faces). `python3 scripts/check_arabic_pdf.py` on the profile, guidelines and deck v02 PDFs, each RESULT: PASS, previews viewed. `pdfinfo`, `pdffonts`, `pdftotext`. `ffprobe` on the MP4 (H.264 High, 1080 × 1080, 30 fps, 90 frames, 3.0 s, bt709) and four frames extracted with `ffmpeg` and viewed. LibreOffice re-render of the PPTX to the scratchpad, compared with the supplied PDF by ImageMagick `compare`: 0 differing pixels on all five slides at 40 dpi. Pillow and zipfile inspection of the PNGs, SVGs and PPTX. No Figma, Canva or export operations. No project file was modified.
Decisions needed: (1) Sample offer on the landing page: confirm with the client or remove; I recommend removing it until confirmed. (2) Mark conflict check (r1 issue 16): have an agent with web access run a preliminary search, or log a scoped waiver like ruling (e); I recommend running it, since the wordmark and a generic bar device are both weak marks. (3) Animation: art-director ruling on partial bar counts during a build and on the fade; I recommend allowing the build provided the first and last held frames show seven bars or none. (4) Ember on two landing-page buttons and the 132 px social headline: art-director to approve or reject. (5) Whether the logo animation is in scope; log it either way.
Assumptions: this report is saved by the Creative Director as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_all-deliverables_2026-11-13_r2.md`. Test rulings by the Creative Director acting as client are treated as valid closures. The native proofread is treated as a single standing condition, as instructed, and not counted against each verdict.
Issues / risks: overall FAIL. One critical (landing page sample offer) and two majors (mark conflict check not run; animation without art-director approval). The native Arabic proofread still blocks all client delivery. `brand-context.md` and four identity documents contradict the latest rulings. Distinctiveness rests on home pages only.
Suggested next agent: ui-ux-designer (N1, N7; needs the ruling on the sample offer and tokens v02); art-director (N2, N4, N5, N12; needs the storyboard, the MP4 and the addendum); naming-specialist or market-researcher with web access (r1 issue 16; needs the logo SVGs and `licences.md`); identity-designer (N4, N8, N10, N13); corporate-designer (N8, N9); presentation-designer (N11); graphic-designer (N3). Then quality-reviewer for round 3 on the identity, animation and landing page only.
