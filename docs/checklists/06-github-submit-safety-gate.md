# GitHub 提交安全门禁

## 目标

在 `git add`、`git commit`、`git push` 或创建 PR 前，阻断账号、密码、token、API key、私钥、cookie、session、storage state 等敏感信息进入 GitHub。

## 必跑命令

macOS / Linux：

```bash
python3 tools/sensitive_info_scan.py
git status --short
git diff --check
```

Windows PowerShell：

```powershell
py -3 tools/sensitive_info_scan.py
git status --short
git diff --check
```

如果已经 staged，还必须执行：

```powershell
git diff --cached --check
git diff --cached --name-only
```

## 强检查项

- [ ] `python3 tools/sensitive_info_scan.py` 或 `py -3 tools/sensitive_info_scan.py` 通过。
- [ ] `git status --short` 中没有 `.env`、私钥、证书、storage state、cookie、session、账号导出文件。
- [ ] `git diff --check` 无空白错误。
- [ ] `git diff` 或 `git diff --cached` 中没有账号、密码、token、API key、租户码、手机号、cookie、session。
- [ ] `.gitignore` 已覆盖本地凭证、缓存、执行产物和浏览器登录态文件。
- [ ] 如果发现真实凭证曾进入文件，先移除并轮换凭证，再继续提交。

## 通过标准

任一强检查项未通过，不允许提交、不允许 push、不允许创建 PR。
