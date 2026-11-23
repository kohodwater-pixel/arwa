"""Boolean welding helpers (skia-pathops): every element becomes one compound
outline with no overlapping contours, so nonzero and evenodd fill are identical
and a cutter/router sees no internal seams."""
import pathops
from fontTools.svgLib.path import parse_path
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.svgPathPen import SVGPathPen
import uharfbuzz as hb
from textpath import _load


def from_d(d, transform=(1, 0, 0, 1, 0, 0)):
    p = pathops.Path()
    parse_path(d, TransformPen(p.getPen(), transform))
    p.simplify(fix_winding=True)
    return p


def union(paths):
    """Union by drawing every (individually winding-fixed) part into one path
    and simplifying once. (Pairwise pathops.op dropped a glyph in testing.)"""
    out = pathops.Path()
    for p in paths:
        q = pathops.Path(); p.draw(q.getPen()); q.simplify(fix_winding=True)
        q.draw(out.getPen())
    out.simplify(fix_winding=True)
    return out


def intersect(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION, fix_winding=True)


def rect(x, y, w, h):
    return from_d(f'M{x},{y} L{x + w},{y} L{x + w},{y + h} L{x},{y + h} Z')


def band(x1, y1, x2, y2, width):
    """A straight line of given width expanded to a filled polygon."""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * width / 2, dx / L * width / 2
    return from_d(f'M{x1 + nx},{y1 + ny} L{x2 + nx},{y2 + ny} L{x2 - nx},{y2 - ny} L{x1 - nx},{y1 - ny} Z')


def to_d(p):
    pen = SVGPathPen(None, ntos=lambda v: f'{v:.3f}'.rstrip('0').rstrip('.'))
    p.draw(pen)
    return pen.getCommands()


def text_glyph_paths(font_path, text, size, var=None, tracking=0.0):
    """Glyph outlines as individually-simplified pathops Paths, origin at
    baseline-left, y down, in units of `size`."""
    font, tt, gs = _load(font_path, var)
    upem = tt['head'].unitsPerEm
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    order = tt.getGlyphOrder(); s = size / upem
    x = 0.0; out = []
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        p = pathops.Path()
        gs[order[info.codepoint]].draw(TransformPen(p.getPen(glyphSet=gs), (s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s)))
        p.simplify(fix_winding=True)
        out.append(p)
        x += pos.x_advance + (tracking * upem if tracking and i < n - 1 else 0)
    return out


def _raster(paths, bounds, px=1600):
    import cairosvg, io, numpy as np
    from PIL import Image
    x0, y0, x1, y1 = bounds
    pad = (x1 - x0) * 0.01
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    body = ''.join(f'<path d="{to_d(p)}"/>' for p in paths)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{int(px * h / w) + 1}" '
           f'viewBox="{x0 - pad} {y0 - pad} {w} {h}"><rect x="{x0-pad}" y="{y0-pad}" width="{w}" height="{h}" fill="white"/>'
           f'<g fill="black" fill-rule="nonzero">{body}</g></svg>')
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('L')).astype(int)


def verified_union(parts):
    """Union, then prove it: rasterise the welded result and the raw
    overlapping parts and require they match. Tries several numeric scales
    and two algorithms because Skia's simplify occasionally drops contours."""
    import numpy as np
    raw_b = union_bounds(parts)
    ref = _raster(parts, raw_b)
    attempts = []
    for scale in (1.0, 0.1, 10.0, 0.37, 3.3):
        for algo in ('combined', 'pairwise'):
            try:
                sp = [xform(p, (scale, 0, 0, scale, 0, 0)) for p in parts]
                if algo == 'combined':
                    u = union(sp)
                else:
                    u = pathops.Path()
                    for p in sp:
                        u = pathops.op(u, p, pathops.PathOp.UNION, fix_winding=True)
                u = xform(u, (1 / scale, 0, 0, 1 / scale, 0, 0))
                diff = int((np.abs(_raster([u], raw_b) - ref) > 64).sum())
                attempts.append((scale, algo, diff))
                if diff == 0:
                    return u
            except Exception as e:
                attempts.append((scale, algo, str(e)[:40]))
    raise RuntimeError(f'no verified union: {attempts}')


def union_bounds(parts):
    bs = [p.bounds for p in parts if len(list(p.contours))]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def text_line(font_path, text, size, var=None, tracking=0.0):
    parts = [p for p in text_glyph_paths(font_path, text, size, var, tracking) if len(list(p.contours))]
    return verified_union(parts)


def moved(p, dx, dy):
    out = pathops.Path()
    p.draw(TransformPen(out.getPen(), (1, 0, 0, 1, dx, dy)))
    return out


def xform(p, t):
    out = pathops.Path()
    p.draw(TransformPen(out.getPen(), t))
    return out


def mark_path():
    from mark import mark_paths
    return verified_union([from_d(d) for d in mark_paths()])
