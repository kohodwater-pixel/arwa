# Creative Agency OS

This repository is the operating system of a creative agency. Every client project runs through the same pipeline, the same folder layout and the same quality gates.

## How work flows

| Stage | Folder in `clients/<client>/` | Skill | Lead agent |
|---|---|---|---|
| 1. Brief | `01-brief/` | `client-onboarding` | brand-strategist |
| 2. Research | `02-research/` | `brand-development` | market-researcher |
| 3. Strategy (and naming if needed) | `03-strategy/` | `brand-development` | brand-strategist, naming-specialist |
| 4. Identity | `04-identity/` | `visual-identity` | art-director, identity-designer |
| 5. Designs | `05-designs/` | `marketing-design`, `print-design` | graphic-designer |
| 6. Profiles | `06-profiles/` | `company-profile` | corporate-designer |
| 7. Presentations | `07-presentations/` | `presentation-design` | presentation-designer |
| 8. Final delivery | `08-final-delivery/` | `quality-control` | quality-reviewer |

Digital product work (websites, apps) is handled by the ui-ux-designer and lands in `05-designs/`.

## Ground rules

- **Start a client by copying** `clients/CLIENT_TEMPLATE/` to `clients/<client-slug>/` (lowercase, hyphenated). Never work inside the template.
- **`clients/<client>/brand-context.md` is the single source of truth** for that client. Read it before any task; update it whenever a decision is approved. If a general-purpose skill wants to write brand context elsewhere (for example `.agents/brand.md`), point it at the client's `brand-context.md` instead.
- **Do not skip stages.** Identity work needs an approved strategy; design work needs an approved identity. If something upstream is missing, say so and produce it first, or get the user's explicit go-ahead to proceed on stated assumptions.
- **Nothing reaches `08-final-delivery/` without passing quality control.** The quality-reviewer checks against `quality-control/*.md` and reports pass or fail per item.
- **Client material is confidential.** Do not reuse one client's content, research or assets in another client's work.
- **Mark assumptions.** Anything not confirmed by the client is labelled as an assumption in the document where it appears.

## Standing rules

The files in `.claude/rules/` always apply:

- `branding.md` — how strategy and identity decisions are made and recorded
- `arabic-design.md` — Arabic and bilingual typography and layout
- `file-delivery.md` — naming, formats, colour modes, folder structure
- `quality-standards.md` — the bar every deliverable must clear

## Reusable material

- `templates/` — starting structures for company profiles, brand guidelines, social media and presentations
- `quality-control/` — the checklists used at each gate
- `.claude/skills/` — besides the eight agency workflow skills above, specialist skills are installed (for example `brand-positioning`, `brand-naming`, `logo-design`, `brand-identity`, `creative-direction`, `collateral-design`, `pptx`, `pdf`). The workflow skills say when to call them.
