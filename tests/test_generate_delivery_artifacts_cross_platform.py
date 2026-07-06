from __future__ import annotations

import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills" / "product-testing" / "scripts" / "generate_delivery_artifacts.py"


class _Styles(dict):
    def add(self, style):
        self[style.name] = style


class _ParagraphStyle:
    def __init__(self, name, parent=None, **kwargs):
        self.name = name
        self.parent = parent
        self.kwargs = kwargs


class _Paragraph:
    def __init__(self, text, style):
        self.text = text
        self.style = style


class _Table:
    def __init__(self, data, colWidths=None, repeatRows=0):
        self.data = data
        self.colWidths = colWidths
        self.repeatRows = repeatRows
        self.style = None

    def setStyle(self, style):
        self.style = style


class _TableStyle:
    def __init__(self, commands):
        self.commands = commands


def _install_dependency_stubs():
    pil = types.ModuleType("PIL")
    pil_image = types.ModuleType("PIL.Image")
    pil_image_draw = types.ModuleType("PIL.ImageDraw")
    pil_image_font = types.ModuleType("PIL.ImageFont")
    pil_image_font.load_default = lambda: "default-font"
    pil_image_font.truetype = lambda path, size: f"font:{path}:{size}"

    reportlab = types.ModuleType("reportlab")
    reportlab_lib = types.ModuleType("reportlab.lib")
    colors = types.ModuleType("reportlab.lib.colors")
    colors.HexColor = lambda value: value
    colors.white = "white"

    enums = types.ModuleType("reportlab.lib.enums")
    enums.TA_CENTER = 1
    pagesizes = types.ModuleType("reportlab.lib.pagesizes")
    pagesizes.A4 = (595, 842)
    pagesizes.landscape = lambda size: (size[1], size[0])
    styles = types.ModuleType("reportlab.lib.styles")

    def get_sample_style_sheet():
        return _Styles(
            {
                "Title": _ParagraphStyle("Title"),
                "Heading2": _ParagraphStyle("Heading2"),
                "Heading3": _ParagraphStyle("Heading3"),
                "BodyText": _ParagraphStyle("BodyText"),
            }
        )

    styles.ParagraphStyle = _ParagraphStyle
    styles.getSampleStyleSheet = get_sample_style_sheet
    units = types.ModuleType("reportlab.lib.units")
    units.mm = 1

    pdfbase = types.ModuleType("reportlab.pdfbase")
    pdfmetrics = types.ModuleType("reportlab.pdfbase.pdfmetrics")
    pdfmetrics.registerFont = lambda font: None
    ttfonts = types.ModuleType("reportlab.pdfbase.ttfonts")
    ttfonts.TTFont = lambda name, path: (name, path)

    platypus = types.ModuleType("reportlab.platypus")
    platypus.PageBreak = object
    platypus.Paragraph = _Paragraph
    platypus.SimpleDocTemplate = object
    platypus.Spacer = object
    platypus.Table = _Table
    platypus.TableStyle = _TableStyle
    platypus.Image = object

    modules = {
        "PIL": pil,
        "PIL.Image": pil_image,
        "PIL.ImageDraw": pil_image_draw,
        "PIL.ImageFont": pil_image_font,
        "reportlab": reportlab,
        "reportlab.lib": reportlab_lib,
        "reportlab.lib.colors": colors,
        "reportlab.lib.enums": enums,
        "reportlab.lib.pagesizes": pagesizes,
        "reportlab.lib.styles": styles,
        "reportlab.lib.units": units,
        "reportlab.pdfbase": pdfbase,
        "reportlab.pdfbase.pdfmetrics": pdfmetrics,
        "reportlab.pdfbase.ttfonts": ttfonts,
        "reportlab.platypus": platypus,
    }
    return patch.dict(sys.modules, modules)


def _load_script(env):
    module_name = "generate_delivery_artifacts_under_test"
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    with _install_dependency_stubs(), patch.dict(os.environ, env, clear=False):
        for key in ("ORISTRAT_REPORT_DIR", "ORISTRAT_REPORT_ROOT"):
            if key not in env:
                os.environ.pop(key, None)
        assert spec.loader is not None
        spec.loader.exec_module(module)
    return module


class GenerateDeliveryArtifactsCrossPlatformTest(unittest.TestCase):
    def test_default_report_dir_uses_archive_output_layout(self):
        module = _load_script({})

        self.assertEqual(
            module.REPORT_DIR,
            Path(r"D:\AAAA\资料归档\codex_files\00_入口\01_产物\输出\报告") / "04_交付报告",
        )

    def test_report_dir_can_be_overridden_with_environment_variable(self):
        custom_report_dir = REPO_ROOT / "tmp" / "cross-platform-report"
        module = _load_script({"ORISTRAT_REPORT_DIR": str(custom_report_dir)})

        self.assertEqual(module.REPORT_DIR, custom_report_dir)

    def test_report_root_legacy_environment_variable_is_supported(self):
        custom_report_root = REPO_ROOT / "tmp" / "legacy-report-root"
        module = _load_script({"ORISTRAT_REPORT_ROOT": str(custom_report_root)})

        self.assertEqual(
            module.REPORT_DIR,
            custom_report_root / "00_入口" / "01_产物" / "04_交付报告",
        )

    def test_pdf_table_uses_resolved_font_name_when_cjk_font_is_unavailable(self):
        module = _load_script({})

        with patch.object(module.Path, "exists", return_value=False):
            pdf_styles = module.setup_pdf_styles()
            table = module.table_for_pdf(["标题"], [["内容"]], pdf_styles)
        font_commands = [cmd for cmd in table.style.commands if cmd[0] == "FONTNAME"]

        self.assertEqual(font_commands, [("FONTNAME", (0, 0), (-1, -1), "Helvetica")])

    def test_pdf_styles_fall_back_when_existing_font_cannot_be_registered(self):
        module = _load_script({})

        with (
            patch.object(module.Path, "exists", return_value=True),
            patch.object(module, "TTFont", side_effect=RuntimeError("unsupported font")),
        ):
            pdf_styles = module.setup_pdf_styles()
            table = module.table_for_pdf(["标题"], [["内容"]], pdf_styles)
        font_commands = [cmd for cmd in table.style.commands if cmd[0] == "FONTNAME"]

        self.assertEqual(font_commands, [("FONTNAME", (0, 0), (-1, -1), "Helvetica")])


if __name__ == "__main__":
    unittest.main()
