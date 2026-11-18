#!/usr/bin/env bash
# Builds the film's sound and muxes it onto the video-only master.
#   bash mux.sh [voice file] [--voice-only] [-o output.mp4]
# - voice file defaults to "voice_file" in timeline.json
# - full mix = voice + the "sfx" cue list in timeline.json; --voice-only leaves the effects out
# - voice: two-pass EBU R128 normalisation to -16 LUFS / -1.5 dBTP, placed at "audio_offset"
# - effects: each cue gets its gain, 5 ms fade-in and 40 ms fade-out, and is placed at its time
# - the sum (no auto-levelling) goes through a limiter, is padded to the video length,
#   and is encoded AAC 192 kb/s stereo 48 kHz. The video stream is copied untouched.
# No music is added.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$HERE/_work/mux_mix.py" "$@"
