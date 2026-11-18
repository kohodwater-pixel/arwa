# HIPPO franchise motion ad — sound panel, production/mix ruling on audio mix v01 (2026-11-18)

Basis: ffmpeg/ffprobe/numpy measurement only; nobody listened. Files read, none changed. Times are seconds in the 40 s mix unless marked "take". Trial renders used to test the fixes were made outside the client folder and are not deliverables.

## 0. Two faults found outside the five questions (fix first)
- **All effects play 50 ms early.** `sfx_track.wav` is 39.95 s and starts mid-waveform at sample 0; the four sub hits fit at -0.050 s against the recipe. Music and voice are on time, so the hook hit lands at 0.95 while the music's first beat lands at 1.00. Fix: add `anullsrc=r=48000:cl=stereo:d=40[z]` as the first `amix` input of the effects graph (tested: length 40.000 s, offset 0.000 s).
- **`alimiter` auto-level is on by default.** `limit=0.9` therefore outputs peaks at 0.0 dBFS, and the slide's `limit=0.5` doubles it (real gain about x36, not x18). Fix: write `level=0` on every `alimiter`.

## 1. Voice cuts (take times; RMS of the 60 ms inside each edge; speech in the take averages -21.6 dBFS, floor -85)
| Seg | In | Level | Out | Level | Ruling |
|---|---|---|---|---|---|
| 1 | 0.00 | -57.0 | 2.10 | -64.1 | keep |
| 2 | 2.30 | -71.7 | 4.25 | **-52.2** | tail runs to 4.33; out = **4.40** |
| 3 | 4.52 | -80.2 | 5.62 | -58.2 | keep |
| 4 «ثقيل» | 5.75 | -61.0 | 6.70 | -63.2 | onset starts at 5.78, 30 ms after the cut; in = **5.70** (set `adelay` 12750), out = **6.76** |
| 5 | 6.87 | -73.7 | 9.15 | **-55.5** | tail runs to 9.19; out = **9.25** |
| 6 «أثقل» | 9.40 | -88.9 | 11.40 | **-53.3** (peak -35.2) | cuts 100 ms of the word's tail (ends 11.50); out = **11.54** |
| 7 | 11.58 | -85.7 | 15.22 | -67.3 | keep |
| 8 | 15.34 | -77.0 | 16.80 | -70.4 | keep |
| 9 | 16.94 | -83.7 | 20.61 | -84.4 | keep (take ends 20.56) |
No cut lands in full-level speech. Three cuts shorten a decaying tail (segs 2, 5, 6) and one is tight (seg 4). Keep the 20/40 ms fades. No placed segments overlap.

## 2. Hook impact
- Final 0–3 s: peak -1.76 dBFS, RMS -11.45, below 100 Hz -12.23 (84 % of the energy; below 60 Hz -12.76). Pre-master sum: peak +2.32, RMS -9.67, below 100 Hz -10.39 (85 %).
- **The hook is not the hardest hit in v01.** 400 ms RMS: hook -6.85, CTA hit (29.6) -6.86, box hit (19.4) -7.58. Before mastering the hook led the CTA hit by 1.0 dB; after, 0.0 dB. Peak: hook -1.76, later hits -1.0.
- Causes, largest first: (a) `sfx_track.wav` is 16-bit and hard-clips the hook, which is +4.9 dB over full scale, with flat tops up to 346 samples (7.2 ms); (b) the limiter takes another 2.2 dB; (c) single-pass `loudnorm` ran in dynamic mode and holds the hook at -1.8 dB (-2.6 dB by 3.5 s) against -0.9 to -1.2 dB for the rest of the film.
- **No silence before the hit.** 0–0.9 s is hook-file rumble at -15.6 dBFS RMS, so the hit only rises about 9 dB. Fix: `[0:a]atrim=1.33:6,asetpts=PTS-STARTPTS,afade=t=in:d=0.005,...,adelay=930` gives digital silence until 0.93, hit at 1.00.
- **Phone speakers will not reproduce it.** With a 250 Hz high-pass, the hook's momentary loudness is -22.6 LUFS against -14.2 for the first voice line, and equal to the pre-hit rumble (-23.0). The sub sweeps 62 to 20 Hz.
- **Mastering chain, ruled:** all stems `-c:a pcm_f32le` (or one filtergraph); effects bus `asoftclip=type=tanh:oversample=4`; sum; fixed gain; `aresample=192000,alimiter=limit=0.841:level=0:attack=5:release=80,aresample=48000`; no `loudnorm` in the path (use it, or `ebur128=peak=true`, only to measure). Target **-14 LUFS integrated ±0.5, true peak -1.5 dBTP** (the v01 MP3 already reads -0.9 against the WAV's -1.0). -14 is the usual working figure for 9:16 social; platform specs were not checked today (assumption).
- Trial of that chain with subs lowered (hook 0.70, others 0.60–0.70) and CTA hit 1.6: -14.3 LUFS, -1.5 dBTP, LRA 4.6; hook 400 ms RMS -8.98 against next hit -11.22, so the hook leads by 2.2 dB. The lead comes mostly from lowering the other hits.
- **Not solved by synthesis:** a 150→80 Hz body layer plus soft clipping moved the phone-band hook only from -22.6 to -20.5 LUFS; a second attempt gave -20.6. A new impact layer with real energy at 300 Hz–2 kHz (soft heavy thump plus paper/holder crunch) is needed; target phone-band momentary loudness at or above the voice (-14 LUFS).

## 3. Slide effect
- Source: peak -29.4 dBFS, active parts -47, gaps -84, so SNR is about 37 dB. Noise is not the problem (floor after gain -53 dBFS).
- **It is too loud and sits on the voice.** In the stem it peaks -2.2 dBFS, RMS -15.8, centred 3.5–4 kHz. During «إيه، طري» (5.7–6.5) the voice leads the effects by only 1.9 dB in 300 Hz–4 kHz, the worst margin in the film.
- It has two events of about 1.1 s; the script has four cups, each stopping on a beat.
- Ruling: **replace** with four short (0.3–0.5 s) ceramic/plastic-on-surface slides, each ending in a small stop "tock", recorded at peak -12 dBFS or higher. Until then: `highpass=f=300,volume=12`, no limiter (margin about 11 dB).

## 4. Music
- **Instrumental: cannot be confirmed without listening or a transcription.** Evidence leans instrumental: 300–3400 Hz sits 12 dB below the total (-27 against -15 dBFS), is bursty (50 ms envelope median -36, 90th percentile -22), and its modulation falls only on the exact 2/4/8 Hz beat grid, with no sustained mid-band line. Short vocal chops or shouts cannot be excluded. One person must listen once; the licence also needs recording.
- **Ducking is too deep and pumps.** Voice over music during speech: 10.3–20.3 dB, reduction up to 17.8 dB, swinging 3.2 dB per 250 ms between words; music falls to -30/-34 dBFS, which is a cause of the dry result. Fix: `sidechaincompress=threshold=0.05:ratio=3:attack=20:release=600` gives 8.2–16.3 dB, reduction up to 11.8 dB, swing 1.9 dB.
- **«ثقيل» (12.8) is the weakest word:** voice -17.7 dBFS against -13 to -15 for the other lines, margin over music 6.8 dB (5.7 with the new ducking). Fix: +3 dB clip gain on seg 4. No masking by the impact: the hit is at 12.40–12.60, the word starts at 12.93, and effects in 300 Hz–4 kHz are at -65 dBFS there.
- **«أثقل» (21.81–22.40):** no masking; voice leads music plus effects by 22.9 dB in 300 Hz–4 kHz, and the box hit is 2.4 s earlier. The word is -19.0 dBFS; split seg 6 in its pause (take 10.62) and give the second part +3 dB.
- Dryness, mix side: voice sits on digital silence (scene 7 gap 24.1–25.0 measures -69.5 dBFS). Add a short room send on the voice about 16 dB under it and a tone/pad at -45 to -40 dBFS through 24.0–29.6. Level and character are the creative expert's call.

## 5. Clipping, DC, clicks
- Final WAV: 0 samples at full scale, true peak -1.0 dBTP, DC -68 dBFS (negligible).
- `sfx_track.wav`: 9,840 samples at full scale at 0.95–1.2, 7.2, 8.5, 9.8, 12.5, 19.4–19.5, 29.6–29.8. `vo_track.wav`: 6 samples at 21.8 («أثقل» onset). Fix: float stems; compressor `makeup=2`.
- Clicks: **0.005** file opens with a step 0 → 0.148 (-16.6 dBFS); **29.40** CTA hit starts with no fade-in, step 0.12 (-18 dBFS); **20.94** sub cut off, step 0.028 (-31 dBFS), under the voice; **33.15** CTA hit tail cut, step 0.022 (-33 dBFS); 29.51 riser end, step 0.018. Fix: `afade=t=in:d=0.01` and `afade=t=out:d=0.2` on both hook pieces, `afade=t=out:st=1.5:d=0.1` on each sub, `afade=t=out:st=2.19:d=0.02` on the riser.
- Music edits (1.0, 24.0, 29.6, 40.0) and all nine voice edges: no step found.
