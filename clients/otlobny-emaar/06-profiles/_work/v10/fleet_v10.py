#!/usr/bin/env python3
"""v10 logistics image (v09 method; r6 m3: cab-door patch limited to the door panel; floor fades to white at its edges)
v09 logistics image: the client's own fleet image (assets/mockups/mockup_fleet_car-scooter-truck.png, a copy of
_originals/client-uploads_2026-11-14/..., never edited) prepared for p12.

1. Edge clean-up: the cut-out was made from a black background; semi-transparent edge pixels are un-premultiplied
   against black and the outermost 1 px of alpha is eased, so no dark fringe shows on the pale floor.
2. Third-party marks painted out with the surrounding surface: Suzuki badge, "DZIRE" plate, "ISUZU" lettering
   (row-wise interpolation keeps the grille bars).
3. AI-drawn logos and garbled descriptor text («اطليني», "CONSANY"...) painted out with each panel's own paint, then
   the REAL lockup v02 / wordmark (04-identity/02-logo) placed with cv2.getPerspectiveTransform and the panel's light:
   - truck box (35 mm on the page): white LOCKUP v02 (descriptor «شركة اطلبني إعمار المحدودة» / OTLOBNY EMAR COMPANY LTD.)
   - cab front, cab door, car door, delivery box, scooter panel (10-17 mm on the page, under the lockup's 45 mm minimum,
     descriptor would be 1-2 pt): WORDMARK alone; their descriptor lines are painted out (clean panel).
   White versions on the blue boxes (system.md: royal blue -> white), colour versions on white panels.
4. Placed on one pale floor with contact and ambient shadows. Working scale x2.
Output: assets/derived/v10_logistics_fleet-client.jpg + 300 dpi crops in _work/v10/."""
import io, numpy as np, cv2, cairosvg
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, binary_dilation, binary_erosion
from pathlib import Path

B = Path(__file__).resolve().parents[2]
W = B / '_work/v10'
LOGO = B.parent / '04-identity/02-logo'
K = 2

src = np.array(Image.open(B / 'assets/mockups/mockup_fleet_car-scooter-truck.png').convert('RGBA')).astype(float)
rgb, al = src[..., :3], src[..., 3] / 255.0
# 1. de-fringe: un-premultiply edge pixels against the original black ground
edge = (al > 0.02) & (al < 0.98)
rgb[edge] = np.clip(rgb[edge] / al[edge][:, None], 0, 255)
# ease the outermost opaque ring where it is darker than the pixels just inside (black halo)
inner = binary_erosion(al > .5, iterations=2)
ring = (al > .5) & ~inner
lum = rgb.mean(axis=2)
inl = gaussian_filter(np.where(inner, lum, 0), 2) / (gaussian_filter(inner.astype(float), 2) + 1e-6)
dark_ring = ring & (lum < inl - 45)
al[dark_ring] *= 0.35
# hard 1 px choke + soft re-feather of the whole silhouette (removes the speckled rim left from the black ground)
choke = binary_erosion(al > .5, iterations=1)
al = np.minimum(al, gaussian_filter(choke.astype(float), 0.7))

# upscale x2
def up(a, mode=Image.LANCZOS):
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return np.array(im.resize((im.width * K, im.height * K), mode)).astype(float)
R = up(rgb)
A = np.array(Image.fromarray((al * 255).astype(np.uint8)).resize((rgb.shape[1] * K, rgb.shape[0] * K), Image.LANCZOS)).astype(float) / 255
H_, W_ = R.shape[:2]

def box_mask(box):
    l, t, r, b = [v * K for v in box]
    m = np.zeros((H_, W_), bool); m[t:b, l:r] = True
    return m

def fill_from(R, hole, good, sigma=7):
    """Normalised convolution: fill hole from 'good' panel pixels only (keeps the panel's own gradient)."""
    w = good.astype(float)
    f = np.stack([gaussian_filter(R[..., i] * w, sigma * K) for i in range(3)], -1) / (gaussian_filter(w, sigma * K)[..., None] + 1e-6)
    out = R.copy()
    n = np.random.default_rng(5).normal(0, 1.6, (hole.sum(), 3))
    out[hole] = f[hole] + n
    return out

def rowfill(R, hole):
    """Row-wise linear interpolation across the hole (keeps horizontal grille bars)."""
    out = R.copy()
    for y in np.where(hole.any(axis=1))[0]:
        xs = np.where(hole[y])[0]
        # split into runs
        runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
        for run in runs:
            x0, x1 = run[0] - 1, run[-1] + 1
            if x0 < 0 or x1 >= W_: continue
            t = (run - x0) / (x1 - x0)
            out[y, run] = out[y, x0] * (1 - t)[:, None] + out[y, x1] * t[:, None]
    return gaussian_filter(out, (1.0, 0.3, 0)) * hole[..., None] + out * ~hole[..., None]

lumR = R.mean(axis=2); satR = R.max(axis=2) - R.min(axis=2)
r_, g_, b_ = R[..., 0], R[..., 1], R[..., 2]

# 2. third-party marks
for box in [(128, 497, 170, 545), (100, 556, 196, 581), (1360, 471, 1456, 498)]:
    z = box_mask(box)
    hole = binary_dilation(z & (lumR > 45), iterations=3 * K) & binary_dilation(z, iterations=2 * K)
    R = rowfill(R, hole)
lumR = R.mean(axis=2); satR = R.max(axis=2) - R.min(axis=2)

# 3a. paint out the AI logos + descriptors
blue_panel = (b_ > r_ + 40) & (lumR < 150) & (g_ < b_)
def white_hole(box):
    z = box_mask(box)
    med = np.median(lumR[z])
    txt = z & ((satR > 26) | ((lumR < med - 10) & (lumR > 80)))
    hole = binary_dilation(txt, iterations=5 * K) & binary_dilation(z, iterations=2 * K)
    good = binary_dilation(z, iterations=14 * K) & ~hole & (satR < 26) & (lumR > 110) & (A > .99)
    return hole, good
def blue_hole(box):
    z = box_mask(box)
    txt = z & ~blue_panel
    hole = binary_dilation(txt, iterations=3 * K) & binary_dilation(z, iterations=2 * K)
    good = binary_dilation(z, iterations=14 * K) & ~hole & blue_panel & (A > .99)
    return hole, good
SURF = {   # paint-out boxes (source px)
 'truck-box': ('blue', (1846, 166, 2110, 346)),
 'cab-front': ('white', (1341, 359, 1481, 449)),
 'cab-door': ('white', (1610, 367, 1704, 446)),
 'car-door': ('white', (562, 420, 724, 536)),
 'delivery-box': ('blue', (1112, 312, 1250, 398)),
 'scooter-panel': ('white', (1088, 470, 1180, 530)),
}
from PIL import ImageDraw
def poly_mask(pts):
    pm = Image.new('L', (W_, H_), 0); ImageDraw.Draw(pm).polygon([(x * K, y * K) for x, y in pts], fill=255)
    return np.array(pm) > 0
SCOOT_POLY = [(1088, 499), (1160, 461), (1183, 476), (1184, 494), (1102, 534), (1084, 530)]
for name, (kind, box) in SURF.items():
    if name == 'scooter-panel':     # curved panel: only the logo's own blue/green pixels inside a band that follows it
        band = poly_mask(SCOOT_POLY)
        logo = band & (lumR > 45) & (((b_ > r_ + 35) & (lumR < 170)) | ((g_ > r_ + 35) & (g_ > b_)))
        hole = binary_dilation(logo, iterations=3 * K) & band
        good = binary_dilation(band, iterations=10 * K) & ~hole & (satR < 28) & (lumR > 200) & (A > .99)
        R = fill_from(R, hole, good, 6)
        continue
    hole, good = (blue_hole if kind == 'blue' else white_hole)(box)
    if name == 'cab-door':   # m3: keep the mirror-bracket corner and the handle out of the patch (door panel only)
        keep = box_mask((1596, 352, 1630, 392)) | box_mask((1704, 360, 1722, 424))
        src_dark = binary_dilation((lumR < 75) & (satR < 30), iterations=1 * K)
        hole &= ~(keep & src_dark)
    R = fill_from(R, hole, good, 6 if kind == 'blue' else 8)
    if kind == 'white':   # second pass: faint grey ghosts of the old lettering (darker than the local panel)
        z = box_mask(box)
        Lm = R.mean(axis=2)
        dev = gaussian_filter(Lm, 10 * K) - Lm
        h2 = binary_dilation(z & (dev > 5) & (Lm > 120), iterations=2 * K) & z
        g2 = binary_dilation(z, iterations=14 * K) & ~h2 & ((R.max(axis=2) - R.min(axis=2)) < 26) & (Lm > 110) & (A > .99)
        R = fill_from(R, h2, g2, 8)

# 3b. place the real marks
VB_W = (307.711, 124.597); VB_L = (307.711, 138.25)
def svg(name, width=2400):
    return np.array(Image.open(io.BytesIO(cairosvg.svg2png(url=str(LOGO / name), output_width=width))).convert('RGBA')).astype(float)
def place(R, name, quad, shade_box, gain=1.0):
    L = svg(name); h, w = L.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32([[x * K, y * K] for x, y in quad]))
    c = cv2.warpPerspective(L[..., :3], M, (W_, H_), flags=cv2.INTER_LINEAR)
    a = cv2.warpPerspective(L[..., 3], M, (W_, H_), flags=cv2.INTER_LINEAR)[..., None] / 255
    l, t, r, b = [v * K for v in shade_box]
    sh = gaussian_filter(R.mean(axis=2), 6 * K); ref = np.median(sh[t:b, l:r])
    ratio = np.clip(sh / max(ref, 1), 0.85, 1.1)[..., None]
    return R * (1 - a) + c * ratio * gain * a
def rect(cx, cy, w, h, ang=0.0, skew_r=0.0):
    """Quad centred at (cx, cy), width w, height h, rotated ang degrees; skew_r shrinks the right edge (receding plane)."""
    hw, hh = w / 2, h / 2
    pts = np.array([[-hw, -hh], [hw, -hh * (1 - skew_r)], [hw, hh * (1 - skew_r)], [-hw, hh]])
    c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    pts = pts @ np.array([[c, s], [-s, c]])
    return [(cx + x, cy + y) for x, y in pts]

# truck box: panel plane TL(1760,58) TR(2152,165) BR(2152,440) BL(1760,440); lockup centred where the AI block was
PQ = np.float32([[1760, 58], [2152, 165], [2152, 440], [1760, 440]])
Hp = cv2.getPerspectiveTransform(np.float32([[0, 0], [400, 0], [400, 300], [0, 300]]), PQ)
Hi = np.linalg.inv(Hp)
def to_panel(x, y):
    p = Hi @ np.array([x, y, 1.0]); return p[0] / p[2], p[1] / p[2]
def to_img(x, y):
    p = Hp @ np.array([x, y, 1.0]); return p[0] / p[2], p[1] / p[2]
pl, pt = to_panel(1856, 186); pr, pb = to_panel(2104, 186)
pw = pr - pl; ph = pw * VB_L[1] / VB_L[0]
quad = [to_img(pl, pt), to_img(pl + pw, pt), to_img(pl + pw, pt + ph), to_img(pl, pt + ph)]
R = place(R, 'otlobny-emaar_logo_lockup-white_ar-en_v02.svg', quad, (1800, 120, 2140, 400), 0.97)
TRUCK_LOCKUP_PX = 2104 - 1856
# wordmark-alone surfaces
R = place(R, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', rect(1411, 389, 124, 124 * VB_W[1] / VB_W[0]), (1340, 350, 1485, 455))
R = place(R, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', rect(1656, 390, 90, 90 * VB_W[1] / VB_W[0], -1.0, 0.06), (1600, 355, 1710, 450))
R = place(R, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', rect(641, 460, 148, 148 * VB_W[1] / VB_W[0], -1.8), (560, 415, 725, 535))
R = place(R, 'otlobny-emaar_logo_wordmark-white_ar_v01.svg', rect(1180, 340, 116, 116 * VB_W[1] / VB_W[0]), (1110, 305, 1252, 400), 0.97)
R = place(R, 'otlobny-emaar_logo_wordmark-colour_ar_v01.svg', rect(1134, 500, 88, 88 * VB_W[1] / VB_W[0], -17.0), (1085, 465, 1185, 535))

# 4. floor and shadows (canvas in source px x K)
PADT, PADB = 40, 50
CH = (719 + PADT + PADB) * K; CW = W_
y = np.arange(CH)[:, None]
hz = 420 * K
t = np.clip((y - hz) / (CH - hz), 0, 1) ** .8
xx_ = np.arange(CW)[None, :]
fx = np.clip(np.minimum(xx_, CW - 1 - xx_) / (0.07 * CW), 0, 1)                 # floor fades out at the sides
fy = np.clip((CH - 1 - np.arange(CH)[:, None]) / (0.14 * CH), 0, 1)              # ... and towards the bottom edge
tt = t * fx * fy
canvas = (np.array([255, 255, 255]) * (1 - tt[..., None]) + np.array([232, 237, 247]) * tt[..., None]).astype(float)
Af = np.zeros((CH, CW)); Af[PADT * K:PADT * K + H_] = A
solid = Af > .5
bottom = np.full(CW, -1)
for x in range(CW):
    ys = np.where(solid[:, x])[0]
    if len(ys): bottom[x] = ys.max()
contact = np.zeros((CH, CW))
for x in np.where(bottom > 0)[0]:
    yb = bottom[x]
    if solid[max(yb - 3 * K, 0):yb, x].all():
        contact[yb - 2 * K: yb + 2 * K, x] = 1
contact = gaussian_filter(contact, (2.5 * K, 5 * K)) * 1.4
amb = np.zeros((CH, CW))
for x in np.where(bottom > 0)[0]:
    amb[bottom[x], x] = 1
amb = gaussian_filter(gaussian_filter(amb, (1, 1)) * 1.0, (9 * K, 22 * K)) * 22
sh = np.clip(contact * .55 + amb * .22, 0, .6)[..., None]
canvas = canvas * (1 - sh) + np.array([31, 49, 98]) * sh * 0.35
Rf = np.zeros((CH, CW, 3)); Rf[PADT * K:PADT * K + H_] = R
canvas = canvas * (1 - Af[..., None]) + Rf * Af[..., None]
out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
out.save(B / 'assets/derived/v10_logistics_fleet-client.jpg', quality=92, optimize=True, progressive=True)
print('fleet image', out.size, 'truck lockup width px (source):', TRUCK_LOCKUP_PX)

# 300 dpi crops at the page size (image runs 297 mm wide)
s300 = (297 / 25.4 * 300) / out.width
def crop(name, box):
    l, t, r, b = box
    c = out.crop((l * K, (t + PADT) * K, r * K, (b + PADT) * K))
    c.resize((round(c.width * s300), round(c.height * s300)), Image.LANCZOS).save(W / f'check300_{name}.png')
for name, (kind, box) in SURF.items():
    l, t, r, b = box; crop(name, (l - 20, t - 20, r + 20, b + 20))
crop('suzuki-badge_dzire', (80, 480, 220, 600)); crop('isuzu', (1320, 450, 1500, 510))
crop('edge_car-front', (0, 380, 160, 640)); crop('edge_truck-rear', (2080, 60, 2188, 660))
