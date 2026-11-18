# HIPPO — franchise enquiry form: UX brief and design notes (v02, 2026-11-18)

## 1. Reference study
The client's reference is `https://bart-cafe.com/franchise` ("a form like this as the franchise link").

- **Not opened by this agent.** The host is outside the session's allowed network domains (`site_capture.cjs`: `ERR_TUNNEL_CONNECTION_FAILED`; WebFetch: `ENOTFOUND`; one attempt each). `_work/reference/capture.json` holds only that error record.
- **Structure as seen by the Creative Director on 2026-11-18** and passed on in writing (this agent did not see the page): a two-step franchise application form with a language switch and a thank-you state; back and submit buttons; submit stores a row in a hosted database.
- Nothing of the reference is copied: labels, layout, colours and code are ours. Only the kind of form and the kind of question are shared.

| Reference has (per the Creative Director) | Ours (v02) | Decision |
|---|---|---|
| Two steps, back / submit | Two steps with a "Step 1 of 2" indicator, next / back / send | Same kind |
| Language switch | Arabic and English pages with a switch | Same kind |
| Thank-you state | Confirmation; plus sending, failed, WhatsApp and draft states | Same kind, more states |
| Full name* | Full name* | Kept |
| Profession* | Profession* | Kept |
| Age* (number) | Age* (number, 18 or older) | Kept; minimum set by the Creative Director |
| Company name | Company name (optional) | Kept |
| Company website | Company website (optional) | Kept |
| Mobile* | Mobile* (Saudi hint, international accepted) | Kept |
| Email* | Email* | Kept; now required |
| Restaurant / café experience* — six choices, "other" reveals a required text field | Same six kinds of answer in our wording; "other" reveals a required field | Kept |
| The applicant's own brand name | Own brand name (optional) | Kept |
| How many branches they run (number) | Branches currently run (optional number) | Kept |
| Why this franchise* (long text) | Why the HIPPO franchise* | Kept |
| Interested in opening* — one / two to five / five to ten / other | Same four answers, in words | Kept; allowed as a neutral answer option |
| Source of investment* — savings / investors / bank / other | Same four kinds of answer | Kept |
| Investment amount* (free number) | Amount the applicant plans to invest*, free number, SAR label; no ranges, minimum or hint amounts | Kept; the figure is the applicant's, not HIPPO's |
| When they expect to start* — four options | Same four options | Kept |
| Expected capital payback period* (number) | — | **Left out** by Creative Director ruling: it invites a return expectation HIPPO has not stated. Client decision, listed in the README |
| Target cities* (free text) | Target cities* (free text) | Kept; no market list |
| Notes | Notes (optional) | Kept |
| — | Do you have a site (optional) | Ours, kept from v01 |
| — | How they heard (optional) | Ours, kept from v01 |
| — | Consent* and a marked privacy-notice gap | Ours |
| — | Hidden spam-trap field | Ours |
| Stores a row in a hosted database | Google Sheet through an Apps Script web app (client decision); endpoint is one config value | Client decision 2026-11-18 |

**No-figures rule, as ruled by the Creative Director:** it forbids figures and claims about HIPPO (fees, returns, branch counts, required capital). Questions the applicant answers, and neutral options such as "two to five branches" or "in 3 to 6 months", are allowed.

## 2. Users, goal, tasks
- **Users (assumption, no approved strategy):** prospective franchisees who have just watched the ad and scanned its QR, on a phone, Arabic first; some on desktop from a shared link.
- **Single goal:** a completed enquiry the HIPPO team can follow up.
- **Tasks:** recognise this is the ad's destination; fill the form quickly with one thumb; know for certain whether it was sent.
- **Success measures (to agree):** completion rate from page open; share of enquiries with a valid mobile number.

## 3. Structure (one page, two steps)
1. Masthead — the ad's end card continued: logo file, «امتياز هيبو التجاري», *Franchise*, language switch.
2. Stage — pink wall, purple floor, level horizon; one photograph (hero sandwich); the lime spot carrying «حُطّ ثقلك.»; one sentence built from the approved scene-7 line.
3. Form sheet (white, on the floor): step indicator, step 1 "About you", step 2 "Your plans".
4. Confirmation, replacing the form. 5. Footer with the logo.

## 4. Fields and behaviour
Fields are listed in the table in section 1. Behaviour:
- Step 1 is checked on "Next" (and on Enter); step 2 on "Send". Errors appear under each field in the page language, focus moves to the first one, and a summary sits above the buttons.
- Answers are kept when going back and forward, and when returning from the draft confirmation.
- Single-choice questions are pill-shaped radio buttons with a visible dot, so selection never depends on colour alone.
- Numbers typed in Arabic-Indic digits are accepted and stored as Western digits; thousands separators in the amount are removed.
- Payload keys: `form, lang, full_name, profession, age, company_name, company_website, mobile, email, experience, experience_other, own_brand, branches_operated, why_hippo, branches_wanted, branches_wanted_other, investment_source, investment_source_other, investment_amount, investment_currency, start_time, target_cities, has_location, heard_from, notes, consent, submitted_at`.

## 5. States
Empty; step 1; step 2; field error (on leaving a field and on next / send); sending (button disabled, "sending"); sent; send failed (answers kept); WhatsApp handoff; **draft** (nothing connected — strip at the top plus a confirmation that says nothing was sent).

## 6. Tokens
- Colour (brand sheet, unchanged): lime `#BBD032`, black `#181717`, pink `#DA6FA2`, app pink `#E75A9E`, purple `#7B5FC2`, app lime `#B8E23A` (unused), white.
- Contrast pairs used: black on white; black on lime; white on purple 4.9:1; white on black; lime on black. Error marking is black bold text with an app-pink badge and a 3 px app-pink border (3.3:1 against white as a UI boundary) — no new colour introduced. Text is never pink.
- Type: Tajawal 400/500/700/800 for Arabic and for English body text (assumption: the brand sheet names a Latin face for headlines only); Playfair Display Italic for English headlines and support lines, as in the ad (only the italic file is in the client folder). Arabic line height 1.7–1.75, no letter-spacing anywhere.
- Shape: fields 54 px high, 2 px black border, 14 px radius; radio pills 50 px high; sheet radius 28 px; pill buttons 60 px; focus ring white + purple, 3 px each.
- Breakpoints: mobile base; 760 px and up widens the stage and sheet (max 720 px); radio pills wrap naturally at every width; below 22.4 rem (or with heavily enlarged text) the language switch takes its own row.
- Motion: the sandwich lands once and the spot settles (about 1 s), off under `prefers-reduced-motion`.
- Numerals: Western (assumption — not yet recorded in `brand-context.md`).

## 7. Components
Draft strip, masthead, language switch, stage (wall, floor, spot), step indicator, text input, short numeric input, amount input with currency, textarea, select, radio pill, revealed "other" field, checkbox, hint, field error, form alert, primary button, secondary button, confirmation panel, marked "to supply" gap, footer.
