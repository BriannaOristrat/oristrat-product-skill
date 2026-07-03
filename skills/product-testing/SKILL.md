---
name: product-testing
description: Use when running Oristrat product testing, acceptance testing, delivery reports, evidence packages, or workflow governance.
---

# Product Testing

Use this skill when a task asks for product testing, acceptance testing, delivery reports, evidence packages, or test workflow governance.

## Process

1. Confirm scope with `references/workflows/01-test-task-intake.md`.
2. Execute and collect evidence with `references/workflows/02-test-execution-and-evidence.md`.
3. Generate reports with `references/workflows/03-report-generation.md`.
4. Review reports using all checklists under `references/checklists/`.
5. Archive delivery package with `references/workflows/04-delivery-package-and-archive.md`.
6. Before any GitHub submission, run `../../docs/github-submit-safety-gate.md`.

## Required Gates

- Evidence report review.
- Actual delivery report review.
- Five-round report review.
- PDF / HTML safety gate.
- Final delivery gate.
- GitHub submission safety gate before commit, push, or PR.

Do not mark a testing task complete until the final delivery gate passes.
