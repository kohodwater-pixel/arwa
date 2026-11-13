#!/usr/bin/env python3
"""Otlobny Emaar: identity capture.

1. Takes the wordmark paths from the back cover of the client's original profile
   (01-brief/assets-received/page20.svg, a pdftocairo export of page 20 of the PDF in _originals/)
   and writes them as standalone SVGs. Letterform coordinates are only translated, never redrawn.
2. Builds the PROPOSED name lockup: the same wordmark with a new descriptor line set in an
   open-licence font and converted to outlines (uharfbuzz + fontTools).

Run: python3 build_logo.py [--candidates]
"""
import math
import os
import re
import sys

import uharfbuzz as hb
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from pathops import Path, LineCap, LineJoin, difference, union

HERE = os.path.dirname(os.path.abspath(__file__))
IDENT = os.path.dirname(HERE)
CLIENT = os.path.dirname(IDENT)
REPO = os.path.abspath(os.path.join(CLIENT, "..", ".."))
SRC = os.path.join(CLIENT, "01-brief/assets-received/page20.svg")
OUT = os.path.join(IDENT, "02-logo")
FONTS_WORK = os.path.join(HERE, "fonts")
SLUG, VER = "otlobny-emaar", "v01"

BLUE, GREEN, NAVY, WHITE, GREY = "#3758B0", "#5AC584", "#1F3162", "#FFFFFF", "#525456"

AR_TEXT = "شركة اطلبني إعمار"
EN_TEXT = "OTLOBNY Emaar Co."


def fmt(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- source paths
def load_source():
    s = open(SRC, encoding="utf-8").read()
    body = s[s.index("</defs>"):]
    return re.findall(r"<path [^>]*/>", body)


def parse_d(d):
    """cairo output: absolute M L C Z only. Returns list of (cmd, [(x, y), ...])."""
    toks = re.findall(r"[MLCZ]|-?\d+\.?\d*(?:e-?\d+)?", d)
    assert not re.search(r"[^MLCZ\d\.\-e\s]", d), "unexpected path command"
    segs, i = [], 0
    while i < len(toks):
        c = toks[i]; i += 1
        n = {"M": 1, "L": 1, "C": 3, "Z": 0}[c]
        pts = [(float(toks[i + 2 * k]), float(toks[i + 2 * k + 1])) for k in range(n)]
        i += 2 * n
        segs.append((c, pts))
    # cairo repeats "M x y" after each Z; drop a trailing lone moveTo
    while segs and segs[-1][0] == "M":
        segs.pop()
    return segs


def circle(cx, cy, r):
    k = 0.5522847498 * r
    return [("M", [(cx, cy - r)]),
            ("C", [(cx + k, cy - r), (cx + r, cy - k), (cx + r, cy)]),
            ("C", [(cx + r, cy + k), (cx + k, cy + r), (cx, cy + r)]),
            ("C", [(cx - k, cy + r), (cx - r, cy + k), (cx - r, cy)]),
            ("C", [(cx - r, cy - k), (cx - k, cy - r), (cx, cy - r)]),
            ("Z", [])]


def to_d(segs, dx=0.0, dy=0.0):
    out = []
    for c, pts in segs:
        out.append(c + " ".join(f"{fmt(x + dx)} {fmt(y + dy)}" for x, y in pts))
    return " ".join(out)


def bbox(segs):
    xs, ys, cur = [], [], None
    for c, pts in segs:
        if c in "ML":
            cur = pts[0]; xs.append(cur[0]); ys.append(cur[1])
        elif c == "C":
            p0, p1, p2, p3 = cur, *pts
            for t in [i / 40 for i in range(41)]:
                a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; cc = 3 * (1 - t) * t * t; d = t ** 3
                xs.append(a * p0[0] + b * p1[0] + cc * p2[0] + d * p3[0])
                ys.append(a * p0[1] + b * p1[1] + cc * p2[1] + d * p3[1])
            cur = p3
        elif c == "Q":
            p0, p1, p2 = cur, *pts
            for t in [i / 40 for i in range(41)]:
                xs.append((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0])
                ys.append((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            cur = p2
    return min(xs), min(ys), max(xs), max(ys)


def union_bbox(list_of_segs):
    bs = [bbox(s) for s in list_of_segs]
    return min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)


def to_skia(segs):
    p = Path(); pen = p.getPen()
    for c, pts in segs:
        if c == "M": pen.moveTo(pts[0])
        elif c == "L": pen.lineTo(pts[0])
        elif c == "C": pen.curveTo(*pts)
        elif c == "Z": pen.closePath()
    return p


def from_skia(p):
    segs = []
    for verb, pts in p.segments:
        if verb == "moveTo": segs.append(("M", list(pts)))
        elif verb == "lineTo": segs.append(("L", list(pts)))
        elif verb == "curveTo": segs.append(("C", list(pts)))
        elif verb == "qCurveTo":
            # TrueType-style implied on-curve points: expand into single quads
            pts = list(pts)
            for k in range(len(pts) - 1):
                c1 = pts[k]
                if k < len(pts) - 2:
                    nx = pts[k + 1]; end = ((c1[0] + nx[0]) / 2, (c1[1] + nx[1]) / 2)
                else:
                    end = pts[-1]
                segs.append(("Q", [c1, end]))
        elif verb in ("closePath", "endPath"): segs.append(("Z", []))
    return segs


def get_parts():
    ps = load_source()
    d = lambda i: parse_d(re.search(r' d="([^"]*)"', ps[i]).group(1))
    # indices found by inspection of the page (see licences.md):
    # 0 page gradient, 1 old Arabic descriptor (outlined), 14 footer rule -> NOT used
    parts = {
        "alef": d(2), "tah_upright": d(3), "tah_body": d(4), "tah_block": d(5),
        "ya_dot": d(6), "lbny": d(7), "squeegee": d(12), "badge": d(13),
    }
    # dot: the source draws a filled circle (path 8) and then a 1-unit stroke on the same circle
    # through matrix(1.412566 0 0 -1.412566 394.538434 284.848264) (path 9; 10 and 11 are duplicates).
    m = re.search(r'matrix\(([^)]*)\)', ps[9]).group(1).split(",")
    sc, tx, ty = float(m[0]), float(m[4]), float(m[5])
    r = 6.603229 * sc
    cx, cy = tx, ty + r
    sw = 1.0 * sc
    assert abs(bbox(d(8))[0] - (cx - r)) < 0.02 and abs(bbox(d(8))[3] - (cy + r)) < 0.02
    parts["dot_ring"] = circle(cx, cy, r + sw / 2)   # outer edge of the stroke
    parts["dot"] = circle(cx, cy, r - sw / 2)        # fill left visible inside the stroke
    parts["_gap"] = sw
    return parts


# ---------------------------------------------------------------- colour schemes
def wordmark_layers(parts, scheme):
    """Returns [(fill, segs)], drawn bottom to top."""
    P = parts
    if scheme == "colour":      # as page 1 (front cover) of the original
        return [(BLUE, P["alef"]), (BLUE, P["tah_body"]), (GREEN, P["tah_upright"]), (GREEN, P["tah_block"]),
                (BLUE, P["ya_dot"]), (BLUE, P["lbny"]), (WHITE, P["dot_ring"]), (GREEN, P["dot"]),
                (GREEN, P["squeegee"]), (BLUE, P["badge"])]
    if scheme == "reversed":    # as page 20 (back cover) of the original
        # tah_body and tah_block touch along one edge and share a colour here: merged into one path so that
        # no anti-aliasing seam shows between them (outline unchanged)
        tah = Path(); union([to_skia(P["tah_body"]), to_skia(P["tah_block"])], tah.getPen())
        g = [P["alef"], P["tah_upright"], from_skia(tah), P["ya_dot"], P["lbny"]]
        return [(GREEN, s) for s in g] + [(GREEN, P["dot_ring"]), (WHITE, P["dot"]),
                                           (WHITE, P["squeegee"]), (GREEN, P["badge"])]
    # one colour: derived by the agency (no one-colour version exists in the originals).
    col = {"white": WHITE, "navy": NAVY}[scheme]
    gap = P["_gap"]
    sq = to_skia(P["squeegee"])
    halo = to_skia(P["squeegee"]); halo.stroke(2 * gap, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, 4)
    halo.convertConicsToQuads(0.01)
    sq_halo = Path(); union([sq, halo], sq_halo.getPen())
    ring = to_skia(P["dot_ring"])
    cutter = Path(); union([sq_halo, ring], cutter.getPen())
    body = Path()
    union([to_skia(P[k]) for k in ("alef", "tah_upright", "tah_body", "tah_block", "lbny")], body.getPen())
    cut = Path(); difference([body], [cutter], cut.getPen())
    return [(col, from_skia(cut)), (col, P["ya_dot"]), (col, P["dot"]), (col, P["squeegee"]), (col, P["badge"])]


# ---------------------------------------------------------------- text to outlines
def cairo_static(wght):
    os.makedirs(FONTS_WORK, exist_ok=True)
    p = os.path.join(FONTS_WORK, f"Cairo-wght{wght}.ttf")
    if not os.path.exists(p):
        f = TTFont(os.path.join(REPO, "assets/fonts/cairo/Cairo[slnt,wght].ttf"))
        f = instancer.instantiateVariableFont(f, {"wght": wght, "slnt": 0})
        f.save(p)
    return p


def text_segs(fontpath, text, tracking=0.0):
    """Shape with HarfBuzz, return outline segments in font units (y up), starting at x=0, and advance."""
    font = TTFont(fontpath); gs = font.getGlyphSet()
    hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(fontpath)))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf)
    segs, x = [], 0.0
    n = len(buf.glyph_infos)
    for k, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = hbfont.glyph_to_string(info.codepoint)
        rec = DecomposingRecordingPen(gs); gs[name].draw(rec)
        ox, oy = x + pos.x_offset, pos.y_offset
        cur_start = None
        for verb, pts in rec.value:
            pts = [(px + ox, py + oy) for px, py in pts]
            if verb == "moveTo": segs.append(("M", pts))
            elif verb == "lineTo": segs.append(("L", pts))
            elif verb == "curveTo": segs.append(("C", pts))
            elif verb == "qCurveTo":
                for j in range(len(pts) - 1):
                    c1 = pts[j]
                    end = ((c1[0] + pts[j + 1][0]) / 2, (c1[1] + pts[j + 1][1]) / 2) if j < len(pts) - 2 else pts[-1]
                    segs.append(("Q", [c1, end]))
            elif verb in ("closePath", "endPath"): segs.append(("Z", []))
        x += pos.x_advance + (tracking if k < n - 1 else 0)
    return segs, x, font


def xform(segs, s, tx, ty):
    """font units (y up) -> page units (y down)"""
    return [(c, [(px * s + tx, -py * s + ty) for px, py in pts]) for c, pts in segs]


def to_d_any(segs, dx=0.0, dy=0.0):
    return " ".join(c + " ".join(f"{fmt(x + dx)} {fmt(y + dy)}" for x, y in pts) for c, pts in segs)


def descriptor(ar_font, la_font, right_x, ar_base, la_base, ar_h, cap_h, la_track_em=None):
    """Arabic line: alef height = ar_h. Latin line: cap height = cap_h, tracked so both lines share a width.
    Both right-aligned to right_x (the right edge of the wordmark's alef)."""
    a, _, _ = text_segs(ar_font, AR_TEXT)
    alef, _, _ = text_segs(ar_font, "ا")
    ab = bbox(alef); s_ar = ar_h / (ab[3] - ab[1])
    abx = bbox(a)
    ar = xform(a, s_ar, right_x - abx[2] * s_ar, ar_base)
    ar_w = (abx[2] - abx[0]) * s_ar

    capH, _, _ = text_segs(la_font, "H")
    hbx = bbox(capH); s_la = cap_h / (hbx[3] - hbx[1])
    l0, _, _ = text_segs(la_font, EN_TEXT)
    w0 = (bbox(l0)[2] - bbox(l0)[0]) * s_la
    n_gaps = len(EN_TEXT) - 1
    track = (ar_w - w0) / n_gaps / s_la if la_track_em is None else la_track_em * 1000  # font units
    l1, _, _ = text_segs(la_font, EN_TEXT, tracking=track)
    lb = bbox(l1)
    # the open-licence fonts carry the dots of the final ya lower than the original descriptor face did,
    # so the Latin line is dropped until its cap top clears the lowest Arabic point by LINE_GAP
    la_base = max(la_base, bbox(ar)[3] + LINE_GAP + cap_h)
    la = xform(l1, s_la, right_x - lb[2] * s_la, la_base)
    info = dict(la_base=la_base, ar_bottom=bbox(ar)[3], ar_left=bbox(ar)[0], ar_right=bbox(ar)[2], la_left=bbox(la)[0], la_right=bbox(la)[2], la_bottom=bbox(la)[3], ar_scale=s_ar, la_scale=s_la, ar_width=ar_w, la_natural_width=w0,
                la_tracking_em=track / 1000.0, ar_pt_equiv=s_ar * 1000, la_pt_equiv=s_la * 1000)
    return ar, la, info


# ---------------------------------------------------------------- output
def svg_doc(layers, title, pad=0.0, extra_bbox=None):
    b = union_bbox([s for _, s in layers] + (extra_bbox or []))
    dx, dy = -b[0] + pad, -b[1] + pad
    w, h = b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad
    body = "\n".join(f'  <path fill="{f}" d="{to_d_any(s, dx, dy)}"/>' for f, s in layers)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" role="img" aria-label="{title}">\n  <title>{title}</title>\n{body}\n</svg>\n'), (w, h)


FONT_CHOICES = {
    "tajawal-medium": os.path.join(REPO, "assets/fonts/tajawal/Tajawal-Medium.ttf"),
    "tajawal-bold": os.path.join(REPO, "assets/fonts/tajawal/Tajawal-Bold.ttf"),
    "cairo-500": None, "cairo-600": None,
}
# geometry of the old descriptor on page 20, reused for the new one
RIGHT_X, AR_BASE, LA_BASE, AR_H, CAP_H = 574.55, 319.105, 333.195, 10.54, 7.84
LINE_GAP = 2.6


def font_path(key):
    if key.startswith("cairo"):
        return cairo_static(int(key.split("-")[1]))
    return FONT_CHOICES[key]


def build(chosen="tajawal-bold", candidates=False):
    parts = get_parts()
    os.makedirs(OUT, exist_ok=True)
    report = {}
    if candidates:
        cdir = os.path.join(OUT, "_work", "candidates"); os.makedirs(cdir, exist_ok=True)
        for key in FONT_CHOICES:
            fp = font_path(key)
            ar, la, info = descriptor(fp, fp, RIGHT_X, AR_BASE, LA_BASE, AR_H, CAP_H)
            layers = wordmark_layers(parts, "colour") + [(GREY, ar), (GREY, la)]
            doc, _ = svg_doc(layers, key)
            open(os.path.join(cdir, f"candidate_{key}.svg"), "w", encoding="utf-8").write(doc)
            print(key, {k: round(v, 3) for k, v in info.items()})
        return
    # ---- wordmark, four versions
    for scheme in ("colour", "reversed", "white", "navy"):
        doc, wh = svg_doc(wordmark_layers(parts, scheme), "اطلبني")
        fn = f"{SLUG}_logo_wordmark-{scheme}_ar_{VER}.svg"
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(doc)
        report[fn] = wh
    # ---- proposed lockup, four versions
    fp = font_path(chosen)
    ar, la, info = descriptor(fp, fp, RIGHT_X, AR_BASE, LA_BASE, AR_H, CAP_H)
    desc_col = {"colour": GREY, "reversed": GREEN, "white": WHITE, "navy": NAVY}
    for scheme in ("colour", "reversed", "white", "navy"):
        layers = wordmark_layers(parts, scheme) + [(desc_col[scheme], ar), (desc_col[scheme], la)]
        doc, wh = svg_doc(layers, "اطلبني — شركة اطلبني إعمار — OTLOBNY Emaar Co. (PROPOSAL)")
        fn = f"{SLUG}_logo_lockup-proposal-{scheme}_ar-en_{VER}.svg"
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(doc)
        report[fn] = wh
    print("descriptor:", chosen, {k: round(v, 3) for k, v in info.items()})
    wb = union_bbox([s for k, s in parts.items() if k != "_gap"])
    print("wordmark bbox in source page units:", [round(v, 2) for v in wb])
    print("alef:", [round(v, 2) for v in bbox(parts["alef"])], "dot gap:", round(parts["_gap"], 3))
    for k, v in report.items():
        print(k, round(v[0], 2), "x", round(v[1], 2))


if __name__ == "__main__":
    build(candidates="--candidates" in sys.argv)
