# Document Delivery Gates

Use these gates for formal, multi-format, customer-facing, archived, repository-bound, or mixed deliverables. Apply only the checks required by the requested result, but never silently mark an omitted required check as passed.

## Scope Gate

Record document type, audience, intended decision/action, source of truth, formats, language, destination, owner, due state, acceptance criteria, and explicit non-goals. Separate repository files from local or external delivery artifacts.

## Evidence Gate

- Trace material claims to authoritative files, links, logs, responses, screenshots, data, decisions, or named assumptions.
- Label `FACT`, `ASSUMPTION`, `INFERENCE`, `UNKNOWN`, `NOT_TESTED`, and superseded content where ambiguity matters.
- Do not create evidence, test outcomes, metrics, approvals, or citations that were not observed.

## Content Gate

- Verify completeness against the requested document type and acceptance criteria.
- Check terminology, names, versions, dates, API/field names, decisions, owners, and next actions for internal consistency.
- Keep internal evidence detail out of customer-facing summaries unless it is required for the audience.
- For requirements and PRDs, require scope, non-goals, states, failure paths, permissions, dependencies, and testable acceptance criteria.
- For decisions, retain rejected options, material dissent, assumptions, risks, owner, and follow-up validation.
- For test reports, require reproducible evidence, failure samples, retest state, untested scope, and consistent conclusions.

## Format And Render Gate

- Validate every requested file exists, opens, and contains the current approved content.
- When layout matters, render and visually inspect headings, tables, pagination, fonts, links, images, clipping, blank pages, headers, and footers.
- Keep Markdown readable in its target viewer. Use Obsidian-specific syntax only when the destination is an Obsidian vault.
- Do not require HTML, PDF, DOCX, slides, spreadsheets, or zip unless the user or application contract requests them.

## Safety Gate

Reject credentials, tokens, keys, cookies, sessions, private account data, unnecessary personal data, customer-sensitive content, prompts, hidden debugging notes, temporary paths, and local absolute paths. Apply repository-specific sensitive-information scanning before any external or GitHub handoff.

## Package And Handoff Gate

- Include only approved final artifacts and necessary evidence or attachments.
- Exclude temporary, superseded, broken, duplicate, cache, local-environment, and unrelated files.
- Confirm filenames, manifests, versions, conclusions, links, and archive contents agree.
- Verify the destination is authorized and distinguish local archive, repository, external system, and user-facing package.
- Do not delete, publish, send, stage, commit, push, or create a PR without matching authorization.

## Status Rules

- `DOCUMENT_DELIVERY_GATE: PASS`: all required gates pass for the exact current document candidate or package.
- `FAIL`: a required content, evidence, format, safety, or package check fails.
- `NOT_TESTED`: required execution or inspection evidence is missing.
- `MIXED_DELIVERY_GATE: PASS`: both the current code gate and document gate pass, their scopes are recorded, and shared facts are consistent.

Any change to document content, evidence, generated format, package contents, destination, or shared release facts invalidates the document pass and requires the affected checks again.
