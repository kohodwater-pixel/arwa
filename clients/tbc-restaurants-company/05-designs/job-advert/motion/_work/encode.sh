#!/usr/bin/env bash
# Frames -> video-only master (H.264 High level 4.2, yuv420p, 30 fps). The voice is added by ../mux.sh.
set -euo pipefail
W="$(cd "$(dirname "$0")" && pwd)"; M="$(dirname "$W")"
NAME="tbc-restaurants-company_job-advert_motion-direction-a_ar_v04"
ffmpeg -y -v error -framerate 30 -i "$W/frames/f_%04d.jpg" -c:v libx264 -profile:v high -level:v 4.2 -preset slow -crf 17 -pix_fmt yuv420p \
  -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p" -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -r 30 -movflags +faststart "$W/${NAME}_video-only.mp4"
echo "wrote video-only master $W/${NAME}_video-only.mp4 — now run: bash mux.sh <audio file>"
