"""v02 directions: embed sRGB, write deliverable PNGs and 390 px previews, and
measure text contrast on the rendered pixels.

Method: render_v02.cjs saves the page twice, with and without glyphs. Pixels that
differ are the glyphs. For each text element the background is sampled from the
text-free render at the glyph pixels and a 3 px halo around them, and compared
with the element's computed text colour (WCAG 2 relative luminance). Reported:
the worst pixel and the 5th percentile, so one stray pixel does not hide a
generally weak area."""
import json, os, re, sys
import numpy as np
from PIL import Image, ImageCms, ImageFilter

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.dirname(here)
icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
dirs = [a for a in sys.argv[1:]] or ['a', 'b']
VER = {'a': 'v04', 'b': 'v03'}


def lin(c):
    c = c / 255.0
    return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lum(rgb):
    l = lin(np.asarray(rgb, dtype=float))
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]


worst = {}
for d in dirs:
    for fmt, size in (("post", (1080, 1350)), ("story", (1080, 1920))):
        name = f"tbc-restaurants-company_job-advert_{fmt}-direction-{d}_ar_{VER[d]}"
        raw = Image.open(os.path.join(here, name + "_raw.png")).convert("RGB")
        assert raw.size == size, raw.size
        p = os.path.join(out, name + ".png")
        raw.save(p, icc_profile=icc, optimize=True)
        chk = Image.open(p)
        assert chk.size == size and len(chk.info.get("icc_profile", b"")) > 100
        raw.resize((390, round(size[1] * 390 / 1080)), Image.LANCZOS).save(os.path.join(here, name + "_390.png"))
        print(f"\n{name}  {chk.size} {chk.mode} icc {len(chk.info['icc_profile'])} B, {os.path.getsize(p) // 1024} KB")

        bg = Image.open(os.path.join(here, name + "_bg.png")).convert("RGB")
        A, B = np.asarray(raw).astype(int), np.asarray(bg).astype(int)
        glyph = (np.abs(A - B).sum(axis=2) > 24).astype(np.uint8) * 255
        halo = np.asarray(Image.fromarray(glyph).filter(ImageFilter.MaxFilter(7))) > 0
        Lbg = lum(B)
        for t in json.load(open(os.path.join(here, name + "_texts.json"), encoding="utf-8")):
            x0, y0 = max(t["x"] - 2, 0), max(t["y"] - 2, 0)
            x1, y1 = min(t["x"] + t["w"] + 2, size[0]), min(t["y"] + t["h"] + 2, size[1])
            m = halo[y0:y1, x0:x1]
            if m.sum() < 20:
                print("  !! no glyph pixels found for", t["key"]); continue
            rgb = [float(v) for v in re.findall(r"[\d.]+", t["color"])[:3]]
            lt = float(lum(rgb))
            lb = Lbg[y0:y1, x0:x1][m]
            cr = (np.maximum(lt, lb) + 0.05) / (np.minimum(lt, lb) + 0.05)
            need = 4.5 if t["kind"] == "body" else 3.0
            lo, p5 = float(cr.min()), float(np.percentile(cr, 5))
            flag = "" if lo >= need else ("  << worst pixel below target" if p5 >= need else "  << FAIL")
            print(f"  {lo:5.2f} min / {p5:5.2f} p5  (need {need})  {t['kind']:7s} {t['fs']:.0f}px  {t['key']}{flag}")
            k = (d, fmt, t["kind"])
            worst[k] = min(worst.get(k, 99), lo)
print()
for k, v in sorted(worst.items()):
    print("worst", k, f"{v:.2f}:1")
