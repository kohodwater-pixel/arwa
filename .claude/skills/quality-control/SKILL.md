---
name: quality-control
description: Review a deliverable against the agency checklists and prepare the final delivery package. Use before anything is shown or sent to a client, when the user says 'review', 'QC', 'check this', 'is this ready', or 'prepare final delivery / handover'.
---

# Quality control

Covers the gate before every client presentation and stage 8: `08-final-delivery/`. Lead: quality-reviewer agent.

## Review

1. **Scope the review.** Every review starts with the mandatory ten-point review in `quality-control/project-review.md`. Then list the files to be reviewed and the detailed checklists that apply:
   - identity or guidelines → `quality-control/brand-checklist.md`
   - any designed piece → `quality-control/design-checklist.md`
   - handover package → `quality-control/delivery-checklist.md`
2. **Hand it to the quality-reviewer agent**, giving it the files and the client folder. The reviewer must not be the agent that made the work.
3. **Inspect the real files:** render and view them, read all text in both languages, verify dimensions, colour mode, resolution, fonts and names.
4. **Report** using the format in the quality-reviewer agent: verdict, issues with location and required fix, and anything not checked.
5. **Save the report** (the Creative Director does this; the reviewer has no write access) as `08-final-delivery/_reviews/review_<deliverable>_<date>_r<N>.md`.
6. **Fail → back to the maker.** Show the notes, have the agent that made the work fix every critical and major issue, then review again. Do not approve or move failed work forward.

## Final delivery

1. First list every deliverable in the brief (section 10) and confirm each one has been through review, **including strategy and other documents**. Anything unreviewed goes to the quality-reviewer before packaging.
2. Only after a PASS, copy the latest reviewed files into `08-final-delivery/` using the structure in `.claude/rules/file-delivery.md`.
3. Rename to `final` only if the client has approved; otherwise keep version numbers and mark the package HELD with its release conditions. Remove drafts and rejected options.
4. Collect sources with `scripts/collect_html.py` (self-contained folders), plus linked assets and fonts (where the licence allows redistribution; otherwise list where to obtain them).
5. Write `08-final-delivery/README.md` for a non-designer: what each folder contains, which logo file to use where, colour values, fonts and licences.
6. Send the finished folder to the quality-reviewer for the delivery checklist; the package is not done until that review passes.
7. Update `brand-context.md` with the delivery date and what was delivered.
