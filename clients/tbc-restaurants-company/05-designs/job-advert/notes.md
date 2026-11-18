# Job advert — notes

**Current:** v02, two directions (A and B), each as post and story. General advert by client decision: no company name, no logo. Awaiting quality review and the client's choice.

## Current pieces
| Direction | Post 1080 × 1350 | Story 1080 × 1920 |
|---|---|---|
| A v03 "Phone on the pass" — device mock with the client's burger photograph breaking out of the screen, frosted reaction cards | `tbc-restaurants-company_job-advert_post-direction-a_ar_v03.png/.html` | `tbc-restaurants-company_job-advert_story-direction-a_ar_v03.png/.html` |
| B v02 "Menu board" — colour blocks, tilted sticker badges, die-cut food and social stickers (unchanged) | `tbc-restaurants-company_job-advert_post-direction-b_ar_v02.png/.html` | `tbc-restaurants-company_job-advert_story-direction-b_ar_v02.png/.html` |

Direction C was dropped by the client before any file was made. A v02 (drawn burger, flat look) and v01 are in `_archive/` with reasons.

Sources: `base.css`, `direction-a.css` (v03), `direction-b.css`, `fonts/`, `assets/`. The HTML files are the editable sources; `_work/build_a_v03.py` and `_work/build_b.py` regenerate them.
Rebuild: `python3 _work/build_a_v03.py && python3 _work/build_b.py && NODE_PATH=/opt/node-tools/node_modules node _work/render_v02.cjs && python3 _work/finish_v02.py`.

## Client photograph (A v03)
`assets/tbc-restaurants-company_burger-photo_client-supplied.png` is a lossless PNG copy of `_originals/tbc-restaurants-company_burger-photo_client-supplied.webp` (1339 × 874, transparent cut-out). Client-supplied; **source and licence not stated by the client**. Used unaltered: proportional scaling (404 px wide in the post, 584 px in the story), a 3° tilt and drop shadows only; no recolouring, redrawing or cropping. The render script asserts the aspect ratio and that no colour filter is applied.

## Copy
Character for character from `01-brief/brief.md`; `_work/render_v02.cjs` asserts all 18 strings in order in each HTML and that no other visible text exists. In the A post the headline breaks into three lines (two in the A story), in B into two. Numerals: none.

## Palettes (assumptions — no brand supplied)
- A v03: night `#0E0611`, aubergine `#2B1430`, plum `#4A1D4F`, tomato `#E5412D`, saffron `#FFB52E`, cream `#FFF3DC`, paper `#FFFAF1`; warm glow amber `#FFB048` to tomato. Type: Tajawal 500/700/800 (IBM Plex Sans Arabic was rendered for comparison, `_work/compare_v02_v03_plex.jpg`; it forces the headline down to 72 px, so Tajawal was kept).
- B: deep green `#0F3D2E`, ink `#0C2E22` (apply sentence `#04120C`), orange `#FF5A1F`, cream `#FFF4DF`, yellow `#FFD23F`, pink `#FF8FB8`, white; sticker extras: red `#EF4B2F`, leaf `#59B947`, bun `#F2A545`. Type: Cairo 600/800/900 (variable file).

## Contrast (measured on rendered pixels, worst pixel under each text element)
- A v03: body 11.07:1 (post), 12.10:1 (story); display 3.64:1 (white on the tomato «العمل عن بُعد» pill, 31 px ExtraBold; all other display text above 9:1).
- B: body 6.14:1 (apply sentence on orange); display 4.71:1.

## Story safe zone
All text sits between y 290 and y 1580; the top and bottom zones hold illustration only.

## Illustration
A v03: CSS device mock, frosted cards and gradient hearts drawn for this piece, plus the one client photograph. B: inline SVG stickers drawn for this piece. No stock, AI images or platform marks.

## History
v01 (plain typographic poster, post and story) is in `_archive/` with the reason.

## Not done
Native Arabic proofread by a second reader; on-device preview under the real story UI; confirmation that `hr@otlobny.co` receives mail.
