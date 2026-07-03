# oristrat-product-skill

Oristrat 产品团队的多 Skill 仓库。这里不是单个测试报告项目，而是集中维护多个可复用 Skill、对应参考文档、脚本和仓库级安全门禁。

Obsidian 不再维护第二份目录，直接把本仓库作为可读目录打开；所有链接使用仓库内相对 Markdown 链接，GitHub 和 Obsidian 共用同一套结构。

## 快速入口

| 入口 | 用途 |
|---|---|
| [Skill Catalog](catalog/README.md) | 查看当前仓库收录的 Skill |
| [仓库结构说明](docs/repository-structure.md) | 查看多 Skill 仓库的目录规范 |
| [Obsidian 直接使用说明](docs/obsidian-usage.md) | 查看 GitHub / Obsidian 共用方式 |
| [GitHub 提交安全门禁](docs/github-submit-safety-gate.md) | 提交前检查账号、密码、token、key 等敏感信息 |
| [Product Testing Skill](skills/product-testing/SKILL.md) | 产品测试、证据报告、实际交付报告工作流 |
| [Product Testing 总览](skills/product-testing/references/overview.md) | 当前测试报告 Skill 的流程和产物总览 |

## 当前 Skill

| Skill | 路径 | 定位 |
|---|---|---|
| `product-testing` | [skills/product-testing/SKILL.md](skills/product-testing/SKILL.md) | 产品测试、运行过程证据报告、实际交付报告、交付包归档 |
| `evidence-report-review` | [skills/evidence-report-review/SKILL.md](skills/evidence-report-review/SKILL.md) | 专门复核 `01_运行过程证据报告` |
| `actual-delivery-report-review` | [skills/actual-delivery-report-review/SKILL.md](skills/actual-delivery-report-review/SKILL.md) | 专门复核客户可读的 `02_实际交付报告` |
| `delivery-package-review` | [skills/delivery-package-review/SKILL.md](skills/delivery-package-review/SKILL.md) | 专门复核最终交付包、zip 和提交安全 |

## 结构原则

1. 每个 Skill 独立放在 `skills/<skill-name>/`。
2. 单个 Skill 内部只保留 `SKILL.md`、`references/`、`scripts/`、`assets/` 等执行所需内容。
3. 根目录 `docs/` 只放跨 Skill 的仓库规则、Obsidian 说明、GitHub 提交门禁。
4. 根目录 `tools/` 只放跨 Skill 的通用工具；某个 Skill 专用脚本放到该 Skill 的 `scripts/`。
5. 根目录 `catalog/` 维护 Skill 目录，后续新增 Skill 先登记到这里。
6. 提交 GitHub 前必须通过 [GitHub 提交安全门禁](docs/github-submit-safety-gate.md)。
