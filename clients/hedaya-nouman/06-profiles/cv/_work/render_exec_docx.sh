#!/usr/bin/env bash
# Build the executive DOCX files and render them through LibreOffice for checking (never touches the approved PDFs).
set -euo pipefail
W=/home/user/arwa/clients/hedaya-nouman/06-profiles/cv/_work
python3 "$W/build_exec_docx.py"
rm -rf "$W/exec-docx-render"; mkdir -p "$W/exec-docx-render"
soffice --headless --convert-to pdf --outdir "$W/exec-docx-render" "$W"/../*executive*_v04.docx >/dev/null 2>&1
for f in "$W"/exec-docx-render/*.pdf; do
  echo "$(basename "$f") pages=$(pdfinfo "$f" | awk '/^Pages/{print $2}') fonts=$(pdffonts "$f" | tail -n +3 | awk '{print $1}' | sed 's/.*+//' | sort -u | tr '\n' ' ')"
done
python3 - <<'PY'
import pymupdf, glob
for f in glob.glob('/home/user/arwa/clients/hedaya-nouman/06-profiles/cv/_work/exec-docx-render/*.pdf'):
    d = pymupdf.open(f)
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=100).save('/home/user/arwa/clients/hedaya-nouman/06-profiles/cv/_work/check-png/execdocx_' + f.split('/')[-1][17:-4] + f'_p{i+1}.png')
PY
cd "$W/.." && md5sum -c _work/approved_exec_md5.txt | grep -vc ': OK' || true
