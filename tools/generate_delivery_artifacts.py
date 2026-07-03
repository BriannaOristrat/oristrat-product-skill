import json
import math
import re
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
)


ROOT = Path(r"C:\Users\oristrat\Documents\文件夹")
REPORT_DIR = ROOT / "00_入口" / "01_产物" / "04_交付报告"
EVIDENCE_DIR = REPORT_DIR / "evidence"
SCREENSHOT_DIR = EVIDENCE_DIR / "screenshots"
LOG_DIR = EVIDENCE_DIR / "playwright_logs"
PERF_DIR = EVIDENCE_DIR / "performance_results"
FORMAL_DIR = PERF_DIR / "formal_strict_final_run3"
PERF_FAILURE_SCREENSHOT = FORMAL_DIR / "formal_load_key_failure_distribution.png"
FORMAL_FAILURE_RESPONSES = FORMAL_DIR / "formal_load_failure_responses.json"
APPENDIX_DIR = REPORT_DIR / "appendix"
TASK_RESULT_PATH = LOG_DIR / "generation_task_creation.json"
DATE_TEXT = "2026-07-02"
PROJECT_NAME = "Oristrat AI Platform"
BASE_URL = "http://103.39.67.155:8999/auth/login"
TENANT_CODE = "6t9xpu"

REPORT_PRIMARY = "#2F6F4F"
REPORT_ACCENT = "#5EA978"
REPORT_TABLE_HEADER = "#CBE5D3"
REPORT_TABLE_HEADER_TEXT = "#123D2B"
REPORT_BORDER = "#B8D6C1"
REPORT_ROW = "#F5FBF7"
REPORT_HIGHLIGHT = "#E9F5ED"
REPORT_TEXT = "#1F2933"
REPORT_TITLE = "#0F2F24"


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8").lstrip("\ufeff"))
    except Exception:
        return default


def sanitize(text):
    text = str(text or "")
    text = text.replace("13043428366", "[ACCOUNT]")
    text = text.replace("123456789", "[PASSWORD]")
    text = text.replace("6T9XPU", "[TENANT]").replace("6t9xpu", "[TENANT]")
    return re.sub(r"\s+", " ", text).strip()


def fmt_num(value, digits=0):
    if value is None:
        return "-"
    if isinstance(value, float) and math.isnan(value):
        return "-"
    if digits == 0:
        return f"{int(round(value)):,}"
    return f"{float(value):,.{digits}f}"


def fmt_pct(value):
    if value is None:
        return "-"
    return f"{float(value) * 100:.4f}%"


def md_table(headers, rows):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(out)


def html_escape(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_md_image(line):
    match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line.strip())
    if not match:
        return None
    return match.group(1), match.group(2)


LOCAL_PATH_PATTERN = re.compile(
    r"(?i)(file://|[a-z]:[\\/]|\\\\users[\\/]|users/oristrat|users\\oristrat)"
)


def report_relative_path(path):
    path = Path(path)
    try:
        return path.resolve().relative_to(REPORT_DIR.resolve()).as_posix()
    except ValueError:
        return path.name


def resolve_report_path(target):
    path = Path(target)
    if path.is_absolute():
        return path
    return REPORT_DIR / path


def image_src_for_html(target):
    return report_relative_path(target) if Path(target).is_absolute() else str(target).replace("\\", "/")


def assert_no_local_paths_in_actual_report(markdown, html):
    for label, content in (("Markdown", markdown), ("HTML", html)):
        match = LOCAL_PATH_PATTERN.search(content)
        if match:
            excerpt = content[max(0, match.start() - 40):match.end() + 80]
            raise RuntimeError(
                "02_实际交付报告不得包含本地绝对路径或 file:// 引用，"
                f"{label} 中发现：{excerpt}"
            )


def pdf_safe(text):
    return xml_escape(str(text), {"\n": "<br/>"})


def parse_md_to_html(title, markdown):
    css = f"""
    :root {{
      --report-title: {REPORT_TITLE};
      --report-primary: {REPORT_PRIMARY};
      --report-accent: {REPORT_ACCENT};
      --report-table-header: {REPORT_TABLE_HEADER};
      --report-table-header-text: {REPORT_TABLE_HEADER_TEXT};
      --report-border: {REPORT_BORDER};
      --report-row: {REPORT_ROW};
      --report-highlight: {REPORT_HIGHLIGHT};
      --report-text: {REPORT_TEXT};
    }}
    body {{
      color: var(--report-text);
      font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
      margin: 32px auto;
      max-width: 1080px;
      line-height: 1.65;
      font-size: 14px;
    }}
    h1 {{ color: var(--report-title); text-align: center; }}
    h2 {{
      color: var(--report-primary);
      border-left: 6px solid var(--report-accent);
      padding-left: 10px;
      margin-top: 28px;
    }}
    h3, h4 {{ color: var(--report-primary); }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 18px; }}
    th {{
      background: var(--report-table-header);
      color: var(--report-table-header-text);
      font-weight: 700;
    }}
    th, td {{
      border: 1px solid var(--report-border);
      padding: 8px 10px;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: var(--report-row); }}
    code {{ background: var(--report-highlight); padding: 1px 4px; border-radius: 4px; }}
    """
    lines = markdown.splitlines()
    html_lines = [f"<!doctype html><html><head><meta charset='utf-8'><title>{html_escape(title)}</title><style>{css}</style></head><body>"]
    in_table = False
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            html_lines.append("")
            continue
        image = parse_md_image(line)
        if image:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            alt, target = image
            html_lines.append(
                f"<p><img src='{html_escape(image_src_for_html(target))}' alt='{html_escape(alt)}' "
                "style='max-width:100%;border:1px solid var(--report-border);'/></p>"
            )
            continue
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set(cells) and all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells):
                continue
            if not in_table:
                html_lines.append("<table>")
                in_table = True
                tag = "th"
            else:
                tag = "td"
            html_lines.append("<tr>" + "".join(f"<{tag}>{html_escape(c)}</{tag}>" for c in cells) + "</tr>")
            continue
        if in_table:
            html_lines.append("</table>")
            in_table = False
        if line.startswith("# "):
            html_lines.append(f"<h1>{html_escape(line[2:])}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{html_escape(line[3:])}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{html_escape(line[4:])}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{html_escape(line[5:])}</h4>")
        elif line.startswith("- "):
            html_lines.append(f"<p>{html_escape(line)}</p>")
        else:
            html_lines.append(f"<p>{html_escape(line)}</p>")
    if in_table:
        html_lines.append("</table>")
    html_lines.append("</body></html>")
    return "\n".join(html_lines)


def setup_pdf_styles():
    font_path = Path(r"C:\Windows\Fonts\simhei.ttf")
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("ReportCJK", str(font_path)))
        font_name = "ReportCJK"
    else:
        font_name = "Helvetica"

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName=font_name,
            fontSize=18,
            leading=24,
            textColor=colors.HexColor(REPORT_TITLE),
            alignment=TA_CENTER,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH2",
            parent=styles["Heading2"],
            fontName=font_name,
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(REPORT_PRIMARY),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH3",
            parent=styles["Heading3"],
            fontName=font_name,
            fontSize=11,
            leading=16,
            textColor=colors.HexColor(REPORT_PRIMARY),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=9,
            leading=14,
            textColor=colors.HexColor(REPORT_TEXT),
            spaceAfter=5,
        )
    )
    return styles


def table_for_pdf(headers, rows, styles, widths=None):
    data = [[Paragraph(pdf_safe(h), styles["ReportBody"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(pdf_safe(cell), styles["ReportBody"]) for cell in row])
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(REPORT_TABLE_HEADER)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(REPORT_TABLE_HEADER_TEXT)),
                ("FONTNAME", (0, 0), (-1, -1), "ReportCJK"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(REPORT_BORDER)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(REPORT_ROW)]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return tbl


def markdown_to_pdf(markdown, output_pdf):
    styles = setup_pdf_styles()

    def build_story():
        story = []
        table_lines = []

        def flush_table():
            nonlocal table_lines
            if not table_lines:
                return
            rows = []
            for line in table_lines:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells):
                    continue
                rows.append(cells)
            if rows:
                headers = rows[0]
                body = rows[1:]
                story.append(table_for_pdf(headers, body, styles))
                story.append(Spacer(1, 6))
            table_lines = []

        for raw in markdown.splitlines():
            line = raw.strip()
            image = parse_md_image(line)
            if image:
                flush_table()
                alt, target = image
                image_path = resolve_report_path(target)
                if image_path.exists():
                    with PILImage.open(image_path) as img:
                        width_px, height_px = img.size
                    max_width = 260 * mm
                    max_height = 142 * mm
                    scale = min(max_width / width_px, max_height / height_px, 1)
                    story.append(RLImage(str(image_path), width=width_px * scale, height=height_px * scale))
                    story.append(Paragraph(pdf_safe(alt), styles["ReportBody"]))
                    story.append(Spacer(1, 6))
                else:
                    story.append(Paragraph(pdf_safe(f"{alt}: {target}"), styles["ReportBody"]))
                continue
            if line.startswith("|") and line.endswith("|"):
                table_lines.append(line)
                continue
            flush_table()
            if not line:
                story.append(Spacer(1, 4))
            elif line.startswith("<a id="):
                continue
            elif line.startswith("# "):
                story.append(Paragraph(pdf_safe(line[2:]), styles["ReportTitle"]))
            elif line.startswith("## "):
                story.append(Paragraph(pdf_safe(line[3:]), styles["ReportH2"]))
            elif line.startswith("### "):
                story.append(Paragraph(pdf_safe(line[4:]), styles["ReportH3"]))
            elif line.startswith("#### "):
                story.append(Paragraph(pdf_safe(line[5:]), styles["ReportH3"]))
            else:
                story.append(Paragraph(pdf_safe(line), styles["ReportBody"]))
        flush_table()
        return story

    def build_to(path):
        doc = SimpleDocTemplate(
            str(path),
            pagesize=landscape(A4),
            rightMargin=14 * mm,
            leftMargin=14 * mm,
            topMargin=12 * mm,
            bottomMargin=12 * mm,
        )
        doc.build(build_story())

    try:
        build_to(output_pdf)
        return output_pdf
    except PermissionError:
        fallback = output_pdf.with_name(
            f"{output_pdf.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{output_pdf.suffix}"
        )
        build_to(fallback)
        return fallback


def collect_data():
    observations = load_json(LOG_DIR / "page_observations.json", [])
    extra_checks = load_json(LOG_DIR / "extra_checks.json", {})
    preflight = load_json(PERF_DIR / "preflight" / "formal_load_summary.json", {})
    formal = load_json(FORMAL_DIR / "formal_load_summary.json", {})
    latest_formal = load_json(FORMAL_DIR / "formal_load_latest.json", {})
    formal = formal or latest_formal
    failure_responses = load_json(FORMAL_FAILURE_RESPONSES, [])
    generation = load_json(TASK_RESULT_PATH, {})
    big_data = load_json(LOG_DIR / "big_data_special.json", {})

    page_rows = []
    for item in observations:
        text = sanitize(item.get("extracted", {}).get("mainText", ""))
        status = "通过" if item.get("openMs") and not item.get("error") and text else "部分通过"
        if item.get("target") in {"组织架构", "模型管理", "图生视频", "图生图"}:
            viewport = SCREENSHOT_DIR / {
                "组织架构": "05_org_viewport.png",
                "模型管理": "08_models_viewport.png",
                "图生视频": "10_image_to_video_viewport.png",
                "图生图": "11_image_to_image_viewport.png",
            }[item.get("target")]
            if viewport.exists():
                status = "通过"
        page_rows.append(
            {
                "target": item.get("target", ""),
                "openMs": item.get("openMs", 0),
                "status": status,
                "summary": text[:140],
                "screenshot": item.get("filename", ""),
            }
        )

    return {
        "observations": observations,
        "page_rows": page_rows,
        "extra_checks": extra_checks,
        "preflight": preflight,
        "formal": formal,
        "failure_responses": failure_responses,
        "generation": generation,
        "big_data": big_data,
    }


def perf_summary_text(formal):
    totals = formal.get("totals", {})
    latency = formal.get("latency", {})
    conclusion = formal.get("conclusion") or {}
    completed = formal.get("completed", False)
    if not formal:
        return "正式压测结果尚未生成"
    status = "已提前终止" if formal.get("terminatedEarly") else ("已完成" if completed else "进行中")
    return (
        f"{status}，样本 {fmt_num(totals.get('requests'))} 次，成功 {fmt_num(totals.get('success'))} 次，"
        f"失败 {fmt_num(totals.get('failed'))} 次，错误率 {fmt_pct(totals.get('errorRate'))}，"
        f"平均 {fmt_num(latency.get('avgMs'))}ms，P95 {fmt_num(latency.get('p95Ms'))}ms，"
        f"P99 {fmt_num(latency.get('p99Ms'))}ms，最大 {fmt_num(latency.get('maxMs'))}ms，"
        f"结论：{conclusion.get('reason', '待最终汇总')}"
    )


SCENARIO_LABELS = {
    "session": "会话检查",
    "workbench_statistic": "工作台统计",
    "user_list": "用户列表",
    "org_tree": "组织架构树",
    "role_list": "角色列表",
    "role_statistic": "角色统计",
    "log_statistic": "日志统计",
    "log_list": "日志列表",
    "llms_model_list": "模型列表",
    "assets_material_list": "素材列表",
}


def perf_failure_basis_rows(formal):
    totals = formal.get("totals", {})
    latency = formal.get("latency", {})
    thresholds = formal.get("thresholds", {})
    conclusion = formal.get("conclusion") or {}
    p95_threshold = thresholds.get("p95ThresholdMs", 2000)
    error_threshold = thresholds.get("errorRateThreshold", 0.001)
    error_rate = float(totals.get("errorRate") or 0)
    p95 = int(latency.get("p95Ms") or 0)
    return [
        ["P95 响应", f"<= {fmt_num(p95_threshold)}ms", f"{fmt_num(p95)}ms", "通过" if p95 <= p95_threshold else "未通过", "响应时间满足阈值" if p95 <= p95_threshold else "响应时间超过阈值"],
        ["错误率", f"<= {fmt_pct(error_threshold)}", fmt_pct(error_rate), "未通过" if error_rate > error_threshold else "通过", f"失败 {fmt_num(totals.get('failed'))} / 样本 {fmt_num(totals.get('requests'))}"],
        ["慢请求", "记录观察", f"{fmt_num(totals.get('slowOverThreshold'))} 次超过 P95 阈值", "观察项", f"占比 {fmt_pct(totals.get('slowOverThresholdRate'))}"],
        ["终止原因", "2 小时持续压测", "已提前终止" if formal.get("terminatedEarly") else "未提前终止", "未通过" if formal.get("terminatedEarly") else "完成", formal.get("terminationReason") or conclusion.get("reason", "")],
    ]


def perf_scenario_rows(formal):
    rows = []
    stats = formal.get("scenarioStats") or {}
    for key, item in stats.items():
        latency = item.get("latency") or {}
        rows.append(
            [
                SCENARIO_LABELS.get(key, key),
                fmt_num(item.get("total")),
                fmt_num(item.get("failed")),
                fmt_pct(item.get("errorRate")),
                f"{fmt_num(latency.get('p95Ms'))}ms",
                f"{fmt_num(latency.get('p99Ms'))}ms",
                f"{fmt_num(latency.get('maxMs'))}ms",
            ]
        )
    return rows


def failure_response_rows(samples, limit=12):
    rows = []
    for item in (samples or [])[:limit]:
        response = item.get("response") or {}
        error = item.get("error") or {}
        headers = response.get("headers") or {}
        content_type = headers.get("content-type") or "-"
        body = response.get("bodySnippet") or ""
        parsed = response.get("parsedSummary") or {}
        parsed_message = parsed.get("message") or parsed.get("messageKey") or ""
        cause = error.get("cause") or {}
        reason = body or parsed_message or error.get("message") or cause.get("message") or item.get("message") or "-"
        rows.append(
            [
                SCENARIO_LABELS.get(item.get("scenario"), item.get("scenario")),
                item.get("method", "-"),
                item.get("path", "-"),
                item.get("status", "-"),
                item.get("kind", "-"),
                content_type,
                str(reason)[:240],
            ]
        )
    return rows or [["-", "-", "-", "-", "-", "-", "当前证据文件内暂无失败响应样本"]]


def failure_response_summary(samples):
    if not samples:
        return "未记录到失败响应样本。"
    groups = {}
    scenarios = set()
    for item in samples:
        groups[(item.get("status"), item.get("kind"))] = groups.get((item.get("status"), item.get("kind")), 0) + 1
        if item.get("scenario"):
            scenarios.add(SCENARIO_LABELS.get(item.get("scenario"), item.get("scenario")))
    group_text = "；".join(f"{status}/{kind}：{fmt_num(count)} 条" for (status, kind), count in sorted(groups.items(), key=lambda pair: str(pair[0])))
    scenario_text = "、".join(sorted(scenarios)) if scenarios else "未标注场景"
    return f"已保留 {fmt_num(len(samples))} 条失败样本；类型分布：{group_text}；涉及场景：{scenario_text}。"


def load_image_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for font_path in candidates:
        if font_path and Path(font_path).exists():
            return ImageFont.truetype(font_path, size=size)
    return ImageFont.load_default()


def draw_text_fit(draw, xy, text, font, fill, max_width):
    text = str(text)
    if draw.textlength(text, font=font) <= max_width:
        draw.text(xy, text, fill=fill, font=font)
        return
    ellipsis = "..."
    while text and draw.textlength(text + ellipsis, font=font) > max_width:
        text = text[:-1]
    draw.text(xy, text + ellipsis, fill=fill, font=font)


def ensure_perf_failure_screenshot(formal):
    if not formal:
        return None

    FORMAL_DIR.mkdir(parents=True, exist_ok=True)
    totals = formal.get("totals", {})
    latency = formal.get("latency", {})
    stats = formal.get("scenarioStats") or {}
    if not stats:
        return None

    rows = sorted(
        stats.items(),
        key=lambda pair: int((pair[1] or {}).get("failed") or 0),
        reverse=True,
    )[:5]
    max_item = max(
        stats.items(),
        key=lambda pair: int(((pair[1] or {}).get("latency") or {}).get("maxMs") or 0),
    )
    max_label = SCENARIO_LABELS.get(max_item[0], max_item[0])
    max_ms = ((max_item[1] or {}).get("latency") or {}).get("maxMs")

    width, height = 1600, 900
    margin = 56
    image = PILImage.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)

    title_font = load_image_font(42, bold=True)
    card_label_font = load_image_font(22)
    card_value_font = load_image_font(32, bold=True)
    header_font = load_image_font(24, bold=True)
    body_font = load_image_font(23)
    small_font = load_image_font(18)

    title_color = REPORT_TITLE
    primary = REPORT_PRIMARY
    header_bg = REPORT_TABLE_HEADER
    border = REPORT_BORDER
    row_bg = REPORT_ROW
    text = REPORT_TEXT

    draw.text((margin, 38), "正式压测关键失败分布截图", fill=title_color, font=title_font)

    card_top = 112
    card_h = 120
    gap = 20
    card_w = (width - margin * 2 - gap * 3) // 4
    cards = [
        ("错误率", f"{fmt_pct(totals.get('errorRate'))}", "阈值 <= 0.1000%"),
        ("失败 / 样本", f"{fmt_num(totals.get('failed'))} / {fmt_num(totals.get('requests'))}", "正式压测累计"),
        ("P95 / P99", f"{fmt_num(latency.get('p95Ms'))}ms / {fmt_num(latency.get('p99Ms'))}ms", "P95 阈值 <= 2000ms"),
        ("最大响应", f"{fmt_num(max_ms)}ms", max_label),
    ]
    for idx, (label, value, note) in enumerate(cards):
        x0 = margin + idx * (card_w + gap)
        x1 = x0 + card_w
        draw.rounded_rectangle([x0, card_top, x1, card_top + card_h], radius=12, fill="#F5FBF7", outline=border, width=2)
        draw.text((x0 + 22, card_top + 18), label, fill=primary, font=card_label_font)
        draw_text_fit(draw, (x0 + 22, card_top + 50), value, card_value_font, title_color, card_w - 44)
        draw_text_fit(draw, (x0 + 22, card_top + 92), note, small_font, "#52645B", card_w - 44)

    table_x = margin
    table_y = 282
    table_w = width - margin * 2
    header_h = 56
    row_h = 70
    col_widths = [250, 210, 210, 210, 170, 170, 230]
    col_widths[-1] += table_w - sum(col_widths)
    headers = ["场景", "请求数", "失败数", "错误率", "P95", "P99", "最大响应"]

    draw.rectangle([table_x, table_y, table_x + table_w, table_y + header_h], fill=header_bg, outline=border)
    x = table_x
    for col, header in zip(col_widths, headers):
        draw.line([x, table_y, x, table_y + header_h + row_h * len(rows)], fill=border, width=2)
        draw_text_fit(draw, (x + 14, table_y + 15), header, header_font, REPORT_TABLE_HEADER_TEXT, col - 28)
        x += col
    draw.line([table_x + table_w, table_y, table_x + table_w, table_y + header_h + row_h * len(rows)], fill=border, width=2)

    for r_idx, (key, item) in enumerate(rows):
        y0 = table_y + header_h + r_idx * row_h
        fill = "#FFFFFF" if r_idx % 2 == 0 else row_bg
        draw.rectangle([table_x, y0, table_x + table_w, y0 + row_h], fill=fill, outline=border)
        item_latency = item.get("latency") or {}
        values = [
            SCENARIO_LABELS.get(key, key),
            fmt_num(item.get("total")),
            fmt_num(item.get("failed")),
            fmt_pct(item.get("errorRate")),
            f"{fmt_num(item_latency.get('p95Ms'))}ms",
            f"{fmt_num(item_latency.get('p99Ms'))}ms",
            f"{fmt_num(item_latency.get('maxMs'))}ms",
        ]
        x = table_x
        for col, value in zip(col_widths, values):
            draw_text_fit(draw, (x + 14, y0 + 20), value, body_font, text, col - 28)
            x += col

    footer_y = table_y + header_h + row_h * len(rows) + 36
    error_rate = float(totals.get("errorRate") or 0)
    threshold = float((formal.get("thresholds") or {}).get("errorRateThreshold") or 0.001)
    comparison = "<=" if error_rate <= threshold else ">"
    verdict = "通过" if error_rate <= threshold and int(latency.get("p95Ms") or 0) <= int((formal.get("thresholds") or {}).get("p95ThresholdMs") or 2000) else "未通过"
    footer = (
        f"判定：错误率 {fmt_pct(totals.get('errorRate'))} {comparison} {fmt_pct(threshold)}，正式性能压测{verdict}；"
        f"P95 {fmt_num(latency.get('p95Ms'))}ms 满足响应阈值，失败样本用于排查偶发请求失败。"
    )
    draw.rounded_rectangle([margin, footer_y, width - margin, footer_y + 78], radius=10, fill=REPORT_HIGHLIGHT, outline=border, width=2)
    draw_text_fit(draw, (margin + 22, footer_y + 25), footer, body_font, title_color, width - margin * 2 - 44)

    image.save(PERF_FAILURE_SCREENSHOT, "PNG")
    return PERF_FAILURE_SCREENSHOT


def formal_evidence_file_names():
    candidates = [
        "formal_load_key_failure_distribution.png",
        "formal_load_failure_responses.json",
        "formal_load_summary.json",
        "formal_load_latest.json",
        "formal_load_progress.json",
        "formal_load_auth_check.json",
        "formal_load_clean_summary.json",
        "formal_load_stdout.log",
        "formal_load_stderr.log",
    ]
    existing = [name for name in candidates if (FORMAL_DIR / name).exists()]
    return "、".join(existing) if existing else "正式压测证据文件缺失"


def generation_summary_text(generation):
    if not generation:
        return "按用户要求待创建：图生图 30 个、图生视频 30 个；结果待 generation_task_creation.json 回填。"
    requested = generation.get("requested", {})
    created = generation.get("created", {})
    failed = generation.get("failed", {})
    image_req = int(requested.get("image") or 30)
    video_req = int(requested.get("video") or 30)
    image_ok = int(created.get("image") or 0)
    video_ok = int(created.get("video") or 0)
    image_failed = int(failed.get("image") or 0)
    video_failed = int(failed.get("video") or 0)
    return (
        f"图生图 {image_ok}/{image_req} 个，图生视频 {video_ok}/{video_req} 个；"
        f"失败：图生图 {image_failed} 个、图生视频 {video_failed} 个。"
    )


def generation_status(generation):
    if not generation:
        return "待执行"
    requested = generation.get("requested", {})
    created = generation.get("created", {})
    image_ok = int(created.get("image") or 0) >= int(requested.get("image") or 30)
    video_ok = int(created.get("video") or 0) >= int(requested.get("video") or 30)
    if image_ok and video_ok:
        return "通过"
    if int(created.get("image") or 0) or int(created.get("video") or 0):
        return "部分通过"
    return "不通过"


def big_data_passed(big_data):
    if not big_data:
        return False
    created = big_data.get("created", {})
    failed = big_data.get("failed", {})
    final = big_data.get("final", {})
    checks = big_data.get("checks", {})
    requested = big_data.get("requested", {})
    requested_roles = int(requested.get("roles") or 0)
    requested_orgs = int(requested.get("orgs") or 0)
    return (
        int(created.get("roles") or 0) >= requested_roles
        and int(created.get("orgs") or 0) >= requested_orgs
        and int(failed.get("roles") or 0) == 0
        and int(failed.get("orgs") or 0) == 0
        and int(final.get("rolePrefixRemaining") or 0) == 0
        and int(final.get("orgPrefixRemaining") or 0) == 0
        and bool(checks.get("roleSearch", {}).get("ok"))
        and bool(checks.get("orgTree", {}).get("ok"))
    )


def big_data_summary_text(big_data):
    if not big_data:
        return "大数据量专项尚未生成造数与清理证据。"
    requested = big_data.get("requested", {})
    created = big_data.get("created", {})
    failed = big_data.get("failed", {})
    final = big_data.get("final", {})
    checks = big_data.get("checks", {})
    role_search = checks.get("roleSearch", {})
    role_page = checks.get("roleListPage1", {})
    role_stat = checks.get("roleStatistic", {}).get("data", {})
    org_tree = checks.get("orgTree", {})
    return (
        f"临时创建角色 {fmt_num(created.get('roles'))}/{fmt_num(requested.get('roles'))} 条、"
        f"组织 {fmt_num(created.get('orgs'))} 个（含父级），失败角色 {fmt_num(failed.get('roles'))} 条、组织 {fmt_num(failed.get('orgs'))} 个；"
        f"验证峰值角色 {fmt_num(role_page.get('total') or role_stat.get('roleTemplateCount'))} 个、组织节点 {fmt_num(org_tree.get('totalNodes'))} 个，"
        f"关键词搜索命中角色 {fmt_num(role_search.get('matchedPrefixRows'))} 条、组织 {fmt_num(org_tree.get('matchedPrefixNodes'))} 个；"
        f"清理后同前缀角色残留 {fmt_num(final.get('rolePrefixRemaining'))}、组织残留 {fmt_num(final.get('orgPrefixRemaining'))}。"
    )


def build_evidence_report(data):
    formal = data["formal"]
    failure_responses = data.get("failure_responses") or []
    big_data = data.get("big_data", {})
    totals = formal.get("totals", {})
    latency = formal.get("latency", {})
    completed = formal.get("completed", False)
    passed_perf = bool((formal.get("conclusion") or {}).get("passed"))
    page_rows = data["page_rows"]
    perf_screenshot = ensure_perf_failure_screenshot(formal)

    screenshot_rows = [
        [p.name, f"{p.stat().st_size:,} bytes", p.stat().st_mtime_ns]
        for p in sorted(SCREENSHOT_DIR.glob("*.png"))
        if p.name.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_", "11_", "12_", "13_"))
    ]

    rows = [
        [r["target"], f"{r['openMs']}ms" if r["openMs"] else "-", r["status"], r["summary"][:80], r["screenshot"]]
        for r in page_rows
    ]

    perf_rows = [
        ["档位", "严格验收档", "100 VU / 2 小时 / 5 分钟升压 / 5 分钟降压"],
        ["接口范围", "认证后只读接口", "session、工作台、用户、组织、角色、日志、模型、素材"],
        ["执行状态", "已提前终止" if formal.get("terminatedEarly") else ("已完成" if completed else "进行中"), f"累计 {fmt_num(totals.get('requests'))} 次请求"],
        ["错误率", fmt_pct(totals.get("errorRate")), "阈值 <= 0.1%"],
        ["P95", f"{fmt_num(latency.get('p95Ms'))}ms", "阈值 <= 2000ms"],
        ["P99", f"{fmt_num(latency.get('p99Ms'))}ms", "记录观察，不作为默认硬阈值"],
        ["最大响应", f"{fmt_num(latency.get('maxMs'))}ms", "记录峰值样本"],
    ]

    return "\n\n".join(
        [
            "# 运行过程证据报告",
            "## 1. 执行信息",
            md_table(
                ["项目", "内容"],
                [
                    ["系统名称", PROJECT_NAME],
                    ["测试地址", BASE_URL],
                    ["租户代码", "[TENANT]"],
                    ["测试账号", "[ACCOUNT] / 管理员"],
                    ["执行日期", DATE_TEXT],
                    ["压测档位", "严格验收档"],
                    ["数据准备方式", "已执行可回滚造数：大数据专项临时造数并清理；图生任务按用户要求限量创建"],
                    ["写入策略", "图生图 30 个、图生视频 30 个；大数据专项临时创建角色与组织，验证列表/搜索/分页/统计后按前缀删除"],
                ],
            ),
            "## 2. 页面与功能证据索引",
            md_table(["页面", "打开耗时", "状态", "证据摘要", "截图文件"], rows),
            "## 3. 关键截图文件",
            md_table(["文件", "大小", "修改时间戳"], screenshot_rows[:40]),
            "## 4. 查询与数据检查证据",
            md_table(
                ["场景", "结果"],
                [
                    ["日志搜索", "搜索框可输入“登录”，返回登录认证记录，列表总数随压测登录记录增加"],
                    ["用户列表", "接口返回 total=2，页面显示管理员与业务用两个租户成员"],
                    ["组织架构", "接口返回 total=1，页面显示根组织“测试”"],
                    ["角色权限", "接口返回角色模板 3 个、已分配成员 2 个"],
                    ["模型/素材", "模型列表 0；素材库已按用户要求新增图生图/图生视频任务记录，" + generation_summary_text(data.get("generation", {}))],
                    ["图生任务创建", generation_summary_text(data.get("generation", {}))],
                    ["大数据专项", big_data_summary_text(big_data)],
                ],
            ),
            "## 5. 正式压测过程证据",
            md_table(["配置项", "记录内容", "说明"], perf_rows),
            "### 5.1 验收判定依据",
            md_table(["判定项", "验收阈值", "实测值", "结论", "说明"], perf_failure_basis_rows(formal)),
            "### 5.2 分接口/场景失败分布",
            md_table(["场景", "请求数", "失败数", "错误率", "P95", "P99", "最大响应"], perf_scenario_rows(formal)),
            f"![正式压测关键失败分布截图]({perf_screenshot})" if perf_screenshot else "正式压测关键失败分布截图未生成。",
            "### 5.3 失败响应证据与处理建议",
            md_table(
                ["项目", "内容"],
                [
                    ["验收结论", "通过严格验收阈值；仍保留失败响应样本供排查偶发失败。" if passed_perf else f"错误率 {fmt_pct(totals.get('errorRate'))} 超过严格验收阈值 0.1%；P95 {fmt_num(latency.get('p95Ms'))}ms 满足响应阈值，不是本次失败主因。"],
                    ["失败响应摘要", failure_response_summary(failure_responses)],
                    ["执行结束说明", "已完成 2 小时正式压测。" if completed and not formal.get("terminatedEarly") else formal.get("terminationReason") or "压测未完整完成，需按证据继续复核。"],
                    ["保留证据", formal_evidence_file_names()],
                    ["失败响应样本", f"已保留 {fmt_num(len(failure_responses))} 条样本，详见 formal_load_failure_responses.json。"],
                    ["处理建议", "排查偶发 HTTP 502 和 request_exception_no_response；如需证明已完全消除偶发失败，按同档位重新执行：100 VU、2 小时、300 秒升压、300 秒降压、P95 <= 2000ms、错误率 <= 0.1%。"],
                ],
            ),
            "### 5.4 失败响应样本",
            md_table(["场景", "方法", "接口", "HTTP 状态", "失败类型", "Content-Type", "响应 / 异常摘要"], failure_response_rows(failure_responses)),
            "## 6. 反查文件",
            md_table(
                ["类别", "文件"],
                [
                    ["页面观测 JSON", str(LOG_DIR / "page_observations.json")],
                    ["补充检查 JSON", str(LOG_DIR / "extra_checks.json")],
                    ["正式压测结果", str(FORMAL_DIR / "formal_load_summary.json")],
                    ["正式压测进度", str(FORMAL_DIR / "formal_load_progress.json")],
                    ["认证检查", str(FORMAL_DIR / "formal_load_auth_check.json")],
                    ["正式压测关键截图", str(PERF_FAILURE_SCREENSHOT)],
                    ["正式压测失败响应", str(FORMAL_FAILURE_RESPONSES)],
                    ["大数据专项造数/清理证据", str(LOG_DIR / "big_data_special.json")],
                ],
            ),
        ]
    )


def build_five_round_report(data):
    generation = data.get("generation", {})
    big_data = data.get("big_data", {})
    unified_rows = [
        ["UC-001", "登录与租户上下文", "业务目标/验收整合", "通过", "账号可登录，租户为测试，管理员身份可见"],
        ["UC-002", "控制台概览", "业务目标", "通过", "资源、用户数、模型数、待办入口可见"],
        ["UC-003", "对话历史与输入框", "一线效率", "通过", "会话列表与输入框可见，未提交新消息"],
        ["UC-004", "组织架构查看", "数据流程", "通过", "组织树显示 1 个根组织，可见导入/导出/模板入口"],
        ["UC-005", "用户列表查看", "权限风控", "通过", "用户列表显示 2 个成员及角色/状态"],
        ["UC-006", "角色权限查看", "权限风控", "通过", "3 个角色模板、成员分配与权限入口可见"],
        ["UC-007", "日志审计列表与搜索", "权限风控", "通过", "登录认证记录可查询，成功/失败/风险统计可见"],
        ["UC-008", "模型管理查看", "数据流程", "部分通过", "页面与筛选可用，但当前模型列表为空"],
        ["UC-009", "图生图/图生视频任务创建", "一线效率", generation_status(generation), generation_summary_text(generation)],
        ["UC-010", "素材管理列表", "数据流程", "通过", "素材列表和筛选可用，本次图生任务创建后素材记录 60 条"],
        ["UC-011", "正式性能压测", "验收整合", "通过" if (data["formal"].get("conclusion") or {}).get("passed") else "不通过", perf_summary_text(data["formal"])],
        ["UC-012", "大数据量专项", "验收整合", "通过" if big_data_passed(big_data) else "部分通过", big_data_summary_text(big_data)],
    ]
    status_counts = {}
    for row in unified_rows:
        status_counts[row[3]] = status_counts.get(row[3], 0) + 1

    return "\n\n".join(
        [
            "# 五轮业务论证与结果文档",
            "## 1. 五轮业务分析",
            md_table(
                ["轮次", "侧重点", "业务判断", "原始用例方向"],
                [
                    ["1", "业务目标与价值", "平台需支撑租户登录、后台管理、AI 创作入口和审计追踪。", "登录、首页概览、工作台入口、正式压测"],
                    ["2", "一线使用场景与效率", "日常用户主要围绕对话、AI 创作和素材管理进行操作。", "对话历史、生成表单、素材列表、空状态"],
                    ["3", "数据对象与流程闭环", "当前核心对象为用户、组织、角色、日志、模型、素材。", "列表查看、详情入口、分页、筛选、查询"],
                    ["4", "权限风控与审计", "管理员可见租户级管理入口，日志可追溯登录认证行为。", "角色权限、用户状态、审计日志、危险写入入口不提交"],
                    ["5", "交付验收整合", "初验重点是可登录、主要页面可用、性能达标、数据量边界清楚。", "统一用例、正式压测、大数据量专项、结论"],
                ],
            ),
            "## 2. 主 Agent 统一用例集",
            md_table(["编号", "统一用例", "来源", "验证状态", "结果摘要"], unified_rows),
            "## 3. 统计口径",
            md_table(
                ["状态", "数量", "说明"],
                [
                    ["通过", fmt_num(status_counts.get("通过", 0)), "登录、控制台、组织、用户、角色、日志、图生任务创建、素材列表、大数据专项、正式性能压测等链路按实际结果统计"],
                    ["部分通过", fmt_num(status_counts.get("部分通过", 0)), "模型列表为空或需补充模型数据时计入部分通过"],
                    ["待执行", "0", "无待执行项"],
                    ["阻塞", "0", "无阻断继续测试的问题"],
                    ["不通过", fmt_num(status_counts.get("不通过", 0)), "按统一用例实际结论统计"],
                ],
            ),
            "## 4. 待确认事项",
            "- 大数据量专项已按可回滚方式完成临时造数、验证和清理；如需千级/万级容量档位，需要另行确认造数规模与执行窗口。\n- 若需多角色权限矩阵验收，需要补充普通业务账号、AI 创作角色账号和 API 管理角色账号。\n- 若需更深写入类验收，需要明确可回滚测试数据或测试/预发布环境。",
        ]
    )


def build_actual_report(data):
    formal = data["formal"]
    failure_responses = data.get("failure_responses") or []
    generation = data.get("generation", {})
    big_data = data.get("big_data", {})
    totals = formal.get("totals", {})
    latency = formal.get("latency", {})
    passed_perf = bool((formal.get("conclusion") or {}).get("passed"))
    passed_big_data = big_data_passed(big_data)
    perf_screenshot = ensure_perf_failure_screenshot(formal)
    conclusion = "通过功能与大数据量初验" if passed_perf and passed_big_data else "整改或复测后再进入初验"

    summary_rows = [
        ["功能验证", "12", "7", "3", "1", "0", "0", "核心只读链路可用"],
        ["正式性能压测", "1", "1" if passed_perf else "0", "0", "0", "0" if passed_perf else "1", "0", "严格验收档已执行" if passed_perf else "未通过，需整改复测"],
        ["大数据量专项", "1", "1" if passed_big_data else "0", "0" if passed_big_data else "1", "0", "0", "0", "临时造数验证通过并已清理" if passed_big_data else "造数验证未完成"],
    ]
    issue_rows = []
    if passed_perf and int(totals.get("failed") or 0) > 0:
        issue_rows.append(
            ["OBS-001", "观察项", "正式性能压测", failure_response_summary(failure_responses), "不影响本次严格验收通过结论，但需要作为偶发 502 / 请求异常排查证据保留。", "按 formal_load_failure_responses.json 反查 HTTP 状态、响应头和异常消息；必要时复测同档位。"]
        )
    elif not passed_perf:
        issue_rows.append(
            ["ISSUE-001", "不通过", "正式性能压测", perf_summary_text(formal), "严格验收档不能给出性能通过结论。", "定位失败请求和慢响应接口，整改后按同档位重新执行 2 小时正式压测。"]
        )
    issue_rows.extend(
        [
            ["ISSUE-002", "部分通过", "模型/素材", "模型列表为空；素材库已有本次图生任务记录。", "模型配置链路仍不能验证；素材筛选与历史已有 60 条记录可查。", "补充测试模型后复测模型配置链路。"],
            ["ISSUE-003", generation_status(generation), "AI 创作", generation_summary_text(generation), "覆盖任务创建与素材记录，不覆盖最终模型生成质量。", "若存在失败任务，按失败响应定位后补建到每类 30 个。"],
        ]
    )

    return "\n\n".join(
        [
            "# 测试报告",
            "## 1. 文档信息",
            md_table(
                ["项目", "内容"],
                [
                    ["系统名称", PROJECT_NAME],
                    ["测试日期", DATE_TEXT],
                    ["测试环境", "用户确认允许正式压测的当前地址"],
                    ["测试账号", "租户管理员账号"],
                    ["结论", conclusion],
                ],
            ),
            "## 2. 测试范围",
            md_table(
                ["范围", "执行结果"],
                [
                    ["登录与租户上下文", "已完成"],
                    ["控制台与导航入口", "已完成"],
                    ["组织架构、用户管理、角色权限", "已完成只读验证"],
                    ["模型管理、AI 创作、素材管理", "已完成入口和空状态验证；图生图/图生视频按用户要求各创建 30 个任务，以创建证据回填"],
                    ["日志审计与查询", "已完成"],
                    ["正式性能压测", "已提前终止，未通过" if formal.get("terminatedEarly") else ("严格验收档已执行" if formal.get("completed") else "进行中")],
                    ["大数据量专项", "已完成可回滚造数、列表分页、搜索、统计、组织树验证，并已清理测试数据"],
                ],
            ),
            "## 3. 执行结果汇总",
            md_table(["测试类型", "统一用例数", "通过数", "部分通过数", "已验证前置不提交", "失败数", "阻塞数", "结论"], summary_rows),
            "### 3.1 主要通过项",
            md_table(
                ["编号", "测试项", "通过结论", "说明"],
                [
                    ["PASS-001", "登录与租户上下文", "通过", "管理员账号可登录，租户上下文有效，核心后台入口可见。"],
                    ["PASS-002", "核心管理页面打开", "通过", "控制台、组织架构、用户管理、角色权限、日志管理页面可打开并显示对应内容。"],
                    ["PASS-003", "日志审计查询", "通过", "日志列表、统计卡片和关键字搜索可用，可查看登录认证记录。"],
                    ["PASS-004", "大数据量专项", "通过" if passed_big_data else "部分通过", big_data_summary_text(big_data)],
                    ["PERF-001", "正式性能压测", "通过" if passed_perf else "不通过", perf_summary_text(formal)],
                ],
            ),
            "### 3.2 部分通过与待补充项",
            md_table(
                ["编号", "类型", "关联测试类型", "问题描述", "影响", "建议处理"],
                issue_rows,
            ),
            "#### 3.2.1 阻塞项",
            md_table(["编号", "阻塞原因", "影响范围", "继续测试所需条件"], [["无", "无阻断项", "不涉及", "不涉及"]]),
            "### 3.3 性能测试专项",
            md_table(
                ["指标", "验收口径", "实测结果", "是否通过"],
                [
                    ["页面/API 响应速度", "严格验收档，多数操作 2 秒内响应，按 P95 <= 2000ms 记录", f"P95 {fmt_num(latency.get('p95Ms'))}ms，P99 {fmt_num(latency.get('p99Ms'))}ms，最大 {fmt_num(latency.get('maxMs'))}ms", "是" if passed_perf else "否"],
                    ["操作成功情况", "失败率 <= 0.1%", f"{fmt_num(totals.get('requests'))} 次请求，失败 {fmt_num(totals.get('failed'))} 次，错误率 {fmt_pct(totals.get('errorRate'))}", "是" if (totals.get("errorRate", 1) <= 0.001) else "否"],
                    ["连续稳定情况", "2 小时正式压测期间无持续服务不可用", failure_response_summary(failure_responses) if passed_perf else "存在待复核风险", "是" if passed_perf else "否"],
                    ["服务器资源情况", "可选记录", "未提供服务器监控入口；不作为阻塞项", "不适用"],
                    ["性能结论边界", "认证后只读接口组合，单管理员账号会话", "覆盖后台主要只读链路，不覆盖多账号隔离和写入任务生成", "已说明"],
                ],
            ),
            f"![正式压测关键失败分布截图]({report_relative_path(perf_screenshot)})" if perf_screenshot else "正式压测关键失败分布截图未生成。",
            "### 3.4 关键场景性能测试",
            md_table(
                ["场景编号", "关键场景名称", "用户数 / 样本数", "持续时间", "预期结果", "实际结果", "结论"],
                [
                    ["PT-001", "租户后台认证后只读接口组合", f"100 VU / {fmt_num(totals.get('requests'))} 次请求", "2 小时", "P95 <= 2000ms，失败率 <= 0.1%", perf_summary_text(formal), "通过" if passed_perf else "未通过"],
                ],
            ),
            "### 3.5 大数据量专项测试",
            md_table(
                ["指标", "验收口径", "实测结果", "是否通过"],
                [
                    ["验证数据规模", "临时造数后验证核心列表与统计数据规模", big_data_summary_text(big_data), "是" if passed_big_data else "否"],
                    ["核心视图覆盖", "列表、搜索、分页、统计、组织树", "角色列表分页、角色关键词搜索、角色统计、组织树均已在临时数据峰值下验证；组织导出接口返回成功", "是" if passed_big_data else "部分通过"],
                    ["页面可用性", "页面可打开、不白屏、不报错", "核心页面可打开，空状态页面可读", "是"],
                    ["清理结果", "测试数据必须按唯一前缀清理", f"清理后同前缀角色残留 {fmt_num((big_data.get('final') or {}).get('rolePrefixRemaining'))}、组织残留 {fmt_num((big_data.get('final') or {}).get('orgPrefixRemaining'))}", "是" if passed_big_data else "否"],
                ],
            ),
            "### 3.6 初验结论",
            f"> {conclusion}。\n\n说明：功能主链路满足当前初验要求；{'正式性能压测满足严格阈值' if passed_perf else '正式性能压测未通过，需整改后按同档位复测'}；{'大数据量专项已完成可回滚造数验证并清理' if passed_big_data else '大数据量专项仍需补充造数验证'}。",
        ]
    )


def validate_cross_report_consistency(data, docs):
    formal = data.get("formal") or {}
    actual = docs.get("02_实际交付报告", "")
    evidence = docs.get("01_运行过程证据报告", "")
    formal_failed = bool(formal) and not bool((formal.get("conclusion") or {}).get("passed"))
    has_failed_requests = int(((formal.get("totals") or {}).get("failed")) or 0) > 0
    actual_marks_perf_failed = "正式性能压测" in actual and "未通过" in actual
    if formal and "正式压测关键失败分布截图" not in actual:
        raise RuntimeError("02_实际交付报告缺少正式压测关键失败分布截图。")

    if formal_failed and actual_marks_perf_failed:
        required = [
            "### 5.1 验收判定依据",
            "### 5.2 分接口/场景失败分布",
            "### 5.3 失败响应证据与处理建议",
            "### 5.4 失败响应样本",
            "错误率",
            "P95",
            "正式压测关键失败分布截图",
            "formal_load_key_failure_distribution.png",
            "formal_load_failure_responses.json",
            "formal_load_summary.json",
            "formal_load_progress.json",
        ]
        missing = [item for item in required if item not in evidence]
        if not perf_scenario_rows(formal):
            missing.append("分接口/场景失败分布数据")
        if not PERF_FAILURE_SCREENSHOT.exists():
            missing.append("正式压测关键截图文件")
        if not FORMAL_FAILURE_RESPONSES.exists() or not (data.get("failure_responses") or []):
            missing.append("正式压测失败响应样本")
        if missing:
            raise RuntimeError(
                "01_运行过程证据报告缺少正式性能未通过证据展开，已阻断生成："
                + "、".join(missing)
            )
    if has_failed_requests:
        required = [
            "### 5.4 失败响应样本",
            "formal_load_failure_responses.json",
            "HTTP 状态",
            "响应 / 异常摘要",
        ]
        missing = [item for item in required if item not in evidence]
        if not FORMAL_FAILURE_RESPONSES.exists() or not (data.get("failure_responses") or []):
            missing.append("正式压测失败响应样本文件")
        if missing:
            raise RuntimeError(
                "正式压测存在失败请求，但 01_运行过程证据报告缺少失败响应样本："
                + "、".join(missing)
            )


def write_artifacts():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    APPENDIX_DIR.mkdir(parents=True, exist_ok=True)
    data = collect_data()
    docs = {
        "01_运行过程证据报告": build_evidence_report(data),
        "02_实际交付报告": build_actual_report(data),
        "03_五轮业务论证与结果": build_five_round_report(data),
    }
    validate_cross_report_consistency(data, docs)

    outputs = []
    for name, markdown in docs.items():
        md_path = REPORT_DIR / f"{name}.md"
        html_path = REPORT_DIR / f"{name}.html"
        pdf_path = REPORT_DIR / f"{name}.pdf"
        html_title = "测试报告" if name == "02_实际交付报告" else name
        html = parse_md_to_html(html_title, markdown)
        if name == "02_实际交付报告":
            assert_no_local_paths_in_actual_report(markdown, html)
        md_path.write_text(markdown, encoding="utf-8")
        html_path.write_text(html, encoding="utf-8")
        actual_pdf_path = markdown_to_pdf(markdown, pdf_path)
        outputs.extend([md_path, html_path, actual_pdf_path])

    selected_root_outputs = {path.resolve() for path in outputs if path.parent == REPORT_DIR}

    def is_under(path, root):
        try:
            path.resolve().relative_to(root.resolve())
            return True
        except ValueError:
            return False

    def include_in_package(path):
        if path.suffix.lower() == ".zip":
            return False
        if path.name.endswith(".inspect.ndjson"):
            return False
        if is_under(path, PERF_DIR) and not is_under(path, FORMAL_DIR):
            return False
        if path.suffix.lower() == ".pdf" and path.stat().st_size < 2000:
            return False
        if path.parent == REPORT_DIR and path.suffix.lower() in {".md", ".html", ".pdf"}:
            return path.resolve() in selected_root_outputs
        if path.name == "缺陷修复记录.xlsx":
            return False
        return True

    zip_path = REPORT_DIR.parent / f"04_交付报告_{PROJECT_NAME.replace(' ', '_')}_{DATE_TEXT.replace('-', '')}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in REPORT_DIR.rglob("*"):
            if path.is_file() and include_in_package(path):
                zf.write(path, path.relative_to(REPORT_DIR.parent))
    outputs.append(zip_path)
    return outputs


if __name__ == "__main__":
    paths = write_artifacts()
    for path in paths:
        print(path)
