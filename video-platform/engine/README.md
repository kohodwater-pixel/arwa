# Engine service — self-hosted video generation

A separate service from the web platform. It queues generation jobs, picks an open-source model, and hands
the job to a GPU worker. Study, licences, costs and design decisions: `../docs/self-hosted-engine-study.md`.

**Status:** runs end to end with the mock worker. No real model has been run yet; the model commands in
`worker/runners/` are built from each project's documentation and have not been executed on a GPU.

## Run (no GPU needed — mock worker)

```bash
# 1) engine (Node 22.13+, no dependencies)
ENGINE_API_KEY=<long random> ENGINE_WORKER_TOKEN=<another long random> node engine/server.js      # :4200

# 2) a worker (Python 3.10+, standard library only)
cd engine/worker && ENGINE_WORKER_TOKEN=<same token> python3 gpu_worker.py --config worker.mock.json

# 3) the platform, pointed at the engine
ENGINE_URL=http://127.0.0.1:4200 ENGINE_API_KEY=<same key> npm start
```

"Self-hosted engine" then appears on the Create page, labelled DEMO because only a mock worker is connected.

## On a GPU host

1. Install one model in **its own** Python environment, following that project's README (the models pin
   incompatible versions; see the compatibility table in the study). Download weights there.
2. Copy `worker/worker.example.json`, set the engine URL, the model's repo path, its Python and checkpoint paths.
3. `python3 gpu_worker.py --config worker.json --dry-run` prints the exact commands it would run. Compare
   them with the model's README before the first real job.
4. Start it with `ENGINE_WORKER_TOKEN` set. The worker connects out to the engine; no inbound port is needed.

## Settings

| Variable | Meaning |
|---|---|
| `ENGINE_API_KEY` | key the platform uses (required) |
| `ENGINE_WORKER_TOKEN` | token GPU workers use (required) |
| `ENGINE_PORT` | default 4200 |
| `ENGINE_DATA_DIR` | database, outputs, LoRA files (default `engine/data`) |
| `ENGINE_LICENSE_POLICY` | `commercial` (default): only models whose weights licence allows paid hosted use. `any`: no gate (research only) |
| `ENGINE_ACCEPTED_LICENCES` | comma-separated model ids with conditional licences whose conditions the owner has read and accepted, e.g. `hunyuan15` |

Put the engine behind HTTPS before exposing it to remote workers.

## Layout

```
server.js            HTTP API (platform routes and worker routes)
models/<id>.js       one provider per model: licence, variants, limits, plan()
lib/router.js        automatic model selection, with reasons
lib/jobs.js          queue, leases, retries, cancel
lib/loras.js         LoRA registry (versions, provenance, promotion gate)
lib/datasets.js      dataset management; cli.js is its command line
lib/eval.js          evaluation runs, technical gate, Bradley–Terry comparison
suites/*.json        fixed prompt suites: gulf_ads, luxury_real_estate, saudi_tourism
worker/gpu_worker.py worker agent; worker/runners/<id>.py builds each model's command
test/                node --test engine/test/*.test.js
```

## Adding a model

`models/<id>.js` (manifest + `plan()`), `worker/runners/<id>.py` (`build()` → argv), register the runner
in `worker/runners/__init__.py`, add a sample spec to `worker/sample_specs.json`, and a test.

## Datasets and LoRA in short

```bash
node engine/cli.js dataset:create tourism-v1 saudi_tourism
node engine/cli.js dataset:add tourism-v1 ./clips --source "own shoot 2026-11" --holder "Company" --license "owned"
node engine/cli.js dataset:list tourism-v1 --status pending
node engine/cli.js dataset:review tourism-v1 <itemId> --status approved --caption "…"
node engine/cli.js dataset:export tourism-v1 --trainer musubi-tuner --out ./exports
```

Train with the chosen trainer in its own environment, then register the result:
`POST /v1/loras`, `POST /v1/loras/<slug>/versions` (path, trainer, trainerCommit, datasetSnapshot),
run `POST /v1/eval/runs` with that version, and promote with `POST /v1/loras/<slug>/versions/<v>/status`.
