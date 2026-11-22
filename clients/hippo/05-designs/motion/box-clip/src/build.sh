#!/usr/bin/env bash
# Rebuilds hippo_box-clip_9x16_ar_v01.mp4 from the two generated pieces, the card PNG and VO take 1.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/01_cleanup_A.py      # badges, wordmarks, plates painted out -> _work/A_clean
bash    src/02_interp_A.sh       # 24 -> 30 fps -> _work/A_30   (about 3 min)
python3 src/03_render_video.py   # picture -> _work/video_v01_silent.mp4 (about 3 min)
python3 src/04_audio.py          # mix -> _work/audio/mix_v01.wav
bash    src/05_mux.sh            # final MP4
mkdir -p _work/chk
python3 src/06_checks.py | tee _work/chk/checks_v01.txt
