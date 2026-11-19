# hippo — franchise motion ad «حُطّ ثقلك» — look B «هيبو بأعلى صوت» — film v03 (9:16)

**Date:** 2026-11-19  **Status:** first full picture in look B, cut to the approved audio mix v02. For internal review; not approved, not released.
**Nobody has watched this film in real time with sound.** Everything stated below was measured on the files or seen in still frames.

## Files
- `hippo_franchise-motion-ad_9x16_ar_v03.mp4` — 1080x1920, 30 fps, 1200 frames, 40.000 s, H.264 yuv420p (CRF 16) + AAC 256k stereo 48 kHz. Audio = `../audio/hippo_franchise-motion-ad_audio-mix_ar_v02.wav`, muxed unchanged.
- `hippo_franchise-motion-ad_stills_ar_v03.jpg` — contact sheet of frames taken from the MP4, labelled with time codes.
- `src/` — editable source: `index.html` (all copy and layout), `film.css`, `film.js` (hit frames at the top, one function per scene), `render.cjs`, `build.sh`, `check.py`, `verify.py`, `sheet.py`, `assets/`.
- `_work/` — frames, stills and check renders (git-ignored).

## Rebuild
```
bash src/build.sh v04                      # renders 1200 PNG frames with Chromium, encodes, muxes the audio
node src/render.cjs check _work/chk 2.5 5.5 8.3 10.8 12.3 14.5 19.2 21.6 23.5 26.2 28.5 30.2 32.5 34.9 37
python3 src/check.py _work/chk             # contrast >= 4.5:1, safe areas 250 / 350 / 60 px, no letter-spacing
python3 src/verify.py hippo_franchise-motion-ad_9x16_ar_v04.mp4 _work    # container, audio onsets, hits, QR
```
Preview with sound: open `src/index.html` in a browser and press play (not possible in the cloud session).
The render is deterministic: `window.seek(t)` lays out a frame from the time alone.

## Scenes and hit frames (frame = round(t x 30), from the mix v02 timing table)
| # | Time | Ground | Picture | Hits (frame) |
|---|---|---|---|---|
| 1 | 0–3.0 | pink | «خفيف؟» floats big; landing shadow grows with the whoosh; freeze 0.92–1.00; sandwich slams in | 30 |
| 2 | 3.0–7.0 | black | «بريوش طري.»; four squash-bounces with four sticker bursts; one deep press | 94, 106, 117, 129; 198 |
| 3 | 7.0–11.0 | pink | proof stickers land and tip the frame; the sandwich is knocked down a stage by each | 216, 255, 294 |
| 4 | 11.0–15.0 | pink, lime from 12.5 | stickers pull back; «خبز خفيف.» floats; «حضور ثقيل.» lands with the colour flip; punch | 375, 386 |
| 5 | 15.0–19.4 | black | four chips stack on the bread; fifth hit squashes the stack | 456, 480, 504, 528; 549 |
| 6 | 19.4–24.0 | lime | gathering box; «وبوكس الجَمعات؟» at 20.43; «أثقل.» | 582; 655 |
| 7 | 24.0–29.6 | lime over pink | full side (box, sandwich) heavy and low; 24.0–26.1 the four proof stickers sit large in the top half with the franchise pill; at 26.1–26.4 they close up into a row and the empty seat (a big white sticker, tilted, with three bouncing dots) pops in at 26.4; «ناقصها ثقلك.» lands inside it at 27.6 with the voice; riser; freeze 29.52–29.60 | — |
| 8 | 29.6–33.3 | lime over pink | «حُطّ ثقلك.» lands in the seat, replaces the light line, slams the seat down and the scale levels; English line; pill | 888 |
| 9 | 33.3–40.0 | white | end card; QR untouched from 33.77 s; band wiggle and blob pop with the sonic logo | 999; 1146 |

## Change the facts or chips
Edit the text in `src/index.html` inside the elements marked `data-swap`. The facts appear twice: in scene 3–4 (`k1`…`k4`) and in scene 7–8 (`n1`…`n4`). Chips are `c1`…`c4`. Then rebuild and re-run `check.py`.
Facts in this version (client-confirmed 2026-11-19): «علامة سعودية» · «من 2021» · «5 فروع» · «منطقتان — الرياض · المدينة المنورة». No other figure or claim.

## Hero photo and swapping in the HQ photos
- Hero = fried shrimp (client instruction 2026-11-19). `src/assets/sandwich.png` is cut locally from `_originals/.../04-menu-photos-web/fried-shrimp.jpg` with `python3 src/tools/cutout_shrimp.py <fried-shrimp.jpg> src/assets/sandwich.png [preview-dir]` (OpenCV only; no shadow baked in, the film adds its own). Native size 933x724 px (object 842x671). Largest use: 989 px wide (106 %) in scenes 1–3.
- The earlier crispy-chicken cut-out is kept in `_archive/`.
- HQ photos: run the same tool on the HQ file (scale its ROI and kernel sizes by HQ width / 1202) and replace the PNG; sizes in `index.html` are CSS widths, so no layout change is needed. The box is `src/assets/box.png` (1068x1135), tools in `../video/src/tools/`. Check the edges by eye again.

## Fonts and colours
Tajawal Light / ExtraBold and Playfair Display Italic from `src/assets/fonts/` (SIL OFL). Lime #BBD032, black #181717, pink #DA6FA2, white. The box keeps its photographed hot pink.

## Assumptions
- Safe areas: 250 px top, 350 px bottom, 60 px sides, applied to settled text.
- The "ears" band is our own vector drawing after the client's lid print and profile outline, not his file.

## Verified on the built MP4 (measured or seen in stills; not watched)
Run `python3 src/verify.py <mp4> _work` and `python3 src/check.py _work/chk`; the figures of the last build are in the hand-off. The end card carries two codes: the client's franchise-form code (right, larger, `assets/qr.png`) labelled «قدّم طلب الامتياز», and the agency-generated menu code (left, `assets/qr-menu.png`, copied from `06-profiles/franchise-brochure/src/assets/`) labelled «تصفّح منيو هيبو». «للاستفسار عن الامتياز:» was dropped by the Creative Director's instruction.

## Deviations from the scene plan
1. Scene 1: the word starts big and low and is knocked up to its place by the hit (to fill the frame before the sandwich arrives).
2. Scene 2 is on black with white type; scene 5 is on black too. Text in the film is therefore black, white or (on black stickers) lime.
3. Scene 3: on pink, so the «5 فروع» circle is lime there and turns pink with the colour flip at 12.5. The sandwich is the hero in the middle and is knocked down a stage by the second and third stickers.
4. Scene 5: the chips stack on the bread; the fifth hit squashes stack and bread (no new object lands).
5. Scene 6: the lid is not separated; the whole box rocks on the three lid taps. The question line enters at 20.43 s.
6. Scene 7: «ناقصها ثقلك.» appears at 27.6 s, the onset of those words measured on the voice stem (the timing table gives only the whole line, 25.09–28.54). The seat is on screen from 26.4 s, never blank: three bouncing dots for 1.2 s, then the phrase. No dashed outlines anywhere.
7. Scene 7–8: all four proof stickers, large until 26.1 s, then a compact row (city names are about 17 px high in the row).
8. Scene 9: logo enters by uniform scale only; the franchise line is there on the cut; at 38.2 the band wiggles and the blobs pop. Both QR tiles static from about 34 s. No colour wipe on this cut (a band behind the transparent logo hid part of it).
9. Flashes are a pale tint of the scene's own ground at 60 % or less, never white; each cut has one colour band (two at 15.0). Colour wipes are bands that sweep behind the content starting on the cut, so the hit frame itself is never covered. No wipe at 3.0 (white type), 24.0 (music stops) or 33.3.
10. For two or three frames after the big hits the hero is oversized and may touch the frame edge.

## Known weak spots
- 29.6–29.9 s: during the hop on the hit the pill and the proof stickers overlap for a few frames.
- Scene 7–8: the box's lower-left corner comes within a few pixels of the frame edge while the full side is tipped.
- Photos are the web-size cut-outs; the sandwich reaches 106 % in scenes 1–3.
