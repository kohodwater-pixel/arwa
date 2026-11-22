#!/usr/bin/env bash
# Rebuilds hippo_box-clip_9x16_ar_v02.mp4 (piece A = gen03, piece B = gen02 B, card v01, VO take 1).
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 src/v02/01_cleanup_A.py      # car nose and wall sign repainted flat -> _work/A3_clean
bash    src/v02/02_interp_A.sh       # -> _work/A3_seg1, _work/A3_seg2  (about 3 min)
python3 src/v02/03_render_video.py   # picture -> _work/video_v02_silent.mp4 (about 8 min)
python3 src/v02/04_audio.py          # mix -> _work/audio/mix_v02.wav
bash    src/v02/05_mux.sh            # final MP4
mkdir -p _work/chk
python3 src/v02/06_checks.py | tee _work/chk/checks_v02.txt
