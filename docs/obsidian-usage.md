# Obsidian 直接使用说明

## 原则

仓库根目录是唯一文档源。Obsidian 直接读取这个目录里的 Markdown 文件，不再复制第二份正文。

## Obsidian 入口

| 内容 | 直接打开 |
|---|---|
| 首页 | [README](../README.md) |
| Skill Catalog | [Skill Catalog](../catalog/README.md) |
| 仓库结构 | [仓库结构说明](repository-structure.md) |
| 来源治理 | [Skill 来源治理与 AI 路由规则](skill-source-governance.md) |
| Product Testing | [Product Testing Skill](../skills/product-testing/SKILL.md) |
| Product Testing 总览 | [Product Testing 总览](../skills/product-testing/references/overview.md) |
| GitHub 提交门禁 | [GitHub 提交安全门禁](github-submit-safety-gate.md) |

## 不复制范围

| 内容 | 原因 |
|---|---|
| 第二份 Obsidian 专用目录 | 已废弃，避免维护第二份正文 |
| `output/`、`tmp/` | 属于执行产物或临时产物，容易污染知识库 |
| `node_modules/`、`__pycache__/` | 依赖和缓存，不应进入 Obsidian |
| PDF、截图、JSON 证据原件 | 证据包由交付目录维护，仓库只保留结构说明 |
| 本机绝对路径 | 面向共享阅读时不可出现 |
| 外部 Skill 正文 | 只记录来源和使用边界，避免把非自研内容混入自研仓库 |
| 本地个人 Skill | 未转自研前不复制进仓库，避免 AI 误判为团队标准 |

## 检查规则

每次修改仓库后，至少检查：

1. GitHub 仓库存在 `README.md`、`catalog/`、`docs/`、`skills/`、`tools/`、`examples/`、`assets/`。
2. 仓库共享入口不使用本机绝对路径；安全检查清单中可保留用于检测路径泄漏的规则。
3. 不再创建第二份 Obsidian 专用目录。
4. 新增 Skill 前先按 [Skill 来源治理与 AI 路由规则](skill-source-governance.md) 判断是否属于自研。
5. 新增流程、清单、矩阵或模板时，只写入 GitHub 仓库。
