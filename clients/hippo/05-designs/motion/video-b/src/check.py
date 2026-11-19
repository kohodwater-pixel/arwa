#!/usr/bin/env python3
"""Text checks on settled moments of the film (run after: node render.cjs check ../_work/chk <times>):
WCAG contrast of every fully opaque text element against the pixels behind its glyphs (1st percentile >= 4.5),
ink inside the safe areas (250 px top, 350 px bottom, 60 px sides), no letter-spacing.  Usage: python3 check.py <chk-dir>"""
import json, os, re, sys
import numpy as np
from PIL import Image
import cv2
D = sys.argv[1]
def lin(c):
    c = c / 255.0
    return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lum(rgb):
    l = lin(np.asarray(rgb, dtype=float)); return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]
def ratio(a, b):
    return (np.maximum(a, b) + 0.05) / (np.minimum(a, b) + 0.05)
fails = 0
M = json.load(open(os.path.join(D, 'metrics.json')))
for key in sorted(M):
    full = np.asarray(Image.open(os.path.join(D, 'chk_%s.png' % key)).convert('RGB')).astype(int)
    bg = np.asarray(Image.open(os.path.join(D, 'chk_%s_bg.png' % key)).convert('RGB')).astype(int)
    print('== t = %s' % key)
    for t in M[key]:
        x0, y0 = max(0, int(t['x']) - 6), max(0, int(t['y']) - 6); x1, y1 = min(1080, int(t['x'] + t['w']) + 6), min(1920, int(t['y'] + t['h']) + 6)
        col = [int(v) for v in re.findall(r'\d+', t['color'])[:3]]
        a, b = full[y0:y1, x0:x1], bg[y0:y1, x0:x1]
        glyph = (np.abs(a - np.array(col)).sum(axis=2) < 40) & (np.abs(a - b).sum(axis=2) > 30)
        if glyph.sum() < 20: print('   ?? no glyph pixels for', t['text']); fails += 1; continue
        k = cv2.dilate(glyph.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        r = ratio(lum(np.array(col)), lum(b[k])); p1 = float(np.percentile(r, 1))
        ys = np.where(glyph.any(axis=1))[0]; xs = np.where(glyph.any(axis=0))[0]
        top, bot, lef, rig = y0 + ys.min(), y0 + ys.max(), x0 + xs.min(), x0 + xs.max()
        safe = top >= 250 and bot <= 1570 and lef >= 60 and rig <= 1020
        ok = p1 >= 4.5 and safe and t['spacing'] == 'normal'
        if not ok: fails += 1
        print('   %s %-26s %7s %s  contrast p1 %.2f  ink x %d-%d y %d-%d %s' % ('OK ' if ok else 'XX ', t['text'][:26], t['size'], t['weight'], p1, lef, rig, top, bot, '' if safe else 'OUTSIDE SAFE AREA'))
print('failures:', fails); sys.exit(1 if fails else 0)
