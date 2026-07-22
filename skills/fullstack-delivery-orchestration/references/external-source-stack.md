# External Source Stack

Local and external skills are method sources only. For Oristrat MSCE full-stack implementation, route engineering through the local `msce-engine-app-development` skill first. External GitHub skills remain references unless the user explicitly asks to install/use them.

## Recommended Install / Reference Order

| Order | Source | Use | Oristrat Role |
|---:|---|---|---|
| 1 | local `product-design-management` | PM control, PRD, acceptance criteria | Formal PM entrypoint |
| 2 | local `product-testing` | QA click testing, evidence package, final report | Formal QA entrypoint |
| 3 | local `msce-engine-app-development` | MSCE / MortiseSpecCodeEngine Next.js app development | Formal engineering entrypoint |
| 4 | `petrkindlmann/qa-skills` | Playwright, exploratory testing, release readiness, bug triage | QA method source |
| 5 | `addyosmani/agent-skills` | spec-driven development, task breakdown, incremental implementation, TDD, code review | Engineering discipline source |
| 6 | `Jeffallan/claude-skills` | Fullstack Guardian, framework specialists, API/architecture, code review | Fallback/reference only |
| 7 | `ercoledevs/codex-council` | Multi-perspective review for risky architecture, frontend behavior, release go/no-go | High-risk review source |
| 8 | `VoltAgent/awesome-codex-subagents` | Subagent catalog and role ideas | Directory only, not direct workflow |

## Recommended External Skill Subset

### QA

From `petrkindlmann/qa-skills`, prioritize:

- `playwright-automation`
- `exploratory-testing`
- `risk-based-testing`
- `ai-bug-triage`
- `release-readiness`
- `test-reliability`
- `visual-testing`
- `accessibility-testing`

### Full-Stack Engineering

Primary engineering skill:

- `msce-engine-app-development`

Use it for:

- MSCE / MortiseSpecCodeEngine Next.js app development.
- New prototype applications.
- Web View / Logic / Workflow / DSL modules.
- MscWebEnv registration.
- Component class and Less isolation checks.
- `msce-language` i18n checks.
- Example-driven implementation.
- `npm run lint` and `npm run build` validation.

From `Jeffallan/claude-skills`, choose by stack only as fallback/reference:

- `Fullstack Guardian`
- `Feature Forge`
- `Architecture Designer`
- `API Designer`
- `Next.js Developer` / `React Expert` / `Vue Expert` / framework equivalent
- `Test Master`
- `Playwright Expert`
- `Code Reviewer`
- `Security Reviewer`

### Engineering Discipline

From `addyosmani/agent-skills`, prioritize:

- `spec-driven-development`
- `planning-and-task-breakdown`
- `incremental-implementation`
- `test-driven-development`
- `frontend-ui-engineering`
- `api-and-interface-design`
- `browser-testing-with-devtools`
- `code-review-and-quality`
- `security-and-hardening`

### Council / Multi-Role Review

From `ercoledevs/codex-council`, use only for high-risk decisions:

- architecture decisions
- migrations
- security/privacy/data-loss risk
- frontend UX behavior and release go/no-go
- contentious implementation trade-offs

## Usage Boundary

- Do not copy external skill text into formal Oristrat `skills/`.
- Do not install every external source by default.
- Install or cache only the subset needed for the current project.
- Keep external cache under ignored `external-skills/`.
- Record public source, license, checked date, and local use boundary when caching.
