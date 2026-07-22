---
name: fullstack-delivery-orchestration
description: Use when Oristrat needs PM-led full-stack delivery, multi-agent collaboration, product-manager control, full-stack engineer implementation, QA engineer real browser click testing, iterative development, acceptance gates, release readiness, or long-running feature/system delivery from PRD to tested software. 中文触发关键词：PM 主控 + 全栈工程师开发 + QA 实际点击测试 + 多 agent 长任务循环 + 发布门禁；也适用于 PM 主控全栈开发、测试工程师一点点点击验证、PRD 到开发测试交付、反复确认和调整的长时间任务。
---

# Fullstack Delivery Orchestration

This is a code-delivery foundation sequencing capability invoked by `ai-native-delivery-governor`, not a peer application or an ordinary standalone shortcut. It coordinates implementation roles and composes MSCE, runtime, QA, and Git gates. Formal specifications, reports, or packages remain on the independent document-delivery route.

Use this skill to coordinate a long-running product delivery loop where PM defines and controls the system, full-stack engineering implements it, QA performs real click-through testing, and reviewers guard quality before release.

This is an Oristrat self-developed orchestration skill. It does not replace:

- `product-design-management`: PM, PRD, scope, user stories, acceptance criteria.
- `msce-engine-app-development`: full-stack MSCE / MortiseSpecCodeEngine Next.js app development.
- `oristrat-product-ui-governor`: business-fit UI/UX decisions, optional external UI capability routing, form feedback, and final UI evidence.
- `product-testing`: acceptance testing, evidence package, actual delivery report, final test report.

## Core Rule

Do not let agents drift into isolated work. PM owns intent and acceptance. Engineering owns implementation. QA owns browser evidence and defect reproduction. Review owns risk. The coordinator owns sequencing, gates, and artifact integrity.

For every code-bearing commit, couple implementation with the strict MSCE submission gate and the separately approved Git workflow. Never hand completed code directly to Git: require `MSCE_SUBMISSION_GATE: PASS`, then define the Git round, stage exact paths, run the MSCE staged audit, and request commit approval.

## Workflow Router

- New system, feature, or PRD-to-build task: read `references/workflow.md` and `references/role-contracts.md`.
- Need to split a product manager request into engineering tasks: first use `product-design-management`, then read `references/workflow.md`.
- Need full-stack engineering implementation: use `msce-engine-app-development` for development rules, then follow this skill's gates and handoffs.
- Need UI design, audit, redesign, form/feedback behavior, or visual acceptance: use `oristrat-product-ui-governor`; it owns the controlled ui-ux-pro-max/Hallmark/frontend-design chain.
- Need QA to actually click through the UI: first use `product-testing`, then read `references/gates-and-artifacts.md`.
- Need multi-agent dispatch rules, long-running task rhythm, or repeated confirmation loops: read all three reference files.
- Need external skill selection or install order: read `references/external-source-stack.md`.

## Execution Order

1. PM gate: clarify problem, user, scope, priority, acceptance criteria, and explicit out-of-scope.
2. Engineering plan gate: map repo, architecture, data model, API/UI surfaces, test strategy, and task slices.
3. UI/UX plan gate when applicable: select surface type, source-of-truth components, form/feedback behavior, responsive targets, external capability evidence, and browser acceptance.
4. QA plan gate: build risk matrix, click-path matrix, data preconditions, and evidence plan before development finishes.
5. Vertical slice loop: implement one slice, self-test, QA click-test, record defects, PM decides accept/rework/descope.
6. MSCE submission gate: validate the exact code candidate, require `MSCE_SUBMISSION_GATE: PASS`, then open the Git round; after exact staging, run the MSCE staged audit before commit approval.
7. Review gate: code review, spec compliance review, security/privacy check, regression scope check.
8. Release gate: final test report, known issues, rollback plan, monitoring checks, PM go/no-go.

## Multi-Agent Dispatch Rules

- Dispatch PM, QA planning, code review, and documentation work in parallel only when they do not edit the same files.
- Do not dispatch multiple implementation agents against the same module or same file set.
- Use one implementation agent per vertical slice; use fresh QA/review agents after the slice is ready.
- If QA finds a product bug, route it through PM for priority before engineering fixes it.
- If QA finds a test/data/environment issue, let QA classify it and keep evidence; do not silently rewrite the result.
- If requirements change mid-slice, PM must record the change and decide whether to swap scope or defer.

## Required Artifacts

Every meaningful delivery run should produce:

- PM control note: goal, scope, assumptions, acceptance criteria, decisions.
- Engineering task plan: slices, files, commands, risks, rollback notes.
- QA click-test report: paths clicked, screenshots/traces, pass/fail/blockers.
- Defect log: expected, actual, reproduction, evidence, owner, priority, status.
- Final test report: what passed, what failed, what remains, release recommendation.

Use `references/gates-and-artifacts.md` for the detailed artifact contract.

## Quality Gates

Before marking a delivery round complete, verify:

- PM acceptance criteria are testable and still current.
- The feature runs locally or in the target environment.
- UI-heavy work records which external UI capabilities were installed, unavailable, used, rejected, or replaced by the Oristrat fallback.
- QA has actually interacted with the UI/API paths relevant to the feature.
- Every code-bearing Git round has a current strict MSCE pass and a matching staged audit; code changes after the pass return to engineering validation.
- Failures are recorded with evidence, not summarized away.
- Regression, security, accessibility, and rollback risks are explicitly classified.
- Final status is one of: `ACCEPTED`, `ACCEPTED_WITH_RISK`, `REWORK_REQUIRED`, `BLOCKED`, or `DESCOPED`.

## External Sources

Local and external engineering skills are references for role execution, not replacements for the orchestration gates. Use `references/external-source-stack.md` to choose the engineering skill stack.
