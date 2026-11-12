---
name: digital-design
description: Design digital products from an approved identity - website UI/UX, landing pages, mobile applications, dashboards and design systems, in Arabic RTL and English LTR. Use when the user asks for a website, landing page, app screens, dashboard, wireframes, prototype, design system or design tokens.
---

# Digital design

Service F. Output folder: `05-designs/<project>/`. Lead: ui-ux-designer agent.

## Gate

An approved identity (or at least approved colours, fonts and logo in `brand-context.md`). Without it, state the assumptions and get a go-ahead.

## Steps

1. **UX brief** → `ux-brief.md`: users, their goals, the three most important tasks, content inventory, languages, devices, success measures.
2. **Structure:** sitemap and key user flows. For a landing page: the single conversion goal and the section order that leads to it.
3. **Wireframes** in grey, mobile first. Get the structure approved before visual design.
4. **Tokens and components:** derive colour, type, spacing, radius and shadow tokens from the brand (`04-identity/03-system/tokens.json`); list the components (button, input, card, nav, table, modal…) with their states.
5. **High-fidelity design** for mobile and desktop, every key screen, every state (empty, loading, error, success).
6. **Build the deliverable:**
   - Figma file with components and variables when write access works (see `.claude/rules/tools-figma-canva.md`), or
   - a working HTML/CSS prototype (single folder, fonts from `assets/fonts/` via `@font-face`).
7. **Verify in a browser:** screenshots at 390 px and 1440 px, Arabic and English, checked for overflow, alignment and contrast.
8. **Handoff notes:** tokens, components, breakpoints, behaviours, assets.
9. **Quality gate:** run `quality-control`.

Specialist skills: `web-design`, `frontend-design`, `motion-design`, `design-principles`, `webapp-testing`, `web-artifacts-builder`.

## By deliverable

| Deliverable | Must include |
|---|---|
| Website UI/UX | Sitemap, home plus key inner pages, navigation, footer, responsive behaviour |
| Landing page | One goal, hero with clear value proposition and CTA, proof, objection handling, final CTA |
| Mobile app | Onboarding, core flow, navigation model, platform conventions (iOS / Android), safe areas |
| Dashboard | Information hierarchy, KPI cards, charts in brand style, tables, filters, empty and loading states |
| Design system | Tokens, type scale, grid, components with states, usage rules, RTL rules |

## RTL and LTR

- Arabic: `dir="rtl"` and `lang="ar"`; use logical CSS properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`) so one stylesheet serves both directions.
- Mirror navigation, breadcrumbs, steppers, carousels and directional icons. Do not mirror logos, media controls, phone numbers or charts' numeric axes.
- Arabic text needs more line height and is often shorter in characters but taller; test with real copy.

## Done when

- Meets WCAG AA (contrast, focus, 44 px targets)
- Works at mobile and desktop widths in both languages
- No placeholder copy and no invented claims
