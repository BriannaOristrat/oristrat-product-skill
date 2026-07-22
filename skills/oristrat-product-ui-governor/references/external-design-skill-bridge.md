# 外部设计 Skill 桥接

外部 Skill 提供设计方法或执行能力；Oristrat 业务规则、产品底座、设计系统、工程约束和最终验收始终由自研 Skill 决定。

## 来源清单

| 来源 | 用途 | 正式入口 | 边界 |
|---|---|---|---|
| `Nutlope/hallmark` | 预扫描、反模板化结构、真实性、Token、状态、响应式、`audit/redesign/study` 方法 | 当前环境已安装的 `hallmark`；安装命令 `npx skills add nutlope/hallmark` | 不执行主题轮换和 `.hallmark/log.json`；不覆盖 Oristrat 设计系统 |
| `frontend-design` | 生产级视觉层级、可访问性、响应式和前端打磨 | 当前 Codex 可发现的 Skill | 作为实现质量补充，不拥有业务与 IA 决策 |
| `ui-ux-pro-max` | 产品类型、密度、设计系统候选、表单/反馈、无障碍和栈适配建议 | 当前环境可发现的正式 Skill/CLI | 输出是候选；不自动持久化 `design-system/`，不直接成为 Oristrat 标准 |

Hallmark 上游记录：

- Repository: `https://github.com/Nutlope/hallmark`
- Version: `1.1.0`
- Reviewed commit: `aeb42fb354ff4efa36ab475773a082315a3af2ce`
- Review date: `2026-07-20`
- License: MIT

UI UX Pro Max 上游记录：

- Repository: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- Local source record: `external-skills/nextlevelbuilder-ui-ux-pro-max-skill/`
- Version: `2.11.0`
- Installed commit: `5c0946f66120079258e1efc8e436d78ec793877c`
- Install verification date: `2026-07-21`
- License: MIT
- Formal execution: only an installed Skill or formal CLI; the cache is read-only source evidence

Hallmark runtime installation was verified at commit `aeb42fb354ff4efa36ab475773a082315a3af2ce` on `2026-07-21`. Its upstream top-level `version` field was moved into `metadata.version` in the installed copy for compatibility with the current Codex Skill validator; the rule body was not changed.

## 运行路由

1. 先执行本 Skill 的业务、IA、产品底座、页面类型和现有 Token 判断。
2. 新页面、系统级改版或确需设计系统候选时：如果正式 `ui-ux-pro-max` 可用，按产品类型、技术栈、密度、动效和结构生成候选；已有页面的小修不强制生成新设计系统。
3. 将候选与现有 Oristrat Token、组件、权限、路由、数据契约和 MSCE 边界对比，只采纳兼容部分。未经用户要求，不持久化外部生成的 `design-system/MASTER.md` 或页面 override。
4. 当前环境已安装 Hallmark 且任务为新建视觉页面、审计、改版或参考设计研究时，调用最窄模式，对选定方向进行预扫描或审计。
5. 使用 `frontend-design` 补强已选方向的视觉层级、语义结构、响应式和可访问性；它不重新选择业务模式。
6. 重新执行 Oristrat 业务适配、实现边界、表单反馈和最终质量门禁，再由 `product-testing` 做真实浏览器验收。
7. 任一外部能力不可用时，使用本 Skill 对应本地门禁，不从 `external-skills/` 缓存目录执行上游 Skill。

## 统一能力链

```text
Oristrat business/IA/product-base scan
→ ui-ux-pro-max candidate (only when useful and installed)
→ Oristrat candidate acceptance/rejection
→ Hallmark pre-flight/audit (only when installed)
→ frontend-design implementation polish (when installed)
→ Oristrat final quality gate
→ product-testing browser evidence
```

这是一条能力编排，不是把外部 Skill 源码拼接成新的上游副本。外部建议冲突时按以下优先级决策：用户明确要求 > Oristrat 业务/权限/产品底座 > MSCE/工程约束 > 现有设计系统 > 外部候选。

## Hallmark 模式映射

| Hallmark 意图 | Oristrat 模式 | 额外限制 |
|---|---|---|
| 默认设计 | `build` | 内部产品先走工作流结构，不自动选择营销主题 |
| `audit` | `audit` | 只读；结论需引用代码、截图或浏览器证据 |
| `redesign` | `redesign` | 保留路由、权限、数据契约、组件所有权和文案意图 |
| `study` | `study` | 只提取设计 DNA；拒绝像素复制和来源不明的付费模板 |

## UI UX Pro Max 使用映射

| 任务 | 使用方式 | Oristrat 限制 |
|---|---|---|
| 新系统/新页面 | 产品类型 + `nextjs`/实际栈 + density/motion 候选 | 内部工作台不套用营销页 Hero/CTA 结构 |
| 既有页面改版 | 查询相关 UX、表单、响应式和无障碍规则 | 复用现有 Token，不自动换色、换字体、换组件库 |
| 单组件/缺陷 | 只查对应 domain 或规则 | 不生成完整设计系统，不扩大改动范围 |
| 表单/认证 | 采用就近错误、密码眼睛、disabled、超时恢复、aria-live 等规则 | 服从项目既有表单与 Toast 组件语义 |

## 执行证据契约

每个候选外部能力记录：

```text
source: ui-ux-pro-max / hallmark / frontend-design
availability: INSTALLED / UNAVAILABLE / NOT_NEEDED
version_or_entry:
mode_or_query:
evidence:
accepted:
rejected:
fallback:
```

`UNAVAILABLE`、只读缓存研究或本地自研 fallback 都不能表述为“已运行该外部 Skill”。

## 明确不采用

- 不在 Oristrat 产品内部轮换 20 套主题。
- 不创建 `.hallmark/log.json` 作为项目运行依赖。
- 不要求所有页面采用不同结构；跨页一致性优先。
- 不默认输出自包含 HTML/CSS 或根目录 `tokens.css`。
- 不把外部 Skill 的评分印章写入生产样式。
- 不允许外部视觉规则覆盖角色权限、业务状态、MSCE 边界或现有设计系统。
