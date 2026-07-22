---
name: document-delivery-orchestration
description: Govern evidence-backed document delivery for Oristrat requirements, PRDs, decision records, test reports, manuals, Markdown, HTML, PDF, and final document packages. Use when the requested result is documentation-only or when a mixed code-and-document delivery needs an independent document gate, format validation, sensitive-information review, packaging, archive, or handoff approval.
---

# Document Delivery Orchestration

Operate as the document-delivery foundation selected by `ai-native-delivery-governor`. Keep it independent from the code-delivery foundation: a document pass never proves code quality, and an MSCE pass never proves document quality.

## Classify The Deliverable

Record the document type, audience, decision or action it must support, required formats, source evidence, destination, and authorization boundary.

- Requirements, PRD, specification, roadmap, or user stories: use `product-design-management` for domain content.
- UI audit, design rationale, or handoff specification: use `oristrat-product-ui-governor` for UI/UX conclusions.
- Test evidence, test report, defect report, or OB package: use `product-testing`; route its formal reports through the existing evidence, actual-delivery, and package review Skills.
- Complex decision, options paper, or meeting resolution: use `task-council` for deliberation and decision content.
- General manuals or formatted artifacts: use the installed document, PDF, or Obsidian capability appropriate to the requested format.

Read [document-delivery-gates.md](references/document-delivery-gates.md) before producing a formal, multi-format, customer-facing, archived, or repository-bound deliverable.

## Run The Document Route

1. Scope the document result, audience, formats, sources, non-goals, destination, and acceptance criteria.
2. Gather authoritative evidence and label facts, assumptions, inferences, unknowns, and untested claims.
3. Draft with the narrow application Skill; do not invent APIs, metrics, decisions, test results, owners, dates, or business rules.
4. Review content for completeness, traceability, internal consistency, audience fit, and actionable acceptance criteria or decisions.
5. Validate every requested format. Inspect rendered layout when PDF, HTML, DOCX, slides, spreadsheets, or visual structure matters.
6. Scan for credentials, personal data, customer-sensitive content, local absolute paths, debug traces, prompts, temporary files, and broken links.
7. Audit the exact package or destination scope; remove temporary or superseded artifacts only when authorized.
8. Emit `DOCUMENT_DELIVERY_GATE: PASS` only when every required content, format, safety, and package check passes.
9. If repository submission is requested, start a separately approved documentation Git round. Mark MSCE `N/A` only when the exact scope contains no code-bearing path.

## Mixed Delivery Contract

When a task produces both code and documents, maintain two independent candidate scopes and gate results:

```text
code candidate     -> MSCE_SUBMISSION_GATE: PASS
document candidate -> DOCUMENT_DELIVERY_GATE: PASS
both current and scope-matched -> MIXED_DELIVERY_GATE: PASS
```

Any code edit invalidates the code pass. Any document content, evidence, format, or package change invalidates the document pass. A shared manifest, version, API name, test conclusion, or release statement must match across both routes before convergence.

## Git Boundary

- Do not execute `git add`, `git commit`, `git push`, or PR creation without the controller's exact, one-shot authorization.
- Documentation-only repository changes may skip MSCE but must still pass this document gate and the Git approval gate.
- Generated documents, reports, screenshots, archives, and local environment files are not automatically repository content. Respect the requested destination and existing ignore rules.
- A mixed Git round must preserve the separate code and document scopes and confirm both gate results against the staged snapshot.

## Output Contract

Report:

- Document type, audience, formats, source evidence, destination, and exact candidate/package scope.
- Content, traceability, format/render, safety, and package checks with evidence.
- `DOCUMENT_DELIVERY_GATE: PASS`, `FAIL`, or `NOT_TESTED`, including whether it matches the current candidate.
- For mixed delivery, both independent gate results and `MIXED_DELIVERY_GATE` status.
- Remaining claims, formats, links, sensitive-data boundaries, or handoff risks.
- Git state and the next approval gate when repository submission is requested.
