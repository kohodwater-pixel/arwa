#!/usr/bin/env python3
"""v08 logistics composite (review_v07_r4 M1, m1, m2, m3).

Works at 2x the source resolution. For every vehicle surface:
  1. the AI-drawn logo is painted out with the surface's own paint (membrane fill from the surrounding panel, plus grain),
  2. the REAL wordmark (04-identity/02-logo, rendered from SVG with cairosvg) is warped onto the surface plane with
     cv2.getPerspectiveTransform and shaded with the surface's own light (multiply by the local luminance ratio).
Version per ground, as system.md allows: reversed (green + white) on the navy truck box and the black delivery box;
colour (blue + green) on the white cab and car. The scooter's curved side panel is only painted out (no logo).
Also: the truck box mask is completed (rear corner step, silver top rail and rear trim restored), the towers seen
through the cab's far window are replaced by dark glass, shadows rebalanced.
Inputs: client mockups (read only), v07 GrabCut masks in _work/v07/. Output: assets/derived/v08_logistics_fleet-composite.jpg
and 300 dpi check crops in _work/v08/."""
import io, numpy as np, cv2, cairosvg
from PIL import Image, ImageFilter, ImageDraw
from scipy.ndimage import gaussian_filter, binary_dilation, binary_erosion
from pathlib import Path

B = Path(__file__).resolve().parents[2]            # 06-profiles/
W = B / '_work/v08'
LOGO = B.parent / '04-identity/02-logo'
K = 2                                               # working scale
VB = (307.711, 124.597)                             # wordmark viewBox

def up(src):
    im = Image.open(B / src).convert('RGB')
    return np.array(im.resize((im.width * K, im.height * K), Image.LANCZOS)).astype(float)

def svg_rgba(name, width=2400):
    png = cairosvg.svg2png(url=str(LOGO / name), output_width=width)
    return np.array(Image.open(io.BytesIO(png)).convert('RGBA')).astype(float)

def inpaint(a, mask, iters=900):
    a = a.copy()
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min() - 3, ys.max() + 4, xs.min() - 3, xs.max() + 4
    sub, m = a[y0:y1, x0:x1], mask[y0:y1, x0:x1]
    ring = binary_dilation(m, iterations=4) & ~m
    sub[m] = sub[ring].mean(axis=0)
    for _ in range(iters):
        avg = (np.roll(sub, 1, 0) + np.roll(sub, -1, 0) + np.roll(sub, 1, 1) + np.roll(sub, -1, 1)) / 4
        sub[m] = avg[m]
    rng = np.random.default_rng(11)
    sd = sub[ring].std(axis=0).clip(0, 6) * 0.6
    sub[m] += rng.normal(0, 1, (m.sum(), 3)) * sd
    a[y0:y1, x0:x1] = sub
    return a

def logo_mask(a, box, kind):
    """Pixels of the AI logo inside box (source px), on a dark or a white surface; dilated to take the anti-aliased rim."""
    l, t, r, b = [v * K for v in box]
    f = a[t:b, l:r]; lum = f.mean(axis=2); sat = f.max(axis=2) - f.min(axis=2)
    if kind == 'dark':
        m = (sat > 45) | (lum > 95)
    else:
        med = np.median(lum)
        m = (sat > 28) | (lum < med - 22)
    m = binary_dilation(m, iterations=3 * K)
    full = np.zeros(a.shape[:2], bool); full[t:b, l:r] = m
    return full

def place(a, svg, quad, shade_box, white_gain=1.0):
    """Warp the wordmark onto quad (TL, TR, BR, BL in source px) and shade it with the surface light."""
    L = svg_rgba(svg)
    h, w = L.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = np.float32([[x * K, y * K] for x, y in quad])
    M = cv2.getPerspectiveTransform(src, dst)
    H_, W_ = a.shape[:2]
    rgb = cv2.warpPerspective(L[..., :3], M, (W_, H_), flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR)
    al = cv2.warpPerspective(L[..., 3], M, (W_, H_), flags=cv2.INTER_LINEAR) / 255.0
    # surface light: luminance of the painted-out panel, blurred, relative to its median, applied to the logo
    l, t, r, b = [v * K for v in shade_box]
    lum = a.mean(axis=2)
    sh = gaussian_filter(lum, 6 * K)
    ref = np.median(sh[t:b, l:r])
    ratio = np.clip(sh / max(ref, 1), 0.82, 1.12)[..., None]
    rgb = rgb * ratio * white_gain
    a = a * (1 - al[..., None]) + rgb * al[..., None]
    return a

# ------------------------------------------------------------------ truck (source: client trucks mockup, front 3/4 view)
T = up('assets/derived/mockup_logistics-trucks_retouched_v03.png')
for box, kind in [((535, 190, 698, 312), 'dark'), ((118, 312, 232, 370), 'white'), ((340, 322, 408, 362), 'white')]:
    T = inpaint(T, logo_mask(T, box, kind))
# towers seen through the cab's far side window -> dark glass
pm = Image.new('L', (T.shape[1], T.shape[0]), 0)
ImageDraw.Draw(pm).polygon([(117 * K, 218 * K), (196 * K, 220 * K), (197 * K, 284 * K), (116 * K, 284 * K)], fill=255)
win = np.array(pm) > 0
lumT = T.mean(axis=2)
T = inpaint(T, win & (lumT > 85), 700)
# box side panel: plane TL(467,88) TR(733,182) BR(733,378) BL(467,388); logo placed in panel space (700 x 280)
PQ = np.float32([[467, 88], [733, 182], [733, 378], [467, 388]])
Hp = cv2.getPerspectiveTransform(np.float32([[0, 0], [700, 0], [700, 280], [0, 280]]), PQ)
def panel(x, y):
    p = Hp @ np.array([x, y, 1.0]); return (p[0] / p[2], p[1] / p[2])
Hinv = np.linalg.inv(Hp)
q = Hinv @ np.array([615.0, 247.0, 1.0]); cx, cy = q[0] / q[2], q[1] / q[2]   # centre of the AI logo, in panel space
lw = 300; lh = lw * VB[1] / VB[0]
box_quad = [panel(cx - lw / 2, cy - lh / 2), panel(cx + lw / 2, cy - lh / 2), panel(cx + lw / 2, cy + lh / 2), panel(cx - lw / 2, cy + lh / 2)]
T = place(T, 'otlobny-emaar_logo_wordmark-reversed_ar_v01.svg', box_quad, (480, 120, 720, 360), 0.93)
# cab front (near frontal face) and cab door (side plane, receding to the right)
fw = 96; fh = fw * VB[1] / VB[0]; fx, fy = 126, 321
T = place(T, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', [(fx, fy), (fx + fw, fy - 1.5), (fx + fw, fy - 1.5 + fh * .97), (fx, fy + fh)], (110, 300, 250, 390))
T = place(T, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', [(346, 324.5), (402, 327.5), (402, 355.5), (346, 359.5)], (330, 310, 415, 375))

# ------------------------------------------------------------------ car + scooter scene
C = up('assets/derived/mockup_car-scooter-facade_retouched_v03.png')
for box, kind in [((468, 586, 690, 690), 'white'), ((1332, 474, 1460, 534), 'dark'), ((1185, 640, 1290, 700), 'dark')]:
    C = inpaint(C, logo_mask(C, box, kind))
# scooter panel: logo only painted out (curved glossy panel); remove the last colour cast of the old logo
l, t, r, b = [v * K for v in (1185, 640, 1290, 700)]
reg = C[t:b, l:r]; Lm = reg.mean(axis=2, keepdims=True); C[t:b, l:r] = Lm + (reg - Lm) * 0.15
# car door: plane read from the AI logo's alef and baseline (left edge nearer to the camera)
C = place(C, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', [(476, 590), (680, 575), (680, 666), (476, 685)], (450, 560, 720, 700))
# delivery box (near frontal)
dw = 112; dh = dw * VB[1] / VB[0]
C = place(C, 'otlobny-emaar_logo_wordmark-reversed_ar_v01.svg', [(1340, 482), (1452, 482), (1452, 482 + dh), (1340, 482 + dh)], (1300, 440, 1470, 570), 0.9)

# ------------------------------------------------------------------ masks (v07 GrabCut), completed and scaled to 2x
def up_mask(m):
    f = Image.fromarray((m * 255).astype(np.uint8)).resize((m.shape[1] * K, m.shape[0] * K), Image.BILINEAR)
    return np.array(f).astype(float) / 255 > .5
mt = np.load(B / '_work/v07/truck_mask.npy')
pm = Image.new('L', (mt.shape[1], mt.shape[0]), 0)
ImageDraw.Draw(pm).polygon([(238, 95), (462, 74), (468, 75), (734, 176), (735, 392), (238, 402)], fill=255)   # whole box incl. rail and rear trim
mt |= np.array(pm) > 0
yy0, xx0 = np.mgrid[0:mt.shape[0], 0:mt.shape[1]]
wheels = (((xx0 - 395) / 44) ** 2 + ((yy0 - 477) / 61) ** 2 <= 1) | (((xx0 - 634) / 40) ** 2 + ((yy0 - 446) / 43) ** 2 <= 1)
ti0 = np.array(Image.open(B / 'assets/derived/mockup_logistics-trucks_retouched_v03.png').convert('RGB')).astype(int)
band = np.zeros_like(mt); band[448:468] = True
mt &= ~(band & (ti0.mean(axis=2) > 62) & ~wheels)          # asphalt just under the bumper
mt[468:] &= wheels[468:]                       # nothing but the two wheels below the bumper line (no asphalt slab)
mc = np.load(B / '_work/v07/carscoot_mask.npy')
MT, MC = up_mask(mt), up_mask(mc)

def layer(a, m, box, scale):
    m = binary_erosion(m, iterations=1)
    al = gaussian_filter(m.astype(float), 0.9 * K)
    rgba = np.dstack([np.clip(a, 0, 255).astype(np.uint8), (al * 255).astype(np.uint8)])
    L = Image.fromarray(rgba, 'RGBA').crop(tuple(v * K for v in box))
    return L.resize((round(L.width * scale), round(L.height * scale)), Image.LANCZOS) if scale != 1 else L

car = layer(C, MC, (10, 280, 1480, 880), 0.62)
truck = layer(T, MT, (60, 90, 770, 575), 1.0)

CW, CH = 1720 * K, 640 * K
y = np.arange(CH)[:, None]
horizon = 300 * K
t = np.clip((y - horizon) / (CH - horizon), 0, 1) ** 0.8
canvas = np.repeat((np.array([255, 255, 255]) * (1 - t) + np.array([232, 237, 247]) * t)[:, None, :], CW, axis=1).astype(float)
yy, xx = np.mgrid[0:CH, 0:CW]
def shadow(cx, cy, rx, ry, s):
    return (np.exp(-(((xx - cx * K) / (rx * K)) ** 2 + ((yy - cy * K) / (ry * K)) ** 2) * 2.2) * s)[..., None]
tx, ty, cx, cy = 960, 70, 60, 255
truck_base = ty + (537 - 90); car_base = cy + round((805 - 280) * 0.62); scoot_base = cy + round((858 - 280) * 0.62)
sh = (shadow(cx + 250, car_base - 3, 280, 12, .55) + shadow(cx + 680, scoot_base - 3, 215, 10, .58)      # firmer contact shadows
      + shadow(cx + 250, car_base, 330, 26, .18) + shadow(cx + 680, scoot_base, 250, 20, .18)
      + shadow(tx + 335, truck_base - 2, 75, 9, .5) + shadow(tx + 574, ty + (487 - 90) - 2, 55, 7, .45))
pm = Image.new('L', (CW, CH), 0)
ImageDraw.Draw(pm).polygon([((tx + a) * K, (ty + b) * K) for a, b in [(30, 455), (330, truck_base - ty), (640, 395), (690, 380), (300, 395), (30, 420)]], fill=150)
sh = sh + (np.array(pm.filter(ImageFilter.GaussianBlur(14 * K))).astype(float) / 255)[..., None] * .28   # softer under the truck
canvas = canvas * (1 - np.clip(sh, 0, .55)) + np.array([31, 49, 98]) * np.clip(sh, 0, .55) * 0.35
out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).convert('RGBA')
out.alpha_composite(truck, (tx * K, ty * K))
out.alpha_composite(car, (cx * K, cy * K))
out = out.convert('RGB')
out.save(B / 'assets/derived/v08_logistics_fleet-composite.jpg', quality=92, optimize=True, progressive=True)
print('composite', out.size)

# ------------------------------------------------------------------ check crops (300 dpi at the page size: composite runs 297 mm wide)
scale_300 = (297 / 25.4 * 300) / out.width          # px of a 300 dpi render per composite px
def crop(name, box_c):
    c = out.crop(tuple(v * K for v in box_c))
    c = c.resize((max(1, round(c.width * scale_300)), max(1, round(c.height * scale_300))), Image.LANCZOS)
    c.save(W / f'check300_{name}.png')
crop('truck-box', (tx + 470, ty + 90, tx + 700, ty + 260))
crop('truck-cab-front-and-door', (tx + 50, ty + 210, tx + 360, ty + 290))
crop('car-door', (cx + 270, cy + 190, cx + 430, cy + 260))
crop('delivery-box', (cx + 810, cy + 115, cx + 900, cy + 165))
crop('scooter-panel', (cx + 715, cy + 225, cx + 800, cy + 270))
ref = Image.open(io.BytesIO(cairosvg.svg2png(url=str(LOGO / 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg'), output_width=600)))
ref.save(W / 'check300_reference_wordmark.png')
