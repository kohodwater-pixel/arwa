#!/usr/bin/env python3
"""Checks for the hippo style frames (run after render.cjs):
  - WCAG contrast of every text element against the pixels actually behind its glyphs
    (glyph pixels = where the frame differs from the same frame rendered with text hidden)
  - text inside the safe areas (250 px top, 350 px bottom)
  - photo scale (shown width / natural width) no more than 110 %
  - no letter-spacing, fonts loaded
  - QR decodes from the rendered end cards (OpenCV)
Usage: python3 check.py"""
import json, os, re, sys
import numpy as np
from PIL import Image
import cv2

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); WORK = os.path.join(OUT, '_work')
NAME = 'hippo_franchise-motion-ad_styleframe-%s-%s_ar_v03.png'
SAFE_TOP, SAFE_BOTTOM = 250, 1920 - 350
QR_EXPECT = 'https://otlobny.net/HIPPO-franchise-form-final/franchise/index.html'

def lin(c):
    c = c / 255.0
    return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lum(rgb):
    l = lin(np.asarray(rgb, dtype=float))
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]
def ratio(l1, l2):
    hi = np.maximum(l1, l2); lo = np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

metrics = json.load(open(os.path.join(WORK, 'metrics.json')))
fails = 0
for fid in sorted(metrics):
    m = metrics[fid]
    full = np.asarray(Image.open(os.path.join(OUT, NAME % (fid[0], fid[1]))).convert('RGB')).astype(int)
    bg = np.asarray(Image.open(os.path.join(WORK, 'bg_%s.png' % fid)).convert('RGB')).astype(int)
    print('== %s  fonts loaded: %s' % (fid, m['fonts']))
    if not all(m['fonts']): fails += 1
    for t in m['texts']:
        x0, y0 = max(0, int(t['x'])), max(0, int(t['y'])); x1, y1 = min(1080, int(t['x'] + t['w']) + 1), min(1920, int(t['y'] + t['h']) + 1)
        col = [int(v) for v in re.findall(r'\d+', t['color'])[:3]]
        a, b = full[y0:y1, x0:x1], bg[y0:y1, x0:x1]
        # glyph pixels: close to the text colour in the frame and changed from the text-hidden render
        glyph = (np.abs(a - np.array(col)).sum(axis=2) < 40) & (np.abs(a - b).sum(axis=2) > 30)
        if glyph.sum() < 20:
            print('   ?? no glyph pixels found for', t['text']); fails += 1; continue
        # background behind and around the glyphs: dilate the glyph mask a little
        k = cv2.dilate(glyph.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        r = ratio(lum(np.array(col)), lum(b[k]))
        worst, p5 = float(r.min()), float(np.percentile(r, 1))
        ys = np.where(glyph.any(axis=1))[0]; top, bot = y0 + ys.min(), y0 + ys.max()
        safe = top >= SAFE_TOP and bot <= SAFE_BOTTOM
        ok = p5 >= 4.5 and safe and t['spacing'] == 'normal'
        if not ok: fails += 1
        print('   %s %-28s %s %s %s  contrast min %.2f / p1 %.2f  ink y %d-%d %s' % ('OK ' if ok else 'XX ', t['text'][:28], t['size'], t['weight'], t['family'].split(',')[0], worst, p5, top, bot, '' if safe else 'OUTSIDE SAFE AREA'))
    for i in m['imgs']:
        if 'logo' in i['src'] or 'qr' in i['src']:
            print('   img %-22s shown %d px wide (natural %d)' % (i['src'], i['shown'], i['natural'])); continue
        s = i['shown'] / i['natural']
        if s > 1.101: fails += 1
        print('   img %-22s scale %.0f %% %s' % (i['src'], s * 100, '' if s <= 1.101 else 'TOO BIG'))

det = cv2.QRCodeDetector()
for d in 'abc':
    im = cv2.imread(os.path.join(OUT, NAME % (d, '4')))
    for label, img in (('full 1080x1920', im), ('half size 540x960', cv2.resize(im, (540, 960), interpolation=cv2.INTER_AREA))):
        s, pts, _ = det.detectAndDecode(img)
        ok = s == QR_EXPECT
        if not ok: fails += 1
        print('QR %s4 %-18s %s %r' % (d, label, 'OK ' if ok else 'XX ', s))

print('failures:', fails)
sys.exit(1 if fails else 0)
