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

---

## Round 3 — 2026-11-13 (added section; everything above is the v01 record, unchanged)

**The film has still not been watched played back by a person.** Not by the maker, the quality-reviewer, the art-director or the Creative Director. Everything below is judged from extracted still frames and from numbers. This stays open until someone plays the MP4 in a player and on a phone.

### Art-director review

`art-director-review.md` approves the concept, the storyboard and the v01 MP4 with no re-export, and asks for a poster frame, `storyboard_v02.md`, `motion-brief_v02.md` and this section.

### Files added in round 3

| File | What it is |
|---|---|
| `demo-sidra-coffee_logo-animation_poster_ar_v01.png` | Poster frame. Last frame (frame 89) of the v01 MP4, extracted with ffmpeg (bt709 matrix, full range), 1080 × 1080, RGB, sRGB ICC profile embedded with Pillow (588 bytes, read back). Viewed: the complete primary logo, wordmark connected, both dots of the ة present, fourth bar in Ember. Dominant colours: Paper 244 236 224, Ink 32 27 24 |
| `storyboard_v02.md` | Status changed to approved; the two open notes replaced by references to rulings 3 and 2; poster added |
| `motion-brief_v02.md` | "Prepared by" records the review; the "no blends" line reworded as the art-director specified; the art-director's rules recorded; platform still an assumption |
| `demo-sidra-coffee_logo-animation_primary_ar_v02.html` | Copy of the v01 source with one change: `litDur` 0.26 → 0.20 (and the version in the page title) |
| `demo-sidra-coffee_logo-animation_primary_ar_v02.mp4` | **Candidate, not approved.** Captured and encoded with the same `_work/capture.cjs` and `_work/encode.sh`. ffprobe: H.264 High, yuv420p, bt709 matrix / transfer / primaries, tv range, 1080 × 1080, 30 fps, 90 frames, 3.000 s, 30,119 bytes, one video stream, no audio |
| `_work/fill-check/` | `v01_f033` … `v01_f045` and `v02_f033` … `v02_f045` (every frame from 1.10 to 1.50 s of each MP4), two contact sheets at 3× nearest-neighbour enlargement of bars 3 to 5, `poster_raw.png`, `v02_last-frame.png` |

`storyboard.md` and `motion-brief.md` (v01) and the v01 HTML and MP4 are untouched.

**Poster file name.** The round-3 task names the poster `…_logo-animation_poster_ar_v01.png`; the art-director's review names it `…_logo-animation_primary-poster_ar_v01.png`. The task's name was used. One file only was written. The Creative Director decides which name stands.

### Watch check on the Ember fill (frames, not playback)

Thirteen frames, 33 to 45 (1.100 to 1.500 s), extracted from each MP4. Ink rows left in the fourth bar, counted down the centre column of the bar (the bar is 32 px tall):

| Frame | Time (s) | v01 (fill 0.26 s) | v02 (fill 0.20 s) |
|---|---|---|---|
| 33, 34 | 1.100, 1.133 | 32 (no Ember) | 32 (no Ember) |
| 35 | 1.167 | 23 | 20 |
| 36 | 1.200 | 14 | 10 |
| 37 | 1.233 | 7 | 4 |
| 38 | 1.267 | 3 | 0 full rows; one dark blended row at the top edge |
| 39 | 1.300 | 1 | 0 full rows; top row within 6 levels of rest |
| 40 | 1.333 | 0 full rows; top row still darker than at rest (138 57 41 against 172 65 42) | 0, at rest from this frame |
| 41 – 45 | 1.367 – 1.500 | 0; at rest from frame 42 | 0, at rest |

What the v01 sheet shows: the sliver is visible across consecutive frames. It is 3 px in frame 38 and 1 px in frame 39, with a darker top row still settling in frames 40 and 41. It only ever shrinks: it never disappears and comes back, and no frame shows the bar lit and then unlit. So it is not an on-off flicker in the frames; it is a thin dark line that lingers for about 0.07 to 0.10 s because the cubic ease-out slows the last few pixels of the fill. Whether that reads as a flicker, a shimmer or nothing at 30 fps cannot be judged from stills.

Because the sliver is present on consecutive frames, the round-3 instruction applied and v02 was made. What v02 changes: the thin sliver (4 px or less) is on frames 37 and 38 instead of 38, 39 and 40, and the bar is at rest two frames earlier (frame 40 instead of 42). The improvement is small. The ease-out tail is the cause, and shortening the duration reduces it without removing it.

Other v02 checks: the last frame of v02 against the last frame of v01 differs by at most 8 levels on any channel, no pixel by more than 8 (encoder noise); the poster therefore serves both. Scene 5 becomes a 0.16 s pause on seven bars, which meets ruling 1. The build, the fade and the hold are untouched in the source.

### Open, and not verified

1. **Playback in motion by a person: still not done**, for v01 or v02.
2. **Which film stands.** v01 is the approved file. The art-director wrote "do not change it on my guess" and tied the 0.20 s change to someone watching the film. v02 was made on a frame check, not a viewing, so it is a candidate until the art-director or a person who has watched both chooses.
3. The v02 film was only checked on frames 33 to 45 and 89 plus ffprobe. Its other 76 frames were not viewed; they come from the same source with the same timings.
4. The 90 captured v02 frames were written to a temporary folder outside the repository and are not kept.
5. The sRGB profile is Pillow's built-in sRGB, not the IEC 61966-2.1 file from the ICC.
6. Platform re-encoding, phone playback and the platform itself remain unverified, as in the art-director's review.
