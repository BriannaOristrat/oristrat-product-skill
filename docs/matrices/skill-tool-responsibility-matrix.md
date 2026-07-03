# Skill / 工具职责矩阵

## Skill 职责

| Skill | 使用时机 | 产物 | 不负责 |
|---|---|---|---|
| `product-manager` | 范围、目标、验收口径不清 | 需求澄清、验收标准 | 自动化执行 |
| `product-specs-writer` | 需要 PRD、用例、验收描述 | 规格和用例文本 | 页面操作 |
| `automation-test-engineer` | 需要自动化测试代码 | Playwright/Vitest/Cypress 测试 | 业务结论 |
| `playwright` | 页面实测、截图、DOM、trace | 截图、日志、交互证据 | 报告结构设计 |
| `data-analytics` | 需要分析压测、失败分布、趋势 | 指标分析、图表 | 页面验证 |
| `spreadsheets` | 测试用例表、缺陷表、验收清单 | `.xlsx` | PDF 渲染 |
| `pdf` | PDF 渲染、文本层扫描、视觉 QA | PNG 预览、PDF 检查 | 测试执行 |
| `obsidian-markdown` | 让仓库 Markdown 适配 Obsidian 直接阅读 | OB 可读链接、索引、frontmatter | GitHub 发布 |
| `github` | 仓库、PR、issue、CI 上下文 | GitHub 状态和 PR 操作 | 本地报告内容判断 |

## 工具职责

| 工具 | 路径 | 职责 |
|---|---|---|
| 报告生成器 | `tools/generate_delivery_artifacts.py` | 生成三份报告和 zip，校验结论一致性和路径安全 |
| 正式压测 | `tools/formal_load.mjs` | 运行严格/约定压测档，输出 summary/progress/failure responses |
| 大数据专项 | `tools/big_data_special.mjs` | 临时造数、列表/搜索/统计/组织树验证、清理 |
| AI 创作造证 | `tools/create_generation_tasks.mjs` | 创建图生图/图生视频任务并记录结果 |
| 前端接口探测 | `tools/frontend_endpoint_probe.mjs` | 反查前端调用接口和路由 |
| 敏感信息扫描 | `tools/sensitive_info_scan.py` | GitHub 提交前扫描账号、密码、token、key、私钥、cookie、session |
| Poppler | `pdftoppm` | PDF 转 PNG 视觉检查 |
| pypdf | Python package | PDF 文本层扫描 |

## 使用顺序

1. 用产品/规格 Skill 明确范围。
2. 用 Playwright 和专项工具采集证据。
3. 用报告生成器生成交付报告。
4. 用 PDF/HTML 门禁检查阅读版。
5. 在 Obsidian 中直接打开 GitHub 仓库文档。
6. 用敏感信息扫描和 GitHub 提交安全门禁检查提交内容。
7. 用 GitHub 管理仓库版本、PR 和发布。
