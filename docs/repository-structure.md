# 仓库结构说明

## 定位

本仓库是多 Skill 仓库，用于沉淀 Oristrat 产品团队可复用的 Agent Skill、流程文档、检查门禁和辅助脚本。

## 根目录职责

| 目录 | 职责 |
|---|---|
| `catalog/` | Skill 索引和新增登记规则 |
| `skills/` | 每个自研 Skill 的独立包 |
| `docs/` | 跨 Skill 的仓库级说明、来源治理、Obsidian 入口、安全门禁 |
| `tools/` | 跨 Skill 的通用工具 |
| `assets/` | 跨 Skill 共用静态资源 |
| `examples/` | 跨 Skill 示例，不放真实敏感数据 |

## 单个 Skill 标准结构

```text
skills/<skill-name>/
  SKILL.md
  references/
  scripts/
  assets/
```

## 分层规则

- 一个自研 Skill 自己的流程、清单、矩阵、模板放入 `skills/<skill-name>/references/`。
- 一个自研 Skill 自己的脚本放入 `skills/<skill-name>/scripts/`。
- 多个 Skill 共用的规则放入根目录 `docs/`。
- 多个 Skill 共用的脚本放入根目录 `tools/`。
- 外部 Skill、系统 Skill、插件 Skill、本地个人 Skill 和任务临时产物不复制进本仓库。
- 新增 Skill 前先执行 [Skill 来源治理与 AI 路由规则](skill-source-governance.md)。
- Obsidian 直接读取本仓库，不额外复制文档。
- GitHub 提交前统一执行 [GitHub 提交安全门禁](github-submit-safety-gate.md)。
