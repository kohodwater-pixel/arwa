#!/usr/bin/env bash
# v02 piece A timing. seg1: frames 1-29 at 100 % (out frame k = source frame 1 + 0.8 k).
# The fall and wobble (frames 29-45) are used as they are, one per output frame. seg2: frames 45-193 at 115 %.
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p _work/A3_seg1 _work/A3_seg2
MI="mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none"
ffmpeg -v error -y -framerate 24 -start_number 1 -i _work/A3_clean/%03d.png -vf "trim=end_frame=29,minterpolate=fps=30:$MI" -start_number 0 _work/A3_seg1/%03d.png
ffmpeg -v error -y -framerate 24 -start_number 45 -i _work/A3_clean/%03d.png -vf "minterpolate=fps=600/23:$MI" -start_number 0 _work/A3_seg2/%03d.png
ls _work/A3_seg1 | wc -l; ls _work/A3_seg2 | wc -l
