# MSCE Example Map

Use this reference to choose examples before writing or checking code. Verify that the example still exists and matches the active harness before copying a pattern.

## Standard MSCE Structure

Use `src/msc-project/web/msc-dev/msc-dev-example/` for View/Logic/Workflow/DSL skeleton and event flow. Older examples may use underscore class names; do not copy deprecated naming into new apps.

## Business Board Prototype

Use `src/msc-project/web/oai-main-tenant/view/oai-main-tenant-crm-pipeline/` for same-View board/card/dialog and local data patterns. Do not copy another View's UI or Less into the target View.

## Tenant Shell Registration

Inspect:

```txt
src/msc-project/web/oai-main-tenant/dsl/oai_main_tenant_dsl.ts
src/msc-project/web/oai-main-tenant/workflow/OaiMainTenantWorkflow.ts
src/msc-project/web/oai-main-tenant/view/oai-main-tenant-sidebar/data/OaiMainTenantSidebarData.ts
src/msc-base/web/env/MscWebEnv.ts
```

Keep all shell keys, body names, order, navigation, permissions, events, and registrations aligned.

## I18n Pattern

Use the current login or closest tenant component for language bootstrap and `useTranslation`. Add one focused namespace in both `zh.js` and `en.js`; do not create duplicate namespace objects during conflict resolution.

## Workbench / Data Request Pattern

Use existing workbench View/Logic/Workflow only when the feature graduates from mock data to real API-backed behavior. Do not add these layers to a mock-only prototype.
