# Logo animation — notes

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS. Not client-ready.

**Date:** 2026-11-13  **Prepared by:** Graphic Designer  **Version:** v01

## Files

| File | What it is |
|---|---|
| `demo-sidra-coffee_logo-animation_primary_ar_v01.mp4` | The animation. H.264 High, yuv420p, bt709, 1080 × 1080, 30 fps, 90 frames, 3.000 s, 30,130 bytes, no audio track |
| `demo-sidra-coffee_logo-animation_primary_ar_v01.html` | Editable source. Plays and loops in a browser; add `?static` for the final logo only. Timings are in the `T` object |
| `motion-brief.md`, `storyboard.md` | Brief and scene list |
| `_work/build.py` | Generates the HTML from the approved logo SVG |
| `_work/capture.cjs` | Playwright frame-by-frame capture (90 PNG frames) |
| `_work/encode.sh` | ffmpeg encode |
| `_work/frame_01` … `frame_06`, `_work/contact-sheet_6-frames.png` | Frames extracted from the MP4 at 0.00, 0.50, 1.23, 1.50, 1.67 and 2.97 s, and a sheet of all six |

## How to rebuild

From this folder: `python3 _work/build.py`, then `node _work/capture.cjs <html> <framesDir> <logo.svg>`, then `sh _work/encode.sh <framesDir> <out.mp4>`. The 90 captured frames were written to a temporary folder outside the repository and are not kept.

## Checks

- ffprobe: values in the table above.
- Six frames extracted from the MP4 and viewed: start is empty Paper; bars arrive from the right; the fourth bar fills with Ember; the wordmark is complete and connected in every frame where it is visible; the last frame is the primary logo.
- Colours sampled from the last MP4 frame: Paper 243 234 223 (target 243 236 224), Ink 30 25 22 (target 31 27 24), Ember 194 57 32 (target 194 58 32).
- The captured end frame was compared with the approved SVG rendered as an image at the same position: 1,265 of 1,166,400 pixels differ strongly, all on the top and bottom edge rows of the bars and the outline of the letters. See below.

## What did not work, or is not verified

1. **First encode had wrong colours.** ffmpeg converted with the bt601 matrix while the file was tagged bt709, and Ember came out as 206 67 27. Fixed with an explicit bt709 matrix in the scale filter; the delivered file is the corrected one.
2. **First reveal of the wordmark was a bottom-up wipe.** Half-way through it hid the dots of the ة and the word read as «سدره». Replaced with a whole-word fade.
3. **The end frame is not pixel-identical to the static SVG.** The differences are one-pixel antialiasing on edges (inline SVG against the same SVG as an image, at a fractional pixel offset). Nothing is visibly different, but a strict pixel match was not achieved.
4. **Colours in the MP4 are within 2 levels of the palette, not exact**, because of 4:2:0 video encoding.
5. **The first frame is empty**, so it fails the "first frame works as a thumbnail" check in the motion skill. Use the last frame as the cover.
6. **Style frames were not made as a separate step** and the storyboard was not approved before animating; the sequence came from the brief. The extracted frames stand in for style frames.
7. **Played back only as extracted frames.** I did not watch the video in a player, so the feel of the timing is judged from the numbers, not from viewing in motion. Playwright's `recordVideo` was not used; capture was frame by frame.
8. The art-director has not reviewed the concept or the fade.
