import { basePlan } from './_plan.js';
/**
 * CogVideoX — THUDM/CogVideo (now zai-org/CogVideo) @ 7a1af71 (2025-11-04). Maintenance mode; CogKit, the
 * toolkit the repository points to, has had no commit since 2025-05-14.
 * Only the 2B model is listed: it is the one with a clear Apache 2.0 weights licence. It generates 720x480
 * (3:2) at 8 fps, which matches none of the platform's aspect ratios, so the router never picks it for
 * production. It is kept as a cheap baseline for the evaluation harness.
 * Not listed: 5B (commercial use needs registration at open.bigmodel.cn and stays under 1M visits/month,
 * MODEL_LICENSE:12-14) and 1.5-5B (weights licence not stated in the repository).
 */
export default {
  id: 'cogvideox', label: 'CogVideoX-2B', repo: 'https://github.com/THUDM/CogVideo', docsCommit: '7a1af71',
  license: { code: 'Apache-2.0', weights: 'Apache-2.0 (2B only)', commercial: 'yes', notes: '2B weights and VAE are Apache 2.0 (README.md:454-455).' },
  prompt: { languages: ['en'], maxChars: 900, negative: false, note: 'English only, 226 tokens (README.md:238-240, 300-301).' },
  lora: { trainers: ['finetrainers', 'CogKit (unmaintained)'], format: 'safetensors (Diffusers)', note: 'Loaded with pipe.load_lora_weights.' },
  variants: [
    { id: '2b', label: '2B · 720x480 8 fps', tier: 'standard', tasks: ['t2v'], modelPath: 'THUDM/CogVideoX-2b',
      sizes: { '3:2': [720, 480] }, fps: 8, steps: 50, frames: { min: 9, max: 49, step: 8, offset: 1 },
      vramGb: 12, documented: '4 GB minimum with sequential offload, about 3x more without; about 90 s per clip on A100 (README.md:216-231)', audio: false,
      strengths: { motion: 2, detail: 1, adherence: 2, resolution: 1, stability: 2, speed: 4, i2v: 0, audio: 0 } },
  ],
  plan(variant, req) { return { ...basePlan(variant, req), modelPath: variant.modelPath }; },
};
