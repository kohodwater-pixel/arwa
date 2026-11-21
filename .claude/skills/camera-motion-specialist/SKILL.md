---
name: camera-motion-specialist
description: Choose and describe the camera movement for a scene — dolly in/out, tracking, crane, drone, pan, tilt, orbit, handheld, static, slow motion — for the text-to-video platform in video-platform/. Use when a scene's camera move must be picked, justified or changed, when generated motion looks unnatural, or when editing the camera move catalog or the move-selection logic in server/engine/storyboard.js. Triggers include "حركة الكاميرا", "camera movement", "tracking shot", "drone shot".
---

# Camera motion specialist

One move per scene, chosen for what the scene has to do. The move is a reason, not decoration.

## Choosing

| Move (catalog id) | Use it when | Avoid it when |
|---|---|---|
| Dolly In (`dolly_in`) | attention should close on the subject; details; emotion | the subject is already moving fast toward camera |
| Dolly Out (`dolly_out`) | revealing surroundings; a closing frame with room for a logo | the scene is a tight detail |
| Tracking (`tracking`) | the subject travels: cars, runners, walking people | nothing in frame moves |
| Crane Up / Down (`crane_up`, `crane_down`) | a reveal of scale, or arriving into a scene | small interiors |
| Drone (`drone`) | landscapes, cities, architecture from outside | interiors and studio sets |
| Pan (`pan`) | showing the width of a place | a single small subject |
| Tilt (`tilt`) | revealing height: towers, a person head to toe | wide landscapes |
| Orbit (`orbit`) | products and hero subjects that should be seen from all sides | crowded scenes where the background would smear |
| Handheld (`handheld`) | documentary feel, human moments, energy | luxury, real estate, minimal and epic styles |
| Static (`static`) | the action in frame is the movement | the scene has no movement at all |

Slow motion is a modifier, not a move: use it on detail and action beats when there is something to see slowly (rain, dust, liquid, fabric). It doubles the apparent duration of an action, so the action must be short.

## Writing the move for a video model

- Name the move, its direction and its speed: "slow, smooth dolly-in toward the subject".
- Tie the camera to the subject for tracking: "moving alongside the car at matching speed".
- State one move only. Two moves in one prompt produce drift or warping.
- For short clips (5 s or less) prefer slow moves; a fast move has no room to start and stop.
- Add the stabilisation the style implies: gimbal-smooth for luxury, gentle sway for handheld.

## Signs the move is wrong

Background smearing on orbit, a subject that slides instead of travelling on tracking, horizon wobble on drone: change the move or slow it down before changing the provider.

## Where this lives in the code

- `video-platform/server/engine/catalog.js` — `cameraMoves` (id, Arabic and English label, prompt phrase)
- `video-platform/server/engine/storyboard.js` — `pickMove`: user cues first, then candidates per beat, no repeated move back to back, no handheld where the style forbids it
- adding a move: add it to `cameraMoves`, list it as a candidate in the beats where it fits, and add it to the table above
