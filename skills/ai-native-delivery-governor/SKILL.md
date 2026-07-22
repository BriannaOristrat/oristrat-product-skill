---
name: ai-native-delivery-governor
description: Govern Oristrat AI-native product delivery by classifying code, document, or mixed results, selecting the smallest application, and composing the required foundation route. Use when the user says 启动AI原生交付总控、AI交付总控、产品研发测试总控、多 Agent 产品交付，or asks for governed product-engineering-QA loops, document packages, staged Git confirmation, release decisions, or difficult cross-team delivery.
---

# AI Native Delivery Governor

Coordinate product intent, product-base fit, engineering, QA, Git boundaries, and release decisions without expanding the user's requested scope.

## 1. Classify Result And Select The Smallest Mode

Before selecting an application or mode, classify the requested material result:

| Result route | Use when | Mandatory foundation result |
|---|---|---|
| `CODE_DELIVERY` | The candidate changes source, tests, executable configuration, routes, APIs, schemas, migrations, packages, DSL, Workflow, Env, registration, or required generated code | Current code validation and `MSCE_SUBMISSION_GATE` when submission is requested |
| `DOCUMENT_DELIVERY` | The result is requirements, PRD, decision record, report, manual, Markdown, HTML, PDF, spreadsheet, slides, or a document package without code-bearing changes | Current `DOCUMENT_DELIVERY_GATE` |
| `MIXED_DELIVERY` | Code and document results are both required | Both independent route gates plus `MIXED_DELIVERY_GATE` |

Advice or diagnosis with no material artifact does not create a delivery route. If scope changes from document-only to executable content, reclassify before continuing.

Then choose one primary internal control mode. Modes are controller mechanics, not a flat list of user-facing applications. Do not run the full governance loop for a narrow task.

| Mode | Use for | Default evidence |
|---|---|---|
| `diagnose` | Explain or locate a problem without implementing | Reproduction, logs, cause, affected paths |
| `hotfix` | One bounded bugfix or small UI correction | Focused diff, targeted validation, residual risk |
| `delivery` | A normal multi-file feature or vertical slice | Scope, implementation, staged validation, QA handoff |
| `full` | Explicit product-engineering-QA orchestration or release decision | Product/UX/AI/engineering/QA/release gates |
| `git` | Internal foundation segment for post-validation review, batch stage, commit, push, or PR preparation | Current MSCE gate for code, exact scope, approvals, staged audit, commit IDs |
| `runtime` | Internal foundation segment for starting, stopping, reconnecting, or inspecting an application | Branch/HEAD, ports, health checks, logs |

Read [delivery-modes.md](references/delivery-modes.md) only when mode details are needed. Use `full` only when the user explicitly requests total-control delivery or the task truly spans product, engineering, QA, and release.

## 2. Preserve User Authority

- Treat the user's scope, exclusions, validation cadence, and approval gates as controlling.
- Do not create PRs, commits, pushes, documents, test data, or external messages without matching authorization.
- Do not generate discussion documents unless the user requests them or `full` mode requires an evidence package.
- Preserve unrelated dirty-worktree changes and identify overlaps before editing or staging.
- Use subagents only when the user requests delegation, applicable project instructions require it, and tooling is available. Otherwise execute locally and state no false multi-agent evidence.

## 3. Maintain A Run Ledger

For changing requirements, staged Git work, document packages, mixed delivery, merges, or runtime operations, maintain a compact run ledger before acting. Read [delivery-state-machine.md](references/delivery-state-machine.md).

- Record the result route, current requirement, superseded requirements, acceptance checks, explicit exclusions, code and document candidate scopes, branch/HEAD, dirty scope, validation state, destination, and next approval gate.
- Treat approvals as one-shot and scope-bound. `可以` approves only the action that was most recently and explicitly presented.
- A new requirement replaces only the conflicting rule; preserve compatible accepted requirements.
- Do not keep a stale guard such as “must request a code first” after the user explicitly removes that condition.

## 4. Compose Foundation And Applications

Use this three-layer architecture instead of treating every capability as a peer shortcut:

1. **Controller entry:** `ai-native-delivery-governor` identifies the task, selects the smallest internal mode, and owns authorization boundaries and final status.
2. **Foundation capabilities:** two independent delivery routes. The code route composes `fullstack-delivery-orchestration`, `msce-engine-app-development`, runtime dependency gates, and Git approval/release gates. The document route is owned by `document-delivery-orchestration`. These are automatically composed when required and are not ordinary user-facing application shortcuts.
3. **Application skills:** `product-design-management` for requirements/PRD, `oristrat-product-ui-governor` for UI/UX work, `product-testing` for product verification, and `task-council` for complex decisions.

Load only the application and foundation capabilities required by the task:

- Requirements, PRD, product scope, or re-acceptance: route to `product-design-management`.
- UI/UX changes: route to `oristrat-product-ui-governor` as the self-developed owner. It may route installed `ui-ux-pro-max` for design-system candidates, Hallmark for pre-flight/audit, and `frontend-design` for implementation polish. Never execute external cache copies or claim an unavailable Skill was used.
- Browser acceptance, regression, evidence, or manual retest: route to `product-testing`.
- Complex multi-option or cross-functional decisions: route to `task-council`.
- External product evidence: use `product-intelligence-workflows` only when evidence is missing.

Applications inherit the correct foundation automatically:

- `CODE_DELIVERY`: add full-stack sequencing when implementation spans roles or vertical slices; add strict MSCE and Git gates for submission; add runtime checks when execution, browser acceptance, ports, proxies, dependencies, or business connectivity must be verified.
- `DOCUMENT_DELIVERY`: load `document-delivery-orchestration`; validate content, evidence, requested formats, rendering, sensitive information, package scope, destination, and handoff. Use a documentation Git round only when repository submission is requested.
- `MIXED_DELIVERY`: keep code and document candidates independent, run both routes, reconcile shared versions/names/conclusions, and require `MIXED_DELIVERY_GATE: PASS` before final handoff or a mixed commit.

An unavailable optional skill is not automatically a blocker. Block only when the missing capability is essential to the user's requested outcome and no safe local fallback exists.

Treat code implementation, strict MSCE validation, and Git submission as one coupled code route. When a task may commit code, load `msce-engine-app-development` before the Git gate. `git` mode owns approvals and repository transitions; it never replaces or bypasses the MSCE submission gate. Treat `runtime` in the same way: it remains available as an internal diagnostic mode, but normal application requests receive it automatically instead of asking the user to start a separate runtime workflow.

Treat document scoping, evidence, content review, format validation, safety review, and package handoff as one coupled document route. A documentation-only Git change may mark MSCE `N/A`, but it still requires `DOCUMENT_DELIVERY_GATE: PASS`. Never use one route's pass as evidence for the other.

## 5. Run A Governed Loop

For code-bearing `hotfix` and `delivery`:

1. Establish requested outcome, non-goals, current branch, dirty files, and affected surface.
2. Reproduce or inspect before editing.
3. Find the closest project example and applicable local rules.
4. Implement the smallest coherent change.
5. Validate according to risk and the user's cadence.
6. If code may be submitted, complete the strict MSCE submission gate before defining or opening a Git round.
7. Report outcome, evidence, remaining risk, and the next authorized action.

For document delivery:

1. Establish document type, audience, sources, formats, destination, non-goals, and acceptance criteria.
2. Use the selected application Skill for domain content and `document-delivery-orchestration` for the foundation route.
3. Require `DOCUMENT_DELIVERY_GATE: PASS` before handoff, archive, publication, or a documentation Git round.

For mixed delivery, run both routes independently and converge only after both current passes and a shared-facts consistency check.

For `full`, read [delivery-gates.md](references/delivery-gates.md) and record explicit product, product-base, AI, UI/UX, engineering, QA, and release decisions.

## 6. Validation Cadence

Select one cadence and state it:

- `targeted`: run focused checks after a risky or isolated change.
- `batch`: accumulate ordinary edits and validate after the user-agreed batch size, commonly 7–8 changes.
- `full`: run repository lint/build/test/browser evidence at a commit, release, route, schema, Env, or DSL gate.

Do not claim `PASS` from a build alone when the requested user flow was not exercised. Preserve failed evidence after fixes and record retest status.

Read [validation-baseline.md](references/validation-baseline.md) whenever repository-wide checks fail or the target branch may already be red. Distinguish target evidence from repository baseline:

- `TARGET_PASS`: the approved target/staged scope introduces no known failure.
- `REPO_PASS`: the repository-wide gate passes.
- `REPO_BASELINE_FAIL`: repository failures exist but are proven unchanged from the selected baseline.
- `NEW_REGRESSION`: the current target introduces or worsens a failure.

Never summarize `TARGET_PASS + REPO_BASELINE_FAIL` as a fully passed strict gate.

## 7. Git Approval Gate

For any code-bearing staged delivery, follow this sequence exactly:

```text
code complete
→ strict MSCE validation on the exact candidate scope
→ MSCE_SUBMISSION_GATE: PASS
→ review exact scope
→ user approves scope
→ git add exact paths
→ audit the staged snapshot against the MSCE-approved scope
→ user approves commit
→ git commit
→ user approves push/PR
→ push or create PR
```

Do not open a code Git round or request `git add` while `MSCE_SUBMISSION_GATE` is `FAIL`, `NOT_TESTED`, stale, or missing. Any code change after the pass invalidates it and returns the run to strict MSCE validation. Documentation-only repository changes may use the Git approval gate without MSCE only after `DOCUMENT_DELIVERY_GATE: PASS` and only when no executable, configuration, schema, DSL, Env, package, route, migration, or test code is included. Mixed rounds require both current passes.

Never infer approval for a later step from approval of an earlier step. Read [git-release-gates.md](references/git-release-gates.md) for the MSCE precondition, exclusions, staged checks, branch handling, and evidence.

Before pull, merge, rebase, conflict resolution, or stash restoration, also read [git-worktree-and-merge-gates.md](references/git-worktree-and-merge-gates.md).

## 8. Runtime Gate

For `runtime` mode or any environment-dependent acceptance, read [runtime-dependency-gates.md](references/runtime-dependency-gates.md). Separate process health, route reachability, business validation, and end-to-end success. HTTP `200` with `{success:false}` proves transport reachability, not business success.

## 9. Status Vocabulary

Use only evidence-backed status:

- `PASS`: verified outcome.
- `PARTIAL`: some evidence exists; named gaps remain.
- `FAIL`: expected behavior did not occur.
- `BLOCKED`: an essential dependency, permission, environment, or decision prevents progress.
- `NOT_TESTED`: no execution evidence.
- `REWORK_REQUIRED`: must be corrected before acceptance.
- `ACCEPTED_WITH_RISK`: user accepts a named risk and mitigation.

## 10. Output Contract

Keep routine updates concise. Final delivery must include:

- Selected mode and achieved outcome.
- Selected result route and its current gate status.
- Changed or inspected scope.
- Exact validation evidence and skipped checks with reasons.
- Remaining risks or untested boundaries.
- Git state and next action requiring approval, when relevant.

For mixed delivery, additionally report separate code and document scopes, both gate results, shared-facts reconciliation, and `MIXED_DELIVERY_GATE`.

For `full` mode, additionally report active gates, role conclusions, product-base fit, AI/app boundary, UI/UX evidence, QA coverage, defects, and release recommendation.
