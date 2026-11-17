#!/usr/bin/env python3
"""v19: client's wide Riyadh skyline (assets/mockups PNG copy of the .webp; original untouched).
- The green wordmark baked into the sky (top right) is malformed: painted out into the sky.
- The baked-in white Vision 2030 logo was inspected at full size: «رؤية» is drawn wrongly (the final ta marbuta
  reads as a lam, «رؤيل») and the emblem squares are blurred blobs, so it is NOT reused (it lies outside the crop anyway).
  A white version is built from the OFFICIAL file instead: same geometry, grey lettering/palm/swords turned white,
  the emblem's colours kept — as in the client's image.
Outputs: assets/derived/v19_client_riyadh-wide_clean.png, assets/derived/v19_vision2030_white.png, checks in _work/v19/."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation
from pathlib import Path
B = Path(__file__).resolve().parents[2]
W = B / '_work/v19'
im = Image.open(B / 'assets/mockups/photo_riyadh-night-skyline_wide_with-logos.png').convert('RGB')
a = np.array(im).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
zone = np.zeros(a.shape[:2], bool); zone[35:110, 1450:1670] = True
mark = zone & (((g > r + 40) & (g > b)) | (a.mean(axis=2) > 120))
hole = binary_dilation(mark, iterations=5) & binary_dilation(zone, iterations=4)
good = binary_dilation(zone, iterations=40) & ~hole & ~mark
w = good.astype(float)
f = np.stack([gaussian_filter(a[..., i] * w, 14) for i in range(3)], -1) / (gaussian_filter(w, 14)[..., None] + 1e-6)
a[hole] = f[hole] + np.random.default_rng(9).normal(0, 1, (hole.sum(), 3)) * a[good].std(axis=0).clip(0, 6) * 0.5
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save(B / 'assets/derived/v19_client_riyadh-wide_clean.png', optimize=True)
im.crop((1400, 10, 1708, 150)).resize((924, 420)).save(W / 'check_top-right_before.png')
out.crop((1400, 10, 1708, 150)).resize((924, 420)).save(W / 'check_top-right_after.png')
im.crop((1370, 680, 1660, 870)).resize((870, 570), Image.LANCZOS).save(W / 'check_baked-in-vision-logo_not-used.png')

L = np.array(Image.open(B / 'assets/logo/logo_saudi-vision-2030.png').convert('RGBA')).astype(float)
rgb, al = L[..., :3], L[..., 3:]
sat = rgb.max(axis=2) - rgb.min(axis=2)
neutral = (sat < 40)[..., None]                                   # grey lettering, palm and swords
rgb = np.where(neutral, 255.0, rgb)
Image.fromarray(np.dstack([rgb, al]).astype(np.uint8), 'RGBA').save(B / 'assets/derived/v19_vision2030_white.png')
print('done')
