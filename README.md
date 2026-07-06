# oristrat-product-skill

Oristrat 产品团队的多 Skill 仓库。这里不是单个测试报告项目，而是集中维护多个可复用 Skill、对应参考文档、脚本和仓库级安全门禁。

Obsidian 不再维护第二份目录，直接把本仓库作为可读目录打开；所有链接使用仓库内相对 Markdown 链接，GitHub 和 Obsidian 共用同一套结构。

## 快速入口

| 入口 | 用途 |
|---|---|
| [Skill Catalog](catalog/README.md) | 查看当前仓库收录的 Skill |
| [仓库结构说明](docs/repository-structure.md) | 查看多 Skill 仓库的目录规范 |
| [Skill 来源治理](docs/skill-source-governance.md) | 区分自研、外部依赖、本地个人和临时产物 |
| [Obsidian 直接使用说明](docs/obsidian-usage.md) | 查看 GitHub / Obsidian 共用方式 |
| [GitHub 提交安全门禁](docs/github-submit-safety-gate.md) | 提交前检查账号、密码、token、key 等敏感信息 |
| [Product Design Management Skill](skills/product-design-management/SKILL.md) | 需求分析、产品设计、产品规范、PRD、路线图和 PM 工作流 |
| [Product Testing Skill](skills/product-testing/SKILL.md) | 产品测试、证据报告、实际交付报告工作流 |
| [Product Testing 总览](skills/product-testing/references/overview.md) | 当前测试报告 Skill 的流程和产物总览 |

## 当前 Skill

| Skill | 路径 | 定位 |
|---|---|---|
| `product-design-management` | [skills/product-design-management/SKILL.md](skills/product-design-management/SKILL.md) | 需求分析、产品设计、产品规范、PRD、路线图、用户故事、设计评审和研发交付拆解 |
| `product-testing` | [skills/product-testing/SKILL.md](skills/product-testing/SKILL.md) | 产品测试、运行过程证据报告、实际交付报告、交付包归档 |
| `evidence-report-review` | [skills/evidence-report-review/SKILL.md](skills/evidence-report-review/SKILL.md) | 专门复核 `01_运行过程证据报告` |
| `actual-delivery-report-review` | [skills/actual-delivery-report-review/SKILL.md](skills/actual-delivery-report-review/SKILL.md) | 专门复核客户可读的 `02_实际交付报告` |
| `delivery-package-review` | [skills/delivery-package-review/SKILL.md](skills/delivery-package-review/SKILL.md) | 专门复核最终交付包、zip 和提交安全 |

## 结构原则

1. 本仓库只正式收录 Oristrat 自研 Skill。
2. 每个自研 Skill 独立放在 `skills/<skill-name>/`。
3. 单个 Skill 内部只保留 `SKILL.md`、`references/`、`scripts/`、`assets/` 等执行所需内容。
4. 外部 Skill、插件 Skill、本地个人 Skill 和任务临时产物不放入正式 `skills/`；需要追溯时可放入 `external-skills/` 缓存并标注来源。
5. 根目录 `docs/` 只放跨 Skill 的仓库规则、Obsidian 说明、GitHub 提交门禁。
6. 根目录 `tools/` 只放跨 Skill 的通用工具；某个 Skill 专用脚本放到该 Skill 的 `scripts/`。
7. 根目录 `catalog/` 维护 Skill 目录，后续新增 Skill 先按 [Skill 来源治理](docs/skill-source-governance.md) 分类。
8. 提交 GitHub 前必须通过 [GitHub 提交安全门禁](docs/github-submit-safety-gate.md)。

## 外部 Skill 使用

本仓库允许参考 Codex 系统 Skill、插件 Skill、社区 Skill 和第三方 Skill，但正式入口必须是 Oristrat 自研 Skill。外部 Skill 只作为方法来源、模板对照和能力补充，不直接替代 `skills/<skill-name>/` 下的自研流程。

- 外部 Skill 正文默认不提交到 GitHub；如需本地调研，可放在本机 `external-skills/` 缓存目录。
- 自研 Skill 使用外部 Skill 时，应在 `references/` 中记录来源、用途、license 边界和使用口径。
- 维护者应定期检查外部 Skill 的上游版本、license 和适用性；需要更新时可手动更新本地缓存，并同步更新来源说明。
- 公开提交前不提交外部缓存正文，除非已确认 license、署名、再分发边界，并通过 GitHub 提交安全门禁。
