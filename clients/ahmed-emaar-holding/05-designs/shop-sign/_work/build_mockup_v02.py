"""v02 photomontage of the sign on the client's site photo (visualisation only).
The photo is not retouched: the warped sign is composited on top and a caption
strip is added OUTSIDE the photo (canvas extended below)."""
import sys, io, json
import numpy as np
import cairosvg
from PIL import Image, ImageFilter, ImageChops
sys.path.insert(0, '.')
import build_sign_v02 as bs
import subprocess, os
sys.path.insert(0, bs.LOGO_WORK)
from textpath import shape

PHOTO = '/home/user/arwa/clients/ahmed-emaar-holding/_originals/ahmed-emaar-holding_shopfront-photo_site.jpg'
PPC = 12  # flat render px per cm

# Sign quad on the slab front face (photo px, original 1512x2016).
# Bottom edge = front arris of the slab soffit (measured: y = 543 at x 260, 478 at x 1100).
# Height = 2 x measured slab-edge face height (~80 px) = 60 cm under the assumption the
# face is ~30 cm; width 250 cm centred between the two column stubs.
def arris(x): return 543 - 0.0774 * (x - 260)
XL, XR = 303, 1053
BL, BR = (XL, arris(XL)), (XR, arris(XR))
TL = (XL + 6, BL[1] - 158)
TR = (XR, TL[1] - 0.09 * (XR - TL[0]))
QUAD = [TL, TR, BR, BL]


def coeffs(dst, src):
    """PIL PERSPECTIVE coefficients mapping output (dst) to input (src)."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def render(svg_text, w, h):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=w, output_height=h))).convert('RGBA')


def build(opt, out_path):
    W, H = int(bs.W * PPC), int(bs.H * PPC)
    channel = render(open(f'v02_option-{opt}_channel.svg').read(), W, H).split()[3]
    flat_l = render(open(f'v02_option-{opt}_flat.svg').read(), W, H).split()[3]
    la = ImageChops.lighter(channel, flat_l)
    panel = render(open(f'v02_option-{opt}_panel.svg').read(), W, H)
    yy = np.linspace(1.18, 0.92, H)[:, None]
    pn = np.asarray(panel).astype(float)
    pn[..., :3] = np.clip(pn[..., :3] * yy[..., None], 0, 255)
    flat = Image.fromarray(pn.astype('uint8'), 'RGBA')
    # cast shadows: deeper for channel letters (6 cm) than flat-cut (1 cm)
    for m, off, blur, k in ((channel, 9, 5, 0.55), (flat_l, 3, 2, 0.45)):
        sh = m.transform(m.size, Image.AFFINE, (1, 0, -3, 0, 1, -off)).filter(ImageFilter.GaussianBlur(blur))
        flat.paste((5, 12, 22, 255), None, sh.point(lambda v, k=k: int(v * k)))
    for m, depth in ((channel, 7), (flat_l, 2)):
        for i in range(depth, 0, -1):
            flat.paste((128, 92, 40, 255), None, m.transform(m.size, Image.AFFINE, (1, 0, 0, 0, 1, -i)))
    g = np.zeros((H, W, 4), 'uint8')
    t = np.linspace(0, 1, H)[:, None]
    base = np.array([238, 205, 140]) * (1 - t[..., None]) + np.array([196, 150, 78]) * t[..., None]
    streak = (np.sin(np.linspace(0, 40, W))[None, :, None] * 6)
    g[..., :3] = np.clip(base + streak, 0, 255).astype('uint8'); g[..., 3] = 255
    flat.paste(Image.fromarray(g, 'RGBA'), (0, 0), la)
    # panel underside return (3 cm, seen from below)
    ret = int(3 * PPC)
    full = Image.new('RGBA', (W, H + ret), (0, 0, 0, 0))
    full.paste(flat, (0, 0))
    full.paste((8, 18, 30, 255), (0, H, W, H + ret))
    # warp to photo
    photo = Image.open(PHOTO).convert('RGBA')
    quad_ret = [QUAD[0], QUAD[1], (BR[0], BR[1] + 7), (BL[0], BL[1] + 7)]
    src = [(0, 0), (W, 0), (W, H + ret), (0, H + ret)]
    warped = full.transform(photo.size, Image.PERSPECTIVE, coeffs(quad_ret, src), Image.BICUBIC)
    # soft contact shadow of the panel on the wall/soffit (slight, down-right)
    a = warped.split()[3]
    shadow = a.transform(a.size, Image.AFFINE, (1, 0, -5, 0, 1, -6)).filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.45))
    comp = photo.copy()
    comp.paste((20, 18, 15, 255), None, shadow)
    comp.alpha_composite(warped)
    # caption strip outside the photo (photo pixels untouched apart from the sign)
    cap = caption(opt, photo.width)
    canvas = Image.new('RGB', (photo.width, photo.height + cap.height), (255, 255, 255))
    canvas.paste(comp.convert('RGB'), (0, 0))
    canvas.paste(cap, (0, photo.height))
    canvas.save(out_path)
    return canvas


def caption(opt, w, h=None):
    L = 'أ' if opt == 'a' else 'ب'
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:A;src:url("file://{bs.F}ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:A;src:url("file://{bs.F}ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}
body{{margin:0;padding:22px 30px 24px;font-family:A;background:#fff;color:#222;font-size:21px;line-height:1.75}}
.ar{{direction:rtl;text-align:right}} .en{{direction:ltr;text-align:left;margin-top:12px;font-size:19px;line-height:1.5;color:#333}}
b{{font-weight:600;color:#102232}} ul{{margin:0;padding:0 1.2em 0 0}} .en ul{{padding:0 0 0 1.2em}}</style></head><body>
<div class="ar"><b>تصوّر توضيحي فقط — الخيار {L} على صورة موقع العميل، وليس صورة للوحة مركّبة.</b><ul>
<li>مقاس اللوحة 250 × 60 سم مفترض؛ يُحدَّد الارتفاع والموضع بالقياس في الموقع.</li>
<li>الشعار إعادة رسم مؤقتة بانتظار الملف الأصلي من العميل.</li>
<li>يُشترط فحص حافة السقف وترميمها قبل التركيب؛ التشققات والحديد المكشوف خلف اللوحة غير ظاهرة في هذا التصوّر.</li></ul></div>
<div class="en"><b>VISUALISATION ONLY — option {opt.upper()} montaged on the client's site photo; not a photo of an installed sign.</b><ul>
<li>250 × 60 cm is assumed; height and position to be measured on site.</li>
<li>The logo is a provisional trace pending the client's original file.</li>
<li>The slab edge must be inspected and repaired before installation; cracks and exposed rebar behind the sign are hidden in this visualisation.</li></ul></div>
</body></html>"""
    open(f'v02_caption-{opt}.html', 'w').write(html)
    subprocess.run(['node', 'shot.cjs', f'v02_caption-{opt}.html', f'v02_caption-{opt}.png', str(w)], check=True)
    return Image.open(f'v02_caption-{opt}.png').convert('RGB')


if __name__ == '__main__':
    out = sys.argv[1]
    for opt in 'ab':
        c = build(opt, f'{out}/ahmed-emaar-holding_shop-sign_option-{opt}-mockup-site_ar-en_v02.png')
        c.crop((150, 230, 1250, 700)).save(f'v02_mock_detail_{opt}.png')
    print('quad', [tuple(round(v, 1) for v in p) for p in QUAD])
