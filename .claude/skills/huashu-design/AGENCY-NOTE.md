# Agency note

This copy of `huashu-design` was trimmed for Creative Agency OS:

- `scripts/cloud/` was removed. Those optional scripts sent narration text and video clips to third-party cloud APIs (ByteDance Doubao TTS and Volcengine Ark). Client material must not leave the agency's approved tools, so they must not be restored.
- The bundled background-music MP3 files in `assets/` were removed to keep the repository small.

Any step in `SKILL.md` that calls a cloud script or a bundled music track is unavailable here: skip it and say so. Running `npx skills update` would restore the removed files; do not run it for this skill without re-applying this trim.
