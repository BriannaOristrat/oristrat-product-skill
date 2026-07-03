---
name: actual-delivery-report-review
description: Use when reviewing 02_实际交付报告 as the customer-facing test report for title, conclusion, readability, or local path safety.
---

# Actual Delivery Report Review

Use this skill to review `02_实际交付报告.md/html/pdf`.

Follow `docs/checklists/02-actual-delivery-report-review.md` and `docs/checklists/04-pdf-html-safety-gate.md`.

## Non-Negotiables

- The visible report title is `测试报告`.
- No `file://`, `C:\`, `C:/`, user directory, temp directory, or browser print footer.
- The report is customer-readable and does not expose internal debugging process.
- Each conclusion is backed by `01_运行过程证据报告`.
