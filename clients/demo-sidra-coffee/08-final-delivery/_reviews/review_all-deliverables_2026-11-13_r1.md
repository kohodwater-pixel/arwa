> Saved by the Creative Director from the quality-reviewer's handoff (the reviewer has no write access). SYSTEM TEST — fictional client.

# Quality review: demo-sidra-coffee, round 1 (2026-11-13)

## Verdicts

| Deliverable | Verdict | Why |
|---|---|---|
| 1. Company profile (`06-profiles/..._company-profile_screen_ar-en_v01.pdf`) | **FAIL** | Placeholder box and "DRAFT V01" on client-facing pages; Arabic not proofread; one misleading Arabic sentence; tagline unconfirmed; distinctiveness unverified. No invented facts found. |
| 2. Identity (logo SVGs, `system.md`, `tokens.json`, guidelines PDF) | **FAIL** | Distinctiveness never checked against real competitors; no mark conflict check; wordmark is not the custom drawing the direction asked for; no Pantone or calibrated CMYK; logo PNGs missing; bilingual lockup fails at 16 px and 10 mm; `brand-context.md` section 5 is empty. |
| 3. Presentation (PDF + PPTX) | **FAIL** | Slide 2 implies an unconfirmed delivery-timing promise; slide 3 steps do not align with the bars as the storyline says; fonts not embedded or listed; no master; not proofread. |
| 4. Social post (PNG) | **FAIL** | The call to action invents an enquiry channel (Instagram direct message) that is not in the brief; tagline unconfirmed; not proofread. Craft and technical checks are clean. |
| **Overall** | **FAIL** | Nothing goes to the client or into `08-final-delivery/` until the critical and major issues are fixed and re-reviewed. |

What held up across all four pieces:
- **No fabrication:** no invented clients, figures, awards, certifications, team names, roast or delivery days were found, and the dummy phone number is not printed in the profile, deck or post.
- **Arabic shaping:** correct and right to left in every export I viewed.
- **Fonts:** all three PDFs pass `check_arabic_pdf.py` with the intended fonts and no fallback.
- **Colour:** the five approved HEX values are used exactly in the HTML and PPTX sources and in all 45 SVGs.
- **Tracking:** none is applied to Arabic.

## Ten-point table: company profile

| # | Point | Score | Evidence |
|---|---|---|---|
| 1 | Creative idea | PASS | Seven-bar "Weekly Beat" with the fourth bar lit carries the cover, the header logo and the closing field. |
| 2 | Distinctiveness | FAIL (not verifiable) | `02-research/competitor-audit.md` lines 10 to 61 label all competitor visuals "unverified recall", so no side-by-side comparison exists. The Brew92 red question in the creative direction is still open. |
| 3 | Colour consistency | PASS | Only #F3ECE0, #E3C9A0, #1F1B18, #C23A20 and #6F6861 in the HTML. No Ash on Crema; Ember appears once per page plus the lit bar; all text pairs meet AA. |
| 4 | Arabic and English typography | PASS (script and visual) / FAIL (proofreading) | Script PASS: IBM Plex Sans Arabic and IBM Plex Sans embedded, 982 Arabic characters, no presentation forms; letters connected on all four pages. Native proofreading is not done (content-gaps C8), which `arabic-design.md` requires. |
| 5 | Logo clarity | PASS | Cover uses the bilingual colour lockup; pages 2 to 4 use the primary at 40 px high (minimum 32); page 4 uses the on-Ember version with Ink bars and Paper lit bar; clear space respected. |
| 6 | Layout | PASS with minor notes | Seven-column 4 + 3 split holds on all pages, Arabic right and English left. Minor: widows and a baseline misalignment on page 3 (issues 11 and 12). |
| 7 | Consistency across pages | PASS with minor notes | Same header, footer, hairlines and type on pages 2 to 4. Headings at 28/32 pt and 40/46 pt are outside the approved scale steps. |
| 8 | Accuracy | **FAIL** | No invented fact found. But page 4 carries "[Placeholder: number to be supplied]" / «[بيان ناقص: رقم الهاتف يُضاف لاحقًا]», every footer reads "DRAFT V01", and the page 2 Arabic sentence reads as "brews at home over the internet". |
| 9 | Export quality | PASS | A4, 4 pages, fonts embedded and subset, sRGB screen PDF, name follows `file-delivery.md`. Minor: the HTML source loads Latin fonts from `04-identity/_work/fonts/`. |
| 10 | Matches client requirements | PASS (format) | 4 pages, bilingual, PDF plus HTML source, as brief section 10 C asks. Content is not client-approved (outline status "draft"). |

Result: points 2, 4 (proofreading) and 8 fail, so the profile is FAIL.

## Issues

| # | Severity | File and location | What is wrong | Rule broken | Fix required | Agent |
|---|---|---|---|---|---|---|
| 1 | Critical | Whole identity; `02-research/competitor-audit.md`; `system.md` section 5 | Distinctiveness has never been checked against the real identities of Camel Step, Elixir Bunn and Brew92. | Project review point 2; brand checklist "distinct from every competitor". | Open the three competitors' sites, bags and social pages; record marks, palettes and type with sources; then compare the mark and Ember side by side. | market-researcher, then art-director |
| 2 | Critical | `05-designs/social-launch/..._instagram-post_wholesale_ar_v01.png`, lower left | «لطلبات المقاهي بالجملة، راسلنا على الخاص.» asserts that the brand takes wholesale orders by Instagram direct message. No handle or channel is in the brief or `brand-context.md` (website and social are TBC); `notes.md` deviation 3 admits it is an assumption. | Review point 8; honesty rules. | Replace with the verified email, or get the channel confirmed and logged before use. Also lift the register of «على الخاص». | graphic-designer (Creative Director gets the confirmation) |
| 3 | Major | Profile PDF page 4, phone row; footers of pages 1 to 4; PDF title "(draft v01)" | Dashed placeholder boxes in both languages and "DRAFT V01" / «مسودة v01» on every page. Honestly marked, and consistent with the decision log, but not client-ready. | `quality-standards.md` "no placeholder text"; creative direction section 7. | Remove the phone row until the number arrives (email and city are enough); remove the draft markers in the client version. | corporate-designer |
| 4 | Major | Profile PDF page 2, About us, Arabic lines 2 to 3 | «ولمن يحضّر قهوته في بيته عبر الإنترنت» attaches "online" to brewing, not selling. | Zero grammar errors; "translate meaning". | Recast, for example «ونبيعها للمقاهي، وعبر الإنترنت لمن يحضّر قهوته في بيته». | corporate-designer |
| 5 | Major | Profile, deck, social post, guidelines: all Arabic copy | No native Arabic proofread has been done; every maker says so. Vision and mission Arabic are designer drafts. «محاصيل مفردة» for "single origin" needs a native check. | `arabic-design.md` production checks; design checklist. | Native proofread of all four pieces before the next review. | Creative Director to arrange; makers apply |
| 6 | Major | Profile pages 1 and 4; deck slide 1; social headline | The tagline is used as final, but `brand-context.md` section 3 says "Tagline: TBC" and the client has not chosen it. The profile also addresses home brewers (subscription), while the tagline is wholesale-only. | Decision log 2026-11-13; creative direction section 7. | Get the tagline confirmed and logged; decide whether the profile counts as wholesale material. | Creative Director |
| 7 | Major | Profile PDF page 2, About us, English | "Sidra is a specialty coffee roastery…" uses "Sidra" alone. | Decision log 2026-11-13; creative direction section 7. | "Sidra Coffee roastery is…" or equivalent. | corporate-designer |
| 8 | Major | Deck PDF slide 2, body line | «سدرة موجودة لتجيب عنهما بإيقاع ثابت» promises an answer to "when does my next order arrive?" and "when was this roasted?". Delivery timing and roast date on the bag are TBC. | Review point 8; `messaging.md` line 73. | Reword to the verified fact only (weekly, to order), with no implied arrival promise. | presentation-designer |
| 9 | Major | Deck PDF slide 3 | The storyline says step 2 «نحمّص» sits under the lit bar; it sits under bars 2 to 3, and the three steps are unevenly spaced. Tying steps to bars also nears the "never a chart, not a roast day" rule. | Review point 6; creative direction section 4. | Align the steps to a consistent column logic; art-director to rule on whether steps may be tied to bars at all. | presentation-designer, art-director |
| 10 | Major | Deck `.pptx` | No embedded fonts and no font list or folder alongside. No brand master (11 default layouts; storyline admits it). Email and numerals are set in the Arabic font's Latin glyphs, not IBM Plex Sans. | `file-delivery.md` presentations; design checklist. | Add a font note or packaged fonts; build a master with the five layouts; set Latin runs in IBM Plex Sans. | presentation-designer |
| 11 | Minor | Profile PDF page 3, row 02; page 2 vision and values | Widows: "cafés" alone on a heading line, "first." and "Hospitality" alone. | `quality-standards.md` craft. | Rebreak or adjust measure. | corporate-designer |
| 12 | Minor | Profile PDF page 3, Arabic item numbers | Arabic "01" to "04" sit lower against their headings than the English ones. | Review point 6. | Align numerals to the heading baseline on both sides. | corporate-designer |
| 13 | Minor | Profile HTML CSS | Headings at 28/32 pt and 40/46 pt and paddings of 5, 6 and 12 px are outside the approved scale and spacing steps. Captions at 6.5/7.5 pt follow the spec but are very small on screen. | `system.md` sections 3 and 4. | Bring onto the scale, or record the A4 profile ladder in the system. | corporate-designer, identity-designer |
| 14 | Minor | Profile HTML `@font-face` | Latin fonts load from `04-identity/_work/fonts/`, which `licences.md` says must not ship. | `file-delivery.md` sources. | Point to official static IBM Plex Sans files before delivery. | corporate-designer |
| 15 | Major | `04-identity/02-logo/` wordmark; `system.md` section 7.1 | The wordmark is unmodified IBM Plex Sans Arabic Bold with two spacing tweaks. The direction asks for a custom wordmark "not simply typed in it". | Creative direction section 5. | Redraw, or record an explicit client-level decision to accept. | identity-designer, art-director |
| 16 | Major | `system.md` section 5; `licences.md` | No conflict check on the mark; the name check was one web search. | Brand checklist; `branding.md` originality. | Run a preliminary mark check and state the result with the not-legal-clearance notice. | identity-designer, naming-specialist |
| 17 | Major | `tokens.json`; guidelines PDF page 4 | Pantone is "to be matched by printer" for all five colours; CMYK is uncalibrated estimates. | `branding.md` identity minimums; `file-delivery.md` colour. | Convert through an ICC profile and give nearest Pantone, or have the Creative Director log a scoped waiver. | identity-designer |
| 18 | Major | `04-identity/02-logo/` | 45 SVGs only: no PNG at 1x/2x/4x and no vector PDF. The brief lists PNG as a format. | `file-delivery.md` formats; review point 10. | Export the PNG and PDF sets. | identity-designer |
| 19 | Major | `test_logo_bar-count.json`; `system.md` size tests | The bilingual lockup fails at 16 px and is unusable at 10 mm; primary and icon merge bars at 16 px. Fallbacks are documented. The icon's bar count is unstable at 32 px (5 counted) and the icon reads as a barcode in the preview. | Brand checklist "legible at 16 px and 10 mm". | Art-director to accept the fallback ladder formally or ask for a redraw; review the icon proportion. | art-director, identity-designer |
| 20 | Major | `brand-context.md` section 5 | "approved: date" with empty colour table, typefaces, imagery and do-nots; current stage still reads 04-identity. Values exist only in the decision log row. | `file-management.md` single source of truth. | Fill section 5 from `system.md` section 8 once the identity decision is made. | Creative Director |
| 21 | Minor | `creative-direction.md` section 2 | Says Ink on Ember is 3.9:1; computed value is 3.19:1 (`system.md`, `tokens.json` and guidelines say 3.2). | Review point 3. | Correct the figure. | art-director |
| 22 | Minor | Guidelines PDF page 1 cover pattern | Stacked rows use wide (rule-like) bars; the system says patterns are band rows, taller than wide. | Creative direction section 4. | Redraw the cover pattern in band proportion or amend the rule. | identity-designer |
| 23 | Minor | Guidelines PDF fonts; page 6 | Variable "IBMPlexSans-Regular" is embedded for the 85% width figures; the business card preview shows the dummy number "+966 5X XXX XXXX" (marked placeholder, allowed by the decision log for the test only). | `file-delivery.md` static fonts; creative direction section 7. | Settle the condensed-figure font; remove the number from the card before any client use. | identity-designer |
| 24 | Minor | Deck `.pptx` and PDF | `sldSz` is typed `screen4x3` although the size is 16:9; logos are PNG rasters; the slide counter is very small; slide 4 caption «حجما الكيس: محاصيل مفردة وخلطات البيت» is a non sequitur. | Design checklist presentations. | Fix the attribute, enlarge the counter, rewrite the caption. | presentation-designer |
| 25 | Minor | Social PNG | Untagged RGB with no sRGB profile; headline at 132 px is above the 115 px step and spans seven columns; the bars run off the bottom edge without art-director sign-off. | `file-delivery.md` sRGB; creative direction section 4. | Embed sRGB; art-director to approve or reject the three deviations. | graphic-designer, art-director |
| 26 | Minor | `brand-context.md` section 1, Canva design link | The linked Canva post is recorded as off-brand in `notes.md` section 6 but is still listed with no warning. | `tools-figma-canva.md`. | Annotate as rejected test output or remove the reference. | Creative Director |

Severity on issue 3: I rated it major, not critical, because the gap is honestly marked and the decision log allowed it for the test. It still fails review point 8 as written.

## Not checked

- **Native Arabic proofreading:** I read all Arabic text and flagged what I could; this does not replace a native proofread.
- **Competitor comparison:** no verified competitor visuals exist in `02-research/`.
- **Second viewer / second machine:** PDFs were checked with poppler and PyMuPDF only; the PPTX was inspected as XML and through the supplied LibreOffice PDF, not opened in PowerPoint or Keynote.
- **Guidelines PDF small text:** pages viewed as contact sheets at reduced size, enough for layout, colour and shaping; I did not proofread every line of the 6 pages.
- **Logo SVGs:** audited by element and colour (paths and rects only, correct fills, 7 bars) and through the maker's `_work` previews; not independently re-rendered at 16 px or 10 mm.
- **Out of scope here:** the landing page, `04-applications/` HTML files, `brand.css` beyond a colour and tracking scan, and the Figma and Canva files (tools not loaded).
- **Print:** nothing here is a print file, so CMYK, bleed and crop marks were not applicable.
- **Device test:** the Instagram 3:4 grid crop was not tested on a device.

## HANDOFF
Agent: quality-reviewer
Client / task: demo-sidra-coffee — ten-point review of company profile, identity, presentation and social post (round 1)
Status: DONE
Files produced: none in the repo. Temporary previews only, outside the client folder: /tmp/claude-0/-home-user-arwa/bbc1fe40-73a4-5cda-add7-c85ae04f8fb7/scratchpad/qc/ (profile/, guide/, deck/ page PNGs; g1.png, g2.png, d1.png contact sheets)
Tool operations: `python3 scripts/check_arabic_pdf.py` on the three PDFs, each RESULT: PASS with previews viewed; `pdfinfo`, `pdffonts`, `pdftotext`; ImageMagick `montage` for contact sheets; Python zipfile and Pillow inspection of the PPTX and PNG. No Figma, Canva or export operations.
Decisions needed: (1) Tagline: confirm option 1 with the client and say whether the profile is wholesale material; recommend confirming and keeping it on the deck and post, and removing it from the profile if home brewers remain a reader. (2) Wordmark: accept outlined Plex Bold or commission a redraw; recommend a redraw before any real use. (3) Pantone and calibrated CMYK: supply or log a scoped waiver; recommend supplying. (4) Phone placeholder: recommend removing the row from the profile and card until the number arrives. (5) Slide 3: may steps be tied to bars; recommend the art-director rules before the fix. (6) Social call to action: recommend the verified email in place of direct message.
Assumptions: the review round is r1; the Creative Director saves this report as `clients/demo-sidra-coffee/08-final-delivery/_reviews/review_<deliverable>_2026-11-13_r1.md`. Severity of the marked placeholder set at major on the strength of the decision log.
Issues / risks: all four deliverables FAIL; two critical issues (distinctiveness unverified, invented enquiry channel on the social post). Native proofread, competitor visuals and PowerPoint rendering were not verifiable by me. My first pass was interrupted by a rate limit; the scratchpad previews survived and no check was repeated.
Suggested next agent: market-researcher (verify competitor visuals, issue 1), then in parallel corporate-designer (issues 3, 4, 7, 11 to 14), presentation-designer (8, 9, 10, 24), graphic-designer (2, 25), identity-designer (15 to 19, 22, 23) and art-director (9, 19, 21, 25); then back to quality-reviewer for round 2 with this issues table as input.
