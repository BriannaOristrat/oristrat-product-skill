---
name: product-testing
description: Use when running Oristrat product testing, acceptance testing, delivery reports, evidence packages, workflow governance, or OB 测试 / ob 测试 / OB测报 / OB测试报告 for a target 网址 or URL.
---

# Product Testing

Use this skill when a task asks for product testing, acceptance testing, delivery reports, evidence packages, or test workflow governance.

## OB Test Shortcut

`ob 测试 <网址>`、`OB 测试 <URL>`、`OB测报`、`OB 测报`、`OB测试报告` must route here. Treat the phrase as an acceptance testing and delivery package request, not as a request for a small ad-hoc note.

## Process

1. Confirm scope with `references/workflows/01-test-task-intake.md`.
2. Execute and collect evidence with `references/workflows/02-test-execution-and-evidence.md`.
3. Generate reports with `references/workflows/03-report-generation.md`.
4. Review reports using all checklists under `references/checklists/`.
5. Archive delivery package with `references/workflows/04-delivery-package-and-archive.md`.
6. Before any GitHub submission, run `../../docs/github-submit-safety-gate.md`.

## Default Delivery Location

For OB testing, the final report folder and zip must be archived under the local archive root configured by `ORISTRAT_REPORT_ARCHIVE_ROOT` by default.

- Keep local absolute paths out of tracked repository files. Configure machine-specific archive roots in the local shell, OS user environment, or ignored `.env.*` files.
- The report script auto-loads ignored local config files from `自研skill\.env.local` and `skills/product-testing/.env.local`; explicit shell or OS environment variables still take priority.
- If `ORISTRAT_REPORT_ARCHIVE_ROOT` is unavailable, use the self-developed skill root fallback: `自研skill\输出\报告`.
- Do not use the current workspace as the final delivery location unless the user explicitly asks for it.
- When a task has a project or customer slug, set `ORISTRAT_REPORT_DIR` to a child folder under the archive root; the zip is generated next to that child folder.

## Required Gates

- Evidence report review.
- Actual delivery report review.
- Five-round report review.
- PDF / HTML safety gate.
- Final delivery gate.
- GitHub submission safety gate before commit, push, or PR.

Do not mark a testing task complete until the final delivery gate passes.
