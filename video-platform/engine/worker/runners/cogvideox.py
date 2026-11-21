"""CogVideoX-2B — command from THUDM/CogVideo inference/cli_demo.py (commit 7a1af71). Baseline only.
NOT yet run on a GPU by us."""


def build(spec, cfg, out_path, image_path=None, lora_path=None):
    argv = [cfg.get("python", "python"), "inference/cli_demo.py", "--prompt", spec["prompt"],
            "--model_path", cfg.get("model_path", spec["modelPath"]), "--generate_type", "t2v",
            "--num_frames", str(spec["frames"]), "--num_inference_steps", str(spec["steps"]),
            "--width", str(spec["width"]), "--height", str(spec["height"]), "--fps", str(spec["fps"]),
            "--seed", str(spec["seed"]), "--output_path", out_path]
    if lora_path:
        argv += ["--lora_path", lora_path]
    return {"argv": argv + cfg.get("flags", []), "cwd": cfg["repo"]}
