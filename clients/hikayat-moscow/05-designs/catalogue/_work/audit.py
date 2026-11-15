#!/usr/bin/env python3
"""Automated self-audit of the Russia Hotel Collection 2026 outputs.

1. Counts hotels, periods, room types, price rows and extras in data/rates.json.
2. Re-reads the client's source file: every price row / priced extra quotes its source line
   verbatim, its RUB equals the figure on that line, and every price line is used.
3. Re-computes every SAR value with Decimal ROUND_HALF_UP.
4. Extracts prices from the generated XLSX, DOCX and PDF and proves:
   - every RUB/SAR pair in rates.json appears in each output, on the same row/line,
     in the exact order of the hotel's tables (rates and extras);
   - analysis tables use only pairs that exist in rates.json;
   - no price-formatted number appears anywhere that is not in rates.json.
   For XLSX the formulas are recalculated by LibreOffice and the recalculated values are checked.
5. Writes audit_report.md (and source_crosswalk.md for the manual line-by-line re-read).
Usage: python3 audit.py [v01]
"""
import json, re, sys, subprocess, pathlib, collections
from decimal import Decimal, ROUND_HALF_UP

WORK = pathlib.Path(__file__).resolve().parent
ROOT = WORK.parent
CLIENT = ROOT.parents[1]
V = sys.argv[1] if len(sys.argv) > 1 else "v01"
DATA = json.loads((ROOT / "data" / "rates.json").read_text(encoding="utf-8"))
SRC = (CLIENT / DATA["meta"]["source_file"]).read_text(encoding="utf-8").split("\n")
PDF = ROOT / f"hikayat-moscow_russia-hotel-collection_catalogue_ar-en_{V}.pdf"
DOCX = ROOT / f"hikayat-moscow_russia-hotel-collection_catalogue_ar-en_{V}.docx"
XLSX = ROOT / f"hikayat-moscow_russia-hotel-collection_rates_ar-en_{V}.xlsx"
PAGEMAP = json.loads((WORK / "pagemap.json").read_text(encoding="utf-8"))
RATE = Decimal("21.4")
CTRL = re.compile(r"[‎‏‪-‮⁦-⁩]")
PRICE_TOKEN = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+(?:\.\d{2})?|\d+\.\d{2})(?![\d,]|\.\d)")

problems = []
log = []


def P(msg):
    problems.append(msg)


def sar(rub):
    return str((Decimal(rub) / RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fr(rub):
    return f"{rub:,}"


def fs(s):
    return f"{Decimal(s):,.2f}"


# ------------------------------------------------------------------ 1. counts
hotels = sorted(DATA["hotels"], key=lambda h: h["order"])
n_hotels = len(hotels)
n_periods = sum(len(h["periods"]) for h in hotels)
room_types = {(h["id"], r["name"], r.get("qualifier_ar")) for h in hotels for p in h["periods"] for r in p["rooms"]}
n_room_tables = sum(len(p["rooms"]) for h in hotels for p in h["periods"])
rows = [(h, p, r, x) for h in hotels for p in h["periods"] for r in p["rooms"] for x in r["rows"]]
extras = [(h, e) for h in hotels for e in h["extras"]]
priced_extras = [(h, e) for h, e in extras if e["rub"] is not None]
by_city = collections.Counter(h["city"] for h in hotels)

# ------------------------------------------------------------------ 2. source re-check
used = collections.Counter()
for h, p, r, x in rows:
    n = x["source_line_no"]
    if SRC[n - 1] != x["source_line"]:
        P(f"source line {n} text differs from rates.json quote")
    m = re.findall(r"(\d{1,3}(?:,\d{3})+|\d+)\s*روبل", SRC[n - 1])
    if len(m) != 1 or int(m[0].replace(",", "")) != x["rub"]:
        P(f"source line {n}: RUB {x['rub']} not the figure on the line")
    used[n] += 1
for h, e in extras:
    for n, t in zip(e["source_line_nos"], e["source_lines"]):
        if SRC[n - 1] != t:
            P(f"extra source line {n} text differs")
        used[n] += 1
        if e["rub"] is not None:
            m = re.findall(r"(\d{1,3}(?:,\d{3})+|\d+)\s*روبل", SRC[n - 1])
            if len(m) != 1 or int(m[0].replace(",", "")) != e["rub"]:
                P(f"extra line {n}: RUB {e['rub']} not the figure on the line")
price_lines = [i for i in range(124, 684) if re.search(r"\d\s*روبل", SRC[i - 1])]
unused = [i for i in price_lines if i not in used]
twice = [i for i, c in used.items() if c > 1]
if unused:
    P(f"source price lines not transcribed: {unused}")
if twice:
    P(f"source lines used twice: {twice}")

# ------------------------------------------------------------------ 3. SAR recompute
sar_errors = 0
for h, p, r, x in rows:
    if sar(x["rub"]) != x["sar"]:
        sar_errors += 1; P(f"SAR mismatch {h['id']} {r['name']} {x['rub']}")
for h, e in priced_extras:
    if sar(e["rub"]) != e["sar"]:
        sar_errors += 1; P(f"SAR mismatch extra {h['id']} {e['item_en']}")

# expected sets
pairs = {(fr(x["rub"]), fs(x["sar"])) for _, _, _, x in rows} | {(fr(e["rub"]), fs(e["sar"])) for _, e in priced_extras}
rub_set = {a for a, _ in pairs}
sar_set = {b for _, b in pairs}
allowed_tokens = rub_set | sar_set


def expected_hotel_seq(h, extras_first=True):
    ex = [(fr(e["rub"]), fs(e["sar"])) for e in h["extras"] if e["rub"] is not None]
    rt = [(fr(x["rub"]), fs(x["sar"])) for p in h["periods"] for r in p["rooms"] for x in r["rows"]]
    return ex + rt if extras_first else rt + ex


results = {}

# ------------------------------------------------------------------ 4a. XLSX
from openpyxl import load_workbook
rc_dir = WORK / "xlsx_recalc"
rc_dir.mkdir(exist_ok=True)
rc = rc_dir / XLSX.name
if rc.exists():
    rc.unlink()
subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", str(rc_dir), str(XLSX)], check=True, capture_output=True)
wb = load_workbook(XLSX)              # formulas
wv = load_workbook(rc, data_only=True)  # recalculated values
x_issues = []
ws, wsv = wb["Rates"], wv["Rates"]
xrows = []
for i in range(2, ws.max_row + 1):
    rub = ws.cell(i, 17).value
    f = ws.cell(i, 18).value
    if f != f"=ROUND(Q{i}/Rate,2)":
        x_issues.append(f"Rates row {i}: SAR is not the live formula ({f})")
    val = wsv.cell(i, 18).value
    xrows.append((fr(rub), f"{Decimal(str(val)).quantize(Decimal('0.01')):,.2f}", ws.cell(i, 4).value, ws.cell(i, 10).value))
exp_rates = [(fr(x["rub"]), fs(x["sar"]), h["name_en"], r["name"]) for h, p, r, x in rows]
if xrows != exp_rates:
    diff = [(a, b) for a, b in zip(xrows, exp_rates) if a != b][:5]
    x_issues.append(f"Rates sheet sequence differs from rates.json ({len(xrows)} vs {len(exp_rates)}): {diff}")
rate_cell = wb.defined_names.get("Rate")
if not rate_cell or "Exchange!$B$4" not in rate_cell.attr_text or wb["Exchange"]["B4"].value != 21.4:
    x_issues.append("named cell Rate is not Exchange!B4 = 21.4")
ws, wsv = wb["Extras"], wv["Extras"]
xex = []
for i in range(2, ws.max_row + 1):
    rub = ws.cell(i, 10).value
    if rub is None:
        continue
    val = wsv.cell(i, 11).value
    xex.append((fr(rub), f"{Decimal(str(val)).quantize(Decimal('0.01')):,.2f}"))
exp_ex = [(fr(e["rub"]), fs(e["sar"])) for h, e in priced_extras]
if xex != exp_ex:
    x_issues.append(f"Extras sheet differs: {xex} vs {exp_ex}")
n_extras_rows_x = ws.max_row - 1
ws, wsv = wb["Analysis"], wv["Analysis"]
an_x = 0
for i in range(1, ws.max_row + 1):
    rub = ws.cell(i, 6).value
    if isinstance(rub, int):
        val = wsv.cell(i, 7).value
        pr = (fr(rub), f"{Decimal(str(val)).quantize(Decimal('0.01')):,.2f}")
        an_x += 1
        if pr not in pairs:
            x_issues.append(f"Analysis row {i}: pair {pr} not in rates.json")
# stray numbers in xlsx: any numeric cell in price columns must be a known RUB/SAR
for name, cols in (("Rates", (17, 18, 19)), ("Extras", (10, 11, 12)), ("Analysis", (6, 7))):
    for row in wv[name].iter_rows(min_row=2):
        for c in cols:
            v = row[c - 1].value
            if isinstance(v, (int, float)):
                tok = fr(int(v)) if c in (17, 10, 6) else f"{Decimal(str(v)).quantize(Decimal('0.01')):,.2f}"
                if tok not in allowed_tokens:
                    x_issues.append(f"{name}: stray price {tok}")
results["XLSX"] = dict(rate_rows=len(xrows), extras_priced=len(xex), extras_rows=n_extras_rows_x, analysis_rows=an_x, issues=x_issues)

# ------------------------------------------------------------------ 4b. DOCX
from docx import Document
d = Document(DOCX)
d_issues = []


def ctext(cell):
    return CTRL.sub("", cell.text)


def cell_price(cell, unit):
    t = ctext(cell)
    m = re.search(r"([\d,]+(?:\.\d{2})?)\s*" + unit, t)
    return m.group(1) if m else None


rate_tables, extra_tables, an_tables = [], [], []
for t in d.tables:
    hdr = " ".join(ctext(c) for c in t.rows[0].cells)
    if "السعر بالريال" not in hdr:
        continue
    seq = []
    for row in t.rows[1:]:
        cells = row.cells
        rub = sar_ = None
        seen = []
        for c in cells:
            if id(c._tc) in seen:
                continue
            seen.append(id(c._tc))
            rub = rub or cell_price(c, "RUB")
            sar_ = sar_ or cell_price(c, "SAR")
        if rub or sar_:
            seq.append((rub, sar_))
    if "الإشغال" in hdr and "نوع الغرفة" in hdr and "الفندق" not in hdr:
        rate_tables.append(seq)
    elif "البند" in hdr:
        extra_tables.append(seq)
    else:
        an_tables.append(seq)
d_rates = [p for s in rate_tables for p in s]
exp_r = [(fr(x["rub"]), fs(x["sar"])) for _, _, _, x in rows]
if d_rates != exp_r:
    d_issues.append(f"DOCX rate tables sequence differs ({len(d_rates)} vs {len(exp_r)})")
if len(rate_tables) != n_periods:
    d_issues.append(f"DOCX has {len(rate_tables)} rate tables, expected {n_periods} (one per period)")
d_ex = [p for s in extra_tables for p in s]
if d_ex != exp_ex:
    d_issues.append(f"DOCX extras differ ({len(d_ex)} vs {len(exp_ex)})")
d_an = [p for s in an_tables for p in s]
for pr in d_an:
    if pr not in pairs:
        d_issues.append(f"DOCX analysis pair {pr} not in rates.json")
# stray tokens anywhere in the docx
alltext = [CTRL.sub("", p.text) for p in d.paragraphs]
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            alltext.append(ctext(c))
for s in alltext:
    for tok in PRICE_TOKEN.findall(s):
        if tok not in allowed_tokens:
            d_issues.append(f"DOCX stray price token {tok} in: {s[:60]}")
results["DOCX"] = dict(rate_tables=len(rate_tables), rate_rows=len(d_rates), extras_priced=len(d_ex), analysis_rows=len(d_an), issues=sorted(set(d_issues)))

# ------------------------------------------------------------------ 4c. PDF
import pymupdf
doc = pymupdf.open(PDF)
p_issues = []


def page_lines(page):
    words = page.get_text("words")  # x0,y0,x1,y1,word,...
    words = [(w[0], (w[1] + w[3]) / 2, CTRL.sub("", w[4])) for w in words]
    words.sort(key=lambda w: w[1])
    lines, cur, cy = [], [], None
    for w in words:
        if cy is None or abs(w[1] - cy) <= 3.2:
            cur.append(w); cy = w[1] if cy is None else (cy + w[1]) / 2
        else:
            lines.append(cur); cur, cy = [w], w[1]
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        ln.sort(key=lambda w: w[0])
        toks = [w[2] for w in ln]
        rub = sar_ = None
        for i, t in enumerate(toks[:-1]):
            if toks[i + 1] == "RUB" and re.fullmatch(r"[\d,]+", t):
                rub = t
            if toks[i + 1] == "SAR" and re.fullmatch(r"[\d,]+\.\d{2}", t):
                sar_ = t
        out.append((toks, rub, sar_))
    return out


page_kind = {p["pn"]: p for p in PAGEMAP["plan"]}
hotel_seq = collections.defaultdict(list)
an_pairs = []
for i, page in enumerate(doc, 1):
    kind = page_kind.get(i, {})
    for toks, rub, sar_ in page_lines(page):
        line = " ".join(toks)
        for tok in PRICE_TOKEN.findall(line):
            if tok not in allowed_tokens:
                p_issues.append(f"PDF p{i}: stray price token {tok} in: {line[:70]}")
        if (rub is None) != (sar_ is None):
            p_issues.append(f"PDF p{i}: RUB/SAR not paired on one line: {line[:80]}")
            continue
        if rub is None:
            continue
        if kind.get("hotel"):
            hotel_seq[kind["hotel"]].append((rub, sar_))
        else:
            an_pairs.append((rub, sar_))
for h in hotels:
    exp = expected_hotel_seq(h, extras_first=True)
    got = hotel_seq.get(h["id"], [])
    if got != exp:
        p_issues.append(f"PDF {h['id']}: sequence differs ({len(got)} vs {len(exp)})")
for pr in an_pairs:
    if pr not in pairs:
        p_issues.append(f"PDF analysis pair {pr} not in rates.json")
pdf_rate_rows = sum(len(v) for v in hotel_seq.values())
results["PDF"] = dict(pages=doc.page_count, hotel_rows=pdf_rate_rows, analysis_rows=len(an_pairs), issues=p_issues)

# every pair present in each output
for name, seen in (("XLSX", set(xrows_p for xrows_p in [(a, b) for a, b, _, _ in xrows]) | set(xex)),
                   ("DOCX", set(d_rates) | set(d_ex)),
                   ("PDF", {pr for v in hotel_seq.values() for pr in v})):
    missing = pairs - seen
    if missing:
        results[name]["issues"].append(f"pairs missing: {sorted(missing)[:10]}")
    results[name]["distinct_pairs_found"] = len(pairs & seen)

# cross-output identity: same 189 rows in same order in all three
same = (xrows and [(a, b) for a, b, _, _ in xrows] == d_rates)
pdf_rates_only = []
for h in hotels:
    k = len([e for e in h["extras"] if e["rub"] is not None])
    pdf_rates_only += hotel_seq.get(h["id"], [])[k:]
same3 = same and pdf_rates_only == d_rates

# ------------------------------------------------------------------ crosswalk for manual re-read
cw = ["# Source ↔ rates.json crosswalk (generated by audit.py)", "",
      "Every line of the source's data block (lines 128–681) with what rates.json holds for it. Use for the line-by-line re-read.", "",
      "| Line | Source text | rates.json |", "|---|---|---|"]
mp = collections.defaultdict(list)
for h, p, r, x in rows:
    mp[x["source_line_no"]].append(f"{h['id']} · {p['key']} · {r['name']} · {x['occupancy']} · {x['breakfast']} · RUB {x['rub']} → SAR {x['sar']}")
for h, e in extras:
    for n in e["source_line_nos"]:
        mp[n].append(f"{h['id']} · EXTRA {e['kind']} · {e['item_en']} · " + (f"RUB {e['rub']} → SAR {e['sar']}" if e["rub"] is not None else e["value_en"]))
for i in range(128, 682):
    t = SRC[i - 1].strip()
    if not t:
        continue
    cw.append(f"| {i} | {t.replace('|', '/')} | {'<br>'.join(mp.get(i, [])) or '—'} |")
(WORK / "source_crosswalk.md").write_text("\n".join(cw) + "\n", encoding="utf-8")

# ------------------------------------------------------------------ report
total_issues = len(problems) + sum(len(r["issues"]) for r in results.values())
L_ = []
L_.append(f"# Audit report — Russia Hotel Collection 2026 ({V})")
L_.append("")
L_.append("Generated by `_work/audit.py` from `data/rates.json`, the client's source file and the three generated outputs. Nothing in this report is typed by hand.")
L_.append("")
L_.append(f"**Result: {'PASS — zero mismatches' if total_issues == 0 else f'FAIL — {total_issues} issue(s)'}**")
L_.append("")
L_.append("## Counts (rates.json)")
L_.append("")
L_.append("| Item | Count |")
L_.append("|---|---|")
L_.append(f"| Hotels | {n_hotels} (Moscow {by_city['moscow']}, Saint Petersburg {by_city['spb']}) |")
L_.append(f"| Validity periods (one rate table each) | {n_periods} |")
L_.append(f"| Distinct room types (hotel × room) | {len(room_types)} |")
L_.append(f"| Room blocks (room × period) | {n_room_tables} |")
L_.append(f"| Price rows | {len(rows)} |")
L_.append(f"| Extras (all) | {len(extras)} — priced {len(priced_extras)}, unpriced {len(extras) - len(priced_extras)} (free / on request / restriction / fee not stated) |")
L_.append(f"| Distinct RUB/SAR pairs | {len(pairs)} |")
L_.append(f"| Source lines with a RUB figure | {len(price_lines)} — all used exactly once |")
L_.append(f"| Anomalies listed for confirmation | {len(DATA['anomalies'])} ({sum(1 for a in DATA['anomalies'] if a.get('print', True))} printed in the catalogue, 1 internal) |")
L_.append("")
L_.append("## Checks")
L_.append("")
L_.append(f"- Source re-check (quotes verbatim, RUB equals the figure on its line, coverage): {'OK' if not problems else 'see issues'}")
L_.append(f"- SAR recomputed with Decimal ROUND_HALF_UP for {len(rows)} rows + {len(priced_extras)} priced extras: {sar_errors} mismatches")
for k_, r_ in results.items():
    L_.append(f"- **{k_}**: " + ", ".join(f"{a}={b}" for a, b in r_.items() if a != "issues") + f" — {'OK' if not r_['issues'] else str(len(r_['issues'])) + ' issue(s)'}")
L_.append(f"- The {len(rows)} rate rows appear in the same order with identical RUB/SAR in XLSX, DOCX and PDF: {'YES' if same3 else 'NO'}")
L_.append("- XLSX SAR cells are live formulas `=ROUND(RUB/Rate,2)` (named cell Rate = Exchange!B4 = 21.4); values checked after LibreOffice recalculation.")
L_.append("- Stray-price scan: every number formatted as a price (thousands separator or two decimals) in each output is a RUB or SAR value from rates.json.")
L_.append("")
if total_issues:
    L_.append("## Issues")
    L_.append("")
    for p_ in problems:
        L_.append(f"- {p_}")
    for k_, r_ in results.items():
        for p_ in r_["issues"]:
            L_.append(f"- {k_}: {p_}")
    L_.append("")
L_.append("## Method notes")
L_.append("")
L_.append("- PDF: words extracted with PyMuPDF and grouped into visual lines; a price is a number followed by `RUB` or `SAR`. Each hotel's pages must yield exactly its priced extras then its rate rows, in table order. Analysis pages may only repeat pairs that exist in rates.json.")
L_.append("- DOCX: python-docx reads every table whose header contains «السعر بالريال»; rate tables (one per period), extras tables and analysis tables are checked separately.")
L_.append("- Arabic copy/search in the PDF: Chromium writes some Arabic ligatures (for example «لا» and «بر») in visual order in the text layer, so searching or copying a word with these ligatures can fail. The printed shapes are correct; numbers are unaffected.")
(ROOT / "audit_report.md").write_text("\n".join(L_) + "\n", encoding="utf-8")
print("\n".join(L_[:40]))
sys.exit(0 if total_issues == 0 else 1)
