# UX brief — Sidra Coffee wholesale landing page

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v02  **Date:** 2026-11-13  **Prepared by:** UI/UX Designer  **Language:** Arabic (RTL). English version not in this scope.
**Previous version:** `_archive/v01/ux-brief.md`. Changed in v02: the conversion goal. No sample offer exists (decision log 2026-11-13, ruling j), so every "request a sample" element is gone and the page asks for a wholesale enquiry only.

## One conversion goal

An independent café owner in Riyadh sends a **wholesale supply enquiry** through the form (or writes to hello@sidra-coffee.example). Everything on the page leads to that form; there is no second goal (no sample, no shop, no subscription sign-up).

## Users and what they want

| User | Wants to know | Source |
|---|---|---|
| Independent café owner, Riyadh (primary) | Is this a dependable local roaster? How does ordering work? What can I buy? How do I start? | Brief section 5; motives are assumptions (brand-context) |
| Home brewer (secondary, not targeted here) | Sees the subscription in one line only | Brief section 5 |

## Key tasks

1. Understand the offer in one screen: roasted to order, every week, from Riyadh.
2. See how the weekly roast works (three steps, the seven-bar device).
3. Send a wholesale enquiry, or copy the email address.

## Section order

Header (logo, enquiry button in Ink outline) → Hero (promise, value proposition, the Ember action «استفسر عن التوريد بالجملة») → How the weekly roast works → What we offer → Enquiry form «اسألنا عن التوريد لمقهاك.» → Footer.

There is **no proof section** (testimonials, client logos, counts): the brief lists these as not available. Verified facts stand in: Riyadh, founded 2023, weekly roast to order, 250 g and 1 kg.

## Content inventory (all from `01-brief/brief.md` and `03-strategy/messaging.md`)

- Tagline option 1 (approved for wholesale material), value proposition, café-owner key messages marked [V].
- Four products and services from brief section 4, described only in the brief's own terms.
- Contact: hello@sidra-coffee.example; Riyadh, Saudi Arabia. Email is the only contact channel (ruling b): no phone number is shown and the form no longer asks for one.
- Form fields: name, café name, email (required); what the café needs (optional).
- Left out on purpose: samples, roast day, delivery day, minimum order, prices, "no cafés of our own", origins, any customer or award claim.

## Devices and accessibility

Mobile first (390 px), desktop at 1440 px. WCAG AA: contrast, visible focus, 44 px targets, text in rem. Western numerals.

## Success measures (to be set up at build; no baseline exists)

- Enquiry completion rate (enquiries sent / visitors who reach the form).
- Hero action click-through to the form.
- Share of enquiries sent by the form against direct email.

## Assumptions to confirm

- That Sidra replies to enquiries by email (the page says «ونردّ عليك على بريدك»). Email is the only verified channel, but the reply promise itself is not in the brief.
- The motives listed for café owners.
