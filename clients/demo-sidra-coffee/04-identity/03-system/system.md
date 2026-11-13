# Identity system — Sidra Coffee (سدرة للقهوة)

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v03  **Date:** 2026-11-13  **Prepared by:** Identity Designer  **Status:** v03 accepted for the system test only, 2026-11-13 (not client-approved); passed quality review r3 with minor fixes. Stale lines corrected after r3 (issue I2, section 13)
**Previous versions:** `_archive/system_v03a.md` (v03 as reviewed in r3, before the corrections in section 13), `_archive/system_v02.md`, `_archive/system_v01.md`. What changed in v03 is listed in section 12; v02 changes are in section 9.
**Built from:** `01-direction/creative-direction.md` (Direction A "Weekly Beat", approved 2026-11-13) as amended by `creative-direction-amendment-01.md` and `creative-direction-amendment-02.md`; where they differ, the later amendment wins. Machine-readable values: `tokens.json`. Shared CSS: `brand-v02.css` (unchanged in v03; `brand.css` is the v01 file, kept because archived v01 HTML files link to it).

## 1. Palette and roles

| Name | HEX | RGB | CMYK (approximate) | Pantone | Role | Share |
|---|---|---|---|---|---|---|
| Paper — ورق | `#F3ECE0` | 243 236 224 | 4 6 12 0 | waived for system test; required before print | Default background | 45% |
| Crema — كريما | `#E3C9A0` | 227 201 160 | 10 20 40 0 | waived for system test; required before print | Warm second ground: panels, alternate pages, 250 g bag | 25% |
| Ink — حبر | `#1F1B18` | 31 27 24 | 60 60 60 85 (large solids); text prints 0 0 0 100 | waived for system test; required before print | All text, the six unlit bars, rules | 15% |
| Ember — جمر | `#C23A20` | 194 58 32 | 15 90 100 5 | waived for system test; required before print | The lit bar; one headline or one field per layout; the 1 kg bag; on web, the one primary action button per screenful (section 10) | 10% |
| Ash — رماد | `#6F6861` | 111 104 97 | 50 47 50 20 | waived for system test; required before print | Captions and small technical text, on Paper only | 5% |

- **CMYK values are my uncalibrated estimates, not conversions through an ICC profile.** Pantone references and ICC-calibrated CMYK are **waived for system test; required before print** (decision log 2026-11-13, ruling e).
- Rules carried from the direction: Crema on at least one surface of any multi-surface piece; Ember once per layout plus the lit bar, never body text; no green, gradients or tints.

## 2. Contrast (WCAG 2.x, computed from the HEX values on 2026-11-13)

| Pair (text on ground) | Ratio | Use |
|---|---|---|
| Ink on Paper / Paper on Ink | 14.56:1 | Any text |
| Ink on Crema / Crema on Ink | 10.69:1 | Any text |
| Paper on Ember | 4.56:1 | Any text (passes AA by a small margin: do not lighten Ember) |
| Ash on Paper | 4.67:1 | Captions |
| Ember on Paper | 4.56:1 | 24 px and above only (direction rule) |
| **Ink on Ember** | **3.19:1** | Bars and rules (graphics). Text only at 24 px / 18 pt and above, or 19 px / 14 pt Bold and above; prefer Paper on Ember for any text |
| Ash on Crema | 3.43:1 | Not for text |
| Ember on Crema | 3.35:1 | Not for text; fine for the lit bar |
| Crema on Paper | 1.36:1 | Not for text |

**Ink on Ember is 3.19:1, not 3.9:1.** `creative-direction.md` section 2 gives 3.9:1; that figure is wrong and was corrected by the art-director in amendment 01 section 1 (the approved direction file itself is left unchanged). 3.19 clears the 3:1 threshold for large text and graphics with very little margin, so the rule was tightened as in the table above. Wherever 3.9:1 still appears in an older file, 3.19:1 is the value to use. All other figures in the direction match to one decimal.

**Colour blindness** (Machado et al. 2009 simulation matrices, full severity, computed):

| Pair | Normal | Protan | Deutan | Tritan |
|---|---|---|---|---|
| Lit bar (Ember) against Ink bars | 3.19 | **2.39** | 3.71 | 3.18 |
| Ember against Paper | 4.56 | 6.06 | 3.93 | 4.57 |
| Ember against Crema | 3.35 | 4.32 | 2.94 | 3.34 |

Finding: for red-blind viewers the lit bar is weakly separated from the Ink bars (2.39:1). The system does not rely on colour alone, because the lit bar is always the fourth bar, but this is a real weakness of Ember-on-Ink adjacency. On Ember grounds (Ink bars, Paper lit bar) the separation is 14.56:1 and is unaffected.

## 3. Typography

**Arabic: IBM Plex Sans Arabic. Latin: IBM Plex Sans.** Both SIL OFL 1.1 (see `../licences.md`). Static files: `assets/fonts/ibmplexsansarabic/` and `assets/fonts/ibmplexsans-static/` (static Light, Regular, Medium, SemiBold, Bold; IBM Plex Sans 3.006 by their own metadata, download source not recorded, see `../licences.md`). The variable font and the instances in `_work/fonts/` have not been used by any current file since v02.
Fallbacks: Arabic — Noto Sans Arabic, Geeza Pro, Tahoma. Latin — Helvetica Neue, Arial.

| Level | Scale | Arabic | Latin | Line height AR / EN | Screen px AR / EN | Print pt AR / EN |
|---|---|---|---|---|---|---|
| Display headline | 5 | Bold 700 | Bold 700, tracking -1.5% | 1.3 / 1.05 | 115 / 100 | 57.5 / 50 |
| Sub-head | 1.6 | Medium 500 | Medium 500 | 1.5 / 1.3 | 37 / 32 | 18.5 / 16 |
| Body | 1 | Regular 400 | Regular 400 | 1.75 / 1.45 | 23 / 20 | 11.5 / 10 |
| Product label | 1 | SemiBold 600 or Bold 700 | SemiBold 600 | 1.5 / 1.3 | 23 / 20 | 11.5 / 10 |
| Caption | 0.65 | Regular 400, Ash | SemiBold 600, uppercase, tracking +12%, Ash | 1.6 / 1.4 | 15 / 13 | 7.5 / 6.5 |
| Large figures | free | Bold 700, unit in Arabic (1 كغ) | Light 300, regular width (v02; the 85% width in the direction needs the variable font and was dropped) | — | — | — |

- Arabic sizes are the Latin size × 1.15 (allowed range 1.15 to 1.20) so the two scripts read as equal.
- Arabic: no tracking, no uppercase styling, no faux bold, no slant. Tracking is for Latin captions and the Latin logo line only.
- Numerals: Western (0123) in both languages. Arabic punctuation ، ؛ ؟ «» in Arabic text.
- Small pieces (business card, label) may scale the whole ladder down, keeping the ratios. The mini guidelines use a 9 pt Latin / 10.5 pt Arabic body.

### 3.1 A4 document ladder (amendment 01 section 9; review r2 N8)

The four-step scale (0.65 / 1 / 1.6 / 5) stays the identity scale. On A4 documents the Latin block is held to three columns and the display step does not fit, so two steps are added **for A4 documents only** (company profile, proposals, reports).

| Level | Scale | Latin | Arabic | Line height EN / AR |
|---|---|---|---|---|
| Caption | 0.65 | 6.5 pt SemiBold, uppercase, +12% | 7.5 pt Regular | 1.4 / 1.6 |
| Body | 1 | 10 pt Regular | 11.5 pt Regular | 1.45 / 1.75 |
| Sub-head | 1.6 | 16 pt Medium | 18.5 pt Medium | 1.3 / 1.5 |
| **Section title** | 2.8 | **28 pt** Bold, -1.5% | **32 pt** Bold | 1.1 / 1.3 |
| **Cover title** | 4 | **40 pt** Bold, -1.5% | **46 pt** Bold | 1.05 / 1.3 |

- One section title per page; the cover title appears on the cover only.
- Tracking applies to the Latin only; Arabic is never tracked.
- These two steps are not used on social, presentation or packaging formats.

### 3.2 Social ladder, formats 1080 px wide (amendment 02 section 4; review r2 N12)

For 1080 × 1080, 1080 × 1350 and 1080 × 1920 only. It is the screen ladder × 1.15, because a 1080 px canvas is seen on a phone at about a third of its pixel size.

| Level | Arabic | Latin beside it |
|---|---|---|
| Display headline | **132 px** Bold, line height 1.3 | 115 px Bold, -1.5%, 1.05 |
| Sub-head | **42 px** Medium, 1.5 | 37 px Medium, 1.3 |
| Body and call to action | **27 px** Regular, 1.75 | 23.5 px Regular, 1.45 |
| Caption | **17.5 px** Regular, Ash on Paper only | 15 px SemiBold, uppercase, +12% |

- 132 px is the maximum, not a starting point. A longer headline drops to the sub-head step or is rewritten shorter; no sizes in between and nothing above 132 px.
- One display headline per post.
- Web, slides, documents and packaging keep their own ladders.

### 3.3 Caption floor on screen

On screen-only pieces no caption or other text is set below **9 px** (decision log 2026-11-13, art-director rulings). The screen caption step is 15 / 13 px, so the floor matters only where a small piece scales the whole ladder down: stop at 9 px. Print captions stay at 7.5 / 6.5 pt.

## 4. Grid and the seven-bar system

- Seven equal columns between the margins. Gutter = 1/5 column for text layouts; none for full-bleed bands.
- Arabic layouts: text on 4 columns from the right, secondary content on 3 from the left. English-only layouts mirror this. Bilingual: Arabic block right, Latin block left, never line by line.
- Spacing steps (px, 4 px base): 4, 8, 16, 24, 40, 64, 104.
- Section break: 2 px Ink hairline, full width. Square corners. No shadows.
- Bar row: always seven equal bars, the fourth lit, gap = 1/5 bar width. **Rule** proportion 2:1 (logo, dividers); **band** proportion 1:2 to 1:4 (packaging, large fields). Pattern: three or more band rows stacked with the same gap, lit bars in one column. **"Always seven" and "one lit bar" are counted per row:** the stacked pattern and the icon therefore show more than seven bars and more than one lit bar in total, which is correct, provided the lit bars line up in one centre column. Never light two bars in one row, never stagger the lit bars from row to row, never stack fewer than three rows (amendment 02 section 2).
- Lit bar colour: Ember on Paper, Crema and Ink. **On Ember: Ink bars with a Paper lit bar** (see section 7, point 2). The bar row is a device, never a chart: nothing is labelled by, numbered by or tied to an individual bar (ruling f).
- No icon set, no illustration (direction section 6). Photography: beans, bags, equipment only, flat and frontal on Paper or Crema; no people or hands.

## 5. Logo specification

Files in `../02-logo/`, named `demo-sidra-coffee_logo_<lockup>-<colour>_<lang>_v01.svg` (icon with bars: `_v02`). All text is converted to outlines; the SVGs contain only `path` and `rect` and need no fonts.

| Lockup | Content | Use |
|---|---|---|
| `primary` (ar) | Wordmark سدرة + rule row of the same width | Default wherever Arabic is read |
| `bilingual` (ar-en) | Primary + SIDRA COFFEE spaced to the same width | Packaging, shared material |
| `latin` (en) | SIDRA COFFEE over the rule row | English-only contexts |
| `icon` (ar-en), **v02** | Three stacked band rows of seven bars filling the square, lit bars in the centre column | Avatars, favicons, stamps, from 48 px |
| `wordmark` (ar) | سدرة alone | Smallest sizes (fallback 3) |
| `*-small` | As above with one solid rule whose centre seventh is lit | Small sizes (fallback 2) |

Colour versions of each: `colour` (on Paper, Crema), `colour-reversed` (on Ink), `colour-on-ember`, `black` (#000000), `white` (#FFFFFF).

**Construction.** Wordmark width = W. Bar width = W / 8.2; bar height = half the bar width; gap = one fifth of the bar width. Clear space = height of the letter د = 0.269 W on every side.

**How the wordmark was made (stated plainly).** The word was shaped with HarfBuzz (`uharfbuzz` 0.57) and outlined with fontTools from IBM Plex Sans Arabic Bold; the Latin line from an IBM Plex Sans SemiBold instance. The only custom work on the Arabic is optical spacing between the unconnected letters (ر and ة pulled in by 22 and 14 font units). **The letterforms themselves are unmodified Plex Bold.** The direction asks for a wordmark "matched to Plex Bold but not simply typed in it"; this v01 does not fully meet that. See section 7, point 1.

**Size tests** (previews in `../02-logo/_work/`, automated bar count in `test_logo_bar-count.json`):

| Test | Result |
|---|---|
| Primary, 16 px high (28 px wide) | **Fails with seven bars**: gap is 0.68 px, bars merge (6 counted). Fallback 2 (`primary-small`) reads clearly, lit seventh visible. |
| Bilingual, 16 px high (22 px wide) | **Fails**: bars merge and the Latin line is illegible, also in the small version. Do not use the bilingual lockup below 48 px high. |
| Latin-led, 16 px high (70 px wide) | Passes: seven bars counted, lit bar distinct. |
| Icon, 16 px | **Fails with seven bars** (1 run counted). `icon-small` reads. |
| Primary 24 px / 32 px high | 7 bars counted at both; visibly soft at 24, clean at 32. Switch size set at 32. |
| Icon 24 / 32 / 48 px | 7 / 5 / 7 counted: unstable below 48 because of pixel-grid alignment. Switch size set at 48. |
| Reversed on Ink, 16 px | Same behaviour as on Paper. |
| 10 mm wide, simulated at 600 dpi, black, white-on-black, colour | Seven bars hold (gap 0.24 mm). **Simulation only, not press-tested.** The bilingual Latin line has a cap height of 0.83 mm at 10 mm and is too small; bilingual minimum set at 18 mm. |
| One colour (black, white) | Works, but the lit bar is not distinguishable (section 7, point 3). |
| On photography | **Not tested.** No licensed photography exists for this client and the direction forbids people imagery. |

**Switch sizes**

| Version | Screen | Print |
|---|---|---|
| Primary with seven bars | from 32 px high | from 10 mm wide |
| Bilingual with seven bars | from 48 px high | from 18 mm wide |
| Latin-led with seven bars | from 16 px high | from 25 mm wide (estimate) |
| Small version (solid rule) | 16 to 31 px high | 6 to 10 mm wide |
| Icon with bars / icon-small | from 48 px / 16 to 47 px | from 10 mm / from 5 mm |
| Wordmark alone | below 16 px | below 6 mm |

**Icon v02 (review issue 19).** The v01 icon (one row of 1:2 bars with a margin) still read as a barcode and its bar count was unstable. v02 uses the system's own pattern rule: three band rows (bar 1:2.6, inside the 1:2 to 1:4 band range), row gap equal to the bar gap, lit bars in one column, filling a 205-unit square so that bar = 25, gap = 5. It reads as a grid of weeks, not a barcode. **Confirmed by the art-director in amendment 02 section 2**, in place of the direction's one-row wording, together with the per-row reading of the misuse rules (section 4).

Bar count, same method as before (`../02-logo/_work/test_logo_icon-v02_bar-count.json`, sheet `test_logo_icon-v02_sizes.png`):

| Size | 16 px | 24 px | 32 px | 41 px | 48 px | 64 px | 96 px |
|---|---|---|---|---|---|---|---|
| Icon v01 (single row) | 1 | 7 | 5 | 5 | 7 | 7 | 7 |
| Icon v02 (each of 3 rows) | 6 | 6 | 6 | 7 | 7 | 7 | 7 |
| v02 gap in px | 0.39 | 0.59 | 0.78 | 1.00 | 1.17 | 1.56 | 2.34 |

v02 is stable from 41 px up; v01 was not stable until 48 px. Below 41 px the gap is under one pixel and seven bars cannot hold in any proportion while the 1/5 gap rule stands, so `icon-small` is still required from 16 to 47 px. The 48 px switch size (ruling g) is unchanged. The five superseded v01 icon files (`icon-<colour>_ar-en_v01.svg`) are now in `../02-logo/_archive/` with the reason (review r2 N10); no current file links to them. The `icon-small` v01 files are current and stay in `../02-logo/`.

**Export formats (review issue 18; r2 N10).** `../02-logo/png/`: transparent PNG at 1x, 2x and 4x for every current lockup and colour version (135 files). Re-exported in v03 at whole-pixel sizes, so 2x and 4x are exact multiples of 1x: lockups 204 / 408 / 816 px wide, icon 205 / 410 / 820, icon-small 200 / 400 / 800. The lockup artwork is 203.6 units wide, so each PNG is scaled up by 0.2% to reach 204 px, with the height rounded to a whole pixel at 1x; the PNGs are for screen use and the SVG stays the master. `../02-logo/pdf/`: vector PDF of each (45 files; checked with pdffonts and pdfimages: no fonts, no raster images). The superseded v01 icon was never exported. PDFs are RGB, straight from the SVG; no CMYK or spot-colour PDFs exist (print colour is waived for the test).

**Difference from competitors.** Compared on 2026-11-13 with the home pages of Camel Step, Elixir Bunn and Brew92: distinct from all three. Home pages only; not a trademark search. (Art-director, `../01-direction/distinctiveness-check_v02.md`, which is the record.) Camel Step: a line-drawn symbol in dark teal-blue on white, against Sidra's heavy Arabic wordmark on seven bars in Ember, Ink and warm Paper. Elixir Bunn: a thin calligraphic Arabic and serif Latin wordmark, black on white with green and gold and ornament, against a low-contrast sans wordmark, a counted bar device and no ornament; its red `#D92C20` is a sale label, not a brand colour, so Ember stays. Brew92: a thin Latin wordmark in electric blue on cool grey, English-led, against an Arabic-led mark. One overlap: Camel Step sets its site text in IBM Plex Sans Arabic, so the wordmark redraw is required before real use (section 7, point 1). "Arabic-first" is not claimed as a differentiator: two of the three are Arabic-led. Not seen: packaging, social accounts, signage, other roasters.

**Conflict check (review issue 16).** A preliminary web search was run by the naming-specialist on 2026-11-13 (`../mark-check.md`; summary in `../licences.md`). **Name: HIGH risk**: search results report a "Sidra" dining complex in Riyadh operated by Alshaya (same word, same city, food and beverage). **Medium risk:** "Sidra" is a coffee variety already sold by Riyadh roasters. **Device:** the seven-bar row could not be checked by text search; its status is unknown, not clear. A row of bars is a generic device and similar marks may exist. No trademark register was searched. **This is not a legal trademark clearance; a formal search and opinion by a trademark attorney is required before any real use.** For the system test the check is recorded and work continues (decision log).

## 6. Self-check against `quality-control/brand-checklist.md`

| Item | Result |
|---|---|
| Approved strategy reflected in brand-context | Pass |
| Each element traceable to strategy | Pass (seven bars = weekly promise; Arabic-led = "rooted and Arabic-led"; plain grid and facts = "plain-spoken") |
| Distinct from every competitor | **Pass within home-page evidence**: art-director's check v02, three competitors, home pages only |
| Primary, secondary, icon exist | Pass |
| Arabic, Latin, bilingual balanced | Pass by eye; no native reviewer |
| One colour, black, reversed | Pass, with the lit-bar caveat |
| Legible at 16 px and 10 mm | **Partial**: only with the fallback ladder, which was accepted for the test (ruling g); bilingual not usable at 16 px or 10 mm |
| Clear space and minimum size defined | Pass |
| Vector artwork clean, text outlined | Pass (paths and rects only, XML validated); curves are the font's own, not hand-optimised |
| Preliminary conflict check; trademark notice | **Done as a preliminary check, with a HIGH name risk found** (Alshaya "Sidra", Riyadh); device not checkable by text search; no register searched; not-legal-clearance notice in `licences.md`, `mark-check.md` and guidelines v04 p6. Counsel's opinion required before real use |
| HEX, RGB, CMYK, Pantone for every colour | **Waived for the test** (ruling e): CMYK approximate, Pantone not given; required before print |
| Text pairs meet AA | Pass |
| Colour-blindness check | Done; one weak pair reported |
| Palette proportions | Pass |
| Typefaces paired, licensed, hierarchy, fallbacks | Pass (static Latin files in `assets/fonts/ibmplexsans-static/`) |
| Graphic elements, iconography, imagery defined | Pass (iconography = none, by direction) |
| At least five applications | **Fail by scope**: two built (test scope set by the Creative Director) |
| Misuse examples | Pass (8 drawn, 5 written, plus the per-row note for the stacked pattern and icon in guidelines v04) |
| Guidelines follow outline and level | **Partial**: 6-page mini, below the "essential" level; sections 10 and 11 are one line each |
| No spelling errors | Not confirmed: Arabic not proofread by a native reader |
| Colour values match files | Pass |

## 7. Decisions and deviations (status after round 3)

1. **Wordmark is outlined Plex Bold with custom spacing, not a redrawn custom wordmark.** **Ruled (d): accepted for the test; redraw required before real use.**
2. **Bars on Ember.** The direction says both "six bars in Paper on Ember, lit bar Paper" (all seven Paper, lit bar invisible) and "1 kg bag in Ember with an Ink band". I resolved it as **Ink bars with a Paper lit bar on Ember**. **Confirmed: Ink bars with a Paper lit bar on Ember** (decision log 2026-11-13, identity v01 acceptance).
3. **One-colour versions cannot show the lit bar.** The direction forbids outlines and tints, so v01 uses seven solid bars. **Accepted: one-colour versions use seven solid bars** (decision log 2026-11-13, identity v01 acceptance). One-colour use is restricted to stamps, embossing and single-colour print.
4. **Phone number.** The direction says the placeholder number appears nowhere; the task brief for this build asked for it to be shown as a clearly marked placeholder. The business card shows it in a dashed box labelled as a placeholder. **Ruled (b): removed. Business card v02 has no phone number; email is the only contact channel.**
5. **Business card carries no personal name or title**, because no team names were supplied.
6. **Label size 100 × 170 mm** is my assumption; no bag dieline exists.
7. **Latin line reads "SIDRA COFFEE"** as the direction specifies, although naming.md warns that "Sidra coffee" reads as a variety in English. **Closed: the Latin line stays "SIDRA COFFEE"** (decision log 2026-11-13; amendment 02 section 7). "Roastery" is used in running copy.

## 8. `brand-context.md` section 5

Nothing is outstanding there. `brand-context.md` section 5 now carries, in the Creative Director's wording: the per-row counting of "always seven" and "one lit bar" (the stacked pattern and icon v02 are exempt), the web button rule (section 10), Ink on Ember 3.19:1, the motion summary (section 11) and the name rule below. The wording this file proposed earlier is kept in `_archive/system_v03a.md` and `_archive/system_v02.md`.

**Name rule** (from `brand-context.md` section 5; mitigation for the recorded name risk, section 5 "Conflict check"):

- Always the full name: «سدرة للقهوة» in Arabic and "Sidra Coffee" in English, with "roastery" in running English copy.
- Never «سدرة» or "Sidra" alone in text, and never beside an origin or variety word.
- The wordmark «سدرة» inside the logo is the only exception.

Held in this file and in `tokens.json` only, not in `brand-context.md` section 5: the A4 and social type ladders (sections 3.1 and 3.2). The 9 px screen caption floor (section 3.3) is in the decision log, not in section 5.

## 9. What changed in v02 (after quality review r1)

| Review issue | Action |
|---|---|
| 15 wordmark | No change. Accepted for the test by ruling (d); redraw required before real use. |
| 16 mark conflict check | Not run: this agent has no web tools. `licences.md` now states exactly what was and was not checked. |
| 17 Pantone, ICC CMYK | Waived by ruling (e). `tokens.json`, this file and guidelines v02 now say "waived for system test; required before print". |
| 18 formats | PNG 1x/2x/4x and vector PDF exported for every current lockup and colour version. |
| 19 fallback ladder, icon | Ladder accepted by ruling (g). Icon redrawn as v02; bar count re-run (section 5). |
| 22 cover pattern | Guidelines v02 cover pattern redrawn in band proportion (bar 10 × 20 mm, 1:2, three rows). |
| 23 fonts, phone number | v02 files use the official static IBM Plex Sans; large figures use Light 300 at regular width; `_work/fonts/` and the variable font are no longer referenced. Phone number removed (business card v02, guidelines v02 page 6). |
| Tagline | No "TBC" on the tagline remains in any `04-identity/` file. `brand-context.md` section 3 still reads "Tagline: TBC"; that file is the Creative Director's to edit. |

Also changed: bag label v02 (figure "1 kg" now regular-width Light, 50 pt). v01 files are all kept.


## 10. Ember on web: the button rule (ruling l; amendment 02 section 3)

- On a web or app screen, Ember may fill **the single primary action button in each screenful**, in addition to the lit bar. A screenful is what is visible without scrolling at 1440 × 900 and at 390 × 844; check both.
- Within one screenful the Ember button **takes the place of** the Ember field or headline: the lit bar plus either one Ember button or one Ember field or headline, never both (confirmed, decision log 2026-11-13).
- Button: Ember fill, Paper label (4.56:1), Medium 500 or heavier, square corners, no shadow.
- Every other button in the same screenful is Ink: Ink fill with Paper label, or a 2 px Ink outline with Ink label on Paper or Crema.
- **A header button that stays on screen while scrolling is always Ink.**
- States use solid colours only: hover and pressed = Ink fill with Paper label; focus = 2 px Ink outline set 2 px outside the button.
- Ember is never a body-text or link colour.
- Web and app screens only. Documents, slides, social and print keep "once per layout".

## 11. Motion rules, summary (amendment 02 section 1, which is the full text)

The static rules describe resting states. In any film, animated slide or web animation:

| Subject | Rule |
|---|---|
| Bar build | Bars may build in. Each appears in its final place and size by a hard-edged wipe or a hard cut; bars never slide, scale, bounce, rotate, swap or fade. Order follows the lockup's reading direction (right to left for Arabic and bilingual, left to right for Latin-led). Seven bars in 1.0 s at most. |
| Partial counts | No hold on a partial count: any moment where nothing moves for 0.1 s or more shows seven bars or none. Bars do not build out. |
| Lit bar | Ember appears only after all seven bars are present, only on the fourth, by a bottom-up hard-edged fill or a hard cut in 0.3 s at most. No blend, glow, pulse or flash. No other bar lights at any moment and the light never travels along the row. |
| Wordmark and Arabic text | Arrive whole: an opacity fade of the complete word or line in 0.5 s at most, or a hard cut. Never letter by letter, never by a wipe. This fade is the only exception to "no tints" and applies to transitions only; nothing is held part-way through it. |
| Ending | A film ends on the complete, static logo held for at least 1.0 s, with no fade-out. An empty Paper lead-in of up to 0.1 s is allowed. |
| Poster frame | Every film ships with a poster frame taken from the final hold. Stills and thumbnails are never taken from a build or a fade. |
| General | One easing, cubic ease-out. Flat colour and square corners; no blur, shadow, gradient or texture. Films work silent; sound only with a recorded licence. Web and app motion honours `prefers-reduced-motion` by showing the final state only. |

## 12. What changed in v03 (after quality review r2)

| Review issue | Action |
|---|---|
| N8 A4 ladder | Recorded in section 3.1 and in `tokens.json` (`font.ladder_a4_document_pt`). |
| N12 social ladder | The approved 1080-wide ladder (132 / 42 / 27 / 17.5 px Arabic) recorded in section 3.2 and in `tokens.json` (`font.ladder_social_1080_px`). |
| Caption floor | 9 px floor for screen-only pieces recorded in section 3.3 and in `tokens.json`. |
| Ruling (l) Ember button | Section 10 and `tokens.json` (`color.ember.web_button`, `button`). |
| Motion | Summary in section 11 and `tokens.json` (`motion`). |
| r1 21 Ink on Ember | 3.19:1 with the tightened text rule from amendment 01, in section 2 and `tokens.json`. |
| N4, r1 16 | Competitor and conflict-check paragraphs in section 5 and the self-check rows in section 6 rewritten to match `distinctiveness-check_v02.md` and `mark-check.md`. `licences.md` v03 and guidelines v03 p6 say the same. |
| N13 misuse exemption | Per-row counting stated in section 4 and on the guidelines v03 misuse page. |
| N10 | Icon v01 SVGs moved to `02-logo/_archive/`; PNGs re-exported at whole-pixel sizes (section 5). |

Not changed in v03: the logo SVGs and PDFs, `brand-v02.css`, the applications, the palette and every measured value.

## 13. Corrections after quality review r3 (issue I2; no version change)

The version stays v03: no value, rule or file specification changed. The text as reviewed in r3 is `_archive/system_v03a.md`.

| Place | Correction |
|---|---|
| Header | Status now matches `brand-context.md`: v03 accepted for the system test only, not client-approved. |
| Section 3 | The line on the variable font no longer names "v02 files". |
| Section 6 | References to the guidelines now point to v04. |
| Section 7, points 2 and 3 | Marked as decided: Ink bars with a Paper lit bar on Ember; one-colour versions use seven solid bars. |
| Section 8 | Rewritten: the per-row wording is in `brand-context.md`; the name rule is added. |

Guidelines v04 (review issue I3) adds the web button rule on p4, a motion block on p5 and the name rule on p6; it changes no value in this file.
