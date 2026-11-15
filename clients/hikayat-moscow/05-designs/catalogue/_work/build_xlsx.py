#!/usr/bin/env python3
"""Build the Excel workbook from data/rates.json (via catalogue_lib).

Sheets: Rates, Extras, Exchange, Analysis, Notes. RUB stored as numbers; SAR as a live
formula =ROUND(RUB/Rate,2) where Rate is a workbook-level named cell (Exchange!B4 = 21.4),
plus a 'SAR (computed)' value column written from Python Decimal and a check column.
"""
import sys, pathlib
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import get_column_letter
import catalogue_lib as L

WORK = pathlib.Path(__file__).resolve().parent
ROOT = WORK.parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v01"
OUT = ROOT / f"hikayat-moscow_russia-hotel-collection_rates_ar-en_{VERSION}.xlsx"
D, M = L.DATA, L.DATA["meta"]
NAVY, GOLD, IVORY, CHAR = "14243A", "C6A66B", "F7F4ED", "292D32"
AR, LAT = "IBM Plex Sans Arabic", "Montserrat"
HFILL = PatternFill("solid", fgColor=NAVY)
SFILL = PatternFill("solid", fgColor=IVORY)
HFONT = Font(name=AR, bold=True, color="FFFFFF", size=10)
BODY = Font(name=AR, size=10, color=CHAR)
NUMF = Font(name=LAT, size=10, color=CHAR)
SARF = Font(name=LAT, size=11, bold=True, color=NAVY)
THIN = Side(style="thin", color="E4DCCB")
BOT = Border(bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="right", readingOrder=2)
NUMAL = Alignment(vertical="center", horizontal="left", readingOrder=1)

wb = Workbook()


def sheet(title, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.sheet_view.rightToLeft = True
    return ws


def header(ws, row, cols, widths=None):
    for j, (ar, en) in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=f"{ar}\n{en}")
        c.fill = HFILL if en not in ("SAR (formula)",) else PatternFill("solid", fgColor="0E1A2B")
        c.font = HFONT
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center", readingOrder=2)
        c.border = Border(bottom=Side(style="medium", color=GOLD))
    ws.row_dimensions[row].height = 34
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w


def put(ws, r, c, v, font=BODY, align=WRAP, fmt=None, fill=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font, cell.alignment, cell.border = font, align, BOT
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    return cell


# ---------------------------------------------------------------- Exchange (first so the name exists)
ex = sheet("Exchange", first=True)
ex.column_dimensions["A"].width = 34
ex.column_dimensions["B"].width = 60
put(ex, 1, 1, "سعر الصرف وطريقة التحويل — Exchange rate and method", Font(name=AR, bold=True, size=14, color=NAVY))
ex.merge_cells("A1:B1")
rows = [
    ("العملة الأساسية / Base", "1 SAR"),
    ("يساوي بالروبل (الخلية المسمّاة Rate) / equals RUB (named cell Rate)", None),
    ("المعادلة / Formula", "السعر بالريال = السعر بالروبل ÷ 21.4  —  SAR = ROUND(RUB / Rate, 2)"),
    ("التقريب / Rounding", "منزلتان عشريتان (ROUND في Excel؛ وفي الكتالوج ROUND_HALF_UP بالأرقام العشرية الدقيقة) — 2 decimals"),
    ("العمولة / Mark-up", "لا عمولة ولا هامش ربح ولا أي زيادة — none"),
    ("المصدر / Source", M["rate_line"] + "  (رسالة العميل 15 نوفمبر 2026)"),
    ("ملاحظة / Note", "غيّر الخلية B4 لإعادة حساب جميع الأسعار بالريال في ورقتي Rates وExtras وAnalysis. القيمة المعتمدة من العميل: 21.4."),
]
for i, (k, v) in enumerate(rows, 3):
    put(ex, i, 1, k, Font(name=AR, bold=True, size=10, color=NAVY))
    if v is not None:
        put(ex, i, 2, v, NUMF if isinstance(v, float) else BODY, NUMAL if isinstance(v, float) else WRAP, "0.0" if isinstance(v, float) else None)
ex.cell(row=4, column=2).value = None
# B4 holds the rate (row of "equals")
ex["B4"] = 21.4
ex["B4"].number_format = "0.0"
ex["B4"].font = Font(name=LAT, size=14, bold=True, color=NAVY)
ex["B4"].fill = SFILL
wb.defined_names["Rate"] = DefinedName("Rate", attr_text="Exchange!$B$4")

# ---------------------------------------------------------------- Rates
ws = sheet("Rates")
cols = [("#", "#"), ("المدينة", "City"), ("الفندق", "Hotel (AR)"), ("Hotel", "Hotel (EN)"), ("النجوم", "Stars"),
        ("الفترة", "Period"), ("Period", "Period (EN)"), ("التواريخ كما وردت", "Dates as written"), ("حالة الفترة", "Status at 15 Nov 2026"),
        ("نوع الغرفة", "Room type"), ("وصف الغرفة", "Room note"), ("المساحة م²", "Size m²"),
        ("الإشغال", "Occupancy"), ("Occupancy", "Occupancy (EN)"), ("الإفطار", "Breakfast"), ("Breakfast", "Breakfast (EN)"),
        ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR (formula)"), ("الريال محسوباً", "SAR (computed)"), ("تطابق", "Check"),
        ("سطر المصدر", "Source line no."), ("نص المصدر", "Source text")]
header(ws, 1, cols, [5, 11, 24, 26, 7, 16, 16, 30, 13, 26, 18, 9, 14, 14, 15, 18, 13, 14, 13, 9, 9, 40])
r = 2
for k, (h, p, rm, x) in enumerate(L.all_rows(), 1):
    city = M["cities"][h["city"]]
    st = "منتهية / ended" if L.period_status(p) == "ended" else ""
    vals = [k, city["ar"], h["name_ar"], h["name_en"], h.get("stars") or "غير مذكور", p["label_ar"], p["label_en"], p["dates_ar"], st,
            rm["name"], rm.get("qualifier_ar") or "", rm.get("size_m2") or "", x["occupancy_ar"], x["occupancy_en"], x["breakfast_ar"], x["breakfast_en"]]
    for j, v in enumerate(vals, 1):
        put(ws, r, j, v, NUMF if j in (1, 12) else BODY, NUMAL if j in (1, 5, 12) else WRAP)
    put(ws, r, 17, x["rub"], NUMF, NUMAL, "#,##0")
    put(ws, r, 18, f"=ROUND(Q{r}/Rate,2)", SARF, NUMAL, "#,##0.00", SFILL)
    put(ws, r, 19, float(Decimal(x["sar"])), NUMF, NUMAL, "#,##0.00")
    put(ws, r, 20, f'=IF(ABS(R{r}-S{r})<0.001,"OK","CHECK")', NUMF, Alignment(horizontal="center", vertical="center"))
    put(ws, r, 21, x["source_line_no"], NUMF, NUMAL)
    put(ws, r, 22, x["source_line"], Font(name=AR, size=9, color="5E6470"), WRAP)
    r += 1
ws.freeze_panes = "E2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{r-1}"
RATES_LAST = r - 1

# ---------------------------------------------------------------- Extras
ws = sheet("Extras")
cols = [("#", "#"), ("المدينة", "City"), ("الفندق", "Hotel (AR)"), ("Hotel", "Hotel (EN)"), ("النوع", "Kind"), ("البند", "Item"), ("Item", "Item (EN)"),
        ("الشرط", "Condition"), ("Condition", "Condition (EN)"), ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR (formula)"),
        ("الريال محسوباً", "SAR (computed)"), ("القيمة إن لم يُذكر سعر", "Value if no price"), ("أسطر المصدر", "Source lines"), ("نص المصدر", "Source text")]
header(ws, 1, cols, [5, 11, 24, 26, 12, 24, 24, 34, 34, 13, 14, 13, 16, 10, 44])
r = 2
k = 0
for h in L.hotels():
    for x in h["extras"]:
        k += 1
        city = M["cities"][h["city"]]
        vals = [k, city["ar"], h["name_ar"], h["name_en"], x["kind"], x["item_ar"], x["item_en"], x["condition_ar"], x["condition_en"]]
        for j, v in enumerate(vals, 1):
            put(ws, r, j, v, NUMF if j == 1 else BODY, NUMAL if j == 1 else WRAP)
        if x["rub"] is not None:
            put(ws, r, 10, x["rub"], NUMF, NUMAL, "#,##0")
            put(ws, r, 11, f"=ROUND(J{r}/Rate,2)", SARF, NUMAL, "#,##0.00", SFILL)
            put(ws, r, 12, float(Decimal(x["sar"])), NUMF, NUMAL, "#,##0.00")
        else:
            put(ws, r, 13, f'{x["value_ar"]} / {x["value_en"]}', BODY, WRAP)
        put(ws, r, 14, ", ".join(str(n) for n in x["source_line_nos"]), NUMF, NUMAL)
        put(ws, r, 15, " | ".join(x["source_lines"]), Font(name=AR, size=9, color="5E6470"), WRAP)
        r += 1
ws.freeze_panes = "E2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{r-1}"

# ---------------------------------------------------------------- Analysis
ws = sheet("Analysis")
for j, w in enumerate([26, 26, 24, 22, 30, 13, 14, 26], 1):
    ws.column_dimensions[get_column_letter(j)].width = w
r = 1
for a in L.analyses():
    put(ws, r, 1, f'{a["n"]}. {a["title_ar"]} — {a["title_en"]}', Font(name=AR, bold=True, size=13, color=NAVY))
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    for bar, ben in zip(a["basis_ar"], a["basis_en"]):
        put(ws, r, 1, f"{bar}\n{ben}", Font(name=AR, size=9.5, color=CHAR), WRAP, fill=SFILL)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        ws.row_dimensions[r].height = 15 * (2 + len(bar) // 120 + len(ben) // 140)
        r += 1
    for t in a["tables"]:
        r += 1
        put(ws, r, 1, f'{t["caption_ar"]} — {t["caption_en"]}', Font(name=AR, bold=True, size=10.5, color=NAVY))
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        r += 1
        if t.get("kind") == "extras":
            hc = [("الفندق", "Hotel (AR)"), ("Hotel", "Hotel (EN)"), ("الشرط", "Condition"), ("Condition", "Condition (EN)"), ("القيمة", "Value"), ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR (formula)")]
        else:
            hc = [("الفندق", "Hotel (AR)"), ("Hotel", "Hotel (EN)"), ("نوع الغرفة", "Room type"), ("الفترة", "Period"), ("الإشغال · الإفطار", "Occupancy · breakfast"), ("السعر بالروبل", "RUB"), ("السعر بالريال", "SAR (formula)"), ("ملاحظة", "Note")]
        header(ws, r, hc)
        r += 1
        for x in t["rows"]:
            if t.get("kind") == "extras":
                vals = [x["hotel_ar"], x["hotel_en"], x["condition_ar"], x["condition_en"], "" if x["rub"] is not None else f'{x["value_ar"]} / {x["value_en"]}']
            else:
                vals = [x["hotel_ar"], x["hotel_en"], x["room_ar"], f'{x["period_ar"]} ({x["dates_ar"]})', x["basis_ar"]]
            for j, v in enumerate(vals, 1):
                put(ws, r, j, v)
            if x["rub"] is not None:
                put(ws, r, 6, x["rub"], NUMF, NUMAL, "#,##0")
                put(ws, r, 7, f"=ROUND(F{r}/Rate,2)", SARF, NUMAL, "#,##0.00", SFILL)
            if t.get("kind") != "extras":
                put(ws, r, 8, x.get("note_ar") or "")
            r += 1
        if not t["rows"]:
            put(ws, r, 1, "لا توجد صفوف تطابق هذا الأساس / No rows match this basis"); r += 1
    r += 2

# ---------------------------------------------------------------- Notes
ws = sheet("Notes")
header(ws, 1, [("رقم", "ID"), ("الملاحظة", "Note (AR)"), ("Note", "Note (EN)"), ("الفنادق", "Hotels"), ("مطبوعة في الكتالوج", "Printed in catalogue")], [7, 70, 70, 30, 12])
for i, a in enumerate(D["anomalies"], 2):
    put(ws, i, 1, a["id"], NUMF, NUMAL)
    put(ws, i, 2, a["ar"])
    put(ws, i, 3, a["en"], Font(name=LAT, size=9.5, color=CHAR), Alignment(wrap_text=True, vertical="center", horizontal="left", readingOrder=1))
    put(ws, i, 4, ", ".join(L.hotel(hid)["name_en"] for hid in a["hotels"]), Font(name=LAT, size=9, color=CHAR), Alignment(wrap_text=True, vertical="center", horizontal="left"))
    put(ws, i, 5, "نعم / yes" if a.get("print", True) else "لا (داخلي) / no (internal)")
    ws.row_dimensions[i].height = 15 * (2 + len(a["en"]) // 85)
ws.freeze_panes = "B2"
n0 = len(D["anomalies"]) + 3
put(ws, n0, 1, "الشروط العامة / General terms", Font(name=AR, bold=True, size=11, color=NAVY))
for i, (ta, te) in enumerate(zip(D["general_terms"]["ar"], D["general_terms"]["en"]), n0 + 1):
    put(ws, i, 2, ta); put(ws, i, 3, te, Font(name=LAT, size=9.5), Alignment(wrap_text=True, horizontal="left", vertical="center"))

for s_ in wb.worksheets:
    s_.page_setup.orientation = "landscape"
    s_.page_setup.paperSize = s_.PAPERSIZE_A4
    s_.page_setup.fitToWidth, s_.page_setup.fitToHeight = 1, 0
    s_.sheet_properties.pageSetUpPr.fitToPage = True
    if s_.title in ("Rates", "Extras", "Notes"):
        s_.print_title_rows = "1:1"
wb.move_sheet("Exchange", offset=2)  # order: Rates, Extras, Exchange, Analysis, Notes
wb.active = 0
for s_ in wb.worksheets:
    s_.sheet_view.tabSelected = (s_.title == "Rates")
wb.properties.title = "RUSSIA HOTEL COLLECTION 2026 — rates"
wb.properties.creator = M["agency_ar"]
wb.save(OUT)
print("wrote", OUT.name, "rate rows:", RATES_LAST - 1)
