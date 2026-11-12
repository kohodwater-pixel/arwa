# Mandatory project review — المراجعة الإلزامية

Every project passes this review before the client sees it and again before final delivery. Score each point **PASS / FAIL / N/A** with one line of evidence (file and location). The detailed checklists (`brand-checklist.md`, `design-checklist.md`, `delivery-checklist.md`) support these ten points.

| # | Point | What to check | Critical if failed? |
|---|---|---|---|
| 1 | **Creative idea** — جودة الفكرة الإبداعية | There is one clear idea; it comes from the approved strategy; it can be said in a sentence | Major |
| 2 | **Distinctiveness** — التميز وعدم تقليد المنافسين | Compared side by side with each competitor in `02-research/`; no borrowed mark, palette or layout; no resemblance to a well-known brand | Critical |
| 3 | **Colour consistency** — تناسق الألوان | Only approved colours; values match `brand-context.md` exactly; contrast meets WCAG AA | Major |
| 4 | **Arabic and English typography** — صحة الخطوط العربية والإنجليزية | Approved fonts actually applied (no fallback); Arabic letters connected and right to left; no tracking or faux styles on Arabic; scripts optically matched; `scripts/check_arabic_pdf.py` passes | Critical |
| 5 | **Logo clarity** — وضوح الشعار | Correct version; clear space and minimum size respected; legible at small size, in one colour and reversed | Critical |
| 6 | **Layout** — جودة توزيع العناصر | Clear hierarchy; consistent grid and margins; nothing cramped, clipped or overflowing; RTL and LTR layouts correct | Major |
| 7 | **Consistency across pages** — التناسق بين صفحات المشروع | Same grid, type scale, colours, icon style and tone on every page, slide and piece | Major |
| 8 | **Accuracy** — دقة المعلومات وعدم اختراع إنجازات | Every name, number, client, project, certification and date is found in the brief or `brand-context.md`; no invented achievements; no placeholder text; zero spelling errors in both languages | Critical |
| 9 | **Export quality** — جودة التصدير | Correct format, size, colour mode and resolution; fonts embedded; bleed for print; files open cleanly; naming follows `file-delivery.md` | Critical for print, major otherwise |
| 10 | **Matches the client's requirements** — مطابقة التسليم لمتطلبات العميل | Every deliverable, language and format in the brief is present and complete | Critical |

## Verdict

- **PASS** — all ten points pass.
- **PASS WITH MINOR FIXES** — only minor issues; none of the ten points fails.
- **FAIL** — any point fails. Any critical issue is an automatic fail.

## Rule

The review notes are shown to the Creative Director and the client-facing summary states them honestly. Work is not approved, and does not enter `08-final-delivery/`, until every critical and major issue has been fixed by the agent that made the work and the review has been run again.

Save each review as `clients/<client>/08-final-delivery/_reviews/review_<deliverable>_<YYYY-MM-DD>_r<N>.md`.
