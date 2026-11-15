# Build notes: «اطلبني إعمار» / OTLOBNY Emar company profile v16

**Date:** 2026-11-15 · **Author:** corporate-designer
**Starting point:** v15, left untouched. Only p7 and the cover's two side images change.

## p7 General Contracting
- **Large double diamond:** the client's engineer in a hi-vis vest, in full colour. The crop is centred on x = 0.35, so the head, vest, plans and the building are all inside it. The crane only shows in part: the diamond's narrow top cannot hold both the engineer's head and the crane. 163 ppi.
- **Normal diamond:** the client's helmet, tape and plans, in full colour. Cropped at 1.35× on the helmet, tape and plans, with the building behind. 250 ppi.
- **Third cell:** a pale tint diamond and a navy diamond fill the remaining cells. No stock photo is used.
- **Removed:** the glass facade, concrete crew and surveyor stock photos are gone from p7. None of them appears anywhere else in the book.
- **Sources:** the new images are copies in `assets/mockups/`; the originals are untouched. Neither image is used on any other page; the build reports no image on two pages.

## Cover side images (client: darker blue)
- **Tone:** shifted towards navy. Shadows #0E1736, mid-tones navy #1F3162, highlights #8EA0D4. In v15 they were royal mid-tones with periwinkle highlights.
- **Strength:** blended at **86%** (v15: 70%). Chosen by eye after comparing 82%, 85% and 88%: clearly darker at first glance, with the subjects still recognisable and the white logo on the window cleaner's back still readable.
- **Hero:** full colour, unchanged.
- **Comparison:** `_work/v16/compare_v15-vs-v16_cover.png`; the trial renders are also in `_work/v16/`.

## Checks
- `check_arabic_pdf.py`: PASS
- Forbidden strings: 0
- Bookmarks: correct
- No image appears on two pages
- p1 and p7 viewed at full size

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v16.pdf` and `.html`
- `_work/build_profile_v16.py`
- `_work/finish_pdf_v16.py`
- `_work/contact_v16*.png`
- `_work/preview_v16/`
- `_work/v16/`
- `_work/build_v16.log`
- `_work/check_v16.log`
