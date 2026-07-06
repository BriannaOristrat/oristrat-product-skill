---
name: product-design-management
description: Use when Oristrat needs 需求分析, product design, product management, PRD/product specification writing, user research synthesis, roadmap planning, prioritization, UX/UI/design-system review, user stories, handoff specs, or turning a product idea into implementation-ready work. This is the Oristrat self-developed wrapper for product design and PM workflows, with external community skills used only as reference sources.
---

# Product Design Management

Use this skill for Oristrat product design, product specification, and product manager workflows. Produce team-ready Chinese artifacts unless the user asks for another language.

## Operating Rules

1. Start by identifying the product stage: idea, discovery, 需求分析, PRD, design, roadmap, delivery decomposition, review, or iteration.
2. Do not copy external skill text into the final answer. Use `references/source-skill-stack.md` only to decide which cached source can inform the work.
3. Keep outputs concrete: decisions, assumptions, user/problem framing, scope, success metrics, risks, owners, and next actions.
4. Prefer Oristrat-facing artifacts over generic templates. If details are missing, make reasonable assumptions and mark them clearly.
5. For implementation-bound work, connect product intent to acceptance criteria, testability, and handoff requirements.

## Workflow Router

- Idea, vague request, or early product thinking: read `references/product-workflow.md`, then frame the problem, users, opportunity, and decision needed.
- 需求分析, PRD, product spec, feature definition, or user story: read `references/templates-and-gates.md`, then produce a structured requirement analysis, PRD/spec, or user story with acceptance criteria.
- Product design, UX flow, UI review, design system, or handoff: read `references/product-workflow.md` and `references/templates-and-gates.md`, then create the relevant design brief, flow, checklist, or review.
- Roadmap, prioritization, or trade-off decision: read `references/product-workflow.md`, then make the scoring logic explicit.
- PRD to engineering tasks, tickets, branch/PR sequence, or delivery plan: read `references/templates-and-gates.md`, then decompose into implementation-ready units.

## External Skill Cache

External sources are cached under `../../external-skills/` for traceability and comparison. They are not formal Oristrat self-developed skills.

Before using external cache, read `references/source-skill-stack.md` and choose the narrowest relevant source group. Do not use `ncklrs/startup-os-skills`; it is intentionally excluded.

## Delivery Gates

Before saying the product/design/spec work is complete, check:

- Problem, target user, business goal, and success metric are explicit.
- Scope includes in-scope, out-of-scope, dependencies, and open questions.
- User experience includes primary flow, states, edge cases, and failure handling when relevant.
- Engineering handoff includes acceptance criteria and testable behavior.
- Decisions and assumptions are separated so the team can challenge them quickly.
- No secrets, customer-sensitive data, local paths, tokens, or private account information are included.
