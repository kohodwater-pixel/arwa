# Handoff notes — Sidra Coffee wholesale landing page (Arabic RTL)

> **SYSTEM TEST — FICTIONAL CLIENT.** Prototype v02, 2026-11-13. Not client-ready: the Arabic copy has not been proofread by a native reader.
> Previous version: `_archive/v01/` (failed quality review r2, issues N1 and N7).

## What changed in v02

| Review issue | Change |
|---|---|
| N1 sample offer | Removed everywhere (ruling j). Header button «استفسر عن التوريد», hero button «استفسر عن التوريد بالجملة», contact heading «اسألنا عن التوريد لمقهاك.», submit «أرسل الاستفسار», success «وصلنا استفسارك.». The radio group is gone (one purpose, no choice to make). The optional phone field is gone: email is the only contact channel. |
| N7 fonts | Static files only, copied into `assets/fonts/` and referenced relatively. No variable font, no `font-stretch`. Step figures are IBM Plex Sans Light 300 at regular width. `font-synthesis: none`. |
| N7 Ember | Ember is used for the lit bar and one button per screenful (ruling l): the hero action, then the form's submit. The header button is Ink outline. Error edges and the error summary are now Ink, not Ember. |
| N7 display size | Arabic display is 115 px at 1440 (token value). The content width grew from 1152 to 1312 px so the headline holds inside the four-column span. |
| Favicon | Icon v02 (`…_logo_icon-colour_ar-en_v02.svg`). |
| Copy | Two offer lines trimmed to the brief's wording (barista courses; monthly delivery to homes). |

## Files

| File | What it is |
|---|---|
| `index.html` | Page markup, `lang="ar" dir="rtl"`, plus a small inline script for the form states |
| `styles.css` | All styles; tokens as CSS variables in `:root`; logical properties only |
| `assets/` | Three approved logo SVGs copied from `04-identity/02-logo/` (primary colour, primary reversed, icon v02) |
| `assets/fonts/` | IBM Plex Sans Arabic 400/500/600/700 and IBM Plex Sans 300/400/500/600/700, static TTF, with both OFL licence texts |
| `ux-brief.md` | UX brief v02 |
| `_work/` | Verification script, its JSON result and six screenshots (v02) |
| `_archive/` | v01, with a README giving the reason |

The folder is self-contained: copy it anywhere and open `index.html`. For production, subset the fonts to WOFF2.

## Tokens (from `04-identity/03-system/tokens.json` v02)

| Group | CSS variables | Values |
|---|---|---|
| Colour | `--paper --crema --ink --ember --ash` | #F3ECE0, #E3C9A0, #1F1B18, #C23A20, #6F6861 |
| Type family | `--font` | IBM Plex Sans (Latin, figures), then IBM Plex Sans Arabic, then system fallbacks |
| Type size (Arabic) | `--fs-caption --fs-body --fs-sub --fs-display` | 15 px; 18 → 23 px; 28 → 37 px; 44–80 px → 80–115 px (115 at 1440) |
| Line height | `--lh-display --lh-sub --lh-body --lh-caption` | 1.3, 1.5, 1.75, 1.6 |
| Space | `--s1` … `--s7` | 4, 8, 16, 24, 40, 64, 104 px |
| Grid | `--gap7`, `--page-max`, `--page-pad` | seven columns, gutter 1/5 column; 1312 px content; 24 → 64 px side padding |
| Rules | `--hairline`, radius, shadow | 2 px Ink; 0; none |
| Targets | `--target` | 44 px minimum; buttons and inputs 52 px |

Letter-spacing is 0 everywhere. No uppercase, no faux bold or italic.

## Contrast of the pairs used (values from `system.md` section 2)

| Pair | Ratio | Where |
|---|---|---|
| Ink on Paper | 14.56:1 | Body, headings, inputs, outline button, error text and edges |
| Ink on Crema | 10.69:1 | "How it works" section |
| Paper on Ink | 14.56:1 | Footer, success panel, button hover and loading |
| Paper on Ember | 4.56:1 | Primary button label (18–23 px, weight 600). Passes AA by a narrow margin |
| Ash on Paper | 4.67:1 | Captions and hints, 15 px, on Paper only |
| Ember against Paper / Crema / Ink | 4.56 / 3.35 / 3.19:1 | Lit bar only (non-text, needs 3:1) |

## Components and states

| Component | States |
|---|---|
| Button, primary (Ember) | default, hover (Ink), focus (3 px Ink ring, 3 px offset), loading (`aria-disabled`, Ink, label «جارٍ الإرسال…») |
| Button, outline (Ink) / small (header) / on Ink (Paper outline) | default, hover (inverts), focus |
| Text link | default (underlined), focus |
| Seven-bar row | `bars--rule` 2:1, `bars--band` 1:2 (1:2.6 in the desktop hero pattern, as in icon v02). Always seven, fourth lit, forced LTR, never labelled |
| Hero pattern | one band row on mobile; three stacked rows from 1040 px |
| Step (figure, title, text) | static |
| Offer row (name, description) | stacked on mobile; 3 + 4 columns from 720 px |
| Text field, email, textarea | empty, filled, focus, error (message with «خطأ:», 8 px Ink edge on the right, `aria-invalid`), optional hint |
| Error summary | hidden; visible with links that move focus to each field (`role="alert"`) |
| Success panel | replaces the form; heading takes focus; «أرسل استفسارًا آخر» resets to the empty form |
| Header, footer, skip link | nav links hidden below 1040 px (logo and enquiry button remain) |

## Form behaviour

- No `action`; the script calls `preventDefault()` and makes no network request. The loading state is a 700 ms simulation.
- Required: name, café name, valid email. Optional: what the café needs.
- On error the summary appears and takes focus; errors clear as fields are corrected.
- The success panel carries a visible prototype note (`data-prototype-note`). Remove it when a real endpoint exists.
- To build: endpoint, spam protection, privacy notice and consent wording, real loading and server-error states.

## Breakpoints

| Width | Change |
|---|---|
| Base (from 320 px) | Single column, 24 px padding, display 12.5vw (44–80 px) |
| 720 px | Name and café fields side by side; offer rows on the seven-column grid |
| 1040 px | Seven-column layouts (hero 4 + 3, contact 4 + 2), nav links shown, body 23 px, 64 px padding, 104 px section spacing, display 8vw (80–115 px) |
| 1440 px and up | Display 115 px; content capped at 1312 px |

## RTL

Logical properties and grid order throughout, so start = right. Not mirrored: logo, bar rows, the email address and the email input (`dir="ltr"`, aligned to the right edge). No directional icons.

## Verification (Chromium via Playwright, `_work/verify_v02.cjs`, result in `_work/verify_v02_result.json`)

At 390 and 1440 px: no horizontal overflow in default, error and success states; all nine font faces report `loaded`; every request stays inside this folder; no interactive target under 44 px; Ember found only on bars and the two primary buttons (never in the same screenful); no "sample" wording in the page; empty submit shows three errors, a bad email shows one, a valid submit shows loading then success, reset returns the empty form; 0 network requests across all submits; no console errors. The two default screenshots, the mobile error state and the desktop success state were opened and checked by eye after the last CSS change.

## Deviations and open points (for the Creative Director)

1. **Mobile type is scaled down** (body 18 px, sub-head 28 px, display about 49 px at 390), keeping the ladder's order but not its exact ratios. Between 1040 and 1439 px the display scales from 80 to 115 px.
2. **Favicon uses icon v02 as instructed.** The size ladder in `system.md` says the barred icon holds from 48 px and `icon-small` is for 16 to 47 px, so in a 16 px browser tab the bars will merge. Not checked in a real tab (headless Chromium does not request the favicon).
3. **Latin and figures inside Arabic lines are set at the Arabic size**, not 1/1.15 smaller.
4. **Reply by email** («ونردّ عليك على بريدك») is an assumption; see `ux-brief.md`.

## Not done

- English LTR version, tablet screenshots, real-device and screen-reader testing.
- Native Arabic proofread.
