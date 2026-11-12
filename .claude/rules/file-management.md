# File management

## One client, one folder

- Every client lives in `clients/<client-slug>/`, created from `clients/CLIENT_TEMPLATE/`.
- Work for a client reads and writes only inside that client's folder, plus the shared `templates/`, `assets/`, `scripts/` and `quality-control/`.
- Never copy text, research, names, logos, colours or images from one client's folder into another's. Shared learning goes into `templates/` only after every client-specific detail is removed.
- Skills that keep their own brand file (for example `brand`, which writes `.agents/brand.md`, or `brand-context`) must be pointed at `clients/<client-slug>/brand-context.md`. Do not create a repo-level brand file.

## brand-context.md

One per client. It holds only approved or verified information: identity, colours, fonts, logo usage, tone of voice, verified facts, the decision log and the delivery log. Unknowns are `TBC`; assumptions are labelled. Update it at every approval.

## Originals are never touched

- Everything the client sends goes into `_originals/` exactly as received, with the date in a `_originals/README.md` line.
- Files in `_originals/` are never edited, renamed, overwritten or deleted. Work on a copy in the relevant stage folder.

## Versions

- Each change that the client or reviewer will see is a new version file (`_v01`, `_v02`…), not an overwrite. See `file-delivery.md` for naming.
- Superseded versions and rejected directions move to the stage's `_archive/` folder with a one-line reason. They are kept.
- An approved file is never modified. A change after approval starts a new version.

## No deletion

- Do not delete client files. If something must go (duplicate, wrong client, sensitive data), tell the user what and why, and let them decide.
- Temporary render and preview files go in a `_work/` subfolder so they are easy to tell apart from deliverables.
