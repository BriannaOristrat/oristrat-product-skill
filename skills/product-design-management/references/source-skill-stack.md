# 外部 Skill 来源栈

本文件记录本次安装进 `external-skills/` 的外部来源。它们用于调研、对照和启发，不作为 Oristrat 正式自研 Skill 直接触发。

## 使用规则

- 先使用 `skills/product-design-management/SKILL.md` 的自研流程。
- 只有在需要更细的方法、模板或检查角度时，才读取下面的外部缓存。
- 输出必须重写为 Oristrat 自研表达，不直接拼接或搬运外部正文。
- 不使用 `ncklrs/startup-os-skills`，这是本次明确排除项。
- 外部 license 可能限制商用或再分发，提交公开仓库前先复核上游 license。

## 已缓存来源

| 来源 | 本地路径 | 用途 | 许可备注 |
|---|---|---|---|
| `deanpeters/Product-Manager-Skills` | `external-skills/deanpeters-product-manager-skills/` | PM 主流程、PRD、用户故事、路线图、优先级、JTBD、机会树 | 上游为 CC BY-NC-SA 4.0，商用和再分发需谨慎 |
| `Owl-Listener/designer-skills` | `external-skills/owl-designer-skills/` | 产品设计、UX research、UI、设计系统、交互、原型测试、设计交付 | MIT |
| `borghei/Claude-Skills` | `external-skills/borghei-claude-skills/` | 产品设计师视角、PRD 到 repo/ticket/PR 计划 | MIT + Commons Clause，禁止销售软件本身 |
| `Digidai/product-manager-skills` | `external-skills/digidai-product-manager-skills/` | SaaS PM 日常诊断、PRD critique、roadmap 和指标思考 | 上游 license 文件为 CC BY-NC-SA 4.0 |
| `RefoundAI/lenny-skills` | `external-skills/refoundai-lenny-skills/` | Lenny 产品方法论：PRD、spec、roadmap、用户反馈、设计评审 | MIT |

## 最近版本检查

检查日期：2026-07-06

| 来源 | 默认分支 | 检查到的 commit | 本地缓存状态 |
|---|---|---|---|
| `deanpeters/Product-Manager-Skills` | `main` | `39986078003cb8621635828a8d6e7342270b0257` | 已更新 8 个已缓存 `SKILL.md` |
| `Owl-Listener/designer-skills` | `main` | `acc3e574b36ef2895268a176dbae886e1b845ae0` | 已缓存文件与上游一致 |
| `borghei/Claude-Skills` | `main` | `83dc60b0eed2e12da70df2b2bd57a973e38abee8` | 已缓存文件与上游一致 |
| `Digidai/product-manager-skills` | `main` | `ab7a40662c8455ece631834dee9670b3322f465b` | 已缓存文件与上游一致 |
| `RefoundAI/lenny-skills` | `main` | `280a57aa42fed3b6f35f51f0d9e71013b4c8ae74` | 已缓存文件与上游一致 |

## 已缓存 Skill 清单

### deanpeters Product Manager Skills

- `prd-development`
- `user-story`
- `roadmap-planning`
- `prioritization-advisor`
- `jobs-to-be-done`
- `opportunity-solution-tree`
- `problem-framing-canvas`
- `lean-ux-canvas`

### Owl Designer Skills

- Research: `user-persona`, `interview-script`, `journey-map`, `usability-test-plan`, `survey-design`, `affinity-diagram`
- UX strategy: `design-brief`, `information-architecture`, `opportunity-framework`, `metrics-definition`, `stakeholder-alignment`, `competitive-analysis`, `service-blueprint`
- UI design: `visual-hierarchy`, `layout-grid`, `responsive-design`, `color-system`, `typography-scale`, `data-visualization`
- Design systems: `component-spec`, `design-token`, `accessibility-audit`, `design-system-governance`, `documentation-template`
- Interaction: `state-machine`, `error-handling-ux`, `feedback-patterns`, `form-design`, `navigation-patterns`, `onboarding-design`
- Prototype/testing: `wireframe-spec`, `prototype-strategy`, `heuristic-evaluation`, `user-flow-diagram`, `a-b-test-design`, `test-scenario`
- Design ops: `handoff-spec`, `design-qa-checklist`, `design-review-process`, `design-debt-audit`
- Visual critique: `critique-visual-hierarchy`, `critique-information-density`, `critique-affordance`, `critique-brand-consistency`

### Borghei Claude Skills

- `product-designer`
- `spec-to-repo`

### Digidai Product Manager Skills

- 根目录 `SKILL.md`
- `README.zh-CN.md`
- `README.md`
- `LICENSE`

### RefoundAI Lenny Skills

- `writing-prds`
- `writing-specs-designs`
- `prioritizing-roadmap`
- `problem-definition`
- `running-design-reviews`
- `usability-testing`
- `ai-product-strategy`
- `analyzing-user-feedback`
- `behavioral-product-design`

## 选择建议

| 任务 | 优先参考 |
|---|---|
| 写 PRD 或产品规范 | deanpeters `prd-development`，RefoundAI `writing-prds`，Digidai root skill |
| 用户故事和验收标准 | deanpeters `user-story`，RefoundAI `writing-specs-designs` |
| 路线图和优先级 | deanpeters `roadmap-planning`、`prioritization-advisor`，RefoundAI `prioritizing-roadmap` |
| 设计研究和用户理解 | Owl research 组，RefoundAI `analyzing-user-feedback` |
| UX/UI/设计系统 | Owl UI/design-system/interaction 组，Borghei `product-designer` |
| 设计评审和可用性测试 | Owl design-ops/prototyping/visual-critique 组，RefoundAI `running-design-reviews`、`usability-testing` |
| PRD 拆成工程任务 | Borghei `spec-to-repo` |
