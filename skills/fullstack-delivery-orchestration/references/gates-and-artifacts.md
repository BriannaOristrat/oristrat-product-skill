# Gates And Artifacts

## Required Status Vocabulary

Use these statuses consistently:

- `PASS`: verified and evidence supports the claim.
- `PARTIAL`: some evidence exists but gaps remain.
- `FAIL`: expected behavior did not happen.
- `BLOCKED`: access, environment, account, dependency, or decision prevents validation.
- `NOT_TESTED`: not run; cannot support acceptance.
- `ACCEPTED`: PM accepts the slice or release.
- `ACCEPTED_WITH_RISK`: PM accepts with known issues and owner.
- `REWORK_REQUIRED`: must fix before acceptance.
- `DESCOPED`: intentionally removed from current scope.

## Gate 1: PM Readiness

Required:

- Goal.
- User.
- Main flow.
- Success state.
- Failure/edge states.
- Acceptance criteria.
- Out-of-scope.
- Test data or data assumptions.

Fail this gate when:

- Acceptance criteria cannot be clicked or asserted.
- PM cannot decide what counts as done.
- The feature depends on unknown auth, payment, customer data, or external service behavior.

## Gate 2: Engineering Plan Readiness

Required:

- Repo/stack map.
- Slice order.
- Files likely to change.
- Test commands.
- Data/migration impact.
- Rollback or feature flag strategy when relevant.

Fail this gate when:

- The implementation plan is too broad to test slice by slice.
- No local verification command exists.
- The plan requires secrets or production data without approval.

## Gate 3: QA Plan Readiness

Required:

- Click-path matrix.
- Risk matrix.
- Environment and account setup.
- Evidence plan.
- Not-tested boundaries.

Fail this gate when:

- QA cannot access the app or test environment.
- Main path cannot be interacted with.
- No evidence method exists for UI behavior.

## Gate 4: Slice Acceptance

Required:

- Engineer command results.
- QA click-through evidence.
- Defect log updated.
- PM decision.

Slice decision table:

| Condition | Status |
|---|---|
| Meets acceptance and QA evidence is sufficient | `ACCEPTED` |
| Main path works, minor known issue has owner | `ACCEPTED_WITH_RISK` |
| Main path fails or blocker defect exists | `REWORK_REQUIRED` |
| Cannot test due to access/environment | `BLOCKED` |
| PM removes slice from this release | `DESCOPED` |

## Gate 5: Release Readiness

Required:

- Final test report.
- All P0/P1 defects closed or explicitly accepted by PM.
- Regression scope checked.
- Security/privacy risks classified.
- Rollback plan or release mitigation.
- Known issues list.

Release is blocked when:

- Main path is `FAIL`, `BLOCKED`, or `NOT_TESTED`.
- Auth, permission, data integrity, payment, or destructive actions are unverified.
- QA evidence is missing for the primary user journey.
- PM has not accepted known risks.

## Artifact Templates

### PM Control Note

```markdown
## PM Control Note

- Product/system:
- Goal:
- Target user:
- Business/user outcome:
- MVP scope:
- Out of scope:
- Acceptance criteria:
- Open questions:
- PM decision:
```

### Engineering Slice Note

```markdown
## Engineering Slice

- Slice name:
- Files changed:
- Implementation summary:
- Commands run:
- Test results:
- Risks:
- Rollback:
- Ready for QA: yes/no
```

### QA Click-Test Note

```markdown
## QA Click-Test

- Environment:
- Account/data:
- Path clicked:
- Expected:
- Actual:
- Status: PASS/PARTIAL/FAIL/BLOCKED/NOT_TESTED
- Evidence:
- Defect ID:
- Retest result:
```

### Defect Record

```markdown
## Defect

- ID:
- Severity:
- Owner:
- Expected:
- Actual:
- Reproduction:
- Evidence:
- Impact:
- PM priority:
- Fix status:
- Retest status:
```

### Final Test Report

```markdown
## Final Test Report

- Scope tested:
- Scope not tested:
- PASS count:
- FAIL count:
- BLOCKED count:
- Known issues:
- Release recommendation:
- PM decision:
```
