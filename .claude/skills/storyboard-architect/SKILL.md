---
name: storyboard-architect
description: Split a film into scenes with durations, beats and per-scene descriptions, and keep the storyboard editable, for the text-to-video platform in video-platform/. Use when planning or reviewing a scene breakdown, when scene counts or durations come out wrong, when adding a narrative beat or video type, when editing server/engine/storyboard.js or the storyboard routes and page, or when the user says "storyboard", "تقسيم المشاهد", "مخطط المشاهد".
---

# Storyboard architect

Input: the director's treatment, the total duration, and what the selected provider tier can generate. Output: an ordered list of scenes the user can edit before anything is generated.

## Each scene carries

- a beat (`establish`, `hook`, `intro`, `context`, `human`, `detail`, `action`, `reveal`, `closing`, or `hero` for a one-shot film)
- a duration in whole seconds
- a description in the user's language: what is in frame, what moves, where the shot starts and where it ends
- shot size, camera move and angle
- optionally a reference image (first frame) and a voice-over line

## Rules

- **Durations sum exactly to the total.** Each scene is at most the tier's longest clip (`clip.max`); a scene shorter than the provider's shortest clip is generated longer and trimmed at assembly.
- **Scene count** follows the total (about 1 scene up to 6 s, 3 for 15 s, 5 for 30 s, 8 for 60 s) and never drops below `ceil(total / clip.max)`.
- **Order tells a story:** opening first, closing last, the closing frame leaves clean space for a logo or message. The opening beat depends on the video type (social opens on the hook, product opens on the product).
- **One scene, one shot, one action.** A scene that needs a cut is two scenes.
- **No two neighbouring scenes use the same camera move** unless the user chose it.
- **Visual sequence:** screen direction, time of day and location carry over from scene to scene. A change of place is written into the description of the scene where it happens.

## Editing must stay safe

The storyboard is edited through `server/routes/projects.js`. Keep these invariants when you touch it:

- editing a description, duration, camera move, shot size, reference or prompt drops that scene's generated clip and sends the project back to the storyboard stage
- reorder, add and delete renumber positions and recompile every prompt that the user has not edited by hand (`refresh`)
- a hand-edited prompt (`prompt_edited`) is never overwritten silently
- nothing is editable while the project is generating (HTTP 409)

## Where this lives in the code

- `video-platform/server/engine/storyboard.js` — `ROLES`, `TYPES`, `sceneCount`, `splitDuration`, `buildStoryboard`, `alternateScene`
- `video-platform/src/pages/Storyboard.jsx` — the editor (drag and buttons to reorder, new take, add, delete)
- `video-platform/test/engine.test.js` and `test/flow.mjs` — duration sums and editing flow

## Hand on

To visual-continuity-specialist: the scene list. Use camera-motion-specialist when a scene's move is in doubt.
