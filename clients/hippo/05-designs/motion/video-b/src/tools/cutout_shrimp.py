#!/usr/bin/env python3
"""Local cut-out of the fried-shrimp hero photo (adapted from the brochure tool cutout_philly.py) (violet studio floor). Nothing leaves the machine.
Usage: python3 cutout_shrimp.py <fried-shrimp.jpg> <out.png> [work-dir]
Output: RGBA PNG, cropped, with a soft contact shadow baked in (set SHADOW=0 to leave it out).
Steps: violet-floor key -> largest component + hole fill -> 1 px choke + feather -> edge colours pulled from the
interior (removes violet fringe) -> blue-spill clamp in the edge band -> soft shadow -> crop."""
import sys, os, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]; work = sys.argv[3] if len(sys.argv) > 3 else None
SHADOW = float(os.environ.get("SHADOW", "0"))      # the film adds its own drop shadow in CSS
img = cv2.imread(src); H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL).astype(np.float32)
h = hsv[..., 0] * 360 / 255; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
violet = (h > 205) & (h < 285) & (s > 0.20)
roi = np.zeros((H, W), np.uint8); roi[696:1450, 120:1090] = 1          # the sandwich sits wholly on the floor
fg = ((~violet) & (roi == 1)).astype(np.uint8)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == big).astype(np.uint8)
# fill holes (navy ink of the printed sleeve keys as violet)
p = cv2.copyMakeBorder(m, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0); ff = p.copy()
cv2.floodFill(ff, np.zeros((p.shape[0] + 2, p.shape[1] + 2), np.uint8), (0, 0), 2); p[ff != 2] = 1; m = p[2:-2, 2:-2].copy()
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == big).astype(np.uint8)
# floor seen through gaps between lettuce leaves: bright violet is never object (navy sleeve ink is dark, v < 0.38)
floor = (violet & (v > 0.38) & (s > 0.24)).astype(np.uint8)
floor = cv2.dilate(cv2.morphologyEx(floor, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)), np.ones((3, 3), np.uint8))
m[floor == 1] = 0
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == big).astype(np.uint8)
# choke + feather
mc = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=1)
a = cv2.GaussianBlur(mc.astype(np.float32), (0, 0), 0.9); a = np.clip((a - 0.12) / 0.76, 0, 1)
# edge colours from the interior
core = cv2.erode(mc, np.ones((3, 3), np.uint8), iterations=2)
inp = cv2.inpaint(img, ((1 - core) * 255).astype(np.uint8), 5, cv2.INPAINT_TELEA)
rgb = img.copy(); band = (core == 0); rgb[band] = inp[band]
# blue-spill clamp in a 6 px inner band: blue may not exceed max(red, green)
inner = (cv2.erode(mc, np.ones((3, 3), np.uint8), iterations=8) == 0) & (a > 0)
b, g, r = [rgb[..., i].astype(np.int16) for i in range(3)]
lim = np.maximum(r, g); b2 = np.where(inner & (b > lim), lim, b); rgb[..., 0] = b2.astype(np.uint8)
# soft contact shadow under the object (brand black), baked into the same PNG
ys, xs = np.where(a > 0.5); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
pad = 46; X0, X1, Y0, Y1 = max(0, x0 - pad), min(W, x1 + pad), max(0, y0 - 8), min(H, y1 + pad)
sh = np.zeros((H, W), np.float32)
if SHADOW:
    low = (a > 0.5).astype(np.float32); low[: int(y0 + 0.55 * (y1 - y0))] = 0           # lower part of the object only
    M = np.float32([[1, 0, 0], [0, 1, 14]]); sh = cv2.warpAffine(low, M, (W, H))
    sh = cv2.GaussianBlur(sh, (0, 0), 13) * SHADOW
A = a + (1 - a) * sh
col = np.empty((H, W, 3), np.float32); k = np.where(A > 1e-4, a / np.maximum(A, 1e-4), 0)[..., None]
col = rgb.astype(np.float32) * k + np.float32([0x17, 0x17, 0x18]) * (1 - k)
rgba = np.dstack([np.clip(col, 0, 255).astype(np.uint8), np.clip(A * 255, 0, 255).astype(np.uint8)])[Y0:Y1, X0:X1]
# retouch: one dark crumb on the bread's lower-left edge (png coords of the 1202 px web photo; scale for HQ)
RET = np.zeros(rgba.shape[:2], np.uint8); cv2.circle(RET, (90, 603), 10, 255, -1)
RET[(rgba[..., :3].max(axis=2) >= 110)] = 0; RET = cv2.dilate(RET, np.ones((3, 3), np.uint8))
keep = rgba[..., 3].copy(); rgba[..., :3] = cv2.inpaint(np.ascontiguousarray(rgba[..., :3]), RET, 4, cv2.INPAINT_TELEA); rgba[..., 3] = keep
cv2.imwrite(out, rgba)
print('object px', x1 - x0 + 1, 'x', y1 - y0 + 1, '| png', rgba.shape[1], 'x', rgba.shape[0], '| object offset in png', x0 - X0, y0 - Y0)
if work:
    al = rgba[..., 3:].astype(np.float32) / 255; hh, ww = rgba.shape[:2]
    for name, bg in [('pink', (0xA2, 0x6F, 0xDA)), ('lime', (0x32, 0xD0, 0xBB)), ('black', (0x17, 0x17, 0x18))]:
        comp = (rgba[..., :3] * al + np.float32(bg) * (1 - al)).astype(np.uint8)
        cv2.imwrite(os.path.join(work, f'on_{name}.png'), comp)
        for q, (y0_, y1_, x0_, x1_) in {'TL': (0, hh // 2, 0, ww // 2), 'TR': (0, hh // 2, ww // 2, ww), 'BL': (hh // 2, hh, 0, ww // 2), 'BR': (hh // 2, hh, ww // 2, ww)}.items():
            cv2.imwrite(os.path.join(work, f'on_{name}_{q}.png'), cv2.resize(comp[y0_:y1_, x0_:x1_], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST))
