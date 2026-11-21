import { basePlan } from './_plan.js';
/**
 * Wan 2.2 — Wan-Video/Wan2.2 @ 1ea34ff (2026-09-21). Facts from README.md, generate.py, wan/configs/*.
 * `strengths` (1–5) are starting assumptions for the router, not measurements; evaluation runs replace them.
 */
export default {
  id: 'wan22', label: 'Wan 2.2', repo: 'https://github.com/Wan-Video/Wan2.2', docsCommit: '1ea34ff',
  license: {
    code: 'Apache-2.0', weights: 'Apache-2.0', commercial: 'yes',
    notes: 'Code and weights are Apache 2.0 (LICENSE.txt; README.md:497). No revenue threshold, territory or hosting restriction. Duties: pass on the licence and keep notices.',
  },
  prompt: { languages: ['en', 'zh'], maxChars: 2000, negative: false, note: 'Arabic is not stated as supported; prompts are sent in English. generate.py has no negative-prompt flag (a default lives in config).' },
  lora: { trainers: ['musubi-tuner (A14B, both experts in one run)', 'diffusion-pipe (A14B and 5B text-to-video)'], format: 'safetensors', note: 'The official generate.py has no general LoRA flag; LoRA inference runs through musubi-tuner wan_generate_video.py, ComfyUI or Diffusers.' },
  variants: [
    { id: 'ti2v-5b', label: 'TI2V-5B · 720p 24 fps', tier: 'standard', tasks: ['t2v', 'i2v'], task: 'ti2v-5B',
      sizes: { '16:9': [1280, 704], '9:16': [704, 1280] }, fps: 24, steps: 50, frames: { min: 25, max: 121, step: 4, offset: 1 },
      vramGb: 24, documented: '5 s 720p in 534.7 s at 22.9 GB peak on one RTX 4090 (assets/comp_effic.png)', audio: false,
      strengths: { motion: 3, detail: 3, adherence: 3, resolution: 3, stability: 3, speed: 2, i2v: 3, audio: 0 } },
    { id: 'a14b-720p', label: 'A14B · 720p 16 fps', tier: 'high', tasks: ['t2v', 'i2v'], task: { t2v: 't2v-A14B', i2v: 'i2v-A14B' },
      sizes: { '16:9': [1280, 720], '9:16': [720, 1280] }, fps: 16, steps: 40, frames: { min: 17, max: 81, step: 4, offset: 1 },
      vramGb: 80, documented: 'README asks for 80 GB; measured peak 59.8 GB, 1041.5 s per 5 s clip on one H100 (2735.7 s on A100)', audio: false,
      strengths: { motion: 5, detail: 4, adherence: 4, resolution: 3, stability: 4, speed: 1, i2v: 4, audio: 0 } },
    { id: 'a14b-480p', label: 'A14B · 480p 16 fps', tier: 'standard', tasks: ['t2v', 'i2v'], task: { t2v: 't2v-A14B', i2v: 'i2v-A14B' },
      sizes: { '16:9': [832, 480], '9:16': [480, 832] }, fps: 16, steps: 40, frames: { min: 17, max: 81, step: 4, offset: 1 },
      vramGb: 48, documented: 'measured peak 41.3 GB, 326.9 s per 5 s clip on one H100 (785.7 s on A100)', audio: false,
      strengths: { motion: 5, detail: 2, adherence: 4, resolution: 1, stability: 4, speed: 3, i2v: 4, audio: 0 } },
  ],
  plan(variant, req) {
    const spec = basePlan(variant, req);
    spec.wanTask = typeof variant.task === 'string' ? variant.task : variant.task[req.task];
    spec.size = `${spec.width}*${spec.height}`;
    return spec;
  },
};
