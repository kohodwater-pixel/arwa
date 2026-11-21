# GPU cost policy

Enforced in `crates/core/src/gpu/mod.rs` and tested in `crates/core/tests/core.rs`
(`gpu_approval_budget_and_idle_shutdown`). The interface cannot bypass these rules: they are checked in the core.

## Rules

| Rule | Value | Where enforced |
|---|---|---|
| Monthly budget | **1,000 SAR** by default | `gpu::budget` |
| Warning | at **70%** and at **90%** of the budget | `budget.level` = `warn70`, `warn90`; shown in the GPU Manager and the status strip |
| Stop | at **100%**: new generation jobs are refused, queued ones wait, and the GPU cannot be started | `assert_can_accept_jobs`, `gpu::start` |
| Starting a GPU | Only by a person, every time, with a ticked approval and their name | `gpu::start(approved, approved_by)` returns `approval_required` otherwise |
| Automatic start | Never. A job that needs the GPU waits with the reason "GPU stopped" | `jobs::tick` |
| Idle shutdown | The instance is stopped after 10 minutes without generation jobs (1–240, configurable) | `gpu::idle_check`, run by the worker |
| Raising the budget | A named approval in the interface; written to the activity log | GPU Manager, `audit_log` |
| LoRA training | Never started by the app. A run is a record that needs a named approval | `lora::run_update` |
| Purchases | The app cannot create, rent or resize instances. It can only start and stop one existing instance | `GpuProvider` trait has `status`, `start`, `stop` only |

## How cost is counted

- Each period the instance runs is a row in `gpu_sessions` with its hourly price (as reported by the
  provider, or the fallback price from the settings) and the exchange rate at the time (default 1 USD = 3.75 SAR).
- Month spend = sum over this calendar month (UTC) of hours × USD per hour × exchange rate, including the session still running.
- Every status read is reconciled with the provider: if the instance was started outside the app, a session
  is opened and labelled "not approved in the app", so that time is still counted; if it was stopped
  outside, the session is closed.
- The figure is this app's own ledger. The provider's invoice is the authority; storage and network
  charges that the provider bills separately are not included.

## Provider

One provider at first: RunPod (REST v2: `GET /v2/pods/{id}`, `POST /v2/pods/{id}/action`).
The request shapes come from RunPod's published documentation and are tested against a protocol double;
**they have not yet been run against a real account.** The first real start must be watched by the manager.

Target hardware: NVIDIA RTX A6000 48 GB, on demand. Wan 2.2 TI2V-5B needs about 24 GB; the A14B 4-step
workflow fits 48 GB with the fp8 files. Prices change; read the current hourly price in the GPU Manager
before approving a start.

## What needs the manager's decision before any spending

1. Create the RunPod account and one pod, and enter its ID and an API key in the GPU Manager.
2. Confirm the monthly budget (1,000 SAR by default) and the idle time.
3. Approve each start by name.
