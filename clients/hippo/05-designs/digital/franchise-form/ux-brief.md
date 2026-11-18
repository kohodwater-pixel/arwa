# HIPPO — franchise enquiry form: UX brief and design notes (v01, 2026-11-18)

## 1. Reference study — not seen
The client's reference is `https://bart-cafe.com/franchise` ("a form like this as the franchise link").

- **It could not be opened.** `scripts/site_capture.cjs` returned `net::ERR_TUNNEL_CONNECTION_FAILED`; WebFetch returned `ENOTFOUND` (host outside the session's allowed network domains). One attempt each, no retries. `_work/reference/capture.json` holds only that error record; no screenshot exists.
- So **nothing here describes that page**: its sections, fields, steps and submit behaviour are unknown to us. Nothing was taken from it.
- **Assumption used instead:** ordinary franchise-enquiry practice — a short single-step form asking who the applicant is, how to reach them, where they want to open, whether they have a site, their background, and consent. To compare against the reference, the host must be allowed in the session's network settings, or the client can send screenshots.

## 2. Users, goal, tasks
- **Users (assumption, no approved strategy):** prospective franchisees who have just watched the ad and scanned its QR, on a phone, Arabic first; some on desktop from a shared link.
- **Single goal:** a completed enquiry the HIPPO team can follow up.
- **Tasks:** recognise this is the ad's destination; fill the form quickly with one thumb; know for certain whether it was sent.
- **Success measures (to agree):** completion rate from page open; share of enquiries with a valid mobile number.

## 3. Structure (one page, one step)
1. Masthead — the ad's end card continued: logo file, «امتياز هيبو التجاري», *Franchise*, language switch.
2. Stage — pink wall, purple floor, level horizon (the horizon levels at the ad's call to action); one photograph (hero sandwich); the lime spot carrying «حُطّ ثقلك.»; one sentence built from the approved scene-7 line.
3. Form sheet (white, on the floor).
4. Confirmation, replacing the form. 5. Footer with the logo.

## 4. Fields
| Field | Type | Required | Note |
|---|---|---|---|
| Full name | text | yes | |
| Mobile | tel, numeric keypad | yes | Saudi format hint; accepts international, spaces, dashes, Arabic-Indic digits |
| Email | email | no | assumption: phone is the main channel |
| City or region | free text | yes | no market list offered |
| Has a site | 3 radios | yes | yes / looking / not decided |
| Experience | short textarea | no | |
| How they heard | select | no | no option implies a fact not confirmed |
| Message | textarea | no | |
| Consent | checkbox | yes | privacy link is a marked gap until supplied |
| Honeypot | hidden text | — | spam trap |

Left out on purpose: investment capacity (its ranges would be invented figures), any list of markets, timelines, fees.

## 5. States
Empty; field error (on leaving a field and on submit, message under the field, focus to the first error, summary above the button); sending (button disabled, "sending"); sent; send failed (answers kept); WhatsApp handoff; **draft** (nothing connected — strip at the top plus a confirmation that says nothing was sent).

## 6. Tokens
- Colour (brand sheet, unchanged): lime `#BBD032`, black `#181717`, pink `#DA6FA2`, app pink `#E75A9E`, purple `#7B5FC2`, app lime `#B8E23A` (unused), white.
- Contrast pairs used: black on white; black on lime; white on purple 4.9:1; white on black; lime on black. Error marking is black bold text with an app-pink badge and a 3 px app-pink border (3.3:1 against white as a UI boundary) — no new colour introduced. Text is never pink.
- Type: Tajawal 400/500/700/800 for Arabic and for English body text (assumption: the brand sheet names a Latin face for headlines only); Playfair Display Italic for English headlines and support lines, as in the ad (only the italic file is in the client folder). Arabic line height 1.7–1.75, no letter-spacing anywhere.
- Shape: fields 54 px high, 2 px black border, 14 px radius; sheet radius 28 px; pill buttons 60 px; focus ring white + purple, 3 px each.
- Breakpoints: mobile base; 760 px and up widens the stage, sheet (max 720 px) and puts the three radios in a row; below 22.4 rem (or with heavily enlarged text) the language switch takes its own row.
- Motion: the sandwich lands once and the spot settles (about 1 s), off under `prefers-reduced-motion`.
- Numerals: Western (assumption — not yet recorded in `brand-context.md`).

## 7. Components
Draft strip, masthead, language switch, stage (wall, floor, spot), text input, textarea, select, radio row, checkbox, hint, field error, form alert, primary button, secondary button, confirmation panel, marked "to supply" gap, footer.
