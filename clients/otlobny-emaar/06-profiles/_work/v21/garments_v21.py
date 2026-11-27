#!/usr/bin/env python3
"""v21: v13 garment method unchanged; the lockup placed on the garments is v03 (registered name, client approval
2026-11-27). Only the window-cleaner panel is saved (assets/derived/v21_client_triptych-cleaner.png): it is the only
garment lockup that shows in the book (p1 small diamond). The lockup is placed by WIDTH with its TOP edge anchored.
REPRO=1 re-runs the v13 composite (lockup v02) into REPRO_OUT to prove the method reproduces v13.
--- v13 docstring follows ---
v13: the client's new AI images (2026-11-15) — fix the malformed logos / descriptors on garments.
Sources: assets/mockups/ copies of _originals/client-uploads_2026-11-15/ (originals never edited).
Per garment: the AI logo + descriptor are painted out with the fabric's own navy (normalised convolution from the
surrounding fabric, which keeps the fold shading), then the REAL white lockup v02 (or white wordmark alone) is
placed with cv2.getPerspectiveTransform, shaded by the fabric light and softened to the photo's own sharpness.
A logo that sits over a strong shoulder curve is painted out only (a clean garment beats a crooked patch).
Outputs (full colour, no grade):
  assets/derived/v13_client_triptych-engineers.png, v13_client_triptych-cleaner.png, v13_client_triptych-landscaping.png
  assets/derived/v13_client_palm-planting-team.png, v13_client_street-planting.png
  _work/v13/check_*.png (before | after, 4x)"""
import io, numpy as np, cv2, cairosvg
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, binary_dilation, binary_erosion
from pathlib import Path

B = Path(__file__).resolve().parents[2]
W = B / '_work/v21'
import os
REPRO = os.environ.get('REPRO') == '1'
LOGO = B.parent / '04-identity/02-logo'
VB_W = (307.711, 124.597); VB_L2 = (307.711, 138.25); VB_L = VB_L2 if REPRO else (307.711, 141.848)   # v03 is 2.6% taller

def svg(name, width=1600):
    return np.array(Image.open(io.BytesIO(cairosvg.svg2png(url=str(LOGO / name), output_width=width))).convert('RGBA')).astype(float)

def poly_mask(shape, pts):
    pm = Image.new('L', (shape[1], shape[0]), 0); ImageDraw.Draw(pm).polygon(pts, fill=255)
    return np.array(pm) > 0

def paint_out(a, region):
    """Remove the light / green print inside region; refill from the navy fabric around it.
    The hole is limited to the garment (navy fabric closed over its own print), so background is never touched."""
    from scipy.ndimage import binary_closing, binary_fill_holes
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = a.mean(axis=2); sat = a.max(axis=2) - a.min(axis=2)
    fabric = (b > r + 12) & (lum < 125)
    # polygons are drawn inside each garment's silhouette; within them, print = everything that is not navy fabric
    garment = binary_closing(fabric | (region & ((lum > 120) | (g > r + 40))), iterations=6) & binary_dilation(fabric, iterations=10)
    ink = region & garment & ~fabric
    hole = binary_dilation(ink, iterations=4) & region & garment
    good = binary_dilation(region, iterations=18) & ~hole & fabric
    w = good.astype(float)
    f = np.stack([gaussian_filter(a[..., i] * w, 5) for i in range(3)], -1) / (gaussian_filter(w, 5)[..., None] + 1e-6)
    out = a.copy()
    out[hole] = f[hole] + np.random.default_rng(3).normal(0, 2.2, (hole.sum(), 3))
    # second pass: faint ghosts of the old print (lighter than the local fabric)
    L2 = out.mean(axis=2); loc = gaussian_filter(L2, 6)
    h2 = binary_dilation(region & garment & ((L2 > loc + 10) | (L2 < loc - 22)), iterations=2) & region & garment
    w2 = (binary_dilation(region, iterations=18) & ~h2 & ~hole & fabric | (hole & ~h2)).astype(float)
    f2 = np.stack([gaussian_filter(out[..., i] * w2, 4) for i in range(3)], -1) / (gaussian_filter(w2, 4)[..., None] + 1e-6)
    out[h2] = f2[h2] + np.random.default_rng(4).normal(0, 2.0, (h2.sum(), 3))
    return out

def place(a, name, quad, soften=0.45, gain=1.0):
    L = svg(name); h, w = L.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(quad))
    H_, W_ = a.shape[:2]
    c = cv2.warpPerspective(L[..., :3], M, (W_, H_), flags=cv2.INTER_AREA)
    al = cv2.warpPerspective(L[..., 3], M, (W_, H_), flags=cv2.INTER_AREA) / 255
    al = gaussian_filter(al, soften)                           # match the photo's own softness (no crisp vector edge)
    c = np.stack([gaussian_filter(c[..., i], soften) for i in range(3)], -1)
    sh = gaussian_filter(a.mean(axis=2), 4)                     # fabric folds carry through the print
    ys, xs = np.nonzero(al > .3)
    ref = np.median(sh[ys, xs]) if len(ys) else 1
    ratio = np.clip(sh / max(ref, 1), 0.85, 1.08)[..., None]
    return a * (1 - al[..., None]) + c * ratio * gain * al[..., None]

def rect(cx, cy, w, h, ang=0.0):
    pts = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]])
    c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    pts = pts @ np.array([[c, s], [-s, c]])
    return [(cx + x, cy + y) for x, y in pts]

def save(a, name):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(B / 'assets/derived' / name, optimize=True)

def check(before, after, box, name, k=4):
    l, t, r, b = box
    x = Image.fromarray(np.clip(before[t:b, l:r], 0, 255).astype(np.uint8)); y = Image.fromarray(np.clip(after[t:b, l:r], 0, 255).astype(np.uint8))
    x = x.resize((x.width * k, x.height * k), Image.LANCZOS); y = y.resize((y.width * k, y.height * k), Image.LANCZOS)
    S = Image.new('RGB', (x.width * 2 + 10, x.height), (128, 128, 128)); S.paste(x, (0, 0)); S.paste(y, (x.width + 10, 0)); S.save(W / f'check_{name}.png')

# ------------------------------------------------------------------ triptych
T0 = np.array(Image.open(B / 'assets/mockups/photo_triptych_landscaping-construction-cleaning.png').convert('RGB')).astype(float)
T = T0.copy()
VESTS = [  # (paint-out polygon, lockup centre, width, angle)
    ([(752, 470), (884, 466), (882, 562), (746, 558)], (812, 512), 124, 1.5),        # engineer left
    ([(1258, 500), (1374, 500), (1376, 600), (1256, 600)], (1316, 551), 114, -1.0),  # engineer right
    ([(1555, 420), (1784, 418), (1786, 552), (1550, 572)], (1668, 492), 226, -4.0),  # window cleaner
]
for poly, (cx, cy), w, ang in VESTS:
    T = paint_out(T, poly_mask(T.shape, poly))
for poly, (cx, cy), w, ang in VESTS:
    h = w * VB_L[1] / VB_L[0]; d = (h - w * VB_L2[1] / VB_L2[0]) / 2          # keep the TOP edge where v02 had it
    a_ = np.radians(ang)
    T = place(T, 'otlobny-emaar_logo_lockup-white_ar-en_v02.svg' if REPRO else 'otlobny-emaar_logo_lockup-white_ar-en_v03.svg',
              rect(cx - d * np.sin(a_), cy + d * np.cos(a_), w, h, ang))   # local "down" is (-sin, cos)
if not REPRO: check(T0, T, (1540, 405, 1800, 585), 'cleaner', 3)
if REPRO: Image.fromarray(np.clip(T[:, 1456:], 0, 255).astype(np.uint8)).save(os.environ['REPRO_OUT'])
else: save(T[:, 1456:], 'v21_client_triptych-cleaner.png')   # landscaping panel: no lockup, v13 file still used; engineers panel: not in the book
print('done')

