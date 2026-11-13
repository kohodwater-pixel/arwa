#!/usr/bin/env python3
"""Builds demo-sidra-coffee_presentation_cafe-owners_ar_v01.pptx (SYSTEM TEST, fictional client).
Arabic, RTL, 16:9. Colours and fonts from 04-identity/03-system/tokens.json."""
import os
import cairosvg
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.dirname(os.path.dirname(HERE))
LOGO_DIR = os.path.join(CLIENT, "04-identity", "02-logo")
OUT = os.path.join(os.path.dirname(HERE), "demo-sidra-coffee_presentation_cafe-owners_ar_v01.pptx")

PAPER = RGBColor(0xF3, 0xEC, 0xE0)
CREMA = RGBColor(0xE3, 0xC9, 0xA0)
INK = RGBColor(0x1F, 0x1B, 0x18)
EMBER = RGBColor(0xC2, 0x3A, 0x20)
ASH = RGBColor(0x6F, 0x68, 0x61)
FONT = "IBM Plex Sans Arabic"

SW, SH = 13.333, 7.5
M = 0.7                      # margin
CW = SW - 2 * M              # content width
COL = CW / 8.2               # seven columns, gutter = 1/5 column
GUT = COL / 5


def col_x(i):
    """Left edge of column i, counted 1..7 from the LEFT."""
    return M + (i - 1) * (COL + GUT)


def span_w(n):
    return n * COL + (n - 1) * GUT


def logo_png(variant, lang="ar"):
    src = os.path.join(LOGO_DIR, f"demo-sidra-coffee_logo_{variant}_{lang}_v01.svg")
    dst = os.path.join(HERE, f"logo_{variant}_{lang}.png")
    cairosvg.svg2png(url=src, write_to=dst, output_width=1600)
    with Image.open(dst) as im:
        return dst, im.size[0] / im.size[1]


def bg(slide, colour):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = colour


def rect(slide, x, y, w, h, colour):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = colour
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def bars(slide, y, h, unlit, lit):
    """Seven bars on the seven grid columns; the fourth is lit."""
    for i in range(1, 8):
        rect(slide, col_x(i), y, COL, h, lit if i == 4 else unlit)


def text(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP):
    """paras: list of dicts: t, size, bold, colour, ls (line spacing), after (pt)."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for n, d in enumerate(paras):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.RIGHT
        p.line_spacing = d.get("ls", 1.6)
        p.space_after = Pt(d.get("after", 0))
        p._p.get_or_add_pPr().set("rtl", "1")
        r = p.add_run()
        r.text = d["t"]
        r.font.size = Pt(d["size"])
        r.font.bold = bool(d.get("bold"))
        r.font.color.rgb = d.get("colour", INK)
        r.font.name = FONT                      # a:latin
        rPr = r._r.get_or_add_rPr()
        rPr.set("lang", "ar-SA")
        for tag in ("a:ea", "a:cs"):
            el = etree.SubElement(rPr, qn(tag))
            el.set("typeface", FONT)
    return box


def header(slide, logo, label, label_colour=ASH):
    path, ar = logo
    w = 1.5
    slide.shapes.add_picture(path, Inches(SW - M - w), Inches(0.6), Inches(w), Inches(w / ar))
    text(slide, M, 0.6, 4, 0.4, [{"t": label, "size": 12, "colour": label_colour, "ls": 1.6}])
    # caption sits at the left edge: left-aligned visually but still an RTL paragraph
    slide.shapes[-1].text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT


def title(slide, t, colour=INK, y=1.95, cols=6, size=36):
    w = span_w(cols)
    text(slide, SW - M - w, y, w, 1.6, [{"t": t, "size": size, "bold": True, "colour": colour, "ls": 1.3}])


prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
blank = prs.slide_layouts[6]

logo_colour = logo_png("primary-colour")
logo_ember = logo_png("primary-colour-on-ember")
logo_rev = logo_png("primary-colour-reversed")

# ---------- 1. Cover (Ember ground: Ink bars, Paper lit bar) ----------
s = prs.slides.add_slide(blank)
bg(s, EMBER)
p, ar = logo_ember
lw = 2.2
s.shapes.add_picture(p, Inches(SW - M - lw), Inches(0.7), Inches(lw), Inches(lw / ar))
w = span_w(6)
text(s, SW - M - w, 2.35, w, 1.4,
     [{"t": "تُحمَّص لطلبك، كل أسبوع.", "size": 60, "bold": True, "colour": PAPER, "ls": 1.3}])
text(s, SW - M - w, 3.85, w, 0.7,
     [{"t": "سدرة للقهوة: محمصة قهوة مختصة من الرياض، لمقاهي الرياض المستقلة.",
       "size": 22, "colour": PAPER, "ls": 1.5}])
bars(s, 5.35, 2.91, INK, PAPER)          # band 1:2, bleeds off the bottom edge

# ---------- 2. The problem ----------
s = prs.slides.add_slide(blank)
bg(s, PAPER)
header(s, logo_colour, "عرض لأصحاب المقاهي  |  2 من 5")
title(s, "صاحب المقهى لا ينبغي أن يتساءل عمّا في الكيس، ولا متى يصل.")
half = (CW - GUT) / 2
cy, ch = 3.75, 1.85
for k, q in enumerate(["«متى حُمّصت هذه القهوة؟»", "«ومتى يصل طلبي القادم؟»"]):
    x = SW - M - half - k * (half + GUT)      # first card on the right
    rect(s, x, cy, half, ch, CREMA)
    text(s, x + 0.4, cy, half - 0.8, ch,
         [{"t": q, "size": 30, "bold": True, "ls": 1.3}], anchor=MSO_ANCHOR.MIDDLE)
text(s, SW - M - span_w(6), 5.95, span_w(6), 0.9,
     [{"t": "سؤالان يشغلان صاحب المقهى عن مقهاه. سدرة موجودة لتجيب عنهما بإيقاع ثابت: تحميصة كل أسبوع، وعلى طلبك.",
       "size": 18, "ls": 1.6}])

# ---------- 3. How Sidra works ----------
s = prs.slides.add_slide(blank)
bg(s, PAPER)
header(s, logo_colour, "عرض لأصحاب المقاهي  |  3 من 5")
title(s, "نحمّص كل أسبوع، وعلى طلبك أنت.")
by = 3.3
bars(s, by, COL / 2, INK, EMBER)             # rule 2:1 on the grid columns
steps = [  # (first column from left, number of columns, number, head, body)
    (6, 2, "1", "تطلب", "تخبرنا بما يحتاجه مقهاك من القهوة."),
    (3, 3, "2", "نحمّص", "يدخل طلبك تحميصة الأسبوع، فيُحمَّص لك أنت."),
    (1, 2, "3", "نورّد", "تصلك قهوتك، ويتكرّر الإيقاع في الأسبوع التالي."),
]
for c0, n, num, head, body in steps:
    x, w = col_x(c0), span_w(n)
    text(s, x, by + COL / 2 + 0.35, w, 2.6, [
        {"t": num, "size": 40, "bold": True, "colour": EMBER if num == "2" else INK, "ls": 1.2},
        {"t": head, "size": 24, "bold": True, "ls": 1.4, "after": 4},
        {"t": body, "size": 17, "ls": 1.6},
    ])

# ---------- 4. Products and services ----------
s = prs.slides.add_slide(blank)
bg(s, PAPER)
header(s, logo_colour, "عرض لأصحاب المقاهي  |  4 من 5")
title(s, "قهوة مختصة، توريد أسبوعي، وتدريب لفريق مقهاك.")
py, ph = 3.45, 3.35
pw = span_w(3)
rect(s, M, py, pw, ph, CREMA)                # left panel, 3 columns
text(s, M + 0.4, py, pw - 0.8, ph, [
    {"t": "250 غ", "size": 54, "bold": True, "ls": 1.2},
    {"t": "1 كغ", "size": 54, "bold": True, "ls": 1.2, "after": 6},
    {"t": "حجما الكيس: محاصيل مفردة وخلطات البيت.", "size": 16, "ls": 1.6},
], anchor=MSO_ANCHOR.MIDDLE)
items = [
    ("حبوب مختصة محمّصة", "محاصيل مفردة وخلطات البيت، في كيس 250 غ أو 1 كغ."),
    ("توريد للمقاهي", "يُحمَّص لطلبك ويُورَّد كل أسبوع."),
    ("دورات للباريستا", "دورات قصيرة لفريق مقهاك، ليخرج الكوب كما يجب."),
    ("اشتراك القهوة", "توصيل شهري إلى البيوت، لمن يحضّر قهوته في بيته."),
]
cw2 = span_w(2)
for k, (head, body) in enumerate(items):
    colk, row = k % 2, k // 2
    x = SW - M - cw2 - colk * (cw2 + GUT)     # first item top right
    y = py + row * 1.75
    text(s, x, y, cw2, 1.6, [
        {"t": head, "size": 22, "bold": True, "ls": 1.4, "after": 2},
        {"t": body, "size": 16, "ls": 1.6},
    ])

# ---------- 5. Next step / contact (Ink ground) ----------
s = prs.slides.add_slide(blank)
bg(s, INK)
p, ar = logo_rev
s.shapes.add_picture(p, Inches(SW - M - lw), Inches(0.7), Inches(lw), Inches(lw / ar))
w = span_w(6)
text(s, SW - M - w, 2.3, w, 1.0,
     [{"t": "الخطوة التالية: أخبرنا بما يحتاجه مقهاك.", "size": 40, "bold": True, "colour": PAPER, "ls": 1.3}])
text(s, SW - M - w, 3.45, w, 0.7,
     [{"t": "راسلنا، ونرتّب معك أول طلب في تحميصة الأسبوع.", "size": 22, "colour": PAPER, "ls": 1.5}])
text(s, SW - M - w, 4.45, w, 1.5, [
    {"t": "البريد الإلكتروني", "size": 14, "colour": CREMA, "ls": 1.6},
    {"t": "hello@sidra-coffee.example", "size": 26, "bold": True, "colour": PAPER, "ls": 1.3, "after": 6},
    {"t": "الرياض، المملكة العربية السعودية", "size": 18, "colour": CREMA, "ls": 1.6},
])
bars(s, 6.35, COL / 2, PAPER, EMBER)

prs.core_properties.title = "سدرة للقهوة: عرض لأصحاب المقاهي"
prs.core_properties.language = "ar-SA"
prs.core_properties.author = "Creative Agency OS (system test)"
prs.save(OUT)
print("saved", OUT)
