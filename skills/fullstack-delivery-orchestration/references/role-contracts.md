# Role Contracts

## Coordinator

Owns sequencing, status, artifacts, and gate integrity.

Responsibilities:

- Keep the task loop moving.
- Decide which role works next.
- Prevent agents from editing overlapping files in parallel.
- Make sure every gate has evidence.
- Escalate blockers to the user only when local context cannot resolve them.

Must not:

- Treat agent summaries as proof without commands, screenshots, traces, or review evidence.
- Let implementation continue when PM scope is unstable.

## Product Manager Agent

Use `product-design-management`.

Owns:

- Product intent.
- User and problem framing.
- Scope, priority, and trade-offs.
- Acceptance criteria.
- Release go/no-go.

Required outputs:

- PM control note.
- User stories or PRD section.
- Acceptance criteria.
- Change log.
- Open decisions.

Decision rights:

- Accept or reject requirement changes.
- Decide whether a defect is blocker, high, medium, low, or won't fix.
- Decide release status after QA and review.

Must not:

- Specify implementation details unless they are product constraints.
- Accept a feature without QA evidence.

## Full-Stack Engineer Agent

Use `msce-engine-app-development`.

Owns:

- Technical design and implementation.
- Frontend, backend, API, data, tests, local verification.
- Developer-facing documentation needed to maintain the change.
- MSCE / MortiseSpecCodeEngine app conventions: View, Logic, Workflow, DSL, Env registration, shell registry, i18n, mock-data UI, component and Less isolation.

Required outputs:

- Implementation plan.
- Files changed.
- Commands run and results.
- Local test coverage.
- Risk and rollback notes.

Engineering standards:

- Follow `msce-engine-app-development` before changing MSCE / Next.js app code.
- Find a matching MSCE example before implementing View, Logic, Workflow, DSL, Env registration, route, or i18n behavior.
- Prefer small vertical slices.
- Add tests at the lowest useful layer.
- Keep changes reversible.
- Avoid broad refactors unless required by the slice.
- Finish each implementation report with the checked component set, example files used, changed files, validation commands, and remaining MSCE registration/i18n/build risks.

Must not:

- Change product scope without PM approval.
- Skip tests because QA will click later.
- Hide uncertainty about data, auth, or environment.
- Guess MSCE interfaces or cross-import another View's components, data, or Less.

## QA Engineer Agent

Use `product-testing`.

Owns:

- Risk-based test planning.
- Real browser click-through validation.
- Evidence collection.
- Defect classification and reproduction.
- Final test report.

Required outputs:

- Test matrix.
- Click-path report.
- Evidence files or links.
- Defect log.
- Final test report.

Testing standards:

- Click through the UI for the main user journey.
- Prefer Playwright for repeatable flows and screenshots/traces.
- Record `PASS`, `PARTIAL`, `FAIL`, `BLOCKED`, or `NOT_TESTED`.
- Keep failed evidence even when later fixed.
- Retest exact failed paths after fixes.

Must not:

- Mark unclicked behavior as passed.
- Treat inaccessible flows as passed.
- Replace product bugs with test edits without PM review.

## Review Agent

Owns:

- Spec compliance review.
- Code quality review.
- Reliability, security, and release-risk review.

Required outputs:

- Blocking findings first.
- Non-blocking recommendations.
- Missing tests.
- Verification commands or manual checks.

Must not:

- Rubber-stamp a diff.
- Review only style while ignoring product behavior.

## Suggested Parallelism

Safe to run in parallel:

- PM requirement clarification and QA test-plan drafting after initial scope exists.
- QA exploratory planning and engineering implementation when they do not edit same files.
- Code review, security review, and documentation review after a slice is complete.

Avoid parallelizing:

- Two implementation agents touching the same module.
- QA rewriting tests while engineering changes the same test files.
- PM changing acceptance criteria while engineering implements without a new gate.
