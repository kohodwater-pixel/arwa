# Database schema

One SQLite file: `<library>/cinematic-studio.db` (WAL mode, foreign keys on).
Schema source: `crates/core/src/db.rs`. Migrations are numbered and applied in order; `schema_version`
records the last one.

**Media bytes are never stored in the database.** It holds paths, hashes and metadata only.
Paths inside the library are stored relative to the library root, so the library can be moved.

## Library layout

```
Documents/Cinematic Studio/          (changeable in Settings)
├── cinematic-studio.db
├── Projects/<slug>-<id8>/
│   ├── project.json                 snapshot of the project, rewritten on every change (atomic)
│   ├── scenes/                      generated clips and previews;  _replaced/ holds earlier takes
│   ├── exports/                     exported films, each with a .json metadata file
│   └── refs/
├── Assets/
├── Models/loras/<family>/           imported LoRA files
├── Cache/thumbs/                    thumbnails (can be deleted; they are rebuilt)
├── Logs/
└── Backups/                         project backups (.zip);  Deleted/ holds removed projects and LoRA files
```

## Tables

| Table | Purpose | Key columns |
|---|---|---|
| `settings` | Key/value settings and session state | `key`, `value` |
| `projects` | One row per film | `name`, `description`, `video_type`, `style`, `aspect`, `duration`, `model_id`, `status` (draft, storyboard, generating, ready, exported), `folder`, `director_json`, `timeline_json`, `model_config_json` |
| `scenes` | Storyboard | `project_id`, `position`, `role`, `title`, `duration`, `description`, `prompt`, `negative_prompt`, `prompt_edited`, `camera_move`, `shot_size`, `camera_angle`, `lighting`, `reference_media_id`, `seed`, `status` (pending, queued, generating, completed, failed), `video_path`, `preview_path`, `video_duration`, `error` |
| `jobs` | Render queue | `project_id`, `scene_id`, `kind` (generate, export), `provider`, `model_id`, `status` (queued, blocked, submitted, running, downloading, succeeded, failed, canceled), `blocked_reason`, `remote_id`, `progress`, `stage`, `attempts`, `request_json`, `result_path`, `error`, timestamps |
| `media` | Media library records | `kind` (image, video, audio), `name`, `path` (absolute path of the user's original), `sha256`, `size`, `duration`, `width`, `height`, `fps`, `thumb_path`, `folder`, `project_id`, `missing`, `corrupted` |
| `exports` | Exported films | `project_id`, `path`, `preset`, `width`, `height`, `duration`, `size`, `status`, `metadata_json`, `error` |
| `loras` | LoRA versions | `name`, `family`, `specialty`, `version`, `file_path`, `sha256`, `size`, `trigger`, `strength`, `enabled`, `trainer`, `source`, `notes`; unique (`name`, `family`, `version`) |
| `lora_datasets` | Registered training folders | `name`, `specialty`, `folder`, `rights_note` (required), `clip_count` |
| `lora_training_runs` | Training records (the app never trains) | `dataset_id`, `lora_id`, `family`, `tool`, `status` (planned, approved, recorded), `approved_by`, `estimated_cost_sar` |
| `gpu_sessions` | Cost ledger | `provider`, `instance_id`, `started_at`, `stopped_at`, `rate_usd_per_hour`, `usd_to_sar`, `approved_by`, `stop_reason` |
| `audit_log` | Approvals, GPU starts/stops, budget and secret changes (never secret values) | `ts`, `level`, `event`, `message` |

## JSON columns

- `director_json`: the twelve directing decisions, the recognised concepts, the reasons, and warnings.
- `timeline_json`: `{ clips: [{ scene_id, trim_in, trim_out, transition: { kind, duration } }], audio: [{ id, media_id, track, start, volume, fade_in, fade_out, trim_in }], color: { brightness, contrast, saturation }, clip_audio_volume, output: { preset, fps, crf } }`

## Not in the database

- API keys and tokens: Windows Credential Manager.
- The library location: `config.json` in the app's configuration folder (so the app can find the database).

## Recovery

- Every edit is written when it is made (auto-save); there is no unsaved state to lose.
- `settings.session_open` is set at start and cleared on a clean exit. If it is still set at the next start,
  the app reports a recovery, puts jobs that were running back in the queue (keeping their server job id),
  and marks an interrupted export as failed.
- `project.json` in each project folder allows a project to be re-imported even without the database.
