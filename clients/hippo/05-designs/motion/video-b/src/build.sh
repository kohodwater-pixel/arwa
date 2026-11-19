#!/usr/bin/env bash
# Full build: render 1200 frames (30 fps, 40 s) -> H.264 MP4 muxed with the approved audio mix (unchanged).
# Usage: bash build.sh [version]   (default v03). Frames go to ../_work/frames (git-ignored).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; VID="$HERE/.."; V="${1:-v03}"
AUDIO="$VID/../audio/hippo_franchise-motion-ad_audio-mix_ar_v02.wav"
OUT="$VID/hippo_franchise-motion-ad_9x16_ar_${V}.mp4"
rm -rf "$VID/_work/frames"; mkdir -p "$VID/_work/frames"
node "$HERE/render.cjs" frames "$VID/_work/frames"
n=$(ls "$VID/_work/frames" | wc -l); [ "$n" -eq 1200 ] || { echo "expected 1200 frames, got $n"; exit 1; }
ffmpeg -y -loglevel error -framerate 30 -i "$VID/_work/frames/f_%05d.png" -i "$AUDIO" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p" \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 256k -ar 48000 -t 40 -movflags +faststart "$OUT"
echo "wrote $OUT"
