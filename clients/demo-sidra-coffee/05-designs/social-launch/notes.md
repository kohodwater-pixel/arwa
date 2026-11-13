# Social launch — notes

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS. Identity v01 is accepted for the system test only; nothing here is client-ready.

**Date:** 2026-11-13  **Prepared by:** Graphic Designer  **Status:** v01, for Creative Director and quality review

## 1. What was made

| File | What it is |
|---|---|
| `demo-sidra-coffee_instagram-post_wholesale_ar_v01.png` | Instagram feed post, 1080 × 1350 px, RGB, Arabic |
| `demo-sidra-coffee_instagram-post_wholesale_ar_v01.html` | Editable source (links `04-identity/03-system/brand.css` and the primary logo SVG) |
| `_work/render.cjs` | Render script: `node _work/render.cjs <html> <png>` (Playwright Chromium, 1080 × 1350 viewport, scale 1) |

**Brief.** Objective: introduce the weekly roast-to-order promise to wholesale buyers. Audience: independent café owners in Riyadh. One message: the tagline. Call to action: send a direct message. Language: Arabic only.

## 2. Copy used

| Role | Text | Source |
|---|---|---|
| Headline | «تُحمَّص لطلبك، كل أسبوع.» set without the quotation marks, with its diacritics | Tagline option 1, `03-strategy/messaging.md`; wholesale use approved in the decision log |
| Sub-head | محمصة من الرياض، لمقاهي الرياض. | Key message "Local supplier" [V], `messaging.md` |
| Call to action | لطلبات المقاهي بالجملة، راسلنا على الخاص. | **Written by me, not in the approved messaging.** See assumptions |
| Logo | Primary Arabic lockup, colour version, 168 px wide (97 px high) | `04-identity/02-logo/demo-sidra-coffee_logo_primary-colour_ar_v01.svg` |

No prices, offers, numbers, roast or delivery days, client names, phone number or web address appear.

## 3. System used

- Grid: seven columns, margin 80 px, content 920 px, column 112.2 px, gutter 22.4 px. Sub-head on 4 columns from the right, call to action on 3 from the left. The headline spans all seven columns (see deviations).
- Type: IBM Plex Sans Arabic only. Headline Bold 132 px / 1.3; sub-head Medium 42 px / 1.5; call to action Regular 27 px / 1.75. No tracking, no Latin text.
- Colour: Paper ground, Crema lower panel, Ink text and six bars, Ember only on the lit bar (and in the logo's own lit bar). All text is Ink on Paper (14.56:1).
- Seven-bar device: band proportion, bars 112 × 406 px (1:3.6), gap 22.4 px (1/5 bar), fourth bar lit in Ember, on Crema, running off the bottom edge.
- 2 px Ink hairline as the section break. Square corners, no shadows, no imagery, no people.

## 4. Checks done

- PNG opened and viewed after the final render: 1080 × 1350, Arabic letters connected and in the right order, diacritics on تُحمَّص clear of the logo and not clipped, Arabic comma used.
- Fonts reported as loaded by the browser: IBM Plex Sans Arabic 400, 500, 700; none failed, so no fallback font was used.
- Self-check against `quality-control/design-checklist.md`: passes brief, brand, layout, Arabic and screen items, except the open points below.

## 5. Deviations and assumptions

1. **Headline width.** The direction puts Arabic text on 4 columns from the right. At display size the tagline does not fit 4 columns, so the headline spans all seven; the supporting text keeps the 4 + 3 split.
2. **Headline size 132 px**, above the 115 px screen step in `system.md`, scaled for a 1080 px canvas read on a phone. Sub-head and body are scaled in proportion (ratios about 5 : 1.6 : 1).
3. **Call to action is my wording** and assumes the brand takes wholesale enquiries by Instagram direct message. No website, handle or usable phone number exists in `brand-context.md`. To be confirmed or replaced.
4. **Bars run off the bottom edge** of the canvas. The direction does not forbid cropping the band at an edge, but does not show it either. Needs the art-director's nod.
5. **Ember appears only on the lit bar**, with no Ember field or headline, which the direction allows but does not require.
6. Arabic copy has **not been proofread by a native reader**.
7. The PNG is untagged RGB (Chromium output, sRGB values, no embedded ICC profile).
8. Instagram crops feed posts to 3:4 on the profile grid; the edges of the logo and bars sit inside that crop by calculation only, not tested on a device.

## 6. Canva test (one pass, 2026-11-13)

| Call | Result |
|---|---|
| `read-design` on `DAHavyXC4eY` with metadata, content and thumbnail | **Succeeded.** Title «منشور سدرة للقهوة», 1 page, 1080 × 1440 px. Edit: https://www.canva.com/d/_ym6s9v1IClXumz · View: https://www.canva.com/d/9UqaFx63dOydVAy. Thumbnail viewed |
| `list-brand-kits` | **Succeeded, returned no Brand Kits** (`items: []`). Compliance was therefore checked by eye against the identity files |
| `resize-design` to custom 1080 × 1920 | **Succeeded.** New design `DAHawovd8j0`. Edit: https://www.canva.com/d/Xv-Skiqd502L1eZ · View: https://www.canva.com/d/GdvalOW1ROp2CHP. The response says 1 trial use of resize remains on this account |
| `read-design` on `DAHawovd8j0` (page metadata and thumbnail), to verify the resize | **Succeeded.** 1080 × 1920 confirmed, thumbnail viewed |

The original design was not edited or deleted. The resized copy is a new, equally off-brand design; it was not edited. Its URL is not yet recorded in `brand-context.md`.

Note: `brand-context.md` lists the Canva design as https://www.canva.com/d/cAgvdNFdbYXi3EZ, which is not either URL returned by `read-design` today. I did not open that link, so I cannot say whether it points to the same design.

### Brand-compliance note on the existing Canva design (`DAHavyXC4eY`)

Judged from the text content and a 387 × 516 px thumbnail, so fine details (exact colours, typeface) are estimates.

| Point | Approved identity | Canva design | Verdict |
|---|---|---|---|
| Size | 1080 × 1350 for a feed post | 1080 × 1440 | Fail |
| Logo | Primary lockup: سدرة wordmark over the seven-bar row | No logo; «سدرة للقهوة» typed as small text | Fail |
| Seven-bar device | Seven bars, fourth lit | Absent | Fail |
| Graphic language | Flat colour, hairlines, square corners; no gradients, no ornament, no bean imagery as illustration | Curved organic shapes, a soft gradient panel, a thin curved line, a rendered coffee-bean image with shadow | Fail |
| Colour | Paper, Crema, Ink, Ember, Ash only; no tints or gradients | A cream ground, a tan gradient and a terracotta shape: close in mood, but not the specified values as far as the thumbnail shows, and tinted | Fail (values unverified) |
| Typeface | IBM Plex Sans Arabic | A geometric Arabic sans that does not look like Plex | Likely fail (not confirmed from the thumbnail) |
| Headline | Tagline «تُحمَّص لطلبك، كل أسبوع.» for wholesale | «محمّصة طازجة كل أسبوع» and «قهوة مختصة تُحمَّص عند الطلب» | Not the approved tagline. The facts stated (weekly, roasted to order, specialty) are verified ones, and the words are in the approved vocabulary |
| Grid | Seven columns, 4 + 3 split | Centred and free-form | Fail |
| Arabic shaping | Connected, correct order | Connected and correct in the thumbnail | Pass |
| People, offers, numbers | None | None | Pass |

**Conclusion:** the Canva design is off-brand and should not be used or resized for publication. Bringing it on brand would mean replacing almost every element, so rebuilding from the HTML source, or uploading the approved PNG and logo to Canva, is the more sensible route. With no Brand Kit on the account, any Canva output has to be checked by hand against `brand-context.md`.
