---
name: task-council
description: Use when a complex decision, formal专题会, or external research request has ambiguous scope, multiple options, disputed recommendations, cross-functional trade-offs, major risk, or a need for structured multi-perspective deliberation.
---

# Task Council

这是由 `ai-native-delivery-governor` 选择的复杂方案决策上层应用 Skill。决策记录、方案对比和会议结论走 `DOCUMENT_DELIVERY`；决策同时进入代码实现时走 `MIXED_DELIVERY`，两条底座分别通过后才能汇合。

把专题会作为决策质量流程，而不是搜索或报告生成器。先确认要解决什么问题、要交付什么证据，再选择能力、组织独立视角、质询和收敛。会议不替代专业调研、实施验证及决策负责人的最终权责。

## 不可违背的原则

- 明确决策负责人；主席组织和综合，不替代负责人拍板。
- 区分 `FACT`、`ASSUMPTION`、`INFERENCE`、`UNKNOWN`；角色偏好和多数意见不是证据。
- 席位用于组织视角；真实 Agent 用于取得独立判断、证据或验证；外部 Skill/工具只是执行能力。三者不得混同。
- 不得把预设结论包装成会议结论。早期倾向标为 `WORKING_HYPOTHESIS`，并写明推翻条件。
- 不得将同一机制的参数、供应商或实现组件包装成不同架构方案；但当用户要调研“仓库/服务商”时，候选来源必须作为**调研对象**逐项记录，不得被架构讨论吞没。
- 重要主张回到原始材料、数据、测试、调研或独立复核；保留重要异议与证据缺口。

## 阶段 0：需求发现门禁

在搜索、选择角色、生成方案、调用外部 Skill 或派发 Agent 前，先形成下列卡片。外部调研必须读取 `references/research-discovery.md`。

```text
议题：
核心决策或调研问题（一句话，不包含预设解法）：
调研对象：开源仓库 / 服务商 / 技术路线 / 其他：
预期交付：清单 / 对比 / 短名单 / PoC 建议 / 最终选型：
优先级与范围：
成功标准与硬约束：
“免费”定义（如适用）：FREE_FOREVER / FREE_QUOTA / TIME_LIMITED_TRIAL / SALES_APPLIED_POC / 其他：
技术展开深度：一行用途 / 架构比较 / 其他：
本次明确不解决：
已知事实、关键未知、工作假设及推翻条件：
状态：DISCOVERY_CONFIRMED / PROVISIONAL / NEED_CLARIFICATION
```

缺失会改变调研对象、筛选条件、交付形态或数据边界的信息时，使用 `NEED_CLARIFICATION`：展示可修改草案，只问 1–3 个实质问题并等待回答。不得以“用户已经说了专题名称”“可以先看一看”或“技术路线显而易见”为由提前搜索。

目标清晰、低风险且可逆时可使用 `PROVISIONAL`，但必须写明默认假设和推翻条件。`DISCOVERY_CONFIRMED` 确认研究什么；它不等于批准真实 Agent、付费工具或实施。

## 阶段 1：会议大纲与外部能力门禁

将需求发现卡片扩展为会议大纲，明确决策层级、负责人、范围内外、成功标准、交付和待验证问题。大纲状态为 `AGENDA_CONFIRMED / PROVISIONAL / NEED_CLARIFICATION`。

若涉及外部事实、开源仓库或服务商，在开始检索前：

1. 读取 `references/task-routing.md` 和 `references/external-capability-routing.md`。
2. 建立外部能力台账：调研问题、所需证据、Skill/工具、数据与成本边界、可用状态、降级方式。
3. 只在 `DISCOVERY_CONFIRMED` 或已声明的 `PROVISIONAL` 下使用外部能力；真实 Agent 派发另行确认。

Skill/工具不可用、缺凭证、需付费或存在未获批准的数据外发时，标记 `UNAVAILABLE`、`USER_CONFIRMATION_REQUIRED` 或 `NEED_EVIDENCE`。记录替代方式与缺口；不得声称已经使用不可用能力，亦不得因工具能搜到更多内容而扩大调研范围。

## 阶段 2：构造调研或决策结构

### 外部调研

先按调研对象建立证据线，再形成结论：

- **开源仓库线**：仓库、许可证、部署入口、维护证据、真实运行证据、适用边界和排除风险。
- **服务商线**：产品、目标能力、免费类型、额度/期限、开通条件、数据边界、私有化可能性和排除风险。
- **红队线**：核验营销表述、许可证、维护、免费条件、数据边界和无法落地的反例。

技术仅以一行说明候选用途。只有用户确认本次交付包含架构选型时，才进入技术方案比较。

### 架构或机制决策

仅在已确认需要比较架构、机制、参数或执行路线时，读取 `references/option-architecture.md`。为真正独立的方案建立机制指纹，合并仅有参数差异的情景，并使用同一组评价标准。推荐只能在独立陈述、质询和修订之后产生。

## 阶段 3：证据、席位与运行模式

1. 建立证据台账；每个重要事实附来源、日期、适用范围或验证动作。
2. 读取 `references/meeting-formation.md`；按证据缺口选择 2–5 个互补席位。
3. 每席写清独立问题、证据或工具边界、初始主张和改变条件。
4. 主席和秘书是流程角色，不参与表决；人物透镜不是证据。

外部调研的标准席位为需求澄清、开源侦察、服务商侦察和红队。它们必须使用不同问题或证据边界；不能做到时减少席位并如实说明。

默认 `SIMULATED`。只有用户确认席位、工具、成本、工作量和派发方式，且每个 Agent 能产生独立且可能改变结论的结果时，才使用 `REAL_MULTI_AGENT`，状态为 `DISPATCH_CONFIRMED`。`SIMULATED` 只能称为“结构化分析”，不得宣称已经完成真实独立辩论或正反博弈。

## 阶段 4：独立陈述、质询、修订与裁决

1. 收集首轮独立陈述；本轮结束前不展示其他席位结论。
2. 由红队或审慎席定向质询具体主张，围绕证据缺口、反例、数据边界、免费条件、许可证、维护、交付限制和方案同质化。
3. 要求提案席以 `KEEP / REVISE / WITHDRAW / NEED_EVIDENCE / MERGE_AS_VARIANT` 回应并记录理由。
4. 再次执行独立性检查；将同质候选合并为参数情景，但保留被排除的仓库或服务商及理由。
5. 用相同标准比较修订后的候选；决策负责人选择 `GO / GO_WITH_GUARDRAILS / EXPERIMENT_REQUIRED / NEED_EVIDENCE / NO_GO / BLOCKED`。

## 输出与完成闸门

读取 `references/output-templates.md`。当交付是外部调研时，先给范围与请求的清单表，再给证据缺口、红队结论和下一步；不要用未被请求的技术架构淹没仓库或服务商结果。

结束前确认：

- 需求发现已确认，或 `PROVISIONAL` 假设和推翻条件可见。
- 外部能力、数据边界、可用状态与降级路径已记录。
- 调研对象、交付形态、免费定义和技术展开深度未发生漂移。
- 每项重要事实有来源、日期、适用范围或 `UNKNOWN`；不可用工具没有被伪装成已使用。
- 正反观点有独立问题和正式回应；模拟分析的限制已说明。
- 结论、被拒绝项、保留异议、负责人、验收证据和停止/复盘条件完整。
