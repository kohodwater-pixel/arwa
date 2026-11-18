#!/bin/bash
# Audio mix v02 for the HIPPO franchise motion ad (40.000 s, 48 kHz stereo). Run from anywhere.
# Built from sound-panel_mix_2026-11-18.md + sound-panel_direction_2026-11-18.md + the Creative Director's rulings.
# Does not touch build_mix.sh or any v01 file. All stems are 32-bit float (no 16-bit clipping between stages).
# All film times below are seconds; "landing" = onset of the hit. Nobody has listened to this: see mix-v02_report_2026-11-18.md.
set -euo pipefail
cd "$(dirname "$0")"
VO=../hippo_franchise-motion-ad_vo-test-take2_ar_v01.mp3
OUT=../hippo_franchise-motion-ad_audio-mix_ar_v02
FF="ffmpeg -v error -y"
smp(){ awk "BEGIN{printf \"%d\", ($1)*48000+0.5}"; }          # seconds -> samples (for sample-exact adelay)

# ---- mix levels (linear gains unless marked dB); tuned by measurement on 2026-11-18 ----
VO_GAIN=${VO_GAIN:-1.5}        # voice into the final bus (as v01)
MUS_GAIN=${MUS_GAIN:-0.70}     # music before ducking
DUCK=${DUCK:-threshold=0.035:ratio=2:attack=20:release=600}
ROOM_GAIN=${ROOM_GAIN:-1.0}    # room-tone bed trim
REV_GAIN=${REV_GAIN:-1.0}      # shared room reverb return (effects only)
MASTER_DB=${MASTER_DB:-0.8}      # fixed master gain before the limiter
HOOK_DB=${HOOK_DB:-2}          # trim of the whole hook hit (1.000)
BOX_DB=${BOX_DB:--1.5}            # trim of the whole box hit (19.400)
CTA_DB=${CTA_DB:--2.5}            # trim of the whole CTA hit (29.600)

# =====================================================================================
# 1) VOICE: corrected cut points (take seconds), same film placements as v01, voice stays dry
#    seg <take in> <take out> <film start> <label>
seg(){ echo "[0:a]atrim=$1:$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=$(awk "BEGIN{printf \"%.3f\", $2-$1-0.04}"):d=0.04,aresample=48000,adelay=$(smp $3)S:all=1[v$4];"; }
F="$(seg 0.00 2.10 1.700 1)$(seg 2.30 4.40 4.600 2)$(seg 4.52 5.62 10.000 3)$(seg 5.70 6.76 12.750 4)$(seg 6.87 9.25 15.500 5)$(seg 9.40 11.54 20.400 6)$(seg 11.58 15.22 25.000 7)$(seg 15.34 16.80 30.300 8)$(seg 16.94 20.56 34.200 9)"
# voice-only peak limiter at -3 dBFS so the master limiter is left for the hits; its 3 ms look-ahead is trimmed off
# +3 dB on «ثقيل» (12.70-13.90); +5 dB on «أثقل» (21.60-22.70) because its loud first syllable is held by the peak limiter,
# so +3 dB moved the word by only 0.3 dB. Both switch points fall in silence of the voice track
$FF -i $VO -filter_complex "$F anullsrc=r=48000:cl=mono:d=40[z];[z][v1][v2][v3][v4][v5][v6][v7][v8][v9]amix=inputs=10:normalize=0,acompressor=threshold=-18dB:ratio=3:attack=5:release=120:makeup=3,highpass=f=70,asetnsamples=n=480,volume='1+0.413*between(t,12.70,13.90)+0.778*between(t,21.60,22.70)':eval=frame,aresample=192000,alimiter=limit=0.71:level=0:attack=3:release=60,aresample=48000,atrim=start=0.003,asetpts=PTS-STARTPTS,apad=whole_dur=40,atrim=0:40" -ac 2 -c:a pcm_f32le vo_track_v02.wav

# =====================================================================================
# 2) REVERB IMPULSE (synthetic short room, about 0.3 s) and ROOM TONE (synthetic, band-limited brown noise)
$FF -f lavfi -i "anoisesrc=d=0.32:c=white:r=48000:a=1:seed=11" -f lavfi -i "anoisesrc=d=0.32:c=white:r=48000:a=1:seed=29" -filter_complex "
[0:a]asetnsamples=n=32,volume='exp(-20*t)':eval=frame,highpass=f=300,lowpass=f=5000[l];
[1:a]asetnsamples=n=32,volume='exp(-20*t)':eval=frame,highpass=f=300,lowpass=f=5000[r];
[l][r]join=inputs=2:channel_layout=stereo,afade=t=out:st=0.27:d=0.05" -c:a pcm_f32le ir_room_v02.wav
# room tone: about -45 dBFS, lifted 7 dB during the music stop (24.0-28.7); hard mute 0.92-1.00 and 29.52-29.60 is applied on the effects bus below
$FF -f lavfi -i "anoisesrc=d=40:c=brown:r=48000:a=1:seed=3" -f lavfi -i "anoisesrc=d=40:c=brown:r=48000:a=1:seed=7" -filter_complex "
[0:a]highpass=f=120,lowpass=f=2500[l];[1:a]highpass=f=120,lowpass=f=2500[r];
[l][r]join=inputs=2:channel_layout=stereo,asetnsamples=n=480,volume='0.035*$ROOM_GAIN*(1+1.24*min(1,max(0,min((t-23.95)/0.15,(28.75-t)/0.15))))':eval=frame,afade=t=in:d=0.05,afade=t=out:st=39.85:d=0.15,atrim=0:40" -c:a pcm_f32le room_track_v02.wav

# =====================================================================================
# 3) EFFECTS
# inputs: 0 hook, 1 boom, 2 thud, 3 impact_mid, 4 whoosh, 5 cup, 6 squish, 7 paper
# thud: onset is 0.135 s into the file -> trim at 0.125, so the attack sits 0.021/rate s after the start
th(){ echo "[2:a]atrim=start=0.125,asetpts=PTS-STARTPTS,asetrate=44100*$1,aresample=48000,volume=$2,adelay=$(smp "$3-0.021/$1")S:all=1[$4];"; }
# sub hit: sine sweep f0 -> down, exponential decay, 0.1 s fade at the end (no cut-off step)
sub(){ echo "aevalsrc='sin(2*PI*($1*t-$2*t*t))*exp(-$3*t)':d=$7:s=48000,afade=t=out:st=$(awk "BEGIN{printf \"%.2f\", $7-0.1}"):d=0.1,volume=$4,adelay=$(smp $5)S:all=1[$6];"; }
# paper hit: <src in> <src out> <rate> <gain> <film time of the hit> <label>; each source hit starts 0.010 s after <src in>
pp(){ echo "[7:a]atrim=$1:$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.003,afade=t=out:st=$(awk "BEGIN{printf \"%.3f\", $2-$1-0.03}"):d=0.03,asetrate=44100*$3,aresample=48000,volume=$4,adelay=$(smp "$5-0.010/$3")S:all=1[$6];"; }
# cup tap: tap peak is 0.151 s into the file -> trim at 0.125; the tap sits 0.026/rate after the start
cup(){ echo "[5:a]atrim=0.125:0.75,asetpts=PTS-STARTPTS,afade=t=out:st=0.5:d=0.12,asetrate=44100*$1,aresample=48000,volume=$2,adelay=$(smp "$3-0.026/$1")S:all=1[$4];"; }
# soft clipper, explicitly 4x oversampled. The 0.513 pre-gain reproduces what ffmpeg 6.1's asoftclip=oversample=4 did
# (it halves the level before the curve); all gains below were tuned by measurement with this in place.
CLIP='aresample=192000,volume=0.513,asoftclip=type=tanh,aresample=48000'
HK=$(awk "BEGIN{printf \"%.4f\", 10^($HOOK_DB/20)}"); BX=$(awk "BEGIN{printf \"%.4f\", 10^($BOX_DB/20)}"); CT=$(awk "BEGIN{printf \"%.4f\", 10^($CTA_DB/20)}")

$FF -i sfx_hook.mp3 -i sfx_boom.mp3 -i sfx_thud.mp3 -i sfx_impact_mid.mp3 -i sfx_whoosh.mp3 -i sfx_cup.mp3 -i sfx_squish.mp3 -i sfx_paper.mp3 -i ir_room_v02.wav -i room_track_v02.wav -filter_complex "
anullsrc=r=48000:cl=stereo:d=40[z];

[7:a]atrim=1.715:1.800,asetpts=PTS-STARTPTS,afade=t=in:d=0.003,afade=t=out:st=0.055:d=0.03,aresample=48000,volume=3.8,adelay=$(smp 0.090)S:all=1[tick];
[4:a]areverse,atrim=0:0.345,asetpts=PTS-STARTPTS,atempo=0.734,afade=t=in:d=0.08,afade=t=out:st=0.462:d=0.008,aresample=48000,volume=1.2,adelay=$(smp 0.450)S:all=1[whoosh];

$(sub 62 13 2.0 "0.90*$HK" 1.000 hsub 1.6)
aevalsrc='sin(2*PI*(170*t-80*t*t))*exp(-7*t)':d=0.6:s=48000,volume=4,$CLIP,afade=t=out:st=0.5:d=0.1,volume=0.45*$HK,adelay=$(smp 1.000)S:all=1[hbody];
[3:a]atrim=start=0.030,asetpts=PTS-STARTPTS,afade=t=in:d=0.002,highpass=f=220,aresample=48000,volume=2.5*$HK,adelay=$(smp 1.000)S:all=1[hmid];
[3:a]atrim=start=0.030,asetpts=PTS-STARTPTS,afade=t=in:d=0.002,asetrate=44100*0.72,aresample=48000,highpass=f=250,volume=2.5*$HK,adelay=$(smp 1.000)S:all=1[hmid2];
[0:a]atrim=1.36:2.40,asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st=0.25:d=0.75,aresample=48000,volume=1.1*$HK,adelay=$(smp 1.000)S:all=1[hrum];
[0:a]atrim=1.36:2.40,asetpts=PTS-STARTPTS,afade=t=in:d=0.004,highpass=f=250,highpass=f=250,afade=t=out:st=0.35:d=0.45,aresample=48000,volume=10.0*$HK,adelay=$(smp 1.000)S:all=1[hair];
$(th 0.80 "1.2*$HK" 1.000 hthud)
$(pp 3.425 3.580 1.00 4.0 1.020 hpap)$(pp 6.655 6.800 0.70 0.55 1.020 hpap2)

$(cup 1.00 0.60 3.138 c1)$(cup 1.06 0.60 3.523 c2)$(cup 1.12 0.60 3.907 c3)$(cup 1.19 0.62 4.291 c4)
[6:a]atrim=0.125:0.75,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=0.5:d=0.12,aresample=48000,volume=3.4,adelay=$(smp 6.600)S:all=1[squish];

$(th 1.00 0.80 7.200 t1)$(th 0.90 0.80 8.500 t2)$(th 1.08 0.80 9.800 t3)
$(pp 0.665 0.800 1.00 0.60 7.220 p1)$(pp 5.620 5.760 0.95 1.9 8.520 p2)$(pp 6.355 6.560 1.05 0.60 9.820 p3)

$(th 0.70 1.10 12.500 t4)$(sub 50 9 3.2 0.50 12.500 s2 1.6)

$(th 0.95 0.62 15.200 t5)$(th 1.02 0.62 16.000 t6)$(th 1.09 0.62 16.800 t7)$(th 1.16 0.62 17.600 t8)$(th 1.24 0.70 18.300 t9)
$(pp 2.075 2.180 1.00 2.4 15.220 p5)$(pp 3.425 3.580 1.10 1.6 16.020 p6)$(pp 5.620 5.760 1.15 1.9 16.820 p7)$(pp 0.665 0.800 1.20 0.60 17.620 p8)$(pp 6.355 6.560 1.25 0.62 18.320 p9)

[1:a]pan=mono|c0=c0,atrim=start=0.385,asetpts=PTS-STARTPTS,afade=t=in:d=0.004,asetrate=44100*0.85,aresample=48000,afade=t=out:st=2.6:d=1.6,volume=1.25*$BX,adelay=$(smp "19.400-0.015/0.85")S:all=1[boom];
$(sub 48 8 1.5 "0.80*$BX" 19.400 s3 2.2)
$(th 0.62 "0.9*$BX" 19.400 tbox)
$(pp 6.655 6.800 0.60 "0.50*$BX" 19.420 pbox)
$(pp 6.355 6.560 0.75 0.42 19.520 lid1)$(pp 3.425 3.580 0.70 1.0 19.740 lid2)$(pp 5.620 5.760 0.70 0.85 19.980 lid3)

[1:a]pan=mono|c0=c0,atrim=0.42:1.24,asetpts=PTS-STARTPTS,areverse,afade=t=in:d=0.55,afade=t=out:st=0.81:d=0.01,aresample=48000,volume=1.6,adelay=$(smp 28.700)S:all=1[riser];
[0:a]atrim=1.36:4.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st=0.6:d=2.4,aresample=48000,volume=1.0*$CT,adelay=$(smp 29.600)S:all=1[crum];
$(sub 62 13 2.6 "0.45*$CT" 29.600 s4 1.6)
$(th 0.90 "0.8*$CT" 29.600 tcta)
[3:a]atrim=start=0.030,asetpts=PTS-STARTPTS,afade=t=in:d=0.002,highpass=f=150,aresample=48000,volume=1.2*$CT,adelay=$(smp 29.600)S:all=1[cmid];

$(th 0.80 0.60 33.300 t10)

aevalsrc='(sin(2*PI*(95*t-40*t*t))+0.35*sin(2*PI*(190*t-80*t*t))+0.15*sin(2*PI*(380*t-160*t*t)))*exp(-13*t)':d=0.32:s=48000,afade=t=in:d=0.006,afade=t=out:st=0.24:d=0.08,volume=0.58,adelay=$(smp 38.200)S:all=1[boop];
aevalsrc='sin(2*PI*2600*t)*exp(-90*t)+0.40*sin(2*PI*3000*max(t-0.045,0))*exp(-110*max(t-0.045,0))*gte(t,0.045)+0.25*sin(2*PI*3300*max(t-0.090,0))*exp(-120*max(t-0.090,0))*gte(t,0.090)':d=0.16:s=48000,afade=t=in:d=0.001,volume=0.22,adelay=$(smp 38.320)S:all=1[ltick];

[hsub][s2][s3][s4][boop]amix=inputs=5:normalize=0,$CLIP,aformat=channel_layouts=stereo[lows];
[z][tick][whoosh][hbody][hmid][hrum][hthud][hpap][hpap2][hmid2][hair][c1][c2][c3][c4][squish][t1][t2][t3][p1][p2][p3][t4][t5][t6][t7][t8][t9][p5][p6][p7][p8][p9][boom][tbox][pbox][lid1][lid2][lid3][riser][crum][tcta][cmid][t10][ltick]amix=inputs=45:normalize=0,$CLIP,aformat=channel_layouts=stereo,asplit=2[dry][send];
[send]highpass=f=200,adelay=576S:all=1,apad=whole_dur=41[send2];
[send2][8:a]afir=dry=0:wet=1:gtype=-1,volume=$REV_GAIN*0.05[wet];
[dry][lows][wet][9:a]amix=inputs=4:normalize=0,
asetnsamples=n=16,volume='min(1,max(0,max((0.920-t)/0.006,(t-0.998)/0.002)))*min(1,max(0,max((29.520-t)/0.006,(t-29.598)/0.002)))':eval=frame,
apad=whole_dur=40,atrim=0:40" -ac 2 -c:a pcm_f32le sfx_track_v02.wav

# =====================================================================================
# 4) MUSIC: music.mp3 slowed 2.44 % (asetrate, no time-stretch artefacts) so that 32 beats span 3.000 -> 19.400:
#    it enters on a beat at 3.000 (scene-2 cut) and its 8-second phrase turns over exactly on the box hit.
#    Hard stop at 24.000 (30 ms), full return on a phrase start at 29.600, long fade to silence by 39.9.
R=0.97561
$FF -i music.mp3 -filter_complex "
[0:a]atrim=0.160:20.660,asetpts=PTS-STARTPTS,asetrate=48000*$R,aresample=48000,afade=t=in:d=0.005,afade=t=out:st=20.970:d=0.030,atrim=0:21.000,adelay=$(smp 3.000)S:all=1[m1];
[0:a]atrim=16.160:26.500,asetpts=PTS-STARTPTS,asetrate=48000*$R,aresample=48000,afade=t=in:d=0.005,afade=t=out:st=7.7:d=2.6:curve=cub,atrim=0:10.300,adelay=$(smp 29.600)S:all=1[m2];
anullsrc=r=48000:cl=stereo:d=40[z];
[z][m1][m2]amix=inputs=3:normalize=0,volume=$MUS_GAIN,apad=whole_dur=40,atrim=0:40" -ac 2 -c:a pcm_f32le music_track_v02.wav

# =====================================================================================
# 5) FINAL: gentle ducking of music under the voice; fixed gain; 4x-oversampled limiter, level=0; no loudnorm.
#    The limiter's 5 ms look-ahead delay is trimmed off so film times stay exact.
$FF -i vo_track_v02.wav -i sfx_track_v02.wav -i music_track_v02.wav -filter_complex "
[0:a]asplit=2[vo][key];[2:a][key]sidechaincompress=$DUCK[mduck];
[vo]volume=$VO_GAIN[vo2];
[vo2][1:a][mduck]amix=inputs=3:normalize=0,volume=${MASTER_DB}dB,aresample=192000,alimiter=limit=0.82:level=0:attack=5:release=80,aresample=48000,atrim=start=0.005,asetpts=PTS-STARTPTS,apad=whole_dur=40,atrim=0:40" -ac 2 -c:a pcm_f32le mix_v02_f32.wav
$FF -i mix_v02_f32.wav -c:a pcm_s16le $OUT.wav
$FF -i $OUT.wav -b:a 256k $OUT.mp3
echo "built $OUT.wav / .mp3"
