# 02 测试执行与证据采集

## 目标

按已确认范围执行测试，并保留能支撑结论的可反查证据。

## 执行分层

| 层级 | 目标 | 默认证据 |
|---|---|---|
| 页面可用性 | 登录、导航、核心页面可打开 | 截图、DOM 摘要、操作日志 |
| 功能验证 | 关键只读/轻写入流程通过 | 用例结果、接口响应、截图 |
| 日志审计 | 操作可追溯 | 日志列表、搜索结果、统计卡片 |
| AI 创作 | 任务创建和素材记录可验证 | 创建结果 JSON、素材列表 |
| 大数据专项 | 临时造数、分页、搜索、统计、清理 | 造数/清理 JSON、列表截图 |
| 正式压测 | 严格档或约定档性能结果 | summary、progress、failure responses |

## 证据命名

证据文件优先放在交付目录下的相对路径：

```text
evidence/
  screenshots/
  playwright_logs/
  performance_results/
```

报告正文只写相对路径或文件名，不写本机绝对路径。

## 执行工具

| 工具 | 用途 | 产物 |
|---|---|---|
| `playwright` | 页面操作、截图、DOM、trace | `screenshots/`、`playwright_logs/` |
| `formal_load.mjs` | 正式压测 | `formal_load_summary.json` 等 |
| `big_data_special.mjs` | 大数据专项 | `big_data_special.json` |
| `create_generation_tasks.mjs` | AI 创作任务创建 | `generation_task_creation.json` |
| `frontend_endpoint_probe.mjs` | 前端接口探测 | endpoint probe 结果 |

## 输出

- 结构化证据目录。
- 可复核的失败响应样本。
- 大数据造数与清理记录。
- 压测结果和关键失败分布图。

## 进入下一步条件

- 证据文件存在且能打开。
- 失败请求有响应/异常摘要。
- 造数任务有清理结果。
- 关键截图没有明显空白或错误页面。
