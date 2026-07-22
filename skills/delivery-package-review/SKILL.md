---
name: delivery-package-review
description: Use when reviewing final delivery package contents, zip archive, report consistency, temp-file cleanup, or sensitive information safety.
---

# Delivery Package Review

Use this skill before handing over a delivery package.

Treat this as a specialized package reviewer routed by `document-delivery-orchestration` when the product-testing package contract applies.

Follow `../product-testing/references/checklists/05-final-delivery-gate.md`.
Before any GitHub submission, also follow `../../docs/github-submit-safety-gate.md`.

## Required Checks

- All three reports exist in `.md`, `.html`, and `.pdf`.
- Zip contains only final outputs and necessary evidence.
- No temp PDFs, broken PDFs, local paths, credentials, or prompt/debug traces.
- No account, password, token, API key, private key, cookie, session, or storage state enters GitHub.
- Report conclusions are consistent across the package.
