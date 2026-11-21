# Development plan and status

Status words used here:
**Verified** = run and checked. **Built, not yet proven live** = code and tests exist, but against a
protocol double, not the real service. **Open** = not done.

Last update: 2026-11-21.

| # | Phase | Status | Evidence |
|---|---|---|---|
| 1 | Project foundation (workspace, Tauri 2 shell, core crate, UI skeleton) | Verified | `cargo check`, `tauri build --debug`; the desktop app was launched under a virtual display and its interface reached the core |
| 2 | Windows desktop shell and installer (NSIS, shortcuts, icon, uninstall keeps projects) | **See "Windows installer" below** | `.github/workflows/cinematic-studio-windows.yml`, `tests/windows-install-test.ps1` |
| 3 | Local project system (SQLite, library folders, auto-save, recovery, backup, import/export, duplicate, delete, integrity) | Verified | core tests; browser test steps 1, 2, 16, 17 |
| 4 | Cinematic Director Engine (Arabic and English, twelve decisions, per-model profiles) | Verified | `src/director/director.test.ts` (7 tests) |
| 5 | Storyboard Studio (add, delete, reorder, edit, new take, regenerate one or all) | Verified | core `storyboard_editing`; browser test step 8 |
| 6 | ComfyUI integration (submit, track over WebSocket, cancel, retry, download, validate, failures) | **Built, not yet proven live** | core tests against a protocol double (HTTP + WebSocket) written from ComfyUI's source |
| 7 | Wan 2.2 generation | **Built, not yet proven live** | workflow graphs follow the official templates; never run on a GPU |
| 8 | Cloud GPU Manager (approval, budget 70/90/100%, idle shutdown, ledger) | Rules verified; RunPod calls **not yet proven live** | core `gpu_approval_budget_and_idle_shutdown` |
| 9 | Timeline and FFmpeg (trim, merge, transitions, colour, audio tracks, MP4 export, metadata) | Verified | core `export_renders_a_playable_mp4_with_audio_tracks`; browser test step 13 (real FFmpeg, output probed) |
| 10 | Media Library (import, thumbnails, search, filter, folders, metadata, duplicates) | Verified | core `media_library`; browser test step 11 |
| 11 | LoRA Manager (import, versions, per-model families, enable/disable, datasets, training records) | Verified (management only; the app never trains) | core `lora_library`, `enabled_lora_is_applied_only_to_its_family…` |
| 12 | Testing and release | In progress | this file |

## Tests

| Suite | Command | Count | Needs |
|---|---|---|---|
| Core (Rust) | `cargo test -p studio-core` | 18 | ffmpeg on PATH |
| Director engine | `npm test` | 7 | — |
| Interface, end to end | `npm run build && cargo build -p studio-core --features dev-bridge && node tests/e2e.mjs` | 18 steps | Chromium (Playwright), ffmpeg |
| Installer on Windows | `pwsh tests/windows-install-test.ps1 -Installer <setup.exe>` | 20 checks | Windows 10/11 |

The end-to-end test drives the real interface against the real Rust core, a real SQLite database and real
FFmpeg. The only stand-in is `tests/fake-comfy.mjs`, which answers ComfyUI's HTTP routes and returns a
test-pattern clip. It is a test tool: it is not shipped, and nothing it returns is a generated video.

## Acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Installs on Windows 10/11 | See "Windows installer" |
| 2 | Opens from the desktop shortcut | See "Windows installer" |
| 3 | Projects are saved and reopened after restart | Verified |
| 4 | An Arabic description becomes a cinematic prompt | Verified |
| 5 | A storyboard is created and can be edited | Verified |
| 6 | A real job is sent to ComfyUI | Built, not yet proven live |
| 7 | A real video is received from Wan 2.2 | **Open** — needs a ComfyUI server with the Wan 2.2 files |
| 8 | The video is saved in the project folder | Verified for the pipeline (download, validation, storage); with a real clip once 7 is done |
| 9 | Preview inside the app | Verified in the browser test (file served and loaded); playback in WebView2 to be confirmed on Windows |
| 10 | MP4 export | Verified |
| 11 | The project stays after restart | Verified (including after a forced kill) |
| 12 | GPU usage and cost are shown | Rules and ledger verified; live figures need a RunPod account |

## Windows installer

The installer is built and tested on a GitHub Actions Windows runner (this development environment is
Linux and cannot run a Windows installer). The workflow builds the NSIS installer, installs it silently,
checks the shortcuts, starts the app, checks that the library was created and the interface reached the
core, restarts it, uninstalls it, and checks that the user's projects are still there.

**Result of the latest run:** recorded in the final report of the session that pushed this file. Until a
run is green, phase 2 and acceptance criteria 1–2 are not passed.

## What needs the owner

1. A ComfyUI server with the Wan 2.2 TI2V-5B files (local GPU with 24 GB, or a cloud pod), reachable over
   HTTPS with a bearer token, to run the first real generation.
2. A RunPod account, one pod and an API key — and an explicit approval before the first paid start.
3. Decisions: code-signing certificate, update host, product identifier (`com.cinematicstudio.desktop` is a placeholder).

## Next steps after a first real generation

- Fix whatever the live ComfyUI run reveals in the Wan 2.2 graphs (most likely the SaveVideo codec field).
- HunyuanVideo 1.5 adapter and prompt profile (licence conditions in `video-platform/docs/self-hosted-engine-study.md`).
- Code signing; Tauri updater.
- Voiceover generation and waveform display in the Audio Studio.
