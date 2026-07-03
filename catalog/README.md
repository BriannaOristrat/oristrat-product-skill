# Skill Catalog

本目录维护仓库内 Skill 的索引。新增 Skill 时，先在 `skills/<skill-name>/` 建立独立包，再登记到这里。

| Skill | 路径 | 状态 | 使用场景 |
|---|---|---|---|
| `product-testing` | [../skills/product-testing/SKILL.md](../skills/product-testing/SKILL.md) | active | 产品测试、证据报告、测试报告、交付包归档 |
| `evidence-report-review` | [../skills/evidence-report-review/SKILL.md](../skills/evidence-report-review/SKILL.md) | active | 复核运行过程证据报告 |
| `actual-delivery-report-review` | [../skills/actual-delivery-report-review/SKILL.md](../skills/actual-delivery-report-review/SKILL.md) | active | 复核客户可读测试报告 |
| `delivery-package-review` | [../skills/delivery-package-review/SKILL.md](../skills/delivery-package-review/SKILL.md) | active | 复核最终交付包和提交安全 |

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
