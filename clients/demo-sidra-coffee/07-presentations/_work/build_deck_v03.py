#!/usr/bin/env python3
"""Builds demo-sidra-coffee_presentation_cafe-owners_ar_v03.pptx (SYSTEM TEST, fictional client).

v03 after quality review r2 minors:
- name rule: the slide 2 card label carries the full name; layout names carry the full name too
- the thin seven-bar row now sits at the foot of both content layouts, so slides 2, 3 and 4 all carry it
  (a device only; no content is tied to a bar); slide 2 and 4 content re-set to end above it

v02 after quality review r1 (issues 8, 9, 10, 24):
- real brand master: theme fonts and colours, four layouts (cover, title + content, title only, closing)
- Latin runs (email, numerals) set in IBM Plex Sans; Arabic inherits IBM Plex Sans Arabic from the theme
- slide 2 states only the verified fact; slide 3 steps sit on their own three-column row
- sldSz no longer typed 4:3; larger slide counter; slide 4 caption rewritten; slide 5 reduced to email
"""
import os
import re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn, nsdecls
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "demo-sidra-coffee_presentation_cafe-owners_ar_v03.pptx")

HEX = {"paper": "F3ECE0", "crema": "E3C9A0", "ink": "1F1B18", "ember": "C23A20", "ash": "6F6861"}
RGB = {k: RGBColor.from_string(v) for k, v in HEX.items()}
AR, LAT = "IBM Plex Sans Arabic", "IBM Plex Sans"

SW, SH = 13.333, 7.5
M = 0.7
CW = SW - 2 * M
COL = CW / 8.2               # seven columns, gutter = 1/5 column
GUT = COL / 5
NS = nsdecls("p", "a", "r")
BODY_Y, BODY_H = 3.2, 2.5      # content zone on Paper slides
BAND_Y = 6.1                   # thin bar row at the foot of content slides
_id = [200]


def E(v):
    return int(round(v * 914400))


def nid():
    _id[0] += 1
    return _id[0]


def col_x(i):
    return M + (i - 1) * (COL + GUT)


def span_w(n):
    return n * COL + (n - 1) * GUT


def logo(variant):
    path = os.path.join(HERE, f"logo_{variant}_ar.png")      # rasterised from the SVG in round 1
    with Image.open(path) as im:
        return path, im.size[0] / im.size[1]


# ---------- raw shapes (usable on slides, layouts and the master) ----------
def add_rect(owner, x, y, w, h, colour, name="Bar"):
    xml = (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
           f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{HEX[colour]}"/></a:solidFill>'
           f'<a:ln><a:noFill/></a:ln></p:spPr></p:sp>')
    owner.shapes._spTree.append(parse_xml(xml))


def add_bars(owner, y, h, unlit, lit):
    """Seven bars on the seven grid columns, the fourth lit. A device, never a chart."""
    for i in range(1, 8):
        add_rect(owner, col_x(i), y, COL, h, lit if i == 4 else unlit)


def add_logo(owner, lg, w, y):
    path, ar = lg
    _, rId = owner.part.get_or_add_image_part(path)
    x, h = SW - M - w, w / ar
    xml = (f'<p:pic {NS}><p:nvPicPr><p:cNvPr id="{nid()}" name="Logo" descr="Sidra Coffee logo"/>'
           f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
           f'<p:blipFill><a:blip r:embed="{rId}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
           f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    owner.shapes._spTree.append(parse_xml(xml))


def set_bg(owner, colour):
    f = owner.background.fill
    f.solid()
    f.fore_color.rgb = RGB[colour]


# ---------- placeholder styling on master / layouts ----------
def place(ph, x, y, w, h, anchor="t"):
    ph.left, ph.top, ph.width, ph.height = Inches(x), Inches(y), Inches(w), Inches(h)
    bp = ph._element.txBody.find(qn("a:bodyPr"))
    for c in list(bp):
        bp.remove(c)
    for k in ("lIns", "tIns", "rIns", "bIns"):
        bp.set(k, "0")
    bp.set("anchor", anchor)
    bp.set("wrap", "square")


def lst_style(ph, size, bold, colour, ls, algn="r", rtl=1, latin_only=False):
    font = f'<a:latin typeface="{LAT}"/><a:ea typeface="{LAT}"/><a:cs typeface="{LAT}"/>' if latin_only else ""
    xml = (f'<a:lstStyle {NS}><a:lvl1pPr marL="0" indent="0" algn="{algn}" rtl="{rtl}">'
           f'<a:lnSpc><a:spcPct val="{int(ls * 100000)}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
           f'<a:defRPr sz="{int(size * 100)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{HEX[colour]}"/></a:solidFill>'
           f'{font}</a:defRPr></a:lvl1pPr></a:lstStyle>')
    tx = ph._element.txBody
    old = tx.find(qn("a:lstStyle"))
    new = parse_xml(xml)
    if old is not None:
        tx.replace(old, new)
    else:
        tx.insert(1, new)


def ph_of(owner, *types):
    for ph in owner.placeholders:
        if ph.placeholder_format.type in types:
            return ph
    return None


def drop(owner, *types):
    for ph in list(owner.placeholders):
        if ph.placeholder_format.type in types:
            ph._element.getparent().remove(ph._element)


# ---------- text on slides ----------
LATIN = re.compile(r"((?:[A-Za-z0-9][A-Za-z0-9@.\-]*[A-Za-z0-9])|[A-Za-z0-9])")


def add_runs(p, t, size=None, bold=None, colour=None, theme_refs=True):
    """Arabic runs take the theme fonts; Latin letters and numerals become separate IBM Plex Sans runs."""
    for n, seg in enumerate(LATIN.split(t)):
        if not seg:
            continue
        latin = n % 2 == 1
        r = p.add_run()
        r.text = seg
        if size is not None:
            r.font.size = Pt(size)
        if bold is not None:
            r.font.bold = bold
        if colour is not None:
            r.font.color.rgb = RGB[colour]
        rPr = r._r.get_or_add_rPr()
        rPr.set("lang", "en-US" if latin else "ar-SA")
        if latin:
            fonts = (("a:latin", LAT), ("a:ea", LAT), ("a:cs", LAT))
        elif theme_refs:
            fonts = (("a:latin", "+mn-lt"), ("a:cs", "+mn-cs"))
        else:
            fonts = ()
        for tag, face in fonts:
            etree.SubElement(rPr, qn(tag)).set("typeface", face)


def rtl(p, ls=None, after=None):
    p.alignment = PP_ALIGN.RIGHT
    p._p.get_or_add_pPr().set("rtl", "1")
    if ls is not None:
        p.line_spacing = ls
    if after is not None:
        p.space_after = Pt(after)


def fill_ph(ph, paras):
    """paras: list of (text, dict of run overrides, dict of paragraph options)."""
    tf = ph.text_frame
    for n, (t, ro, po) in enumerate(paras):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        rtl(p, po.get("ls"), po.get("after"))
        add_runs(p, t, theme_refs=False, **ro)


def text(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for n, d in enumerate(paras):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        rtl(p, d.get("ls", 1.6), d.get("after", 0))
        add_runs(p, d["t"], d["size"], bool(d.get("bold")), d.get("colour", "ink"))
    return box


def add_counter(slide, idx, total):
    xml = (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{nid()}" name="Slide Number"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
           f'<p:nvPr><p:ph type="sldNum" sz="quarter" idx="{idx}"/></p:nvPr></p:nvSpPr><p:spPr/>'
           f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p>'
           f'<a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum"><a:rPr lang="en-US"/><a:t>‹#›</a:t></a:fld>'
           f'<a:r><a:rPr lang="en-US"/><a:t xml:space="preserve"> / {total}</a:t></a:r></a:p></p:txBody></p:sp>')
    slide.shapes._spTree.append(parse_xml(xml))


# =====================================================================
prs = Presentation()
prs.slide_width, prs.slide_height = 12192000, 6858000   # exact widescreen EMU
sld_sz = prs._element.find(qn("p:sldSz"))
if "type" in sld_sz.attrib:
    del sld_sz.attrib["type"]            # was screen4x3; 13.333 x 7.5 in is the untyped widescreen size

master = prs.slide_masters[0]

# ----- theme: brand fonts and colours -----
theme = master.part.part_related_by(RT.THEME)
x = theme.blob.decode("utf-8")
fs = re.search(r"<a:fontScheme.*?</a:fontScheme>", x, re.S).group(0)
fs2 = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="Sidra Coffee"', fs)
fs2 = re.sub(r'<a:latin typeface="[^"]*"', f'<a:latin typeface="{LAT}"', fs2)
fs2 = re.sub(r'<a:cs typeface="[^"]*"', f'<a:cs typeface="{AR}"', fs2)
fs2 = re.sub(r'<a:font script="Arab" typeface="[^"]*"', f'<a:font script="Arab" typeface="{AR}"', fs2)
x = x.replace(fs, fs2)
scheme = [("dk1", "ink"), ("lt1", "paper"), ("dk2", "ash"), ("lt2", "crema"), ("accent1", "ember"),
          ("accent2", "ink"), ("accent3", "crema"), ("accent4", "ash"), ("accent5", "paper"),
          ("accent6", "ember"), ("hlink", "ember"), ("folHlink", "ash")]
clr = '<a:clrScheme name="Sidra Coffee">' + "".join(
    f'<a:{k}><a:srgbClr val="{HEX[v]}"/></a:{k}>' for k, v in scheme) + "</a:clrScheme>"
x = re.sub(r"<a:clrScheme.*?</a:clrScheme>", clr, x, flags=re.S)
x = re.sub(r'<a:theme([^>]*) name="[^"]*"', r'<a:theme\1 name="Sidra Coffee"', x, count=1)
theme._blob = x.encode("utf-8")

# ----- master: Paper ground, RTL title and body styles, slide number -----
set_bg(master, "paper")
tx = master._element.find(qn("p:txStyles"))


def tune(lvl, size, ls, bold=None):
    lvl.set("algn", "r")
    lvl.set("rtl", "1")
    for tag in ("a:lnSpc", "a:buFont"):
        old = lvl.find(qn(tag))
        if old is not None:
            lvl.remove(old)
    lvl.insert(0, parse_xml(f'<a:lnSpc {NS}><a:spcPct val="{int(ls * 100000)}"/></a:lnSpc>'))
    bu = lvl.find(qn("a:buChar"))
    if bu is not None:                    # bullet glyph from the brand font, not a symbol fallback
        bu.addprevious(parse_xml(f'<a:buFont {NS} typeface="{LAT}"/>'))
    d = lvl.find(qn("a:defRPr"))
    d.set("sz", str(size * 100))
    if bold is not None:
        d.set("b", str(int(bold)))


tune(tx.find(qn("p:titleStyle")).find(qn("a:lvl1pPr")), 32, 1.3, True)
body_style = tx.find(qn("p:bodyStyle"))
for i, sz in zip(range(1, 10), (18, 16, 15, 14, 14, 14, 14, 14, 14)):
    lv = body_style.find(qn(f"a:lvl{i}pPr"))
    if lv is not None:
        tune(lv, sz, 1.6)

drop(master, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER)
place(ph_of(master, PP_PLACEHOLDER.TITLE), M, 1.9, CW, 1.0)
place(ph_of(master, PP_PLACEHOLDER.BODY), M, BODY_Y, CW, BODY_H)
num = ph_of(master, PP_PLACEHOLDER.SLIDE_NUMBER)
place(num, M, 0.6, 2.0, 0.45)
lst_style(num, 18, False, "ash", 1.2, algn="l", rtl=0, latin_only=True)

# ----- layouts: keep four, restyle, remove the rest -----
by_name = {l.name: l for l in master.slide_layouts}
L_COVER, L_CONTENT, L_TITLE, L_CLOSE = (by_name[n] for n in
                                        ("Title Slide", "Title and Content", "Title Only", "Section Header"))
for l in list(master.slide_layouts):
    if l not in (L_COVER, L_CONTENT, L_TITLE, L_CLOSE):
        master.slide_layouts.remove(l)

lg_colour, lg_ember, lg_rev = logo("primary-colour"), logo("primary-colour-on-ember"), logo("primary-colour-reversed")

# cover: Ember ground, Ink bars with a Paper lit bar
L_COVER.name = "Sidra Coffee 1 Cover"
set_bg(L_COVER, "ember")
drop(L_COVER, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.SLIDE_NUMBER)
t = ph_of(L_COVER, PP_PLACEHOLDER.CENTER_TITLE, PP_PLACEHOLDER.TITLE)
place(t, M, 2.35, CW, 1.4)
lst_style(t, 60, True, "paper", 1.3)
st = ph_of(L_COVER, PP_PLACEHOLDER.SUBTITLE)
place(st, M, 3.85, CW, 0.8)
lst_style(st, 22, False, "paper", 1.5)
add_logo(L_COVER, lg_ember, 2.2, 0.7)
add_bars(L_COVER, 5.35, 2.91, "ink", "paper")       # band 1:2, bleeds off the bottom edge

# title + content and title only: Paper ground, logo top right, counter top left
for l, nm in ((L_CONTENT, "Sidra Coffee 2 Title and content"), (L_TITLE, "Sidra Coffee 3 Title only")):
    l.name = nm
    drop(l, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER)
    add_logo(l, lg_colour, 1.5, 0.6)
    add_bars(l, BAND_Y, COL / 2, "ink", "ember")     # device at the foot of every content slide

# closing: Ink ground, Paper bars with the Ember lit bar
L_CLOSE.name = "Sidra Coffee 4 Closing"
set_bg(L_CLOSE, "ink")
drop(L_CLOSE, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.SLIDE_NUMBER)
t = ph_of(L_CLOSE, PP_PLACEHOLDER.TITLE)
place(t, M, 2.3, CW, 1.0)
lst_style(t, 40, True, "paper", 1.3)
b = ph_of(L_CLOSE, PP_PLACEHOLDER.BODY)
place(b, M, 3.6, CW, 2.2)
lst_style(b, 22, False, "paper", 1.5)
add_logo(L_CLOSE, lg_rev, 2.2, 0.7)
add_bars(L_CLOSE, 6.35, COL / 2, "paper", "ember")

NUM_IDX = ph_of(L_TITLE, PP_PLACEHOLDER.SLIDE_NUMBER).placeholder_format.idx
TOTAL = 5

# =====================================================================
# 1. Cover
s = prs.slides.add_slide(L_COVER)
fill_ph(s.shapes.title, [("تُحمَّص لطلبك، كل أسبوع.", {}, {})])
fill_ph(s.placeholders[1], [("سدرة للقهوة: محمصة قهوة مختصة من الرياض، لمقاهي الرياض المستقلة.", {}, {})])

# 2. The problem: need on the right, the verified fact on the left
s = prs.slides.add_slide(L_TITLE)
fill_ph(s.shapes.title, [("المقهى المستقل يحتاج محمصة تحمّص لطلبه هو.", {}, {})])
half = (CW - GUT) / 2
cy, ch = BODY_Y, BODY_H
cards = [("ما يحتاجه مقهاك", "قهوة تُحمَّص لطلبك أنت."),
         ("ما تفعله سدرة للقهوة", "نحمّص كل أسبوع، وعلى الطلب.")]
for k, (label, line) in enumerate(cards):
    cx = SW - M - half - k * (half + GUT)          # first card on the right
    add_rect(s, cx, cy, half, ch, "crema", name="Panel")
    text(s, cx + 0.4, cy, half - 0.8, ch, [
        {"t": label, "size": 18, "ls": 1.6, "after": 6},
        {"t": line, "size": 26, "bold": True, "ls": 1.3},
    ], anchor=MSO_ANCHOR.MIDDLE)
add_counter(s, NUM_IDX, TOTAL)

# 3. How Sidra Coffee works: three equal columns, right to left; the bar row comes from the layout
s = prs.slides.add_slide(L_TITLE)
fill_ph(s.shapes.title, [("ثلاث خطوات تتكرّر كل أسبوع: تطلب، نحمّص، نورّد.", {}, {})])
gap = 0.5
tw = (CW - 2 * gap) / 3
steps = [("1", "تطلب", "تخبرنا بما يحتاجه مقهاك من القهوة."),
         ("2", "نحمّص", "نحمّص طلبك في تحميصة هذا الأسبوع."),
         ("3", "نورّد", "نورّد لمقهاك القهوة التي حُمّصت له.")]
for k, (n, head, body) in enumerate(steps):
    sx = SW - M - tw - k * (tw + gap)              # step 1 on the right
    text(s, sx, BODY_Y, tw, BODY_H, [
        {"t": n, "size": 40, "bold": True, "ls": 1.2},
        {"t": head, "size": 24, "bold": True, "ls": 1.4, "after": 4},
        {"t": body, "size": 17, "ls": 1.6},
    ])
add_counter(s, NUM_IDX, TOTAL)

# 4. Products and services: bulleted body placeholder (4 columns from the right) + Crema panel (3 from the left)
s = prs.slides.add_slide(L_CONTENT)
fill_ph(s.shapes.title, [("قهوة مختصة، توريد أسبوعي، وتدريب لفريق مقهاك.", {}, {})])
py, ph_h = BODY_Y, BODY_H
pw = span_w(3)
body = s.placeholders[1]
body.left, body.top, body.width, body.height = Inches(col_x(4)), Inches(py), Inches(span_w(4)), Inches(ph_h)
items = [("حبوب مختصة محمّصة: ", "محاصيل مفردة وخلطات البيت."),
         ("توريد للمقاهي: ", "يُحمَّص لطلبك ويُورَّد كل أسبوع."),
         ("تدريب الباريستا: ", "دورات قصيرة لفريق مقهاك."),
         ("اشتراك القهوة: ", "توصيل شهري إلى البيوت.")]
tf = body.text_frame
for n, (head, rest) in enumerate(items):
    p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
    rtl(p, after=10)
    add_runs(p, head, bold=True, theme_refs=False)
    add_runs(p, rest, theme_refs=False)
add_rect(s, M, py, pw, ph_h, "crema", name="Panel")
text(s, M + 0.4, py, pw - 0.8, ph_h, [
    {"t": "250 غ", "size": 44, "bold": True, "ls": 1.1},
    {"t": "1 كغ", "size": 44, "bold": True, "ls": 1.1, "after": 6},
    {"t": "نبيع الحبوب المحمّصة بحجمين.", "size": 16, "ls": 1.6},
], anchor=MSO_ANCHOR.MIDDLE)
add_counter(s, NUM_IDX, TOTAL)

# 5. Next step / contact: email only (no phone, no timing)
s = prs.slides.add_slide(L_CLOSE)
fill_ph(s.shapes.title, [("الخطوة التالية: أخبرنا بما يحتاجه مقهاك.", {}, {})])
fill_ph(s.placeholders[1], [
    ("راسلنا", {}, {"after": 4}),
    ("hello@sidra-coffee.example", {"size": 30, "bold": True}, {"ls": 1.3}),
])

prs.core_properties.title = "سدرة للقهوة: عرض لأصحاب المقاهي"
prs.core_properties.language = "ar-SA"
prs.core_properties.author = "Creative Agency OS (system test)"
prs.core_properties.revision = 3
prs.save(OUT)
print("saved", OUT)
