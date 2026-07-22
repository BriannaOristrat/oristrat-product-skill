# Skill 来源治理与 AI 路由规则

## 目标

让 GitHub、Obsidian 和 AI 在使用 Skill 时先区分来源，再决定是否读取、复用、包装或沉淀到自研仓库。

本仓库只维护 Oristrat 自研 Skill。外部 Skill、系统 Skill、插件 Skill、本地个人 Skill 和任务临时产物不直接复制进本仓库。

## 来源分类

| 类型 | 是否放入本仓库 | 典型位置 | AI 使用规则 |
|---|---|---|---|
| 自研 Skill | 是 | `skills/<skill-name>/` | 优先读取本仓库 `SKILL.md` 和 `references/`，按仓库门禁维护 |
| 自研 Skill 仓库 | 视仓库职责决定 | `github/<repo-name>/` | 如果是另一个自研 Skill 仓库，只做链接或说明，不复制正文 |
| 外部/非自研 Skill | 否 | Codex 系统、插件、社区或第三方来源 | 作为依赖调用，不放入正式 `skills/`；需要真实运行时必须通过 Codex 插件、系统 Skill 或正式安装入口 |
| 外部 Skill 缓存 | 否 | `external-skills/<source-name>/` | 只做来源追溯、方法对照和 license 记录，不作为运行入口，不直接作为自研 Skill 触发 |
| 本地个人 Skill | 否，除非正式转自研 | 本地 Codex/Agent skills 目录 | 只记录使用边界；转自研前必须重写、脱敏、补齐 owner 和门禁 |
| 任务临时产物 | 否 | `work/`、`outputs/`、交付证据目录 | 不登记为 Skill，只作为一次性执行证据或产物 |
| 候选自研 Skill | 暂不放入正式 `skills/` | 需求草稿、实验目录 | 稳定复用后再建 `skills/<skill-name>/` 并登记 Catalog |

## AI 路由顺序

1. 先判断任务是否属于 Oristrat 自研流程、业务规则、交付规范或团队私有方法。
2. 如果属于，优先读取本仓库 `skills/<skill-name>/SKILL.md`。
3. 如果是通用能力，例如 GitHub、PDF、Obsidian、浏览器、表格、文档、数据分析，优先使用当前 Codex 环境里已有的外部 Skill 或插件。
4. 如果外部 Skill 需要叠加 Oristrat 私有规则，只创建轻量自研包装 Skill；包装 Skill 只写 Oristrat 规则和入口。
5. 如果用户明确要求安装外部 Skill，优先通过 Codex 插件、系统 Skill 或该外部 Skill 的正式稳定安装方式使用；`external-skills/` 只能记录来源、版本、license 和方法对照，不能作为执行入口。
6. 如果只是一次性脚本、报告、截图、日志或验证产物，不纳入 `skills/`。
7. 如果用户要求新增 Skill，先按本页分类，再决定是加入本仓库、引用外部 Skill，还是保持为临时产物。

## 自研 Skill 入库标准

- 有明确 Oristrat 业务场景或团队复用价值。
- 有稳定触发描述，能写入 `SKILL.md` frontmatter 的 `description`。
- 有 owner 或维护责任。
- 需要的长文档放在 `references/`，脚本放在 `scripts/`，资产放在 `assets/`。
- 不包含账号、密码、token、API key、私钥、cookie、session、本机用户路径或客户敏感数据。
- 已登记到 [Skill Catalog](../catalog/README.md)。

## 不入库标准

- 只是 Codex 系统能力或插件能力。
- 只是第三方 Skill 的原文、教程或安装缓存；这类内容只能作为 `external-skills/` 来源缓存，不进入正式 `skills/`。
- 需要真实调用的外部过程能力或工具链；这类能力必须走 Codex 插件、系统 Skill 或正式安装入口，不能从 `external-skills/` 降级执行。
- 只是某次任务的临时脚本、日志、截图或交付结果。
- 只服务个人本地偏好，尚未成为团队规范。
- 无法脱敏或版权/来源不清。

## Catalog 字段要求

Catalog 至少记录：

| 字段 | 含义 |
|---|---|
| Skill | Skill 名称 |
| 来源 | `自研`、`外部依赖`、`本地个人`、`候选` |
| 是否入库 | 是否正式放入本仓库 `skills/` |
| 路径/入口 | 本仓库相对路径或外部来源说明 |
| 使用边界 | AI 什么时候应该使用，什么时候不应该使用 |

## Obsidian 使用规则

- Obsidian 直接打开本仓库 Markdown，先从 [README](../README.md) 或本页判断 Skill 来源。
- 自研 Skill 使用本仓库相对链接。
- 外部 Skill 只记录来源类型和使用边界，不复制外部正文。
- 如果一个 Skill 不属于自研仓库，不要为了 Obsidian 阅读方便把它复制到本仓库。

## 外部插件运行规则

当外部 Skill 是交付流程中的真实运行依赖时，必须按正式运行入口使用：

- Codex 插件提供的 Skill，使用当前环境可发现的插件 Skill 名称调用。
- Codex 系统 Skill，使用系统已安装入口调用。
- 第三方 Skill，使用其稳定 release 或官方安装方式，不从 `external-skills/` 直接执行。

`external-skills/` 可以保存来源缓存、调研材料、license 记录和方法对照，但不能替代正式运行入口。若某流程要求的外部插件不可用，应把该步骤标记为 `BLOCKED_EXTERNAL_PLUGIN_NOT_INSTALLED` 或更具体的阻塞状态，而不是读取缓存副本继续执行。

例如 `obra/superpowers` 在 MSCE 研发流程中必须作为 Codex 插件运行；如果 `superpowers:*` 不可发现，研发流程应标记 `BLOCKED_SUPERPOWERS_PLUGIN_NOT_INSTALLED`。不得复制、提交或从 `external-skills/` 执行 Superpowers 源码、skill 正文、模板、脚本或资源文件。

## 运行版本门禁

- `catalog/runtime-skill-lock.json` 记录正式自研源、用户级安装名和外部依赖入口。
- 修改自研 Skill 后运行 `tools/validate_skills_utf8.ps1`，固定 UTF-8 验证，避免 Windows 默认编码造成假失败。
- 运行 `tools/check_skill_install_sync.ps1` 比较正式源与用户级安装副本。`DRIFT` 表示运行时可能没有采用仓库最新规则。
- 检查工具只读；同步或覆盖用户级安装目录必须获得单独授权。
- 可选外部能力不可用时记录 `UNAVAILABLE_OPTIONAL` 并走自研 fallback；只有该能力是用户要求或交付结果不可替代的必要条件时才标记 `BLOCKED`。
- 外部 Skill 的缓存存在不等于正式能力已安装，也不得作为“已使用”的证据。
