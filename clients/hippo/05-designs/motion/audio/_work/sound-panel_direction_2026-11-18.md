# HIPPO franchise motion ad — sound panel ruling (direction), 2026-11-18
Art-director half of the panel. Decided from script v03, `build_mix.sh` and the v01 measurements; nobody listened. All times are film seconds.

## 1. Hook (0–3 s): quiet, fall, gap, one hit, then the voice alone
- 0.00–0.45: no music, no whoosh. Room tone only at about -45 dB, plus one tiny dry paper "tick" at 0.10 (about -26 dB) as «خفيف؟» appears. The quiet is what makes the hit big.
- 0.45–0.92: falling whoosh, 0.47 s (v01: 0.95 s). Shorter and steeper; it must rise in level right up to 0.92.
- 0.92–1.00: 80 ms of hard mute on everything (whoosh and room tone).
- 1.00: impact = sub + soft thud + paper-holder crinkle (see 3b). Keep it at 1.00 so picture sync does not move.
- 1.00–1.70: the sub tail rings alone. No music.
- 1.70: VO «خفيف؟… جرّب تشيله.» stays where it is (ends about 3.8).
- 3.00: music enters on the scene-2 cut, not on the impact. In v01 the music start masks the tail of the hit.
- Loudness order: the hook is the single loudest event, about -7 dB RMS. Box boom at 19.4 comes down to about -9; CTA hit at 29.6 to about -10/-11. The box stays the "heaviest" in character (lowest pitch, longest tail, cardboard layer), not in level.

## 2. Cup slide (scene 2): drop the slide, sound the stops
Delete `sfx_slide` and the x18 boost. A slide is quiet by nature; what the picture gives us is four stops and one touch on the bread.
- Prompt A (use 4 times, pitched up a step each time, about 1.00 / 1.06 / 1.12 / 1.19): "Small plastic sauce cup sliding a very short distance on a smooth matte tabletop and stopping with a soft hollow tap. Close microphone, dry, no reverb, no music, single event, 1 second."
- Prompt B (once, when the last cup touches the bread): "Soft squishy bread being gently pressed and released, pillowy squeeze with a tiny wet sauce blip. Close microphone, dry, no reverb, no music, 1 second."
- Level about -18 dB, each tap on a music beat. The first three taps go between 3.1 and 4.5, before the VO line at 4.6; the squish goes after the line ends (about 6.6). Exact frames must follow the picture.

## 3. Three additions against "dry" (voice stays dry and on top)
- a) Room tone and space: a continuous room-tone bed at about -45 dB for the whole film, lifted to about -38 dB during the music stop (24.0–28.7) so the silence breathes instead of dropping to digital zero. One short shared room reverb on the effects only. Move the riser to 28.70–29.52 (v01 starts at 27.35, on top of «ناقصها ثقلك», which ends about 28.64), then an 80 ms gap before the 29.6 hit, as in the hook.
- b) Paper and cardboard foley about 20 ms after each landing, at about -16 dB: holder crinkle at 1.02; carton taps on the five scene-5 landings (15.07–18.17); lid wobble and creak at 19.5–20.1. Prompt: "Thin paperboard food tray and small cardboard box being set down, short crinkle and soft creak, close microphone, dry, no reverb, several separate single hits."
- c) Sonic logo for the hippo blink, two sounds 120 ms apart: a soft round low "boop" (about 80 Hz, short) and a tiny high felt "tick" with a light ear-flutter. Place it on the blink. Recommended blink time is about 38.2, after the VO ends at about 37.9, so it lands in clear air. About -14 dB; it is the last sound of the film.

## 4. Music
- Must be true: instrumental only (no vocals, chants or vocal chops); percussion and bass led; open mid-range (1–4 kHz) for the voice; about 92 BPM so the scene-3 landings (every 1.3 s) fall on every second beat.
- Energy curve: light from 3.0; build 7–11; thin to kick and bass only 11–15 (typography); build 15–19; peak on 19.4; hard stop at 24.0; full return at 29.6; resolved by 33; soft tail under the end card to 40.
- Level is not a constant -19: about -22 under the voice, about -16 in the gaps (7–10, and 29.6–30.3).
- Regenerate if the v01 track has any voice in it, has no real ending, or cannot follow this curve. Prompt: "Instrumental only, no vocals. Playful, heavy, minimal percussion groove at 92 BPM: deep soft sub kick, hand claps, finger snaps, bouncy muted bass stabs, cheeky and confident. Lots of empty space in the midrange, dry and punchy, no cymbal wash, no lead melody. Builds for 20 seconds to a big downbeat and a clean stop, then a full confident final section ending on one hit with a short warm tail. 40 seconds."

## Open for the mix engineer
- Whether a 0.47 s whoosh can be cut cleanly from `sfx_hook` or needs regenerating.
- Beat alignment at 92 BPM: scene-5 landings are 0.8 s apart and will not sit on the same grid as scene 3. Proposal: align scene 3 and the 19.4 peak, let scene 5 run as a free accelerating roll.
- Cup-stop and blink frames depend on the animation timing, which this panel has not seen.
