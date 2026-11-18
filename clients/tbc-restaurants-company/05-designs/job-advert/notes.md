# Job advert — notes

**Current:** v02, two directions (A and B), each as post and story. General advert by client decision: no company name, no logo. Awaiting quality review and the client's choice.

## v02 pieces
| Direction | Post 1080 × 1350 | Story 1080 × 1920 |
|---|---|---|
| A "Phone on the pass" — a tilted phone showing a burger post, reactions floating out | `tbc-restaurants-company_job-advert_post-direction-a_ar_v02.png/.html` | `tbc-restaurants-company_job-advert_story-direction-a_ar_v02.png/.html` |
| B "Menu board" — colour blocks, tilted sticker badges, die-cut food and social stickers | `tbc-restaurants-company_job-advert_post-direction-b_ar_v02.png/.html` | `tbc-restaurants-company_job-advert_story-direction-b_ar_v02.png/.html` |

Direction C ("Night service") was dropped by the client before any file was made.

Sources: `base.css` (fonts, reset), `direction-a.css`, `direction-b.css` (palette variables at the top), `fonts/`. The HTML files are the editable sources; `_work/build_a.py` and `_work/build_b.py` regenerate them (the illustration is kept once there, positions per format).
Rebuild: `python3 _work/build_a.py && python3 _work/build_b.py && NODE_PATH=/opt/node-tools/node_modules node _work/render_v02.cjs && python3 _work/finish_v02.py`.

## Copy
Character for character from `01-brief/brief.md`; `_work/render_v02.cjs` asserts all 18 strings in order in each HTML and that no other visible text exists. In A the headline breaks into three lines, in B into two. Numerals: none.

## Palettes (assumptions — no brand supplied)
- A: aubergine `#2B1430` / `#1B0B1F`, tomato `#E5412D`, saffron `#FFB52E`, cream `#FFF3DC`; illustration extras: lettuce `#6DBE45`, cheese `#FFD23F`, patty `#6E3420`. Type: Tajawal 500/700/800.
- B: deep green `#0F3D2E`, ink `#0C2E22` (apply sentence `#04120C`), orange `#FF5A1F`, cream `#FFF4DF`, yellow `#FFD23F`, pink `#FF8FB8`, white; sticker extras: red `#EF4B2F`, leaf `#59B947`, bun `#F2A545`. Type: Cairo 600/800/900 (variable file).

## Contrast (measured on rendered pixels, worst pixel under each text element)
- A: body 13.98:1 (post), 14.22:1 (story); display 4.10:1 (white on the tomato «العمل عن بُعد» pill; every other display element is above 8:1).
- B: body 6.14:1 (apply sentence on orange); display 4.71:1.

## Story safe zone
All text sits between y 290 and y 1580; the top and bottom zones hold illustration only.

## Illustration
All inline SVG drawn for this piece: phone, burger, pizza, fries, generic social symbols (heart, comment bubble, share arrow, play, hashtag, megaphone). No photos, stock, AI images or platform marks.

## History
v01 (plain typographic poster, post and story) is in `_archive/` with the reason.

## Not done
Native Arabic proofread by a second reader; on-device preview under the real story UI; confirmation that `hr@otlobny.co` receives mail.
