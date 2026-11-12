---
name: visual-identity
description: Create a client's visual identity - creative direction, logo and bilingual lockups, colour, typography, graphic system, applications and brand guidelines. Use when the user asks for a logo, identity, brand guidelines, a rebrand's visuals, or 'the look' of a brand.
---

# Visual identity

Covers stage 4: `04-identity/`.

## Gate

An approved strategy must exist in `03-strategy/`. If it does not, run `brand-development` first or get explicit go-ahead to work from stated assumptions.

## Steps

1. **Direction** (art-director agent) → `04-identity/01-direction/`. Two or three distinct creative directions with moodboards and a recommendation. Skills: `creative-direction`, `art-direction`, `brand-strategy`.
2. **Approval of one direction.** Do not start logo refinement before this.
3. **Logo** (identity-designer agent) → `02-logo/`. Concepts within the chosen direction, then refinement; Arabic, Latin and bilingual lockups; colour, black and white versions. Skills: `logo-design`, `brand-identity`.
4. **System** → `03-system/`. Primary and secondary colours with all values, Arabic and English typefaces with hierarchy, patterns, icons, imagery style, and `tokens.json`.
5. **Applications** → `04-applications/`. Official stationery (letterhead, envelope, folder), business cards, uniform, plus the touchpoints this client actually uses (signage, vehicles, packaging, social, digital). At least five.
6. **Guidelines** → `05-guidelines/`, built from `templates/brand-guidelines/`.
7. **Quality gate.** Run `quality-control` with `brand-checklist.md`.
8. **Record.** Update `brand-context.md` with the final palette, fonts and logo usage; list licences in `licences.md`.

## Done when

The identity meets every item under "Identity system minimums" in `.claude/rules/branding.md` and passes the brand checklist.
