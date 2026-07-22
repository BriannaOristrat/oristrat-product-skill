# Validation Baseline Attribution

Use this gate when repository-wide lint, type, test, or build checks fail and the failure may predate the target change.

## Required Evidence

Capture:

1. Selected baseline ref and commit ID.
2. Target/staged file set.
3. Exact command, exit code, duration, and durable output for each check.
4. Failure fingerprint: rule/test name, file, line when stable, and normalized message.
5. Whether each fingerprint exists in the baseline and in the current snapshot.

Do not infer baseline ownership only because the failing file is outside the target. Prove it by running the baseline, using existing trusted CI evidence, or comparing an unchanged blob and an unchanged diagnostic.

## Classification

| Condition | Classification |
|---|---|
| Target checks pass and full repository checks pass | `TARGET_PASS` + `REPO_PASS` |
| Target checks pass; repository failures are proven unchanged | `TARGET_PASS` + `REPO_BASELINE_FAIL` |
| A new or worsened failure appears | `NEW_REGRESSION` |
| Baseline cannot be executed or compared | `PARTIAL` |

`REPO_BASELINE_FAIL` is not a strict full-gate pass. It can proceed only under the user's explicit risk decision or when the requested workflow permits target-only acceptance.

## Execution Integrity

- Run long checks as independently observable commands or write each command's output to its own log before parallelizing.
- Give each check its own timeout and exit code.
- A wrapper timeout with missing child results is `NOT_TESTED`; rerun the affected checks individually.
- Preserve the first failure output and the retest output.
