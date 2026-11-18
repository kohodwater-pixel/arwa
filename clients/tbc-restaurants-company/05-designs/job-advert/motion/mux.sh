#!/usr/bin/env bash
# Adds the voice-over to the motion graphic.
#   bash mux.sh <audio file> [output.mp4]
# - video stream is copied untouched from the video-only master (length kept)
# - audio: two-pass EBU R128 loudness normalisation to -16 LUFS, true peak -1.5 dBTP,
#   then placed at 0.15 s, padded with silence to the video length, AAC 192 kb/s stereo 48 kHz
# No music is added.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="tbc-restaurants-company_job-advert_motion-direction-a_ar_v04"
MASTER="$HERE/_work/${NAME}_video-only.mp4"
AUDIO="${1:?usage: bash mux.sh <audio file> [output.mp4]}"
OUT="${2:-$HERE/${NAME}.mp4}"
OFFSET_MS=150
TARGET="I=-16:TP=-1.5:LRA=11"
[ -f "$MASTER" ] || { echo "missing video master: $MASTER (run _work/capture.cjs and _work/encode.sh first)"; exit 1; }
[ -f "$AUDIO" ]  || { echo "missing audio file: $AUDIO"; exit 1; }
VDUR="$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$MASTER")"
ADUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO")"
echo "video ${VDUR}s, audio ${ADUR}s, audio starts at 0.15s"
awk -v a="$ADUR" -v v="$VDUR" 'BEGIN { if (a + 0.15 > v) print "WARNING: the voice-over runs past the end of the video and will be cut; lengthen \"duration\" in timeline.json and re-render." }'
# pass 1: measure
M="$(ffmpeg -hide_banner -nostats -i "$AUDIO" -af "loudnorm=${TARGET}:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')"
val() { printf '%s' "$M" | sed -n "s/.*\"$1\" *: *\"\([^\"]*\)\".*/\1/p"; }
II="$(val input_i)"; ITP="$(val input_tp)"; ILRA="$(val input_lra)"; ITH="$(val input_thresh)"; OFF="$(val target_offset)"
[ -n "$II" ] || { echo "loudness measurement failed"; exit 1; }
echo "measured: ${II} LUFS, true peak ${ITP} dBTP, LRA ${ILRA}"
# pass 2: normalise with the measured values, place and pad
TMP="${OUT%.mp4}.tmp.mp4"
ffmpeg -y -v error -i "$MASTER" -i "$AUDIO" \
  -filter_complex "[1:a]loudnorm=${TARGET}:measured_I=${II}:measured_TP=${ITP}:measured_LRA=${ILRA}:measured_thresh=${ITH}:offset=${OFF}:linear=true,aresample=48000,adelay=${OFFSET_MS}:all=1,apad[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -ac 2 -t "$VDUR" -movflags +faststart "$TMP"
mv "$TMP" "$OUT"
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration,bit_rate -of compact "$OUT"
echo "wrote $OUT"
