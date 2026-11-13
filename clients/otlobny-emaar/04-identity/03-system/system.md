# Identity system (captured) — otlobny-emaar

Date: 2026-11-13 · Version v01 · Status: **captured from the client's existing profile; not yet approved by the client**

This is a record of the identity the client already uses, so the new company profile can be built on it. Nothing here is a redesign. The two things that are new, and are proposals for the client, are marked **PROPOSAL**.

Source: `_originals/otlobny_company-profile_original_2026-11-13.pdf` (20 pages, A4 landscape). Machine-readable values: `tokens.json`.

## 1. Logo

Files in `04-identity/02-logo/` (SVG, paths only, no fonts, tight viewBox 307.71 × 124.6):

| File | Use |
|---|---|
| `otlobny-emaar_logo_wordmark-colour_ar_v01.svg` | White and light-tint backgrounds. Blue letters, green accents, as on page 1 |
| `otlobny-emaar_logo_wordmark-reversed_ar_v01.svg` | Navy and the dark half of the gradient. Green letters, white dot and squeegee, as on page 20 |
| `otlobny-emaar_logo_wordmark-white_ar_v01.svg` | One colour, on navy, royal blue, the gradient and photographs |
| `otlobny-emaar_logo_wordmark-navy_ar_v01.svg` | One colour, on white and light backgrounds; stamps, fax, single-colour print |

**PROPOSAL, name lockup** (wordmark plus the new descriptor «شركة اطلبني إعمار» / "OTLOBNY Emaar Co.", viewBox 307.71 × 130.06): `otlobny-emaar_logo_lockup-proposal-{colour,reversed,white,navy}_ar-en_v01.svg`. The name spelling is an assumption until the client confirms it.

What is original and what is not:

- Letterforms, star badge, dot and squeegee are the vector paths of page 20, moved but not redrawn. Checked by eye against 400 dpi renders of pages 1 and 20: `02-logo/_work/compare_original-left_extracted-right.png`.
- The colour split (which parts are blue, which green) is read from page 1, where the logo is a raster; the shapes are the same as on page 20.
- The dot's outline was a stroke in the source and is now two filled circles with the same edges.
- The one-colour versions do not exist in the original. They were derived: the squeegee and dot are kept apart from the letters by a gap of the same width as the source's own ring around the dot.

Descriptor of the proposed lockup:

- Typeface **Tajawal Bold**, outlined. Chosen over Cairo because its low-contrast, squarer geometric construction and flat stroke endings match the heavy geometric wordmark, and its bold weight holds next to the mass of the letters. Cairo (tested at 500 and 600) is narrower and lighter in colour; the line looked thin under the wordmark. Tajawal is also the Arabic typeface recommended for the profile, so the logo line and the document share one face.
- Position follows the old descriptor: right edge aligned to the right edge of the alef, Arabic line on the old baseline with the same alef height (10.54 units), Latin line at the old cap height (7.84 units), tracked +0.13 em so both lines have the same width (133.2 units). Arabic is not tracked.
- One change from the old layout: the Latin line sits 3.1 units lower, because Tajawal carries the two dots of the final ya lower than the old typeface did and they would have touched the Latin capitals.
- Colour: grey `#525456` in the colour version (as on page 1), green in the reversed version (as on page 20), the single colour in the one-colour versions.

Usage (agency recommendations; the original states none):

- Clear space: X = the width of the alef (6.9% of the logo width) on all sides.
- Minimum size, wordmark: 16 px high on screen, 10 mm high in print. At 16 px the star in the badge and the squeegee handle close up but the word stays recognisable (`02-logo/_work/test_small-sizes_16px-and-10mm.png`).
- Minimum size, lockup: 96 px high on screen, 17 mm high in print; below that the descriptor is under 6 pt. Use the wordmark alone at smaller sizes.
- On royal blue use the white version (the reversed green version has only 3.06:1 against royal blue).
- On photographs use the white version over a dark or navy-tinted area.

Do not:

- Do not place the blue wordmark on navy. The mockup images show this; blue on navy is 1.9:1.
- Do not use the all-green wordmark on white. The inner pages of the original do this; green on white is 2.15:1. Use the colour version.
- Do not use the old descriptor, retype the name next to the wordmark in another typeface, redraw, stretch, outline or recolour the mark, or copy the logo from the mockup images (their letterforms and spellings are wrong).

## 2. Colour

Sampled from the original: vector fills on page 20, pixels of pages 1, 6, 10 and 16. sRGB. The source holds no CMYK or Pantone values: **to be matched by the printer** if the profile is printed.

| Name | HEX | RGB | Where it comes from | Use |
|---|---|---|---|---|
| Royal blue | `#3758B0` | 55, 88, 176 | Wordmark on p1; light end of the p20 gradient | Wordmark, headings, large shapes |
| Green | `#5AC584` | 90, 197, 132 | Vector fill on p20; accents on p1 | Accent only |
| Navy | `#1F3162` | 31, 49, 98 | Dark end of the p20 gradient | Dark backgrounds; text on light |
| Light tint | `#F7F8FC` | 247, 248, 252 | Panels on p10, p16 | Backgrounds |
| Periwinkle tint | `#9BABD7` | 155, 171, 215 | Sparkle pattern on p6 | Pattern; secondary text on navy |
| White | `#FFFFFF` | 255, 255, 255 | Page | Background; text on navy and blue |
| Ink | `#231F20` | 35, 31, 32 | Body text of the original | Optional body text on white |
| Descriptor grey | `#525456` | 82, 84, 86 | Descriptor on p1 | Lockup descriptor, captions |
| Deep green (**PROPOSAL**, not in the original) | `#1E7A4A` | 30, 122, 74 | Brand green darkened to pass AA on white | Small green text or thin lines on white, only if the client approves |

Brand gradient (p20, also behind most dark pages): linear, left to right, `#1F3162` → `#2B458A` at 52% → `#3758B0`.

Contrast of the text pairs a document will use (WCAG ratio; AA = 4.5 body, 3.0 large text):

| Text | Background | Ratio | Body text | Large text |
|---|---|---|---|---|
| Navy | White | 12.55 | pass | pass |
| Navy | Light tint | 11.82 | pass | pass |
| Royal blue | White | 6.59 | pass | pass |
| Royal blue | Light tint | 6.21 | pass | pass |
| Ink | White | 16.30 | pass | pass |
| Descriptor grey | White | 7.61 | pass | pass |
| White | Navy | 12.55 | pass | pass |
| White | Royal blue | 6.59 | pass | pass |
| Light tint | Navy | 11.82 | pass | pass |
| Green | Navy | 5.83 | pass | pass |
| Periwinkle | Navy | 5.50 | pass | pass |
| Navy | Green | 5.83 | pass | pass |
| Green | Royal blue | 3.06 | **fail** | pass (large only) |
| Green | White | 2.15 | **fail** | **fail** |
| White | Green | 2.15 | **fail** | **fail** |
| Periwinkle | White | 2.28 | **fail** | **fail** |
| Royal blue | Navy | 1.90 | **fail** | **fail** |
| Deep green (proposal) | White | 5.33 | pass | pass |

Rules that follow: text is navy (or ink) on light and white on dark. Green is an accent: on navy it may carry text; on white it is for shapes, rules and markers only (the original's green page numbers and green logo on white fail). On a green shape the text is navy, never white. Colour blindness: blue and green are never the only difference between two pieces of information; the pair navy/white and green/navy keep a strong lightness difference (ratios above) under protan, deutan and tritan vision. Not tested with a simulator.

## 3. Graphic language, as observed in the original

All four devices come from the wordmark itself: its 45-degree cuts, its rounded ends and the star in its badge.

1. **Rounded diamond.** A square turned 45 degrees with soft corners (radius about 14 to 18% of the side). Used as an image mask (cover p1: three diamonds of different sizes running down a diagonal, two of them bleeding off the page), as a blue-tinted overlay on photographs (p2), as the holder for service icons (p10, with a pale outer ring and a soft shadow), as a half-hidden shape entering from a page edge (p6 top, p16 left) and as small white bullets in lists (p11). On photographs the diamond carries a royal-blue duotone or a strong blue overlay (opacity estimated by eye at 70 to 85%).
2. **Four-point sparkle pattern.** The concave four-point star from the logo badge, repeated on a square grid, small (roughly 2 mm on a 5 mm pitch, estimated by eye), in periwinkle `#9BABD7` on white or in a lighter blue on the gradient. It appears as a narrow band, not a full-page texture: a vertical strip 6 columns wide on the outer edge (p6), a strip 3 rows high fading out at one end (p5), or a very pale all-over ground behind icons (p10, p16).
3. **Diagonal image masks.** Photographs are cut on a 45-degree line: a full-height photo ending in a diagonal edge with a blue gradient panel overlapping it (p5, p11), or a blue panel shaped as a large arrow or chevron pointing into the photo (p5). Photographs under a mask are greyscale or blue-toned; full-bleed photos are blue-toned (p9).
4. **Gradient panels.** Text on dark pages sits on the navy-to-royal-blue gradient with white type, a thin white or blue rule under the title (about 60 mm long), the logo in the top-right corner and the page number bottom-right in green.
5. **Vertical title tab.** On the services page a navy vertical band carries the section title rotated 90 degrees (p10).
6. **Pill.** The fully rounded bar that is the dot of the ya in the wordmark; not used in the original's layout but available for tags and page-number holders without leaving the brand's shapes.

For the new profile: keep devices 1 to 3 as the signature, use them with more restraint and a consistent grid (one diamond scale system, one sparkle band per spread at most), and keep photographs in a single blue-toned treatment.

Imagery in the original: stock-style photographs of construction, cleaning, rope-access, landscaping; licences unknown (see `licences.md`). Icons: solid white glyphs in blue diamonds; source unknown.

## 4. Typography for the new profile

The original uses Bahij TheSansArabic, Hacen, Frutiger Arabic and Cairo. Except Cairo these are commercial fonts not licensed here; they are not used.

**Recommendation: Tajawal (Arabic) + IBM Plex Sans (Latin).** Both SIL OFL 1.1, both available as static files that embed by name.

- Tajawal: low contrast, geometric, with squared curves and flat endings that echo the wordmark; its ExtraBold gives headings the same heavy presence the original had with Hacen; Regular reads well in body sizes. It is also the face of the proposed descriptor line.
- IBM Plex Sans: matching low contrast and flat terminals, a similar weight range (Light to Bold), clear numerals, and a technical, engineering tone that suits contracting, maintenance and logistics.
- Western numerals in both scripts. No letter-spacing on Arabic. No italics.

Weights: Arabic Regular 400 (body), Medium 500 (lead, labels), Bold 700 (headings), ExtraBold 800 (titles, numerals). Latin Regular 400, Medium 500, SemiBold 600, Bold 700.

Type scale, A4 landscape (297 × 210 mm), sizes in pt:

| Level | Arabic (Tajawal) | Line height | Latin (IBM Plex Sans) | Line height |
|---|---|---|---|---|
| Cover title | 46 ExtraBold | 1.25 | 38 Bold, −0.01 em | 1.1 |
| Section title | 32 ExtraBold | 1.3 | 27 Bold | 1.15 |
| Heading | 20 Bold | 1.4 | 17 SemiBold | 1.25 |
| Lead paragraph | 14 Medium | 1.7 | 12.5 Regular | 1.5 |
| Body | 11.5 Regular | 1.75 | 10 Regular | 1.5 |
| Label / caption | 9.5 Medium | 1.6 | 8.5 Medium, caps, +0.06 em | 1.4 |
| Large numeral | 40 ExtraBold | 1.0 | 40 Bold | 1.0 |
| Page number | 9 Medium | | 9 Medium | |

Arabic is set 12 to 15% larger than the Latin beside it so the two read as equal. Arabic block right-aligned, Latin block left-aligned, never interleaved line by line. Body measure: 9 to 13 words per Arabic line.

## 5. Open points

1. Client approval of the new name spelling and of the proposed lockup.
2. Client approval of the derived one-colour versions.
3. Whether the client wants Deep green `#1E7A4A` added (otherwise green is never used for small text on white).
4. The original writes the name both «اطلبني» (logo, descriptor) and «أطلبني» (body text, p6). The logo spelling «اطلبني» is used here; the client should confirm the spelling for running text.
5. "Emaar / إعمار" is the name of a well-known real-estate group; trademark check advised. This document is not a legal clearance.
6. No black version, PDF or 1x/2x/4x PNG exports of the logo were made at this stage (capture for the profile only); they belong to final delivery once the lockup is approved.

---

## Proposed text for `brand-context.md` section 5

> To be pasted by the Creative Director. Nothing below is client-approved yet.

## 5. Visual identity (captured 2026-11-13 from the client's existing profile; client approval pending)

- **Creative direction (one sentence):** No new direction: the existing identity is kept — the heavy geometric «اطلبني» wordmark in royal blue with green accents, on white or on a navy-to-blue gradient, with rounded diamonds, a four-point sparkle pattern and 45-degree image masks.
- **Logo files and usage:** `04-identity/02-logo/`. Wordmark: `otlobny-emaar_logo_wordmark-{colour,reversed,white,navy}_ar_v01.svg` (vector, extracted from p20 of the original; one-colour versions derived by the agency). PROPOSED name lockup with «شركة اطلبني إعمار / OTLOBNY Emaar Co.» in Tajawal Bold: `otlobny-emaar_logo_lockup-proposal-{colour,reversed,white,navy}_ar-en_v01.svg` — awaiting client approval; name spelling ASSUMED. Colour version on white/light; reversed (green + white) on navy; white on royal blue, gradient and photos; navy for single-colour use. Clear space = alef width on all sides. Minimum: wordmark 16 px / 10 mm high; lockup 96 px / 17 mm high (agency recommendations).
- **Colours:**

| Name | HEX | RGB | CMYK | Pantone | Use |
|---|---|---|---|---|---|
| Royal blue | #3758B0 | 55, 88, 176 | to be matched by printer | to be matched by printer | Wordmark, headings, large shapes; text on white (6.59:1) |
| Green | #5AC584 | 90, 197, 132 | to be matched by printer | to be matched by printer | Accent only; text only on navy (5.83:1); never text on white (2.15:1) |
| Navy | #1F3162 | 31, 49, 98 | to be matched by printer | to be matched by printer | Dark backgrounds; text on white (12.55:1) |
| Light tint | #F7F8FC | 247, 248, 252 | to be matched by printer | — | Page and panel backgrounds |
| Periwinkle tint | #9BABD7 | 155, 171, 215 | to be matched by printer | — | Sparkle pattern; secondary text on navy (5.5:1) |
| White | #FFFFFF | 255, 255, 255 | 0, 0, 0, 0 | — | Background; text on navy and blue |
| Descriptor grey | #525456 | 82, 84, 86 | to be matched by printer | — | Lockup descriptor, captions |

  Gradient: linear, `#1F3162` → `#3758B0`. Proposed extra (not approved): Deep green `#1E7A4A` for small green text on white. Tokens: `04-identity/03-system/tokens.json`.
- **Typefaces:** Arabic — Tajawal (Regular, Medium, Bold, ExtraBold); Latin — IBM Plex Sans (Regular, Medium, SemiBold, Bold); both SIL OFL 1.1; licences in `04-identity/licences.md`. The original's Bahij TheSansArabic, Hacen and Frutiger Arabic are commercial and not licensed here. Type scale in `04-identity/03-system/system.md`.
- **Imagery and graphic style:** rounded diamonds (45-degree squares with soft corners) as image masks, icon holders and bullets; four-point sparkle pattern in narrow bands; photographs cut on 45-degree diagonals and toned blue or greyscale; white type on the navy-to-blue gradient. Photographs and client logos in the original have unknown licences; the four supplied mockups appear AI-generated.
- **Do not:** blue wordmark on navy (1.9:1); all-green wordmark or green text on white (2.15:1); white text on green; the old descriptor «للصيانة والنظافة»; logos copied from the mockup images ("OTLOBY", "OTLOBIY"); letter-spacing on Arabic; redrawing or recolouring the wordmark.
