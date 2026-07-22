# MSCE Prototype Development Workflow

Use this reference when creating a new Oristrat MSCE prototype application.

## 1. Establish Scope

1. Confirm whether the work is a tenant app, platform app, dev example, Server Logic, API route, or existing feature change.
2. Confirm whether data is mock-only. Keep mock-only data in the View's own `data/`; do not create DB tables or Server Logic.
3. Confirm whether original files may be changed. If not, create only authorized files and report integration changes separately.
4. Record the active requirement ledger and remove superseded guards/contracts when user instructions change.

## 2. Read Standards and Examples

Read local `AGENTS.md`, the harness-selected `FRAMEWORK.md` chapters, `HARNESS.md`, and a closest example. If Next.js app routes or handlers change, read local Next docs when available.

## 3. Choose the MSCE Shape

Start with the smallest shape. Add Logic for event bridging, API calls, persistence, or reusable business behavior. Add Server Logic only when the feature requires server-side behavior.

## 4. Tenant Shell Integration

When adding a tenant-shell app, align:

- tenant DSL shell keys, order, body mapping, layout, and events;
- tenant workflow keys, order, META, and shell metadata;
- sidebar navigation and permissions;
- local href/shell mappings;
- `MscWebEnv` View/Logic/Workflow/ActionKeys/StateKeys registration.

## 5. Implementation Discipline

- Modify one component boundary at a time.
- Keep View-local data and subcomponents inside that View.
- Do not import another View's Less or use global CSS variables when forbidden by the harness.
- Use component-prefixed kebab-case classes.
- Add i18n keys before final validation and check for duplicate namespace keys after merges.
- For real APIs, verify route reachability, backend health, business success, and end-to-end state separately.

## 6. Validation

Run target lint, type checks, focused tests, required build, and browser/API acceptance proportionate to risk. Keep each command independently observable. Missing dependencies or valid business test data produce `BLOCKED`/`PARTIAL`, not `PASS`.
