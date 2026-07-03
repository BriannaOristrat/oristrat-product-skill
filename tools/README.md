# Tools

自动化工具目录。

当前可执行脚本仍保留在 `tools/` 根目录，以兼容现有运行方式：

| 脚本 | 职责 |
|---|---|
| `generate_delivery_artifacts.py` | 生成三份报告和交付 zip，校验报告一致性和路径安全 |
| `formal_load.mjs` | 正式性能压测 |
| `big_data_special.mjs` | 大数据量专项 |
| `create_generation_tasks.mjs` | AI 创作任务创建 |
| `frontend_endpoint_probe.mjs` | 前端接口探测 |
| `sensitive_info_scan.py` | 提交 GitHub 前扫描账号、密码、token、key、私钥等敏感信息 |

## 目标结构

后续脚本可以逐步迁移到：

```text
tools/
  generate_delivery_artifacts.py
  formal_load.mjs
  big_data_special.mjs
  create_generation_tasks.mjs
  frontend_endpoint_probe.mjs
  sensitive_info_scan.py
```

迁移前必须同步更新 `docs/workflows/03-report-generation.md` 和相关命令。
