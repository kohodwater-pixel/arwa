# AI development toolkit — install record (2026-11-21)

Restore point before this change: commit `48c1d08`. Everything below was added on top of it; nothing existing was replaced.

## Plugins (project scope, `.claude/settings.json`, marketplace `anthropics/claude-plugins-official`)

| Plugin | Version | What it adds | Needs |
|---|---|---|---|
| superpowers | 7.0.2 | 15 skills (brainstorming, writing-plans, test-driven-development, systematic-debugging, requesting/receiving-code-review, subagent-driven-development, verification-before-completion …) and a session-start hook | — |
| feature-dev | 1.0.1 | `/feature-dev` and three agents (code-explorer, code-architect, code-reviewer) | — |
| claude-code-setup | 1.0.0 | `claude-automation-recommender` skill | — |
| security-guidance | 2.0.21 | hooks: warnings on risky edits, diff review when a turn ends | — |
| context7 | 73c8cf3 | MCP server for current library documentation | host `mcp.context7.com` (allowed in the cloud environment); API key optional |

Not installed, on purpose: `frontend-design` (identical to the skill already in `.claude/skills/`), `code-review` and `code-simplifier` (Claude Code already ships `/code-review` and `/simplify`), `github` (GitHub is already connected in this environment; the plugin needs a personal access token), `playwright` (Playwright and the `webapp-testing` skill are already here).

## Skills added with `npx skills add` (recorded in `skills-lock.json`)

- `vercel-labs/agent-skills`: vercel-react-best-practices, vercel-composition-patterns, web-design-guidelines
- `wshobson/agents` (9 of the repository's skills): api-design-principles, nodejs-backend-patterns, javascript-testing-patterns, e2e-testing-patterns, auth-implementation-patterns, error-handling-patterns, sql-optimization-patterns, secrets-management, github-actions-templates
- `anthropics/skills`: skill-creator, webapp-testing, mcp-builder, frontend-design were already installed and match upstream.

## Project skills written for this product (`.claude/skills/<name>/SKILL.md`)

cinematic-prompt-engineer, cinematic-director, storyboard-architect, camera-motion-specialist, visual-continuity-specialist, ai-video-integration-engineer, video-pipeline-engineer, fullstack-qa-engineer. Their order and when to use which is in `video-platform/CLAUDE.md`.

## Undo

- A plugin: `claude plugin uninstall <name>@claude-plugins-official --scope project`
- A skill: `npx skills remove <name>` (or delete its folder and its `skills-lock.json` entry)
