"""Mock runner: NO model is called. It renders a labelled placeholder with ffmpeg at the size, frame
rate and length the job asked for, so the control plane, the platform adapter and the evaluation
plumbing can be exercised on a machine without a GPU. The engine marks every such output as mock."""
import shutil


def build(spec, cfg, out_path, image_path=None, lora_path=None):
    from . import RunnerError
    if not shutil.which("ffmpeg"):
        raise RunnerError("ffmpeg not found")
    dur = spec["frames"] / spec["fps"]
    vf = "format=yuv420p"
    font = cfg.get("font")
    if font:
        f = font.replace(":", "\\:")
        size = max(14, min(spec["width"], spec["height"]) // 22)
        vf = (f"drawbox=x=0:y=0:w=iw:h={size * 2}:color=0xE5484D@0.92:t=fill,"
              f"drawtext=fontfile='{f}':text='MOCK WORKER - NO MODEL WAS RUN':fontcolor=white:fontsize={size}:x=(w-text_w)/2:y={size // 2},"
              f"drawtext=fontfile='{f}':text='{spec['width']}x{spec['height']}  {spec['frames']}f @ {spec['fps']}fps':fontcolor=white@0.8:fontsize={size}:x={size}:y=h-{size * 2},format=yuv420p")
    argv = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
            f"gradients=s={spec['width']}x{spec['height']}:d={dur}:r={spec['fps']}:c0=0x0B0F1A:c1=0x1B2A4A:c2=0x43226B:nb_colors=3:speed=0.02",
            "-vf", vf, "-frames:v", str(spec["frames"]), "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", out_path]
    return {"argv": argv, "cwd": None}
