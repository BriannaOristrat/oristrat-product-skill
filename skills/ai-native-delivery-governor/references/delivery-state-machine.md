# Delivery State Machine

Use a run ledger when requirements change repeatedly or the task crosses product, code, document, Git, and runtime gates. Keep it in conversation or under `.git/`; do not create tracked project documentation unless requested.

## Requirement Ledger

Record one row per active requirement:

| ID | Requirement | Source of truth | Acceptance check | Status |
|---|---|---|---|---|
| R1 | Current user rule | Existing component/API/spec | Observable check | ACTIVE/SUPERSEDED/DEFERRED |

When a new instruction conflicts with an active row:

1. Mark the old row `SUPERSEDED`.
2. Add the new rule and its concrete acceptance check.
3. Search implementation and documents for stale conditions from the old rule.
4. Preserve all compatible rows.

## Delivery Routes

Classify the material result before entering a route. Reclassify whenever scope crosses the code/document boundary.

### Code Delivery Phases

```text
DISCOVERED
→ SCOPE_ACCEPTED
→ IMPLEMENTING
→ TARGET_VALIDATED
→ UI_OR_API_ACCEPTED
→ RUNTIME_VERIFIED
→ MSCE_STRICT_VALIDATED
→ GIT_ROUND_DEFINED
→ STAGED_AUDITED
→ COMMITTED
```

### Document Delivery Phases

```text
DOCUMENT_SCOPED
→ SOURCE_EVIDENCE_READY
→ DOCUMENT_DRAFTED
→ CONTENT_REVIEWED
→ FORMAT_VERIFIED
→ SAFETY_VERIFIED
→ PACKAGE_AUDITED
→ DOCUMENT_DELIVERY_GATE: PASS
→ DOCUMENT_DELIVERED
```

### Mixed Delivery Convergence

```text
MSCE_SUBMISSION_GATE: PASS
+ DOCUMENT_DELIVERY_GATE: PASS
+ SHARED_FACTS_RECONCILED
→ MIXED_DELIVERY_GATE: PASS
→ MIXED_HANDOFF_READY
```

Phases may be skipped only when outside the user's request. Record the skipped phase as `N/A` or `NOT_TESTED`, never silently treat it as passed.

For any code-bearing commit, `MSCE_STRICT_VALIDATED` is mandatory and must record `MSCE_SUBMISSION_GATE: PASS`. A code edit after that state returns the run to `IMPLEMENTING`; a staged snapshot that differs from the approved candidate scope returns it to `TARGET_VALIDATED` or earlier. Only a repository change with no code, executable configuration, schema, DSL, Env, package, route, migration, or test code may mark the MSCE phase `N/A`.

For any material document handoff or repository submission, record `DOCUMENT_DELIVERY_GATE: PASS` for the exact content, formats, package, and destination. A document, evidence, generated-format, package, or destination change returns the document route to the affected earlier phase. Mixed delivery cannot pass while either route is stale, failed, or untested.

## Approval Rule

Every proposed mutating action must name:

- action;
- exact scope;
- expected state transition;
- excluded files;
- next action that is not yet authorized.

Short approval such as `可以` applies only to that proposal. A later `git add`, commit, push, stash cleanup, dependency install, process stop, document publication, archive, or external handoff needs its own authority when it was not part of the approved action.

## Final Ledger

Report result route, active requirements, superseded requirements removed from code or documents, independent candidate scopes and gate status, Git state, runtime state, document destination/package state, temporary backup/stash resources, and the next user-owned decision.
