"""Embed an sRGB ICC profile in the raw screenshots, write the deliverable PNGs,
and measure WCAG contrast for the palette pairs. Run after render.cjs."""
import os
from PIL import Image, ImageCms

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.dirname(here)
icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
for n, size in (("post", (1080, 1350)), ("story", (1080, 1920))):
    name = f"tbc-restaurants-company_job-advert_{n}_ar_v01"
    im = Image.open(os.path.join(here, name + "_raw.png")).convert("RGB")
    assert im.size == size, im.size
    p = os.path.join(out, name + ".png")
    im.save(p, icc_profile=icc, optimize=True)
    chk = Image.open(p)
    print(name, chk.size, chk.mode, "icc bytes:", len(chk.info.get("icc_profile", b"")), os.path.getsize(p) // 1024, "KB")


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


pairs = [
    ("body / headline line 1  #F7F1E5 on #15302A", "#F7F1E5", "#15302A"),
    ("sector line             #D8D1C0 on #15302A", "#D8D1C0", "#15302A"),
    ("accent text (kicker, headline line 2, block titles) #F2A93B on #15302A", "#F2A93B", "#15302A"),
    ("apply line + tag        #15302A on #F2A93B", "#15302A", "#F2A93B"),
    ("gap label (logo)        #A9B5AE on #15302A", "#A9B5AE", "#15302A"),
    ("gap label (contact)     #4A3A12 on #F2A93B", "#4A3A12", "#F2A93B"),
]
for label, a, b in pairs:
    print(f"{cr(a, b):5.2f}:1  {label}")
