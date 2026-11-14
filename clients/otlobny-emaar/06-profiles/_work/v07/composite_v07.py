#!/usr/bin/env python3
"""v07: one composed logistics visual from the client's own mockups — car + delivery scooter (one cut-out group, kept in
its original relative positions) and the box truck (cut-out from the front three-quarter view; the Riyadh tower behind it
is removed with the background). Both stand on one shared light ground with soft contact shadows.
Output: assets/derived/v07_logistics_fleet-composite.png (illustrative image)."""
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_erosion, gaussian_filter
from pathlib import Path
B = Path(__file__).resolve().parents[2]
W = B / '_work/v07'

def layer(src, mask_name, box, scale):
    im = Image.open(B / src).convert('RGB')
    m = np.load(W / f'{mask_name}_mask.npy')
    m = binary_erosion(m, iterations=1)
    a = gaussian_filter(m.astype(float), 0.8)                     # 1 px feather, no halo
    rgba = np.dstack([np.array(im), (a * 255).astype(np.uint8)])
    L = Image.fromarray(rgba, 'RGBA').crop(box)
    if scale != 1:
        L = L.resize((round(L.width * scale), round(L.height * scale)), Image.LANCZOS)
    return L

car = layer('assets/derived/mockup_car-scooter-facade_retouched_v03.png', 'carscoot', (10, 280, 1480, 880), 0.62)
truck = layer('assets/derived/mockup_logistics-trucks_retouched_v03.png', 'truck', (60, 90, 770, 575), 1.0)

CW, CH = 1720, 640
canvas = np.zeros((CH, CW, 3), float)
# shared ground: white sky fading into a pale brand-tint floor
y = np.arange(CH)[:, None]
horizon = 300
t = np.clip((y - horizon) / (CH - horizon), 0, 1) ** 0.8
top, floor = np.array([255, 255, 255]), np.array([232, 237, 247])
canvas[:] = np.repeat((top * (1 - t) + floor * t)[:, None, :], CW, axis=1)

def shadow(cx, cy, rx, ry, strength):
    yy, xx = np.mgrid[0:CH, 0:CW]
    d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    s = np.exp(-d * 2.2) * strength
    return s[:, :, None]

# placements: truck behind (right), car + scooter in front (left); baselines from each source's wheel contact line
tx, ty = 960, 70            # truck top-left on canvas
cx, cy = 60, 255             # car group top-left on canvas
truck_base = ty + (537 - 90)            # front wheel contact (source y 537)
car_base = cy + round((805 - 280) * 0.62)   # car wheels
scoot_base = cy + round((858 - 280) * 0.62)
sh = (shadow(cx + 250, car_base - 4, 300, 18, .38) + shadow(cx + 680, scoot_base - 4, 230, 14, .40)
      + shadow(tx + 335, truck_base - 2, 75, 9, .55) + shadow(tx + 574, ty + (487 - 90) - 2, 55, 7, .5))
# soft ground shadow under the truck body: a blurred quadrilateral from the bumper to the rear axle
from PIL import ImageDraw
pm = Image.new('L', (CW, CH), 0)
ImageDraw.Draw(pm).polygon([(tx + 30, ty + 455), (tx + 330, truck_base), (tx + 640, ty + 395), (tx + 690, ty + 380), (tx + 300, ty + 395), (tx + 30, ty + 420)], fill=150)
pm = np.array(pm.filter(ImageFilter.GaussianBlur(14))).astype(float) / 255
sh = sh + pm[:, :, None] * .45
canvas = canvas * (1 - np.clip(sh, 0, .5)) + np.array([31, 49, 98]) * np.clip(sh, 0, .5) * 0.35
out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).convert('RGBA')
out.alpha_composite(truck, (tx, ty))
out.alpha_composite(car, (cx, cy))
out = out.convert('RGB')
out.save(B / 'assets/derived/v07_logistics_fleet-composite.png', optimize=True)
out.resize((out.width * 2, out.height * 2), Image.NEAREST).crop((900, 300, 2300, 1100)).save(W / 'composite_zoom200_scooter-truck.png')
print('composite', out.size)
