# Motion brief — logo animation

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS. Identity v01 is accepted for the system test only.

**Date:** 2026-11-13  **Prepared by:** Graphic Designer (concept given by the Creative Director in the round-2 brief; reviewed and approved by the art-director on 2026-11-13, see `art-director-review.md`)  **Version:** v02 (supersedes `motion-brief.md` v01, which is kept unchanged)

| | |
|---|---|
| Objective | Introduce the primary logo in motion and show the idea behind it: seven beats in the week, one of them yours |
| Audience | Independent café owners in Riyadh first; home brewers second |
| Single message | The week has seven beats and one is lit |
| Platform | Social (square feed video, profile intro); may also open or close longer films. No platform was specified: **assumption** |
| Duration | 3.0 s, 30 fps, 90 frames |
| Size | 1080 × 1080 px (1:1) |
| Background | Solid Paper `#F3ECE0` |
| Language | Arabic (the wordmark سدرة only; no other text) |
| Sound / voice | None. Works silent. No music, so no licence is needed |
| Deadline | None given |

## Motion rules used

- Bars and the Ember light arrive as hard-edged wipes. The wordmark alone fades in by opacity, whole, in 0.5 s or less.
- One easing for every move: cubic ease-out.
- The Arabic wordmark arrives as one whole piece, never letter by letter and never as a partial wipe.
- The bar row keeps its order and its count: seven bars, the fourth lit. The bars draw from right to left, the Arabic reading direction.
- The film ends on the static primary logo, held for at least one second.
- The source honours `prefers-reduced-motion` by showing the final logo only.

## Rules set by the art-director (2026-11-13)

Recorded from `art-director-review.md`; that file is the authority if the wording differs.

**Bar build (ruling 1).** "Always seven" governs every resting state of the row. A build-in is a transition and is allowed when all of these hold:

- Each bar appears in its final position and at its final size. No sliding, scaling, bouncing, rotating or swapping.
- Bars appear in the reading order of the lockup: right to left for the Arabic and bilingual lockups, left to right for the Latin-led lockup.
- First bar to seventh takes no more than 1.0 s.
- No hold on a partial count: any moment where nothing moves for 3 frames or more (0.1 s at 30 fps) shows seven bars or none.
- Ember does not appear until all seven bars are present. Only the fourth bar ever takes Ember. No bar flashes, pulses or lights in passing.
- No still, poster, thumbnail or cover is ever taken from the build.

**Wordmark fade (ruling 2).** "No tints" stands for every static layout and every held frame. The fade is a narrow exception, for the wordmark only:

- Opacity fade of the complete wordmark as one piece. Never letter by letter, never a wipe, blur, scale or slide.
- 0.5 s at most, never paused or held part-way.
- The bars and the Ember light never fade.
- No frame from inside the fade is used as a still.
- The logo does not fade out at the end. The film ends on the held logo.

**First frame and poster (ruling 3).**

- An empty Paper lead-in of up to 0.1 s (3 frames) is acceptable in the master file.
- The film ships with a poster frame: the final held frame, 1080 × 1080, sRGB PNG, saved beside the MP4.
- The poster is the cover wherever a cover can be chosen and the `poster` attribute on any web embed.
- Where no cover can be set and the first frame is the preview, the film is not used; the static logo is used instead.
- The end hold on the complete logo is at least 1.0 s.

**Craft notes.**

- The bars stay in their final logo position throughout, below the optical centre of the square. They are not centred and then moved.
- The Ember fill may be shortened from 0.26 s to 0.20 s only if the Ink sliver at the top of the fourth bar reads as a flicker when the film is watched played. See `notes.md`, round 3, for the frame check and the v02 candidate.

## Limits

Code-driven animation only (HTML and SVG rendered to video). No footage, no voice-over, no 3D, no sound.
