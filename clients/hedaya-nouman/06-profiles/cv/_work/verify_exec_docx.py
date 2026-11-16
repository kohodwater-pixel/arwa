#!/usr/bin/env python3
"""Checks the executive DOCX files against the approved executive PDFs (which are only read, never written)."""
import hashlib, pathlib, re, subprocess, sys, unicodedata, zipfile
import docx, pymupdf
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_cv as B

CV, W = B.OUT, B.OUT / "_work"
MARKS = re.compile("[‎‏‪-‮⁦-⁩﻿]")
TOKEN = re.compile("[A-Za-z0-9]+|[ء-ي]+")
qn = docx.oxml.ns.qn
ok_all = True


def words(t):
    t = MARKS.sub("", unicodedata.normalize("NFKC", t)).casefold()
    return ["".join(sorted(w)) for w in TOKEN.findall(t)]


def pdftotext(pdf, *flags):
    return subprocess.run(["pdftotext", *flags, str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def pages(pdf):
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))


def pdf_fonts(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
    return sorted({l.split()[0].split("+")[-1] for l in out})


def docx_paragraphs(d):
    """All paragraphs in document order: table cells (merged cells once), then body paragraphs."""
    out, seen = [], set()
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                if id(c._tc) in seen:
                    continue
                seen.add(id(c._tc)); out += c.paragraphs
    return out + list(d.paragraphs)


def expected_exec(m):
    """Text of the executive layout in reading order, straight from the data: band, side column, main column."""
    b = m["base"]
    o = [b["name"], *m["title"], b["contact_heading"], b["city_label"], b["city"], b["nat_label"], b["nat"],
         b["phone_label"], B.PHONE, b["email_label"], B.EMAIL]
    for k in [x for x in m["order"] if x in B.SIDE_KEYS]:
        o.append(b["H"][k])
        o += b["tech"] if k == "tech" else b["langs"] if k == "lang" else [x for parts in b[k] for x in parts]
    for k in [x for x in m["order"] if x not in B.SIDE_KEYS]:
        o.append(b["H"][k])
        if k == "summary":
            o.append(m["summary"])
        elif k == "comp":
            o += [x for row in m["comp"] for x in row]
        elif k == "exp":
            for (t, e, dts), bl in B.roles(m):
                o += [t, e, dts, *bl]
        elif k == "vol":
            o += [x for parts in b["vol"] for x in parts]
    return [w for line in o for w in words(line)]


approved = dict(l.split()[::-1] for l in (W / "approved_exec_md5.txt").read_text().splitlines())
for key, m in B.MODELS.items():
    b = m["base"]; rtl = b["lang"] == "ar"
    name = B.fname(m, "executive", "docx").replace("_v02.docx", "_v03.docx")
    dx, pdf = CV / name, CV / B.fname(m, "executive", "pdf")
    lo, lo_nf = W / "exec-docx-render" / (name[:-4] + "pdf"), W / "exec-docx-render-nofonts" / (name[:-4] + "pdf")
    d = docx.Document(dx)
    ps = docx_paragraphs(d)
    text = "\n".join(p.text for p in ps)
    xml = zipfile.ZipFile(dx).read("word/document.xml").decode()
    names = zipfile.ZipFile(dx).namelist()
    band, side = round(B.BAND_MM / 25.4 * 72), round(B.SIDE_MM / 25.4 * 72)
    sx, mx = (595 - side, 0) if rtl else (0, side)
    zone = lambda f, x, y, w, h: pdftotext(f, "-x", str(x), "-y", str(y), "-W", str(w), "-H", str(h))
    pdf_words = words(zone(pdf, 0, 0, 595, band) + zone(pdf, sx, band, side, 842 - band) + zone(pdf, mx, band, 595 - side, 842 - band))
    dw = words(text)
    lot = MARKS.sub("", pdftotext(lo))
    c = {}
    c["approved PDF and its HTML unchanged (md5)"] = all(
        hashlib.md5((CV / f).read_bytes()).hexdigest() == approved[f] for f in (pdf.name, pdf.name[:-3] + "html"))
    exp = expected_exec(m)
    c[f"python-docx re-read: every word of the source data, in reading order ({len(dw)} words)"] = dw == exp
    c["approved PDF carries exactly the same words (pdftotext by zone)"] = sorted(pdf_words) == sorted(exp)
    c["e-mail and phone present as plain text"] = B.EMAIL in text and B.PHONE in text
    c["one layout table; no text boxes, drawings, pictures or floating shapes"] = (
        len(d.tables) == 1 and len(d.inline_shapes) == 0 and not re.search(r"w:txbxContent|w:drawing|w:pict|mc:AlternateContent|v:shape", xml)
        and not any(n.startswith("word/media") for n in names))
    c["no bidi control characters"] = not MARKS.search(xml)
    fam = "Tajawal" if rtl else "IBM Plex Sans"
    runs = [r for p in ps for r in p.runs]
    c[f"font named in every run: {fam}"] = all(r._r.rPr.rFonts.get(qn("w:ascii")) == fam and r._r.rPr.rFonts.get(qn("w:cs")) == fam for r in runs)
    odttf = [n for n in names if n.endswith(".odttf")]
    c[f"fonts embedded in the package: {len(odttf)} files (regular + bold), embedTrueTypeFonts set"] = (
        len(odttf) == 2 and "embedTrueTypeFonts" in zipfile.ZipFile(dx).read("word/settings.xml").decode())
    cp = d.core_properties
    c[f"core properties: author = name, title set, description empty, created {cp.created:%Y-%m-%d}"] = (
        cp.author == b["name"] and cp.title.startswith(b["name"]) and not cp.comments and cp.created.year == 2026)
    if rtl:
        ar = re.compile("[؀-ۿ]")
        c["table is w:bidiVisual; section is bidi"] = "<w:bidiVisual/>" in xml and "<w:bidi/>" in xml.split("<w:sectPr")[-1]
        nb = [p for p in ps if p.text.strip() and (p._p.pPr is None or p._p.pPr.find(qn("w:bidi")) is None)]
        c["every text paragraph is w:bidi, except the phone and e-mail values (left-to-right, set right)"] = (
            sorted(p.text for p in nb) == sorted([B.PHONE, B.EMAIL]))
        c["every run with Arabic letters has w:rtl"] = all(r._r.rPr.find(qn("w:rtl")) is not None for r in runs if ar.search(r.text))
        c["LibreOffice render: Arabic date ranges read «يونيو 2022 إلى ديسمبر 2026» and «2016 إلى 2017»"] = all(
            contains for contains in [any(words(x) == words(l)[-len(words(x)):] or " ".join(words(x)) in " ".join(words(l)) for l in lot.splitlines())
                                      for x in (b["hospital"][2], b["school"][2])])
    c[f"LibreOffice render (fonts installed): pages = {pages(lo)}, fonts {', '.join(pdf_fonts(lo))}"] = pages(lo) == 1
    c[f"LibreOffice render (fonts NOT installed, embedded fonts only): pages = {pages(lo_nf)}, fonts {', '.join(pdf_fonts(lo_nf))}"] = (
        pages(lo_nf) == 1 and all(re.match("Tajawal|IBMPlexSans", f) for f in pdf_fonts(lo_nf)))
    lw = sorted(words(lot))
    c["LibreOffice render: same words as the approved PDF (nothing clipped or lost)"] = lw == sorted(exp)
    if lw != sorted(exp):
        import collections
        a, e2 = collections.Counter(lw), collections.Counter(exp)
        print("      render-only:", list((a - e2).elements()), " missing:", list((e2 - a).elements()))
    c["LibreOffice render: phone reads +966 54 093 0121"] = B.PHONE in lot
    pg = pymupdf.open(lo)[0]
    low = max(x[3] for x in pg.get_text("blocks")) / 72 * 25.4
    def slack(f):   # white space left on the page under the layout table = how much it can grow before page 2
        g = pymupdf.open(f)[0]
        return 297 - max(dr["rect"].y1 for dr in g.get_drawings() if dr.get("fill")) / 72 * 25.4
    s1, s2 = slack(lo), slack(lo_nf)
    c[f"LibreOffice render: lowest text at {low:.0f} mm; vertical slack under the table {s1:.1f} mm (fonts installed), {s2:.1f} mm (embedded only)"] = min(s1, s2) >= 7
    hl = re.findall(r'<w:hyperlink r:id="(rId\d+)"', xml)
    rels = zipfile.ZipFile(dx).read("word/_rels/document.xml.rels").decode()
    c["e-mail is a real mailto hyperlink (external relationship)"] = len(hl) == 1 and f'Target="mailto:{B.EMAIL}"' in rels and 'TargetMode="External"' in rels
    rules = re.findall(r'w:lineRule="(\w+)"', xml)
    c[f"line heights: {rules.count('atLeast')} paragraphs at-least, {rules.count('exact')} exact (rules, spacers, closing paragraph)"] = rules.count("atLeast") > 40
    bad = [k for k, v in c.items() if not v]
    ok_all &= not bad
    print(("PASS  " if not bad else "FAIL  ") + name)
    for k, v in c.items():
        print(f'      [{"ok" if v else "XX"}] {k}')
    # side-by-side: approved PDF (left) and LibreOffice render of the DOCX (right)
    ims = []
    for f in (pdf, lo, lo_nf):
        px = pymupdf.open(f)[0].get_pixmap(dpi=62)
        ims.append(Image.frombytes("RGB", (px.width, px.height), px.samples))
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 24, max(i.height for i in ims)), "#888888")
    x = 0
    for im in ims:
        sheet.paste(im, (x, 0)); x += im.width + 12
    sheet.save(W / "check-png" / f'compare_exec_pdf-vs-docx-v03_{m["slug"]}_{b["lang"]}.png')
    print()
print("ALL PASS" if ok_all else "SOME CHECKS FAILED")
