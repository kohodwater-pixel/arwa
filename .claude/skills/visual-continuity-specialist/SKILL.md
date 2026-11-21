---
name: visual-continuity-specialist
description: Keep characters, wardrobe, locations, lighting and colour consistent across separately generated scenes in the text-to-video platform in video-platform/. Use when scenes look like unrelated videos, when building a character or visual reference, when working on reference images, frame chaining or the continuity block in prompts, or when the user says "استمرارية", "ثبات الشخصية", "continuity", "character reference".
---

# Visual continuity specialist

Every scene is generated on its own, by a model that remembers nothing. Continuity is whatever you write down and feed back in. You have three tools, in order of strength.

## 1. The continuity block (always)

A fixed text repeated word for word in every scene prompt.

- **Character Reference** — per character: age, build, face, hair, wardrobe item by item with colours, accessories. For objects: make or type, colour, material, distinguishing details.
- **Visual Reference** — location with its fixed features, time of day, weather, lens, colour grade.

Write it once, as specifics a stranger could draw from. "A woman in elegant clothes" drifts; "a woman in her thirties, shoulder-length black hair, ivory linen blazer over a black top, thin gold necklace" holds. If the brief does not say, choose once and keep it; do not leave it open.

In code: `continuity` in the treatment (`server/engine/analyze.js`), or `subject_lock` and `location_lock` from the AI director (`server/engine/llm.js`). `compileScenePrompt` places it right after the key elements so it survives short prompt limits.

## 2. Reference images (when the provider tier supports image-to-video)

A scene can start from an uploaded image (`scenes.reference_asset_id`). Use it to pin the hero subject or the location in the scene where it first appears. Check `imageToVideo` for the tier; Luma reads images by URL and needs `PUBLIC_BASE_URL`.

## 3. Frame chaining (when cuts should feel continuous)

With `options.chainFrames`, each scene starts from the last frame of the previous one (`lastFrame` in `server/ffmpeg.js`, used by `sceneJob` in `server/pipeline.js`). Strongest match of light and colour, but generation becomes sequential, an error in one scene carries into the next, and every cut becomes a continuation. Do not use it when the storyboard changes location or shot size sharply between scenes.

## Review checklist for a generated film

Compare each scene against scene 1, then against its neighbour:

1. Same face, hair, wardrobe, colour of the hero object
2. Same location features; same time of day and weather
3. Same grade and contrast; no scene visibly warmer, cooler or flatter
4. Screen direction: a subject moving left to right keeps doing so
5. Lens feel: no jump from anamorphic wide to telephoto without a reason

A scene that fails is regenerated alone (`POST /api/projects/:id/scenes/:sid/generate`); the film is re-assembled automatically. Tighten the continuity block first if two scenes fail the same way.

## Limits to state plainly

Text-only continuity reduces drift; it does not guarantee an identical face. For a recurring human character, a reference image or frame chaining is needed, and the user should be told which was used.
