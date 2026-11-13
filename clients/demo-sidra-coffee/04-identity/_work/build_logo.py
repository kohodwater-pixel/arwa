#!/usr/bin/env python3
"""Build the Sidra Coffee logo set as outlined SVG (no font dependency).

Shaping: uharfbuzz. Outlines: fontTools. Source fonts: IBM Plex Sans Arabic Bold
(static) and IBM Plex Sans SemiBold (instance cut from the variable font).
Run: python3 build_logo.py
"""
import json
import os
import sys

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
IDENT = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(IDENT, "..", "..", ".."))
OUT = os.path.join(IDENT, "02-logo")
FONTS_WORK = os.path.join(HERE, "fonts")
AR_BOLD = os.path.join(REPO, "assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf")
LAT_VAR = os.path.join(REPO, "assets/fonts/ibmplexsans/IBMPlexSans[wdth,wght].ttf")
SLUG = "demo-sidra-coffee"
VER = "v01"

PAPER, CREMA, INK, EMBER, ASH = "#F3ECE0", "#E3C9A0", "#1F1B18", "#C23A20", "#6F6861"
S = 0.1  # font units -> SVG units


def static_latin():
    """Cut static instances from the variable Latin font (work files only)."""
    os.makedirs(FONTS_WORK, exist_ok=True)
    made = {}
    for name, wght, wdth in [("Light", 300, 100), ("Regular", 400, 100), ("Medium", 500, 100),
                             ("SemiBold", 600, 100), ("Bold", 700, 100), ("LightCondensed", 300, 85)]:
        p = os.path.join(FONTS_WORK, f"IBMPlexSans-{name}.ttf")
        if not os.path.exists(p):
            f = TTFont(LAT_VAR)
            try:
                f = instancer.instantiateVariableFont(f, {"wght": wght, "wdth": wdth}, updateFontNames=True)
            except Exception:
                f = TTFont(LAT_VAR)
                f = instancer.instantiateVariableFont(f, {"wght": wght, "wdth": wdth})
            f.save(p)
        made[name] = p
    return made


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


class Run:
    """A shaped, outlined run of text. y is down, baseline at y=0, starts at x=0."""

    def __init__(self, fontpath, text, size_scale=S, tracking=0.0, kern_after=None):
        self.font = TTFont(fontpath)
        self.gs = self.font.getGlyphSet()
        face = hb.Face(hb.Blob.from_file_path(fontpath))
        hbfont = hb.Font(face)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hbfont, buf)
        self.scale = size_scale
        self.glyphs = []  # (name, cluster, x, y) in font units, visual order
        x = 0.0
        n = len(buf.glyph_infos)
        for k, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            name = hbfont.glyph_to_string(info.codepoint)
            self.glyphs.append((name, info.cluster, x + pos.x_offset, pos.y_offset))
            x += pos.x_advance
            if k < n - 1:
                x += tracking
                if kern_after and info.cluster in kern_after:
                    x += kern_after[info.cluster]
        self.advance = x * size_scale
        self.bounds = self._bounds()

    def _draw(self, pen, ox=0.0, oy=0.0, only_cluster=None):
        s = self.scale
        for name, cluster, gx, gy in self.glyphs:
            if only_cluster is not None and cluster != only_cluster:
                continue
            t = TransformPen(pen, (s, 0, 0, -s, ox + gx * s, oy - gy * s))
            self.gs[name].draw(t)

    def _bounds(self, only_cluster=None):
        rec = DecomposingRecordingPen(self.gs)
        self._draw(rec, only_cluster=only_cluster)
        bp = BoundsPen(None)
        rec.replay(bp)
        return bp.bounds  # xmin, ymin, xmax, ymax (y down)

    def cluster_bounds(self, cluster):
        return self._bounds(only_cluster=cluster)

    def path(self, ox, oy):
        pen = SVGPathPen(self.gs, ntos=fmt)
        self._draw(pen, ox, oy)
        return pen.getCommands()


SCHEMES = {
    # name: (wordmark, bars, lit bar)
    "colour": (INK, INK, EMBER),             # on Paper and Crema
    "colour-reversed": (PAPER, PAPER, EMBER),  # on Ink
    "colour-on-ember": (PAPER, INK, PAPER),    # on Ember (Ink band, Paper lit bar)
    "black": ("#000000", "#000000", "#000000"),
    "white": ("#FFFFFF", "#FFFFFF", "#FFFFFF"),
}


def bar_row(x0, y0, width, ratio_h, scheme, solid=False):
    """Seven bars across `width`; gap = 1/5 bar width; bar height = ratio_h * bar width.
    solid=True is the small-size fallback: one rule with the centre seventh lit."""
    _, cbar, clit = SCHEMES[scheme]
    w = width / 8.2
    h = w * ratio_h
    out = []
    if solid:
        seg = width / 7.0
        out.append(f'<rect x="{fmt(x0)}" y="{fmt(y0)}" width="{fmt(width)}" height="{fmt(h)}" fill="{cbar}"/>')
        if clit != cbar:
            out.append(f'<rect x="{fmt(x0 + 3 * seg)}" y="{fmt(y0)}" width="{fmt(seg)}" height="{fmt(h)}" fill="{clit}"/>')
    else:
        for i in range(7):
            c = clit if i == 3 else cbar
            out.append(f'<rect x="{fmt(x0 + i * w * 1.2)}" y="{fmt(y0)}" width="{fmt(w)}" height="{fmt(h)}" fill="{c}"/>')
    return "\n  ".join(out), h, w


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" '
            f'width="{fmt(w)}" height="{fmt(h)}" role="img" aria-label="{title}">\n'
            f'  <title>{title}</title>\n  {body}\n</svg>\n')


def build():
    lat = static_latin()
    # --- Arabic wordmark. Logical clusters: 0 seen, 1 dal, 2 ra, 3 ta marbuta.
    # Optical spacing between the unconnected letters is tightened by hand (font units).
    KERN = {2: -22, 3: -14}  # in visual order: after ta marbuta... see note below
    ar = Run(AR_BOLD, "سدرة", kern_after=KERN)
    axmin, aymin, axmax, aymax = ar.bounds
    W = axmax - axmin
    dal = ar.cluster_bounds(1)
    dal_h = dal[3] - dal[1]
    base_y = -aymin  # baseline position when ink top sits at y=0

    def latin_run(target_w, base_track_em):
        probe = Run(lat["SemiBold"], "SIDRA COFFEE", size_scale=1.0)
        b = probe.bounds
        nat = b[2] - b[0]  # at 1 unit per font unit
        n_gaps = len(probe.glyphs) - 1
        # size so that natural width + tracking fills target width
        s = target_w / (nat + n_gaps * base_track_em * 1000)
        r = Run(lat["SemiBold"], "SIDRA COFFEE", size_scale=s, tracking=base_track_em * 1000)
        # exact fit
        bb = r.bounds
        fit = target_w / (bb[2] - bb[0])
        r = Run(lat["SemiBold"], "SIDRA COFFEE", size_scale=s * fit, tracking=base_track_em * 1000)
        return r

    meta = {"unit": "SVG user units (font units x 0.1)", "wordmark_width": round(W, 2),
            "dal_height_clear_space": round(dal_h, 2)}
    files = {}

    def write(name, lang, content):
        fn = f"{SLUG}_logo_{name}_{lang}_{VER}.svg"
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(content)
        files[f"{name}_{lang}"] = fn

    for scheme, (cword, _, _) in SCHEMES.items():
        for solid in (False, True):
            tag = "-small" if solid else ""
            # ---- primary Arabic: wordmark + rule row
            w_bar = W / 8.2
            hb_ = w_bar / 2.0
            gap = hb_ * 1.15
            bars, bh, _ = bar_row(0, aymax - aymin + gap, W, 0.5, scheme, solid)
            wm = f'<path fill="{cword}" d="{ar.path(-axmin, base_y)}"/>'
            H1 = aymax - aymin + gap + bh
            write(f"primary{tag}-{scheme}", "ar", svg(W, H1, wm + "\n  " + bars, "سدرة"))
            meta.update(primary_height=round(H1, 2), bar_w=round(w_bar, 2), bar_h=round(hb_, 2),
                        bar_gap=round(w_bar / 5, 2), bars_y=round(aymax - aymin + gap, 2))

            # ---- bilingual: wordmark + rule row + SIDRA COFFEE tracked to the same width
            lr = latin_run(W, 0.16)
            lb = lr.bounds
            lat_h = lb[3] - lb[1]
            y_lat_top = H1 + gap
            lp = f'<path fill="{cword}" d="{lr.path(-lb[0], y_lat_top - lb[1])}"/>'
            H2 = y_lat_top + lat_h
            write(f"bilingual{tag}-{scheme}", "ar-en",
                  svg(W, H2, wm + "\n  " + bars + "\n  " + lp, "سدرة — Sidra Coffee"))
            meta.update(bilingual_height=round(H2, 2), latin_cap_height=round(lat_h, 2))

            # ---- Latin-led: SIDRA COFFEE over the rule row
            lr2 = latin_run(W, 0.05)
            l2 = lr2.bounds
            l2h = l2[3] - l2[1]
            bars2, bh2, _ = bar_row(0, l2h + gap, W, 0.5, scheme, solid)
            lp2 = f'<path fill="{cword}" d="{lr2.path(-l2[0], -l2[1])}"/>'
            H3 = l2h + gap + bh2
            write(f"latin{tag}-{scheme}", "en", svg(W, H3, lp2 + "\n  " + bars2, "Sidra Coffee"))
            meta.update(latin_height=round(H3, 2))

            if not solid:  # fallback 3: the wordmark alone
                write(f"wordmark-{scheme}", "ar", svg(W, aymax - aymin, wm, "سدرة"))

            # ---- icon: seven bars in band proportion (1:2, the widest band, to stay clear of a barcode look) centred in a square
            SQ = 200.0
            bw_total = SQ * 0.84
            wb = bw_total / 8.2
            hh = wb * 2
            ib, _, _ = bar_row((SQ - bw_total) / 2, (SQ - hh) / 2, bw_total, 2.0, scheme, solid)
            write(f"icon{tag}-{scheme}", "ar-en", svg(SQ, SQ, ib, "Sidra Coffee — seven bars"))

    with open(os.path.join(HERE, "logo-metrics.json"), "w") as f:
        json.dump({"metrics": meta, "files": files}, f, indent=1, ensure_ascii=False)
    print(json.dumps(meta, indent=1))
    print(len(files), "SVG files written")


if __name__ == "__main__":
    build()
