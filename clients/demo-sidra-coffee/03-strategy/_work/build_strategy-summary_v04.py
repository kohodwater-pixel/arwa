#!/usr/bin/env python3
"""Build the Sidra Coffee strategy summary HTML from its Markdown source.
pandoc (gfm -> html5 fragment, no title block), then direction handling for Arabic.
Usage: build_strategy.py <source.md> <out.html>
"""
import re, subprocess, sys
from bs4 import BeautifulSoup, NavigableString

src, out = sys.argv[1], sys.argv[2]
body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none", src],
                      check=True, capture_output=True).stdout.decode("utf-8")
soup = BeautifulSoup(body, "html.parser")

AR = r"؀-ۿݐ-ݿ"
ar_letter = re.compile(r"[ء-يٮ-ۓ]")
ar_any = re.compile(f"[{AR}]")
lat_letter = re.compile(r"[A-Za-z]")
# an Arabic run inside Latin text: a guillemet-quoted phrase, or bare Arabic words
run = re.compile(f"«[^«»]*[{AR}][^«»]*»|[{AR}](?:[{AR}\\s،؛؟]*[{AR}])?")
NAME = "سدرة للقهوة"
name_re = re.compile(f"«{NAME}»|{NAME}")


def is_arabic(el):
    t = el.get_text()
    a, l = len(ar_letter.findall(t)), len(lat_letter.findall(t))
    if a == 0 and l == 0:
        return bool(ar_any.search(t))      # Arabic punctuation only
    return a > l


def split_strings(el, regex, make):
    for s in list(el.find_all(string=True)):
        text = str(s)
        if not regex.search(text):
            continue
        parts, pos = [], 0
        for m in regex.finditer(text):
            if m.start() > pos:
                parts.append(NavigableString(text[pos:m.start()]))
            parts.append(make(m.group(0)))
            pos = m.end()
        if pos < len(text):
            parts.append(NavigableString(text[pos:]))
        for p in parts:
            s.insert_before(p)
        s.extract()


def nw(text):
    t = soup.new_tag("span", attrs={"class": "nw"})
    t.string = text
    return t


def bdi(text):
    cls = "ar-in nw" if len(text.split()) <= 3 else "ar-in"
    t = soup.new_tag("bdi", attrs={"lang": "ar", "dir": "rtl", "class": cls})
    t.string = text
    return t


def mark_ar(el, cls="ar"):
    el["dir"] = "rtl"
    el["lang"] = "ar"
    el["class"] = (el.get("class") or []) + [cls]


# strip pandoc's own column widths and inline styles
for cg in soup.find_all("colgroup"):
    cg.decompose()
for el in soup.find_all(style=True):
    del el["style"]

blocks = []
for bq in soup.find_all("blockquote"):
    blocks.append(bq)
for el in soup.find_all(["p", "li", "td", "th", "h1", "h2", "h3"]):
    if el.find_parent("blockquote"):
        continue
    blocks.append(el)

for el in blocks:
    if not el.get_text(strip=True):
        continue
    if is_arabic(el):
        mark_ar(el)
        if el.name == "blockquote":
            for p in el.find_all("p"):
                mark_ar(p)
        split_strings(el, name_re, nw)
    else:
        split_strings(el, run, bdi)

# tables: column widths, all-Arabic tables read from the right, Arabic columns get right-aligned heads
WIDTHS = [
    [16, 42, 42],            # audience
    [15, 51, 34],            # competitors
    [14, 14, 21, 21, 30],    # personality
    [38, 16, 46],            # values
    [10, 43, 37, 10],        # key messages
    [38, 42, 20],            # held lines
    [8, 33, 39, 20],         # Arabic do / don't
    [10, 30, 38, 22],        # English do / don't
    [18, 41, 41],            # vocabulary
    [25, 10, 65],            # risks
    [26, 74],                # verified / assumed
]
tables = soup.find_all("table")
assert len(tables) == len(WIDTHS), len(tables)
for t, widths in zip(tables, WIDTHS):
    rows = t.find_all("tr")
    assert all(len(r.find_all(["td", "th"])) == len(widths) for r in rows)
    cg = soup.new_tag("colgroup")
    for w in widths:
        cg.append(soup.new_tag("col", attrs={"style": f"width:{w}%"}))
    t.insert(0, cg)
    cells = [c for c in t.find_all(["td", "th"]) if c.get_text(strip=True)]
    if all("ar" in (c.get("class") or []) for c in cells):
        t["dir"] = "rtl"
        t["lang"] = "ar"
        t["class"] = ["ar-table"]
    else:
        body_rows = t.find("tbody").find_all("tr")
        heads = t.find("thead").find_all("th")
        for i, th in enumerate(heads):
            col = [r.find_all("td")[i] for r in body_rows]
            col = [c for c in col if c.get_text(strip=True)]
            if col and all("ar" in (c.get("class") or []) for c in col):
                th["class"] = (th.get("class") or []) + ["ar-col"]

# title block: H1 on the left, Arabic name on the right, one bar row
h1 = soup.find("h1").extract()
name_p = soup.find("p")
assert NAME in name_p.get_text()
name_p.extract()
name_p["class"] = ["ar", "name"]
note = soup.find("blockquote").extract()   # system-test notice
note["class"] = ["notice"]
meta = soup.find("ul").extract()
meta["class"] = ["meta"]

# keep each section heading with what follows; keep label paragraphs with their quote or table
content = soup.decode(formatter="minimal")

LOGO = "assets/logo/demo-sidra-coffee_logo_bilingual-colour_ar-en_v01.svg"
html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<title>Sidra Coffee: brand strategy summary</title>
<!--
  Sidra Coffee brand strategy summary, A4 screen PDF, English with Arabic. v04.
  SYSTEM TEST, fictional client. Colours and type ladder follow 04-identity/03-system/system.md (A4 document ladder).
  Text: demo-sidra-coffee_brand-strategy_summary_en_v04.md, wording unchanged.
  Export: node scripts/html2pdf.cjs <this file> <same name>.pdf --size A4
  Self-contained: fonts (SIL OFL, OFL.txt beside each family) and the logo load from ./assets/ next to this file.
  Arabic: every Arabic block carries dir="rtl" lang="ar"; Arabic inside English lines is isolated with <bdi>.
-->
<style>
@font-face {{ font-family: "IBM Plex Sans Arabic"; font-weight: 400; src: url("assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans Arabic"; font-weight: 500; src: url("assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Medium.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans Arabic"; font-weight: 600; src: url("assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans Arabic"; font-weight: 700; src: url("assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans"; font-weight: 400; src: url("assets/fonts/ibmplexsans-static/IBMPlexSans-Regular.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans"; font-weight: 500; src: url("assets/fonts/ibmplexsans-static/IBMPlexSans-Medium.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans"; font-weight: 600; src: url("assets/fonts/ibmplexsans-static/IBMPlexSans-SemiBold.ttf"); }}
@font-face {{ font-family: "IBM Plex Sans"; font-weight: 700; src: url("assets/fonts/ibmplexsans-static/IBMPlexSans-Bold.ttf"); }}

@page {{ size: A4; margin: 17mm 17mm 19mm; background: #F3ECE0;
  @bottom-center {{ content: counter(page, decimal-leading-zero); font-family: "IBM Plex Sans", Arial, sans-serif; font-weight: 600; font-size: 8pt; color: #1F1B18; }}
}}
:root {{
  --paper: #F3ECE0; --crema: #E3C9A0; --ink: #1F1B18; --ember: #C23A20; --ash: #6F6861;
  --ar: "IBM Plex Sans Arabic", "IBM Plex Sans", "Noto Sans Arabic", Tahoma, sans-serif;
  --en: "IBM Plex Sans", "IBM Plex Sans Arabic", "Helvetica Neue", Arial, sans-serif;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; background: var(--paper); }}
body {{ color: var(--ink); background: var(--paper); font-family: var(--en); font-size: 10pt; line-height: 1.45; font-weight: 400; }}
strong {{ font-weight: 600; }}

/* ---------- Arabic: 1.15 x the Latin size, more line height, never tracked ---------- */
.ar {{ font-family: var(--ar); font-size: 1.15em; line-height: 1.75; direction: rtl; text-align: right; letter-spacing: 0; }}
.ar .ar {{ font-size: 1em; }}
.ar-in {{ font-family: var(--ar); font-size: 1.15em; letter-spacing: 0; line-height: 1; }}
.nw {{ white-space: nowrap; }}

/* ---------- title block (page 1 only) ---------- */
.top {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.top img {{ height: 25mm; display: block; }}
.top .cap {{ font-size: 6.5pt; line-height: 1.4; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: var(--ash); }}
.bars {{ display: grid; grid-template-columns: repeat(7, 1fr); column-gap: calc(100% / 41); direction: ltr; height: 12mm; margin-top: 10mm; }}
.bars i {{ background: var(--ink); display: block; }}
.bars i:nth-child(4) {{ background: var(--ember); }}
.titles {{ display: flex; justify-content: space-between; align-items: baseline; gap: 8mm; margin-top: 8mm; padding-bottom: 5mm; border-bottom: 2px solid var(--ink); }}
h1 {{ font-size: 28pt; line-height: 1.1; font-weight: 700; letter-spacing: -0.015em; max-width: 110mm; }}
.name {{ font-size: 18.5pt; line-height: 1.5; font-weight: 500; white-space: nowrap; }}
.notice {{ margin-top: 5mm; background: var(--crema); padding: 3mm 4mm; font-size: 8.5pt; line-height: 1.45; }}
.meta {{ list-style: none; margin-top: 5mm; display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 6mm; row-gap: 2mm; font-size: 8.5pt; line-height: 1.45; }}
.meta li:nth-child(4) {{ grid-column: 1 / span 3; }}
.meta li:nth-child(5) {{ grid-column: 1 / span 3; }}
.meta strong {{ display: block; font-size: 6.5pt; line-height: 1.4; text-transform: uppercase; letter-spacing: 0.12em; color: var(--ash); }}

/* ---------- running text ---------- */
main > p, main > ul, main > ol {{ margin-top: 3mm; }}
main > p:first-child {{ margin-top: 5mm; font-size: 8.5pt; }}
h2 {{ font-size: 16pt; line-height: 1.3; font-weight: 500; margin-top: 9mm; padding-top: 3mm; border-top: 2px solid var(--ink); break-after: avoid; }}
p, li {{ orphans: 3; widows: 3; }}
ul, ol {{ padding-left: 5mm; }}
main li + li {{ margin-top: 1.5mm; }}
p:has(+ blockquote), p:has(+ table), p:has(+ ul), p:has(+ ol) {{ break-after: avoid; }}

/* ---------- quotations: each language in its own block ---------- */
blockquote {{ margin-top: 3mm; padding: 1mm 0 1mm 4mm; border-left: 2px solid var(--ink); font-size: 12pt; line-height: 1.4; font-weight: 500; break-inside: avoid; }}
blockquote.ar {{ padding: 1mm 4mm 1mm 0; border-left: 0; border-right: 2px solid var(--ink); font-size: 13.8pt; line-height: 1.75; }}
blockquote + blockquote {{ break-before: avoid; margin-top: 2mm; }}
blockquote.notice {{ border: 0; padding: 3mm 4mm; font-size: 8.5pt; line-height: 1.45; font-weight: 400; }}

/* ---------- tables: kept together, fixed columns ---------- */
table {{ width: 100%; table-layout: fixed; border-collapse: collapse; margin-top: 4mm; font-size: 8.5pt; line-height: 1.45; break-inside: avoid; border-bottom: 2px solid var(--ink); }}
th, td {{ text-align: left; vertical-align: top; padding: 1.8mm 2mm 1.8mm 0; }}
th {{ font-size: 6.5pt; line-height: 1.4; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: var(--ash); border-top: 2px solid var(--ink); border-bottom: 2px solid var(--ink); vertical-align: bottom; }}
td {{ text-wrap: pretty; }}
.ar-table td {{ text-wrap: balance; }}
tbody tr + tr td {{ border-top: 0.5pt solid var(--ink); }}
td.ar, th.ar {{ text-align: right; padding: 1.2mm 5mm 1.2mm 2mm; }}
.ar-table td, .ar-table th {{ padding: 1.2mm 0 1.2mm 4mm; }}
th.ar-col {{ text-align: right; padding: 1.8mm 5mm 1.8mm 2mm; }}
th.ar {{ font-size: 7.5pt; line-height: 1.6; font-weight: 600; text-transform: none; letter-spacing: 0; }}
td:last-child:not(.ar), th:last-child:not(.ar) {{ padding-right: 0; }}
</style>
</head>
<body>
<header>
  <div class="top">
    <img src="{LOGO}" alt="Sidra Coffee logo">
    <p class="cap">Brand strategy</p>
  </div>
  <div class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="titles">
    {h1.decode(formatter="minimal")}
    {name_p.decode(formatter="minimal")}
  </div>
  {note.decode(formatter="minimal")}
  {meta.decode(formatter="minimal")}
</header>
<main>
{content.strip()}
</main>
</body>
</html>
"""
assert "�" not in html
open(out, "w", encoding="utf-8").write(html)
print("tables:", len(tables), "| rtl blocks:", html.count('dir="rtl" lang="ar"') + html.count('lang="ar" dir="rtl"'),
      "| bdi:", html.count("<bdi"), "| rtl tables:", html.count('class="ar-table"'))
