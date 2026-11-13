#!/usr/bin/env bash
# Build, export, finish and check the profile draft v01.
set -e
D=/home/user/arwa/clients/otlobny-emaar/06-profiles
N=otlobny-emaar_company-profile_screen_ar-en_v01
python3 $D/_work/build_profile_v01.py
node /home/user/arwa/scripts/html2pdf.cjs $D/$N.html $D/$N.pdf --size 297x210mm
python3 $D/_work/finish_pdf_v01.py $D/$N.pdf
python3 /home/user/arwa/scripts/check_arabic_pdf.py $D/$N.pdf --png $D/_work/preview_v01 --dpi 110 --expect "اطلبني إعمار"
python3 -c "
import pymupdf;d=pymupdf.open('$D/$N.pdf');print('pages',len(d),sorted({(round(p.rect.width/72*25.4,1),round(p.rect.height/72*25.4,1)) for p in d}))"
