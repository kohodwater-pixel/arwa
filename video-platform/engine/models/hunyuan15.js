import { basePlan } from './_plan.js';
/**
 * HunyuanVideo 1.5 — Tencent-Hunyuan/HunyuanVideo-1.5 @ 60783e7 (2026-04-10). 8.3B DiT.
 * Exact pixel sizes are computed by the model from --resolution and --aspect_ratio; widths/heights here are nominal.
 */
export default {
  id: 'hunyuan15', label: 'HunyuanVideo 1.5', repo: 'https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5', docsCommit: '60783e7',
  license: {
    code: 'Tencent Hunyuan Community License', weights: 'Tencent Hunyuan Community License', commercial: 'conditions',
    notes: 'Territory is worldwide EXCLUDING the European Union, United Kingdom and South Korea, and that covers use of outputs too (LICENSE:17,35): users and delivery in those places must be blocked. Service must disclose the provider\'s legal name and non-affiliation with Tencent, carry the acceptable-use terms, and label content as machine generated. Above 100M monthly users a licence from Tencent is needed. Outputs may not be used to improve another AI model. Open risk: the vision encoder is taken from FLUX.1-Redux-dev (gated, its own licence, not in this repository) and must be cleared separately.',
  },
  prompt: { languages: ['en', 'zh'], maxChars: 2000, negative: true, note: 'Chinese and English only. Prompt rewriting is recommended and needs a large Qwen model behind a vLLM endpoint; without it quality may drop (README.md:231-239).' },
  lora: { trainers: ['musubi-tuner (text- and image-to-video, marked experimental)', 'diffusion-pipe (LoRA and full fine-tune)', 'train.py in the repository (you write the data loader)'], format: 'safetensors', note: '--lora_path exists in generate.py but is not documented in the README.' },
  variants: [
    { id: '720p', label: '720p 24 fps', tier: 'high', tasks: ['t2v', 'i2v'], resolution: '720p',
      sizes: { '16:9': [1280, 720], '9:16': [720, 1280], '1:1': [960, 960] }, fps: 24, steps: 50, frames: { min: 25, max: 121, step: 4, offset: 1 },
      vramGb: 14, documented: 'minimum 14 GB with model offloading (README.md:135-142); per-resolution VRAM and timings are not published', audio: false,
      strengths: { motion: 4, detail: 4, adherence: 4, resolution: 3, stability: 4, speed: 2, i2v: 4, audio: 0 } },
    { id: '480p', label: '480p 24 fps', tier: 'standard', tasks: ['t2v', 'i2v'], resolution: '480p',
      sizes: { '16:9': [848, 480], '9:16': [480, 848], '1:1': [640, 640] }, fps: 24, steps: 50, frames: { min: 25, max: 121, step: 4, offset: 1 },
      vramGb: 14, documented: 'step-distilled 480p image-to-video within 75 s on one RTX 4090 (README.md:45)', audio: false,
      strengths: { motion: 4, detail: 2, adherence: 4, resolution: 1, stability: 4, speed: 4, i2v: 4, audio: 0 } },
  ],
  plan(variant, req) { return { ...basePlan(variant, req), resolution: variant.resolution }; },
};
