---
name: product-testing
description: Use when running Oristrat product testing, acceptance or regression testing, manual retest, defect verification, reference-site parity checks, batch validation, large-data or pagination/filter/import/export checks, delivery reports, evidence packages, workflow governance, or OB 测试 / OB测报 / OB测试报告 for a target URL.
---

# Product Testing

This is an application Skill selected by `ai-native-delivery-governor` for acceptance, regression, and defect verification. Runtime-backed execution without a material artifact uses the runtime foundation only; a formal report or evidence package uses `DOCUMENT_DELIVERY`; a tested code fix plus formal report uses `MIXED_DELIVERY`.

Use this skill for product testing, acceptance, regression, defect retest, browser evidence, delivery reports, and test-governance tasks.

When testing is part of PM-led full-stack delivery, let `fullstack-delivery-orchestration` own sequencing and PM gates. This skill owns QA execution, browser click evidence, defect records, regression conclusions, and test reports.

## Select the Smallest Test Mode

Choose one mode before loading references or running tools:

- `smoke`: Check page availability, login, the primary click path, and essential API health. Return a concise result; do not generate or archive a formal report.
- `feature`: Verify a named feature, defect, or reference-site parity target. Collect only evidence needed to prove the result.
- `batch`: Validate an agreed batch of changes, such as after roughly seven or eight related modifications. Run targeted regression, type checks, and lint/build checks proportional to the batch risk.
- `formal-ob`: Produce the complete OB acceptance-test evidence, reports, review rounds, archive package, and delivery gates.

Do not silently escalate `smoke`, `feature`, or `batch` into `formal-ob`. Escalate only when the user requests a formal report/package or the delivery owner explicitly requires it.

## OB Test Shortcut

`OB 测试 <网址>`、`OB 测试 <URL>`、`OB测报`、`OB 测报`、`OB测试报告` route to `formal-ob`. Treat them as acceptance-testing and delivery-package requests, not small ad-hoc checks.

## Reference Routing

- All modes: read `references/workflows/01-test-task-intake.md` only as needed to establish scope, environment, and risk.
- `feature` and `batch`: use `references/workflows/02-test-execution-and-evidence.md`; load only the defect/report templates relevant to the requested evidence.
- `formal-ob`: follow all four workflow files in order, then review with every checklist under `references/checklists/`.
- Before an authorized GitHub submission, apply `../../docs/github-submit-safety-gate.md`. Testing does not itself authorize commit, push, PR, or external publication.

## Execution Rules

1. Establish the target URL, build/branch, account prerequisites, in-scope paths, and expected result.
2. Prefer the smallest reproducible test set. Reuse an existing browser session only when its state is part of the requested scenario.
3. Record observed behavior, expected behavior, reproducible steps, and concrete evidence. Keep failed click-path evidence after a defect is fixed.
4. For filters, pagination, import/export, and large datasets, verify the full-data behavior rather than only the visible page.
5. For API probes, accept either a direct response model or a response wrapped in `{ model: ... }`; evaluate HTTP status, business success, cookies, and returned data separately.
6. Report status as `PASS`, `PARTIAL`, `FAIL`, `BLOCKED`, or `NOT_TESTED`. State what was not tested and why.
7. For login, password, verification-code, modal/drawer form, or interruption-recovery scenarios, use the acceptance matrix in `../oristrat-product-ui-governor/references/form-feedback-and-validation.md` when that Skill is available. Verify close/reopen and preserved state, not only a fresh happy path.
8. HTTP `200` with a business failure proves route reachability only. A real mutation is `PASS` only after business success and an authorized readback/login/state verification.

## Validation Cadence

- During rapid iteration, run focused checks for the changed path and defer broad lint/build/E2E until the agreed batch boundary.
- At a batch boundary, run the relevant regression set plus type checks and lint/build checks proportional to risk.
- Run full-suite or formal acceptance checks before delivery, release, or when explicitly requested.
- A deferred check is not a passed check. List it as deferred until it runs.

## Formal OB Delivery Location

For `formal-ob`, archive the final report folder and zip under `ORISTRAT_REPORT_ARCHIVE_ROOT` by default.

- Keep local absolute paths out of tracked repository files. Configure machine-specific roots in the local shell, OS user environment, or ignored `.env.*` files.
- If `ORISTRAT_REPORT_ARCHIVE_ROOT` is unavailable, use the self-developed skill root fallback `自研skill\输出\报告`.
- Do not use the current workspace as the final delivery location unless the user explicitly asks.
- When a project or customer slug exists, set `ORISTRAT_REPORT_DIR` to a child folder below the archive root; generate the zip beside that folder.

## Gates by Mode

- `smoke`: scope identified, core path exercised, result and blockers stated.
- `feature`: acceptance criteria exercised, focused evidence captured, regression impact stated.
- `batch`: agreed batch scope covered, targeted regression complete, deferred broad checks disclosed.
- `formal-ob`: evidence report review, actual delivery report review, five-round report review, PDF/HTML safety gate, final delivery gate, and GitHub submission safety gate when GitHub delivery is authorized.

Do not mark `formal-ob` complete until its final delivery gate passes. Other modes may complete with a narrower evidence set when their stated scope passes.
