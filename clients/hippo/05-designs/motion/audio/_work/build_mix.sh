#!/bin/bash
# Audio mix v01 for the HIPPO franchise motion ad (40 s). Run from audio/_work/.
set -e
VO=../hippo_franchise-motion-ad_vo-test-take2_ar_v01.mp3
OUT=../hippo_franchise-motion-ad_audio-mix_ar_v01
seg(){ echo "[0:a]atrim=$1:$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=$(echo "$2 $1" | awk '{printf "%.2f", $1-$2-0.04}'):d=0.04,adelay=$3:all=1[v$4];"; }
# 1) voice track: lines placed on the scene timings
F="$(seg 0 2.10 1700 1)$(seg 2.30 4.25 4600 2)$(seg 4.52 5.62 10000 3)$(seg 5.75 6.70 12800 4)$(seg 6.87 9.15 15500 5)$(seg 9.40 11.40 20400 6)$(seg 11.58 15.22 25000 7)$(seg 15.34 16.80 30300 8)$(seg 16.94 20.61 34200 9)"
ffmpeg -v error -y -i $VO -filter_complex "$F[v1][v2][v3][v4][v5][v6][v7][v8][v9]amix=inputs=9:normalize=0,acompressor=threshold=-18dB:ratio=3:attack=5:release=120:makeup=3,highpass=f=70,apad=whole_dur=40,atrim=0:40,aresample=48000" -ac 2 vo_track.wav
# 2) effects track
th(){ echo "[2:a]asetrate=44100*$1,aresample=48000,volume=$2,adelay=$3:all=1[t$4];"; }
sub(){ echo "aevalsrc='sin(2*PI*($1*t-$2*t*t))*exp(-$3*t)':d=1.6:s=48000,volume=$4,adelay=$5:all=1[s$6];"; }
ffmpeg -v error -y -i sfx_hook.mp3 -i sfx_boom.mp3 -i sfx_thud.mp3 -i sfx_slide.mp3 -filter_complex "
[0:a]atrim=0.45:6,asetpts=PTS-STARTPTS,aresample=48000,volume=2.2,adelay=50:all=1[hook];
[0:a]atrim=1.25:5,asetpts=PTS-STARTPTS,aresample=48000,volume=1.8,adelay=29450:all=1[hook2];
[1:a]aresample=48000,volume=1.6,adelay=19000:all=1[boom];
[1:a]atrim=0.39:2.6,asetpts=PTS-STARTPTS,areverse,afade=t=in:d=1.5,aresample=48000,volume=0.5,adelay=27350:all=1[riser];
[3:a]aresample=48000,volume=18,alimiter=limit=0.5,adelay=3100:all=1[slide];
$(th 1.0 1.3 7070 1)$(th 0.9 1.3 8370 2)$(th 1.08 1.3 9670 3)$(th 0.7 1.8 12320 4)$(th 0.95 1.0 15070 5)$(th 1.02 1.0 15870 6)$(th 1.09 1.0 16670 7)$(th 1.16 1.0 17470 8)$(th 1.24 1.1 18170 9)$(th 0.8 0.9 33100 10)
$(sub 62 13 2.6 0.95 1000 1)$(sub 50 9 3.2 0.7 12450 2)$(sub 55 12 2.0 1.0 19390 3)$(sub 62 13 2.6 0.9 29600 4)
[hook][hook2][boom][riser][slide][t1][t2][t3][t4][t5][t6][t7][t8][t9][t10][s1][s2][s3][s4]amix=inputs=19:normalize=0,apad=whole_dur=40,atrim=0:40" -ac 2 sfx_track.wav
# 3) music: enters on the hook impact (1.0 s), stops for the silence of scene 7 (24.0 s), returns on the CTA (29.6 s) with the track's own ending
ffmpeg -v error -y -i music.mp3 -filter_complex "
[0:a]atrim=0:23,asetpts=PTS-STARTPTS,afade=t=out:st=22.92:d=0.08,aresample=48000,adelay=1000:all=1[m1];
[0:a]atrim=22.5:40,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=10.1:d=0.3,aresample=48000,adelay=29600:all=1[m2];
[m1][m2]amix=inputs=2:normalize=0,volume=0.55,apad=whole_dur=40,atrim=0:40" -ac 2 music_track.wav
# 4) final: music ducks under the voice; limiter; loudness -14 LUFS
ffmpeg -v error -y -i vo_track.wav -i sfx_track.wav -i music_track.wav -filter_complex "
[0:a]asplit=2[vo][key];[2:a][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[mduck];
[vo]volume=1.5[vo2];[vo2][1:a][mduck]amix=inputs=3:normalize=0,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000" -ac 2 $OUT.wav
ffmpeg -v error -y -i $OUT.wav -b:a 256k $OUT.mp3
