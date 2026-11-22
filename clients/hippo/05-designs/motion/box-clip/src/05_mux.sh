#!/usr/bin/env bash
# Picture + mix -> final MP4 (H.264 High, yuv420p, 30 fps, AAC 48 kHz stereo, faststart).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=hippo_box-clip_9x16_ar_v01.mp4
ffmpeg -v error -y -i _work/video_v01_silent.mp4 -i _work/audio/mix_v01.wav \
  -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -maxrate 16M -bufsize 24M \
  -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart -t 17.5 "$OUT"
ls -la "$OUT"
