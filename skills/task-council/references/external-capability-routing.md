# External Capability Routing

`task-council` is the governance and decision-record layer. The repositories below are cached upstream tools under `external-skills/`; they are optional execution or verification capabilities, not mandatory dependencies.

选择外部能力的前提是 `DISCOVERY_CONFIRMED` 或已说明的 `PROVISIONAL`，而不是 `REAL_MULTI_AGENT`。真实 Agent 派发与工具使用是独立闸门。先建立能力台账，再记录选用能力、版本、配置边界、数据/成本边界和输出限制。

| 状态 | 含义 | 必须动作 |
|---|---|---|
| `READY` | 前提、权限和边界满足 | 按已界定问题使用。 |
| `UNAVAILABLE` | 工具或访问不可用 | 记录缺口和已批准替代方式。 |
| `USER_CONFIRMATION_REQUIRED` | 需要付费、凭证、数据外发或新权限 | 等待用户确认。 |
| `NOT_NEEDED` | 不会增加决策相关证据 | 不调用。 |

| Need | Preferred upstream capability | Local source | Use boundary |
|---|---|---|---|
| Codex-native council with anonymized candidate review and preflight | `codex-council` | `external-skills/ercoledevs-codex-council/skills/codex-council/` | Use for high-risk Codex review when its own approval and token preflight are accepted. Its role diversity is not multi-provider diversity. |
| Independent plans, anonymous random-order review, and separate judge | `llm-council` | `external-skills/am-will-codex-skills/skills/llm-council/` | Use only when distinct configured planner runtimes can produce genuinely independent plans. Do not treat multiple prompts to one shared context as independent evidence. |
| Structured 3-4 round expert debate with a separate moderator | `agent-roundtable` | `external-skills/erickong-agent-roundtable/` | Use only after its Python dependencies and provider configuration are explicitly approved. Require the moderator to retain unresolved dissent rather than force convergence. |
| Independent validation and adversarial review gate | `metaswarm` review and validation skills | `external-skills/dsifry-metaswarm/skills/` | Use the relevant review gate, rubric, or validation protocol; do not automatically adopt the full SDLC workflow, project state system, or PR automation. |

## Selection Rules

1. Prefer the smallest tool that supplies the missing capability.
2. Run the discovery card, capability ledger and evidence ledger before an external runtime; pass bounded questions rather than an unframed topic.
3. Use distinct evidence or tool boundaries for real agents. A different role label alone does not establish independence.
4. Keep original artifacts available for audit. The chair must independently validate material claims, citations, tests, or calculations.
5. If prerequisites, credentials, cost approval or source access are absent, record the status and downgrade path; do not silently substitute a claimed capability or expand the research scope.

## Capability Ledger

| 调研问题 | 所需证据 | Skill/工具 | 数据与成本边界 | 状态 | 降级方式 |
|---|---|---|---|---|---|
|  |  |  |  | READY / UNAVAILABLE / USER_CONFIRMATION_REQUIRED / NOT_NEEDED |  |

## Result Intake

For every accepted external result, add to the council record:

- Source repository and commit or release used.
- Run mode, participating models or agents, and evidence/tool boundaries.
- Claims adopted, claims rejected, and validation performed by the chair or an independent verifier.
- Remaining dissent, missing evidence, cost or privacy limits, and a reversal condition.
