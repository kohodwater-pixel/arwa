#!/usr/bin/env python3
"""Verification of the CV set against the single source in build_cv.py.

ATS PDFs : pdftotext (plain and -layout) must give the full text in logical order.
DOCX     : python-docx re-read must equal the expected lines exactly; structure checks.
Executive: every expected phrase must be extractable (order differs: side column first).

Arabic note: pdftotext writes the lam-alef ligature in visual order (e.g. "األحمدي" for
"الأحمدي") for every Arabic PDF, whatever the font or the producing tool. Words are therefore
compared with their letters sorted, which still proves word content and word ORDER.
"""
import pathlib
import re
import subprocess
import sys
import unicodedata
import zipfile

import docx

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_cv as B

CV = B.OUT
MARKS = re.compile("[‎‏‪-‮⁦-⁩﻿]")
ok_all = True


TOKEN = re.compile("[A-Za-z0-9]+|[\u0621-\u064a]+")


def words(text, fold=False):
    """Word tokens (Latin/digit runs and Arabic-letter runs), letters sorted inside each token.
    pdftotext moves spaces and punctuation around bidi boundaries, so those are not compared."""
    t = MARKS.sub("", unicodedata.normalize("NFKC", text))
    if fold:
        t = t.casefold()
    return ["".join(sorted(w)) for w in TOKEN.findall(t)]


def expected_lines(m):
    out = []
    for line in B.md_cv(m).splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^\*\*(.*)\*\*$", r"\1", line)
        line = re.sub(r"^\*(.*)\*$", r"\1", line)
        line = re.sub(r"^- ", "", line)
        out.append(line)
    return out


def contains(hay, needle):
    n = len(needle)
    return any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))


def pdftotext(pdf, *flags):
    return subprocess.run(["pdftotext", *flags, str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def pdfinfo(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


def fonts(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
    return sorted({l.split()[0].split("+")[-1] for l in out}), all(" yes " in l[40:] for l in out)


def report(name, checks):
    global ok_all
    bad = [k for k, v in checks.items() if not v]
    ok_all &= not bad
    print(f'{"PASS" if not bad else "FAIL"}  {name}')
    for k, v in checks.items():
        print(f'      [{"ok" if v else "XX"}] {k}')


FORBIDDEN = ["1994", "متزوجة", "married", "Opera", "PMS", "40%", "Guest Relations", "علاقات الضيوف", "warm welcome",
             "busy service environments", "Guests of Allah", "العمل الإرشادي", "Student Guidance", "LinkedIn", "‎", "‏"]
import pymupdf
W = docx.oxml.ns.qn

for key, m in B.MODELS.items():
    b = m["base"]
    rtl = b["lang"] == "ar"
    exp = expected_lines(m)
    exp_words = [w for line in exp for w in words(line)]
    heads = [b["H"][k] for k in m["order"]]
    brk = b["H"][B.PAGE_BREAK_BEFORE[key]]

    # ---------------- ATS PDF ----------------
    pdf = CV / B.fname(m, "ats", "pdf")
    plain, layout = pdftotext(pdf), pdftotext(pdf, "-layout")
    fl, emb = fonts(pdf)
    n = pdfinfo(pdf)
    c = {}
    c[f"pages = {n} (max 2)"] = n <= 2
    if n == 2:
        p2 = words(pdftotext(pdf, "-f", "2", "-l", "2"))
        c[f"page 2 starts with a section heading and its content ({brk})"] = p2[:len(words(brk))] == words(brk) and len(p2) > 25
    c[f"fonts embedded, intended only: {', '.join(fl)}"] = emb and all(re.match("Tajawal|IBMPlexSans", f) for f in fl)
    c["pdftotext plain: complete text, logical reading order (band included)"] = words(plain) == exp_words
    c["pdftotext -layout: complete text, logical reading order"] = words(layout) == exp_words
    if rtl:
        pw = words(plain)
        c["section headings intact"] = all(contains(pw, words(h)) for h in heads)
    else:
        pos = [plain.find(h) for h in heads]
        c["section headings intact and in order"] = all(p >= 0 for p in pos) and pos == sorted(pos)
    c["email extractable"] = B.EMAIL in plain and B.EMAIL in layout
    c["phone extractable"] = B.PHONE in MARKS.sub("", plain) and B.PHONE in MARKS.sub("", layout)
    c["email is a mailto link"] = any(l.get("uri") == "mailto:" + B.EMAIL for l in pymupdf.open(pdf)[0].get_links())
    c["no replacement/garbage characters"] = "�" not in plain and not re.search(r"[-]", plain)
    c["no withdrawn or forbidden wording"] = not any(f in plain for f in FORBIDDEN[:-2])
    report(pdf.name, c)

    # ---------------- ATS DOCX ----------------
    dx = CV / B.fname(m, "ats", "docx")
    d = docx.Document(dx)
    paras = [p.text for p in d.paragraphs if p.text.strip()]
    xml = zipfile.ZipFile(dx).read("word/document.xml").decode("utf8")
    c = {}
    c["python-docx re-read equals the expected lines exactly, same order"] = paras == exp
    c["no tables / images / text boxes / shapes / columns"] = (
        len(d.tables) == 0 and len(d.inline_shapes) == 0
        and not re.search(r"w:txbxContent|w:drawing|w:pict|mc:AlternateContent|<w:cols [^>]*w:num=\"[2-9]", xml))
    c["header and footer empty"] = all(not p.text.strip() for s in d.sections for p in (*s.header.paragraphs, *s.footer.paragraphs))
    st = [p.style.name for p in d.paragraphs]
    c["heading styles: 1 x Heading 1 (name), 8 x Heading 2 (sections), 3 x Heading 3 (roles)"] = (
        st.count("Heading 1"), st.count("Heading 2"), st.count("Heading 3")) == (1, 8, 3)
    c["real bullet lists (List Bullet style)"] = st.count("List Bullet") == sum(len(x[1]) for x in B.roles(m)) + 10
    c["section headings match"] = [p.text for p in d.paragraphs if p.style.name == "Heading 2"] == heads
    nband = 1 + len(m["title"]) + 2
    shaded = [p._p.pPr is not None and p._p.pPr.find(W("w:shd")) is not None for p in d.paragraphs]
    c[f"header band = paragraph shading on the first {nband} paragraphs only (name, title, contact)"] = (
        all(shaded[:nband]) and not any(shaded[nband:]))
    c["section rules = paragraph bottom border on the 8 section headings"] = all(
        p._p.pPr.find(W("w:pBdr")) is not None for p in d.paragraphs if p.style.name == "Heading 2")
    c["email and phone present"] = any(B.EMAIL in p for p in paras) and any(B.PHONE in p for p in paras)
    c["no bidi control characters anywhere (no U+200E)"] = not MARKS.search(xml)
    c["font named in every run: Arial (ascii, hAnsi, cs)"] = all(
        r._r.rPr.rFonts.get(W("w:cs")) == "Arial" and r.font.name == "Arial" for p in d.paragraphs for r in p.runs)
    cp = d.core_properties
    c[f"core properties: author = name, title set, description empty, created {cp.created:%Y-%m-%d}"] = (
        cp.author == b["name"] and cp.title.startswith(b["name"]) and not cp.comments and cp.created.year == 2026
        and cp.modified == cp.created)
    if rtl:
        c["every paragraph has w:bidi"] = all(p._p.pPr is not None and p._p.pPr.find(W("w:bidi")) is not None for p in d.paragraphs)
        ar = re.compile("[؀-ۿ]")
        c["every run with Arabic letters has w:rtl"] = all(
            r._r.rPr.find(W("w:rtl")) is not None for p in d.paragraphs for r in p.runs if ar.search(r.text))
        c["no explicit w:jc (start edge = right in a bidi paragraph)"] = "<w:jc " not in xml
        c["section is bidi"] = "<w:bidi/>" in xml.split("<w:sectPr")[-1]
    c["page break before: " + brk] = [p.text for p in d.paragraphs if p.paragraph_format.page_break_before] == [brk]
    c["no withdrawn or forbidden wording"] = not any(f in "\n".join(paras) for f in FORBIDDEN)
    report(dx.name, c)

    lo = CV / "_work" / "docx-render" / B.fname(m, "ats", "pdf")
    lot = pdftotext(lo)
    c = {f"LibreOffice opens it, pages = {pdfinfo(lo)}": pdfinfo(lo) == 2,
         "LibreOffice render: same word sequence as expected": words(lot) == exp_words,
         "LibreOffice render: phone reads +966 54 093 0121": B.PHONE in MARKS.sub("", lot)}
    report("  (LibreOffice render of the DOCX) " + lo.name, c)

    # ---------------- Executive PDF ----------------
    pdf = CV / B.fname(m, "executive", "pdf")
    band, side = round(B.BAND_MM / 25.4 * 72), round(B.SIDE_MM / 25.4 * 72)
    side_x, main_x = (595 - side, 0) if rtl else (0, side)
    zone = lambda x, y, w, h: pdftotext(pdf, "-x", str(x), "-y", str(y), "-W", str(w), "-H", str(h))
    plain = zone(0, 0, 595, band) + zone(side_x, band, side, 842 - band) + zone(main_x, band, 595 - side, 842 - band)
    pw = words(plain, fold=True)
    fl, emb = fonts(pdf)
    cl = B.contact_lines(b)
    phrases = [ph for line in exp if line not in cl for ph in re.split(r" \| | · |: ", line)]
    phrases += [b["city"], b["nat_label"], b["nat"], b["phone_label"], B.PHONE, b["email_label"], B.EMAIL]
    missing = [ph for ph in phrases if not contains(pw, words(ph, fold=True))]
    pg = pymupdf.open(pdf)[0]
    bottom = max(bl[3] for bl in pg.get_text("blocks")) / 72 * 25.4
    c = {}
    c[f"pages = {pdfinfo(pdf)}"] = pdfinfo(pdf) == 1
    c[f"fonts embedded, intended only: {', '.join(fl)}"] = emb and all(re.match("Tajawal|IBMPlexSans", f) for f in fl)
    c[f"pdftotext by zone (band, side, main): every phrase of the ATS content extractable ({len(phrases) - len(missing)}/{len(phrases)})"] = not missing
    c["nothing clipped or added: word count = content + Contact heading + location caption"] = (
        len(pw) == sum(len(words(ph)) for ph in phrases) + len(words(b["contact_heading"])) + len(words(b["city_label"])))
    c[f"lowest text at {bottom:.0f} mm of 297 (bottom margin kept)"] = bottom <= 291
    c["email and phone extractable"] = B.EMAIL in plain and B.PHONE in MARKS.sub("", plain)
    c["email is a mailto link"] = any(l.get("uri") == "mailto:" + B.EMAIL for l in pg.get_links())
    c["no withdrawn or forbidden wording"] = not any(f in plain for f in FORBIDDEN[:-2])
    report(pdf.name, c)
    if missing:
        print("      missing:", missing)
    print()

print("ALL PASS" if ok_all else "SOME CHECKS FAILED")
sys.exit(0 if ok_all else 1)
