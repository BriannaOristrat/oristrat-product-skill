# Skill Catalog

本目录维护仓库内 Skill 的索引。新增 Skill 时，先按 [Skill 来源治理与 AI 路由规则](../docs/skill-source-governance.md) 判断来源，再决定是否在 `skills/<skill-name>/` 建立独立包。

## 三层运行架构

| 层级 | 组成 | 运行方式 |
|---|---|---|
| 总控入口 | `ai-native-delivery-governor` | 识别任务、选择上层应用、维护授权和状态，并自动组合底座能力 |
| 代码交付底座 | `fullstack-delivery-orchestration`、运行态检查、`msce-engine-app-development`、Git 门禁 | 交付代码结果；严格验证实现、真实运行和提交边界 |
| 文档交付底座 | `document-delivery-orchestration` | 交付 PRD、决策、报告、手册和资料包；验证证据、内容、格式、安全与归档 |
| 上层应用 | `product-design-management`、`oristrat-product-ui-governor`、`product-testing`、`task-council` | 分别处理需求/PRD、UI/UX 改版、产品测试和复杂方案专题会 |

总控先把结果分类为 `CODE_DELIVERY`、`DOCUMENT_DELIVERY` 或 `MIXED_DELIVERY`，再选择应用并自动组合底座。混合交付必须分别通过 `MSCE_SUBMISSION_GATE` 和 `DOCUMENT_DELIVERY_GATE`，共享事实一致后才能通过 `MIXED_DELIVERY_GATE`。

## 自研 Skill

| Skill | 来源 | 是否入库 | 路径 | 状态 | 使用边界 |
|---|---|---|---|---|---|
| `task-council` | 自研 | 是 | [../skills/task-council/SKILL.md](../skills/task-council/SKILL.md) | active | 复杂任务、争议方案、跨职能取舍或重大决策的角色化会议编制；按需选择角色与席位，保留异议并形成有证据的行动决议 |
| `ai-native-delivery-governor` | 自研 | 是 | [../skills/ai-native-delivery-governor/SKILL.md](../skills/ai-native-delivery-governor/SKILL.md) | active | AI 原生交付总控，在产品底座上协调产品、研发、测试、多 agent、多轮论证、MSCE 规范、QA 证据和发布门禁 |
| `document-delivery-orchestration` | 自研 | 是 | [../skills/document-delivery-orchestration/SKILL.md](../skills/document-delivery-orchestration/SKILL.md) | active | 文档交付底座，统一治理来源证据、内容复核、多格式渲染、安全检查、交付包、归档和可选 Git 提交 |
| `product-design-management` | 自研 | 是 | [../skills/product-design-management/SKILL.md](../skills/product-design-management/SKILL.md) | active | 需求分析、产品设计、产品规范、PRD、路线图、用户故事、设计评审、研发交付拆解 |
| `oristrat-product-ui-governor` | 自研 | 是 | [../skills/oristrat-product-ui-governor/SKILL.md](../skills/oristrat-product-ui-governor/SKILL.md) | active | Oristrat 产品 UI 总控：业务场景、IA、界面设计、审计、改版、参考设计研究、视觉质量和浏览器验收门禁 |
| `fullstack-delivery-orchestration` | 自研 | 是 | [../skills/fullstack-delivery-orchestration/SKILL.md](../skills/fullstack-delivery-orchestration/SKILL.md) | active | PM 主控的全栈交付编排，协调全栈工程师、QA 点击测试、代码/安全/发布评审和长任务循环 |
| `msce-engine-app-development` | 自研 | 是 | [../skills/msce-engine-app-development/SKILL.md](../skills/msce-engine-app-development/SKILL.md) | active | MSCE / MortiseSpecCodeEngine 开发、组件隔离、Harness、staged scope 和基线感知验证 |
| `product-testing` | 自研 | 是 | [../skills/product-testing/SKILL.md](../skills/product-testing/SKILL.md) | active | 产品测试、证据报告、测试报告、交付包归档 |
| `evidence-report-review` | 自研 | 是 | [../skills/evidence-report-review/SKILL.md](../skills/evidence-report-review/SKILL.md) | active | 只复核 `01_运行过程证据报告` |
| `actual-delivery-report-review` | 自研 | 是 | [../skills/actual-delivery-report-review/SKILL.md](../skills/actual-delivery-report-review/SKILL.md) | active | 只复核客户可读的 `02_实际交付报告` |
| `delivery-package-review` | 自研 | 是 | [../skills/delivery-package-review/SKILL.md](../skills/delivery-package-review/SKILL.md) | active | 只复核最终交付包、zip 和提交安全 |

## 外部 Skill 与不入库内容

| 类型 | 来源 | 是否入库 | AI 使用边界 |
|---|---|---|---|
| Codex 系统 Skill | 外部依赖 | 否 | 例如通用文档、PDF、图片、Skill 创建能力；直接调用当前环境能力，不复制到本仓库 |
| 插件 Skill | 外部依赖 | 否 | 例如 GitHub、浏览器、数据分析、Figma、Notion 等插件能力；作为依赖调用 |
| 外部 Skill 缓存 | 外部依赖 | 否 | 仅用于来源追溯和方法参考，放在本地忽略目录 `external-skills/`；正式输出必须通过自研 Skill 重写 |
| `Nutlope/hallmark` | 外部依赖 | 否 | [来源、版本、License 与使用边界](../skills/oristrat-product-ui-governor/references/external-design-skill-bridge.md)；正式运行使用已安装 Hallmark，自研入口为 `oristrat-product-ui-governor` |
| `nextlevelbuilder/ui-ux-pro-max-skill` | 外部依赖 | 否 | [统一 UI/UX 能力链](../skills/oristrat-product-ui-governor/references/external-design-skill-bridge.md)；正式 Skill/CLI 只生成候选，自研 UI 总控决定采用与拒绝内容 |
| 本地个人 Skill | 本地个人 | 否 | 只有正式转为团队自研规范后，才重写并放入 `skills/` |
| 任务临时产物 | 临时产物 | 否 | 脚本草稿、执行日志、截图、交付包不登记为 Skill |

## 新增 Skill 规则

```text
skills/<skill-name>/
  SKILL.md
  references/
  scripts/
  assets/
```

- `SKILL.md` 写触发场景、执行顺序和必须门禁。
- `references/` 放长文档、流程、检查清单、模板。
- `scripts/` 放这个 Skill 专用脚本。
- `assets/` 放这个 Skill 专用静态资源。
- 跨 Skill 的规则和工具放回根目录 `docs/` 或 `tools/`。
- 外部 Skill 不放入正式 `skills/`；若用户明确要求安装作为调研来源，放入 `external-skills/` 并记录 license 与使用边界。
