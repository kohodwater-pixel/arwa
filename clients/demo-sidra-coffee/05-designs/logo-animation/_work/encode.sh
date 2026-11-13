#!/bin/sh
# Encode captured frames to MP4. Usage: sh _work/encode.sh <framesDir> <out.mp4>
# The explicit bt709 matrix in the scale filter matters: without it ffmpeg converts with bt601 while the file is tagged bt709, and Ember shifts.
ffmpeg -y -loglevel error -framerate 30 -i "$1/f%03d.png" -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p" -c:v libx264 -pix_fmt yuv420p -r 30 -crf 14 -preset slow -movflags +faststart -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv "$2"
