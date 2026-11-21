---
name: cinematic-prompt-engineer
description: Turn a plain video idea into a structured, provider-specific production prompt for the text-to-video platform in video-platform/. Use when writing or reviewing a prompt for Runway, Veo, Luma or Kling, when a generated clip ignores part of the brief, when changing server/engine/prompt.js or the lexicon, or when the user says "production prompt", "enhance the prompt", "برومبت إخراجي", "حوّل الوصف إلى برومبت".
---

# Cinematic prompt engineer

First and last link of the chain: you structure the raw brief at the start, and you compile the final per-scene prompt once direction, storyboard and continuity are settled.

`brief → [you: structure] → cinematic-director → storyboard-architect → visual-continuity-specialist → [you: compile per provider] → ai-video-integration-engineer`

## Output contract

Every prompt you write or review is checked against these fields. A field the brief does not cover is filled by the director's decision, never invented as new content (no brands, people, slogans or places the user did not mention).

| Field | What it holds |
|---|---|
| Main Subject | who or what, with colour, material, age, wardrobe |
| Environment | place, time of day, weather |
| Scene Description | one action with a start and an end, for one continuous shot |
| Camera Movement | one move from the catalog (see camera-motion-specialist) |
| Lens | focal length and type, depth of field |
| Lighting | scheme plus sources |
| Color Grading | grade and film look |
| Motion | speed and physics of subject and camera |
| Atmosphere | mood, particles, haze |
| Composition | shot size, angle, negative space |
| Negative Instructions | only as a separate field when the provider supports it |

## Rules that come from the providers

- A video model sees one scene's prompt and nothing else. Anything that must match across scenes is repeated in every prompt (the continuity block).
- Write the prompt in English. Keep the user's own words for names and proper nouns.
- Order by importance, because limits differ and the tail gets cut: shot → scene action → key elements → continuity → lighting → look → motion → quality.
- Respect the limit of the selected quality tier (`maxPromptChars` in `server/providers/<name>.js`). Shorten or drop the least important section; never cut a sentence in half. `compileScenePrompt` already does this — extend it, do not bypass it.
- Negative instructions: send them in the provider's own field when `negativePrompt` is true (Veo, Kling); otherwise fold a short "Avoid: …" line into the prompt (Runway, Luma).
- Models that generate sound (`nativeAudio`) get the audio direction appended; silent models never do.
- Describe what is seen, not what is meant. "Rain streaks across the windscreen" works; "a feeling of solitude" does not.

## Where this lives in the code

- `video-platform/server/engine/prompt.js` — `compileScenePrompt`, `compileMasterPrompt`, `negativePrompt`
- `video-platform/server/engine/lexicon.js` — Arabic/English cue detection; add stems here when a word is missed
- `video-platform/server/engine/llm.js` — optional AI director that supplies `action_en`, `subject_lock`, `location_lock`
- `video-platform/test/engine.test.js` — add a case for every prompt rule you change

## Check before handing on

1. All eleven fields are present or deliberately absent.
2. Length is within the tier limit, measured, not estimated.
3. The continuity block is identical in every scene of the film.
4. Nothing in the prompt is absent from the brief or the director's treatment.
