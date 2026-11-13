# Distinctiveness check — Sidra Coffee "Weekly Beat" against three competitors

> **SYSTEM TEST — FICTIONAL CLIENT.** The client is invented. The three competitors are real companies.

**Date:** 2026-11-13  **Prepared by:** Art Director  **Answers:** quality review r1, issue 1 (critical)
**Captures:** `02-research/_work/captures/` (12 PNGs, `capture.json`, `capture-products.json`)

## Result in one paragraph

**Brew92 is verified and distinct.** **Camel Step and Elixir Bunn are only partly verified:** their pages loaded, but their logos, product photographs and theme stylesheets did not, so I have not seen either company's mark or packaging. On what did load, neither is close to Sidra in colour or device. Two things were found that the audit did not know: Camel Step's site is set in **IBM Plex Sans Arabic, the same typeface as Sidra**, and Elixir Bunn's page uses **a red (`#D92C20`) near Ember**, whose role I could not see. Review issue 1 is therefore closed for Brew92 and still open for the other two.

## What was captured, and what failed

| Site | Pages captured | Loaded | Did not load |
|---|---|---|---|
| brew92.com | Home, products list, one product (Cheetah) | Everything: logo, styles, photographs, bags | Nothing that matters |
| camelstep.com | Home, coffee category | Page text, the web font, inline colours | All 47 images including the logo, and the theme stylesheet |
| elixirbunn.com | Home, all-products list | Page text, the web font (Google Fonts), inline colours | All 100 images including the logo, and the theme stylesheet |

Camel Step and Elixir Bunn both run on the Zid store platform. Their images and stylesheets are served from `img.zid.store` and `static.zid.store`, and every request to those two hosts failed in this environment (a direct test of both hosts also returned no response). Their screenshots are therefore unstyled pages with broken-image icons. I did not retry further.

Colour values below are the computed values reported by `scripts/site_capture.cjs`, converted from RGB to HEX by me.

## 1. Brew92 — verified

| | What I saw |
|---|---|
| Logo | Latin-only wordmark "BREW92°": thin, wide-spaced capitals with a small ring after the numeral. No symbol. A short "92°" appears alone on the bags |
| Colours | Electric blue `#000CDB` (logo, links, buttons, product text); cool grey `#C9CDD0` (header band); white; near-black `#120C0E`. No red anywhere |
| Typefaces | TheSans (reported as TheSansArabicPlain, TheSansArabicBold, TheSansBoldCaps); English set in capitals |
| Language lead | English. The page is `lang="en"`, left to right, with an "العربية" switch |
| Imagery | Home page is a full-width photograph of coffee cherries held in a hand, with a serif-italic origin title. Bags are matte white or silver pouches with a small label; one label carries an animal-print pattern |

**Against Sidra:** blue and grey against Ember and warm Paper; thin Latin capitals against a heavy Arabic wordmark; no device against the seven bars; photography with a person against no people at all; English-led against Arabic-led.

**Verdict: DISTINCT.** The open question in `creative-direction.md` ("if Brew92 uses a strong red, Ember is reviewed") is closed: it does not. The audit's recall of a "neutral palette" was wrong; the lead colour is a saturated blue.

## 2. Camel Step — partly verified

| | What I saw |
|---|---|
| Logo | **Not seen.** The logo image failed to load. Only its alt text, «خطوة جمل», was visible. Whether it is an emblem, a camel, or a wordmark is still unknown |
| Colours | Dark blue-teal `#133F57` (announcement bar, visible in the screenshot); slate blue `#365A7A` (add-to-cart buttons, visible); white ground; text `#172026`. A purple `#6F42C1` also appears, on a "featured product" badge; the same purple appears on Elixir Bunn's page, so I read it as the store platform's colour, not the brand's |
| Typefaces | **IBM Plex Sans Arabic** for all text, reported by the script and visibly rendered in the screenshot |
| Language lead | Arabic. `lang="ar"`, right to left, Arabic page title |
| Imagery | **Not seen.** No product or banner image loaded |

**Against Sidra:** the colours seen are cool blues, far from Ember, and nothing earthy or warm loaded. No device could be compared because the mark was not seen. Both brands are Arabic-led. **Both use IBM Plex Sans Arabic.**

**Verdict: NOT YET VERIFIED. On what was seen, distinct in colour; one real overlap in typeface.**

- The typeface overlap is not, by itself, "too close": IBM Plex Sans Arabic is a widely used open font, I could not tell whether it is Camel Step's brand typeface or the store theme's default, and Sidra's recognisable elements are the seven bars and Ember, not the text face.
- It does raise the stakes on one existing ruling. Sidra's current wordmark is outlined IBM Plex Sans Arabic Bold, accepted for the test only. A wordmark typed in the same family a category leader uses for its whole site is not ownable. **Change required: the custom-drawn wordmark in `creative-direction.md` section 5 is mandatory before any real use, and this is now a distinctiveness requirement, not only a craft one.**
- The audit's recall of a "warm earthy palette" is not supported by the site, but packaging was not seen, so it is not disproved either.

## 3. Elixir Bunn — partly verified

| | What I saw |
|---|---|
| Logo | **Not seen.** The logo image failed to load. Its alt text is the Latin "Elixir Bunn" |
| Colours | Reported by the script: red text `#D92C20`; pale pink ground `#FEE4E2` (largest coloured area on the home page); pale yellow `#FEF8D8`; pale violet `#F1EFFE` with violet `#7462F4`; black text on white. **None of these could be seen in place**, because the stylesheet did not load. A red on a pale pink ground is a common pattern for discount or stock labels, but I cannot confirm that is what it is |
| Typefaces | Changa (a Google font, loaded and visibly rendered) for Arabic and Latin |
| Language lead | Arabic on the site: `lang="ar"`, right to left, Arabic title «اكسير البن», with an "English" switch. The logo's alt text is Latin |
| Imagery | **Not seen** |

**Against Sidra:** Changa is a squarer, more geometric face than IBM Plex Sans Arabic; the two do not look alike. No device could be compared. The audit's recall of "dark, minimal, Latin-prominent" is not supported by the site (it is Arabic-led and light), though the logo itself may still be Latin.

**Verdict: NOT YET VERIFIED. Distinct in typeface; one open colour risk.**

- `#D92C20` is close to Ember `#C23A20`: both are orange-leaning reds, and Ember is the darker of the two.
- **If** inspection shows that red is Elixir Bunn's lead brand colour (logo, bags, shopfronts), then Ember as Sidra's lead colour is too close for two Riyadh roasters, even with a different device. **Change in that case:** move Ember darker and browner, towards a brick tone, until it no longer reads as the same red beside theirs; keep Paper on Ember at 4.5:1 or better; re-issue the tokens and re-export. The seven bars, grid and type stay.
- **If** it is only a sale or stock label colour, no change is needed.

## Side by side

| | Sidra — Weekly Beat | Brew92 (seen) | Camel Step (partly seen) | Elixir Bunn (partly seen) |
|---|---|---|---|---|
| Lead colour | Ember `#C23A20` on Paper `#F3ECE0` | Blue `#000CDB` on grey `#C9CDD0` | Blues `#133F57`, `#365A7A` on white | Unknown; a red `#D92C20` is present, role unknown |
| Mark | Heavy Arabic wordmark سدرة on seven bars, one lit | Thin Latin wordmark, no symbol | Not seen | Not seen |
| Device | Seven-bar row and seven-column grid | None seen | Not seen | Not seen |
| Typeface | IBM Plex Sans Arabic + IBM Plex Sans | TheSans | IBM Plex Sans Arabic | Changa |
| Language lead | Arabic | English | Arabic | Arabic on site |
| Imagery | No people; flat colour and type | Photography, including a hand | Not seen | Not seen |
| Verdict | — | **Distinct** | **Not verified**; typeface overlap | **Not verified**; possible red overlap |

## Corrections to the audit and to my earlier claims

- "Arabic-first" is **not** a visible difference from Camel Step or Elixir Bunn: both sites are Arabic-led. It separates Sidra from Brew92 only. `directions.md` and the strategy lean on this more than the evidence allows.
- Brew92 is not "neutral"; it is blue-led.
- Nothing seen supports "warm earthy" for Camel Step or "dark minimal" for Elixir Bunn. Nothing seen disproves them for packaging.

## Still not seen

- The logos of Camel Step and Elixir Bunn.
- Any packaging of Camel Step or Elixir Bunn. Brew92's bags were seen only as small web photographs.
- Instagram or any other social account, for all three.
- Cafés, signage, cups or printed material, for all three.
- Whether any roaster in the market, including the five named but not audited, uses a row-of-bars device. No search was made.
- This is a visual comparison, not a trademark search or legal clearance.

## What is needed to close review issue 1

1. Someone on an unrestricted connection opens camelstep.com and elixirbunn.com, saves the two logos and three or four bag photographs each into `02-research/_work/captures/`, and notes where `#D92C20` is used on Elixir Bunn's site.
2. I then complete sections 2 and 3 and give final verdicts. Estimated effort: one short pass.
3. Until then, the identity should not be described as "checked distinct from all three competitors".
