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

macOS / Linux：

```bash
python3 -m pip install -r requirements.txt
python3 skills/product-testing/scripts/generate_delivery_artifacts.py
```

Windows PowerShell：

```powershell
py -3 -m pip install -r requirements.txt
py -3 skills/product-testing/scripts/generate_delivery_artifacts.py
```

该工具负责：

- 读取 `evidence/` 下的结构化证据。
- 生成 `.md`、`.html`、`.pdf` 三种阅读形态。
- 生成正式压测关键失败分布图。
- 校验三份报告结论一致性。
- 阻断 `02_实际交付报告` 中的本机路径泄漏。
- 打包最终交付 zip。

默认输出目录按仓库所在位置推导；如需指定交付目录，可设置 `ORISTRAT_REPORT_DIR`。若系统无法自动找到中文字体，可设置 `ORISTRAT_CJK_FONT` 或 `ORISTRAT_CJK_FONT_BOLD` 指向本机字体文件。

macOS / Linux：

```bash
ORISTRAT_REPORT_DIR="<交付报告目录>" python3 skills/product-testing/scripts/generate_delivery_artifacts.py
```

Windows PowerShell：

```powershell
$env:ORISTRAT_REPORT_DIR="<交付报告目录>"
py -3 skills/product-testing/scripts/generate_delivery_artifacts.py
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
