# HIPPO — box clip «ما ينزل خفيف», 9:16: production notes v01

Date: 2026-11-22. By: graphic-designer. Status: v01, not reviewed. Built to `hippo_box-clip_direction_ar-en_v01.md` and the Creative Director's brief of the same day.

## Files
- `hippo_box-clip_9x16_ar_v01.mp4` — 1080 × 1920, 30 fps, 17.5 s, H.264 High + AAC 48 kHz stereo, −14.1 LUFS, −1.5 dBTP.
- `src/build.sh` runs everything: `01_cleanup_A.py`, `02_interp_A.sh`, `03_render_video.py`, `04_audio.py`, `05_mux.sh`, `06_checks.py`.
- `_work/frames_v01/` — nine stills from the final MP4 and `hippo_box-clip_contact-sheet_v01.png`.
- `_work/chk/checks_v01.txt` — output of the checks. `_work/` also holds every intermediate (about 2 GB).

## Timeline (seconds)
0.00–6.70 piece A (source from 1.27 s; impact at 1.40) · 6.53–6.90 whip blur and exposure dip, cut at 6.70 · 6.70–8.77 piece B live (source frames 9–70) · card first visible 7.87 · VO 7.90–15.42 · 8.77–17.50 hold on one still (1 s settle, then drift only).

## Copy on screen
Only the card v01, unchanged: امتياز هيبو التجاري · افتح هيبو / في مدينتك. · علامة سعودية منذ 2021 / 5 فروع في منطقتين · قدّم طلب الامتياز. No captions or supers.

## Decisions taken while building
- Piece B rotated 90° clockwise (hand enters from the bottom). The lid panel is then 212 × 550 px, ratio 2.6:1, so card v01 fits as it is; no v02 card was needed.
- Hold framing: card 480 px wide (44 %), top at y 150, bottom at y 1398. To get there the phone "lifts" from 2.75× to 2.35× during the first second of the hold, and 190 px of asphalt was added below the frame from asphalt of the same frame.
- Piece B plays at 125 % (one source frame per output frame), above the 115 % in the direction: it avoids repeated frames on the hand and keeps the card track exact.
- Piece A is motion-interpolated to 30 fps; the seven frames of the fall are the real frames.
- A jolt of 20 px was added at the impact.
- No HIPPO lettering on the box. No car chirp: it could not be auditioned here, so it was left out as briefed.
- Sound: the clips' own audio is the bed (phone band 150 Hz–9 kHz, mono); B's sound is speeded with the picture; the thud is synthesised; VO take 1 has 3:1 compression and a limiter, nothing else.

## Not verified
- Nothing was listened to. Levels are measured; the character of the thud, the clips' own sounds and the VO limiting need a person's ears.
- QR scanned only with OpenCV, not with a phone camera off a phone screen.
- Arabic checked by eye on exported frames, not proofread by a native reader.

---

# v02 (2026-11-22) — after the quality review of v01

File: `hippo_box-clip_9x16_ar_v02.mp4` (v01 kept untouched). Scripts: `src/v02/` (`build.sh` runs all). Stills: `_work/frames_v02/`. Checks: `_work/chk/checks_v02.txt`.

## Timeline (seconds)
0.00–7.03 piece A = gen03 (box enters 1.20, first ground contact 1.40) · 6.80–7.27 whip blur, cut at 7.03 · 7.03–9.10 piece B live (source frames 9–70) · card on the lid from 8.03 · VO 8.10–15.62 · 9.10–17.50 hold.

## What changed against the reviewer's list
1. Join: piece A is gen03, which ends looking down at the box with the stripe on the right. A pushes in 24 % over its last 20 frames so the box is as wide in frame as B's; B starts at the same x. 7 + 7 frames of vertical blur (up to 620 px) with a 4-frame dissolve and exposure dip inside. B is graded to A (asphalt tint, pink and lime onto A's values) and has an added soft shadow left of the box.
2. Card: tracked from source frame 39, the first frame the lid panel shows; no fade. The tuck flap being folded (pink) or flat (white) is detected per frame so the card keeps its place on the panel.
3. Colours: the card is no longer desaturated or graded. Its white is a neutral white 6 % above the lid's own white; black is lifted 4.5 %. B's white point is raised before the card goes on.
4. Car: gen03 has one small car, side-on. Its grille/badge area and a small sign on the wall are repainted flat (no blur patches). No plates are visible in this take.
5. Thumb matte: the hand is now found as one skin-coloured blob (saturation 38 or more, closed and dilated) and removed from the lid matte.
6. QR: card 525 px wide, code 324 px = 30 % of frame width, 8.75 px per module; top of card at y 90.
7. Timing of A: frames before the fall interpolated at 100 %, the fall and wobble (source frames 28–45) used as shot, walk-up interpolated at 115 %. No repeated frames.
8. Sound: bed rebuilt from gen03's audio following the picture's timing; thud longer and denser; VO about 1 dB lower; overall −14.9 LUFS.
9. Hold: box and card are one still; the asphalt around them plays on (B frames 70–193 registered to the still, forwards then backwards), plus grain.

## Not verified (unchanged from v01)
Nothing was listened to. No phone-to-phone QR scan. No native proofread of the Arabic.
