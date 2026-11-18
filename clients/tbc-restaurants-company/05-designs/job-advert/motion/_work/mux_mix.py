"""Sound build for the motion graphic; called by ../mux.sh (see the usage there)."""
import json, os, re, subprocess, sys
W = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(W)
NAME = "tbc-restaurants-company_job-advert_motion-direction-a_ar_v04"
MASTER = os.path.join(W, NAME + "_video-only.mp4")
TL = json.load(open(os.path.join(M, "timeline.json"), encoding="utf-8"))
args = sys.argv[1:]
voice_only = "--voice-only" in args
out = None
if "-o" in args:
    out = args[args.index("-o") + 1]; del args[args.index("-o"):args.index("-o") + 2]
pos = [a for a in args if not a.startswith("--")]
voice = pos[0] if pos else os.path.join(M, TL["voice_file"])
out = out or os.path.join(M, NAME + ("_voice-only" if voice_only else "") + ".mp4")
for f in (MASTER, voice):
    if not os.path.isfile(f): sys.exit("missing file: " + f)

def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

vdur, adur, off = dur(MASTER), dur(voice), TL["audio_offset"]
print(f"video {vdur:.2f}s, voice {adur:.2f}s placed at {off}s, {'voice only' if voice_only else str(len(TL['sfx'])) + ' sfx cues'}")
if adur + off > vdur: print("WARNING: the voice runs past the end of the video and will be cut; lengthen 'duration' in timeline.json and re-render.")
TARGET = "I=-16:TP=-1.5:LRA=11"
p1 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", voice, "-af", f"loudnorm={TARGET}:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1, re.S).group(0))
print(f"voice measured: {m['input_i']} LUFS, true peak {m['input_tp']} dBTP")
cmd = ["ffmpeg", "-y", "-v", "error", "-i", MASTER, "-i", voice]
chains = [f"[1:a]loudnorm={TARGET}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,adelay={round(off * 1000)}:all=1[v0]"]
labels = ["[v0]"]
if not voice_only:
    for i, c in enumerate(TL["sfx"]):
        f = os.path.join(M, c["file"])
        if not os.path.isfile(f): sys.exit("missing sfx: " + f)
        if c["t"] > vdur - 0.6: sys.exit(f"sfx cue at {c['t']}s is inside the last 0.6 s")
        d = dur(f); cmd += ["-i", f]
        chains.append(f"[{i + 2}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={c['gain_db']}dB,"
                      f"afade=t=in:d=0.005,afade=t=out:st={max(d - 0.04, 0):.3f}:d=0.04,adelay={round(c['t'] * 1000)}:all=1[s{i}]")
        labels.append(f"[s{i}]")
mix = "".join(labels) + (f"amix=inputs={len(labels)}:normalize=0:duration=longest," if len(labels) > 1 else "anull,")
chains.append(mix + "alimiter=limit=0.794:attack=2:release=50:level=0,apad[a]")   # 0.794 = -2 dBFS sample ceiling, margin for true peak
tmp = out[:-4] + ".tmp.mp4"
cmd += ["-filter_complex", ";".join(chains), "-map", "0:v:0", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000", "-t", f"{vdur:.3f}", "-movflags", "+faststart", tmp]
subprocess.run(cmd, check=True)
os.replace(tmp, out)
rep = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
s = rep[rep.rindex("Summary:"):]
I = re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1); LRA = re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1); TP = re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)
line = f"{os.path.basename(out)}: integrated {I} LUFS, loudness range {LRA} LU, true peak {TP} dBTP"
print(line); print("wrote", out)
open(os.path.join(W, "loudness_" + os.path.basename(out)[:-4] + ".txt"), "w", encoding="utf-8").write(line + "\n(measured on the final file with ffmpeg ebur128=peak=true)\n")
