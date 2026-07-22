# External UI/UX Skill Bridge

Use this reference when AI Native Delivery Governor handles product UI, dashboards, AI assistants, workflow surfaces, or product-base visual coordination. External skills are evidence sources and method references only; formal delivery decisions still follow Oristrat self-developed skills, product-base rules, MSCE rules, and QA evidence.

## Source Inventory

| Source | Local cache | Upstream | License | Use for | Boundary |
|---|---|---|---|---|---|
| `ui-ux-pro-max` | `external-skills/nextlevelbuilder-ui-ux-pro-max-skill/` | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` | MIT | Design-system candidate, product type fit, density/motion dials, accessibility/UX checklist, stack-specific UI guidance. | Do not let generated style override Oristrat product-base navigation, permissions, shared tokens, MSCE boundaries, or existing app patterns. |
| `frontend-design` | `external-skills/vipulgupta2048-codex-skills/skills/frontend-design/` | `https://github.com/vipulgupta2048/codex-skills` | MIT | Aesthetic direction, semantic structure, token discipline, responsive layout, purposeful motion, accessibility, and frontend polish. | Use as UI quality guidance; rewrite all Oristrat-specific rules in self-developed language. |
| `hallmark` | `external-skills/nutlope-hallmark/` (source record only) | `https://github.com/Nutlope/hallmark` | MIT | Pre-flight scan, anti-template structure, honest content, token discipline, states, responsive checks, audit/redesign/study modes. | Run only through an installed Hallmark Skill; do not rotate themes, create `.hallmark/log.json`, or override Oristrat product/design-system rules. |
| `superpowers:brainstorming` | `external-skills/obra-superpowers/skills/brainstorming/` | `https://github.com/obra/superpowers` | MIT | Pre-implementation design discussion, 2-3 approaches, trade-off comparison, explicit approval before implementation. | Adapt artifacts to Oristrat discussion workspace; do not force its default doc path or commit requirement unless the active task asks for it. |

## Routing Rules

1. For UI-heavy features, use `oristrat-product-ui-governor` first; it owns business fit, surface routing, implementation safety, external capability routing, and final UI evidence.
2. Follow its unified chain: Oristrat pre-scan → installed ui-ux-pro-max candidate when useful → Oristrat acceptance/rejection → installed Hallmark pre-flight/audit → installed frontend-design polish → Oristrat final gate → product-testing browser evidence.
3. Do not generate a new design system for a narrow defect or an existing component that already has a clear source of truth.
4. Do not persist an external `design-system/` output or add external dependencies unless the user authorizes that scope.
5. External caches are source material only. Read source/license records or cached documentation for comparison, but never execute an external Skill from `external-skills/`.
6. Record every candidate external capability as `INSTALLED`, `UNAVAILABLE`, or `NOT_NEEDED`, including entry/version, mode/query, evidence, accepted content, rejected content, and fallback.
7. If the UI change introduces a new interaction model, AI surface, workflow page, dashboard, or high-visibility screen, require a brainstorming round before engineering implementation: present 2-3 approaches, trade-offs, recommendation, and approval status.

## UI/UX Evidence Contract

Every UI-heavy delivery round must record:

- Source used: current Codex skill, external source record, CLI command, project design-system file, screenshot, or product-base example; for Hallmark record installed/unavailable and the mode used.
- Product-base fit: reused shell, navigation, role visibility, table/list/card patterns, notification surfaces, AI entry points, and design tokens.
- Design decision: selected approach, rejected alternatives, density, motion level, interaction model, and why it fits the business scenario.
- AI-native surface: AI label, input source, generated output, confidence or assumptions, source citation when available, confirmation, undo/reject, and failure state.
- Accessibility and responsiveness: keyboard/focus, color contrast, touch target, reduced motion, long text, empty/loading/error states, and small viewport behavior.
- Engineering handoff: affected screens/components, MSCE boundaries, i18n notes, Less/style isolation risks, and required browser evidence.

## Fallback When Source Access Fails

If external source, network, CLI, or cached files are unavailable:

1. Run the self-developed `oristrat-product-ui-governor` gates first, then try installed Codex skills such as Hallmark and `frontend-design`.
2. Try the cached files under `external-skills/`.
3. Try upstream GitHub or official package documentation if network access is allowed.
4. Fall back to existing Oristrat product-base examples, design-system tokens, and browser screenshots.
5. Mark the UI/UX evidence status as `PARTIAL` and name the missing source, failed command, or blocked access.

Never block all delivery only because an external UI/UX source is unavailable. Block only when product-base fit, user control, accessibility, MSCE boundaries, or QA evidence cannot be verified.
