# Build notes — Russia Hotel Collection 2026 — v01 (2026-11-15)

## What is here

| File | What it is |
|---|---|
| `hikayat-moscow_russia-hotel-collection_catalogue_ar-en_v01.pdf` | Designed catalogue, A4 portrait, 35 pages, 0.54 MB (fine for WhatsApp and email), fonts embedded |
| `hikayat-moscow_russia-hotel-collection_catalogue_ar-en_v01.html` | Editable source of the PDF (needs `assets/`) |
| `hikayat-moscow_russia-hotel-collection_catalogue_ar-en_v01.docx` | Editable Word version, same content and order |
| `hikayat-moscow_russia-hotel-collection_rates_ar-en_v01.xlsx` | Workbook: Rates, Extras, Exchange, Analysis, Notes |
| `data/rates.json` | The single data file all three outputs are generated from |
| `audit_report.md` | Automated audit result (PASS, zero mismatches) |
| `assets/fonts/` | IBM Plex Sans Arabic, Montserrat, Playfair Display (static TTF + OFL licences) |
| `assets/photos/` | Two CC0 city photos + `CREDITS.md` (sourcing record; nothing is printed in the catalogue) |
| `_work/` | Build scripts, previews, contact sheets, logs |

## How to rebuild

`bash _work/build_all.sh v01` does the following in order:
1. `transcribe.py`: source file → `data/rates.json`. RUB values are read from the cited source lines (no price is typed), and occupancy and breakfast labels are asserted against each line's wording. Every source line with a RUB figure must be used exactly once.
2. `build_html.py`: measures every block in Chromium, then paginates (no table splits, nothing overflows) → HTML and `pagemap.json`.
3. `scripts/html2pdf.cjs` → PDF; `measure.cjs check` → overflow report (must be 0).
4. `build_docx.py` and `build_xlsx.py`, from the same `catalogue_lib.py`.
5. `check_arabic_pdf.py` on the PDF and on the LibreOffice render of the DOCX.
6. `audit.py` → `audit_report.md`, plus `_work/source_crosswalk.md` (each source line next to what rates.json holds).

## Decisions taken in this build

- **Master page order per hotel:** name card → validity → booking notes → extras → one rate table per period. Conditions come before prices, and no hotel ends on a near-empty page.
- **Columns:** rate tables use exactly نوع الغرفة | الإشغال | الإفطار | السعر بالروبل | السعر بالريال. SAR is the largest and boldest figure, in an ivory column with a gold rule; RUB is smaller beside it.
- **Missing occupancy:** where the source gives no occupancy (for example «مع إفطار لشخص / لشخصين»), occupancy is shown as «غير مذكور» and breakfast exactly as written.
- **Room sizes:** shown as «المساحة 35 متراً مربعاً», because «م²» reorders in RTL.
- **Ended periods:** carry a small «فترة منتهية — تُعرض كما وردت» tag (as of 15 Nov 2026). Nothing is removed.
- **Analysis reference dates:** comparisons use 18 Nov 2026 and 10 Dec 2026. "With breakfast for 2" is treated as two guests with breakfast; this is stated on each analysis page. Where the source says «نهاية نوفمبر», 30 Nov is used for comparisons only. No averages or differences are computed, so no number appears that is not in the source.
- **Images:** the client asked for no printed credits, so only CC0 or public-domain images are used. No usable photo of any specific hotel was found, so every hotel has a typographic name card. Each section opener uses a CC0 city photo.
- **Notes page:** 18 short factual notes; one internal note (the agency name assumption) is kept out of print and appears in the XLSX Notes sheet.
- **Word:** paragraphs and sections are bidi, tables use `bidiVisual`, and Latin/number runs are wrapped in LTR embedding. In bidi paragraphs, jc "left" is the visual right, so alignment is swapped for RTL paragraphs (verified in LibreOffice). The index lists PDF page numbers, because Word repaginates.
- **Excel:** the sheet view is RTL. SAR is `=ROUND(RUB/Rate,2)`, with Rate as a named cell (Exchange!B4 = 21.4), plus a computed column and an OK/CHECK column. Values were verified after LibreOffice recalculation.

## Known limits

- PDF text layer: Chromium stores some Arabic ligatures (for example «لا», «بر») in visual order, so copying or searching words that contain them can fail. The printed shapes are correct and numbers are unaffected.
- Not yet print-production ready: the PDF is RGB without bleed or crop marks, and the city photos are about 150 ppi at their placed size. Fine for screen, WhatsApp, email and office printing. A commercial print version needs a CMYK/PDF-X export, 3 mm bleed and higher-resolution photos.
- The DOCX needs the three fonts installed (they are in `assets/fonts/`). Without them Word substitutes fonts and the layout reflows.
- The Arabic copy has not been proofread by a native reader (required by `arabic-design.md` before delivery).
