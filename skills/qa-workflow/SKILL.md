---
name: qa-workflow
description: Use when running Oristrat product testing, acceptance testing, delivery reports, evidence packages, or workflow governance.
---

# QA Workflow

Use this skill when a task asks for product testing, acceptance testing, delivery reports, evidence packages, or test workflow governance.

## Process

1. Confirm scope with `docs/workflows/01-test-task-intake.md`.
2. Execute and collect evidence with `docs/workflows/02-test-execution-and-evidence.md`.
3. Generate reports with `docs/workflows/03-report-generation.md`.
4. Review reports using all checklists under `docs/checklists/`.
5. Archive delivery package with `docs/workflows/04-delivery-package-and-archive.md`.
6. Before any GitHub submission, run `docs/checklists/06-github-submit-safety-gate.md`.

## Required Gates

- Evidence report review.
- Actual delivery report review.
- Five-round report review.
- PDF / HTML safety gate.
- Final delivery gate.
- GitHub submission safety gate before commit, push, or PR.

Do not mark a testing task complete until the final delivery gate passes.
