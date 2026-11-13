# Fonts for the Sidra Coffee presentation

> **SYSTEM TEST — FICTIONAL CLIENT.**

Applies to `demo-sidra-coffee_presentation_cafe-owners_ar_v03.pptx`. Date: 2026-11-13.

## Before you open the PowerPoint file

The PPTX does not carry its fonts inside it. Install the two families below first; otherwise PowerPoint, Keynote or LibreOffice will substitute another typeface and the line breaks will change. The PDF has its fonts embedded and needs nothing installed.

| Family | Used for | Weights used in the deck | Licence |
|---|---|---|---|
| IBM Plex Sans Arabic | All Arabic text | Regular, Bold | SIL Open Font License 1.1 |
| IBM Plex Sans | Latin text and numerals: the email address, 250, 1, the step numbers, the slide counter | Regular, Bold | SIL Open Font License 1.1 |

Both families are supplied in the delivery package, in the folder `07-fonts-and-licences/`, each in its own subfolder with its licence file (`OFL.txt`).

## How to install

1. Open the folder `07-fonts-and-licences/` in the delivery package.
2. In each of the two subfolders, open the Regular and Bold `.ttf` files and choose Install (Windows: right-click, Install; macOS: double-click, Install Font).
3. Close and reopen PowerPoint, then open the deck.

## Licence

Both families are Copyright © 2017 IBM Corp. with Reserved Font Name "Plex", released under the SIL Open Font License 1.1. The licence allows use, embedding and redistribution together with the licence file; the fonts may not be sold on their own. Keep each `OFL.txt` with its font files.

## How the fonts are set in the file

- The deck's theme ("Sidra Coffee") sets IBM Plex Sans for Latin text and IBM Plex Sans Arabic for Arabic text, for headings and body. New slides made from the four layouts pick these up without manual formatting.
- Latin letters and numerals inside Arabic text are separate runs set in IBM Plex Sans.
- No other typeface is used.

## Things to know about this file

- **Logos are PNG images.** The logo on each layout is a PNG picture inside the file, not a vector: the tool that built the deck (python-pptx) cannot place SVG. Do not enlarge the logos beyond their placed size. For any larger use, take the vector logo from the logo folder of the delivery package.
- **Rendered in LibreOffice only.** The deck was built by script and checked by rendering it in LibreOffice. It has not been opened in Microsoft PowerPoint or Keynote. Line breaks and spacing may differ slightly there; check all five slides in PowerPoint before presenting.
- **PDF for screen, not print.** In the PDF, some glyphs are embedded as outlines (Type 3). They look correct on screen. The PDF is not a print file.
