#!/usr/bin/env python3
"""v07: GrabCut cut-outs of the client's car + scooter + rider and box truck (client mockups) for the logistics composite.
Sources are read only; masks are saved in _work/v07/ and reused by build_profile_v07.py."""
import cv2, numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, binary_opening, label
from pathlib import Path
B = Path(__file__).resolve().parents[2]
W = B / '_work/v07'
def cut(src, rect, name, bgboxes=(), fgboxes=(), iters=12):
    im = np.array(Image.open(B / src).convert('RGB')); bgr = im[:, :, ::-1].copy()
    mask = np.zeros(im.shape[:2], np.uint8)
    x, y, w, h = rect; mask[y:y + h, x:x + w] = cv2.GC_PR_FGD
    for (l, t, r, b) in bgboxes: mask[t:b, l:r] = cv2.GC_BGD
    for (l, t, r, b) in fgboxes: mask[t:b, l:r] = cv2.GC_FGD
    bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
    cv2.grabCut(bgr, mask, None, bg, fg, iters, cv2.GC_INIT_WITH_MASK)
    m = (mask == 1) | (mask == 3)
    m = binary_opening(m, iterations=2)
    lab, n = label(m); sizes = np.bincount(lab.ravel()); sizes[0] = 0
    m = (sizes > sizes.max() * 0.05)[lab]
    m = binary_fill_holes(m)
    np.save(W / f'{name}_mask.npy', m)
    out = im.copy(); out[~m] = [255, 0, 255]
    Image.fromarray(out).save(W / f'{name}_check.jpg', quality=90)

S = 'assets/derived/mockup_car-scooter-facade_retouched_v03.png'
cut(S, (15, 440, 830, 380), 'car',
    bgboxes=[(0, 0, 1536, 438), (840, 0, 1536, 1024), (0, 822, 1536, 1024), (380, 436, 440, 482), (440, 436, 470, 458), (0, 436, 380, 520)],
    fgboxes=[(480, 600, 680, 680), (250, 700, 370, 780), (100, 600, 230, 700), (720, 640, 800, 720), (30, 610, 130, 740)])
cut(S, (775, 285, 700, 585), 'scoot',
    bgboxes=[(1250, 60, 1362, 420), (1218, 60, 1250, 282), (1475, 0, 1536, 1024), (0, 868, 1536, 1024), (0, 0, 775, 1024),
             (775, 285, 930, 470), (930, 285, 1105, 398), (1012, 530, 1040, 548), (1262, 320, 1284, 440), (1112, 398, 1146, 425), (999, 552, 1015, 745)],
    fgboxes=[(1120, 300, 1200, 420), (1150, 430, 1240, 560), (1300, 440, 1460, 570), (1210, 690, 1370, 840), (830, 720, 930, 830),
             (1280, 590, 1400, 660), (1100, 600, 1250, 660), (1030, 580, 1080, 740), (1010, 498, 1048, 526)])
mc, ms = np.load(W / 'car_mask.npy'), np.load(W / 'scoot_mask.npy')
im = np.array(Image.open(B / S).convert('RGB')); m = mc | ms
# pavement and wall left inside small enclosed gaps of the scooter group: light, unsaturated pixels in these zones only
f = im.astype(int); lum = f.mean(axis=2); sat = f.max(axis=2) - f.min(axis=2)
for (l, t, r, b) in [(955, 515, 1140, 738), (1105, 355, 1152, 428), (1360, 630, 1435, 835), (1150, 800, 1310, 872), (180, 780, 760, 830)]:
    z = np.zeros_like(m); z[t:b, l:r] = True
    m &= ~(z & (lum > 105) & (sat < 40))
zz = np.zeros_like(m); zz[398:428, 1105:1150] = True; m &= ~(zz & (lum > 120))
m = binary_opening(m, iterations=1)
lab, n = label(m); sizes = np.bincount(lab.ravel()); sizes[0] = 0; m = (sizes > sizes.max() * 0.02)[lab]
np.save(W / 'carscoot_mask.npy', m)
out = im.copy(); out[~m] = [255, 0, 255]; Image.fromarray(out).save(W / 'carscoot_check.jpg', quality=90)
T = 'assets/derived/mockup_logistics-trucks_retouched_v03.png'
cut(T, (70, 95, 670, 465), 'truck',
    bgboxes=[(0, 0, 240, 170), (0, 0, 836, 92), (0, 90, 92, 330), (686, 92, 760, 162), (88, 120, 160, 186), (735, 92, 836, 560)],
    fgboxes=[(300, 120, 700, 370), (120, 200, 330, 400), (360, 400, 440, 500)])

# truck: sky left above the sloping box roof (bluish light pixels) is removed in that zone only
mt = np.load(W / 'truck_mask.npy'); ti = np.array(Image.open(B / T).convert('RGB')).astype(int)
lum = ti.mean(axis=2); z = np.zeros_like(mt); z[85:180, 440:770] = True
mt &= ~(z & (lum > 150) & (ti[..., 2] > ti[..., 0] + 6))
# asphalt kept under the chassis: below the bumper line keep only dark tyre/chassis pixels, then refill the wheel rims
z2 = np.zeros_like(mt); z2[455:600, 60:780] = True
sat = ti.max(axis=2) - ti.min(axis=2)
mt &= ~(z2 & (lum > 70) & (sat < 35))
mt = binary_fill_holes(mt)
# below the chassis line (y 472) only the two wheels stay: ellipses measured on a 2x grid of the source
yy, xx = np.mgrid[0:mt.shape[0], 0:mt.shape[1]]
wheels = (((xx - 395) / 44) ** 2 + ((yy - 477) / 61) ** 2 <= 1) | (((xx - 634) / 40) ** 2 + ((yy - 446) / 43) ** 2 <= 1)
mt[472:] &= wheels[472:]
mt[:, 752:] = False
z3 = np.zeros_like(mt); z3[100:178, 560:760] = True; z3[160:245, 82:138] = True
mt &= ~(z3 & (lum > 140) & (sat < 30))
z4 = np.zeros_like(mt); z4[160:292, 80:120] = True
mt &= ~(z4 & (lum > 105) & (sat < 40))
mt = binary_opening(mt, iterations=1)
lab, n = label(mt); sizes = np.bincount(lab.ravel()); sizes[0] = 0; mt = (sizes > sizes.max() * 0.02)[lab]
np.save(W / 'truck_mask.npy', mt)
out = ti.astype(np.uint8).copy(); out[~mt] = [255, 0, 255]; Image.fromarray(out).save(W / 'truck_check.jpg', quality=90)
