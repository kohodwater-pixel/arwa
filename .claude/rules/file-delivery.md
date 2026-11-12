# File delivery rules

## Naming

`<client>_<deliverable>_<variant>_<lang>_v<NN>.<ext>`

- lowercase, hyphens inside a part, underscores between parts, no spaces, no Arabic characters in file names
- `lang` is `ar`, `en` or `ar-en`
- versions are two digits: `v01`, `v02`; the approved file is re-exported with `final` in place of the version
- example: `almada_company-profile_print_ar-en_v03.pdf`

Never name a file `final2`, `new`, `last` or `edited`.

## Formats

| Deliverable | Formats |
|---|---|
| Logo | SVG, PDF (vector), PNG transparent at 1x/2x/4x; each in full colour, black, white |
| Print | PDF/X-4 or PDF/X-1a, CMYK, 300 dpi images, 3 mm bleed (5 mm for large format), crop marks, fonts embedded or outlined |
| Digital and social | PNG or JPG in sRGB at exact platform pixel size; MP4 (H.264) for motion |
| Presentations | PPTX or Keynote source plus PDF; fonts packaged or listed |
| Documents | PDF for reading plus the editable source |
| Guidelines | PDF plus colour tokens (JSON or CSS) and font list with licence notes |

## Output formats by project

Deliver what the project needs from: **PDF, PPTX, DOCX, SVG, PNG, JPG, HTML** (and MP4 for motion). Every deliverable ships with an editable source so work can continue: HTML/CSS, SVG, PPTX, DOCX, or a Figma/Canva edit link.

## Arabic and English

- Both languages are supported on every project. Arabic is right to left (`dir="rtl"`, right-aligned, mirrored layout); English is left to right.
- Arabic and bilingual PDFs are produced from HTML with `node scripts/html2pdf.cjs` using fonts from `assets/fonts/`.
- **Before any Arabic PDF is approved** run `python3 scripts/check_arabic_pdf.py <file.pdf> --png <dir>` and open the previews. It must report PASS, name the intended fonts (no DejaVu, FreeSerif or other fallback), and the letters must be visibly connected and in the right order.
- PPTX and DOCX with Arabic are rendered to PDF with LibreOffice and checked the same way; set paragraph direction to RTL, not just right alignment.
- For print, use static font files rather than variable fonts so the fonts embed by name.

## Colour

- Print files are CMYK with spot colours named exactly as in the guidelines. Rich black only for large solids; body text is 100K.
- Screen files are sRGB.
- Each brand colour is delivered with HEX, RGB, CMYK and Pantone values.

## Final delivery folder

`08-final-delivery/` contains only approved files, arranged as:

```
08-final-delivery/
├── 01-logo/
├── 02-brand-guidelines/
├── 03-stationery-print/
├── 04-digital-social/
├── 05-profile/
├── 06-presentations/
├── 07-fonts-and-licences/
├── 08-source-files/
└── README.md   # what is inside, how to use it, font and image licences
```

- No working files, no drafts, no rejected options.
- Source files are included with linked assets collected.
- The README is written for a non-designer.
