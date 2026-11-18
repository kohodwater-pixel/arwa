# Job advert — notes (v01)

**Status:** finished unbranded advert, no placeholders. Awaiting quality review and client approval.

## Pieces
| File | Size | Use |
|---|---|---|
| `tbc-restaurants-company_job-advert_post_ar_v01.png` / `.html` | 1080 × 1350, sRGB | Instagram / Facebook feed 4:5 |
| `tbc-restaurants-company_job-advert_story_ar_v01.png` / `.html` | 1080 × 1920, sRGB | Story 9:16; all text between y 250 and y 1580 |

Shared: `job-advert.css` (palette variables in the first `:root` block), `fonts/` (IBM Plex Sans Arabic static, SIL OFL, copied from `assets/fonts/`).
Rebuild: `NODE_PATH=/opt/node-tools/node_modules node _work/render.cjs && python3 _work/finish.py`.

## Copy
Taken character for character from `01-brief/brief.md` (copy v01 plus the 2026-11-18 client additions: «خبرة في التصميم (شرط أساسي)», the tag «العمل عن بُعد», the apply sentence «للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني» and the email `hr@otlobny.co`). `_work/render.cjs` asserts every string and their order. Numerals: none appear; Western if added.

## Unbranded by ruling
No logo and no company name appear (Creative Director ruling in the brief). The email is set LTR (`<bdi dir="ltr">`, isolated, no wrap) as the call to action.

## Look (assumption — no brand supplied)
Neutral restaurants-sector palette, to be replaced by the brand's:
ground `#15302A`, ground tint `#21443B`, text `#F7F1E5`, soft text `#D8D1C0`, accent `#F2A93B`.
Type: IBM Plex Sans Arabic 400/500/600/700 (also used for the Latin email). No letter-spacing; body line-height 1.6; body 30 px (post), 32 px (story); email 60 / 64 px.
Icons: six inline SVG line icons drawn for this piece (megaphone, chat, heart, plate and cutlery, chef hat, home/remote). No photos, stock or AI images.

## History inside v01
The first render carried two dashed gap markers (logo box, apply method). Both were removed the same day when the client supplied the email and the advert was ruled unbranded; that render was never shown to the client.

## Not done
Native Arabic proofread by a second reader; on-device preview under the real Instagram story UI; confirmation that the mailbox `hr@otlobny.co` exists and receives mail.
