"""Wan 2.2 — command from Wan-Video/Wan2.2 README.md:147,198,229 and generate.py (commit 1ea34ff).
NOT yet run on a GPU by us: confirm on first deployment."""


def build(spec, cfg, out_path, image_path=None, lora_path=None):
    from . import RunnerError
    task = spec["wanTask"]
    ckpt = cfg.get("checkpoints", {}).get(task)
    if not ckpt:
        raise RunnerError(f"no checkpoint directory configured for {task}")
    if lora_path:
        # The official generate.py has no general LoRA flag. LoRA inference needs another backend.
        raise RunnerError("LoRA requested, but this worker runs the official Wan generate.py, which cannot load LoRAs. "
                          "Configure a musubi-tuner or ComfyUI backend for LoRA jobs.")
    argv = [cfg.get("python", "python"), "generate.py", "--task", task, "--size", spec["size"], "--ckpt_dir", ckpt,
            "--frame_num", str(spec["frames"]), "--base_seed", str(spec["seed"]), "--prompt", spec["prompt"], "--save_file", out_path]
    if spec.get("steps"):
        argv += ["--sample_steps", str(spec["steps"])]
    if image_path:
        argv += ["--image", image_path]
    argv += cfg.get("flags", ["--offload_model", "True", "--convert_model_dtype"])
    return {"argv": argv, "cwd": cfg["repo"]}
