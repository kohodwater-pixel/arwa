# Art direction — «اطلبني إعمار» / OTLOBNY Emaar company profile

**Client slug:** otlobny-emaar  **Stage:** 06-profiles  **Version:** v01, 2026-11-13  **Author:** art-director
**Status:** DRAFT for the Creative Director. Not approved by the client. Built on the captured identity (`04-identity/03-system/system.md`, `tokens.json`), which is itself not yet client-approved, and on `content-outline.md` v01.
**For:** the corporate-designer. Everything below is a specification; where a number is given, use the number.

Scope note: the existing identity is kept. This document directs the layout of one document; it proposes no new logo, colour or typeface. There is no approved strategy in `03-strategy/`; each decision is traced instead to the brief (audience: decision makers in government bodies, hotels and companies who award contracts) and to the captured identity.

Units: millimetres unless stated. Page origin is the top-left corner; x runs left to right, y runs down. Crops are fractions of the source file: (left, top, right, bottom).

---

## 1. Critique of the original, and what to keep

Seen in `06-profiles/_work/original_pages_contact.png`.

1. **No grid.** Titles, logo, text blocks and page numbers sit in a different place on almost every page (title centred on pp6–7, right on p8, inside a panel on pp11–15). Nothing lines up from page to page.
2. **Low-resolution images blown up.** Photographs of 412 px (rebar worker) and 644 px (Chamber) are run at full page height or width. They are soft on screen and would fail in print.
3. **Images that do not match the text.** A greenhouse nursery for parks and street trees (p12), an electrical panel for air-conditioning and lifts (p13), a stock waiter for manpower (p14), the Riyadh skyline for a Madinah company (p9).
4. **Contrast failures.** The all-green logo on white (2.15:1), green page numbers on white, small white text at about 7 pt on the blue panels of pp11–15.
5. **Weak hierarchy and tiny body text.** Service pages carry the title, paragraph and list at nearly the same small size, pushed into one corner of a dark panel while two thirds of the page is a decorative photograph.
6. **Decoration without a rule.** Diamonds, half-diamonds, green outlines, chevrons, dotted bands and a rotated title tab appear in different combinations per page; three pages (pp2–4) carry almost no information ("WE DO THE BEST").
7. **Not bilingual, and careless where it is English.** "Mantinance", "WEBSIUT", "Abdulmajyed"; two different web domains; four typefaces, three of them commercial.
8. **Unsupported claims and borrowed marks.** "The chosen company … for 2021", "one of the leading companies", the Vision 2030 logo, the Ajeer logo inside running text, eighteen client logos at mixed sizes with no order.

**Worth keeping** (and kept):

- The «اطلبني» wordmark, unchanged, and the royal blue / green / navy palette on white.
- The rounded diamond as the cover's image mask: it is the one device a returning reader will recognise.
- The 45-degree cut, which comes from the wordmark itself.
- The four-point sparkle from the logo badge, as a small quiet band.
- White type on the navy-to-blue gradient for the darkest pages.
- The bus-shelter photograph: the client's own work and the strongest image in the file.
- A4 landscape and the 20-page length.

---

## 2. Concept and system

### 2.1 Concept

**"Two languages, one centre":** Arabic stands on the right, English on the left, and whatever the two share — the image, the number, the logo — sits in the middle of the page; the wordmark's own 45-degree cut is the only ornament.

Why: the buyers are bilingual institutions, and the original was neither bilingual nor ordered. A structure in which the two languages face each other as equals across a shared centre is the plainest way to show an organised company, and it needs no fact the client has not supplied. It is distinct from the original (which had no structure) and is not taken from any other company's profile.

### 2.2 Page and grid

| | |
|---|---|
| Format | A4 landscape, 297 × 210. 20 pages. Screen PDF first; if printed, add 3 mm bleed and extend every bleeding shape into it |
| Side margins | 19 left, 19 right (symmetric: the PDF is read as single pages) |
| Columns | 12 columns of 17, gutter 5. Live width 259 (x 19 to 278) |
| Column names | **K1 to K12, counted from the RIGHT** (the document is right to left). Right edge of Kn = 278 − 22 × (n − 1); left edge = right edge − 17 |
| Rows | 6 rows of 22.5, gutter 5. Live height 160 (y 26 to 186). R1 26–48.5, R2 53.5–76, R3 81–103.5, R4 108.5–131, R5 136–158.5, R6 163.5–186 |
| Header zone | y 10 to 19 |
| Footer zone | y 192 to 200 |

Three fixed zones on every inside page:

| Zone | Columns | x | Width | Holds |
|---|---|---|---|---|
| Arabic block | K1–K4 (triptych) or K1–K5 (list pages) | 195–278 or 173–278 | 83 or 105 | Arabic only, right-aligned, `dir="rtl"` |
| Centre | K5–K8 (triptych) or K6–K7 (list pages) | 107–190 or 129–168 | 83 or 39 | What both languages share: image, graphic panel, numerals, icons, logos, phone, email |
| English block | K9–K12 (triptych) or K8–K12 (list pages) | 19–102 or 19–124 | 83 or 105 | English only, left-aligned |

Every edge of every text block, image and panel sits on a column line and a row line. Deliver one export with the grid overlaid (see section 6).

### 2.3 Bilingual structure

- The document reads right to left: page 1 is the cover, the PDF's reading direction and binding are set right to left, even pages are right-hand pages, odd pages are left-hand pages. Spreads are 2–3, 4–5 … 18–19.
- Arabic is always on the right and English always on the left, on every page, in the same zones. Never interleaved line by line, never swapped.
- Rows that pair the two languages (contents, goals, facts, contact) align on the same top line so one item reads straight across.
- Bullets and ordinals: on the right of Arabic lines, on the left of English lines. Shared numerals sit once, in the centre.
- Arabic body in Navy `#1F3162`; English body in Descriptor grey `#525456` (7.61:1). Arabic titles Navy; English titles Royal blue `#3758B0`. This gives Arabic the lead without making English small.
- Not mirrored: the logo, photographs, phone number, Latin words and numerals inside Arabic text.

### 2.4 Type hierarchy

Tajawal (Arabic) and IBM Plex Sans (Latin), static files from `assets/fonts/`, as recommended in `system.md`. Sizes follow its scale; one level (**Page title**) is added between its "section title" and "heading" because 32 pt titles do not fit an 83 mm column.

| Level | Used for | Arabic (Tajawal) | LH | Latin (IBM Plex Sans) | LH |
|---|---|---|---|---|---|
| Cover title | p1 document title | 46 ExtraBold | 1.25 | 38 Bold, −0.01 em | 1.1 |
| Section title | p2, p7, p18 title block, p20 | 32 ExtraBold | 1.3 | 27 Bold | 1.15 |
| Page title (added) | title of every other inside page | 26 ExtraBold | 1.3 | 22 Bold | 1.15 |
| Heading | project names, statements on pp4–5, contents entries, fact values | 20 Bold | 1.4 (1.6 when it runs over 2 lines) | 17 SemiBold | 1.25 (1.35 over 2 lines) |
| Lead | service intro paragraph, about paragraph, point titles (Bold / SemiBold) | 14 Medium | 1.7 | 12.5 Regular | 1.5 |
| Body | lists, sentences, descriptions | 11.5 Regular | 1.75 | 10 Regular | 1.5 |
| Label / caption | running header, ordinals line, captions, notes | 9.5 Medium | 1.6 | 8.5 Medium, caps, +0.06 em | 1.4 |
| Large numeral | ordinals 01–06 in the centre, the year 2021 | 40 ExtraBold | 1.0 | 40 Bold (IBM Plex Sans; shared numerals are always Latin-font Western digits) | 1.0 |
| Folio | page number | 9 Medium | | 9 Medium | |

Rules: no tracking on Arabic, ever. No italics, no faux bold, no all-caps effect on Arabic. Latin caps only at label level. Western numerals everywhere. Page titles may run to two lines; they never shrink to fit. At most three type levels on one page besides the header and folio. Arabic text is ragged-left (right-aligned), not justified; English ragged-right. No hyphenation in either language. Minimum size anywhere: 8.5 pt Latin, 9.5 pt Arabic.

### 2.5 Colour proportions

Across the whole document, by area (tolerance ± 3 points):

| Colour | Share | Where |
|---|---|---|
| White `#FFFFFF` | about 62% | Ground of pp1, 3–6, 8–13, 15–17 |
| Light tint `#F7F8FC` | about 14% | Ground of pp2, 14, 18, 19 |
| Navy-to-royal-blue gradient | about 16% | Full pages 7 and 20; centre panels on pp9, 10, 13; one diamond on the cover |
| Photographs | about 6% | Six photographs plus the cover diamond |
| Green `#5AC584` | under 2% | Markers, bullets, one small cover diamond, short rules. Never text on white or tint; never white text on green |
| Periwinkle `#9BABD7` | under 1% | Sparkles and hairlines only |

Rhythm: no two full-gradient pages are adjacent. Text is Navy or grey on light grounds and white on the gradient. On the gradient, green appears only as a shape, and only on the dark (left) half. Hairlines: 0.25 pt Periwinkle on light grounds; 0.25 pt white at 35% opacity on the gradient.

### 2.6 Where the brand shapes may appear — and nowhere else

**Rounded diamond** (square turned 45 degrees, corner radius 16% of the side):

| Use | Size | Pages |
|---|---|---|
| Large, as image mask and colour shape | see cover spec, 2.9 | **p1 only** |
| Icon holder, outline 0.75 pt | bounding box 18 × 18 | p7 only (six holders, in the centre) |
| Bullet, solid green | bounding box 2.2 × 2.2 | every list, pp3–17 and p20 |

No half-hidden diamonds entering from page edges, no diamond overlays on photographs, no diamond behind text, on any page other than the cover.

**45-degree cut (chamfer):** one corner only — the bottom-right corner — of the centre panel on service pages 8–13, leg 27.5 (the diagonal runs from (190, 131) to (162.5, 158.5)). Straight, not rounded. Used on both photograph panels and gradient panels. Not used on project photographs, partner tiles or text boxes.

**Four-point sparkle** (concave four-point star, traced from the logo badge):

| Use | Size | Pages |
|---|---|---|
| Section marker in the running header, one sparkle, green | 2.4 | every inside page |
| Band: 3 rows on a 5 mm pitch, each sparkle 2 mm, Periwinkle on light grounds, white at 30% opacity on the gradient | 3 rows × 7 to 16 sparkles | **at most one band per spread**, only at: p1 (under the lockup), p4 (pair 4–5), inside the gradient panels of pp9, 10, 13, and p20 |

Never a full-page texture, never under text, never on a photograph, never on the partner pages.

**Pill** (fully rounded bar): draft markers and scope chips on project pages only, height 6.5.

### 2.7 Running header, folio, section marker

Present on pp2–19. Absent on p1 and p20.

- **Header, y 12–16.** Right end (x 278, right-aligned): green sparkle 2.4, then the section number and the Arabic section name, Label 9.5 Medium, Navy. Left end (x 19, left-aligned): the English section name, Label 8.5 caps, grey. Hairline across x 19–278 at y 19.
- **Section numbers** follow the contents page: 01 About Us (p3), 02 Vision, Mission and Goals (pp4–6), 03 Our Services (pp7–13), 04 Why OTLOBNY Emaar (p14), 05 Our Work (pp15–17), 06 Partners (pp18–19), 07 Contact (p20). Page 2 carries the header without a number.
- **Folio, baseline y 198.** Two digits (02 … 19), Folio 9 Medium, Navy. On the outer corner: even pages at x 278 (right), odd pages at x 19 (left). In the opposite corner, in Label style, the document name in the language of that side (Arabic on the right, English on the left); strings from the content outline's cover lines.
- **No logo on inside pages.** The wordmark's minimum size is 10 mm; repeated 18 times it becomes noise, and the name is still awaiting confirmation. The logo appears on p1, p7 and p20 only.
- On gradient pages (p7) header and folio are white; the hairline is white at 35%.
- **Draft marker.** Any page carrying content tagged [D] or TBC in the outline (p13 in full; website lines; the name) shows a pill in the footer centre, x 148.5: outline 0.5 pt, Label style, "DRAFT — to be confirmed" with its Arabic equivalent from the content team. It is removed only when the client confirms.

### 2.8 Divider pages

Twenty pages leave no room for stand-alone dividers, and none is added: an empty divider is padding. Instead:

- **p7 is the one full divider.** It opens the largest section (seven pages) and doubles as the services overview. Template T5.
- Every other section opens on a normal page; the section change is signalled by the header marker and number alone.
- If the client later supplies enough content for 24 pages, extra dividers use T5 without the six rows: gradient ground, Section title in both languages on R3, the section number as a Large numeral in the centre, one sparkle band (3 × 12, white 30%, x 19–78, y 176–188).

### 2.9 Templates

**T1 Cover (p1).** White ground.
- Lockup, colour version, height 42 (width 99.4), right edge at x 278, top at y 26. Clear space as in `system.md`.
- Diamond cascade on the left, three diamonds on one 45-degree line running down from the top-left, centres and bounding boxes: **D1** gradient fill, box 100, centre (20, 20), bleeding off the top-left corner; **D2** photograph (image plan no. 1), box 110, centre (95, 85); **D3** solid green, box 18, centre (160, 150).
- Sparkle band: 3 × 12, Periwinkle, x 219–278, y 76–88.
- Bottom band, bilingual: Arabic document title, Cover title 46, Navy, right-aligned at x 278, baseline y 168; English document title, Cover title 38, Royal blue, left-aligned at x 19, same baseline. Activity line (optional in the outline; **keep it**, it is the only place the six fields are named on the cover): Label style, Arabic right, English left, baseline y 184; each language has a half-width of 127; if either wraps to a second line, drop the line on both sides.
- No contact details, no year, no tagline.

**T2 Contents (p2).** Light tint ground. Title in Section title size in R1 (Arabic K1–K5, English K8–K12). Seven rows from y 56, pitch 18, hairline above each row across x 19–278: Arabic entry (Heading 20, right) | page number in the centre at x 148.5 (IBM Plex Sans Bold 26, Royal blue) | English entry (Heading 17, left). Entries and page numbers from the outline, with the corrections in section 3.

**T3 Statement (pp3, 4, 5).** White ground. Page title in R1. Arabic K1–K5, English K8–K12, a vertical hairline at x 148.5 from y 53.5 to y 158.5.
- pp4–5 (vision, mission): the single sentence set in Heading 20 Bold / 17 SemiBold with the longer line heights, starting at y 58. Nothing else on the page except, on p4, one sparkle band 3 × 7 centred on x 148.5 at y 166–178. The two pages are identical in structure so they read as a pair.
- p3 (about): the paragraph in Lead, R2–R3. Fact table in R4–R6 (see 2.10).

**T4 Numbered list (pp6, 14).** Arabic K1–K5, centre K6–K7, English K8–K12. Page title in R1. Hairline above each row across x 19–278.
- p6 (four goals): rows start at y 56, pitch 31. Centre: ordinal 01–04, Large numeral 40, Royal blue. Text in Lead, top-aligned with the numeral's top.
- p14 (six points): Light tint ground; rows start at y 51, pitch 22.5. Centre: ordinal 01–06, IBM Plex Sans Bold 26, Royal blue. Point title in Lead Bold / SemiBold (line height 1.5), description in Body, two lines at most.

**T5 Divider and services overview (p7).** Full-bleed brand gradient (dark on the left, as in the tokens). White text.
- R1: Arabic title, Section title 32, K1–K5; English, 27, K8–K12. White wordmark (not the lockup), height 12, centred on x 148.5, y 28–40.
- Six rows from y 54, pitch 22: Arabic service name (Heading 20) with its one-line description (Body) on the right | centre: diamond holder 18 × 18, 0.75 pt white outline, with the service's line icon in white and, beneath the holder, the page number of that service (Label, white) | English name (Heading 17) and line (Body) on the left. Hairlines white at 35%.
- No sparkle band on this page: the six rows fill the live area to y 186.
- **Icons:** six, one per service, one style: line only, 1.5 pt stroke at 12 mm, rounded caps and joins, ends cut at 45 degrees where a stroke terminates freely, drawn on a 24-unit grid. Either drawn for this document or taken from one openly licensed set (MIT / ISC / Apache), with the set and licence recorded in `04-identity/licences.md`. The original's solid glyphs are of unknown source and are not reused.

**T6 Service page (pp8–13).** White ground. A triptych.
- **Arabic block K1–K4** (x 195–278): in R1, the ordinal line in Label style (section name and "0n / 06"), then the Page title 26. From y 53.5: intro sentence in Lead 14. Then 6 mm space. Then the sub-service list: Body 11.5 Medium, one item per row, row pitch 10, hairline above each, green diamond bullet 2.2 on the right. Where the outline gives a second sentence (p12, the Ajeer contract line), it follows the list after 6 mm, in Body, with «أجير» in guillemets and no logo.
- **English block K9–K12** (x 19–102): the same, mirrored, in the Latin sizes; bullets on the left.
- **Centre panel K5–K8:** x 107–190, y 26–158.5 (83 × 132.5), bottom-right corner chamfered. Either **T6-P**, a photograph in the blue duotone (section 4), or **T6-G**, a graphic panel (below). Under the panel, on the R6 top line (baseline y 169), for T6-P only: the caption "illustrative image" in both languages, Label style, Arabic right-aligned at x 190 and English left-aligned at x 107. Wording from the content team.
- **T6-G graphic panel:** the brand gradient filling the panel; the service's icon from p7 enlarged to 46 × 46, white, stroke scaled with it, centred at (148.5, 84); sparkle band 3 × 7, white 30%, x 113–145, y 140–152. No photograph, no ordinal, no text.
- The six pages alternate so every spread has one photograph and one graphic panel: 8 P · 9 G | 10 G · 11 P | 12 P · 13 G.

**T7 Project page (pp15–17).** White ground. A triptych, but the evidence is treated differently from the illustrative photographs.
- R1: section name as Page title (Arabic K1–K4, English K9–K12) with the ordinal line "0n / 03" above it in Label style.
- **Centre frame K5–K8:** x 107–190, y 53.5–128.5 (83 × 75). The photograph in **full colour**, no duotone, no chamfer, no rounded corners, no overlay. Square corners and true colour say "this is the real thing".
- **Arabic block K1–K4** from y 53.5: project name in Heading 20; 4 mm; the sentence in Body. **English block K9–K12** the same.
- **Scope chips**, top at y 136: one pill per service named in that project's sentence and no other (p15: design, installation; p16: operation, maintenance, cleaning; p17: maintenance, cleaning). Pill height 6.5, outline 0.5 pt Royal blue, Label text Navy; Arabic chips right-aligned at x 278 flowing leftwards, English chips left-aligned at x 19.
- **Project index** in R6, top at y 168, hairline above across x 19–278: the three project names in Label style in three equal cells (K1–K4, K5–K8, K9–K12, order right to left on the Arabic line; the English line beneath runs left to right in its own row). The current project in Navy Bold with a green diamond bullet; the other two in grey.
- Fields the client has not supplied (client, location, year, quantity, contract value) are **not shown and not left as empty labels**.
- If the client supplies originals at least 1,750 px wide, the frame may grow to K4–K9 (127 × 86) on all three pages together, never on one alone.

**T8 Partners (pp18–19).** Section 5.

**T9 Contact and back cover (p20).** Full-bleed brand gradient. No header, no folio.
- Lockup, white version, height 34 (width 80.4), centred on x 148.5, y 34–68.
- Rows from y 92, pitch 14, hairlines white 35% across x 60–237: Arabic label (Label, right-aligned at x 237) | value in the centre (IBM Plex Sans Medium 17, white, centred on x 148.5) | English label (Label, left-aligned at x 60). Rows: phone, email, website, commercial registration. The website row appears only once the client has named the domain; in drafts it shows the draft pill instead of a value.
- Address row beneath, top at y 152: Arabic address right (K2–K5, Body, white), English address left (K8–K11), a green diamond bullet in the centre.
- Sparkle band: 3 × 12, white 30%, x 19–78, y 180–192.
- No map and no QR code until the address and domain are confirmed.

### 2.10 Showing facts without inventing numbers

- The only numerals the client's material supports are **2021**, **4650245200**, **2030** (inside the vision sentence) and the phone number. Only 2021 may be set as a Large numeral. Ordinals (01–06) and page numbers are navigation, not statistics, and are the only other large figures.
- **Fact table on p3** (R4–R6, four rows, pitch 18 from y 110, hairline above each): Arabic label and value on the right (label in Label style, value in Heading 20) | centre | English label and value on the left. The centre holds the value when it is a number shared by both languages (2021 as a Large numeral; the CR number in IBM Plex Sans Bold 20) and a green diamond bullet when it is not. For the two numeric rows the value is shown once, in the centre, and not repeated in the side blocks.
- No counters, percentage rings, bar charts, maps with pins, timelines, "+" figures, star ratings, certificate badges or award seals: there is no data behind any of them.
- A missing fact is omitted, never shown as a blank field, a dash or "TBC" in a version presented as final. Unconfirmed content carries the draft pill (2.7).
- Photographs that are not the client's own work carry the "illustrative image" caption.

---

## 3. Page-by-page plan

Page numbers and content follow `content-outline.md` for pages 1–17. Two deviations, both forced by the client's later instructions, are marked **CHANGE** and need the Creative Director's decision (see handoff).

| Page | Content (outline) | Template | Ground | Centre element |
|---|---|---|---|---|
| 1 | Cover | T1 | White | Lockup, diamond cascade with photo no. 1 |
| 2 | Contents | T2 | Light tint | Page numbers |
| 3 | About Us | T3 + fact table | White | 2021, CR number |
| 4 | Our Vision | T3 statement | White | Hairline, sparkle band |
| 5 | Our Mission | T3 statement | White | Hairline |
| 6 | Our Goals | T4, four rows | White | Ordinals 01–04 |
| 7 | Our Services (overview) | T5 divider | Gradient | Six icon holders |
| 8 | General Contracting | T6-P | White | Photo no. 2 |
| 9 | Landscaping | T6-G | White | Gradient panel, landscaping icon |
| 10 | Maintenance | T6-G | White | Gradient panel, maintenance icon |
| 11 | Cleaning | T6-P | White | Photo no. 3 |
| 12 | Manpower Supply | T6-P (falls back to T6-G) | White | Photo no. 4, conditional |
| 13 | Logistics Services — all draft | T6-G + draft pill | White | Gradient panel, logistics icon |
| 14 | Why OTLOBNY Emaar | T4, six rows | Light tint | Ordinals 01–06 |
| 15 | Our Work: bus waiting shelters | T7 | White | Photo no. 5 |
| 16 | Our Work: Madinah Chamber | T7 | White | Photo no. 6 |
| 17 | Our Work: Shahd Al Madinah Hotel | T7 | White | Photo no. 7 |
| 18 | Partners, first page — **CHANGE** | T8 | Light tint | Title block + 12 logos |
| 19 | Partners, second page — **CHANGE** | T8 | Light tint | 15 logos |
| 20 | Contact and back cover, merged — **CHANGE** | T9 | Gradient | Lockup, contact rows |

**CHANGE 1 — partners take two pages (18–19); contact merges into the back cover (20).** The outline gives the partners one page (18) and the contact its own page (19). The client has since confirmed 27 logos. On one page that means tiles about 33 mm wide with marks about 24 mm, most of them from 106 ppi sources: the weakest page in the document, at the point where a buyer looks for names they know. Pages 18–19 are a true facing spread, and the contact details (four short lines and an address) sit naturally on the back cover. Nothing in the outline's page 19 is lost. The contents page entry for Contact becomes 20.
*Fallback if the Creative Director keeps a separate contact page:* partners on p18 alone, 7 columns × 4 rows, tiles 33.5 × 28, gap 4, logo box 24 × 16, grid top at y 56, Page title in R1; the 28th cell stays empty with no tile. Not recommended.

**CHANGE 2 — the section title.** The outline titles the page «عملاؤنا وشركاؤنا» / "Clients and Partners"; the brief's later addenda record the client's title as «شركاء النجاح». The layout uses the client's title. The English equivalent and the matching contents entry are the content team's to write.

---

## 4. Image plan

### 4.1 Rules that apply to every image

- **Resolution floor: 150 dpi at placed size. No upscaling.** Maximum printed size = pixels ÷ 150 × 25.4.
- **Two treatments only.** *Duotone* for illustrative photographs: convert to greyscale, raise contrast about 10%, apply a gradient map — shadows Navy `#1F3162`, midpoint Royal blue `#3758B0` at 55%, highlights White. *Full colour, untouched* for the client's own work (pp15–17). Never mix: a duotone project photo or a colour stock photo breaks the code that tells the reader which is which.
- No image is flipped, stretched, extended with generated pixels, or retouched beyond the crop and the treatment.
- **Licences.** Every photograph taken from the old profile has an unknown licence (`04-identity/licences.md`). They may be used in drafts. Before a version is released as final the client must confirm the right to use each, or the page switches to its fallback, which is given for every image below.
- Crops below were checked by eye at reduced size (`06-profiles/_work/art-direction_crop-check_v01.png`). They are accurate to about ± 0.02; the designer checks each at 100% and adjusts within that tolerance only.

### 4.2 Images used

Source folder for nos. 1–3 and 5–7: `clients/otlobny-emaar/01-brief/assets-received/pdf-images/` (extracted from the client's PDF).

| No. | Page | File | Source px | Max printed width × height at 150 dpi | Crop (l, t, r, b) | Crop px | Placed size | Effective dpi | Treatment | Fallback |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1, diamond D2 | `img-004.png` | 1237 × 876 | 209 × 148 | (0.45, 0.00, 0.98, 0.75) | 655 × 657 | diamond, bounding box 110 × 110 | 151 | Duotone; masked by the rounded diamond. The crop is the glass facade with **no rope-access workers** in it (they sit outside the crop; rope access is not a listed service) | D2 becomes a Royal blue solid diamond; the cover is then purely graphic |
| 2 | 8 | `img-028.png` | 1240 × 873 | 210 × 148 | (0.17, 0.00, 0.611, 1.00) | 547 × 873 | 83 × 132.5 | 167 | Duotone; chamfer. Hands and distribution board; the face is outside the crop. Fits "electrical works", a listed sub-service of contracting — which is why it moves here from the maintenance page | T6-G with the contracting icon |
| 3 | 11 | `img-006.png` | 1623 × 873 | 275 × 148 | (0.63, 0.00, 0.967, 1.00) | 547 × 873 | 83 × 132.5 | 167 | Duotone; chamfer. Cleaner wiping glass | T6-G with the cleaning icon |
| 4 | 12 | `clients/otlobny-emaar/_originals/mockup_cleaning-team.png` (work on a copy in `06-profiles/assets/mockups/`) | 1536 × 1024 | 260 × 173 | (0.385, 0.04, 0.719, 0.84) | 513 × 819 | 83 × 132.5 | 157 | Duotone; chamfer. Two team members. **Conditional**, see 4.3 | T6-G with the manpower icon |
| 5 | 15 | `img-043.png` | 950 × 471 | 161 × 80 | (0.44, 0.00, 0.989, 1.00) | 522 × 471 | 83 × 75 | 160 | Full colour, square frame. The crop starts right of the debris lying on the pavement at about x 0.33–0.40 of the source; check at 100% that none of it is inside the frame | None needed for drafts; ask the client for the original photograph |
| 6 | 16 | `img-044.png` (identical to `img-046.png`) | 644 × 454 | 109 × 77 | (0.21, 0.00, 0.99, 1.00) | 503 × 454 | 83 × 75 | 154 | Full colour, square frame. This is the smallest source in the plan and sets the size of all three project frames. It appears to be an architectural rendering, not a photograph, and its owner is unknown | A light-tint frame of the same size holding the project name in Heading, both languages; no image |
| 7 | 17 | `img-045.png` | 1055 × 743 | 179 × 126 | (0.20, 0.00, 0.979, 1.00) | 822 × 743 | 83 × 75 | 251 | Full colour, square frame. Hotel with the Prophet's Mosque minarets behind: the only image in the set that shows Madinah | Same fallback as no. 6 |

No other raster image appears anywhere in the profile except the partner logos (section 5).

### 4.3 The four mockups in `_originals/`

They look AI-generated; their small lettering is garbled, their Latin reads "OTLOBIY" and "OTLOBY", they carry the old activity names, and their logos are wrong drawings of the wordmark. Verdict per file:

| File | Verdict | Reason |
|---|---|---|
| `mockup_cleaning-team.png` | **One crop allowed** (image no. 4), conditional | Inside the crop the only lettering is the chest logos, about 8 mm wide on the page, with a descriptor under 0.5 mm high: not legible at printed size (checked at true size in `_work/crop-check_team-and-cleaning_true-size.png`), and the duotone removes the colour error. The trolley with the garbled line (x above 0.80) is outside the crop. Do not widen the crop to the right |
| `mockup_delivery-rider.png` | **Not used** | The bag and jacket carry the garbled descriptor; a crop that avoids both is under 300 px wide (47 mm) |
| `mockup_car-scooter-facade.png` | **Not used** | "OTLOBIY Maintenance & Cleaning Co." on the facade, car and box; the banner text; no crop of useful size is free of them |
| `mockup_logistics-trucks.png` | **Not used** | "OTLOBY Logistics Services Co." is legible on every box face at any useful size; the top-left panel shows a Riyadh landmark, and the company is in Madinah |

Conditions on image no. 4: (a) the client answers the brief's open question 5 and agrees to the image being used; (b) it carries the "illustrative image" caption like every other non-project photograph. It shows generated people, not the company's staff, and must never be captioned or described as the team. If either condition fails, p12 uses T6-G, and the alternation in T6 becomes 8 P · 9 G | 10 G · 11 P | 12 G · 13 G, which is acceptable.

### 4.4 Pages with no acceptable image — the graphic solution

| Page | Why no photograph | Solution |
|---|---|---|
| 9 Landscaping | The only image (`img-021.png`) shows a greenhouse nursery; the service is parks, street trees, gardens and irrigation | T6-G, landscaping icon |
| 10 Maintenance | No image of air-conditioning plant or lifts exists in the material; the electrical-panel image belongs to contracting and is used there | T6-G, maintenance icon |
| 13 Logistics | No real fleet photograph exists; every mockup fails (4.3); the whole page is unconfirmed draft and showing vehicles would imply a fleet nobody has evidenced | T6-G, logistics icon, plus the draft pill |
| 3 About, 4 Vision, 5 Mission | No photograph of the company itself or licensed image of Madinah | Typographic (T3) |
| 6, 14 | None needed | Typographic (T4) |

A gradient panel with a well-drawn icon is honest and looks deliberate. A mismatched stock photograph does neither.

### 4.5 Images in the old profile that are not used, and why

| File(s) | Shows | Reason |
|---|---|---|
| `img-011.png`, `img-014.png` | Riyadh skyline (Kingdom Centre) | Wrong city; unknown licence |
| `img-015.png`, `img-016.png` | Vision 2030 logo | **Not reproduced.** The reference stays in the vision sentence only |
| `img-047.png`, `img-048.png` (p14) | Ajeer logo | Not reproduced; the word appears in guillemets in text |
| `img-000`, `012`, `013`, `022`, `023`, `032` | Rebar worker | 412 × 401 px: 70 mm wide at most, 126 dpi in the 83 mm panel |
| `img-021.png` and copies | Greenhouse nursery | Does not match the service |
| `img-029.png`, `img-037.png` | Stock waiter | Generic stock portrait flagged in the outline; p12 has a better-matched candidate |
| `img-030.png` and copies | Pest control with insects on the floor | Unpleasant at any size; one image per service page |
| `img-041.png`, the rest of `img-004.png` | Rope-access window cleaners | Not a listed service |
| `img-002.png`, `img-003.png` | Cable patch panel; cleaners' legs | Not on any page of the outline; small |

---

## 5. Partners — «شركاء النجاح» (pp18–19)

**Sources, and nothing else:**
- Existing 18: cropped from page 19 of `_originals/otlobny_company-profile_original_2026-11-13.pdf`, into `06-profiles/assets/partners/`.
- New nine: `_originals/partner-logos-client_2026-11-13/` (01–09), black bars and outer margins cropped, into the same folder.
- **`_originals/partner-logos_2026-11-13/` is the REJECTED set. Never open it for artwork, never place anything from it.** `01-brief/assets-received/partner-logos_contact-sheet.png` may derive from that set; do not use it as a reference either.
- No logo is redrawn, traced, recoloured, converted to one colour, inverted or given an effect.

**Grid (one spread, one sub-grid of five).** Both pages: Light tint ground, normal header and folio, no page title in R1.

| | |
|---|---|
| Columns | 5 tiles of 47, gap 6 (5 × 47 + 4 × 6 = 259). Left edges at x 19, 72, 125, 178, 231 |
| Rows | 3 tiles of 40, gap 6. Tops at y 40, 86, 132; grid ends at y 172 |
| Cells | 30 over the two pages = 27 logos + a title block of 3 cells |
| Title block | p18, row 1, the three right-hand cells (x 125–278, y 40–80). No tile behind it. Arabic title, Section title 32, Navy, right-aligned at x 278; English title, 27, Royal blue, left-aligned at x 125; both sitting on the block's bottom line (baseline y 76). Green sparkle marker 2.4 at the top-right of the block |
| Note line | p19 only, baseline y 182: one line in Label style stating that the logos belong to their owners; Arabic right-aligned at x 278, English left-aligned at x 19. Wording from the content team |

**Uniform tile.**

- 47 × 40, corner radius 3, white fill, hairline 0.35 pt Periwinkle `#9BABD7` at 45% opacity, no shadow.
- **Logo box 31 × 20, centred in the tile** (8 clear at each side, 10 above and below). Each logo is scaled to fit inside the box, whichever limit it meets first.
- **Optical levelling:** compact or tall marks (emblems, badges, roundels) use the full 20 height; wide wordmarks use the full 31 width; nothing is enlarged past the box to "match".
- **Resolution cap for the existing 18:** the raster logos on the old page are embedded at 106 ppi, so each may be placed at no more than **70% of the size it has on the old page 19**. If the box would allow more, the cap wins. Those that are vector in the old PDF have no cap. Crop them from a render of at least 600 dpi so the vector ones stay sharp.
- **Coloured-ground logos keep their own ground, filling the tile edge to edge.** Keeta: the tile is a 47:40 crop of the supplied yellow image itself, the mark scaled to the 31 × 20 box. ZERO: the same with the supplied dark charcoal image. Same radius, same hairline. No synthetic colour is added: the ground is the client's own pixels, and both files have enough ground for the crop. Neither is inverted or placed on white.
- Logos supplied on white sit directly on the white tile. HungerStation's yellow badge is part of the mark and sits on white.
- Off-white haze or a pale panel around an existing logo (Cooperative Taibah's sits on a pale grey panel): crop inside it as tightly as the mark's clear space allows and leave what remains; do not erase or paint the ground by hand.
- No names under the logos. Give every logo alternative text in the PDF with the owner's name where it is known.

**Order: the existing 18 first, in the client's own published order, then the nine.** Reasons:

1. The client's instruction is that the 18 stay "unchanged". The order in which the client published them is the only order the client has approved, and it already opens with the regional bodies.
2. Five of the 18 cannot yet be named with certainty and nobody has said which party is a client and which a partner. Sorting by sector would mean classifying organisations on evidence we do not have, and unlabelled groups would imply relationships the client has not stated.
3. The grid hides the seam. The 18 end and the nine begin in the middle of a row on p19, so the new names read as part of one family, not as an appendix.

Within the nine, the order is by kind where the logo itself states the kind (hotels, then the festival, then delivery platforms, then the other two), arranged so the two coloured tiles close the last row as bookends.

Reading order is right to left, top to bottom. Existing logos E1–E18 are numbered by their position on the old page 19, read right to left, row by row. Described by what the logo shows where the owner is not confirmed:

| Page | Row | Cell 1 (right) | Cell 2 | Cell 3 | Cell 4 | Cell 5 (left) |
|---|---|---|---|---|---|---|
| 18 | 1 | title block | title block | title block | E1 green-dome emblem (owner to be named by the client) | E2 Al Madinah Region Development Authority |
| 18 | 2 | E3 Al Maqar | E4 "AR / Spa" geometric mark (to be named) | E5 Mawaddah | E6 Imagine More Travel Agency | E7 round "HSH" mark (to be named) |
| 18 | 3 | E8 Cooperative Taibah | E9 Dar Al Taqwa Hotel | E10 Dallah Taibah Hotel | E11 Al Madinah Harmony | E12 Tiny House |
| 19 | 1 | E13 Platinum | E14 Almadinah Almunawarah Chamber | E15 brown column emblem (to be named) | E16 Hippo | E17 Taza |
| 19 | 2 | E18 black calligraphic mark with ® (to be named) | N1 Manazil Al-Mukhtara Company | N2 Novotel Hotels & Resorts | N3 Rotana | N4 International Medina Festival Dates |
| 19 | 3 | N5 Keeta (yellow tile) | N6 Jahez | N7 HungerStation | N8 Chop & Co | N9 ZERO (charcoal tile) |

Count check before handing over: 12 logos on p18, 15 on p19, 27 in all; 18 from the old page, 9 from the client folder; none from the rejected folder.

Quality note for the handoff: the nine are JPEG screen captures and thirteen of the 18 are 106 ppi rasters. At these sizes they hold in a screen PDF. Print needs vector files from the owners, and permission to show each logo is the client's responsibility (brief, addendum 2).

---

## 6. International standard: five requirements and five prohibitions

### Required

1. **One grid, provably.** Every text block, image, panel and tile sits on the column and row lines of 2.2. Deliver `_work/` previews of pp3, 8, 15 and 18 with the grid overlaid, and identical positions for header, title zone and folio on every inside page (differences of 0 mm, not "about").
2. **Real bilingual parity.** Arabic right, English left, in the same zones on all 20 pages; Arabic set first and 12–15% larger; paired rows aligned; right-to-left pagination and binding set in the PDF; every point of `.claude/rules/arabic-design.md` met; `scripts/check_arabic_pdf.py` reports PASS with Tajawal and IBM Plex Sans named and no fallback font, and the previews are opened and read.
3. **Evidence is told apart from illustration.** Client work in full colour in square frames; everything else in duotone with the "illustrative image" caption; no image under 150 dpi at placed size; no number, chart or badge without a source in the outline.
4. **Accessible and technically clean.** Every text pair at WCAG AA or better using only the pairs marked "pass" in `system.md`; static fonts embedded by name; a tagged PDF with bookmarks for the seven sections, document title and language set, alternative text on images and logos; sRGB; file naming per `.claude/rules/file-delivery.md`; the PDF opened in a second viewer.
5. **Typographic finish and restraint.** No widows, orphans or single-word last lines in either language; no title shrunk or squeezed to fit; at most three type levels per page; Western numerals and Arabic punctuation (، ؛ ؟ «») throughout; consistent hairline weights; at least half of every white-ground page left empty; brand shapes only where 2.6 allows them.

### Forbidden

1. **Any garbled, misspelt or wrong-name lettering**, at any size at which it can be read: the four mockups outside the single crop in 4.3, the old descriptor «للصيانة والنظافة», "OTLOBIY", "OTLOBY", "Mantinance".
2. **Borrowed or misleading marks and places:** the Vision 2030 logo, the Ajeer logo, the Riyadh skyline or the truck panel with the Riyadh landmark, anything from the rejected partner folder, any partner logo redrawn, recoloured, greyed, inverted or re-ordered against section 5.
3. **Invented or inflated content:** figures, counters, charts, maps, certificates, awards, staff or fleet numbers, "leading" or "chosen" claims, generated people presented as the company's team, placeholder text or lorem ipsum, and any [D] or TBC item shown without its draft pill.
4. **Upscaled, stretched or effect-laden artwork:** images below 150 dpi, drop shadows, glows, bevels, gradient or outlined text, photo collages, diamond overlays on photographs, full-page sparkle textures, more than one large device on a page.
5. **Typographic and logo misuse:** letter-spacing on Arabic, faux bold or italic, justified Arabic with stretched gaps, line-by-line interleaving of the two languages, the all-green wordmark or any green text on white, the blue wordmark on navy, white text on green, the logo on every page, the name retyped beside the wordmark as a substitute logo.

---

## Open points carried by this document

1. Partners over two pages with the contact merged into p20 (CHANGE 1): Creative Director to decide; fallback specified.
2. The partners title and its English form; the "illustrative image" caption, the draft pill wording and the ownership note on p19: content team to write.
3. Image no. 4 depends on the client's answer about the mockups.
4. Licences of images nos. 1–3 and 6–7 are unknown; each has a fallback.
5. The lockup on p1 and p20 is still a proposal with an assumed name; because the logo is on three pages only and the name elsewhere is live text, a change of name costs three placements.
6. Five existing partner logos are unnamed; this affects alternative text only, not the layout.
7. No approved strategy exists in `03-strategy/`; this direction rests on the brief and the captured identity.
