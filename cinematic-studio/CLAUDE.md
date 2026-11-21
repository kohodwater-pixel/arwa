# Cinematic Studio — working notes for Claude

A Windows desktop product (Tauri 2 + Rust core + React), separate from the agency's client work in the rest
of the repository. The agency rules about client folders and delivery packages do not apply to code here;
the honesty rules do.

Commands, layout and tests are in `README.md`. Status of every phase is in `DEVELOPMENT_PLAN.md`: update it
when something changes from "built" to "verified", and never mark a live integration verified without a real run.

## Standing rules (from the owner's specification)

- Monthly GPU budget 1,000 SAR; warn at 70% and 90%; refuse new generation jobs at 100%.
- Never start a GPU, a LoRA training run or any paid resource without the manager's explicit approval.
- No keys in JavaScript or interface files; secrets go through Rust into the Windows Credential Manager.
- ComfyUI is never exposed publicly without authentication and TLS; the app refuses remote `http://`.
- No mock data presented as a real result. Test doubles live in `tests/` and are labelled.
- A feature is shown as supported only if the connected model adapter lists it.
- Every command goes through the allow-list in `crates/core/src/rpc.rs`; no shell strings from user input.
- The build is not "successful" until install, launch and uninstall pass on Windows
  (`.github/workflows/cinematic-studio-windows.yml`).

## Where things go

- New rule or behaviour: the core (`crates/core`), with a test in `crates/core/tests/core.rs`.
- New model: an adapter in `crates/core/src/comfy/` and a prompt profile in `src/director/index.ts`.
- New screen action: one `rpc` command; the interface never touches files or the network itself.
- Pushing to this branch cancels a Windows build that is still running (workflow concurrency).
