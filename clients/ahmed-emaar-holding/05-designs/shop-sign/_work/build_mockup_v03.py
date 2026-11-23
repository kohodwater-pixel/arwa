"""v03 photomontage: individual raised letters on the wall (no panel).
Visualisation only. The photo is not retouched: letters, their returns and
their cast shadows are composited on top; the wall pattern, crack and rebar
stay visible. Caption strip is added below the photo.

Geometry: wall-plane frame in cm, same homography as v01/v02 (x 0-250 between
the column stubs; y = 60 at the slab's front lower edge, y = 0 is 60 cm above
it; scale rests on the assumed ~30 cm slab-edge face and is approximate).
Letters: bounding box x 0-250, top at Y_TOP, i.e. the whole lockup on the wall
ABOVE the crack line (crack at y ~ 31-40), clear of the damaged strip.
Depth: camera ~6 m away, ~2 m below the slab edge (estimates) -> letter faces
project up and away from the camera centre; returns are visible below.
Sun: high and in front, slightly right (from the shutter-housing shadow) ->
cast shadows fall down and a little left.
"""
import sys, io, json, subprocess
import numpy as np
import cairosvg
from PIL import Image, ImageFilter, ImageChops
from build_mockup_v02 import QUAD, coeffs, PHOTO

M = json.load(open('metrics_v03.json'))
LW, LH = M['overall_w'], M['overall_h']
Y_TOP = -44.9                     # lettering top, wall frame (cm)
X0, Y0, X1, Y1 = -15, -60, 265, 20  # flat canvas extent in wall cm
PPC = 10
CAM = (150.0, 260.0, 600.0)       # camera x, y in wall frame, distance D (cm) - estimates
STANDOFF, DEPTH = 1.5, 4.0        # cm
SUN = (-0.3, 1.8)                 # shadow offset per cm of projection from the wall

src = [(0, 0), (250, 0), (250, 60), (0, 60)]
_a = coeffs(src, QUAD)            # wall -> photo


def w2p(x, y):
    a, b, c, d, e, f, g, h = _a
    den = g * x + h * y + 1
    return ((a * x + b * y + c) / den, (d * x + e * y + f) / den)


def render_mask(name):
    w, h = int(round(LW * PPC)), int(round(LH * PPC))
    png = cairosvg.svg2png(url=f'v03_letters_{name}.svg', output_width=w, output_height=h)
    m = Image.open(io.BytesIO(png)).convert('RGBA').split()[3]
    canvas = Image.new('L', (int((X1 - X0) * PPC), int((Y1 - Y0) * PPC)), 0)
    canvas.paste(m, (int((0 - X0) * PPC), int((Y_TOP - Y0) * PPC)))
    return canvas


def shift(m, dx_cm, dy_cm):
    return m.transform(m.size, Image.AFFINE, (1, 0, -dx_cm * PPC, 0, 1, -dy_cm * PPC), Image.BILINEAR)


def solid(size, rgb):
    return Image.new('RGBA', size, rgb + (255,))


def metal(size, top, bottom, streak=6):
    W, H = size
    t = np.linspace(0, 1, H)[:, None, None]
    base = np.array(top) * (1 - t) + np.array(bottom) * t
    s = np.sin(np.linspace(0, 90, W))[None, :, None] * streak
    g = np.zeros((H, W, 4), 'uint8'); g[..., :3] = np.clip(base + s, 0, 255); g[..., 3] = 255
    return Image.fromarray(g, 'RGBA')


GOLD_FACE = ((242, 210, 145), (200, 154, 80))
GOLD_RET = (122, 88, 40)
NAVY_FACE = ((40, 58, 82), (22, 38, 56))
NAVY_RET = (9, 17, 27)
VARIANTS = {
    'v1-gold': {'label_ar': 'الصيغة 1: حروف ذهبية بالكامل (وجه وجوانب ذهبية)', 'label_en': 'Variant V1: all-gold letters (gold faces and returns)',
                'face': {'mark': GOLD_FACE, 'name-ar': GOLD_FACE, 'name-en': GOLD_FACE},
                'ret': {'mark': GOLD_RET, 'name-ar': GOLD_RET, 'name-en': GOLD_RET}, 'outline': None},
    'v2-navy': {'label_ar': 'الصيغة 2: الاسمان بحروف كحلية والشعار ذهبي', 'label_en': 'Variant V2: navy lettering, gold mark',
                'face': {'mark': GOLD_FACE, 'name-ar': NAVY_FACE, 'name-en': NAVY_FACE},
                'ret': {'mark': GOLD_RET, 'name-ar': NAVY_RET, 'name-en': NAVY_RET}, 'outline': None},
    'v3-gold-navy-edge': {'label_ar': 'الصيغة 3: وجه ذهبي بجوانب كحلية وحافة كحلية خلف الحرف', 'label_en': 'Variant V3: gold faces with navy returns and a navy backer edge',
                          'face': {'mark': GOLD_FACE, 'name-ar': GOLD_FACE, 'name-en': GOLD_FACE},
                          'ret': {'mark': NAVY_RET, 'name-ar': NAVY_RET, 'name-en': NAVY_RET}, 'outline': (12, 24, 38)},
}


def build_flat(var):
    v = VARIANTS[var]
    masks = {n: render_mask(n) for n in ('mark', 'name-ar', 'name-en')}
    size = masks['mark'].size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    shadow = Image.new('L', size, 0)
    cx = {'mark': LW - M['mark']['w'] / 2, 'name-ar': M['pos']['left'] + M['name_ar']['width'] / 2,
          'name-en': M['pos']['left'] + M['name_en']['width'] / 2}
    cy = {'mark': Y_TOP + LH / 2, 'name-ar': Y_TOP + 12, 'name-en': Y_TOP + LH - 4}
    zf = STANDOFF + DEPTH
    for n in ('name-en', 'name-ar', 'mark'):
        m = masks[n]
        X, Yy, D = CAM
        fdx, fdy = (cx[n] - X) * zf / D, (cy[n] - Yy) * zf / D          # face projected offset
        bdx, bdy = (cx[n] - X) * STANDOFF / D, (cy[n] - Yy) * STANDOFF / D
        # cast shadow on the wall from the whole letter (back to face)
        for z in np.linspace(STANDOFF, zf, 6):
            shadow = ImageChops.lighter(shadow, shift(m, SUN[0] * z, SUN[1] * z))
        if v['outline']:
            ol = shift(m, bdx, bdy).filter(ImageFilter.MaxFilter(25))   # ~1.2 cm navy backer edge
            layer.paste(solid(size, v['outline']), (0, 0), ol)
        # returns: stack from back to face
        steps = 24
        for i in range(steps + 1):
            t = i / steps
            mm = shift(m, bdx + (fdx - bdx) * t, bdy + (fdy - bdy) * t)
            layer.paste(solid(size, v['ret'][n]), (0, 0), mm)
        fm = shift(m, fdx, fdy)
        layer.paste(metal(size, *v['face'][n]), (0, 0), fm)
    shadow = shadow.filter(ImageFilter.GaussianBlur(PPC * 0.8))
    return layer, shadow


def warp(img, photo_size):
    W, H = img.size
    flat_pts = [(0, 0), (W, 0), (W, H), (0, H)]
    wall_pts = [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]
    photo_pts = [w2p(*p) for p in wall_pts]
    return img.transform(photo_size, Image.PERSPECTIVE, coeffs(photo_pts, flat_pts), Image.BICUBIC)


def caption(var, w):
    v = VARIANTS[var]
    F = '/home/user/arwa/assets/fonts/'
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:A;src:url("file://{F}ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:A;src:url("file://{F}ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}
body{{margin:0;padding:22px 30px 24px;font-family:A;background:#fff;color:#222;font-size:21px;line-height:1.75}}
.ar{{direction:rtl;text-align:right}} .en{{direction:ltr;text-align:left;margin-top:12px;font-size:19px;line-height:1.5;color:#333}}
b{{font-weight:600;color:#102232}} ul{{margin:0;padding:0 1.2em 0 0}} .en ul{{padding:0 0 0 1.2em}}</style></head><body>
<div class="ar"><b>تصوّر توضيحي فقط — حروف بارزة مثبّتة على الجدار مباشرة، على صورة موقع العميل، وليست صورة لتركيب فعلي.</b><ul>
<li>{v['label_ar']}.</li>
<li>المقاسات مفترضة: عرض الكتابة 250 سم وارتفاعها نحو 45 سم؛ تُحدَّد بالقياس في الموقع.</li>
<li>الشعار إعادة رسم مؤقتة بانتظار الملف الأصلي من العميل.</li>
<li>يُشترط فحص وترميم حافة السقف والجدار قبل التركيب؛ مسامير التثبيت تدخل في هذه الخرسانة المتشققة.</li></ul></div>
<div class="en"><b>VISUALISATION ONLY — raised letters fixed directly on the wall, montaged on the client's site photo; not a photo of an installation.</b><ul>
<li>{v['label_en']}.</li>
<li>Sizes are assumed: lettering 250 cm wide, about 45 cm high; to be measured on site.</li>
<li>The logo is a provisional trace pending the client's original file.</li>
<li>The slab edge and wall must be inspected and repaired before installation; the fixings go into this cracked concrete.</li></ul></div>
</body></html>"""
    open(f'v03_caption-{var}.html', 'w').write(html)
    subprocess.run(['node', 'shot.cjs', f'v03_caption-{var}.html', f'v03_caption-{var}.png', str(w)], check=True)
    return Image.open(f'v03_caption-{var}.png').convert('RGB')


if __name__ == '__main__':
    out = sys.argv[1]
    photo = Image.open(PHOTO).convert('RGBA')
    details = []
    for var in VARIANTS:
        layer, shadow = build_flat(var)
        L = warp(layer, photo.size)
        S = warp(shadow.convert('RGBA'), photo.size).split()[0]
        comp = photo.copy()
        comp.paste((25, 20, 15, 255), (0, 0), S.point(lambda v: int(v * 0.42)))
        comp.alpha_composite(L)
        cap = caption(var, photo.width)
        canvas = Image.new('RGB', (photo.width, photo.height + cap.height), 'white')
        canvas.paste(comp.convert('RGB'), (0, 0)); canvas.paste(cap, (0, photo.height))
        canvas.save(f'{out}/ahmed-emaar-holding_shop-sign_letters-on-wall-mockup-site-{var}_ar-en_v03.png')
        det = comp.convert('RGB').crop((120, 150, 1300, 620)); det.save(f'v03_mock_detail_{var}.png'); details.append((var, det))
    # side-by-side sheet of the three variants (detail crops)
    w, h = details[0][1].size
    sheet = Image.new('RGB', (w, (h + 10) * len(details)), 'white')
    for i, (_, d) in enumerate(details):
        sheet.paste(d, (0, i * (h + 10)))
    sheet.save('ahmed-emaar-holding_shop-sign_letters-on-wall-variants-sheet_ar-en_v03.png')
    print('letters photo corners', [tuple(round(c) for c in w2p(*p)) for p in [(0, Y_TOP), (LW, Y_TOP), (LW, Y_TOP + LH), (0, Y_TOP + LH)]])
