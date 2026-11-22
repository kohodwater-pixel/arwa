#!/usr/bin/env bash
# Cleaned piece A (24 fps) -> 30 fps by motion-compensated interpolation. Out frame k = source frame 0.8*k.
# Takes about 3 minutes.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p _work/A_30
ffmpeg -v error -y -framerate 24 -i _work/A_clean/%03d.png \
  -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none" \
  -start_number 0 _work/A_30/%03d.png
ls _work/A_30 | wc -l
