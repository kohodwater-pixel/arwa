#!/usr/bin/env python3
"""Build the editable Word catalogue from data/rates.json (via catalogue_lib).

Same content and order as the PDF: cover, about/legend/index, Moscow section, Saint
Petersburg section, analysis, notes. RTL is set as paragraph bidi + table bidiVisual,
not just right alignment. Fonts are referenced by name (IBM Plex Sans Arabic for
Arabic / complex script, Montserrat for Latin and numerals, Playfair Display for
Latin display lines); they must be installed on the machine that opens the file.
"""
import re, sys, pathlib
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import catalogue_lib as L

WORK = pathlib.Path(__file__).resolve().parent
ROOT = WORK.parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v01"
OUT = ROOT / f"hikayat-moscow_russia-hotel-collection_catalogue_ar-en_{VERSION}.docx"
D, M = L.DATA, L.DATA["meta"]
NAVY, GOLD, IVORY, CHAR, MUTED, GOLDTXT, WHITE = "14243A", "C6A66B", "F7F4ED", "292D32", "5E6470", "8A6D32", "FFFFFF"
AR_FONT, LAT_FONT, DISP_FONT = "IBM Plex Sans Arabic", "Montserrat", "Playfair Display"
ARABIC = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Mm(210), Mm(297)
sec.left_margin = sec.right_margin = Mm(18)
sec.top_margin, sec.bottom_margin = Mm(20), Mm(18)
sec.header_distance, sec.footer_distance = Mm(9), Mm(8)
# section direction RTL
sectPr = sec._sectPr
bidi = OxmlElement("w:bidi"); sectPr.append(bidi)

# default style: fonts per script, RTL
st = doc.styles["Normal"]
st.font.name = LAT_FONT
st.font.size = Pt(10)
rpr = st.element.get_or_add_rPr()
rf = rpr.find(qn("w:rFonts"))
if rf is None:
    rf = OxmlElement("w:rFonts"); rpr.append(rf)
for k, v in (("w:ascii", LAT_FONT), ("w:hAnsi", LAT_FONT), ("w:cs", AR_FONT), ("w:eastAsia", LAT_FONT)):
    rf.set(qn(k), v)
szcs = OxmlElement("w:szCs"); szcs.set(qn("w:val"), "20"); rpr.append(szcs)
ppr = st.element.get_or_add_pPr()
b = OxmlElement("w:bidi"); ppr.append(b)
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.line_spacing = 1.25
# lang
lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "en-US"); lang.set(qn("w:bidi"), "ar-SA"); rpr.append(lang)


def set_rtl_par(p, rtl=True):
    pPr = p._p.get_or_add_pPr()
    for el in pPr.findall(qn("w:bidi")):
        pPr.remove(el)
    el = OxmlElement("w:bidi")
    if not rtl:
        el.set(qn("w:val"), "0")
    pPr.append(el)


def set_align(p, align, rtl):
    """In a bidi paragraph OOXML jc is logical: 'left' = start (visual right). Swap for RTL paragraphs."""
    if rtl and align in ("left", "right"):
        align = {"left": "right", "right": "left"}[align]
    p.alignment = {"right": WD_ALIGN_PARAGRAPH.RIGHT, "left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER}[align]


def run(p, text, size=10, bold=False, color=CHAR, font=None, rtl=None):
    is_ar = bool(ARABIC.search(text)) if rtl is None else rtl
    if not is_ar and re.search(r"\d", text):
        text = "\u202A" + text + "\u202C"   # LRE ... PDF: keep Latin+number runs in LTR order inside RTL paragraphs
    elif is_ar and text[:1].isdigit():
        text = "\u200F" + text   # RLM: an Arabic run that starts with a digit stays with the Arabic text
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor.from_string(color)
    rPr = r._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.insert(0, rf)
    lat = font or LAT_FONT
    for k, v in (("w:ascii", lat), ("w:hAnsi", lat), ("w:cs", AR_FONT)):
        rf.set(qn(k), v)
    sz = OxmlElement("w:szCs"); sz.set(qn("w:val"), str(int(size * 2))); rPr.append(sz)
    if bold:
        bc = OxmlElement("w:bCs"); rPr.append(bc)
    if is_ar:
        rt = OxmlElement("w:rtl"); rPr.append(rt)
    return r


def par(container, parts, align="right", after=2, before=0, keep=False, rtl=True, line=None):
    p = container.add_paragraph()
    set_rtl_par(p, rtl)
    set_align(p, align, rtl)
    # in a bidi paragraph Word's 'right' is the logical start; python-docx writes w:jc right which Word shows correctly
    pf = p.paragraph_format
    pf.space_after, pf.space_before = Pt(after), Pt(before)
    pf.keep_with_next = keep
    if line:
        pf.line_spacing = line
    for part in parts:
        if isinstance(part, str):
            run(p, part)
        else:
            run(p, part[0], **part[1])
    return p


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def borders(table, color="E4DCCB", sz=4, inside_v=False):
    tblPr = table._tbl.tblPr
    bd = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        if edge == "insideV" and not inside_v or edge in ("left", "right"):
            el.set(qn("w:val"), "nil")
        else:
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz)); el.set(qn("w:color"), color)
        bd.append(el)
    tblPr.append(bd)


def table_rtl(table):
    tblPr = table._tbl.tblPr
    bv = OxmlElement("w:bidiVisual"); tblPr.append(bv)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER


def cell_margins(table, top=50, bottom=50, side=90):
    tblPr = table._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for k, v in (("top", top), ("bottom", bottom), ("start", side), ("end", side), ("left", side), ("right", side)):
        el = OxmlElement(f"w:{k}"); el.set(qn("w:w"), str(v)); el.set(qn("w:type"), "dxa"); m.append(el)
    tblPr.append(m)


def header_row(row):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); trPr.append(h)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    c = OxmlElement("w:cantSplit"); trPr.append(c)


def cell_text(cell, parts, align="right", rtl=True, keep=False):
    cell.text = ""
    p = cell.paragraphs[0]
    set_rtl_par(p, rtl)
    set_align(p, align, rtl)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.keep_with_next = keep
    first = True
    for part in parts:
        if part == "\n":
            p = cell.add_paragraph(); set_rtl_par(p, rtl)
            set_align(p, align, rtl)
            p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.keep_with_next = keep
            continue
        text, kw = part
        run(p, text, **kw)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def widths(table, mm_list):
    for row in table.rows:
        for i, w in enumerate(mm_list):
            row.cells[i].width = Mm(w)


def hdr_cells(table, cols, sar_idx=None, num_idx=()):
    row = table.rows[0]
    header_row(row)
    for i, (ar, en) in enumerate(cols):
        c = row.cells[i]
        shade(c, "0E1A2B" if i == sar_idx else NAVY)
        al = "left" if i in num_idx else "right"
        cell_text(c, [(ar, dict(size=9.5, bold=True, color=WHITE)), "\n", (en.upper(), dict(size=7, color=GOLD, rtl=False))], align=al, keep=True)


def rub_parts(rub):
    return [(L.fmt_rub(rub), dict(size=10, color="3B3F45", rtl=False)), (" RUB", dict(size=7, color=MUTED, rtl=False))]


def sar_parts(sar):
    return [(L.fmt_sar(sar), dict(size=12, bold=True, color=NAVY, rtl=False)), (" SAR", dict(size=7, bold=True, color=GOLDTXT, rtl=False))]


def page_break():
    p = doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)
    p.paragraph_format.space_after = Pt(0)


def heading(ar, en, size=13, before=8, after=3):
    return par(doc, [(ar, dict(size=size, bold=True, color=NAVY)), ("   ", dict(size=size)), (en, dict(size=size - 2.5, color=GOLDTXT, font=DISP_FONT, rtl=False))],
               before=before, after=after, keep=True)


def bullets(items, size=10):
    for it in items:
        par(doc, [("•  ", dict(size=10, color=GOLD, rtl=False)), (it, dict(size=size))], after=1.5, line=1.3)


# ------------------------------------------------------------------ footer / header
def set_header_footer():
    hp = sec.header.paragraphs[0]
    set_rtl_par(hp); set_align(hp, "left", True)
    run(hp, "RUSSIA HOTEL COLLECTION 2026", size=7.5, color=MUTED, rtl=False)
    pPr = hp._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "4"), ("w:color", GOLD)):
        bt.set(qn(k), v)
    bdr.append(bt); pPr.append(bdr)
    fp = sec.footer.paragraphs[0]
    set_rtl_par(fp); fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(fp, M["agency_ar"] + "   ·   ", size=8.5, color=MUTED)
    r = run(fp, "", size=9, color=NAVY, font=DISP_FONT, rtl=False)
    for t, txt in (("begin", None), (None, " PAGE "), ("end", None)):
        if t:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), t); r._r.append(fc)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._r.append(it)

    sec.different_first_page_header_footer = True


set_header_footer()

# ------------------------------------------------------------------ cover
t = doc.add_table(rows=1, cols=1); table_rtl(t)
c = t.rows[0].cells[0]; shade(c, NAVY); c.width = Mm(174)
trPr = t.rows[0]._tr.get_or_add_trPr(); h = OxmlElement("w:trHeight"); h.set(qn("w:val"), "14000"); h.set(qn("w:hRule"), "exact"); trPr.append(h)
cell_text(c, [("إصدار 15 نوفمبر 2026", dict(size=9.5, color="CFC6B4")), "\n", (" ", dict(size=40)), "\n",
              ("MOSCOW · SAINT PETERSBURG", dict(size=8.5, color=GOLD, rtl=False)), "\n", (" ", dict(size=14)), "\n",
              ("RUSSIA", dict(size=44, color=IVORY, font=DISP_FONT, rtl=False)), "\n",
              ("HOTEL COLLECTION", dict(size=24, color=IVORY, font=DISP_FONT, rtl=False)), "\n",
              ("2026", dict(size=28, color=GOLD, font=DISP_FONT, rtl=False)), "\n", (" ", dict(size=14)), "\n",
              (M["subtitle_en"], dict(size=15, color=IVORY, font=DISP_FONT, rtl=False)), "\n", (" ", dict(size=10)), "\n",
              (M["title_ar"], dict(size=20, bold=True, color=IVORY)), "\n",
              (M["subtitle_ar"], dict(size=13, color=GOLD)), "\n", (" ", dict(size=60)), "\n",
              (M["agency_ar"], dict(size=15, bold=True, color=IVORY)), "\n",
              ("PRICES IN RUB · SAR CONVERSION AT 21.4", dict(size=8, color=GOLD, rtl=False))], align="center")
c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
page_break()

# ------------------------------------------------------------------ about page
par(doc, [("قبل أن تبدأ", dict(size=19, bold=True, color=NAVY))], after=0)
par(doc, [("About this catalogue", dict(size=13, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=4)
par(doc, ["جميع الأسعار مأخوذة كما وردت من العميل بالروبل الروسي، ولليلة الواحدة ما لم يُذكر خلاف ذلك، ومحوّلة إلى الريال السعودي آلياً. السعر بالريال هو الرقم الأبرز في كل صف، والسعر بالروبل بجانبه للمراجعة."], after=8, line=1.4)
heading("سعر الصرف وطريقة التحويل", "Exchange rate", size=11.5, before=2)
x = doc.add_table(rows=1, cols=1); table_rtl(x); cell_margins(x, 120, 120, 200)
xc = x.rows[0].cells[0]; shade(xc, NAVY)
cell_text(xc, [("1 SAR = 21.4 RUB", dict(size=20, bold=True, color=GOLD, rtl=False)), "\n",
               ("السعر بالريال = السعر بالروبل ÷ 21.4 · تُقرَّب النتيجة إلى منزلتين عشريتين · سعر الصرف ثابت كما حدده العميل · لا عمولة ولا هامش ربح ولا أي زيادة · السعر الأصلي بالروبل معروض للمراجعة.", dict(size=10, color=IVORY))], align="center")
heading("حالة الإفطار والإشغال", "Breakfast & occupancy", size=11.5, before=10)
lg = [("مع الإفطار", "السعر يشمل الإفطار", "With breakfast"), ("بدون إفطار", "سعر الغرفة فقط", "Without breakfast"),
      ("مع إفطار لشخص", "يشمل إفطار شخص واحد", "With breakfast for 1"), ("مع إفطار لشخصين", "يشمل إفطار شخصين", "With breakfast for 2"),
      ("شخص واحد / مفردة", "إشغال شخص واحد أو غرفة مفردة", "1 person / Single"), ("شخصان / مزدوجة", "إشغال شخصين أو غرفة مزدوجة", "2 persons / Double"),
      ("ثلاثة أشخاص", "إشغال ثلاثة أشخاص", "3 persons"), ("غير مذكور", "لم يذكر المصدر ذلك", "Not stated in the source"),
      ("فترة منتهية", "فترة انتهت قبل 15 نوفمبر 2026، معروضة كما وردت", "Period ended — shown as supplied")]
lt = doc.add_table(rows=len(lg), cols=3); table_rtl(lt); borders(lt); cell_margins(lt, 30, 30, 80)
for i, (a, bdesc, en) in enumerate(lg):
    cell_text(lt.rows[i].cells[0], [(a, dict(size=9.5, bold=True, color=NAVY))])
    cell_text(lt.rows[i].cells[1], [(bdesc, dict(size=9.5))])
    cell_text(lt.rows[i].cells[2], [(en, dict(size=8.5, color=MUTED, rtl=False))], align="left")
widths(lt, [45, 75, 54])
heading("فهرس الفنادق", "Index", size=11.5, before=10)
par(doc, [("أرقام الصفحات تخص نسخة PDF؛ في ملف Word تبدأ كل منشأة بصفحة جديدة بالترتيب نفسه.", dict(size=9, color=MUTED))], after=3)
import json
PM = json.loads((WORK / "pagemap.json").read_text(encoding="utf-8"))
k = 0
idx_rows = []
for city in L.CITY_ORDER:
    for h_ in L.hotels(city):
        k += 1
        idx_rows.append((f"{k:02d}", h_["name_ar"], h_["name_en"], M["cities"][city]["ar"], str(PM["hotels"][h_["id"]])))
for a in L.analyses():
    idx_rows.append((f"A{a['n']}", a["title_ar"], a["title_en"], "التحليل", str(PM["analysis"][a["key"]])))
idx_rows.append(("N", "ملاحظات للتأكيد والشروط العامة", "Notes & terms", "", str(PM["notes"])))
it = doc.add_table(rows=len(idx_rows) + 1, cols=5); table_rtl(it); borders(it); cell_margins(it, 20, 20, 70)
hdr_cells(it, [("#", "No."), ("الاسم", "Name"), ("English", "English"), ("القسم", "Section"), ("صفحة PDF", "PDF page")], num_idx=(4,))
for i, r in enumerate(idx_rows, 1):
    cells = it.rows[i].cells
    cell_text(cells[0], [(r[0], dict(size=9.5, color=GOLDTXT, font=DISP_FONT, rtl=False))])
    cell_text(cells[1], [(r[1], dict(size=10))])
    cell_text(cells[2], [(r[2], dict(size=8.5, color=MUTED, rtl=False))], align="left")
    cell_text(cells[3], [(r[3], dict(size=9, color=MUTED))])
    cell_text(cells[4], [(r[4], dict(size=10, color=NAVY, font=DISP_FONT, rtl=False))], align="left")
widths(it, [12, 62, 52, 26, 22])


# ------------------------------------------------------------------ hotels
def hotel_section(h, n):
    page_break()
    city = M["cities"][h["city"]]
    t = doc.add_table(rows=1, cols=2); table_rtl(t); cell_margins(t, 120, 120, 200)
    a, b_ = t.rows[0].cells
    shade(a, NAVY); shade(b_, NAVY)
    stars_txt = (L.stars_ar(h["stars"]) + " (وفق المصدر)") if h.get("stars") else "تصنيف النجوم غير مذكور في المصدر"
    cell_text(a, [(f"N° {n:02d}", dict(size=8.5, color=GOLD, font=DISP_FONT, rtl=False)), "\n",
                  (h["name_ar"], dict(size=19, bold=True, color=IVORY)), "\n",
                  (h["name_en"], dict(size=13, color=GOLD, font=DISP_FONT, rtl=False)), "\n",
                  (stars_txt, dict(size=9.5, color="E9E3D6"))])
    cell_text(b_, [(city["en"].upper(), dict(size=10, color=GOLD, font=DISP_FONT, rtl=False)), "\n", (city["ar"], dict(size=11, color=IVORY))], align="center")
    widths(t, [130, 44])
    facts = [f for f in h["facts_ar"] if "نجوم" not in f or "اقتصادي" in f]
    if facts:
        par(doc, [(" · ".join(facts), dict(size=10))], before=6, after=2)
    vals = []
    for p in h["periods"]:
        vals.append(p["dates_ar"] if not p.get("date_line_nos") else f'{p["label_ar"]}: {p["dates_ar"]}')
    par(doc, [("الصلاحية: ", dict(size=10, bold=True, color=NAVY)), (" · ".join(vals), dict(size=10))], before=2, after=6, line=1.35)
    heading("ملاحظات الحجز", "Booking notes", size=12, before=4)
    bullets(h["booking_notes_ar"])
    # extras
    heading("الإضافات ورسوم الأطفال", "Extras & children", size=12, before=8)
    if not h["extras"]:
        par(doc, [("لم يذكر المصدر أي إضافات لهذا الفندق.", dict(size=10))])
    else:
        et = doc.add_table(rows=len(h["extras"]) + 1, cols=4); table_rtl(et); borders(et); cell_margins(et)
        hdr_cells(et, [("البند", "Item"), ("الشرط", "Condition"), ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR")], sar_idx=3, num_idx=(2, 3))
        for i, x in enumerate(h["extras"], 1):
            row = et.rows[i]; cant_split(row)
            cell_text(row.cells[0], [(x["item_ar"], dict(size=10))])
            cell_text(row.cells[1], [(x["condition_ar"], dict(size=9.5))])
            if x["rub"] is not None:
                cell_text(row.cells[2], rub_parts(x["rub"]), align="left", rtl=False)
                cell_text(row.cells[3], sar_parts(x["sar"]), align="left", rtl=False); shade(row.cells[3], IVORY)
            else:
                m = row.cells[2].merge(row.cells[3])
                cell_text(m, [(x["value_ar"], dict(size=10, bold=True, color=NAVY))], align="center"); shade(m, IVORY)
        widths(et, [47, 68, 27, 32])
    # periods
    for p in h["periods"]:
        status = L.period_status(p)
        parts = [(p["label_ar"], dict(size=12.5, bold=True, color=NAVY)), ("   ", dict(size=10)), (p["label_en"], dict(size=10, color=GOLDTXT, font=DISP_FONT, rtl=False)),
                 ("   |   ", dict(size=10, color=GOLD, rtl=False)), (p["dates_ar"], dict(size=10))]
        if status == "ended":
            parts += [("   ", dict(size=9)), ("فترة منتهية — تُعرض كما وردت", dict(size=8.5, color="7A2E2E"))]
        par(doc, parts, before=10, after=3, keep=True)
        nrows = sum(len(r["rows"]) for r in p["rooms"])
        tt = doc.add_table(rows=nrows + 1, cols=5); table_rtl(tt); borders(tt); cell_margins(tt, 40, 40, 90)
        hdr_cells(tt, [("نوع الغرفة", "Room type"), ("الإشغال", "Occupancy"), ("الإفطار", "Breakfast"), ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR")], sar_idx=4, num_idx=(3, 4))
        ri = 1
        for r in p["rooms"]:
            start = ri
            for x in r["rows"]:
                row = tt.rows[ri]; cant_split(row)
                cell_text(row.cells[1], [(x["occupancy_ar"], dict(size=10, color=MUTED if x["occupancy"] == "not stated" else CHAR))])
                cell_text(row.cells[2], [(x["breakfast_ar"], dict(size=10, color=MUTED if x["breakfast"] == "not stated" else CHAR))])
                cell_text(row.cells[3], rub_parts(x["rub"]), align="left", rtl=False)
                cell_text(row.cells[4], sar_parts(x["sar"]), align="left", rtl=False); shade(row.cells[4], IVORY)
                ri += 1
            mc = tt.rows[start].cells[0]
            if ri - 1 > start:
                mc = mc.merge(tt.rows[ri - 1].cells[0])
            sub = L.room_sub_ar(r)
            cell_text(mc, [(r["name"], dict(size=10, bold=True, color=NAVY, rtl=False))] + (["\n", (sub, dict(size=9, color=MUTED))] if sub else []))
            shade(mc, "FCFBF8")
        widths(tt, [52, 30, 33, 27, 32])


n = 0
for ci, city in enumerate(L.CITY_ORDER):
    c = M["cities"][city]
    page_break()
    par(doc, [(" ", dict(size=60))], after=0)
    par(doc, [(f"SECTION 0{ci+1}", dict(size=10, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=0)
    par(doc, [(c["ar"], dict(size=40, bold=True, color=NAVY))], after=0)
    par(doc, [(c["en"].upper(), dict(size=22, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=10)
    for h_ in L.hotels(city):
        par(doc, [(h_["name_ar"], dict(size=11)), ("   ", dict(size=10)), (h_["name_en"], dict(size=10, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=2)
    cnt = len(L.hotels(city))
    par(doc, [(f'{L.ar_count(cnt, "فنادق", "فندقاً", "فندقان")} في هذا القسم، بترتيب ورودها في المصدر.', dict(size=9.5, color=MUTED))], before=6)
    for h_ in L.hotels(city):
        n += 1
        hotel_section(h_, n)

# ------------------------------------------------------------------ analysis
WID = {"hotel": 40, "room": 34, "basis": 32, "pbasis": 36, "breakfast": 34, "rub": 27, "sar": 31, "note": 24, "condition": 60}


def an_table(t):
    cols = t["cols"]
    kind = t.get("kind")
    ws = [WID[c] for c in cols]
    scale = 174 / sum(ws)
    ws = [w * scale for w in ws]
    tb = doc.add_table(rows=max(1, len(t["rows"])) + 1, cols=len(cols)); table_rtl(tb); borders(tb); cell_margins(tb, 35, 35, 80)
    hdr_cells(tb, [L.COLS[c] for c in cols], sar_idx=cols.index("sar"), num_idx=tuple(i for i, c in enumerate(cols) if c in ("rub", "sar")))
    if not t["rows"]:
        cell_text(tb.rows[1].cells[0], [("لا توجد صفوف تطابق هذا الأساس.", dict(size=10))])
    for i, r in enumerate(t["rows"], 1):
        row = tb.rows[i]; cant_split(row)
        for j, c in enumerate(cols):
            cell = row.cells[j]
            if c == "hotel":
                cell_text(cell, [(r["hotel_ar"], dict(size=10)), "\n", (r["hotel_en"], dict(size=8, color=MUTED, rtl=False))])
            elif c == "room":
                rs = r["room_ar"].split(" — ", 1)
                cell_text(cell, [(rs[0], dict(size=10, bold=True, color=NAVY, rtl=False))] + (["\n", (rs[1], dict(size=9, color=MUTED))] if len(rs) > 1 else []))
            elif c == "basis":
                cell_text(cell, [(r["occupancy_ar"], dict(size=9.5)), "\n", (r["breakfast_ar"], dict(size=9.5))])
            elif c == "pbasis":
                cell_text(cell, [(r["period_short_ar"], dict(size=9.5, bold=True, color=NAVY)), "\n", (f'{r["occupancy_ar"]} · {r["breakfast_ar"]}', dict(size=9.5))])
            elif c == "breakfast":
                cell_text(cell, [(r["breakfast_ar"], dict(size=10))])
            elif c == "note":
                cell_text(cell, [(r.get("note_ar") or "", dict(size=9))])
            elif c == "condition":
                cell_text(cell, [(r["condition_ar"], dict(size=9.5))])
            elif c == "rub":
                if r["rub"] is not None:
                    cell_text(cell, rub_parts(r["rub"]), align="left", rtl=False)
            elif c == "sar":
                if r["sar"] is not None:
                    cell_text(cell, sar_parts(r["sar"]), align="left", rtl=False); shade(cell, IVORY)
        if r.get("rub") is None and "rub" in cols:
            m = row.cells[cols.index("rub")].merge(row.cells[cols.index("sar")])
            cell_text(m, [(r.get("value_ar") or "", dict(size=10, bold=True, color=NAVY))], align="center"); shade(m, IVORY)
    widths(tb, ws)


for a in L.analyses():
    page_break()
    par(doc, [(f"ANALYSIS {a['n']:02d}", dict(size=9, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=0)
    par(doc, [(a["title_ar"], dict(size=17, bold=True, color=NAVY)), ("   ", dict(size=12)), (a["title_en"], dict(size=12.5, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=4)
    bx = doc.add_table(rows=1, cols=1); table_rtl(bx); cell_margins(bx, 100, 100, 160)
    bc = bx.rows[0].cells[0]; shade(bc, IVORY)
    parts = [("أساس المقارنة", dict(size=9.5, bold=True, color=NAVY))]
    for bl in a["basis_ar"]:
        parts += ["\n", ("•  " + bl, dict(size=9.5))]
    cell_text(bc, parts)
    for t in a["tables"]:
        par(doc, [(t["caption_ar"], dict(size=10.5, bold=True, color=NAVY)), ("   ", dict(size=9)), (t["caption_en"], dict(size=8.5, color=MUTED, rtl=False))], before=10, after=3, keep=True)
        an_table(t)

# ------------------------------------------------------------------ notes
page_break()
par(doc, [("NOTES FOR CONFIRMATION", dict(size=9, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=0)
par(doc, [("ملاحظات للتأكيد", dict(size=17, bold=True, color=NAVY)), ("   ", dict(size=12)), ("Notes for confirmation", dict(size=12.5, color=GOLDTXT, font=DISP_FONT, rtl=False))], after=2)
par(doc, [("نقاط في بيانات المصدر عُرضت كما وردت وتحتاج إلى تأكيد.", dict(size=10, color=MUTED))], after=6)
for a in [x for x in D["anomalies"] if x.get("print", True)]:
    par(doc, [(a["id"] + "   ", dict(size=10, color=GOLDTXT, font=DISP_FONT, rtl=False)), (a["ar"], dict(size=10))], after=4, line=1.4)
heading("الشروط العامة", "General terms", size=12, before=10)
bullets(D["general_terms"]["ar"])

doc.core_properties.title = "RUSSIA HOTEL COLLECTION 2026 — " + M["title_ar"]
doc.core_properties.author = M["agency_ar"]
doc.core_properties.comments = "Fonts needed: IBM Plex Sans Arabic, Montserrat, Playfair Display (SIL OFL 1.1). Generated from data/rates.json."
doc.save(OUT)
print("wrote", OUT.name)
