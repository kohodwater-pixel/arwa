---
name: presentation-design
description: Plan and design a presentation or slide template - pitch deck, credentials, proposal, brand presentation. Use when the user asks for a deck, slides, presentation, pitch, or a PowerPoint/Keynote/Google Slides/Canva template.
---

# Presentation design

Covers stage 7: `07-presentations/`. Lead: presentation-designer agent.

## Steps

1. **Define the job.** Audience, what they should decide or do, how it is delivered (presented live, sent to read, or both), duration, format (PPTX, Keynote, Google Slides, Canva, PDF), aspect ratio, and language.
2. **Storyline.** Write `07-presentations/storyline.md`: the single takeaway, then one line per slide where the title states the point. Start from `templates/presentations/storyline.md`.
3. **Get the storyline approved** before designing.
4. **Build the master.** Title, section, content, image, data, quote and closing layouts on the brand grid with brand colours and fonts.
5. **Design the slides.** One idea per slide; charts redrawn in brand style; real images; consistent margins. A deck sent to read may carry more text than one presented live; decide which it is.
6. **Arabic decks** are right to left throughout, including masters, bullets, chart axes and animation direction.
7. **Export** the source plus a PDF; package or list the fonts.
8. **Quality gate.** Run `quality-control` with `design-checklist.md`.

Specialist skills: `pptx`, `collateral-design`, `theme-factory`, `huashu-design` (HTML slides); Canva connector for Canva decks.

## Done when

- A reader of only the slide titles understands the argument
- The file opens with correct fonts on another machine
- The deck fits the time available (roughly one to two minutes per slide when presented)
