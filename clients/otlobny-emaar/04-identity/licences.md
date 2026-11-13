# Licences and sources — otlobny-emaar

Date: 2026-11-13. Stage: identity capture (no new identity was designed).

## 1. Logo artwork: what was extracted from where

| Item | Source | How |
|---|---|---|
| «اطلبني» wordmark (letterforms, star badge, dot, squeegee) | `_originals/otlobny_company-profile_original_2026-11-13.pdf`, page 20 (back cover), where it is vector artwork. Working copy: `01-brief/assets-received/page20.svg` | Paths 2 to 13 of the page were copied; coordinates were only shifted to a tight viewBox. Nothing was redrawn. Build script: `04-identity/_work/build_logo.py` |
| Colours of the full-colour version | Page 1 (front cover) of the same PDF, where the logo is a raster image; sampled at 400 dpi | Royal blue `#3758B0`, green `#5AC584`. Which part is blue and which is green was read from page 1 |
| Reversed version | Page 20 as it stands: green wordmark, white dot and squeegee | Same paths and fills as the source |
| Dot | Source draws a filled circle plus a stroked circle of the same radius | The stroke was converted to two filled circles with the same visible edges (outer radius 10.03, inner 8.62 page units). Geometry equivalent, no longer a stroke |
| One-colour white and navy versions | **Derived by the agency.** The original contains no one-colour version | The squeegee and the dot are separated from the letters by a gap equal to the source's own ring width (1.41 units). The gap was cut with skia-pathops. Needs client approval |
| Not carried over | The old descriptor line «شركة اطلبني للصيانة والنظافة / OTLOBNY Mantinance & Cleaning Co.», the page gradient and the contact lines | Left out on purpose |

Ownership: the wordmark is the client's existing logo. The agency has no information on who drew it or on any trademark registration. **Not a legal clearance.** The new name contains «إعمار / Emaar», which is also the name of a very well-known real-estate group; a trademark check by the client is advised before the name is used publicly.

## 2. Proposed descriptor line (new)

«شركة اطلبني إعمار» / "OTLOBNY Emaar Co." set in **Tajawal Bold**, shaped with HarfBuzz and converted to outlines, so the SVGs carry no font. Name spelling is an assumption pending the client.

## 3. Fonts

| Font | Used for | Licence | File |
|---|---|---|---|
| Tajawal (Boutros Fonts) | Descriptor line of the proposed lockup (outlined); recommended Arabic typeface for the profile | SIL Open Font License 1.1: free for commercial use, embedding and modification; may not be sold on its own | `assets/fonts/tajawal/` (`OFL.txt` included) |
| IBM Plex Sans (IBM) | Recommended Latin typeface for the profile | SIL Open Font License 1.1 | `assets/fonts/ibmplexsans-static/` (`OFL.txt` included) |
| Cairo | Tested for the descriptor, not chosen. Also one of the fonts in the original profile | SIL Open Font License 1.1 | `assets/fonts/cairo/` |

Fonts found in the original profile that are **not** licensed here and are not used in new work: Bahij TheSansArabic, Hacen (heading face), Frutiger Arabic / Frutiger-family Latin. They are commercial typefaces. If the client holds licences and wants them kept, the client must supply the font files and the licence.

## 4. Images and third-party marks in the original: licence unknown

- **Photographs** in the original profile (construction worker, cleaners, rope-access window cleaners, Riyadh skyline, landscaping and others): source and licence unknown. They are embedded at about 1240 × 875 px. They may be reused only if the client confirms the right to use them; otherwise they must be replaced.
- **Client logos** on page 19 («أصدقاؤنا», 18 logos): each belongs to its owner. Permission to display them is not documented and the copies are low resolution.
- **Saudi Vision 2030 logo** (page 9): its use is governed by official guidelines. Not to be reproduced unless the client confirms permission.
- **Icons** in the services page (hammer, tree, wrench, person, bucket): source and licence unknown; to be redrawn or replaced with openly licensed icons.

## 5. Mockup images supplied by the client

`_originals/mockup_cleaning-team.png`, `mockup_delivery-rider.png`, `mockup_car-scooter-facade.png`, `mockup_logistics-trucks.png` **appear to be AI-generated** (garbled small text, misspelt "OTLOBY" / "OTLOBIY", inconsistent logo details). Their generator, terms of use and any model or property releases are unknown. They show the logo with a brighter blue than the real artwork, the old activity names, and a Riyadh landmark behind a truck. They are evidence of the client's intent, not approved brand artwork, and were not used as a colour source.

## 6. Tools

fontTools, uharfbuzz, skia-pathops, CairoSVG, Pillow, Poppler (pdftoppm): open-source software used to build and preview the files. No Figma or Canva file was created.
