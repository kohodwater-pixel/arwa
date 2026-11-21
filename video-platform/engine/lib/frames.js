/** Frame arithmetic shared by the registry and the model manifests (kept separate to avoid an import cycle). */
/** Nearest frame count the variant accepts for a duration (models constrain frames, e.g. 4n+1). */
export function framesFor(variant, seconds) {
  const { fps, frames } = variant;
  const want = Math.round(seconds * fps);
  const step = frames.step || 1, offset = frames.offset || 0;
  let n = Math.ceil((want - offset) / step) * step + offset;      // round up: the platform trims, it never stretches
  n = Math.min(frames.max, Math.max(frames.min, n));
  return n;
}
export const maxSeconds = (variant) => Math.floor(variant.frames.max / variant.fps);
export const minSeconds = (variant) => Math.max(1, Math.ceil(variant.frames.min / variant.fps));

