#!/usr/bin/env python3
"""Cinematic grade for a composed 1080x1920 background: S-curve contrast, warm highlights / cooler-deeper shadows,
saturation trim and a gentle vignette. No content is added, removed or replaced."""
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
contrast, warm, sat, vig, gamma = [float(v) for v in sys.argv[3:8]]
a = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
a = a ** gamma
# S-curve around mid grey
a = np.clip(0.5 + (a - 0.5) * (1 + contrast) - contrast * 0.9 * (a - 0.5) ** 3 * 4 * 0.25, 0, 1)
L = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
# warm the highlights, deepen and slightly warm-brown the shadows
hi = np.clip((L - 0.45) / 0.55, 0, 1); lo = np.clip((0.4 - L) / 0.4, 0, 1)
a = a + warm * hi * np.array([0.06, 0.015, -0.07]) + warm * lo * np.array([0.012, -0.004, -0.02])
a = L + (a - L) * sat
H, W = a.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.75)) ** 2)
a = a * (1 - vig * np.clip(r - 0.35, 0, 1) ** 1.6)[..., None]
Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype('uint8')).save(out, quality=93, subsampling=0)
print(out)
