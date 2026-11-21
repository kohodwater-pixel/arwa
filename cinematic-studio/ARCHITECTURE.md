# Cinematic Studio — Architecture

Windows 10/11 desktop application for directing, generating, editing and exporting cinematic AI video.
Projects and media stay on the user's computer. Generation runs on a ComfyUI server the user configures
(their own machine or an on-demand cloud GPU).

## Fixed decisions

| Area | Decision |
|---|---|
| Desktop shell | Tauri 2 |
| Interface | React 19, TypeScript, Vite, Tailwind CSS 4 |
| Backend | Rust |
| Database | SQLite (`rusqlite`, bundled) |
| Local processing | FFmpeg, run as a separate program |
| Generation | ComfyUI HTTP API and WebSocket |
| Models | Wan 2.2 first (TI2V-5B, I2V-A14B 4-step); HunyuanVideo 1.5 later |
| Cloud GPU | On demand only, sized for NVIDIA RTX A6000 48 GB; first provider RunPod |
| LoRA | Trained outside the app with Musubi Tuner; managed here |

### Documented deviation: secrets are kept in Windows Credential Manager, not Tauri Stronghold

The specification allows "Tauri Stronghold or an equivalent secure mechanism". This app uses the
Windows Credential Manager through the `keyring` crate, for these reasons:

- Stronghold encrypts a vault file with a password. A desktop app with no login has to keep that password
  somewhere on the same disk, which protects little. Credential Manager encrypts with the Windows account
  (DPAPI), so another Windows user or a copied project folder cannot read the keys.
- The secret store is called only from Rust. The interface can store or delete a secret and see
  whether one exists; there is no command that returns a secret's value.
- Only two names are accepted: `comfy_token` and `gpu_api_key`.

## Layers

```
┌──────────────────────────── Tauri window (WebView2) ─────────────────────────────┐
│ React UI: 15 screens · director engine (rules, no network) · no keys, no file IO │
└───────────────┬──────────────────────────────────────────────┬───────────────────┘
        invoke('rpc', {cmd,args})                     studio://localhost/file?path=
                │                                              │ (read-only, allow-listed)
┌───────────────▼──────────────────────────────────────────────▼───────────────────┐
│ src-tauri (thin shell): one command, one URI scheme, dialogs, single instance     │
└───────────────┬───────────────────────────────────────────────────────────────────┘
┌───────────────▼───────────────────────────────────────────────────────────────────┐
│ crates/core  (studio_core — no Tauri dependency, fully tested on any OS)           │
│  rpc        allow-list of ~50 commands, one validation point                       │
│  projects   projects, scenes, snapshots, backup, import/export, integrity          │
│  media      library records, hashing, thumbnails, duplicate detection              │
│  comfy      client (HTTP + WebSocket) · one adapter per model (wan22)              │
│  jobs       queue worker: submit, track, cancel, retry, download, validate         │
│  gpu        provider trait · RunPod · approval, budget, idle shutdown, ledger      │
│  timeline   timeline JSON → FFmpeg arguments → export                              │
│  lora       LoRA library, datasets, training records                               │
│  secrets    Credential Manager · files  read-only file policy · paths  safe joins  │
└───────┬──────────────┬───────────────────┬───────────────────┬─────────────────────┘
     SQLite      Windows file system     FFmpeg/ffprobe     HTTPS: ComfyUI, RunPod
```

Why the core is a separate crate: every rule that matters (budget, approval, path checks, job state)
is compiled and tested without a window, on Linux and on Windows. The shell is about 90 lines.

A development bridge (`crates/core/src/bin/dev_bridge.rs`, feature `dev-bridge`) serves the same `rpc`
over HTTP on 127.0.0.1 so the interface can be driven by a browser test. It is not part of the installer.

## Screens

Dashboard · New Project · AI Video Creator · Cinematic Prompt Editor · Storyboard Studio · Scene Editor ·
Timeline Editor · Video Preview · Audio Studio · Media Library · Model Manager (with LoRA) · GPU Manager ·
Render Queue · Export Center · Settings. Arabic (right-to-left) and English (left-to-right).

## Cinematic Director Engine (`src/director/`)

Rule-based, runs in the interface, uses no network and no model.

1. `engine/lexicon.js` recognises concepts in Arabic and English text (subjects, places, time, weather,
   light, mood, camera cues).
2. `engine/analyze.js` takes the directing decisions from those concepts (for example: night + city + rain
   → practical neon lighting; moving subject → tracking shots).
3. `index.ts` exposes the twelve decisions — Main Subject, Environment, Scene Composition, Camera Movement,
   Camera Angle, Lens, Lighting, Color Grading, Motion Description, Atmosphere, Visual Style, Negative
   Instructions — all in English and all editable.
4. `engine/storyboard.js` splits the film into scenes that fit the model's longest clip.
5. A **prompt profile per model** writes each scene's prompt:
   - Wan 2.2 TI2V-5B: descriptive prose (shot, action, subject, setting, light, motion, colour, lens);
     negative prompt sent separately.
   - Wan 2.2 I2V-A14B 4-step: motion and camera only, because the reference image fixes the look; the
     negative prompt is not used (the workflow runs at CFG 1).

It is not a translator. Arabic the lexicon does not recognise is reported as a warning; Arabic text is
never sent to the model.

## Generation flow

```
Storyboard → generate → job (queued) → worker:
  budget check → GPU running? → ComfyUI reachable + authenticated?
  → preflight (nodes and model files present on the server, enabled LoRA present)
  → upload reference image (if any) → POST /prompt → WebSocket progress + /history polling
  → GET /view download to <file>.part → rename → ffprobe + full decode → thumbnail
  → scene = completed
```

- A job is successful only after the file is downloaded and decodes from start to end.
- Waiting causes (server not configured, unreachable, GPU stopped, budget used up) put the job in
  `blocked`; it is retried automatically. Real errors mark it `failed` with the server's message.
- After a crash, running jobs go back to `queued` and re-attach to their server job id, so nothing is
  submitted twice.
- The app never starts a GPU by itself.

## Adding a model

Implement `ModelAdapter` (`info`, `workflow`, `output_node`) in `crates/core/src/comfy/`, add it to
`adapters()`, and add a prompt profile in `src/director/index.ts`. Limits (frame rate, frame-count rule,
sizes, files, nodes, LoRA family) come from the adapter; the interface shows only what the adapter lists.

## FFmpeg

Looked for in this order: the folder chosen in Settings, the copy bundled with the installer, `PATH`.
Arguments are always passed as a list (never through a shell). The timeline is JSON; `timeline::plan`
turns it into arguments (trim, concat or `xfade`, `eq` colour, `amix`, H.264/AAC, `+faststart`) and is
unit-tested without running FFmpeg. Four tracks: video, audio, voiceover, music.

The bundled FFmpeg is a GPL build run as a separate program. Its licence file is installed next to it.

## What is verified and what is not

See `DEVELOPMENT_PLAN.md`. In short: the core, interface and export pipeline are tested; the ComfyUI and
RunPod integrations are tested against protocol doubles written from the official sources, **not yet
against a live server**. No video has been generated by Wan 2.2 through this app yet.

## Connecting a ComfyUI server safely

ComfyUI has no authentication of its own. Do not expose its port to the internet.

- On this computer: `http://127.0.0.1:8188` (the only case where plain http is accepted).
- On a cloud GPU: put a reverse proxy in front of it that terminates HTTPS and requires
  `Authorization: Bearer <token>` on every request including the WebSocket; store that token in
  Settings. The app refuses `http://` for any host other than localhost.
- Model files for the chosen adapter go in the server's `models/diffusion_models`, `models/text_encoders`,
  `models/vae` and `models/loras`. The Model Manager lists the exact file names and shows which are missing.

## Updates

The installer is NSIS, per user. Installing a newer version over an older one upgrades in place and
keeps the library. In-app automatic updates (Tauri updater) are not enabled yet: they need a signing key
and a release host, which are the owner's decisions.
