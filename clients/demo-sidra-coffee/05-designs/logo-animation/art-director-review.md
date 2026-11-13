# Art-director review — logo animation v01

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS. Not client-ready.

**Date:** 2026-11-13  **Reviewer:** Art Director  **Answers:** quality review r2, issue N2 (major) and the art-direction part of N3
**Reviewed:** `motion-brief.md` v01, `storyboard.md` v01, `notes.md` v01, `demo-sidra-coffee_logo-animation_primary_ar_v01.mp4`, and the `T` timing object in the HTML source.

## Verdict

**APPROVED — concept, storyboard and the v01 MP4. No re-export of the film is required.**

Two companion items are required before the piece can go to quality review round 3. They do not change the film:

1. A poster frame (see ruling 3).
2. A `storyboard_v02.md` that records this approval and the wording corrections in "Exact changes" below.

## How I reviewed it

- Extracted six frames from the MP4 with ffmpeg at 0.0, 0.5, 1.0, 1.3, 1.7 and 2.9 s into `_work/ad-review/` (`frame_t0.0.png` … `frame_t2.9.png`, plus `contact-sheet.png`) and looked at each one.
- Sampled the dominant colours of each frame with Pillow.
- Read the timings in the source: bars start 0.10 s, 0.12 s apart, 0.22 s each; lit bar 1.14 to 1.40 s; wordmark 1.50 to 2.00 s; one cubic ease-out throughout.
- **Not done:** I did not watch the film played in motion. No player is available in this environment. The feel of the timing is judged from the numbers and six stills, the same limit the maker and the quality-reviewer reported.

## What the frames show

| Time | What I saw |
|---|---|
| 0.0 s | Empty field, one colour only: 243 234 223 (Paper target 243 236 224, within video tolerance) |
| 0.5 s | Three complete Ink bars and a fourth half-drawn, on the right half of the row's final position. Nothing else on screen |
| 1.0 s | Seven Ink bars in final position, none lit |
| 1.3 s | Seven bars; the fourth is Ember with a thin Ink sliver still at its top edge (the fill rising from the bottom, hard edge). Ember samples as 194 57 32 |
| 1.7 s | Seven bars, fourth in Ember; the wordmark سدرة whole, connected, both dots of the ة present, in a warm grey of about 76 71 68 (Ink at roughly 78% opacity) |
| 2.9 s | The primary logo, centred, in Ink and Ember, clear space generous |

## Concept — first

The concept is on direction. The approved idea is "the week has seven beats and one of them is your roast". Seven beats arriving in turn, then one lighting, then the name, is that sentence in three seconds, and it uses nothing outside the system: flat colour, the rule row, the outlined wordmark, Paper. The bars arrive right to left, which is right for an Arabic-led mark. The lit bar is lit only after all seven are present, so the build does not suggest that the fourth day "arrives" in sequence or that the bars are a progress meter. I would have set the same sequence.

## Rulings

### 1. Partial bar count during the build — ALLOWED, with conditions

The rule "always seven, never change the count" governs any **resting state** of the bar row. A build-in is a transition towards that state, not a version of the logo. It is allowed when all of the following hold:

- Each bar appears in its final position and at its final size. Bars do not slide, scale, bounce, rotate or swap places.
- Bars appear in reading order of the lockup: right to left for the Arabic and bilingual lockups, left to right for the Latin-led lockup. No other order.
- The whole build, first bar to seventh, takes no more than 1.0 s.
- **No hold on a partial count.** Any moment where nothing moves for 3 frames or more (0.1 s at 30 fps) must show either seven bars or none.
- Ember does not appear until all seven bars are present. Only the fourth bar ever takes Ember. No bar flashes, pulses or lights in passing.
- No still, poster, thumbnail or cover image is ever taken from the build.

v01 meets every condition: the build runs 0.10 to 1.04 s (0.94 s), and its two pauses (1.04 to 1.14 s and 1.40 to 1.50 s) both show seven bars. The 0.5 s frame with three and a half bars is therefore acceptable.

### 2. Whole-word fade of the wordmark — ALLOWED, as a narrow exception

"No tints" stands for every static layout and for every held frame of a film. The fade is allowed as a transition, for the wordmark only, for this reason: it is the only reveal tried that keeps the Arabic word whole. The maker's first attempt, a wipe, hid the dots of the ة half-way through, so the word read as «سدره». A wrong word for a quarter of a second is worse than a grey one. Conditions:

- Opacity fade only, of the complete wordmark as one piece. Never letter by letter, never a wipe, blur, scale or slide.
- 0.5 s at most, never paused or held part-way.
- The bars and the Ember light never fade. They arrive by hard-edged wipes only.
- No frame from inside the fade is used as a still.
- The logo does not fade out at the end. The film ends on the held logo.

v01 meets these. The grey at 1.7 s is a passing state and I accept it.

The motion brief's own line "flat colour only … with no blends" is therefore inaccurate for the wordmark and must be corrected in wording (see below).

### 3. Empty first frame — ACCEPTABLE in the film; a poster frame is mandatory

An empty Paper lead-in of up to 0.1 s (3 frames) is acceptable in the master file. The idea needs the field to start empty, and starting on the finished logo would spend the reveal before it begins. The file does not have to start or hold differently.

It is not acceptable as the image a viewer sees before playing. So:

- The film ships with a poster frame: the final held frame, exported as a 1080 × 1080 sRGB PNG, named `demo-sidra-coffee_logo-animation_primary-poster_ar_v01.png`, saved beside the MP4.
- The poster is set as the cover wherever a cover can be chosen, and as the `poster` attribute on any web embed.
- Where no cover can be set and the first frame is shown as the preview, this film is not used; the static logo is used instead.
- The end hold on the complete logo is at least 1.0 s. v01 holds 1.0 s, which is the minimum, not a target; a longer version may hold longer.

### 4. Storyboard — APPROVED

`storyboard.md` v01 is approved as built, scenes 1 to 7, with the timings in its table. The process fault the reviewer recorded (animated before art-director approval) is real and is noted here; it does not change the result, because the sequence is one I approve.

## Exact changes required

No change to the MP4 or the HTML source.

| # | What | Who |
|---|---|---|
| 1 | Export the poster frame named in ruling 3 from the last frame and view it | graphic-designer |
| 2 | Save `storyboard_v02.md`: status line changed to "Approved by the art-director 2026-11-13, see `art-director-review.md`"; the two notes on the empty first frame and the fade replaced by a reference to rulings 3 and 2; add the poster file to the notes | graphic-designer |
| 3 | Save `motion-brief_v02.md`: "Prepared by" line updated to record this review; the rule "flat colour only: … no blends or glows" reworded to "Bars and the Ember light arrive as hard-edged wipes. The wordmark alone fades in by opacity, whole, in 0.5 s or less"; platform still marked as an assumption | graphic-designer |
| 4 | Record in `notes.md` (as a v02 or an added dated section) that the film is still not watched in motion by anyone, until someone does | graphic-designer |

The earlier files stay as they are; these are new versions.

## Craft notes, not blocking

- At 1.3 s the Ember fill leaves a thin Ink sliver at the top of the fourth bar for a few frames. It is a correct consequence of a bottom-up hard-edged fill and I accept it. If it reads as a flicker when someone finally watches the film played, shorten the fill from 0.26 s to 0.20 s. Do not change it on my guess.
- The bars alone, from 0.1 to 1.5 s, sit below the optical centre of the square because they are in their final logo position. That is the right choice; do not centre them and then move them.
- The film uses the primary logo `…_logo_primary-colour_ar_v01.svg`. That is still the current primary: identity v02 changed the icon only. No update needed.

## Not verified

- Playback in motion, on a phone, and inside any social platform.
- Whether platform re-encoding shifts Ember further than the 1 to 2 levels already measured.
- The platform itself: none was specified in the brief.
