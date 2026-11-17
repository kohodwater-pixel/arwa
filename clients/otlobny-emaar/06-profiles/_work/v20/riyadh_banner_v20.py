#!/usr/bin/env python3
"""v20: client's 3:1 Riyadh banner (assets/mockups copy; original untouched).
The baked-in white Vision 2030 logo misdraws «رؤية» (final ta marbuta reads as a lam) and blurs the emblem, so it is
painted out into the dark surroundings; the official white version (assets/derived/v19_vision2030_white.png) is then
placed by the page at the same position and size (source box x 1891-2118, y 502-650 px).
Output: assets/derived/v20_client_riyadh-banner_clean.png + checks in _work/v20/."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation
from pathlib import Path
B = Path(__file__).resolve().parents[2]
W = B / '_work/v20'
im = Image.open(B / 'assets/mockups/photo_riyadh-night-skyline_banner-ratio.png').convert('RGB')
a = np.array(im).astype(float)
zone = np.zeros(a.shape[:2], bool); zone[490:662, 1880:2132] = True
sat = a.max(axis=2) - a.min(axis=2); lum = a.mean(axis=2)
mark = zone & ((a.min(axis=2) > 120) | ((sat > 55) & (lum > 70)))
hole = binary_dilation(mark, iterations=4) & zone
good = binary_dilation(zone, iterations=30) & ~hole & (lum < 90)
w = good.astype(float)
f = np.stack([gaussian_filter(a[..., i] * w, 7) for i in range(3)], -1) / (gaussian_filter(w, 7)[..., None] + 1e-6)
a[hole] = f[hole] + np.random.default_rng(12).normal(0, 1, (hole.sum(), 3)) * a[good].std(axis=0).clip(0, 8) * 0.45
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save(B / 'assets/derived/v20_client_riyadh-banner_clean.png', optimize=True)
im.crop((1860, 480, 2172, 680)).resize((936, 600)).save(W / 'check_logo-corner_before.png')
out.crop((1860, 480, 2172, 680)).resize((936, 600)).save(W / 'check_logo-corner_painted-out.png')
print('done')
