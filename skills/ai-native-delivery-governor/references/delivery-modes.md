# Delivery Modes

These are internal controller modes, not a flat set of user-facing applications. First classify the material result as `CODE_DELIVERY`, `DOCUMENT_DELIVERY`, or `MIXED_DELIVERY`; then select a mode while routing the request to an application Skill. The code route composes Git, strict MSCE, full-stack sequencing, and runtime verification. The document route uses `document-delivery-orchestration`. Mixed delivery runs both independently before convergence.

## Diagnose

- Inspect and reproduce without modifying source unless the user expands the request.
- Return the cause, evidence, affected paths, and safe fix options.

## Hotfix

- Limit work to one bounded defect or interaction.
- Prefer targeted lint/type checks and a direct reproduction/retest.
- Escalate to `delivery` when the fix changes schema, routes, permissions, shared contracts, or multiple product surfaces.

## Delivery

- Define one coherent vertical slice with acceptance criteria and non-goals.
- Coordinate product-base boundaries, full-stack sequencing, MSCE rules, UI states, implementation, runtime verification, and QA handoff as required by the application.
- For document results, coordinate sources, content review, requested formats, rendering, safety, destination, and package handoff.
- For mixed results, keep separate candidate scopes and gate states until convergence.
- Validate the staged snapshot before requesting commit approval.

## Full

- Use for explicit total-control delivery, cross-team loops, or release decisions.
- Run product, opposition, AI-native, product-base/UX, engineering, QA, re-acceptance, and release gates.
- Create working artifacts only when the user requests documents or the evidence package is part of the agreed outcome.

## Git

- Use as a foundation segment inherited by code-bearing application work, not as a normal standalone shortcut.
- Treat Git as the post-validation segment of a code delivery, not as a substitute for engineering validation.
- For code-bearing scope, require a current `MSCE_SUBMISSION_GATE: PASS` before defining the Git round or requesting `git add`.
- Do not edit unless required to correct staged scope or a validation failure.
- Separate review, add, commit, and push approvals.
- Report branch, upstream, commit IDs, staged count, and remaining dirty files.

## Runtime

- Use as a foundation segment inherited by application work that requires execution, browser acceptance, service dependencies, or business connectivity, not as a normal standalone shortcut.
- Confirm branch and HEAD before launching.
- Inspect existing listeners and process ownership before stopping anything.
- Use service-specific configuration instead of assuming one port variable controls every process.
- Verify the user-facing URL, proxy route, dependent service health endpoints, business response, and end-to-end success separately.
- Mark a route-only or invalid-parameter probe as `PARTIAL`, not as proof that the requested business operation succeeds.
