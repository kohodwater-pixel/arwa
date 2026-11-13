# Identity system — Sidra Coffee (سدرة للقهوة)

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v01  **Date:** 2026-11-13  **Prepared by:** Identity Designer  **Status:** for Creative Director review, not yet approved
**Built from:** `01-direction/creative-direction.md` (Direction A "Weekly Beat", approved 2026-11-13). Machine-readable values: `tokens.json`. Shared CSS: `brand.css`.

## 1. Palette and roles

| Name | HEX | RGB | CMYK (approximate) | Pantone | Role | Share |
|---|---|---|---|---|---|---|
| Paper — ورق | `#F3ECE0` | 243 236 224 | 4 6 12 0 | to be matched by printer | Default background | 45% |
| Crema — كريما | `#E3C9A0` | 227 201 160 | 10 20 40 0 | to be matched by printer | Warm second ground: panels, alternate pages, 250 g bag | 25% |
| Ink — حبر | `#1F1B18` | 31 27 24 | 60 60 60 85 (large solids); text prints 0 0 0 100 | to be matched by printer | All text, the six unlit bars, rules | 15% |
| Ember — جمر | `#C23A20` | 194 58 32 | 15 90 100 5 | to be matched by printer | The lit bar; one headline or one field per layout; the 1 kg bag | 10% |
| Ash — رماد | `#6F6861` | 111 104 97 | 50 47 50 20 | to be matched by printer | Captions and small technical text, on Paper only | 5% |

- **CMYK values are my uncalibrated estimates, not conversions through an ICC profile.** They are a starting point for the printer, who matches to the HEX value on a proof. No Pantone reference is licensed in this project, so none is quoted.
- Rules carried from the direction: Crema on at least one surface of any multi-surface piece; Ember once per layout plus the lit bar, never body text; no green, gradients or tints.

## 2. Contrast (WCAG 2.x, computed from the HEX values on 2026-11-13)

| Pair (text on ground) | Ratio | Use |
|---|---|---|
| Ink on Paper / Paper on Ink | 14.56:1 | Any text |
| Ink on Crema / Crema on Ink | 10.69:1 | Any text |
| Paper on Ember | 4.56:1 | Any text (passes AA by a small margin: do not lighten Ember) |
| Ash on Paper | 4.67:1 | Captions |
| Ember on Paper | 4.56:1 | 24 px and above only (direction rule) |
| **Ink on Ember** | **3.19:1** | Bars, rules and type of 24 px and above only |
| Ash on Crema | 3.43:1 | Not for text |
| Ember on Crema | 3.35:1 | Not for text; fine for the lit bar |
| Crema on Paper | 1.36:1 | Not for text |

**Correction to the direction:** `creative-direction.md` section 2 gives Ink on Ember as 3.9:1. The computed value is **3.19:1**. The rule (not below 24 px) still holds, since 3.19 clears the 3:1 large-text and graphics threshold, but the figure in the direction should be corrected by the art-director. All other figures in the direction match to one decimal.

**Colour blindness** (Machado et al. 2009 simulation matrices, full severity, computed):

| Pair | Normal | Protan | Deutan | Tritan |
|---|---|---|---|---|
| Lit bar (Ember) against Ink bars | 3.19 | **2.39** | 3.71 | 3.18 |
| Ember against Paper | 4.56 | 6.06 | 3.93 | 4.57 |
| Ember against Crema | 3.35 | 4.32 | 2.94 | 3.34 |

Finding: for red-blind viewers the lit bar is weakly separated from the Ink bars (2.39:1). The system does not rely on colour alone, because the lit bar is always the fourth bar, but this is a real weakness of Ember-on-Ink adjacency. On Ember grounds (Ink bars, Paper lit bar) the separation is 14.56:1 and is unaffected.

## 3. Typography

**Arabic: IBM Plex Sans Arabic. Latin: IBM Plex Sans.** Both SIL OFL 1.1 (see `../licences.md`).
Fallbacks: Arabic — Noto Sans Arabic, Geeza Pro, Tahoma. Latin — Helvetica Neue, Arial.

| Level | Scale | Arabic | Latin | Line height AR / EN | Screen px AR / EN | Print pt AR / EN |
|---|---|---|---|---|---|---|
| Display headline | 5 | Bold 700 | Bold 700, tracking -1.5% | 1.3 / 1.05 | 115 / 100 | 57.5 / 50 |
| Sub-head | 1.6 | Medium 500 | Medium 500 | 1.5 / 1.3 | 37 / 32 | 18.5 / 16 |
| Body | 1 | Regular 400 | Regular 400 | 1.75 / 1.45 | 23 / 20 | 11.5 / 10 |
| Product label | 1 | SemiBold 600 or Bold 700 | SemiBold 600 | 1.5 / 1.3 | 23 / 20 | 11.5 / 10 |
| Caption | 0.65 | Regular 400, Ash | SemiBold 600, uppercase, tracking +12%, Ash | 1.6 / 1.4 | 15 / 13 | 7.5 / 6.5 |
| Large figures | free | Bold 700, unit in Arabic (1 كغ) | Light 300, width 85% | — | — | — |

- Arabic sizes are the Latin size × 1.15 (allowed range 1.15 to 1.20) so the two scripts read as equal.
- Arabic: no tracking, no uppercase styling, no faux bold, no slant. Tracking is for Latin captions and the Latin logo line only.
- Numerals: Western (0123) in both languages. Arabic punctuation ، ؛ ؟ «» in Arabic text.
- Small pieces (business card, label) may scale the whole ladder down, keeping the ratios. The mini guidelines use a 9 pt Latin / 10.5 pt Arabic body.

## 4. Grid and the seven-bar system

- Seven equal columns between the margins. Gutter = 1/5 column for text layouts; none for full-bleed bands.
- Arabic layouts: text on 4 columns from the right, secondary content on 3 from the left. English-only layouts mirror this. Bilingual: Arabic block right, Latin block left, never line by line.
- Spacing steps (px, 4 px base): 4, 8, 16, 24, 40, 64, 104.
- Section break: 2 px Ink hairline, full width. Square corners. No shadows.
- Bar row: always seven equal bars, the fourth lit, gap = 1/5 bar width. **Rule** proportion 2:1 (logo, dividers); **band** proportion 1:2 to 1:4 (packaging, large fields). Pattern: three or more band rows stacked with the same gap, lit bars in one column.
- Lit bar colour: Ember on Paper, Crema and Ink. **On Ember: Ink bars with a Paper lit bar** (see section 7, point 2).
- No icon set, no illustration (direction section 6). Photography: beans, bags, equipment only, flat and frontal on Paper or Crema; no people or hands.

## 5. Logo specification

Files in `../02-logo/`, named `demo-sidra-coffee_logo_<lockup>-<colour>_<lang>_v01.svg`. All text is converted to outlines; the SVGs contain only `path` and `rect` and need no fonts.

| Lockup | Content | Use |
|---|---|---|
| `primary` (ar) | Wordmark سدرة + rule row of the same width | Default wherever Arabic is read |
| `bilingual` (ar-en) | Primary + SIDRA COFFEE spaced to the same width | Packaging, shared material |
| `latin` (en) | SIDRA COFFEE over the rule row | English-only contexts |
| `icon` (ar-en) | Seven bars centred in a square | Avatars, favicons, stamps |
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

**Barcode fallback 1 applied:** the icon was first drawn with 1:4 bars and read as a barcode; it now uses 1:2, the widest band proportion.

**Difference from competitors.** Per the audit, competitor visuals are unverified recall, so this is a comparison against those notes, not against anything seen: Camel Step is noted as an illustrative camel emblem (this mark has no emblem or illustration); Elixir Bunn as dark, minimal and Latin-prominent (this mark is Arabic-led on warm light grounds); Brew92 as an English-led wordmark with a numeral and neutral palette (this mark is Arabic-led with a counted seven-bar device and a red accent). **Nobody has yet looked at the three competitors' real identities.** If Brew92 uses a strong red, Ember is to be reviewed (open point in the direction).

**Conflict check.** None performed on the mark beyond the naming specialist's name check in `03-strategy/naming.md` (one web search, registers not searched). A row of bars is a generic device; similar marks may exist. **This is not a legal trademark clearance.** "Sidra" is also a coffee variety name, which counsel should consider before filing.

## 6. Self-check against `quality-control/brand-checklist.md`

| Item | Result |
|---|---|
| Approved strategy reflected in brand-context | Pass |
| Each element traceable to strategy | Pass (seven bars = weekly promise; Arabic-led = "rooted and Arabic-led"; plain grid and facts = "plain-spoken") |
| Distinct from every competitor | **Not verifiable**: competitor visuals unverified |
| Primary, secondary, icon exist | Pass |
| Arabic, Latin, bilingual balanced | Pass by eye; no native reviewer |
| One colour, black, reversed | Pass, with the lit-bar caveat |
| Legible at 16 px and 10 mm | **Partial**: only with the documented fallbacks; bilingual not usable at 16 px or 10 mm |
| Clear space and minimum size defined | Pass |
| Vector artwork clean, text outlined | Pass (paths and rects only, XML validated); curves are the font's own, not hand-optimised |
| Preliminary conflict check; trademark notice | **Partial**: name only; mark not searched |
| HEX, RGB, CMYK, Pantone for every colour | **Partial**: CMYK approximate, Pantone "to be matched by printer" |
| Text pairs meet AA | Pass |
| Colour-blindness check | Done; one weak pair reported |
| Palette proportions | Pass |
| Typefaces paired, licensed, hierarchy, fallbacks | Pass (static Latin files still to be obtained, see licences) |
| Graphic elements, iconography, imagery defined | Pass (iconography = none, by direction) |
| At least five applications | **Fail by scope**: two built (test scope set by the Creative Director) |
| Misuse examples | Pass (8 drawn, 5 written) |
| Guidelines follow outline and level | **Partial**: 6-page mini, below the "essential" level; sections 10 and 11 are one line each |
| No spelling errors | Not confirmed: Arabic not proofread by a native reader |
| Colour values match files | Pass |

## 7. Decisions needed and deviations

1. **Wordmark is outlined Plex Bold with custom spacing, not a redrawn custom wordmark.** Recommendation: accept for the system test; commission real letterform refinement (flatter terminals, tighter ة) before any real use.
2. **Bars on Ember.** The direction says both "six bars in Paper on Ember, lit bar Paper" (all seven Paper, lit bar invisible) and "1 kg bag in Ember with an Ink band". I resolved it as **Ink bars with a Paper lit bar on Ember**. Needs the art-director's confirmation.
3. **One-colour versions cannot show the lit bar.** The direction forbids outlines and tints, so v01 uses seven solid bars. Recommendation: accept, and restrict one-colour use to stamps, embossing and single-colour print.
4. **Phone number.** The direction says the placeholder number appears nowhere; the task brief for this build asked for it to be shown as a clearly marked placeholder. The business card shows it in a dashed box labelled as a placeholder. The card is therefore **not client-ready** until the real number arrives or the field is removed.
5. **Business card carries no personal name or title**, because no team names were supplied.
6. **Label size 100 × 170 mm** is my assumption; no bag dieline exists.
7. **Latin line reads "SIDRA COFFEE"** as the direction specifies, although naming.md warns that "Sidra coffee" reads as a variety in English. "SIDRA ROASTERY" would avoid this in the logo itself; raised for a decision, not changed.

## 8. Proposed text for `brand-context.md` section 5 (not yet written there)

```markdown
## 5. Visual identity (approved: <date on approval>)

- **Creative direction (one sentence):** Weekly Beat — a seven-part system with the centre part lit in Ember; see `04-identity/01-direction/creative-direction.md`
- **Logo files and usage:** `04-identity/02-logo/` (outlined SVG). Primary = Arabic wordmark سدرة over the seven-bar rule row; bilingual adds SIDRA COFFEE; Latin-led for English-only; icon = seven bars in a square. Clear space = height of the letter د (0.27 × logo width). Seven bars from 32 px high / 10 mm wide (bilingual 48 px / 18 mm); below that the `-small` version (solid rule, centre seventh lit) down to 16 px / 6 mm; below that the wordmark alone. Print minimums to be confirmed on a proof.
- **Colours:**

| Name | HEX | RGB | CMYK | Pantone | Use |
|---|---|---|---|---|---|
| Paper — ورق | #F3ECE0 | 243 236 224 | 4 6 12 0 (approx.) | to be matched by printer | Default background, about 45% |
| Crema — كريما | #E3C9A0 | 227 201 160 | 10 20 40 0 (approx.) | to be matched by printer | Warm second ground, about 25% |
| Ink — حبر | #1F1B18 | 31 27 24 | 60 60 60 85 (approx.); text 0 0 0 100 | to be matched by printer | Text, unlit bars, rules, about 15% |
| Ember — جمر | #C23A20 | 194 58 32 | 15 90 100 5 (approx.) | to be matched by printer | Lit bar; one field or headline per layout; 1 kg bag, about 10% |
| Ash — رماد | #6F6861 | 111 104 97 | 50 47 50 20 (approx.) | to be matched by printer | Captions on Paper only, about 5% |

- **Typefaces:** Arabic — IBM Plex Sans Arabic; Latin — IBM Plex Sans (both SIL OFL 1.1); Arabic set 15–20% larger than adjacent Latin; scale 0.65 / 1 / 1.6 / 5; licences in `04-identity/licences.md`
- **Imagery and graphic style:** flat colour, 2 px Ink hairlines, the seven-bar row (rule 2:1, band 1:2 to 1:4, gap 1/5 bar, fourth bar lit), seven-column grid. No icons or illustration. Photography of beans, bags and equipment only, flat and frontal on Paper or Crema.
- **Do not:** move the lit bar, light two, change the count or label bars with days; use green, gradients, tints, shadows or rounded corners; set body text in Ember; put Ash or Ember text on Crema; track Arabic; show people or hands; place "Sidra" / «سدرة» beside an origin or variety word; place the bar row beside a barcode.
```
