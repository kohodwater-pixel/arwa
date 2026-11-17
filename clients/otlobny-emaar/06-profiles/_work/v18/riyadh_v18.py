#!/usr/bin/env python3
"""v18: client's Riyadh night skyline (assets/mockups copy; original untouched) for the p6 banner.
The malformed green wordmark baked into the sky (top right) is painted out with the surrounding sky
(normalised convolution from sky pixels only + matched grain). The baked-in Vision 2030 logo (bottom right)
lies below the banner crop and is not shown; the official logo file is placed on the white tab instead.
Output: assets/derived/v18_client_riyadh-skyline_clean.png (full image, cleaned) + check crops in _work/v18/."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation
from pathlib import Path
B = Path(__file__).resolve().parents[2]
im = Image.open(B / 'assets/mockups/photo_riyadh-night-skyline_with-logos.png').convert('RGB')
a = np.array(im).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
zone = np.zeros(a.shape[:2], bool); zone[50:140, 1240:1435] = True
mark = zone & (((g > r + 40) & (g > b)) | (a.mean(axis=2) > 120))      # green letters + white dot ring
hole = binary_dilation(mark, iterations=5) & binary_dilation(zone, iterations=4)
good = binary_dilation(zone, iterations=40) & ~hole & ~mark
w = good.astype(float)
f = np.stack([gaussian_filter(a[..., i] * w, 14) for i in range(3)], -1) / (gaussian_filter(w, 14)[..., None] + 1e-6)
noise = a[good].std(axis=0).clip(0, 6) * 0.5
a[hole] = f[hole] + np.random.default_rng(9).normal(0, 1, (hole.sum(), 3)) * noise
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save(B / 'assets/derived/v18_client_riyadh-skyline_clean.png', optimize=True)
W = B / '_work/v18'
im.crop((1180, 20, 1487, 180)).resize((921, 480), Image.LANCZOS).save(W / 'check_top-right_before.png')
out.crop((1180, 20, 1487, 180)).resize((921, 480), Image.LANCZOS).save(W / 'check_top-right_after.png')
print('done, hole px:', int(hole.sum()))
