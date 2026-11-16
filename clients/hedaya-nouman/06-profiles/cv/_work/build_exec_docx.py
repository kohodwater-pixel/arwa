#!/usr/bin/env python3
"""Editable Word versions of the approved Executive Modern CVs (v02).

Same data as the approved PDFs (imported from build_cv.py; nothing here changes the PDFs or their HTML).
Layout = one borderless layout table: teal band row, then tinted side column + main column.
Spacer columns are used instead of cell paddings so the geometry is identical when the table is
mirrored for Arabic (w:bidiVisual). No text boxes, no floating shapes, no images.

Run: python3 _work/build_exec_docx.py
"""
import datetime
import pathlib
import re
import shutil
import sys
import uuid
import zipfile

from docx import Document
from PIL import ImageFont
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Mm, Pt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_cv as B

REPO = B.OUT.parents[3]
FONT_FILES = {
    "Tajawal": {"Regular": REPO / "assets/fonts/tajawal/Tajawal-Regular.ttf", "Bold": REPO / "assets/fonts/tajawal/Tajawal-Bold.ttf"},
    "IBM Plex Sans": {"Regular": REPO / "assets/fonts/ibmplexsans-static/IBMPlexSans-Regular.ttf",
                      "Bold": REPO / "assets/fonts/ibmplexsans-static/IBMPlexSans-Bold.ttf"},
}
TEAL, SAND, SANDL, TINT = B.TEAL, B.SAND, B.SAND_LIGHT, "F5F1E8"
INK, MUTED, WHITE, TAG_LINE, TAG_TEXT = "20282B", "566266", "FFFFFF", "9DB7BA", "184A52"
# column grid in mm: outer margin, side content, tinted gap, white gap, main content, outer margin
GRID = [13, 41, 4, 7, 132, 13]
BAND_MM, BODY_MM = 33, 262.5
NBSP = "\u00a0"
BOXED_TAGS = {"en": True, "ar": False}   # competencies as boxed tags (True) or as middle-dot lines (False)


def tw(mm):
    return str(int(round(mm / 25.4 * 1440)))


class Doc:
    def __init__(self, m):
        self.m, self.b = m, m["base"]
        self.rtl = self.b["lang"] == "ar"
        self.font = "Tajawal" if self.rtl else "IBM Plex Sans"
        self.body = (10, 16.0) if self.rtl else (9.5, 13.8)   # size pt, exact line pt (as in the PDF)

    # ---- low level -------------------------------------------------------------------------
    def run(self, p, text, size, bold=False, color=INK, rtl=None, caps=False, track=0, box=False, underline=None):
        # hyphens inside Latin words (Al-Ahmadi, front-desk) are Word's own non-breaking hyphen, so the
        # word stays on one line as in the approved PDF; it is still read back and copied as "-"
        segs = re.split(r"(?<=[A-Za-z])-(?=[A-Za-z])", text)
        r = p.add_run(segs[0])
        for seg in segs[1:]:
            r._r.append(OxmlElement("w:noBreakHyphen"))
            t = OxmlElement("w:t"); t.text = seg
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            r._r.append(t)
        rpr = r._r.get_or_add_rPr()
        f = OxmlElement("w:rFonts")
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            f.set(qn(a), self.font)
        rpr.append(f)
        for tag in ("w:b", "w:bCs"):
            e = OxmlElement(tag); e.set(qn("w:val"), "1" if bold else "0"); rpr.append(e)
        if caps:
            rpr.append(OxmlElement("w:caps"))
        c = OxmlElement("w:color"); c.set(qn("w:val"), color); rpr.append(c)
        if track:
            s = OxmlElement("w:spacing"); s.set(qn("w:val"), str(track)); rpr.append(s)
        for tag in ("w:sz", "w:szCs"):
            e = OxmlElement(tag); e.set(qn("w:val"), str(int(round(size * 2)))); rpr.append(e)
        if underline:
            u = OxmlElement("w:u"); u.set(qn("w:val"), "thick"); u.set(qn("w:color"), underline); rpr.append(u)
        if box:
            bd = OxmlElement("w:bdr")
            for a, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "2"), ("w:color", TAG_LINE)):
                bd.set(qn(a), v)
            rpr.append(bd)
        is_rtl = self.rtl if rtl is None else rtl
        if is_rtl:
            rpr.append(OxmlElement("w:rtl"))
        lang = OxmlElement("w:lang")
        lang.set(qn("w:val"), "en-GB")
        if is_rtl:
            lang.set(qn("w:bidi"), "ar-SA")
        rpr.append(lang)
        return r

    def text(self, p, text, size, **kw):
        """Arabic text: Latin words, digits, e-mail and phone go into left-to-right runs."""
        if not self.rtl:
            return self.run(p, text, size, **kw)
        pos = 0
        for mt in B.LATIN_CHUNK.finditer(text):
            if mt.start() > pos:
                self.run(p, text[pos:mt.start()], size, rtl=True, **kw)
            self.run(p, mt.group(0), size, rtl=False, **kw)
            pos = mt.end()
        if pos < len(text):
            self.run(p, text[pos:], size, rtl=True, **kw)

    def par(self, cell, line, before=0, after=0, keep=False, ltr_right=False):
        """New paragraph in a cell with exact line height (pt), like the CSS line boxes of the PDF."""
        ps = cell.paragraphs
        if len(ps) == 1 and not ps[0].runs:   # the empty paragraph every new cell starts with
            p = ps[0]
        else:
            p = cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before, pf.space_after = Pt(before), Pt(after)
        pf.line_spacing = Pt(line)
        pf.keep_with_next = keep
        ppr = p._p.get_or_add_pPr()
        if self.rtl and not ltr_right:
            ppr.insert_element_before(OxmlElement("w:bidi"), *B.PPR_ORDER[B.PPR_ORDER.index("w:bidi") + 1:])
        elif self.rtl and ltr_right:
            jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "right")
            ppr.insert_element_before(jc, *B.PPR_ORDER[B.PPR_ORDER.index("w:jc") + 1:])
        return p

    # ---- components ------------------------------------------------------------------------
    def heading(self, cell, text, width, first=False):
        gap = 11 if self.rtl else 12.2
        if self.rtl:
            p = self.par(cell, 17.1, before=0 if first else gap, keep=True)
            self.text(p, text, 11.8, bold=True, color=TEAL)
        else:
            p = self.par(cell, 12.8, before=0 if first else gap, keep=True)
            self.run(p, text, 8.8, bold=True, color=TEAL, caps=True, track=14)
        # short sand accent bar: an empty paragraph whose bottom border is cut to 9 mm by its end indent
        # (in a right-to-left paragraph w:right is the trailing edge, so the bar stays at the start side)
        bar = self.par(cell, 2.5, after=5.6 if self.rtl else 6.6, keep=True)
        self.run(bar, "", 1)
        ppr = bar._p.get_or_add_pPr()
        bd = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="0" w:color="{SAND}"/></w:pBdr>')
        ppr.insert_element_before(bd, *B.PPR_ORDER[B.PPR_ORDER.index("w:pBdr") + 1:])
        ind = parse_xml(f'<w:ind {nsdecls("w")} w:right="{tw(width - 9)}"/>')
        ppr.insert_element_before(ind, *B.PPR_ORDER[B.PPR_ORDER.index("w:ind") + 1:])

    def bullets(self, cell, items):
        for x in items:
            p = self.par(cell, self.body[1], after=1.1)
            ppr = p._p.get_or_add_pPr()
            num = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="{self.num_id}"/></w:numPr>')
            ppr.insert_element_before(num, *B.PPR_ORDER[B.PPR_ORDER.index("w:numPr") + 1:])
            ppr.append(parse_xml(f'<w:rPr {nsdecls("w")}><w:color w:val="{SAND}"/></w:rPr>'))
            self.text(p, x, self.body[0])

    def build(self, path):
        m, b, rtl = self.m, self.b, self.rtl
        H = b["H"]
        size, line = self.body
        doc = Document()
        sec = doc.sections[0]
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Mm(0)
        sec.header_distance = sec.footer_distance = Mm(0)
        if rtl:
            sec._sectPr.append(OxmlElement("w:bidi"))
        normal = doc.styles["Normal"]
        normal.font.name = self.font
        rf = normal.element.get_or_add_rPr().find(qn("w:rFonts"))
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), self.font)
        normal.paragraph_format.space_after = Pt(0)

        # sand bullets: one numbering definition (no drawing, real list)
        numbering = doc.part.numbering_part.element
        absn = parse_xml(
            f'<w:abstractNum {nsdecls("w")} w:abstractNumId="90"><w:multiLevelType w:val="hybridMultilevel"/>'
            f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/>'
            f'<w:pPr><w:ind w:left="{tw(4)}" w:hanging="{tw(3.2)}"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}" w:hint="default"/>'
            f'<w:color w:val="{SAND}"/></w:rPr></w:lvl></w:abstractNum>')
        first_num = numbering.find(qn("w:num"))
        first_num.addprevious(absn) if first_num is not None else numbering.append(absn)
        numbering.append(parse_xml(f'<w:num {nsdecls("w")} w:numId="90"><w:abstractNumId w:val="90"/></w:num>'))
        self.num_id = 90

        # ---- layout table ----
        t = doc.add_table(rows=2, cols=6)
        tblpr = t._tbl.tblPr
        for child in list(tblpr):
            tblpr.remove(child)
        xml = (f'<w:tblW {nsdecls("w")} w:w="{tw(210)}" w:type="dxa"/>',
               f'<w:tblInd {nsdecls("w")} w:w="0" w:type="dxa"/>',
               f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>',
               f'<w:tblCellMar {nsdecls("w")}><w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>'
               f'<w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>')
        if rtl:
            tblpr.append(OxmlElement("w:bidiVisual"))
        for x in xml:
            tblpr.append(parse_xml(x))
        for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), GRID):
            gc.set(qn("w:w"), tw(w))

        def cellfmt(cell, width, fill=None, top=0, bottom=0, valign=None, bottom_rule=False):
            tcpr = cell._tc.get_or_add_tcPr()
            for child in list(tcpr):
                if child.tag != qn("w:gridSpan"):
                    tcpr.remove(child)
            tcw = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{tw(width)}" w:type="dxa"/>')
            tcpr.insert(0, tcw)
            if bottom_rule:
                tcpr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="13" w:space="0" w:color="{SAND}"/></w:tcBorders>'))
            if fill:
                tcpr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill}"/>'))
            tcpr.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{tw(top)}" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>'
                                  f'<w:bottom w:w="{tw(bottom)}" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>'))
            if valign:
                tcpr.append(parse_xml(f'<w:vAlign {nsdecls("w")} w:val="{valign}"/>'))

        def spacer(cell):
            p = self.par(cell, 1)
            self.run(p, "", 1)

        r0, r1 = t.rows
        r0.height, r0.height_rule = Mm(BAND_MM), WD_ROW_HEIGHT_RULE.EXACTLY
        r1.height, r1.height_rule = Mm(BODY_MM), WD_ROW_HEIGHT_RULE.AT_LEAST
        for r in (r0, r1):
            r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        band = r0.cells[0].merge(r0.cells[5])
        cellfmt(band, sum(GRID), TEAL, valign="center", bottom_rule=True)
        fills = [TINT, TINT, TINT, None, None, None]
        for i, c in enumerate(r1.cells):
            cellfmt(c, GRID[i], fills[i], top=6.5, bottom=4)
            if i not in (1, 4):
                spacer(c)
        side, main = r1.cells[1], r1.cells[4]

        # ---- band ----
        def inset(p):   # same indent on both sides: no left/right ambiguity when mirrored
            ind = parse_xml(f'<w:ind {nsdecls("w")} w:left="{tw(GRID[0])}" w:right="{tw(GRID[0])}"/>')
            p._p.get_or_add_pPr().insert_element_before(ind, *B.PPR_ORDER[B.PPR_ORDER.index("w:ind") + 1:])
            return p

        p = inset(self.par(band, 36.5 if rtl else 31))
        self.text(p, b["name"], 28 if rtl else 27, bold=True, color=WHITE)
        p = inset(self.par(band, 18.3 if rtl else 16.7, before=0.5 if rtl else 4))
        self.text(p, m["title"][0], 12.2 if rtl else 11.5, color=SANDL)
        for extra in m["title"][1:]:
            p = inset(self.par(band, 16.5 if rtl else 15.2))
            self.text(p, extra, 11 if rtl else 10.5, color=WHITE)

        # ---- side column ----
        cap = (9, 13.5) if rtl else (8.5, 11.5)
        small = (9.2, 14.7) if rtl else (8.8, 12.8)
        self.heading(side, b["contact_heading"], GRID[1], first=True)
        contact = [(b["city_label"], b["city"], False), (b["nat_label"], b["nat"], False),
                   (b["phone_label"], B.PHONE, True), (b["email_label"], B.EMAIL, True)]
        for i, (label, value, latin) in enumerate(contact):
            p = self.par(side, cap[1], keep=True)
            self.text(p, label, cap[0], color=MUTED)
            # phone and e-mail: a left-to-right paragraph set to the right, so the digits can never reorder
            p = self.par(side, line, after=0 if i == 3 else 5.4, ltr_right=latin)
            if latin:
                # let the e-mail use the tinted gap beside the column instead of wrapping
                side_attr = "w:left" if rtl else "w:right"
                ind = parse_xml(f'<w:ind {nsdecls("w")} {side_attr}="-{tw(GRID[2] - 0.5)}"/>')
                p._p.get_or_add_pPr().insert_element_before(ind, *B.PPR_ORDER[B.PPR_ORDER.index("w:ind") + 1:])
                self.run(p, value, size, rtl=False)
            else:
                self.text(p, value, size)
        for k in [x for x in m["order"] if x in B.SIDE_KEYS]:
            self.heading(side, H[k], GRID[1])
            if k == "tech":
                for i, x in enumerate(b["tech"]):
                    p = self.par(side, line, after=0 if i == len(b["tech"]) - 1 else 5.4)
                    self.text(p, x, size)
            elif k in ("edu", "train"):
                for i, parts in enumerate(b[k]):
                    last = i == len(b[k]) - 1
                    p = self.par(side, line, keep=True, after=0 if len(parts) > 1 or last else 6.5)
                    self.text(p, parts[0], size)
                    if len(parts) > 1:
                        p = self.par(side, small[1], after=0 if last else 6.5)
                        self.text(p, " | ".join(parts[1:]), small[0], color=MUTED)
            elif k == "lang":
                for i, x in enumerate(b["langs"]):
                    p = self.par(side, line, after=0 if i == len(b["langs"]) - 1 else 5.4)
                    self.text(p, x, size)

        # ---- main column ----
        first = True
        for k in [x for x in m["order"] if x not in B.SIDE_KEYS]:
            self.heading(main, H[k], GRID[4], first=first)
            first = False
            if k == "summary":
                p = self.par(main, line)
                self.text(p, m["summary"], size)
            elif k == "comp":
                self.competencies(main)
            elif k == "exp":
                for j, ((title, org, dates), bl) in enumerate(B.roles(m)):
                    p = self.par(main, 17.6 if rtl else 15.2, before=0 if j == 0 else (5.7 if rtl else 7), keep=True)
                    self.text(p, title, 11 if rtl else 10.5, bold=True)
                    p = self.par(main, line, after=2.6, keep=True)
                    ppr = p._p.get_or_add_pPr()
                    tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:pos="{tw(GRID[4])}"/></w:tabs>')
                    ppr.insert_element_before(tabs, *B.PPR_ORDER[B.PPR_ORDER.index("w:tabs") + 1:])
                    self.text(p, org, size, color=TEAL)
                    self.run(p, "\t", size)
                    self.text(p, dates, small[0], color=MUTED)
                    self.bullets(main, bl)
            elif k == "vol":
                for i, parts in enumerate(b["vol"]):
                    p = self.par(main, line, after=0 if i == len(b["vol"]) - 1 else (3.1 if rtl else 4.8))
                    self.text(p, parts[0], size, bold=True)
                    self.text(p, " | " + " | ".join(parts[1:]), size, color=MUTED)

        # a table cannot be the last thing in a Word document: one 1 pt paragraph closes it
        tail = doc.add_paragraph()
        tail.paragraph_format.line_spacing = Pt(1)
        tail.paragraph_format.space_before = tail.paragraph_format.space_after = Pt(0)
        self.run(tail, "", 1)

        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None)
        cp = doc.core_properties
        cp.title = f'{b["name"]} | {m["title"][0]}'
        cp.author = cp.last_modified_by = b["name"]
        cp.comments = cp.subject = cp.keywords = cp.category = ""
        cp.created = cp.modified = now
        cp.revision = 1
        cp.language = "ar-SA" if rtl else "en-GB"
        doc.save(path)

    def competencies(self, cell):
        """English: tags — each competency is a real-text run with a thin box border (w:bdr); words inside a
        tag are joined by no-break spaces so a tag never splits across lines.
        Arabic: run borders break apart around right-to-left text when rendered, so the competencies are set
        as middle-dot lines instead; rows are packed by measured width so no separator hangs at a line end."""
        items = [x for row in self.m["comp"] for x in row]
        if BOXED_TAGS[self.b["lang"]]:
            p = self.par(cell, 20)
            for i, x in enumerate(items):
                self.run(p, NBSP + x.replace(" ", NBSP) + NBSP, 8.7, color=TAG_TEXT, box=True)
                if i < len(items) - 1:
                    self.run(p, "  ", 8.7)
            return
        size, line = self.body
        font = ImageFont.truetype(str(FONT_FILES[self.font]["Regular"]), 100)
        width = lambda t: font.getlength(t) / 100 * size / 72 * 25.4   # mm
        rows, cur = [], []
        for x in items:
            if cur and width(" · ".join(cur + [x])) > GRID[4] - 8:
                rows.append(cur); cur = []
            cur.append(x)
        rows.append(cur)
        for i, row in enumerate(rows):
            p = self.par(cell, line, after=0 if i == len(rows) - 1 else 1.5)
            for j, x in enumerate(row):
                self.text(p, x, size)
                if j < len(row) - 1:
                    self.run(p, " · ", size, bold=True, color="A8873F")


# ---- font embedding (ECMA-376 obfuscated fonts, written straight into the package) --------------
def obfuscate(data, guid):
    key = bytes.fromhex(guid.replace("-", ""))[::-1]
    head = bytes(data[i] ^ key[i % 16] for i in range(32))
    return head + data[32:]


def embed_fonts(path, family):
    src = zipfile.ZipFile(path)
    parts = {n: src.read(n) for n in src.namelist()}
    src.close()
    parts.pop("docProps/thumbnail.jpeg", None)   # python-docx template leftover: not our content
    parts["_rels/.rels"] = re.sub(rb'<Relationship [^>]*thumbnail[^>]*/>', b"", parts["_rels/.rels"])
    rels, fonts_xml = [], []
    for i, (style, tag) in enumerate((("Regular", "embedRegular"), ("Bold", "embedBold")), 1):
        guid = str(uuid.uuid4()).upper()
        parts[f"word/fonts/font{i}.odttf"] = obfuscate(FONT_FILES[family][style].read_bytes(), guid)
        rels.append(f'<Relationship Id="rIdF{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{i}.odttf"/>')
        fonts_xml.append(f'<w:{tag} r:id="rIdF{i}" w:fontKey="{{{guid}}}"/>')
    parts["word/_rels/fontTable.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>").encode()
    ft = parts["word/fontTable.xml"].decode()
    ft = ft.replace("</w:fonts>", f'<w:font w:name="{family}"><w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
                    + "".join(fonts_xml) + "</w:font></w:fonts>")
    parts["word/fontTable.xml"] = ft.encode()
    st = parts["word/settings.xml"].decode()
    st = re.sub(r"(<w:zoom [^>]*/>)", r"\1<w:embedTrueTypeFonts/>", st, count=1)
    assert "<w:embedTrueTypeFonts/>" in st
    parts["word/settings.xml"] = st.encode()
    ct = parts["[Content_Types].xml"].decode()
    ct = ct.replace('<Default Extension="rels"', '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default Extension="rels"')
    parts["[Content_Types].xml"] = ct.encode()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", parts.pop("[Content_Types].xml"))
        for n, d in parts.items():
            z.writestr(n, d)


if __name__ == "__main__":
    for key, m in B.MODELS.items():
        d = Doc(m)
        out = B.OUT / B.fname(m, "executive", "docx")
        d.build(out)
        embed_fonts(out, d.font)
        print("built", out.name)
    # fallback fonts beside the files, with their licences
    fdir = B.OUT / "fonts"
    for fam, sub in (("Tajawal", "tajawal"), ("IBM Plex Sans", "ibmplexsans-static")):
        (fdir / sub).mkdir(parents=True, exist_ok=True)
        for f in FONT_FILES[fam].values():
            shutil.copy2(f, fdir / sub / f.name)
        shutil.copy2(f.parent / "OFL.txt", fdir / sub / "OFL.txt")
