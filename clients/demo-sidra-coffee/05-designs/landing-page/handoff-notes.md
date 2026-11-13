# Handoff notes — Sidra Coffee wholesale landing page (Arabic RTL)

> **SYSTEM TEST — FICTIONAL CLIENT.** Prototype v01, 2026-11-13. Not client-ready: Arabic copy has not been proofread by a native reader.

## Files

| File | What it is |
|---|---|
| `index.html` | Page markup, `lang="ar" dir="rtl"`, plus a small inline script for the form states |
| `styles.css` | All styles; tokens as CSS variables in `:root`; logical properties only |
| `assets/` | Copies of three approved logo SVGs from `04-identity/02-logo/` (primary colour, primary reversed, icon-small as favicon) |
| `_work/` | Verification screenshots (390 and 1440 px; default, form error, form success) |

Open `index.html` from its place in the repo: fonts load from `../../../../assets/fonts/` (IBM Plex Sans Arabic static 400/500/600/700; IBM Plex Sans variable). For production, subset to WOFF2 and host the fonts with the site.

## Tokens (from `04-identity/03-system/tokens.json`)

| Group | CSS variables | Values |
|---|---|---|
| Colour | `--paper --crema --ink --ember --ash` | #F3ECE0, #E3C9A0, #1F1B18, #C23A20, #6F6861 |
| Type family | `--font` | IBM Plex Sans (Latin, figures) then IBM Plex Sans Arabic, then system fallbacks |
| Type size | `--fs-caption --fs-body --fs-sub --fs-display` | 15 px; 18 → 23 px; 28 → 37 px; 44–80 → 100 px |
| Line height | `--lh-display --lh-sub --lh-body --lh-caption` | 1.3, 1.5, 1.75, 1.6 |
| Space | `--s1` … `--s7` | 4, 8, 16, 24, 40, 64, 104 px |
| Grid | `--gap7`, `--page-max`, `--page-pad` | seven columns, gutter 1/5 column; 1152 px content; 24 → 64 px side padding |
| Rules | `--hairline`, radius, shadow | 2 px Ink; 0; none |
| Targets | `--target` | 44 px minimum; buttons and inputs 52 px |

Letter-spacing is 0 everywhere. No uppercase, no faux bold or italic.

## Contrast of the pairs used (WCAG 2.x, recomputed in the verification script)

| Pair | Ratio | Where |
|---|---|---|
| Ink on Paper | 14.56:1 | Body, headings, inputs, outline button |
| Ink on Crema | 10.69:1 | "How it works" section |
| Paper on Ink | 14.56:1 | Footer, success panel, button hover |
| Paper on Ember | 4.56:1 | Primary button label (18–23 px, weight 600). Passes AA by a narrow margin |
| Ash on Paper | 4.67:1 | Captions and hints, 15 px, on Paper only |
| Ember against Paper | 4.56:1 | Error borders, lit bar (non-text, needs 3:1) |
| Ember against Crema | 3.35:1 | Lit bar only (non-text) |
| Ember against Ink | 3.19:1 | Lit bar in the success panel and footer logo (non-text) |

Ember is never used for text. Errors are Ink text with a "خطأ:" prefix and a thick Ember edge, so they do not rely on colour.

## Components and states

| Component | States |
|---|---|
| Button, primary (Ember) | default, hover (Ink), focus (3 px Ink ring, 3 px offset), loading (`aria-disabled`, label "جارٍ الإرسال…") |
| Button, outline (Ink) / small (header) / on Ink (Paper outline) | default, hover (inverts), focus |
| Text link | default (underlined), focus |
| Seven-bar row | `bars--rule` 2:1, `bars--band` 1:2 (1:2.4 in the desktop hero pattern), on-Ink variant. Always seven bars, fourth lit, forced LTR, never labelled |
| Hero pattern | one band row on mobile; three stacked rows from 1040 px |
| Step (number, title, text) | static |
| Offer row (name, description) | stacked on mobile; 3 + 4 columns from 720 px |
| Text field, email, phone, textarea | empty, filled, focus, error (message + Ember edge + `aria-invalid`), with optional hint |
| Radio group | unselected, selected, focus, error |
| Error summary | hidden; visible with links that move focus to each field (`role="alert"`) |
| Success panel | replaces the form; heading takes focus; "send another" resets |
| Header, footer, skip link | header nav links hidden below 1040 px (logo and CTA remain) |

## Form behaviour

- The form has no `action`; the script calls `preventDefault()` and makes no network request (checked: 0 requests after submit). The loading state is a 700 ms simulation.
- Required: name, café name, valid email, one choice. Optional: mobile number, notes.
- On error: summary appears and takes focus; errors clear as fields are corrected.
- The success panel carries a visible prototype note (`data-prototype-note`). Remove it when a real endpoint exists.
- To build: endpoint, spam protection, privacy notice and consent wording, real loading and server-error state.

## Breakpoints

| Width | Change |
|---|---|
| Base (from 320 px) | Single column, 24 px padding, display type 12.5vw (44–80 px) |
| 720 px | Form fields in two columns; offer rows on the seven-column grid |
| 1040 px | Seven-column layouts (hero 4 + 3, contact 4 + 2), nav links shown, body 23 px, 64 px padding, 104 px section spacing |
| 1280 px | Display headline 100 px |

## RTL

All layout uses logical properties and grid order, so start = right. Not mirrored: logo, bar rows, email address and Latin inputs (`dir="ltr"`, aligned to the right edge). There are no directional icons.

## Deviations from the identity system (for the Creative Director)

1. **Display size is 100 px, not 115 px**, at desktop: at 115 px the first headline line overran the four-column span and touched the bars.
2. **Mobile type is scaled down** (body 18 px, sub-head 28 px), keeping the ladder's order but not its exact ratios.
3. **Ember appears on the hero CTA and the submit button**, plus the lit bars and error edges. The system says "once per layout"; I read a long scrolling page as one Ember action per screenful. The header CTA is Ink outline for that reason.
4. Radio buttons are native round controls (square ones read as checkboxes).

## Not done

- English LTR version, tablet screenshots, real-device and screen-reader testing.
- Native Arabic proofread.
