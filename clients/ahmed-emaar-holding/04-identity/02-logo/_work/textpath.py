"""Shape text with HarfBuzz and return it as outlined SVG path data (y down).

Used to outline the Arabic and Latin lettering of the provisional logo and the
shop sign so the delivered SVG/PDF contain no live text.
"""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

_cache = {}


def _load(path, var):
    key = (path, tuple(sorted((var or {}).items())))
    if key not in _cache:
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        font = hb.Font(face)
        if var:
            font.set_variations(var)
        tt = TTFont(path)
        gs = tt.getGlyphSet(location=var) if var else tt.getGlyphSet()
        _cache[key] = (font, tt, gs)
    return _cache[key]


def shape(path, text, size, var=None, tracking=0.0, features=None):
    """Return (d, advance_width, bounds) for text at `size` px, origin at
    baseline-left, y down. tracking in em (Latin only)."""
    font, tt, gs = _load(path, var)
    upem = tt["head"].unitsPerEm
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    order = tt.getGlyphOrder()
    s = size / upem
    pen = SVGPathPen(gs)
    bpen = BoundsPen(gs)
    x = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = order[info.codepoint]
        gx = x + pos.x_offset
        gy = pos.y_offset
        t = (s, 0, 0, -s, gx * s, -gy * s)
        gs[name].draw(TransformPen(pen, t))
        gs[name].draw(TransformPen(bpen, t))
        x += pos.x_advance
        if tracking and i < n - 1:
            x += tracking * upem
    return pen.getCommands(), x * s, bpen.bounds


def translate_d(d, dx, dy):
    """Wrap path data in a transform-free form by returning a <path> with transform."""
    return d, dx, dy
