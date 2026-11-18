#!/usr/bin/env bash
# Adds the voice-over to the motion graphic.
#   bash mux.sh <audio file> [output.mp4]
# - video stream is copied untouched from the video-only master (length kept)
# - audio is encoded AAC 192 kb/s stereo 48 kHz and starts at 0.15 s
# - audio is padded with silence, or cut, to the video length
# No music is added.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="tbc-restaurants-company_job-advert_motion-direction-a_ar_v03"
MASTER="$HERE/_work/${NAME}_video-only.mp4"
AUDIO="${1:?usage: bash mux.sh <audio file> [output.mp4]}"
OUT="${2:-$HERE/${NAME}.mp4}"
OFFSET_MS=150
[ -f "$MASTER" ] || { echo "missing video master: $MASTER (run _work/encode.sh first)"; exit 1; }
[ -f "$AUDIO" ]  || { echo "missing audio file: $AUDIO"; exit 1; }
VDUR="$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$MASTER")"
ADUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO")"
echo "video ${VDUR}s, audio ${ADUR}s, audio starts at 0.15s"
awk -v a="$ADUR" -v v="$VDUR" 'BEGIN { if (a + 0.15 > v) print "WARNING: the voice-over runs past the end of the video and will be cut; lengthen \"duration\" in timeline.json and re-render." }'
TMP="${OUT%.mp4}.tmp.mp4"
ffmpeg -y -v error -i "$MASTER" -i "$AUDIO" \
  -filter_complex "[1:a]aresample=48000,adelay=${OFFSET_MS}:all=1,apad[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -ac 2 -t "$VDUR" -movflags +faststart "$TMP"
mv "$TMP" "$OUT"
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration,bit_rate -of compact "$OUT"
echo "wrote $OUT"
