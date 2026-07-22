# Full Delivery Gates

## Product Gate

Record target user, business scenario, expected outcome, scope, non-goals, success metric, acceptance criteria, and changed assumptions. Include positive, aggressive, conservative, and opposition views only when they affect a decision.

## Product-Base Gate

Record where the application lives, reused auth/tenant/navigation/permission/i18n/audit capabilities, app-specific extensions, duplicated concepts to avoid, and unresolved platform decisions.

## AI-Native Gate

Separate what AI proposes from what the application deterministically enforces. Record user confirmation, failure recovery, reversibility, auditability, and the concrete effort saved. Reject decorative chat-only AI or unbounded automation.

## UI/UX Gate

Check entry path, information architecture, empty/loading/error/permission states, long text, large lists, accessibility, responsiveness, and visual consistency with the product base. Compare alternatives only for new or ambiguous interaction models.

## Engineering Gate

Require project-rule discovery, a matching example, bounded file ownership, architecture boundary review, relevant lint/type/build checks, and an explicit QA handoff. MSCE completion requires its own skill evidence; generic code review is not a substitute. Any code-bearing Git submission requires `MSCE_SUBMISSION_GATE: PASS` before the Git round and an MSCE staged audit before commit approval.

## Document Delivery Gate

Use `document-delivery-orchestration` for requirements, PRDs, decisions, reports, manuals, formatted documents, and delivery packages. Require audience and destination, source traceability, content review, every requested format/render check, sensitive-information safety, exact package scope, and `DOCUMENT_DELIVERY_GATE: PASS` before handoff or repository submission.

## Mixed Delivery Gate

Keep code and document candidates separate. Require current `MSCE_SUBMISSION_GATE: PASS`, current `DOCUMENT_DELIVERY_GATE: PASS`, and agreement on shared names, versions, APIs, acceptance statements, test conclusions, and release claims before emitting `MIXED_DELIVERY_GATE: PASS`.

## QA Gate

Cover the main path plus applicable empty, extreme, invalid, permission, repeated-action, refresh/back, interruption, recovery, and regression cases. Preserve screenshots, network/console findings, responses, defects, and retest evidence proportionate to risk.

## Release Gate

Require product re-acceptance, the selected result-route gates, QA status, open-defect ownership, document/package status when applicable, security/privacy/rollback risks, and an explicit recommendation: accept, accept with risk, rework, block, or descope.
