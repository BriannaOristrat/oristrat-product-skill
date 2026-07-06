# PDF / HTML 安全门禁

## 目标

防止正式阅读版报告泄漏本机路径、临时目录、浏览器默认页眉页脚或内部调试痕迹。

## 禁止内容

正式 `.md/.html/.pdf` 中不得出现：

- `file://`
- `C:\`
- `C:/`
- `Users/`
- `Users\`
- 用户名路径
- `AppData`
- `Temp`
- 浏览器打印的 URL 页脚
- 调试命令、Prompt、临时脚本说明

## HTML 检查

```powershell
rg -n "file://|C:\\|C:/|Users/|Users\\|AppData|Temp" *.html *.md
```

期望：无命中，除非是在工作流文档中作为禁止项示例。

## 视觉配色检查

- [ ] 报告使用固定低饱和绿色系：标题 `#0B3D2E`、表头 `#C8E0D0`、卡片底色 `#F4FAF6`、强调色 `#2F6B4F`、边框 `#B7D6C3`。
- [ ] HTML、PDF 和正式压测关键失败分布图的颜色一致，不使用亮绿、荧光绿或大面积高饱和绿色。
- [ ] 表头、卡片、正文文字对比度清晰，截图缩放后仍可阅读。
- [ ] `02_实际交付报告` 中的压测图内容来自实际压测证据，不得复用示例数值。

## PDF 检查

1. 渲染第一页：

```powershell
pdftoppm -f 1 -l 1 -png -r 144 02_实际交付报告.pdf page
```

2. 打开 PNG 预览：

- 无浏览器默认日期。
- 无标题栏 URL。
- 无底部 `file:///C:/...`。
- 无页码以浏览器格式显示。

3. 文本层扫描：

```powershell
python -c "from pypdf import PdfReader; import re; text='\n'.join((p.extract_text() or '') for p in PdfReader('02_实际交付报告.pdf').pages); print(bool(re.search(r'(?i)(file://|[a-z]:[\\/]|users/|users\\\\|appdata|temp)', text)))"
```

期望：`False`。

## 生成规则

- 优先使用 ReportLab 或 `page.pdf(displayHeaderFooter=False)`。
- 如果使用浏览器打印 PDF，必须关闭 header/footer。
- 图片路径进入报告正文前必须转换为相对路径。
- 生成脚本必须在写出 `02_实际交付报告` 前阻断本机路径。
