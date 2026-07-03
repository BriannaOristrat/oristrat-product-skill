# Obsidian 直接使用说明

## 原则

`00_入口/01_产物/github/测试报告skill/` 是唯一文档源。Obsidian 直接读取这个目录里的 Markdown 文件，不再复制第二份正文。

## Obsidian 入口

| 内容 | 直接打开 |
|---|---|
| 首页 | `00_入口/01_产物/github/测试报告skill/README.md` |
| 总览 | `00_入口/01_产物/github/测试报告skill/docs/00-overview.md` |
| 工作流 | `00_入口/01_产物/github/测试报告skill/docs/workflows/` |
| 检查清单 | `00_入口/01_产物/github/测试报告skill/docs/checklists/` |
| Skill | `00_入口/01_产物/github/测试报告skill/skills/` |

## 不复制范围

| 内容 | 原因 |
|---|---|
| 第二份 Obsidian 专用目录 | 已废弃，避免维护第二份正文 |
| `output/`、`tmp/` | 属于执行产物或临时产物，容易污染知识库 |
| `node_modules/`、`__pycache__/` | 依赖和缓存，不应进入 Obsidian |
| PDF、截图、JSON 证据原件 | 证据包由交付目录维护，仓库只保留结构说明 |
| 本机绝对路径 | 面向共享阅读时不可出现 |

## 检查规则

每次修改仓库后，至少检查：

1. GitHub 仓库存在 `README.md`、`docs/`、`skills/`、`tools/`、`examples/`、`assets/`。
2. 仓库 Markdown 不包含 `file://`、`C:\`、`C:/` 或用户目录。
3. 不再创建第二份 Obsidian 专用目录。
4. 新增流程、清单、矩阵或模板时，只写入 GitHub 仓库。
