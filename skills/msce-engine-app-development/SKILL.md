---
name: msce-engine-app-development
description: Develop, fix, review, stage, and validate Oristrat MSCE / MortiseSpecCodeEngine Next.js applications. Use for View/Logic/Workflow/DSL/Env work, MSCE Harness compliance, component isolation, i18n and Less checks, staged-scope audits, baseline-aware lint/type/test/build validation, or MSCE delivery gates.
---

# MSCE Engine App Development

This is a code-delivery foundation capability invoked by `ai-native-delivery-governor` for MSCE code work. It is not a peer application or an ordinary standalone shortcut; requirements/PRD, UI/UX, testing, or other application work inherits it automatically whenever the resulting change includes code. It never substitutes for the independent document-delivery gate.

Apply the current project MSCE contract with the smallest relevant discovery and validation scope. Treat the user's instructions and local `AGENTS.md`/`HARNESS.md` as higher priority.

## Harness-Aware Discovery

1. Attempt the requested target-file access first when project `HARNESS.md` defines an MSCE loader. Let the loader decide whether a read, review, or component-directory pass is required.
2. Follow the exact `MSCE.Harness` response wording required by the project. Do not pre-announce a read/review state before the loader decides.
3. Load only the chapters named by the loader. Do not reload the complete `FRAMEWORK.md` or `HARNESS.md` when cached chapters remain valid.
4. If no loader exists, read `AGENTS.md`, `HARNESS.md`, the relevant `FRAMEWORK.md` sections, and the closest existing example before editing.
5. Re-run discovery when the target component, task type, or harness file changes.

## Workflow Router

- New MSCE application or vertical slice: read [development-workflow.md](references/development-workflow.md).
- Component review or pre-commit check: read [component-checklist.md](references/component-checklist.md).
- Need an implementation example: read [example-map.md](references/example-map.md) and inspect the selected source files.
- Staged delivery audit: run `scripts/audit-staged-scope.ps1`.
- Batch validation with independent logs: run `scripts/validate-staged-batch.ps1`.

## Code Submission Coupling

Treat code completion, strict MSCE validation, and Git submission as one non-skippable workflow for every code-bearing commit.

1. Validate the exact candidate working-tree scope before a Git round is opened. Record affected components, paths, Harness chapters, examples, commands, exit codes, and baseline classification.
2. Emit `MSCE_SUBMISSION_GATE: PASS` only when every check required by the changed scope has passed and no `NEW_REGRESSION`, required `NOT_TESTED`, or unresolved staged dependency remains. Otherwise emit `FAIL` or `NOT_TESTED` and block the Git handoff.
3. After the user authorizes exact staging, run `scripts/audit-staged-scope.ps1` and the required staged validation. Confirm the staged snapshot matches the MSCE-approved candidate content before commit approval.
4. Invalidate the pass after any code edit, partial-stage mismatch, dependency or registration change, generated-file change, or scope expansion. Re-run the strict gate before continuing Git.

Code-bearing scope includes source, tests, executable configuration, routes, APIs, schemas, migrations, package changes, DSL, Workflow, Env, registration, and required generated code. Documentation-only or non-code repository changes may report the MSCE gate as `N/A` when none of those paths is present.

This skill never authorizes or executes `git add`, `git commit`, or `git push`. It produces the mandatory engineering evidence that allows the separately approved Git workflow to begin.

## Core Boundaries

- `Brick/Layer/Virtual`: keep only MSCE mounting, proxy lifecycle, state/action bridging, and child assembly.
- `Component`: keep React rendering and interaction; route DB/network operations through Logic.
- `Logic`: own API and business orchestration; do not make a View guess server contracts.
- `Workflow`: use DSL `name` values as senders/receivers and constants for event strings.
- `DSL/Env`: synchronize View, Logic, Workflow, ActionKeys, StateKeys, shell order, navigation, and registrations.
- View imports: use only the same View's `action`, `state`, `data`, `less`, and `view` modules; do not import another View's UI or Less.
- Less: use full component-prefixed kebab-case classes; avoid `_`, BEM `--`, and `var(--...)` unless the current harness explicitly changes the rule.
- I18n: route visible copy, placeholders, aria labels, buttons, tabs, empty/error states, and titles through the project language files.

## Change Discipline

- Preserve unrelated dirty-worktree changes.
- Find a matching example before adding or changing an MSCE interface.
- Keep one coherent component/slice boundary per implementation batch.
- Remove superseded endpoints and compatibility paths when the user says the old implementation must not remain.
- Do not stage test, generated, runtime, or local-environment files unless explicitly authorized.
- “Do not upload tests” does not imply adding a repository-wide test ignore rule. Report hidden feature-related ignored files before staging.

## Validation Cadence

- Targeted change: lint changed files and run TypeScript when types or contracts change.
- User-agreed batch: defer ordinary repeated checks, then validate the complete staged batch once.
- Route, schema, package, Env, DSL, registration, or broad UI change: run build after lint/type checks.
- Run each long check with its own exit code, duration, and log. A wrapper timeout without child output is `NOT_TESTED`.
- Full repository failures may be historical, but do not assume ownership from file scope alone. Prove the baseline or report `PARTIAL`.

Use these validation classifications:

- `TARGET_PASS`: target/staged checks pass.
- `REPO_PASS`: full repository gate passes.
- `REPO_BASELINE_FAIL`: full failures are proven unchanged from baseline.
- `NEW_REGRESSION`: target introduced or worsened a failure.

`TARGET_PASS + REPO_BASELINE_FAIL` is not a complete strict gate pass.

Use the bundled scripts instead of rebuilding long PowerShell commands. The scripts do not stage, commit, reset, install, or push files.

## Output Contract

Report:

- Checked component set such as `{oai-main-tenant-example}` or `{}`.
- Harness chapters and example files actually used.
- Changed/staged files, feature-related ignored files, and explicit exclusions.
- Exact validation commands, exit codes, log paths, and pass/fail/skipped reason.
- Target and repository-baseline classifications.
- `MSCE_SUBMISSION_GATE: PASS`, `FAIL`, `NOT_TESTED`, or `N/A`, including whether it still matches the candidate or staged snapshot.
- Remaining registration, i18n, runtime, or untested risks.
- Git state and the next approval gate when doing staged delivery.
