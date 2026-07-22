# Full-Stack Delivery Workflow

## Purpose

Run long-lived delivery work without losing control of scope, quality, or evidence. This workflow assumes a product manager provides a system or feature, a full-stack engineer builds it, and a QA engineer validates it through actual use.

## Phase 0: Intake And Framing

Owner: PM Agent, using `product-design-management`.

Inputs:

- Product idea, PRD, customer request, existing system, screenshot, workflow, or rough requirement.
- Known constraints: deadline, stack, customer, compliance, budget, access.

Outputs:

- Problem statement.
- Target users and key jobs.
- In-scope and out-of-scope.
- MVP / V1 / later split.
- Acceptance criteria that QA can test.
- Open questions and assumptions.

Gate:

- Do not begin engineering if the main flow, success behavior, failure behavior, and minimum test data are unclear.

## Phase 1: Engineering Discovery

Owner: Full-Stack Engineer Agent, using `msce-engine-app-development`.

Actions:

1. Load `msce-engine-app-development` before inspecting or editing MSCE / MortiseSpecCodeEngine / Next.js app code.
2. Inspect project rules first: `AGENTS.md`, `FRAMEWORK.md`, `HARNESS.md`, and the closest existing examples.
3. Identify files likely to change across View, Logic, Workflow, DSL, Env registration, route, data, and i18n.
4. Identify integration risk: auth, permissions, state, persistence, async jobs, third-party services, migrations, shell registry, DSL events, and language files.
5. Propose vertical slices that can each be tested independently.

Outputs:

- Architecture note.
- Task breakdown by vertical slice.
- Test command map.
- Risk and rollback notes.
- MSCE example files used as references.
- Expected `npm run lint` / `npm run build` validation scope.

Gate:

- PM approves slice order and scope trade-offs before implementation.

## Phase 2: QA Planning Before Build Completes

Owner: QA Engineer Agent, using `product-testing`.

Actions:

1. Convert acceptance criteria into click paths.
2. Define smoke, happy path, negative path, edge state, empty/loading/error state, role/permission path, and regression path.
3. Prepare data preconditions and accounts.
4. Decide which checks are manual click-through, scripted Playwright, API, unit/component, visual, accessibility, or performance.

Outputs:

- QA matrix.
- Evidence plan.
- Data and environment checklist.
- Blocker list.

Gate:

- QA can start with mocked or staging data, but must mark anything not actually clicked as `NOT_TESTED`.

For UI-heavy slices, run an Oristrat UI/UX plan before QA finalizes the matrix:

- identify the closest existing product surface and shared validation/notification source;
- select `component`, `page`, or `system` scope;
- record ui-ux-pro-max, Hallmark, and frontend-design as `INSTALLED`, `UNAVAILABLE`, or `NOT_NEEDED`;
- define form feedback, interruption/recovery, responsive, accessibility, and real-browser acceptance;
- never execute an external cache copy or report it as a formally used Skill.

## Phase 3: Vertical Slice Loop

Repeat this loop for each slice.

1. Engineer writes/updates the narrowest relevant tests first when feasible.
2. Engineer implements the slice.
3. Engineer runs local checks and records commands/results.
4. UI owner checks product-base and form/feedback compliance when the slice changes UI behavior.
5. QA performs real click-through validation in browser or test environment.
6. QA captures screenshot, trace, video, console/network issue, or reproduction notes.
7. PM reviews pass/fail evidence and decides: accept, rework, descope, or defer.
8. If rework is required, engineer fixes only the classified issue, then QA retests the exact path.

Rules:

- Do not batch many slices before QA sees anything.
- Do not let QA only read code; they must interact with the product path.
- Do not silently convert product bugs into test changes.
- Do not accept a slice if failures lack owner and next action.

## Phase 4: Review And Hardening

Owners: Review Agent, Engineer, QA, PM.

Checks:

- Spec compliance: built behavior matches PM acceptance criteria.
- Code quality: maintainability, local patterns, testability, naming, boundaries.
- Reliability: failure modes, retries, data cleanup, rollback.
- Security/privacy: auth, permission, secrets, customer data, external services.
- UX/accessibility: labels, keyboard, error states, loading states, responsive behavior.

Gate:

- Any blocker in security, data loss, auth boundary, P0/P1 regression, or untestable main path blocks release.

## Phase 5: Release Readiness

Owner: PM Agent.

Inputs:

- Final QA report.
- Defect log.
- Engineering implementation note.
- Review findings.
- Known issues and rollback plan.

Decision statuses:

- `ACCEPTED`: passes criteria and risks are acceptable.
- `ACCEPTED_WITH_RISK`: can ship with documented known issues and owner.
- `REWORK_REQUIRED`: cannot ship until listed blockers are fixed.
- `BLOCKED`: missing access, environment, dependency, or product decision.
- `DESCOPED`: intentionally removed from current release.

## Phase 6: Retrospective And Memory

Record:

- What requirements changed.
- What tests caught real defects.
- Which defects escaped initial planning.
- Which selectors/data/setup were flaky.
- Which workflow rule should be updated.

Store durable improvements in the relevant self-developed skill, not only in a one-off report.
