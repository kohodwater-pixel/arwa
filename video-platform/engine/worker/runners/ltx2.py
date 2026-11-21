"""LTX-2.5 — command from Lightricks/LTX-2 README.md:50-59,79-89 and ltx_pipelines args (v1.6.2).
The repository publishes no VRAM figure; measure before offering it. NOT yet run on a GPU by us.
Licence: weights need a written answer from Lightricks before paid use (see models/ltx2.js)."""

PATH_FLAGS = [("transformer", "--transformer-path"), ("text_encoder", "--text-encoder-path"), ("video_vae", "--video-vae-path"),
              ("audio_vae", "--audio-vae-path"), ("spatial_upsampler", "--spatial-upsampler-path")]


def build(spec, cfg, out_path, image_path=None, lora_path=None):
    from . import RunnerError
    paths = cfg.get("paths", {}).get(spec["pipeline"], {})
    argv = list(cfg.get("launcher", ["uv", "run", "python"])) + ["-m", spec["pipeline"]]
    for key, flag in PATH_FLAGS:
        if not paths.get(key):
            raise RunnerError(f"path for {key} is not configured for {spec['pipeline']}")
        argv += [flag, paths[key]]
    if paths.get("detailing_lora"):
        argv += ["--detailing-lora", paths["detailing_lora"]]
    argv += ["--height", str(spec["height"]), "--width", str(spec["width"]), "--frame-rate", str(spec["fps"]),
             "--num-frames", str(spec["frames"]), "--seed", str(spec["seed"]), "--output-path", out_path, "--prompt", spec["prompt"]]
    if image_path:
        argv += ["--image", image_path, "0", "1.0"]
    if lora_path:
        argv += ["--lora", lora_path, str(spec.get("lora", {}).get("strength", 1.0))]
    argv += cfg.get("flags", [])
    return {"argv": argv, "cwd": cfg["repo"]}
