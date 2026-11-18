# hippo — franchise motion ad «حُطّ ثقلك» — picture draft v01 (9:16)

**Date:** 2026-11-18  **Status:** first picture DRAFT for internal review. Not approved, not for release.

## What was made
- `hippo_franchise-motion-ad_draft_9x16_ar_v01.mp4` — 1080x1920, 30 fps, 40.000 s (1200 frames), H.264 yuv420p (CRF 16) + AAC 256k stereo 48 kHz. Audio = `../audio/hippo_franchise-motion-ad_audio-mix_ar_v02.wav`, muxed unchanged.
- `hippo_franchise-motion-ad_draft_stills_ar_v01.jpg` — contact sheet of 15 frames taken from the MP4.
- `src/` — editable source: `index.html` + `film.js` (all copy, hit times and layout at the top), `render.cjs` (Chromium frame render), `build.sh` (render + encode + mux), `tools/` (cut-out scripts, contact-sheet script), `assets/` (two cut-outs, logo copy, fonts).
- `_work/` — frames, stills, cut-out previews (frames and stills are git-ignored).

## Approved deviation from script v03 (client change, Creative Director ruling 2026-11-18)
The film is brand-graphic motion, not a menu-photo film. Only two photographs are used: the hero sandwich (`crispy-chicken.jpg`, scenes 1–2, again in 7–8) and the gathering box (`box-breakfast-89.jpg`, scene 6, stays in 7–8). Everything else is flat identity graphics. This replaces the asset table of script v03 for scenes 2, 3 and 5.

## Scene by scene (times in film seconds; hits per audio mix v02 timing table)
| # | Time | Picture | On-screen copy |
|---|---|---|---|
| 1 | 0–3.0 | Level empty stage. Sandwich lands at 1.000 (squash, shake, horizon tilts toward it); the word slides down the horizon, piles up against the sandwich, tips behind the floor edge | «خفيف؟» |
| 2 | 3.0–7.0 | Camera settles lower; four flat cups slide in and stop on 3.138 / 3.523 / 3.907 / 4.291; row nudges the bread at 6.600, bread and word squash | «بريوش طري.» |
| 3 | 7.0–11.0 | The three names are the weights: land 7.200 left, 8.500 right, 9.800 left; each landing swings the horizon and catapults the previous name out | «فيلي تشيز ستيك» / «فرايد شرمب» / «الحلومي» |
| 4 | 11.0–15.0 | Light line floats up; heavy line lands 12.500 and tilts the line above; «ثقيل.» punches at 12.867 with the voice | «خبز خفيف.» «حضور ثقيل.» + *Soft bread. Heavy presence.* |
| 5 | 15.0–19.4 | Five flat pink/lime blocks land 15.200 / 16.000 / 16.800 / 17.600 / 18.300; camera climbs with the tower | none |
| 6 | 19.4–24.0 | Box lands 19.400 (biggest shake), tower collapses, lid wobbles (19.52 / 19.74 / 19.98), food hops once, camera is pushed back; «أثقل.» lands 21.83 | «وبوكس الجَمعات؟» «أثقل.» |
| 7 | 24.0–29.6 | Wide shot, floor tilted, everything piled at the low end; lime light circle on the empty side | «ناقصها ثقلك.» / «امتياز هيبو التجاري» |
| 8 | 29.6–33.3 | Phrase lands in the circle at 29.600; horizon snaps level; everything hops once and lines up | «حُطّ ثقلك.» + *Put your weight behind it.* |
| 9 | 33.3–40.0 | White end card, logo file, franchise line, enquiry line, empty QR slot (static from 35.9 s); ears twitch at 38.2 | «امتياز هيبو التجاري» / *Franchise* / «للاستفسار عن الامتياز:» |

## Fonts actually used
- Arabic: Tajawal Light (300) and ExtraBold (800), from `assets/fonts/tajawal/` (SIL OFL).
- English support lines: Playfair Display Italic (variable font file, weight 500), downloaded 2026-11-18 from the google/fonts GitHub repository, `ofl/playfairdisplay` (SIL OFL; licence text in `src/assets/fonts/`). No fallback font was used; the page reported all three faces loaded.

## Colours
Stage and graphics use the identity values exactly: wall #DA6FA2, floor #7B5FC2, blocks #E75A9E with #BBD032 band, circle #BBD032, cup tops #BBD032 / #E75A9E / white / #B8E23A, text #181717 or white. The stage is NOT colour-matched to the photos (changed with the client's "frames in the identity" direction).

## Deviations and simplifications (other than the approved one above)
1. Logo blink not done. The mark has no shape that is unambiguously an eye; the two shapes under the brow line could be eyes or teeth. A blink on them was tested (`CFG.blink`, off) and breaks the outline, so v01 has the ear twitch only: the ears piece (a separate shape in the file) lifts and rotates about 3.6 degrees for 0.7 s, then returns. Nothing is redrawn.
2. Scene 1: the word stands on the horizon line (black on pink), not on the violet floor, to keep the script's colour rule (white on violet).
3. Scene 2: the nudge into the bread is the whole row at 6.600 (where the squish sound is), not the last cup's arrival. Sauce "ripple" is a wobble of the flat top ellipse.
4. Scene 4: both heavy words land together at 12.500 (the thud); «ثقيل.» gets a second punch at 12.867 with the voice. The line rests just above the floor; it sinks only at the moment of impact (the dots of the ي disappeared when it stayed sunk).
5. Scene 5: no fries (no photo); the lower blocks squash at each landing instead. Blocks are blank (no logo, no lettering). The word «ثقيل» does not fall a last time; the heavy line sinks through the floor before the first block.
6. Scene 6: «أثقل.» contact is on frame 655 (21.833 s), the first frame after 21.810.
7. Scene 7–8: sandwich and cups slide into the pile during the pull-back (22.5–23.9). The circle grows and the camera re-frames during the riser (28.85–29.5), before the hit.
8. Scenes 7–8: the three name-words do not reappear.
9. End card cut is at 33.300 (the soft thud in the mix), not 33.0.
10. Motion blur, real letter shadows with depth and 2.5D parallax are not in this draft; dust is a soft blurred puff.

## To swap in the HQ photos / QR
- Photos: put the HQ files under the same names in a folder, run `python3 src/tools/cutout.py <folder> <out> crispy-chicken` and `python3 src/tools/cutout_box.py <folder>/box-breakfast-89.jpg <out>` (set `SCALE` in `cutout_box.py` to HQ width / 1236), copy results to `src/assets/sandwich.png` and `box.png`, and scale the sprite anchors in `film.js` (`SW`, `BX`) by the same factor. Check the cut-outs by eye again.
- QR: save the code as `src/assets/qr.png`, set `CFG.qr = 'assets/qr.png'` in `film.js`; the placeholder and its label disappear.
- Rebuild: `bash src/build.sh v02`.

## Assumptions
- The on-screen placeholder label «مكان رمز QR / يُضاف عند استلام الرابط» is draft-only wording, not client copy.
- Safe areas taken as 250 px top / 350 px bottom.
