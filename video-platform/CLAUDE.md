# Video platform — working notes for Claude

This folder is a software product (Node.js + SQLite + React), separate from the agency's client work in the rest of the repository. The agency rules about client folders, brand files and delivery packages do not apply to code here; the honesty rules do.

Run, build and test commands are in `README.md`.

## Skill chain

Eight project skills in `.claude/skills/` cover the product's pipeline. They follow the order in which a video is made:

```
User description
  → cinematic-prompt-engineer      structure the brief; later compile the per-provider prompt
  → cinematic-director             look: style, lighting, colour, lens, camera language
  → storyboard-architect           scenes, durations, beats, editable plan
  → visual-continuity-specialist   character and visual reference, reference images, frame chaining
  → ai-video-integration-engineer  provider adapters, jobs, queue, retries, webhooks
  → video-pipeline-engineer        storage, trim, join, audio mix, MP4 export
  → fullstack-qa-engineer          run it and prove it
```

`camera-motion-specialist` is called from the director or the storyboard step when a scene's move is in question.

Use the one skill that matches the task, not the whole chain:

| Task | Skill |
|---|---|
| A prompt is weak, too long, or ignored by the model | cinematic-prompt-engineer |
| The look or lighting choice is wrong; new style or video type | cinematic-director |
| Scene count, durations, order, storyboard editing | storyboard-architect |
| Which camera move, or motion looks unnatural | camera-motion-specialist |
| Scenes do not match each other | visual-continuity-specialist |
| Provider API, keys, failed or stuck jobs, queue | ai-video-integration-engineer |
| Final film length, sound, size, format | video-pipeline-engineer |
| Before saying a change works | fullstack-qa-engineer |

A change that crosses stages (for example a new provider that also needs new prompt rules) uses the skills of those stages in chain order and ends with fullstack-qa-engineer.

General engineering skills installed in the repository (React, Node.js, API design, auth, testing, SQL, CI) and the Superpowers plugin (planning, TDD, debugging, review, verification) support these; they do not replace the product knowledge in the eight skills.

## Self-hosted engine

`engine/` is a separate service (own database, own port) that runs open-source video models on GPU workers; the platform reaches it through `server/providers/selfhosted.js`. Licences, costs, version pins and design are in `docs/self-hosted-engine-study.md`; how to run it is in `engine/README.md`. Model facts in `engine/models/*.js` come from each project's own repository at a recorded commit: re-read the source before changing them. The mock worker runs no model, and its output must stay labelled.

## Standing rules for this product

- No provider key in front-end code, logs, or API responses.
- No simulated generation presented as real. Demo output is always labelled.
- An option is shown as supported only if the connected provider's adapter lists it.
- A provider integration is "verified" only after a real call succeeded.
