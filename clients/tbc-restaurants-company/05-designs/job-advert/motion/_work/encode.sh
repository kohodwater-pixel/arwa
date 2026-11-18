#!/usr/bin/env bash
# Frames -> video-only master (H.264 yuv420p, 30 fps) -> silent deliverable with a silent AAC track.
set -euo pipefail
W="$(cd "$(dirname "$0")" && pwd)"; M="$(dirname "$W")"
NAME="tbc-restaurants-company_job-advert_motion-direction-a_ar_v03"
ffmpeg -y -v error -framerate 30 -i "$W/frames/f_%04d.jpg" -c:v libx264 -profile:v high -level:v 4.2 -preset slow -crf 17 -pix_fmt yuv420p \
  -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p" -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -r 30 -movflags +faststart "$W/${NAME}_video-only.mp4"
VDUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/${NAME}_video-only.mp4")"
ffmpeg -y -v error -i "$W/${NAME}_video-only.mp4" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -t "$VDUR" -movflags +faststart "$M/${NAME}.mp4"
echo "wrote $M/${NAME}.mp4 (silent)"
