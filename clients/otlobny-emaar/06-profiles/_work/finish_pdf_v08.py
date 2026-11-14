#!/usr/bin/env python3
"""Adds document title, language, right-to-left reading direction and section bookmarks to the v08 PDF (in place)."""
import sys, os
from pypdf import PdfWriter
from pypdf.generic import NameObject, DictionaryObject, TextStringObject, BooleanObject
f = sys.argv[1]
w = PdfWriter(clone_from=f)
w.add_metadata({'/Title': 'اطلبني إعمار — الملف التعريفي | OTLOBNY Emaar — Company Profile (draft v08)',
                '/Subject': 'Company profile, draft v08, Arabic and English'})
root = w._root_object
root[NameObject('/Lang')] = TextStringObject('ar')
root[NameObject('/ViewerPreferences')] = DictionaryObject({NameObject('/Direction'): NameObject('/R2L'), NameObject('/DisplayDocTitle'): BooleanObject(True)})
for title, page in [('المحتويات — Contents', 2), ('من نحن — About Us', 3), ('الرؤية والرسالة والأهداف — Vision, Mission and Goals', 4),
                    ('خدماتنا — Our Services', 6), ('لماذا نحن — Why Us', 13), ('أعمالنا — Our Work', 14),
                    ('شركاء النجاح — Partners in Success', 17), ('تواصل معنا — Contact', 19), ('حقوق الصور — Photo credits', 20)]:
    w.add_outline_item(title, page - 1)
tmp = f + '.tmp'
with open(tmp, 'wb') as fh: w.write(fh)
os.replace(tmp, f)
print('finished', f, len(w.pages), 'pages')
