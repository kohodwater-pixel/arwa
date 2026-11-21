"""HunyuanVideo 1.5 — command from Tencent-Hunyuan/HunyuanVideo-1.5 README.md:286-300 and generate.py
(commit 60783e7). Prompt rewriting and super-resolution are switched off here: rewriting needs a large
external LLM endpoint, and SR changes the output size. NOT yet run on a GPU by us."""


def build(spec, cfg, out_path, image_path=None, lora_path=None):
    from . import RunnerError
    if not cfg.get("model_path"):
        raise RunnerError("model_path is not configured")
    argv = [cfg.get("python", "python"), "generate.py", "--prompt", spec["prompt"], "--image_path", image_path or "none",
            "--resolution", spec["resolution"], "--aspect_ratio", spec["aspect"], "--seed", str(spec["seed"]),
            "--video_length", str(spec["frames"]), "--rewrite", "false", "--sr", "false",
            "--output_path", out_path, "--model_path", cfg["model_path"]]
    if spec.get("steps"):
        argv += ["--num_inference_steps", str(spec["steps"])]
    if spec.get("negativePrompt"):
        argv += ["--negative_prompt", spec["negativePrompt"]]
    if lora_path:
        argv += ["--lora_path", lora_path]  # present in generate.py:434, undocumented in the README
    argv += cfg.get("flags", [])
    return {"argv": argv, "cwd": cfg["repo"]}
