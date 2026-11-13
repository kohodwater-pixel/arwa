# Creative direction — amendment 02

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Amends:** `creative-direction.md` v01 and `creative-direction-amendment-01.md` (both unchanged)  **Date:** 2026-11-13  **Prepared by:** Art Director
**Authority:** round-3 rulings (j) to (m) and the distinctiveness row in the decision log of `brand-context.md`; quality review r2 issues N2, N4, N5, N7, N12, N13; my review in `05-designs/logo-animation/art-director-review.md`.
**How to read:** where this amendment differs from the direction or amendment 01, this amendment wins. Everything not mentioned stands.

## 1. Motion rules (new section; qualifies section 4 "never animated out of order")

The static rules describe resting states. In motion, the following applies to every film, animated slide and web animation.

**Bars**
- A bar row may build in. During a build, fewer than seven bars may be visible.
- Each bar appears in its final position and at its final size, by a hard-edged wipe or a hard cut. Bars never slide, scale, bounce, rotate, swap places or fade.
- Order: the reading order of the lockup. Right to left for the Arabic and bilingual lockups and for Arabic layouts; left to right for the Latin-led lockup and English-only layouts.
- A full build of seven takes 1.0 s at most.
- **No hold on a partial count.** Any moment where nothing moves for 0.1 s or more shows seven bars or none.
- Bars do not build out. A piece ends on the complete row.

**The lit bar**
- Ember appears only after all seven bars are present, and only on the fourth bar.
- It arrives by a hard-edged fill (bottom up) or a hard cut, in 0.3 s at most. No colour blend, glow, pulse or flash.
- No other bar lights at any moment, even in passing. The light never travels along the row. This keeps ruling (f): the row is not a counter, a progress bar or a calendar.

**The wordmark and type**
- The Arabic wordmark arrives whole: by an opacity fade of the complete word in 0.5 s at most, or by a hard cut. Never letter by letter and never by a wipe, because a partial wipe hides the dots of the ة and misspells the name.
- This fade is the only exception to "no tints", and it applies to transitions only. Live Arabic text follows the same rule: whole lines, by fade or cut.
- Nothing is held part-way through a fade.

**Holds, first and last frames**
- A film ends on the complete, static logo, held for at least 1.0 s. No fade-out.
- An empty Paper lead-in of up to 0.1 s is allowed.
- Every film ships with a poster frame taken from the final hold. Stills, covers and thumbnails are never taken from a build or a fade. Where a platform shows the first frame and no cover can be set, use the static logo instead of the film.

**General**
- One easing for every move: cubic ease-out.
- Flat colour and square corners as in static work; no blur, shadow, gradient or texture.
- Films work silent. Sound is added only with a recorded licence.
- Web and app motion honours `prefers-reduced-motion` by showing the final state only.

The logo animation v01 complies and is approved; see `05-designs/logo-animation/art-director-review.md`.

## 2. Icon v02 confirmed (replaces the icon line in section 5 of the direction)

The direction asked for "the seven bars in band proportion inside a square", one row. I confirm the identity-designer's v02 in its place:

- **Icon:** three band rows of seven bars, stacked, filling a square. Row gap equals the bar gap. The fourth bar of each row is lit, so the three lit bars form one centre column.
- It is the pattern rule of section 4 (three rows minimum, lit bars aligned in one column) cropped to a square, not a new device.
- Use from 48 px; from 16 to 47 px the `icon-small` version; ladder as in amendment 01 section 3.
- The single-row icon v01 is superseded and is not used.

**Misuse-rule exemption.** The misuse rules "always seven bars" and "never light more than one bar" are counted **per row**. The following wording is to be added to the misuse page of the guidelines and to `brand-context.md` section 5:

> **Stacked pattern and icon.** Each row always has seven bars and one lit bar, the fourth. The pattern and the icon stack three or more identical rows, so they show more than seven bars and more than one lit bar in total. This is correct. The lit bars must line up in one centre column. Never light two bars in the same row, never stagger the lit bars from row to row, and never stack fewer than three rows.

## 3. Ember on web: one primary action button per screenful — ruling (l)

- On a web page, Ember may fill **the single primary action button in each screenful**, in addition to the lit bar.
- A screenful is what is visible at once without scrolling, at 1440 × 900 and at 390 × 844. Check both.
- Button: Ember fill, Paper label (4.56:1), square corners, no shadow. Label in Medium 500 or heavier.
- Every other button in the same screenful is Ink: Ink fill with Paper label, or a 2 px Ink outline with Ink label on Paper or Crema.
- A header button that stays on screen while scrolling is always Ink, so that it never becomes a second Ember button beside a section's own primary action.
- States use solid colours only, no tints: hover and pressed = Ink fill with Paper label; focus = 2 px Ink outline set 2 px outside the button.
- Ember is still never a body-text or link colour.
- **My reading, for the Creative Director to confirm:** within one screenful the Ember button takes the place of the "one Ember field or headline" allowed per layout. A screenful has the lit bar plus either one Ember button or one Ember field or headline, not both. Ruling (l) is silent on this; I recommend it so that a screen never carries three separate Ember elements.
- This applies to web and app screens only. Documents, slides, social and print keep "once per layout".

## 4. Social formats: type ladder at 1080 px wide — N12

**The 132 px Arabic headline on the social post v02 is approved**, for social formats 1080 px wide (1080 × 1080, 1080 × 1350, 1080 × 1920).

Reason: a 1080 px canvas is seen on a phone at about a third of its pixel size, so the screen steps in `system.md` (Arabic display 115 px) come out too small. The post already scales the whole ladder together, at 1.15 times the screen steps, which keeps the 1 : 1.6 : 5 proportions of the identity scale. I viewed the post: the hierarchy is clear and the headline holds the seven columns in two lines.

Fixed steps for 1080-wide social formats:

| Level | Arabic | Latin beside it |
|---|---|---|
| Display headline | **132 px** Bold, line height 1.3 | 115 px Bold, -1.5%, 1.05 |
| Sub-head | 42 px Medium, 1.5 | 37 px Medium, 1.3 |
| Body and call to action | 27 px Regular, 1.75 | 23.5 px Regular, 1.45 |
| Caption | 17.5 px Regular, Ash on Paper only | 15 px SemiBold, uppercase, +12% |

- 132 px is the maximum, not a starting point: a longer headline drops to the sub-head step or is rewritten shorter. No sizes in between.
- One display headline per post. No size above 132 px on any social format.
- These steps are for 1080-wide social formats only. Web, slides, documents and packaging keep their own ladders.
- The identity-designer records this ladder in `system.md` and `tokens.json` in their next versions, with the A4 ladder from amendment 01 section 9 (review N8).

## 5. Landing page, Ember on two buttons — N7 (art-direction part)

Follows from section 3: the landing page's sticky header button becomes Ink; the hero's wholesale-enquiry button may be Ember; any later section may carry one Ember button of its own when it is the only one in view. The call to action is a wholesale enquiry, per ruling (j).

## 6. Distinctiveness verdicts are no longer pending — N4, N5

- Amendment 01 "Still open", first bullet, is **closed**. Camel Step, Elixir Bunn and Brew92 are each **distinct** on home-page evidence. Elixir Bunn's red `#D92C20` is a sale label, not a brand colour. **Ember `#C23A20` is not revised.**
- I viewed the three captures and countersign the Creative Director's addendum. The current document is `distinctiveness-check_v02.md`; the earlier file with its addendum is kept as the record.
- The "Open points" line in `creative-direction.md` ("competitor visuals remain unverified; if Brew92 is found to use a strong red, Ember is reviewed") is also closed.
- Amendment 01 section 8 stands: the custom-drawn wordmark is required before real use.
- Not covered and still to be said wherever distinctiveness is claimed: home pages only; not a trademark search. The preliminary conflict check on the mark (review r1 issue 16) remains open and is not an art-direction item.

## 7. Latin line — closed

Amendment 01 "Still open", third bullet, is closed by the decision log: the Latin line stays "SIDRA COFFEE".

## Still open

- Caption floor of 9 px for screen-only pieces (amendment 01): my recommendation stands; no ruling yet.
- Confirmation of my reading in section 3 (Ember button replaces the Ember field or headline within a screenful).
- The logo animation has not been watched in motion by anyone. If the Ember fill reads as a flicker when it is, shorten it to 0.20 s.
- Arabic copy still needs a native proofread before delivery.
