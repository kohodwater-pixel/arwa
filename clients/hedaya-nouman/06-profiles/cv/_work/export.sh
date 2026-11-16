#!/usr/bin/env bash
# Build everything, export PDFs, render DOCX through LibreOffice for verification only.
set -euo pipefail
CV=/home/user/arwa/clients/hedaya-nouman/06-profiles/cv
W=$CV/_work
python3 "$W/build_cv.py"
for h in "$CV"/hedaya-nouman_cv_*_v01.html; do
  node /home/user/arwa/scripts/html2pdf.cjs "$h" "${h%.html}.pdf" --size A4 | tr -d '\n'; echo
done
mkdir -p "$W/docx-render" "$W/png"
soffice --headless --convert-to pdf --outdir "$W/docx-render" "$CV"/hedaya-nouman_cv_*_v01.docx >/dev/null 2>&1
for p in "$CV"/hedaya-nouman_cv_*_v01.pdf; do
  n=$(basename "${p%.pdf}")
  pdftoppm -r 80 -png "$p" "$W/png/$n"
  echo "$n pages=$(pdfinfo "$p" | awk '/^Pages/{print $2}')"
done
for p in "$W"/docx-render/*.pdf; do
  n=$(basename "${p%.pdf}")
  pdftoppm -r 80 -png "$p" "$W/png/docx_$n"
  echo "docx-render $n pages=$(pdfinfo "$p" | awk '/^Pages/{print $2}')"
done
