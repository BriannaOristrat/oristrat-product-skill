# Skill Catalog

本目录维护仓库内 Skill 的索引。新增 Skill 时，先按 [Skill 来源治理与 AI 路由规则](../docs/skill-source-governance.md) 判断来源，再决定是否在 `skills/<skill-name>/` 建立独立包。

## 自研 Skill

| Skill | 来源 | 是否入库 | 路径 | 状态 | 使用边界 |
|---|---|---|---|---|---|
| `product-design-management` | 自研 | 是 | [../skills/product-design-management/SKILL.md](../skills/product-design-management/SKILL.md) | active | 需求分析、产品设计、产品规范、PRD、路线图、用户故事、设计评审、研发交付拆解 |
| `product-testing` | 自研 | 是 | [../skills/product-testing/SKILL.md](../skills/product-testing/SKILL.md) | active | 产品测试、证据报告、测试报告、交付包归档 |
| `evidence-report-review` | 自研 | 是 | [../skills/evidence-report-review/SKILL.md](../skills/evidence-report-review/SKILL.md) | active | 只复核 `01_运行过程证据报告` |
| `actual-delivery-report-review` | 自研 | 是 | [../skills/actual-delivery-report-review/SKILL.md](../skills/actual-delivery-report-review/SKILL.md) | active | 只复核客户可读的 `02_实际交付报告` |
| `delivery-package-review` | 自研 | 是 | [../skills/delivery-package-review/SKILL.md](../skills/delivery-package-review/SKILL.md) | active | 只复核最终交付包、zip 和提交安全 |

## 外部 Skill 与不入库内容

| 类型 | 来源 | 是否入库 | AI 使用边界 |
|---|---|---|---|
| Codex 系统 Skill | 外部依赖 | 否 | 例如通用文档、PDF、图片、Skill 创建能力；直接调用当前环境能力，不复制到本仓库 |
| 插件 Skill | 外部依赖 | 否 | 例如 GitHub、浏览器、数据分析、Figma、Notion 等插件能力；作为依赖调用 |
| 外部 Skill 缓存 | 外部依赖 | 否 | 仅用于来源追溯和方法参考，放在 [../external-skills/](../external-skills/)；正式输出必须通过自研 Skill 重写 |
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
