# Panel review: art direction. Company profile v09 (screen, ar-en), 2026-11-14

**Reviewer:** art-director (panel seat: visual level). The quality-reviewer covers the technical ten-point check, and the brand-strategist covers copy and facts. I have not repeated their work.
**File:** `06-profiles/otlobny-emaar_company-profile_screen_ar-en_v09.pdf` (20 pages).

**What I looked at:**
- every page in `_work/preview_v09/`;
- the whole PDF re-rendered at 200 dpi, with crops of p1, p2, p12 and p17;
- the embedded image list (`pdfimages -list`, which gives the effective ppi of each image);
- the v09 HTML for pages 11, 16 and 17;
- `brand-context.md`, `system.md` §1a, `assets/stock/README.md`, `build-notes_v09.md` and `review_v08_r5.md`;
- the client's original 20 pages (`01-brief/assets-received/pages/`).

**Client's bar:** world-class, «متعة بصرية» (visual delight), not «مشي حالك». The cover should be one large image with several small ones, and the images should be chosen with care.

---

## Verdict

**v09 is clean, orderly and credible.** On order, bilingual typography, legibility and honesty it is far ahead of the original. p12 (the fleet) is now a genuinely strong commercial page.

**It is not yet visual delight, for three reasons:**
- **Pacing.** From p6 to p18 there are 13 light pages in a row with no dark beat. The original, for all its faults, was immersive: its dark, image-led service pages had a mood that v09 has traded for tidiness.
- **Photography.** Images are small, low-resolution stock, and their colour does not hang together. This shows most on the cover, which is the page the client judges first.
- **The ending.** The last page is a page of photo credits.

**Would I put my name to it?** Yes, as a reviewed draft for the client, **once the five must-fixes below are done.** All five use existing assets; I estimate half a day of work.

**Would I call it world-class?** No. After the top-five (A) changes it reaches a strong regional standard. The remaining gap is photography of the company's own people, sites and works, and only the client can supply that (B).

---

## Must-fix before the client sees it

- **MF1. p2: the lockup has no clear space.** The diamond lattice lines run through the reversed lockup, behind the wordmark and both descriptor lines (crop at 200 dpi, bottom left). This breaks `system.md` §1a clear space.
  - Knock the lattice out of a clear zone: the lockup's bounds plus X on every side (X = alef width = 6.9% of the lockup width, about 4 mm at 58 mm).
  - Fill that zone with solid navy `#1F3162`.
- **MF2. p1 cover: give the images one treatment.** Right now the cover reads as five unrelated stock photos: orange racking, hi-vis yellow, red rope bags, a warm park and rust-brown steel.
  - Put the **four small tiles in one navy-to-royal duotone** (`#1F3162` → `#3758B0`, 100%; the stock README already allows this, "all tiles, never a mix").
  - Keep the **hero (steel erector) in colour** with the README grade.
  - This gives the client exactly what he asked for: one large image and several small, read as one set, in the spirit of his old cover (which unified its images in greyscale and blue).
- **MF3. p16: put it on the works master.** The title is set smaller than on p14 and p15 (HTML classes `flow sm` and `t1 st tw`). The tinted image panel is also a different width on each works page (about 142, 140 and 172 mm). Specifically:
  - set p16's Arabic and English titles at the same size as p14 and p15;
  - use one panel width on all three pages: 142 mm on p14 and p16, mirrored on p15;
  - start every photo at the same top line.
- **MF4. p20: make it a real back cover.** The book currently closes on a block of attribution small print, which is the last impression the client takes away.
  - **Top 62%:** the navy-to-royal gradient (`system.md` §2), with the **reversed** lockup v02 centred at 90 mm, and `otlobny.net` · «المدينة المنورة» in white beneath it.
  - **Bottom 38%:** a white band holding the credits exactly as they are now.
  - This keeps the attributions the licences require without letting them be the ending.
- **MF5. Pacing: add a dark beat in the middle.** **p13 «لماذا اطلبني إعمار» goes onto the navy gradient**, using the same treatment as p5 «أهدافنا»:
  - white titles;
  - green numerals;
  - periwinkle `#9BABD7` for secondary text (5.5:1 on navy);
  - hairlines at 25% white.

  It is a text-only page, so this is a style change only. It breaks the run of 13 light pages exactly where the book turns from services to proof.

---

## Page by page

| Page | What works | Weakness and location | Direction |
|---|---|---|---|
| **p1 Cover** | The lockup at 86 mm is dominant and correctly placed top left. The collage structure matches the client's request. The hero (1536 px, 202 ppi) is sharp. | (1) Colour chaos across the tiles (MF2). (2) The floating green diamond (left of the collage, about 40% down) is a stray accent that belongs to nothing. (3) The name appears three times in the left column: in both descriptor lines, then in the kicker «اطلبني إعمار» / "OTLOBNY EMAR". (4) There is a dead gap of about 60 mm between the lockup and the title. | Apply MF2. Move the green diamond so its edge aligns with the collage gap, or delete it. Remove the name kicker; if the strategist wants a line there, use a services strap instead (copy is theirs). Move the title block up to two grid rows below the lockup. |
| **p2 Contents** | Clean contents table, a strong two-panel split, and a well-sized lockup (58 mm). | Lattice through the lockup (MF1). The three filled diamonds scattered in the lattice read as random. | MF1. Keep only one filled green diamond, on the diagonal that leads to the lockup. |
| **p3 About** | The Madinah plaza photo is the right regional anchor (300 ppi). The fact table is excellent. | The lower 45% of the photo is empty marble floor, so the umbrellas and minarets (the subject) sit in the top half. | Re-derive from the 3600 × 2700 source at about 118% scale, anchored to the top centre. That still gives about 250 ppi, which is fine on screen. Do not cut the minaret tops. |
| **p4 Vision** | The Arabic vision statement in large bold type is the right hierarchy. | The pattern band is attractive but purely decorative. | Acceptable as is. |
| **p5 Goals** | A good dark page: generous, with green numerals. | None. | Keep, and use it as the model for p13 (MF5). |
| **p6 Services overview** | The six-field grid is clear, and page references make it useful. | The band image is the underside of a beige umbrella against a flat grey sky, and the dome is amputated by the band's bottom edge. It is the weakest photo in the book, and the second Haram image in four pages. | Re-crop to the umbrella crown and the two minarets with the dome whole or out of frame, and set the band in the navy-to-royal duotone. It becomes a brand moment rather than a washed-out photo. |
| **p7 Contracting** | The large diamond with the glass facade (300 ppi) is strong, and the cluster has good weight. | The two small tiles (245 ppi) are fine. | No change. |
| **p8 Landscaping** | Clean text side. | (1) The two photos are the weakest pair in the book: a hazy Doha walkway, and a San Diego harbour with skyline and boats. (2) The solid green diamond is as large as the photos and takes the eye first; `system.md` says green is an accent. (3) The Arabic list item «صيانة المنتزهات وأشجار الشوارع» wraps to two lines while the English stays on one. (4) Large empty area at bottom left. | Change the green filler diamond to tint `#E8ECF7` or navy, and keep green to one small diamond at most. Crop the San Diego tile tight to the palm and planting bed so the harbour and skyline leave the frame. Widen the Arabic list column by about 6 mm or reduce the gutter so the item fits on one line. |
| **p9 Maintenance** | The best service page: the gauges hero (300 ppi) is close, human and on-subject. | None of consequence. | No change. |
| **p10 Cleaning** | Good mop detail. | The same green filler issue as p8 (left diamond). The rope-access tile shows a European brick building. | Use tint or navy for the filler. Crop the rope-access tile tighter on the worker and glass so the brick leaves the frame. |
| **p11 Manpower** | A coherent cluster. The "Illustrative" caption is correctly placed under the AI tile. | Two of the five diamonds are empty colour, top left. The AI uniform image is ungraded and much brighter than the two graded tiles beside it. | Accept the AI image as supplied (ruling m9). Reduce the upper pale diamond to the same tint as p8 and p10 so the three filler treatments match across pp8, 10 and 11. |
| **p12 Logistics** | The strongest page in the book. The fleet is large, the logos are real and in perspective, the descriptor on the truck box is legible, and the shadows are consistent. | (1) The pale floor panel ends in a hard horizontal edge just above the chip rule, which reads as a mistake rather than a panel. (2) The truck's rear and the car's nose sit about 3 to 4 mm from the trim edges, which is tight. | End the floor tint exactly on the chip rule (or fade it out over the last 8 mm). Scale the image to about 96% and centre it so both vehicles clear the trim by at least 8 mm. |
| **p13 Why us** | Clear six-point list. | Light page in the middle of a long light run. | MF5 (navy gradient). |
| **p14 Bus shelters** | The client's own work, honestly captioned. | (1) About 60 mm of empty space above the work number on the text side; the page floats. (2) The photo is 550 px (133 ppi), so it cannot grow. | Fill the top of the text column with the work number as a large numeral (40 pt ExtraBold from the type scale, royal blue): «01», on all three works pages. Change the tint panel behind the photo to navy, so the small photos sit like framed prints and the works section gains weight. Leave the photo size as is. |
| **p15 Chamber** | Correct mirroring; good chips. | The same top void. The rendering is 644 px (149 ppi). | As p14 (large «02»; navy panel). |
| **p16 Dar Al Taqwa** | Both client photos are present, at matching heights. | (1) Off-master title size and panel width (MF3). (2) The English body breaks as "services for / Dar Al Taqwa Hotel.", leaving a short line. | MF3. Widen the English body column to the p14 width so the sentence breaks after "cleaning". Large «03». |
| **p17–18 Partners** | An even hairline grid on white, as ruled. 32 logos, properly attributed. | Optical weight is uneven: Tiny House and Imagine More are heavy, while WE AR SPA, Harmony and Madinah Award are pale or tall and thin. The Dar Al Taqwa logo is 64.5 mm wide in a 65.25 mm cell, touching the hairlines. The original 18 logos are low-resolution (some at about 100 ppi) and look soft beside the new ones. | Size logos to equal optical area inside a box of at most 45 × 20 mm per cell (70% × 60% of the cell). Give Dar Al Taqwa 45 mm. The soft originals need official files (B). |
| **p19 Contact** | Clear contact table, white on navy, and the lockup is the right version. | The lockup's top sits about 13 mm from the trim, above the 20 mm top margin every other page uses, so it feels jammed against the edge. The bottom 30% of the page is empty. | Move the lockup down to the 20 mm top margin and reduce it to 64 mm. Once p20 is rebuilt (MF4), p19 and p20 together give two different logo moments rather than the same one twice. |
| **p20 Back** | Correct colour lockup, 90 mm. | Ends on credits (MF4). | MF4. |

---

## (A) Changes the designer can make now with existing assets, ranked by impact

1. **Cover image system (MF2), plus the cover clean-up from the table.** This is the page the client judges first, and the one he asked about by name.
2. **Dark beats across the book: p13 on the navy gradient (MF5) and navy photo panels on pp14–16.** Together they give a dark page or panel every two to five pages (pp2, 5, 13, 14–16, 19, 20) instead of none between p5 and p19. This is the single biggest change to how the whole book feels.
3. **Back cover (MF4) and p19 lockup position.** These shape the last impression.
4. **One works master for pp14–16 (MF3), with large work numerals filling the top void.** The works section is the client's proof, and today it is the visually weakest stretch.
5. **The p6 band in duotone and re-cropped, the p3 photo re-cropped, and the green filler diamonds on pp8, 10 and 11 brought back to accent use.** These make the images read as one set, use the brand colours with discipline, and drop the weakest frames.

Also do these, as smaller items:
- **MF1:** small in impact but a brand rule, so it is mandatory.
- **p12:** floor edge and trim clearance.
- **p8:** the Arabic list wrap.
- **p17–18:** optical sizing.
- **p1:** the stray green diamond.

## (B) Improvements that need material from the client

1. **His own photographs.** This is still the biggest lever by far. Minimum shot list, landscape, 3000 px or more, shot in daylight or golden hour:
   - one hero: a team in uniform at a Madinah site;
   - the bus shelters as installed (two or three angles);
   - the Chamber building as it stands (a photo, not the rendering);
   - a larger Dar Al Taqwa photo;
   - staff at work in cleaning, maintenance and landscaping;
   - any real vehicles.

   Every one of these would replace a stock tile.
2. **The original bus-shelter file.** The current one is 550 px.
3. **Official, high-resolution or vector files of the original 18 partner logos.** Several are soft at about 100 ppi.
4. **Optional:** permission to commission or generate a proper set of uniform and fleet visuals carrying the real lockup, replacing the AI mockups used on p11.

## Summary for the Creative Director

- Fix MF1–MF5, have the quality-reviewer re-check, and send v10 to the client as a reviewed draft.
- Put the B1 shot list to the client in the same message: without his own photography, the profile will stay well made rather than world-class.
- Not checked by me: anything inside the quality-reviewer's or brand-strategist's seats (Arabic proofing, facts, technical export).
