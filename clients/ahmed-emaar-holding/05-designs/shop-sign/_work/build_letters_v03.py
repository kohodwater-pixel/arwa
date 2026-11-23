"""v03 - individual raised letters fixed directly on the wall (no panel).
Content = option A (mark + Arabic name + English name). Overall lettering
width 250 cm (mark included). Every element is one welded outline; the
artboard is the lettering's bounding box, written at 1:10.

Fabrication adjustments vs the logo trace (stated in the drawing):
- English line in Inter ExtraBold (800) so every stroke is >= 1.5 cm.
- Swoosh tip of the mark blunted where it gets thinner than ~1.5 cm.
"""
import sys, json, math
import build_sign_v02 as bs
import weld
from textpath import shape
import pathops

TARGET_W = 250.0
bs.LATIN = (bs.F + 'inter/Inter[opsz,wght].ttf', {'wght': 800, 'opsz': 32})
CAP = 8.5               # English cap height, cm (bar >= 1.5 cm at Inter 800)
SWOOSH_CUT_PX = 151.6   # board px: blunt the swoosh tip left of this x


_ORIG_MARK = weld.mark_path
_MARK_CACHE = []


def blunted_mark_path():
    if _MARK_CACHE:
        return _MARK_CACHE[0]
    m = _ORIG_MARK()
    keep = weld.rect(SWOOSH_CUT_PX, 0, 400, 400)
    r = weld.intersect(m, keep)
    _MARK_CACHE.append(r)
    return r


def build(mark_h):
    # patch the mark used by lockup(): blunted, bbox unchanged on the right/top/bottom
    x0, y0, x1, y1 = bs.BBOX
    orig = weld.mark_path
    weld.mark_path = blunted_mark_path
    try:
        els, info = bs.lockup(0, 0, mark_h, mark_h * 7.5 / 38, CAP)
    finally:
        weld.mark_path = orig
    return els, info


def solve():
    lo, hi = 30.0, 60.0
    for _ in range(30):
        m = (lo + hi) / 2
        els, info = build(m)
        w = info['pos']['x_right'] - info['pos']['left']
        (lo, hi) = (m, hi) if w < TARGET_W else (lo, m)
    return build((lo + hi) / 2)


def contour_parts(p):
    """Separate solid pieces (outer contours with their holes) of a welded path."""
    outs = []
    for c in p.contours:
        q = pathops.Path(); c.draw(q.getPen())
        outs.append(q)
    # classify: outer contours are those not inside another contour
    pieces = []
    for i, q in enumerate(outs):
        b = q.bounds
        inside = any(j != i and o.bounds[0] <= b[0] and o.bounds[1] <= b[1] and o.bounds[2] >= b[2] and o.bounds[3] >= b[3]
                     and (o.bounds != b) for j, o in enumerate(outs))
        if not inside:
            pieces.append(b)
    return pieces


if __name__ == '__main__':
    els, info = solve()
    # shift so the bounding box starts at 0,0
    allb = weld.union_bounds([els[n] for n in ('mark', 'name-ar', 'name-en')])
    dx, dy = -allb[0], -allb[1]
    for n in list(els):
        els[n] = weld.moved(els[n], dx, dy)
    W, H = allb[2] - allb[0], allb[3] - allb[1]
    p = info['pos']
    for k in p: p[k] += dx if k in ('x_right', 'mark_left', 'left', 'text_right') else dy
    # Arabic letter-body height (bowl/tooth height, = 'ه' height) for the legibility rule
    ar_size = info['name_ar']['alef_h'] / (70.6697 / 100)
    _, _, hb = shape(bs.AR_BOLD[0], 'ه', 100, bs.AR_BOLD[1])
    body = -hb[1] * ar_size / 100
    # small isolated pieces of the Arabic line (hamzas, dots)
    pieces = contour_parts(els['name-ar'])
    small = sorted([b for b in pieces if (b[2] - b[0]) * (b[3] - b[1]) < 40], key=lambda b: -b[0])
    # swoosh cut edge (vertical extent at the cut) and its perpendicular thickness
    k = info['mark']['h'] / (bs.BBOX[3] - bs.BBOX[1])
    info.update({'overall_w': W, 'overall_h': H, 'arabic_body_h': body,
                 'gap_ar_bottom_to_en_top': p['lat_top'] - p['ar_bottom'],
                 'gap_ar_base_to_en_top': p['lat_top'] - p['ar_base'],
                 'small_pieces': [{'x': (b[0] + b[2]) / 2, 'y': (b[1] + b[3]) / 2, 'w': b[2] - b[0], 'h': b[3] - b[1]} for b in small],
                 'n_pieces_ar': len(pieces), 'n_pieces_en': len(contour_parts(els['name-en'])),
                 'n_pieces_mark': len(contour_parts(els['mark'])), 'mark_k_cm_per_px': k})
    _, _, hi = shape(bs.LATIN[0], 'I', 100, bs.LATIN[1]); _, _, hh = shape(bs.LATIN[0], 'H', 100, bs.LATIN[1]); _, _, hd = shape(bs.LATIN[0], '-', 100, bs.LATIN[1])
    cap = hh[3] - hh[1]
    info['name_en'].update({'stem': CAP * (hi[2] - hi[0]) / cap, 'bar': CAP * (hd[3] - hd[1]) / cap, 'weight': 800})
    title = ('Ahmed Emaar Holding - letters on wall v03 - cut-file artwork at 1:10 (1 mm = 1 cm real), overall '
             f'{W:.1f} x {H:.1f} cm, RGB, not print-ready. Logo PROVISIONAL trace (swoosh tip blunted for fabrication); '
             'lettering typeface match (Cairo 700 / Inter 800). One welded outline per element; no live text.')
    def svg(fill_rule='nonzero', only=None, colours=None):
        colours = colours or {}
        body_ = ''.join(f'<path id="{n}" fill="{colours.get(n, bs.GOLD)}" fill-rule="{fill_rule}" d="{weld.to_d(els[n])}"/>'
                        for n in ('mark', 'name-ar', 'name-en') if only is None or n in only)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {W:.3f} {H:.3f}">'
                f'<title>{title}</title>{body_}</svg>')
    open('v03_letters_full.svg', 'w').write(svg())
    for r in ('nonzero', 'evenodd'):
        open(f'v03_letters_fill-{r}.svg', 'w').write(svg(r))
    for n in ('mark', 'name-ar', 'name-en'):
        open(f'v03_letters_{n}.svg', 'w').write(svg(only=[n]))
    open('v03_title.txt', 'w').write(title)
    json.dump(bs.r1(info), open('metrics_v03.json', 'w'), indent=1, ensure_ascii=False)
    out = bs.r1({k: v for k, v in info.items() if k != 'pos'})
    print(json.dumps(out, indent=1, ensure_ascii=False))
