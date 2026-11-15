#!/usr/bin/env bash
# Rebuild every output of the Russia Hotel Collection catalogue from the client's source file.
# Usage: bash _work/build_all.sh [v01]
set -euo pipefail
V="${1:-v01}"
W="$(cd "$(dirname "$0")" && pwd)"; C="$(dirname "$W")"
H="hikayat-moscow_russia-hotel-collection_catalogue_ar-en_$V"
cd "$W"
python3 transcribe.py                       # source -> data/rates.json (with self-checks)
python3 build_html.py "$V" > "$W/build_html.log"   # measured pagination -> HTML + pagemap.json
node /home/user/arwa/scripts/html2pdf.cjs "$C/$H.html" "$C/$H.pdf" --size 210x297mm > "$W/html2pdf.log"
node measure.cjs check "$C/$H.html" "$W/overflow.json"
python3 -c "import json,sys;d=json.load(open('$W/overflow.json'));p=[x for x in d if not x.get('info')];print('overflow problems:',len(p));sys.exit(1 if p else 0)"
python3 build_docx.py "$V"
python3 build_xlsx.py "$V"
rm -rf "$W/preview_$V"
python3 /home/user/arwa/scripts/check_arabic_pdf.py "$C/$H.pdf" --png "$W/preview_$V" --expect "حكايات موسكو" --expect "فنادق موسكو" --expect "السعر بالريال"
mkdir -p "$W/docx_render"; soffice --headless --convert-to pdf --outdir "$W/docx_render" "$C/$H.docx" > /dev/null 2>&1
rm -rf "$W/docx_render/preview"
python3 /home/user/arwa/scripts/check_arabic_pdf.py "$W/docx_render/$H.pdf" --png "$W/docx_render/preview" --dpi 70 --expect "حكايات موسكو" --expect "السعر بالريال"
python3 audit.py "$V"
