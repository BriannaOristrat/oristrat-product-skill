# oristrat-product-skill

产品测试与交付报告工作流仓库。

本仓库按 GitHub 可维护结构组织。Obsidian 不再维护第二份目录，直接使用本仓库内的 Markdown 文件：

- GitHub / repo 主结构：`00_入口/01_产物/github/测试报告skill/`
- Obsidian 直接入口：`00_入口/01_产物/github/测试报告skill/README.md`

## 快速入口

| 入口 | 用途 |
|---|---|
| [总览](docs/00-overview.md) | 阅读整体结构、产物边界和执行顺序 |
| [测试任务启动](docs/workflows/01-test-task-intake.md) | 明确范围、环境、账号、风险和写入权限 |
| [测试执行与证据采集](docs/workflows/02-test-execution-and-evidence.md) | 执行手工、自动化、压测和大数据专项 |
| [报告生成](docs/workflows/03-report-generation.md) | 生成运行过程证据报告、实际交付报告和业务论证报告 |
| [交付包归档](docs/workflows/04-delivery-package-and-archive.md) | 生成 zip、清理临时文件、归档最终产物 |
| [Skill / 工具矩阵](docs/matrices/skill-tool-responsibility-matrix.md) | 明确 Skill、脚本和检查工具职责 |
| [Obsidian 直接使用说明](docs/matrices/obsidian-usage-map.md) | 明确 Obsidian 如何直接读取 GitHub 仓库内容 |

## 最重要的门禁

正式交付或提交 GitHub 前必须通过这些检查：

- [运行过程证据报告检查](docs/checklists/01-evidence-report-review.md)
- [实际交付报告检查](docs/checklists/02-actual-delivery-report-review.md)
- [五轮业务论证与结果检查](docs/checklists/03-five-round-report-review.md)
- [PDF / HTML 安全门禁](docs/checklists/04-pdf-html-safety-gate.md)
- [最终交付门禁](docs/checklists/05-final-delivery-gate.md)
- [GitHub 提交安全门禁](docs/checklists/06-github-submit-safety-gate.md)

## 结构原则

1. `docs/workflows/` 写人如何执行流程。
2. `docs/checklists/` 写交付前如何验收。
3. `docs/matrices/` 写职责和产物映射。
4. `docs/templates/` 写可复制模板。
5. `skills/*/SKILL.md` 写 Agent 执行规范。
6. `tools/` 放脚本；脚本必须由检查清单约束。
7. Obsidian 直接读取 GitHub 主结构，不维护第二份文档。
8. 提交 GitHub 前必须执行敏感信息强检查。
