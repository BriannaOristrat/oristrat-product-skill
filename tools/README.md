# Tools

仓库级通用工具目录。这里只放多个 Skill 共用的工具；某个 Skill 专用脚本应放在对应 Skill 的 `scripts/` 目录。

| 脚本 | 职责 |
|---|---|
| `sensitive_info_scan.py` | 提交 GitHub 前扫描账号、密码、token、key、私钥、cookie、session、本机用户路径等敏感信息 |

## Skill 专用脚本

| Skill | 脚本目录 |
|---|---|
| `product-testing` | [../skills/product-testing/scripts/](../skills/product-testing/scripts/) |

提交前统一执行：

```powershell
python tools/sensitive_info_scan.py
```
