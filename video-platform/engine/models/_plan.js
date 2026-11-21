import { framesFor } from '../lib/frames.js';
/** Shared plan(): platform request → job spec a worker runs. Models add their own fields on top. */
export function basePlan(variant, { prompt, negativePrompt, seconds, aspect, seed, task }) {
  const [width, height] = variant.sizes[aspect];
  const frames = framesFor(variant, seconds);
  return { task, prompt, negativePrompt, seconds, aspect, width, height, frames, fps: variant.fps, steps: variant.steps, seed };
}
