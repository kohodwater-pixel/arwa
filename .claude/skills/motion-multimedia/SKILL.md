---
name: motion-multimedia
description: Plan and produce motion and multimedia - motion graphics, animated advertisements, presentation animations, logo animation and visual storytelling. Use when the user asks for animation, a motion graphic, an animated ad, a video, a reel, a logo sting, animated slides or a storyboard.
---

# Motion & multimedia

Service G. Output folder: `05-designs/<project>/`. Concept: art-director agent. Production: graphic-designer (ads, social, logo animation) or ui-ux-designer (web and UI motion); presentation-designer for slide animation.

## Steps

1. **Motion brief** → `motion-brief.md`: objective, audience, single message, platform, duration, aspect ratio (16:9, 9:16, 1:1, 4:5), language, whether sound or voice is needed, deadline.
2. **Script and storyboard** → `storyboard.md`: scene by scene — what is on screen, on-screen text (AR / EN), motion, duration. Total duration must add up. Get it approved before animating.
3. **Style frames:** two or three still frames in final quality, from the approved identity.
4. **Animate** with code so the result is editable: HTML + CSS/JS (or SVG animation) at exact pixel size.
5. **Render:** record with Playwright (Chromium) and encode with `ffmpeg` to MP4 (H.264, yuv420p, 30 fps); GIF only when asked. Keep the HTML source as the editable file.
6. **Check the render:** extract frames at the start, middle and end and look at them; confirm duration, size, that Arabic text is shaped and readable long enough (about one second per three words), and that the first frame works as a thumbnail.
7. **Quality gate:** run `quality-control`.

Specialist skills: `motion-design` (UI motion principles), `huashu-design` (HTML animation and MP4/GIF export), `art-direction`, `slack-gif-creator` (GIF constraints).

## By deliverable

| Deliverable | Typical spec |
|---|---|
| Logo animation | 2–4 s, ends on the static logo, works silent, transparent or solid background |
| Animated ad / reel | 6–15 s, 1080 × 1920 or 1080 × 1350, message readable without sound, CTA in the last 2 s |
| Motion graphic / explainer | 30–90 s, script first, one idea per scene |
| Presentation animation | Built into the deck's slide transitions and builds; purposeful, not decorative |
| Visual storytelling | A sequence (carousel, scroll story or film) with beginning, turn and resolution |

## Rules

- Motion serves the message: every movement directs attention or shows a relationship. Remove the rest.
- Use the brand's easing and timing consistently; respect `prefers-reduced-motion` on the web.
- Arabic text animates as whole words or lines, never letter by letter (it breaks the joins).
- Music, voice and footage need a licence the client can rely on; record it. Do not send client scripts or footage to third-party cloud services for voice or review without the user's explicit approval.

## Limits to state honestly

This system produces code-driven animation (HTML/SVG rendered to video). It does not shoot footage, record voice-over or do 3D. Say so when a request needs those.
