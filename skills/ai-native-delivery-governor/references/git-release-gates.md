# Git And Release Gates

## Code Submission Precondition

Treat code implementation, strict MSCE validation, and Git submission as one continuous controlled workflow:

```text
CODE_COMPLETE
→ MSCE_STRICT_VALIDATED
→ MSCE_SUBMISSION_GATE: PASS
→ GIT_ROUND_DEFINED
→ ADD_APPROVED
→ STAGED
→ MSCE_STAGED_AUDITED
→ COMMIT_APPROVED
→ COMMITTED
```

- Code-bearing scope includes source, tests, executable configuration, routes, APIs, schemas, migrations, package changes, DSL, Workflow, Env, registration, and generated code required by the implementation.
- Before opening a Git round, require a current strict MSCE result for the exact candidate paths and current working-tree content. `FAIL`, `NOT_TESTED`, a stale result, or a missing required check blocks `git add`.
- After staging, run the MSCE staged-scope audit and required staged validation. Confirm the staged content matches the MSCE-approved candidate scope.
- Any later code edit, partial-stage mismatch, added dependency, registration change, or regenerated file invalidates the previous pass and returns the workflow to strict MSCE validation.
- A documentation-only or non-code repository change may mark the MSCE precondition `N/A`; do not use that exception when any code-bearing path is present.

## Document And Mixed Submission Preconditions

- Documentation-only repository submission requires a current `DOCUMENT_DELIVERY_GATE: PASS` for the exact content, requested formats, safety review, and repository candidate scope before the Git round.
- Mixed submission requires both `MSCE_SUBMISSION_GATE: PASS` and `DOCUMENT_DELIVERY_GATE: PASS`. Keep their candidate scopes separate and reconcile shared release facts before defining the round.
- A content, evidence, generated-format, package, or destination change invalidates the document pass. A code change invalidates the MSCE pass.

## Scope Review

Before staging, list exact paths or coherent categories and identify mixed files that need partial staging. Preserve unrelated user changes.

Default exclusion candidates unless explicitly authorized:

- `*.test.*`, `*.spec.*`, test fixtures, and test setup files.
- Generated framework files such as `next-env.d.ts`.
- Local `.env.*`, logs, caches, reports, and runtime queues.
- Load/performance scripts not part of the requested product delivery.
- Documentation the user explicitly excluded.

“Do not upload” does not automatically authorize a tracked `.gitignore` change. Prefer exact staging; for machine-local temporary exclusions use `.git/info/exclude` or another untracked local mechanism when appropriate. Never add a repository-wide `**/*.test.*` rule without explicitly reporting that it hides quality assets from status and stash workflows.

## Round State

Use this order for every commit round:

```text
ROUND_DEFINED
→ SCOPE_REVIEWED
→ ADD_APPROVED
→ STAGED
→ MSCE_STAGED_AUDITED
→ COMMIT_APPROVED
→ COMMITTED
→ PUSH_APPROVED
→ PUSHED
```

“Start/open round N” defines the round only. It does not authorize `git add` or `git commit`. Approval is consumed by one transition and cannot be reused for a later transition.

## Staged Audit

After `git add`, verify:

1. `git diff --cached --name-only` matches the approved scope.
2. Forbidden or excluded paths are absent.
3. `git diff --cached --check` passes.
4. The staged snapshot has no missing dependency or registration file.
5. `MSCE_SUBMISSION_GATE: PASS` is current, and the staged content matches its approved candidate scope.
6. Target lint/type checks pass; build is run when routes, schema, Env, DSL, package, or broad UI changes require it.
7. No staged file still has unreviewed unstaged hunks unless explicitly accepted.

For documentation-only or mixed rounds, also confirm `DOCUMENT_DELIVERY_GATE: PASS` is current and the staged document content matches its approved candidate scope. Treat MSCE as `N/A` only for a strictly documentation-only round.

## Commit And Push

- Request a new approval after staging and before commit.
- Confirm staged count immediately before committing.
- Request a new approval before push or PR creation.
- Push a new branch with upstream only when authorized.
- Verify local and remote HEAD match after push.

## Handoff

Report commit IDs, branch/upstream, validation results, excluded local files, and the PR title/body or URL when requested.
