---
name: ai-video-integration-engineer
description: Build and maintain the integrations with AI video generation APIs (Runway, Kling, Luma, Google Veo) in video-platform/ — provider adapters, capability differences, generation jobs, the queue, retries, status polling and webhooks. Use when adding or fixing a provider adapter, when a generation job fails, hangs or is submitted twice, when a provider changes its API, or when the user says "ربط مزود", "provider", "adapter", "API key", "webhook", "queue".
---

# AI video integration engineer

## Ground rules

- **No key, no generation.** Nothing here works without the provider's official API key, and none of the providers is free. A provider without credentials is shown as "not configured"; it is never simulated. Only the `demo` provider renders placeholders, and those are stamped as demo.
- **The provider's own documentation or official SDK is the source.** Read it before writing or changing an adapter, and record in the adapter's header what was read, when, and which values are assumptions. Do not copy request shapes from memory or from another provider.
- **Keys stay on the server**: environment variables or the encrypted `provider_settings` table. They are never logged and never returned to the browser.
- **A call succeeded only when the provider answered.** Never mark a job as submitted, running or finished before the response says so.

## Architecture (video-platform/server)

```
routes/projects.js → pipeline.startGeneration → queue (SQLite) → sceneJob
        sceneJob: provider.submit → provider.poll … → download → storage → maybeFinish → assembleJob
```

- `providers/<name>.js` — one adapter per provider. `providers/index.js` is the registry; nothing else names a provider.
- `providers/http.js` — `request`, `ProviderError { status, code, retryable, retryAfterMs }`, `fitClip`.
- `queue.js` — durable jobs: `{ done }`, `{ again: ms }`, or throw. Retryable errors back off exponentially up to `max_attempts`; jobs that were running when the process stopped resume from their stored `provider_job_id`, so nothing is submitted twice.
- `pipeline.js` — per-provider concurrency (`maxConcurrent`), 30-minute timeout, download into our own storage (provider URLs expire), usage accounting.

### Adapter contract

```js
{ id, label, demo, verified: 'sdk' | 'unverified' | 'local', docsUrl,
  credentialFields: [{ key, label, env, secret, required }],
  qualities: () => [{ id: 'standard'|'high'|'ultra', label, resolution, aspects: { '16:9': <provider value> },
                      clip: { min, max, values? }, maxPromptChars, negativePrompt, imageToVideo: true|false|'url', nativeAudio }],
  maxConcurrent, minPollMs,
  submit({ prompt, negativePrompt, duration, aspect, quality, image, seed, wantAudio }, creds) → { jobId, clipDuration },
  poll(jobId, creds) → { status: 'pending'|'running'|'succeeded'|'failed', progress?, videoUrl?, downloadHeaders?, error?, retryable? },
  cancel?(jobId, creds), test?(creds) }
```

The UI builds its quality, aspect-ratio and duration options from `qualities()`. An option that is not in the table is not offered, so the table must describe what the API accepts today, per model.

## Providers differ — handle it in the adapter, not in the pipeline

| | Runway | Google Veo | Luma | Kling |
|---|---|---|---|---|
| Auth | Bearer + version header | API key header | Bearer | JWT signed from access + secret key |
| Clip length | range or fixed set per model | fixed set | fixed set, sent as a string | fixed set, sent as a string |
| Progress number | yes while running | no | no | no |
| Negative prompt | no | yes | no | yes |
| Reference image | data URI | inline base64 | public URL only | base64 |
| Result | URL list on the task | file URI, download needs the key | asset URL | URL in task result |

Values and model ids change; confirm them in the adapter header and the provider docs, not here. The Kling adapter is marked `unverified` until its documentation has been read.

## Errors

Map every failure to a `ProviderError`: 401/403 → `provider_auth` (not retryable, tell the admin); 429 → retryable, honour `retry-after`; 5xx and network → retryable; 400/422 and moderation blocks → not retryable, show the provider's reason to the user. A finished task with no video is a failure, not a success.

## Webhooks

The platform polls today. To add callbacks for a provider that offers them: expose `POST /api/webhooks/<provider>` outside the session and CSRF guards, verify the provider's signature or a per-job secret in the URL, look the job up by `provider_job_id`, make the handler idempotent, and set the job's `run_at` to now so the existing `poll` path does the state change. Keep polling as the fallback; a lost webhook must not strand a job.

## Adding a provider

1. Read the official docs or SDK; note the source and date in the file header.
2. Write the adapter; add it to the list in `providers/index.js`.
3. Add a contract test in `test/providers.test.js` (request body, every status, an auth error, a rate limit).
4. With a real key: admin panel → Test connection, then generate one short scene and watch the job in the admin jobs tab.
5. Update `.env.example` and the README status table.
