# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v01

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Date:** 2026-11-13  **Author:** corporate-designer
**Status:** DRAFT v01 for the Creative Director and the quality-reviewer. Not approved by the client. Not for release as final.

## 1. What was built

| File | What it is |
|---|---|
| `otlobny-emaar_company-profile_screen_ar-en_v01.pdf` | The profile: 20 pages, 297 × 210 mm, screen PDF (sRGB), 8.9 MB |
| `otlobny-emaar_company-profile_screen_ar-en_v01.html` | Editable source: one HTML document with its CSS inline; fonts, logos and images are linked from `assets/` |
| `_work/build_profile_v01.py` | The generator that writes the HTML (copy, positions and CSS in one place). Edit here and re-run to keep all 20 pages consistent; the HTML can also be edited directly |
| `_work/prepare_images_v01.py` | Makes the cropped and duotone derivatives in `assets/derived/` |
| `_work/export_v01.sh` | Build → `scripts/html2pdf.cjs --size 297x210mm` → `_work/finish_pdf_v01.py` → `scripts/check_arabic_pdf.py` |
| `_work/finish_pdf_v01.py` | Adds to the exported PDF: document title, language `ar`, right-to-left reading direction, seven section bookmarks |
| `_work/measure_v01.cjs` | Playwright measurement of every page and text block (overflow, line counts) |
| `_work/preview_v01/` | 20 page previews at 110 dpi from the final export |
| `_work/otlobny-emaar_company-profile_grid-proof_p03/p08/p15/p18_v01.png` | Pages 3, 8, 15, 18 with the 12-column / 6-row grid overlaid |
| `assets/fonts/` | Tajawal Regular, Medium, Bold, ExtraBold; IBM Plex Sans Regular, Medium, SemiBold, Bold (static TTF) with both OFL texts |
| `assets/logo/` | Unchanged copies of the three logo SVGs used (colour lockup proposal, white lockup proposal, white wordmark) |
| `assets/derived/` | Seven image derivatives (one of them, `p12_team_duotone_candidate.png`, is NOT placed) |

Page map: 1 cover · 2 contents · 3 about · 4 vision · 5 mission · 6 goals · 7 services overview · 8–13 six services · 14 why · 15–17 three works · 18–19 partners («شركاء النجاح» / Partners in Success, 12 + 15 = 27 logos) · 20 contact and back cover.

## 2. Checks carried out

- `check_arabic_pdf.py --expect "اطلبني إعمار"`: **PASS**. 20 pages, 297 × 210 mm. Fonts named in the PDF: Tajawal Regular / Medium / Bold / ExtraBold and IBM Plex Sans Regular / Medium / SemiBold / Bold, all embedded subsets; no fallback font; 4,367 Arabic characters extracted, no presentation forms.
- Every one of the 20 previews of the final export was opened and read: Arabic connected and right to left, punctuation on the correct side, numerals not reversed («01 / 06», phone, CR), nothing clipped, headers / folios consistent, no placeholder text other than the two marked draft items (section 5).
- Playwright: every page box is exactly 297 × 210 mm with no scrolling content; no text block leaves the 19 mm side margins or the header / footer zones; no horizontal overflow.
- Second renderer: pages 7 and 20 rendered with Poppler (`_work/preview_v01_poppler/`); page 7 opened and compared.
- PDF read-back: title, `/Lang ar`, `/Direction R2L`, 7 bookmarks, 15 links (contents entries, service rows on page 7, phone, email).

## 3. Deviations from `art-direction.md` (AD) and `content-outline.md`, with reasons

Rulings of the Creative Director (brand-context decision log, last row) applied as given: partners on pp18–19 on a white ground with a hairline grid and no tiles; contact merged into p20; title «شركاء النجاح» / "Partners in Success"; partner order existing 01–18 then new 01–09 in file order (this replaces the AD's order "by kind" for the nine); transparent Keeta and ZERO; page 13 draft pill wording; no logo on inside pages except p7.

| # | Page | AD / outline says | Built | Reason |
|---|---|---|---|---|
| 1 | 1 | Activity line under the titles; "if either wraps to a second line, drop the line on both sides" | Line dropped; titles moved down 10 mm (baseline about y 178 instead of 168) | The English line in Label caps is about 180 mm wide against the 127 mm half-width, so the AD's own rule removes it. The titles were lowered so the foot of the cover is not left empty |
| 2 | 12 | Mockup crop (image no. 4) if no wrong text is legible, otherwise the graphic panel | **Graphic panel (T6-G)** | In the crop the two chest logos are clearly recognisable as a wordmark with a descriptor line under it, and they are wrong drawings of the logo. Not used. Alternation is therefore 8 P · 9 G / 10 G · 11 P / 12 G · 13 G, which the AD accepts. No mockup image appears anywhere |
| 3 | All inside | Page title in R1 from y 26 | Title top at y 31.5 on every inside page; on service and project pages the ordinal line sits at y 26 above it | So the title is at an identical position on all pages whether or not there is an ordinal line |
| 4 | 3 | Paragraph in R2–R3; fact table from y 110, pitch 18 | Fact table from y 118, pitch 16 | The Arabic paragraph needs seven lines at Lead size (to y 112) and would touch the table |
| 5 | 7 | Six rows from y 54, pitch 22; holder 18 × 18 with the page number beneath; one-line descriptions | Rows from y 46 to 187, heights 21.4–26.8 mm shared by content; holder 14 × 14; description line-height 1.6 (Arabic) | With the real copy three Arabic descriptions run to two lines and the English manpower line to three; holder + page number alone is 22.5 mm. Equal 22 mm rows cannot hold the outline's copy at the AD's sizes, and the copy may not be cut |
| 6 | 14 | Rows from y 51, pitch 22.5, descriptions two lines at most | Rows from y 47 to 186, heights 17.7–27.9 mm shared by content | Same cause: point 01 runs to three English lines and point 06's English title to two |
| 7 | 14 | Outline writes each point as "**Title** — description" | Title on its own line, description beneath; the first letter of each English description is capitalised; the dash is dropped | The AD sets title and description in two sizes on two lines. No word changed |
| 8 | 8–13 | List rows at a fixed 10 mm pitch | 10 mm minimum; rows with a two-line item are taller, and the two languages share each row so tops align | Five list items do not fit one line in an 83 mm column |
| 9 | 15–17 | Ordinal line above the title | The ordinal only ("01 / 03"), without repeating the section name | The title on these pages is itself «أعمالنا» / "Our Work" |
| 10 | 15–17 | Scope chips | Words taken from each project's own sentence: تصميم، تركيب / تشغيل، صيانة، نظافة / صيانة، نظافة (and the English equivalents) | Specified by the AD; not separate lines in the outline. No service is listed that the sentence does not name |
| 11 | 18 | Title block in Section size (32 / 27) on one baseline | Page-title size (26 / 22) | At 32 / 27 the two titles together are wider than the three-cell block |
| 12 | 18–19 | Tiles 47 × 40 with 6 mm gaps on a tint ground; logo box 31 × 20; Keeta and ZERO on their own coloured tiles | White ground; 5 × 3 cells of 51.8 × 44 mm with internal 0.25 pt hairlines; each mark capped at 34 × 21 mm and levelled by area (about 400 mm²) | Creative Director's ruling 3 (client instruction: transparent logos, no tiles) |
| 13 | 18–19 | Low-resolution cap: 70% of the size on the old page | Cap: never above native pixels at 150 ppi (two soft-masked logos capped by their effective detail: Development Authority 20.6 mm wide, Taza 23.8 mm) | Creative Director's ruling 3. `assets/partners-transparent/` had no README when the pages were built, so the caps were computed from the pixel sizes and the notes in `assets/partners/README.md` |
| 14 | 20 | Lockup at y 34–68; address blocks in K2–K5 / K8–K11; website row "shows the draft pill instead of a value" | Lockup at y 26–60; a title row «تواصل معنا» / "Contact" (Section size) at y 71; address aligned with the contact rows (x 60–237) and broken after the road name; website row shows a pill with both candidate domains, labelled «الموقع الإلكتروني — يحدده العميل» / "Website — client to confirm" | The outline's contact-page heading had to move here with the merge; the address reads better aligned to the rows; the website wording follows the outline's own placeholder |
| 15 | 20 | Outline's back-cover lines (phone · email, city, website) | Not repeated: the same facts are in the contact rows on the same page | Merge of pages 19 and 20 |
| 16 | 2–19 | Draft pill on "any page carrying [D] or TBC content (p13 in full; website lines; the name)" | Pill on p13 and on the website row of p20 only | Creative Director's ruling 6 names page 13. The name is on every page; logistics is also mentioned on pp3, 7 and 14 without a pill — see open item 3 |
| 17 | 7–13 | Icon strokes "cut at 45 degrees where a stroke terminates freely" | Round caps and joins only | The same sentence asks for rounded caps; one rule was kept. Icons were drawn for this document (no icon set, no licence needed) |
| 18 | All | Sparkle "traced from the logo badge" | A concave four-point star drawn to match it | Not traced from the logo paths |
| 19 | 10, 11 | — | "air-conditioning" kept on one line; the English intro on p11 is balanced | Avoids a break at a hyphen and a one-word last line |
| 20 | — | AD requirement 4: tagged PDF | **Not tagged.** Title, language, reading direction and bookmarks were added; alternative text exists in the HTML only | `scripts/html2pdf.cjs` does not ask Chromium for a tagged PDF |

Typographic changes to the copy, none of them a rewrite: straight apostrophes set as typographic ones; numerals and the "01 / 06" ordinals isolated left to right inside Arabic lines.

## 4. Images and effective resolution (read back from the PDF)

| Page | File placed | Source | Crop (l, t, r, b) | Pixels | Placed size | Effective ppi | Treatment |
|---|---|---|---|---|---|---|---|
| 1 | `assets/derived/cover_glass-facade_duotone.png` | `assets/photos/glass-facade-cleaners.png` | 0.45, 0, 0.98, 0.75 | 655 × 657 | 110 × 110 mm, diamond mask | 151 | Duotone |
| 8 | `assets/derived/p08_electrical-panel_duotone.png` | `assets/photos/electrical-panel.png` | 0.17, 0, 0.611, 1 | 547 × 873 | 83 × 132.5 mm | 167 | Duotone, chamfer |
| 11 | `assets/derived/p11_office-cleaner_duotone.png` | `assets/photos/office-cleaner.png` | 0.63, 0, 0.967, 1 | 547 × 873 | 83 × 132.5 mm | 167 | Duotone, chamfer |
| 15 | `assets/derived/p15_bus-shelter.png` | `assets/photos/bus-shelter.png` | 0.44, 0, 0.989, 1 | 522 × 471 | 83 × 75 mm | 160 | Full colour |
| 16 | `assets/derived/p16_chamber-building.png` | `assets/photos/chamber-building.png` | 0.21, 0, 0.99, 1 | 503 × 454 | 83 × 75 mm | 154 | Full colour |
| 17 | `assets/derived/p17_shahd-hotel.png` | `assets/photos/shahd-hotel.png` | 0.20, 0, 0.979, 1 | 822 × 743 | 83 × 75 mm | 251 | Full colour |
| — | `assets/derived/p12_team_duotone_candidate.png` | `assets/mockups/mockup_cleaning-team.png` | 0.385, 0.04, 0.719, 0.84 | 513 × 819 | not placed | — | Rejected, deviation 2 |

No image is upscaled, flipped or retouched. Nothing in `_originals/` was opened for writing.

Partner logos, from `assets/partners-transparent/` (27 files; the `_on-yellow` and `_on-dark` variants are not used). Size of the visible mark on the page and its effective resolution:

| Logo | Mark, mm | ppi | | Logo | Mark, mm | ppi |
|---|---|---|---|---|---|---|
| existing-01 green-dome emblem | 10.8 × 16.9 | 150 | | existing-15 column emblem | 14.9 × 17.3 | 150 |
| existing-02 Development Authority | 20.6 × 13.0 | 150 (effective) | | existing-16 Hippo | 14.5 × 21.0 | 893 |
| existing-03 Al Maqar | 21.7 × 14.1 | 150 | | existing-17 Taza | 23.8 × 16.8 | 153 (effective) |
| existing-04 AR Spa | 22.1 × 18.1 | 983 | | existing-18 calligraphic mark | 18.8 × 10.7 | 150 |
| existing-05 Mawaddah | 25.9 × 15.5 | 156 | | new-01 Manazil Al-Mukhtara | 22.4 × 17.8 | 1178 |
| existing-06 Imagine More | 28.7 × 13.9 | 900 | | new-02 Novotel | 32.0 × 12.5 | 994 |
| existing-07 HSH | 17.6 × 9.1 | 150 | | new-03 Keeta (black) | 27.4 × 14.6 | 691 |
| existing-08 Cooperative Taibah | 13.5 × 12.2 | 150 | | new-04 Jahez | 24.0 × 16.7 | 846 |
| existing-09 Dar Al Taqwa Hotel | 34.0 × 5.2 | 218 | | new-05 Medina Festival Dates | 15.3 × 21.0 | 1264 |
| existing-10 Dallah Taibah Hotel | 16.6 × 16.8 | 150 | | new-06 HungerStation | 27.9 × 14.3 | 1063 |
| existing-11 Al Madinah Harmony | 29.2 × 13.7 | 162 | | new-07 Rotana | 34.0 × 11.7 | 855 |
| existing-12 Tiny House | 30.2 × 13.3 | 613 | | new-08 Chop & Co | 24.9 × 16.1 | 1187 |
| existing-13 Platinum | 26.3 × 15.2 | 928 | | new-09 ZERO (charcoal) | 33.9 × 11.8 | 759 |
| existing-14 Madinah Chamber | 31.5 × 12.7 | 1533 | | | | |

Because of the 150 ppi cap the low-resolution logos are visibly smaller than the others, and their small lettering cannot be read (green-dome emblem, Development Authority, Dar Al Taqwa, Cooperative Taibah, HSH, the column emblem, the calligraphic mark). That is the honest size of the files; only official artwork from the owners fixes it.

## 5. What remains open

1. **Name and lockup.** «اطلبني إعمار» / "OTLOBNY Emaar", the legal form, and the proposed lockup on pp1 and 20 are still assumptions awaiting the client. A change of name touches the three logo placements and the live text.
2. **Website.** Page 20 shows both otlobny.co and otlobny.com inside a marked draft pill. It must be replaced by the confirmed domain, or the row removed, before any final.
3. **Logistics.** Page 13 is all draft and carries the pill. Logistics is also named, without a pill, on p3 ("six fields"), p7 (sixth row) and p14 (point 01), exactly as the outline writes them. If the client does not confirm logistics these four pages and the service ordinals ("0n / 06") change.
4. **Phone 054 955 5514** and the address: taken from the old profile, not reconfirmed.
5. **Image rights.** The photographs on pp1, 8, 11, 16 and 17 come from the old profile with unknown licences; p16 looks like an architectural rendering. Each has a fallback in the AD. The client's own higher-resolution photographs would lift pp15–17.
6. **Partner logos.** Permission from each owner is the client's responsibility. Twelve of the existing 18 are low-resolution; five owners are still unnamed (alternative text describes those marks instead of naming them).
7. **Mockups.** None is used. The client is still to say whether to regenerate them with the new name; if a clean team image arrives, p12 can return to a photograph panel.
8. **Mission wording** (outline note on p5) is unchanged and still describes manpower supply only.
9. **Arabic proofreading by a native reader** has not been done on the layout.
10. **Print.** This is a screen PDF: RGB, no bleed, no crop marks, not PDF/X. A print version needs CMYK values from the printer, 3 mm bleed (the cover diamond and the gradient pages bleed) and vector partner logos.
11. **Accessibility.** The PDF is not tagged (deviation 20). Contrast uses only pairs marked "pass" in `system.md`; green appears as shapes only.
12. `assets/partners-transparent/README.md` did not exist at build time; if the other agent's README gives different size caps, pp18–19 should be checked against it.
