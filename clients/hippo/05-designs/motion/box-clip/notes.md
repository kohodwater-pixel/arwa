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
