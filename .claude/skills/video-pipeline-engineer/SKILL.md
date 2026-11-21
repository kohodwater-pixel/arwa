---
name: video-pipeline-engineer
description: Handle video and audio files after generation in video-platform/ — storing clips, trimming and joining scenes, transitions, mixing music, effects and voice-over, syncing audio to scenes, and exporting MP4 with FFmpeg. Use when the final film has wrong length, size, frame rate or sound, when adding transitions or audio features, when tuning output size and quality, or when editing server/ffmpeg.js, storage.js, uploads.js or the assemble job. Triggers include "تجميع الفيديو", "FFmpeg", "MP4", "الصوت", "transitions".
---

# Video pipeline engineer

Everything between "the provider returned a clip" and "the user downloads a film".

## What exists (video-platform/server)

- `storage.js` — storage driver (local disk under `data/storage`). Swap it for object storage by keeping the same functions; `localPath` must still give FFmpeg a real file.
- `uploads.js` — uploads are identified by file signature, probed with ffprobe, and limited by size and type. Never trust the file name or the browser's MIME type.
- `ffmpeg.js` — `probe`, `assemble`, `lastFrame`, `poster`, `renderDemoClip`. FFmpeg is called with an argument array, never through a shell string.
- `pipeline.js` — `assembleJob` and `resolveTracks`.

## How a film is assembled

1. Each clip is trimmed to its scene duration, scaled and cropped to the frame size of the first clip, set to one frame rate, `yuv420p`, square pixels. A clip shorter than its scene holds its last frame.
2. Clips are concatenated with the `concat` filter (re-encode), not the concat demuxer, because providers return different codecs and timebases.
3. Audio: clip audio (when the model produced it) plus music, ambience, effects and voice-over tracks, each with its volume. Music and ambience loop to the film length; voice-over lines start at their scene's start time (`adelay`). `amix` with `normalize=0`, then a limiter.
4. Export: H.264, CRF 18, `+faststart`, AAC 192 kbps when there is any audio, no audio stream when there is none.

## Rules

- **Lengths are arithmetic, check them.** Film duration = sum of scene durations. After any change, probe the output and compare.
- **No upscaling claims.** Output resolution comes from the generated clips; do not label a 720p source as 1080p.
- **Transitions change the maths.** The film currently uses hard cuts. A cross-fade (`xfade`) of `t` seconds between two scenes shortens the film by `t` per transition and needs each offset computed from the running total; voice-over offsets must shift with it. Add transitions as a per-project option and cover the duration in a test.
- **Size and quality:** raise CRF (20–23) or lower the preset speed for smaller files; keep `+faststart` for web playback; offer a separate lower-bitrate rendition instead of degrading the master.
- **Audio rights:** uploaded audio is the user's responsibility; generated audio comes only from a configured, licensed provider. Never fetch music from a URL.
- **Temp files** go in `data/tmp` and are removed in `finally`. Generated assets are deleted with their project; user uploads are not.
- **Long work runs in the queue**, never inside an HTTP request.

## Debugging a bad output

`ffprobe -v error -show_streams -show_format <file>` on the output and on each input clip first. Wrong length → trim/tpad values. Stretched picture → the scale/crop chain and the first clip's size. Silent film → whether any clip has an audio stream and whether tracks resolved. Out-of-sync voice-over → scene durations versus `adelay` offsets.
