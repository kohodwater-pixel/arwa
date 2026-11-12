---
name: print-design
description: Design and prepare print-ready material - stationery, business cards, brochures, flyers, posters, roll-ups, signage, packaging. Use when the user asks for anything that will be printed or produced physically, or asks to prepare or check a file for a printer.
---

# Print design

Covers stage 5 (print): `05-designs/<project>/`. Lead: graphic-designer agent.

## Steps

1. **Get the production spec before designing.** Finished size, folds, page count, paper or material, print method, finishes (foil, emboss, spot UV, die cut), quantity, and the printer's own requirements if known.
2. **Set up the document correctly.** Finished size, 3 mm bleed (5 mm for large format, or as the printer specifies), safe margin of at least 5 mm, CMYK, and spot colours named as in the guidelines.
3. **Design** from the approved identity. For multi-page work, page count for saddle stitch must be a multiple of 4; allow for creep and the binding edge. Arabic documents bind on the right.
4. **Check images.** 300 dpi at final size (large format may be 100-150 dpi at full size), converted to CMYK, nothing upscaled.
5. **Check type.** Body text 100K, not rich black; minimum about 6 pt for Latin and 7-8 pt for Arabic; small reversed text avoided on four-colour backgrounds.
6. **Special finishes** go on a separate named spot-colour layer set to overprint; die lines likewise.
7. **Export** PDF/X-4 (or what the printer asks for) with bleed and crop marks, fonts embedded or outlined. Keep an un-outlined source.
8. **Preflight and quality gate.** Verify page size, bleed, colour mode, resolution and fonts in the exported PDF, then run `quality-control` with `design-checklist.md`.

Specialist skills: `collateral-design`, `canvas-design`, `pdf`, `brand-packaging`.

## Common finished sizes

| Item | Size |
|---|---|
| Business card | 90 × 50 mm or 85 × 55 mm (confirm locally) |
| Letterhead | A4, 210 × 297 mm |
| DL flyer / envelope | 99 × 210 mm / 110 × 220 mm |
| Roll-up banner | 850 × 2000 mm |
