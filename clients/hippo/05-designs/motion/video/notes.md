# hippo — franchise motion ad «حُطّ ثقلك» — picture draft v02 (9:16)

**Date:** 2026-11-18  **Status:** second picture DRAFT for internal review. Not approved, not for release. v01 is in `_archive/` (failed review on layout).

## What was made
- `hippo_franchise-motion-ad_draft_9x16_ar_v02.mp4` — 1080x1920, 30 fps, 40.000 s (1200 frames), H.264 yuv420p (CRF 16) + AAC 256k stereo 48 kHz. Audio = `../audio/hippo_franchise-motion-ad_audio-mix_ar_v02.wav`, muxed unchanged.
- `hippo_franchise-motion-ad_draft_stills_ar_v02.jpg` — contact sheet of 22 frames taken from the MP4.
- `src/` — live editable source: `index.html` + `film.js` (copy, hit times, cameras and screen layouts at the top), `render.cjs`, `build.sh`, `tools/`, `assets/`.
- `_work/` — frames, stills, guide sheets, cut-out previews (frames and stills are git-ignored).

## Standing rulings (Creative Director, 2026-11-18)
- Brand-graphic motion; only two photographs: hero sandwich (`crispy-chicken.jpg`) and gathering box (`box-breakfast-89.jpg`). Replaces the asset table of script v03 for scenes 2, 3 and 5.
- The hero sandwich stays on stage from 1.0 s to 33.3 s and is thrown about by every weight. It never covers a line of text.
- Logo: ears twitch only at 38.2 s; no blink. "QR static for 3 s" applies to the QR element.
- The box keeps its photographed hot pink. The draft label inside the QR slot stays.

## Scene by scene (film seconds; hits per audio mix v02 timing table)
| # | Time | Picture | On-screen copy |
|---|---|---|---|
| 1 | 0–3.0 | Level stage, word centred on the horizon. Sandwich falls from 0.3, lands 1.000; horizon tilts; the word slides and settles upright beside the sandwich, then tips behind the floor edge | «خفيف؟» |
| 2 | 3.0–7.0 | Camera pulls back; four flat cups stop on 3.138 / 3.523 / 3.907 / 4.291; row nudges the bread at 6.600 | «بريوش طري.» |
| 3 | 7.0–11.0 | Names land 7.200 / 8.500 / 9.800 at about 65 % of frame width; each one stamps the previous one into the floor; the sandwich is thrown left / right / left | «فيلي تشيز ستيك» / «فرايد شرمب» / «الحلومي» |
| 4 | 11.0–14.55 | Third name slides off as the light line fades in; heavy line lands 12.500; «ثقيل.» punches at 12.867 | «خبز خفيف.» «حضور ثقيل.» + *Soft bread. Heavy presence.* |
| 5 | 14.55–19.4 | Five blocks land 15.200 / 16.000 / 16.800 / 17.600 / 18.300 in the middle of the frame; sandwich hops with each; camera climbs | none |
| 6 | 19.4–24.0 | Box lands 19.400; tower collapses into a heap behind it; sandwich thrown to the front; lid wobble, food hop, camera shoved back; «أثقل.» lands on frame 655 | «وبوكس الجَمعات؟» «أثقل.» |
| 7 | 24.0–29.6 | Wide pan: pile on the low left, lime circle alone on the high right, line directly above the circle | «ناقصها ثقلك.» / «امتياز هيبو التجاري» |
| 8 | 29.6–33.3 | Phrase lands in the circle at 29.600; horizon snaps level; everything hops into a row | «حُطّ ثقلك.» + *Put your weight behind it.* |
| 9 | 33.3–40.0 | White end card, logo file, franchise line, enquiry line, empty QR slot (static from 35.9 s); ears twitch 38.2 | «امتياز هيبو التجاري» / *Franchise* / «للاستفسار عن الامتياز:» |

## Fonts actually used
- Arabic: Tajawal Light (300) and ExtraBold (800), from `assets/fonts/tajawal/` (SIL OFL).
- English: Playfair Display Italic (variable file, weight 500), from the google/fonts repository, `ofl/playfairdisplay` (SIL OFL). No fallback used.

## Colours
Identity values exactly: wall #DA6FA2, floor #7B5FC2, blocks #E75A9E with #BBD032 band, circle #BBD032, cup tops #BBD032 / #E75A9E / white / #B8E23A, text #181717 or white. Dust is a dark violet tint, only where an object meets the floor.

## Deviations and simplifications
1. No logo blink (ruling). Ears piece lifts and rotates about 3.6 degrees for 0.7 s.
2. Scene 1: the word is larger (150 px Light) and stands on the horizon line, black on pink.
3. Scene 2: the push into the bread is the whole row at 6.600. Sauce "ripple" is a wobble of the flat top.
4. Scene 3: no hard cuts; the new name stamps the old one below the floor line.
5. Scene 4: both heavy words land together at 12.500; «ثقيل.» punches at 12.867. The line rests just above the floor (keeps the dots of the ي). Texts leave by 14.55, before the camera moves.
6. Scene 5: blank blocks, no fries; small camera climb (84 px).
7. Scene 6: «أثقل.» contact on frame 655 (21.833 s).
8. Scenes 7–8: cups slide back in during the pull-back (22.7–24.2). Circle grows and camera re-frames during the riser (28.85–29.5). The three names do not reappear.
9. End-card cut at 33.300 (the soft thud).
10. No motion blur, no parallax.
11. Box photo: two white specks on the lid retouched (inpainted) in `tools/cutout_box.py`.

## To swap in the HQ photos / QR
- Photos: put the HQ files under the same names in a folder, run `python3 src/tools/cutout.py <folder> <out> crispy-chicken` and `python3 src/tools/cutout_box.py <folder>/box-breakfast-89.jpg <out>` (set `SCALE` in `cutout_box.py` to HQ width / 1236), copy results to `src/assets/sandwich.png` and `box.png`, and scale the sprite anchors in `film.js` (`SW`, `BX`) and `SW_SC` / `BOX_SC` by the same factor. Check the cut-outs by eye again.
- QR: save the code as `src/assets/qr.png`, set `CFG.qr = 'assets/qr.png'`; the placeholder and its label disappear.
- Rebuild: `bash src/build.sh v03`. Safe-area and margin guides: `GUIDES=1 node src/render.cjs stills <dir> <times>`.

## Assumptions
- The placeholder label «مكان رمز QR / يُضاف عند استلام الرابط» is draft-only wording, not client copy.
- Safe areas: 250 px top, 350 px bottom; side margin 60 px.
