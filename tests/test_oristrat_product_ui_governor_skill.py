from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "oristrat-product-ui-governor"


class OristratProductUiGovernorSkillTest(unittest.TestCase):
    def test_required_skill_files_exist(self):
        required = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "references" / "surface-routing.md",
            SKILL_ROOT / "references" / "visual-quality-gates.md",
            SKILL_ROOT / "references" / "external-design-skill-bridge.md",
            SKILL_ROOT / "references" / "final-quality-gates.md",
        ]

        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())
                path.read_text(encoding="utf-8")

    def test_skill_frontmatter_has_only_supported_fields(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
        self.assertIsNotNone(match)

        fields = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual(fields, {"name", "description"})
        self.assertIn("name: oristrat-product-ui-governor", match.group(1))

    def test_formal_skill_contains_no_personal_absolute_path(self):
        forbidden = ("C:\\Users", "Documents\\Codex", "file://", "design-taste-frontend")

        for path in SKILL_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                with self.subTest(path=path, marker=marker):
                    self.assertNotIn(marker, text)

    def test_hallmark_source_and_runtime_boundary_are_recorded(self):
        bridge = (
            SKILL_ROOT / "references" / "external-design-skill-bridge.md"
        ).read_text(encoding="utf-8")

        self.assertIn("https://github.com/Nutlope/hallmark", bridge)
        self.assertIn("Version: `1.1.0`", bridge)
        self.assertIn("aeb42fb354ff4efa36ab475773a082315a3af2ce", bridge)
        self.assertIn("License: MIT", bridge)
        self.assertIn("不从 `external-skills/` 缓存目录执行", bridge)

    def test_upstream_skills_route_ui_work_to_governor(self):
        routed_files = [
            REPO_ROOT / "skills" / "product-design-management" / "SKILL.md",
            REPO_ROOT / "skills" / "ai-native-delivery-governor" / "SKILL.md",
            REPO_ROOT / "catalog" / "README.md",
        ]

        for path in routed_files:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("oristrat-product-ui-governor", text)


if __name__ == "__main__":
    unittest.main()
