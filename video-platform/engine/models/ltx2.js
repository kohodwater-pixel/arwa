import { basePlan } from './_plan.js';
/**
 * LTX-2 family — Lightricks/LTX-2 @ daa6b16 (v1.6.2, 2026-11-19; headline model LTX-2.5).
 * The repository publishes NO inference VRAM or timing figures (packages/ltx-pipelines/docs/optimization.md:245),
 * so vramGb is unknown until measured on our own hardware. Frame sizes below only satisfy the documented
 * divisibility rule (32; 64 for DFR) and are untested.
 */
export default {
  id: 'ltx2', label: 'LTX-2.5', repo: 'https://github.com/Lightricks/LTX-2', docsCommit: 'daa6b16',
  license: {
    code: 'Apache-2.0', weights: 'LTX-2.5 model licence (LICENSE-2_x)', commercial: 'conditions',
    notes: 'Weights: free below USD 10M annual group revenue; hosting as a service is allowed if Attachment A is passed to users (LICENSE-2_x:176-190). BUT use in a product that "directly competes with Licensor\'s commercial products or services" needs a separate commercial licence (LICENSE-2_x:604-608), and Lightricks sells video-generation API access. Get a written answer from licensing@ltx.io before any paid use. Watermark/provenance features must not be removed. Fine-tunes stay under the same licence.',
  },
  prompt: { languages: ['en'], maxChars: 1400, negative: true, note: 'One flowing paragraph within 200 words (README.md:170-178). Text encoder is described as multilingual; Arabic is not stated.' },
  lora: { trainers: ['ltx-trainer (in the repository; LoRA, full fine-tune, IC-LoRA)', 'diffusion-pipe (LTX 2.3 only, text-to-video, no audio)'], format: 'safetensors', note: 'Loaded with --lora <path> [strength]. A LoRA only works with the model it was trained on (README.md:141).' },
  variants: [
    { id: 'distilled', label: 'Distilled · fast, with audio', tier: 'standard', tasks: ['t2v', 'i2v'], pipeline: 'ltx_pipelines.distilled',
      sizes: { '16:9': [1280, 704], '9:16': [704, 1280], '1:1': [1024, 1024] }, fps: 24, steps: null, frames: { min: 25, max: 121, step: 8, offset: 1 },
      vramGb: null, documented: 'no VRAM or timing published; quick-start download is about 66 GiB', audio: true,
      strengths: { motion: 3, detail: 3, adherence: 3, resolution: 3, stability: 3, speed: 5, i2v: 3, audio: 5 } },
    { id: 'dfr', label: 'DFR · production, with audio', tier: 'high', tasks: ['t2v', 'i2v'], pipeline: 'ltx_pipelines.dfr_pipeline',
      sizes: { '16:9': [1536, 832], '9:16': [832, 1536], '1:1': [1024, 1024] }, fps: 24, steps: null, frames: { min: 25, max: 121, step: 8, offset: 1 },
      vramGb: null, documented: 'needs "more VRAM" than distilled (README.md:68); no figure published', audio: true,
      strengths: { motion: 4, detail: 4, adherence: 4, resolution: 4, stability: 4, speed: 3, i2v: 4, audio: 5 } },
  ],
  plan(variant, req) { return { ...basePlan(variant, req), pipeline: variant.pipeline, audio: true }; },
};
