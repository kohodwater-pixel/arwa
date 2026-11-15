#!/usr/bin/env python3
"""Places a source photo on a 1080x1920 canvas without upscaling.
If the photo does not reach the top, the sky is continued upward from the photo's own top rows
(colour trend extrapolated, slight grain). If it does not reach the bottom, the ground fades into
the footer brown (that area sits under the dark footer gradient anyway)."""
import os, sys, numpy as np
from PIL import Image, ImageFilter
src, out, w, x, y = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
im = Image.open(src).convert('RGB')
assert w <= im.width, 'would upscale'
h = round(im.height * w / im.width)
im = im.resize((w, h), Image.LANCZOS)
W, H = 1080, 1920
canvas = np.zeros((H, W, 3), float)
crop = np.asarray(im).astype(float)[:, x:x + W]
assert crop.shape[1] == W
y1 = min(H, y + h)
canvas[max(0, y):y1] = crop[max(0, -y):max(0, -y) + (y1 - max(0, y))]
rng = np.random.default_rng(7)
if y > 0:  # extend sky upward
    band = crop[:60]
    top = band[:12].mean(axis=0)                    # per-column colour at the top edge
    top = np.asarray(Image.fromarray(top[None].astype('uint8')).resize((W, 1)).filter(ImageFilter.GaussianBlur(40))).astype(float)[0]
    if os.environ.get('FLAT_SKY'):  # sky colour taken as the median across the width (used when a building edge touches the top rows)
        top = np.tile(np.median(top, axis=0), (W, 1))
    slope = (band[:12].mean(axis=(0, 1)) - band[48:60].mean(axis=(0, 1))) / 42.0   # colour change per px going up
    slope = np.clip(slope, -0.06, 0.06)
    for r in range(y):
        d = y - r
        col = top + slope * d * np.exp(-d / 900.0)
        canvas[r] = np.clip(col, 0, 255)
    canvas[:y] += rng.normal(0, 1.1, (y, W, 1))
    # soften the seam
    k = 24
    seam = Image.fromarray(np.clip(canvas[y - k:y + k], 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(6))
    a = np.linspace(0, 1, 2 * k)[:, None, None]; wgt = 1 - np.abs(a * 2 - 1)
    canvas[y - k:y + k] = canvas[y - k:y + k] * (1 - wgt) + np.asarray(seam).astype(float) * wgt
if y1 < H:  # fade ground to footer brown
    last = crop[-40:].mean(axis=0); last = np.asarray(Image.fromarray(last[None].astype('uint8')).filter(ImageFilter.GaussianBlur(30))).astype(float)[0]
    foot = np.array([23, 12, 7.0])
    for r in range(y1, H):
        t = min(1, (r - y1) / 260.0); t = t * t * (3 - 2 * t)
        canvas[r] = last * (1 - t) + foot * t
    k = 30
    seam = Image.fromarray(np.clip(canvas[y1 - k:y1 + k], 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(8))
    a = np.linspace(0, 1, 2 * k)[:, None, None]; wgt = 1 - np.abs(a * 2 - 1)
    canvas[y1 - k:y1 + k] = canvas[y1 - k:y1 + k] * (1 - wgt) + np.asarray(seam).astype(float) * wgt
Image.fromarray(np.clip(canvas, 0, 255).astype('uint8')).save(out, quality=93, subsampling=0)
print(out, 'scaled', im.size, 'placed at', (-x, y))
