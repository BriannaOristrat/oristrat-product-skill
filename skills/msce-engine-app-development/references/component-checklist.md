# MSCE Component Check List

Use this reference for review, pre-commit checks, or after creating a prototype app.

## 1. Fill The Component Set

Start from changed/new files:

```powershell
git status --short --untracked-files=all
git diff --name-only
```

Also inspect feature-related ignored files. A test hidden by `.gitignore` is not visible in normal status and can be lost during preservation or omitted from review.

Map changed files to View or Logic root directories, then fill:

```txt
{oai-main-tenant-pm-board, oai-main-tenant-pm-filter, ...}
```

If there are no changed/new MSCE components, use `{}`.

## 2. Loop One Component At A Time

Do not merge all structural checks into one opaque pass. Record the result for each component.

## 3. Structure Check

For each View:

- Directory is under `src/msc-project/web/{module}/view/{component}/`.
- Has exactly one MSC mount entry: `*Brick.tsx`, `*Layer.tsx`, or `*Virtual.tsx`.
- Has `*Component.tsx` for non-trivial React UI.
- Has `action/` and `state/` files when it sends or receives events.
- Has `less/{component}.less` unless explicitly style-free.
- Mock data is in local `data/`.

## 4. Import Boundary Check

Allowed from a View:

- React, Next, UI libraries.
- `@mortiseai/mai_msc_engine_ts_module` in mount files.
- Own `./action`, `./state`, `./data`, `./less`, and same-View `./view`.
- Project language bootstrap: `@/src/msc-core/language/language`.

Flag another View's Component/Data/Dialog/Less, global Less imports for component styling, or prototype mock data moved to shared/global locations.

## 5. Class And Less Check

- Classes are kebab-case and begin with the component prefix.
- Do not use `_`, BEM `--`, or `var(--...)` unless the harness changes the rule.
- Dynamic classes must still be complete component-prefixed strings.

## 6. I18n Check

Visible copy, placeholders, `aria-label`, `title`, tabs, buttons, empty states, errors, and mock labels use the focused project namespace in both `zh.js` and `en.js`. Check duplicate namespace objects after conflict/stash restoration.

## 7. Event Chain Check

- ActionKeys/StateKeys strings are constants.
- Workflow sender/receiver values match DSL `name`.
- DSL events include every sender/action pair.
- Env registers View/Logic/Workflow/ActionKeys/StateKeys.

## 8. Final Validation

Run target lint/type/tests first, then repository lint/build when required. Preserve independent exit codes and logs. If `node_modules` is missing, report dependency installation as required; do not claim validation passed.
