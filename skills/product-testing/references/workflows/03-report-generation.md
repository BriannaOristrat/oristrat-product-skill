# 03 报告生成工作流

## 目标

从结构化证据生成三份报告，并保持结论一致。

## 报告集合

| 编号 | 报告 | 定位 |
|---|---|---|
| 01 | 运行过程证据报告 | 内部复核和审计，保留详细证据 |
| 02 | 实际交付报告 | 客户/业务可读，正文标题固定为“测试报告” |
| 03 | 五轮业务论证与结果 | 说明业务论证、统一用例和统计口径 |

## 默认工具

```powershell
python skills/product-testing/scripts/generate_delivery_artifacts.py
```

该工具负责：

- 读取 `evidence/` 下的结构化证据。
- 生成 `.md`、`.html`、`.pdf` 三种阅读形态。
- 生成正式压测关键失败分布图。
- 校验三份报告结论一致性。
- 阻断三份报告中的本机路径泄漏，尤其是 `02_实际交付报告`。
- 打包最终交付 zip。

## 固定配色和压测图规则

- 报告和压测图固定使用低饱和绿色系：标题 `#0B3D2E`、表头 `#C8E0D0`、卡片底色 `#F4FAF6`、强调色 `#2F6B4F`、边框 `#B7D6C3`。
- `02_实际交付报告` 必须包含“正式压测关键失败分布”内容：错误率、失败 / 样本、P95 / P99、最大响应、分场景表格和判定说明。
- 示例截图只作为版式参考；生成时必须使用实际压测证据，指标来自 `formal_load_summary.json`、`formal_load_failure_responses.json` 等本次证据文件，不得复用示例数值。
- 若实际压测证据缺失或字段不足，不得伪造图片和指标；报告应标记为未生成/待补证据，并要求补齐正式压测后重新生成。
- `01_运行过程证据报告` 必须保留 `02` 中异常、观察项、不通过项的明细证据，包括失败响应样本、关键失败分布图、源 JSON 和必要的错误截图。

默认归档根目录固定为 `D:\AAAA\资料归档\codex_files\00_入口\01_产物\输出\报告`。如果该本地归档根不可用，则回退到 `自研skill\输出\报告`，不得默认落到当前 C 盘工作区。

报告生成脚本的 `REPORT_DIR` 是单次交付报告文件夹；最终 zip 会生成在 `REPORT_DIR` 的父目录。执行 OB 测试时，应优先把 `REPORT_DIR` 设置为归档根目录下的任务子目录，例如 `...\输出\报告\ob-项目名-日期-acceptance`。

如需指定单次交付目录，设置：

```powershell
$env:ORISTRAT_REPORT_DIR="<交付报告目录>"
python skills/product-testing/scripts/generate_delivery_artifacts.py
```

## 报告标题规则

| 文件 | 文件名 | 正文标题 |
|---|---|---|
| `01_运行过程证据报告.*` | 保持编号和说明 | 运行过程证据报告 |
| `02_实际交付报告.*` | 保持历史文件名 | 测试报告 |
| `03_五轮业务论证与结果.*` | 保持编号和说明 | 五轮业务论证与结果文档 |

## 生成后必须执行

1. [运行过程证据报告检查](../checklists/01-evidence-report-review.md)
2. [实际交付报告检查](../checklists/02-actual-delivery-report-review.md)
3. [五轮业务论证与结果检查](../checklists/03-five-round-report-review.md)
4. [PDF / HTML 安全门禁](../checklists/04-pdf-html-safety-gate.md)
