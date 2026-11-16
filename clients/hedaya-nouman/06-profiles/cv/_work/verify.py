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


FORBIDDEN = ["1994", "متزوجة", "married", "Opera", "PMS", "الجنسية", "Nationality", "Saudi national", "40%"]

for key, m in B.MODELS.items():
    b = m["base"]
    rtl = b["lang"] == "ar"
    exp = expected_lines(m)
    exp_words = [w for line in exp for w in words(line)]
    heads = [b["H"][k] for k in m["order"]]

    # ---------------- ATS PDF ----------------
    pdf = CV / B.fname(m, "ats", "pdf")
    plain, layout = pdftotext(pdf), pdftotext(pdf, "-layout")
    fl, emb = fonts(pdf)
    c = {}
    c[f"pages = {pdfinfo(pdf)} (max 2)"] = pdfinfo(pdf) <= 2
    c[f"fonts embedded, intended only: {', '.join(fl)}"] = emb and all(re.match("Tajawal|IBMPlexSans", f) for f in fl)
    c["pdftotext plain: complete text, logical reading order (word-for-word sequence)"] = words(plain) == exp_words
    c["pdftotext -layout: complete text, logical reading order"] = words(layout) == exp_words
    pos = [plain.find(unicodedata.normalize("NFKC", h)) for h in heads] if not rtl else None
    if rtl:
        pw = words(plain)
        c["section headings intact and in order"] = all(contains(pw, words(h)) for h in heads)
    else:
        c["section headings intact and in order"] = all(p >= 0 for p in pos) and pos == sorted(pos)
    c["email extractable"] = B.EMAIL in plain and B.EMAIL in layout
    c["phone extractable"] = B.PHONE in MARKS.sub("", plain) and B.PHONE in MARKS.sub("", layout)
    c["no replacement/garbage characters"] = "�" not in plain and not re.search(r"[-]", plain)
    c["no forbidden items (birth year, marital status, nationality, hotel systems)"] = not any(f in plain for f in FORBIDDEN)
    if rtl:
        c["year range extracts as 2016 – 2017"] = "2016 – 2017" in MARKS.sub("", plain)
    report(pdf.name, c)

    # ---------------- ATS DOCX ----------------
    dx = CV / B.fname(m, "ats", "docx")
    d = docx.Document(dx)
    paras = [MARKS.sub("", p.text) for p in d.paragraphs if p.text.strip()]
    xml = zipfile.ZipFile(dx).read("word/document.xml").decode("utf8")
    c = {}
    c["python-docx re-read equals the expected lines exactly, same order"] = paras == exp
    c["no tables / images / text boxes / shapes / columns"] = (
        len(d.tables) == 0 and len(d.inline_shapes) == 0
        and not re.search(r"w:txbxContent|w:drawing|w:pict|<w:cols [^>]*w:num=\"[2-9]", xml))
    c["header and footer empty"] = all(not p.text.strip() for s in d.sections for p in (*s.header.paragraphs, *s.footer.paragraphs))
    st = [p.style.name for p in d.paragraphs]
    c["heading styles: 1 x Heading 1 (name), 7 x Heading 2 (sections), 3 x Heading 3 (roles)"] = (
        st.count("Heading 1"), st.count("Heading 2"), st.count("Heading 3")) == (1, 7, 3)
    c["real bullet lists (List Bullet style)"] = st.count("List Bullet") == sum(len(x[1]) for x in B.roles(m)) + 10
    c["section headings match"] = [p.text for p in d.paragraphs if p.style.name == "Heading 2"] == heads
    c["email and phone present"] = any(B.EMAIL in p for p in paras) and any(B.PHONE in p for p in paras)
    c["font named in every run: Arial (ascii, hAnsi, cs)"] = all(
        r._r.rPr.rFonts.get(docx.oxml.ns.qn("w:cs")) == "Arial" and r.font.name == "Arial" for p in d.paragraphs for r in p.runs)
    if rtl:
        c["every paragraph has w:bidi"] = all(p._p.pPr is not None and p._p.pPr.find(docx.oxml.ns.qn("w:bidi")) is not None for p in d.paragraphs)
        ar = re.compile("[؀-ۿ]")
        c["every run with Arabic letters has w:rtl"] = all(
            r._r.rPr.find(docx.oxml.ns.qn("w:rtl")) is not None for p in d.paragraphs for r in p.runs if ar.search(r.text))
        c["no explicit w:jc (start edge = right in a bidi paragraph)"] = "<w:jc " not in xml
        c["section is bidi"] = "<w:bidi/>" in xml.split("<w:sectPr")[-1]
    c["no forbidden items"] = not any(f in "\n".join(paras) for f in FORBIDDEN)
    report(dx.name, c)

    # LibreOffice render of the DOCX (verification only)
    lo = CV / "_work" / "docx-render" / B.fname(m, "ats", "pdf")
    c = {f"LibreOffice opens it, pages = {pdfinfo(lo)}": pdfinfo(lo) <= 2,
         "LibreOffice render: same word sequence as expected": words(pdftotext(lo)) == exp_words}
    report("  (LibreOffice render of the DOCX) " + lo.name, c)

    # ---------------- Executive PDF ----------------
    pdf = CV / B.fname(m, "executive", "pdf")
    # zone by zone (header, side column, main column): default pdftotext reads across both columns
    side_x = 370 if rtl else 0
    main_x = 0 if rtl else 225
    zone = lambda x, y, w, h: pdftotext(pdf, "-x", str(x), "-y", str(y), "-W", str(w), "-H", str(h))
    plain = zone(0, 0, 595, 119) + zone(side_x, 119, 225, 723) + zone(main_x, 119, 370, 723)
    pw = words(plain, fold=True)
    fl, emb = fonts(pdf)
    phrases = []
    for line in exp:
        if B.EMAIL in line:
            phrases += [b["city"], B.PHONE, B.EMAIL]
        elif line in (" | ".join(m["comp"]), " | ".join(b["langs"])):
            phrases += line.split(" | ")
        elif line == m["title"]:
            phrases.append(line)
        else:
            phrases += line.split(" | ")
    missing = [p for p in phrases if not contains(pw, words(p, fold=True))]
    c = {}
    c[f"pages = {pdfinfo(pdf)}"] = pdfinfo(pdf) == 1
    c[f"fonts embedded, intended only: {', '.join(fl)}"] = emb and all(re.match("Tajawal|IBMPlexSans", f) for f in fl)
    c[f"pdftotext by zone (header, side, main): every phrase of the ATS content extractable ({len(phrases) - len(missing)}/{len(phrases)})"] = not missing
    c["no extra words beyond the content, the contact captions and the Contact heading"] = (
        len(pw) == len(exp_words) + len(words(b["contact_heading"])) + len(words(b["city_label"])))
    c["email and phone extractable"] = B.EMAIL in plain and B.PHONE in MARKS.sub("", plain)
    c["no forbidden items"] = not any(f in plain for f in FORBIDDEN)
    report(pdf.name, c)
    if missing:
        print("      missing:", missing)
    print()

print("ALL PASS" if ok_all else "SOME CHECKS FAILED")
sys.exit(0 if ok_all else 1)
