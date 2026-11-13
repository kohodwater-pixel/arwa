# Storyboard — logo animation

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Date:** 2026-11-13  **Version:** v02 (supersedes `storyboard.md` v01, which is kept unchanged)  **Status:** Approved by the art-director 2026-11-13, see `art-director-review.md`. Total 3.0 s at 30 fps, 1080 × 1080, Paper background, no sound.

The scenes and timings below are those of the approved film, `demo-sidra-coffee_logo-animation_primary_ar_v01.mp4`. They are unchanged from storyboard v01.

| # | Time (s) | Length (s) | On screen | Motion | Text |
|---|---|---|---|---|---|
| 1 | 0.00 – 0.10 | 0.10 | Empty Paper field | None | None |
| 2 | 0.10 – 1.04 | 0.94 | The seven bars of the logo's rule row, in Ink, in their final position | Bars appear one by one from right to left. Each wipes in from its right edge in 0.22 s; starts are 0.12 s apart | None |
| 3 | 1.04 – 1.14 | 0.10 | Seven Ink bars | Short pause | None |
| 4 | 1.14 – 1.40 | 0.26 | Fourth bar turns Ember | Ember fills the fourth bar from the bottom up, hard edge, no colour blend | None |
| 5 | 1.40 – 1.50 | 0.10 | Six Ink bars, fourth in Ember | Short pause | None |
| 6 | 1.50 – 2.00 | 0.50 | Wordmark سدرة above the bars | The whole wordmark fades in by opacity as one piece | سدرة (logo artwork, not live text) |
| 7 | 2.00 – 3.00 | 1.00 | Static primary logo, 540 px wide, centred | Hold | سدرة |

Sum of lengths: 0.10 + 0.94 + 0.10 + 0.26 + 0.10 + 0.50 + 1.00 = 3.00 s.

## Notes

- The logo artwork is the approved `04-identity/02-logo/demo-sidra-coffee_logo_primary-colour_ar_v01.svg`; its geometry is copied unchanged into the animation.
- Clear space: the logo is 540 px wide, so the required clear space is 146 px; the nearest edge is 270 px away.
- Reading time: one word, visible in full for 1.0 s. The art-director set 1.0 s as the minimum end hold, not a target.
- **Empty first frame:** see ruling 3 of `art-director-review.md`. It is acceptable in the film (lead-in of up to 0.1 s); it is not acceptable as the image shown before playing, so the film ships with a poster frame.
- **Wordmark fade:** see ruling 2 of `art-director-review.md`. Allowed as a narrow exception, for the wordmark only.
- **Partial bar count during the build:** see ruling 1 of `art-director-review.md`. Allowed as a transition; never held and never used as a still.
- **Poster frame:** `demo-sidra-coffee_logo-animation_poster_ar_v01.png`, 1080 × 1080, sRGB profile embedded, the last frame (frame 89) of the v01 MP4. It is the cover wherever a cover can be chosen and the `poster` attribute on any web embed. Where no cover can be set and the first frame is the preview, the film is not used; the static logo is used instead. File name: the round-3 task named it `…_poster_ar_v01.png`; the art-director's review names it `…_primary-poster_ar_v01.png`. The task's name was used; the Creative Director decides which stands.

## Alternative under consideration (not approved)

`demo-sidra-coffee_logo-animation_primary_ar_v02.mp4` differs in scene 4 only: the Ember fill runs 1.14 – 1.34 s (0.20 s instead of 0.26 s), so the pause in scene 5 becomes 0.16 s. Every other timing is identical. It was made in round 3 after a frame-by-frame check of the fill; see `notes.md`, round 3. The art-director has not seen it and nobody has watched either version played.
