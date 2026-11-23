"""Photomontage of the sign on the client's site photo (visualisation only).
The photo is not retouched: the warped sign is composited on top and a caption
strip is added OUTSIDE the photo (canvas extended below)."""
import sys, io, json
import numpy as np
import cairosvg
from PIL import Image, ImageFilter, ImageChops
sys.path.insert(0, '.')
import build_sign as bs
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


def build(opt, body, acc, out_path):
    W, H = int(bs.W * PPC), int(bs.H * PPC)
    panel = render(bs.svg(body, acc, 'panel'), W, H)
    letters = render(bs.svg(body, acc, 'letters'), W, H)
    la = letters.split()[3]
    # panel: navy with a soft daylight gradient (lighter at the top)
    yy = np.linspace(1.18, 0.92, H)[:, None]
    pn = np.asarray(panel).astype(float)
    pn[..., :3] = np.clip(pn[..., :3] * yy[..., None], 0, 255)
    flat = Image.fromarray(pn.astype('uint8'), 'RGBA')
    # cast shadow of the raised letters on the panel (sun high, slightly left)
    sh = la.transform(la.size, Image.AFFINE, (1, 0, -3, 0, 1, -9)).filter(ImageFilter.GaussianBlur(5))
    flat.paste((5, 12, 22, 255), None, sh.point(lambda v: int(v * 0.55)))
    # extrusion (letter returns, seen from below): stacked darker gold copies
    depth = 7
    for i in range(depth, 0, -1):
        m = la.transform(la.size, Image.AFFINE, (1, 0, 0, 0, 1, -i))
        flat.paste((128, 92, 40, 255), None, m)
    # letter faces: brushed metallic gold gradient
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
    # caption strip outside the photo
    cap_h = 150
    canvas = Image.new('RGB', (photo.width, photo.height + cap_h), (255, 255, 255))
    canvas.paste(comp.convert('RGB'), (0, 0))
    canvas.paste(caption(opt, photo.width, cap_h), (0, photo.height))
    canvas.save(out_path)
    return canvas


def caption(opt, w, h):
    F = bs.F
    ar_font = (F + 'ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf', None)
    la_font = (F + 'ibmplexsans-static/IBMPlexSans-Regular.ttf', None)
    l1 = f'تصوّر توضيحي فقط — الخيار {"أ" if opt == "a" else "ب"} على صورة الموقع، ليس صورة للوحة مركّبة'
    l2 = ('VISUALISATION ONLY - option ' + opt.upper() + ' montaged on the client site photo. '
          'Sign 250 x 60 cm assumed; height and position to be measured on site.')
    l3 = ('Logo = provisional trace. Slab-edge cracks behind the sign must be inspected and repaired before installation.')
    els = []
    d, _, b = shape(ar_font[0], l1, 100, None); s = 30 / 100
    els.append(f'<path transform="translate({w - 30 - b[2]*s:.1f},48) scale({s})" d="{d}" fill="#102232"/>')
    for i, t in enumerate((l2, l3)):
        d, _, b = shape(la_font[0], t, 100, None); s = 21 / 100
        els.append(f'<path transform="translate(30,{92 + i*32}) scale({s})" d="{d}" fill="#333"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#fff"/>{"".join(els)}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')


if __name__ == '__main__':
    out = sys.argv[1]
    for opt, fn in (('a', bs.option_a), ('b', bs.option_b)):
        body, acc, info = fn()
        c = build(opt, body, acc, f'{out}/ahmed-emaar-holding_shop-sign_option-{opt}_mockup-site_ar-en_v01.png')
        c.crop((150, 230, 1250, 700)).save(f'mock_detail_{opt}.png')
    print('quad', [tuple(round(v, 1) for v in p) for p in QUAD])
