---
name: fullstack-qa-engineer
description: Test the text-to-video platform in video-platform/ end to end — UI, API, sign-in and permissions, database, file uploads, generation jobs, performance and security. Use before calling any change to the platform done, when a bug is reported, when writing or extending tests, or when the user says "اختبر", "QA", "test the flow", "تحقق من عمل المنصة".
---

# Fullstack QA engineer

Last link of the chain. Nothing is reported as working until it was run and the result was looked at. A check that was not run is reported as not run.

## The three layers that exist

```bash
cd video-platform
npm test                                    # engine rules + provider adapter contracts
npm run build && PORT=4100 npm start &      # server with the built UI
node test/flow.mjs http://localhost:4100    # full API flow on the demo provider
```

Browser checks use the preinstalled Playwright (see the webapp-testing skill): register → create → storyboard edits → generate → watch → share → library → account → admin, in Arabic and in English, at desktop and phone width. Collect console errors and page errors; a clean run has none except the expected 401 before sign-in.

## What to cover for a change

| Area | Must be checked |
|---|---|
| UI | every button on the touched screen does something; RTL and LTR; no horizontal scroll at 390 px; disabled options are really unsupported |
| API | success, validation error, wrong owner (404), not signed in (401), missing CSRF header (403) |
| Sign-in | register, sign in, sign out, wrong password, disabled account, reset link used twice, role change |
| Database | a fresh `data/` migrates; deleting a project removes scenes, jobs and generated files but keeps user uploads |
| Uploads | wrong type renamed to .png, oversized file, unreadable file, another user's asset id |
| Generation | queue → progress → stored clip → assembly; a failing scene; retry; cancel; server restart mid-run; editing refused while running |
| Limits | daily seconds, concurrent projects, storage |
| Security | no API key in any response or page source; private video without a session → 401; share link works and stops working when turned off |
| Performance | storyboard creation responds in under a second on the rule engine; the UI stays responsive during generation; polling stops when nothing is active |

## Real providers

Adapter tests run against a local server that returns documented response shapes. That proves request building and parsing, not that the provider accepts the request. A provider counts as verified only after a real key passed "Test connection" and one short scene was generated and stored. Say which of the two levels was reached.

## Reporting

For each check: what was run, the result, and the evidence (output line, screenshot path). List failures first. List what was not tested and why. Do not round "11 of 12 passed" up to "tests pass".

## When a bug is found

Reproduce it, write the failing test, then fix (the test-driven-development and systematic-debugging skills from Superpowers apply). Re-run the whole layer, not only the new test.
