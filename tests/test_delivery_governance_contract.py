import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DeliveryGovernanceContractTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_runtime_lock_tracks_self_developed_and_external_ui_skills(self):
        lock = json.loads(self.read("catalog/runtime-skill-lock.json"))
        self_names = {item["name"] for item in lock["selfDeveloped"]}
        external_names = {item["name"] for item in lock["externalDependencies"]}
        self.assertIn("msce-engine-app-development", self_names)
        self.assertIn("oristrat-product-ui-governor", self_names)
        self.assertIn("task-council", self_names)
        self.assertIn("document-delivery-orchestration", self_names)
        council = next(item for item in lock["selfDeveloped"] if item["name"] == "task-council")
        document = next(
            item for item in lock["selfDeveloped"]
            if item["name"] == "document-delivery-orchestration"
        )
        self.assertTrue(council["installRequired"])
        self.assertTrue(document["installRequired"])
        self.assertTrue({"ui-ux-pro-max", "hallmark", "frontend-design"} <= external_names)
        ui_ux = next(item for item in lock["externalDependencies"] if item["name"] == "ui-ux-pro-max")
        self.assertEqual("2.11.0", ui_ux["version"])

    def test_delivery_governor_enforces_one_shot_approval_and_baseline_status(self):
        skill = self.read("skills/ai-native-delivery-governor/SKILL.md")
        self.assertIn("one-shot and scope-bound", skill)
        self.assertIn("TARGET_PASS", skill)
        self.assertIn("REPO_BASELINE_FAIL", skill)
        self.assertIn("NEW_REGRESSION", skill)
        self.assertIn("HTTP `200`", skill)

    def test_code_submission_requires_strict_msce_before_git(self):
        governor = self.read("skills/ai-native-delivery-governor/SKILL.md")
        git_gate = self.read("skills/ai-native-delivery-governor/references/git-release-gates.md")
        state_machine = self.read("skills/ai-native-delivery-governor/references/delivery-state-machine.md")
        msce = self.read("skills/msce-engine-app-development/SKILL.md")
        fullstack = self.read("skills/fullstack-delivery-orchestration/SKILL.md")
        dashboard = self.read("看板.md")

        for content in (governor, git_gate, state_machine, msce, fullstack):
            self.assertIn("MSCE_SUBMISSION_GATE: PASS", content)
        self.assertIn("CODE_COMPLETE", git_gate)
        self.assertIn("MSCE_STAGED_AUDITED", git_gate)
        self.assertIn("Any code change after the pass invalidates it", governor)
        self.assertIn("启动 AI 原生交付总控", dashboard)
        self.assertNotIn("[!skill-command] 01 · 代码开发 + 严格 MSCE + Git 分轮", dashboard)
        self.assertNotIn("[!skill-command] 02 · 严格 MSCE 门禁", dashboard)
        self.assertNotIn("[!skill-command] 07 · Git 分轮提交", dashboard)
        self.assertNotIn("[!skill-command] 06 · 运行态检查", dashboard)

    def test_governor_uses_controller_foundation_application_architecture(self):
        governor = self.read("skills/ai-native-delivery-governor/SKILL.md")
        modes = self.read("skills/ai-native-delivery-governor/references/delivery-modes.md")
        runtime = self.read("skills/ai-native-delivery-governor/references/runtime-dependency-gates.md")
        catalog = self.read("catalog/README.md")
        dashboard = self.read("看板.md")

        for phrase in ("Controller entry", "Foundation capabilities", "Application skills"):
            self.assertIn(phrase, governor)
        for skill_name in (
            "fullstack-delivery-orchestration",
            "msce-engine-app-development",
            "document-delivery-orchestration",
            "product-design-management",
            "oristrat-product-ui-governor",
            "product-testing",
            "task-council",
        ):
            self.assertIn(skill_name, governor)
        self.assertIn("internal controller modes", modes)
        self.assertIn("foundation capability automatically inherited", runtime)
        self.assertIn("三层运行架构", catalog)
        self.assertIn("总控（唯一任务入口）", dashboard)
        self.assertIn("代码交付底座（由总控自动组合，仅供维护查看）", dashboard)
        self.assertIn("文档交付底座（由总控自动组合，仅供维护查看）", dashboard)

    def test_code_document_and_mixed_routes_have_independent_gates(self):
        governor = self.read("skills/ai-native-delivery-governor/SKILL.md")
        state_machine = self.read(
            "skills/ai-native-delivery-governor/references/delivery-state-machine.md"
        )
        git_gate = self.read("skills/ai-native-delivery-governor/references/git-release-gates.md")
        document_skill = self.read("skills/document-delivery-orchestration/SKILL.md")
        document_gate = self.read(
            "skills/document-delivery-orchestration/references/document-delivery-gates.md"
        )
        dashboard = self.read("看板.md")

        for route in ("CODE_DELIVERY", "DOCUMENT_DELIVERY", "MIXED_DELIVERY"):
            self.assertIn(route, governor)
            self.assertIn(route, dashboard)
        for gate in (
            "MSCE_SUBMISSION_GATE: PASS",
            "DOCUMENT_DELIVERY_GATE: PASS",
            "MIXED_DELIVERY_GATE: PASS",
        ):
            self.assertIn(gate, governor)
            self.assertIn(gate, state_machine)
        self.assertIn("DOCUMENT_DELIVERY_GATE: PASS", git_gate)
        self.assertIn("a document pass never proves code quality", document_skill)
        self.assertIn("an MSCE pass never proves document quality", document_skill)
        for heading in (
            "Scope Gate",
            "Evidence Gate",
            "Content Gate",
            "Format And Render Gate",
            "Safety Gate",
            "Package And Handoff Gate",
        ):
            self.assertIn(heading, document_gate)
        self.assertNotIn("[!skill-command] 06 · 文档交付", dashboard)

    def test_git_merge_gate_covers_dirty_and_ignored_state(self):
        gate = self.read("skills/ai-native-delivery-governor/references/git-worktree-and-merge-gates.md")
        for phrase in ("ignored files", "backup branch", "stash commit hashes", "both parents"):
            self.assertIn(phrase, gate)

    def test_ui_chain_records_external_availability_and_does_not_execute_cache(self):
        bridge = self.read("skills/oristrat-product-ui-governor/references/external-design-skill-bridge.md")
        for phrase in ("ui-ux-pro-max", "Hallmark", "frontend-design", "UNAVAILABLE", "product-testing browser evidence"):
            self.assertIn(phrase, bridge)
        self.assertIn("不从 `external-skills/` 缓存目录执行", bridge)

    def test_form_gate_covers_password_reset_regressions(self):
        form = self.read("skills/oristrat-product-ui-governor/references/form-feedback-and-validation.md")
        required = (
            "对应输入框下方",
            "warning/黄色 Toast",
            "两次密码不一致",
            "关闭、重新打开",
            "服务端验证码校验",
            "用新密码登录",
        )
        for phrase in required:
            self.assertIn(phrase, form)

    def test_msce_source_and_read_only_scripts_exist(self):
        skill_root = REPO_ROOT / "skills" / "msce-engine-app-development"
        expected = (
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/audit-staged-scope.ps1",
            "scripts/validate-staged-batch.ps1",
        )
        for relative in expected:
            self.assertTrue((skill_root / relative).is_file(), relative)

        scripts = "\n".join(
            path.read_text(encoding="utf-8") for path in (skill_root / "scripts").glob("*.ps1")
        )
        self.assertIsNone(re.search(r"git\s+(add|commit|push|reset|checkout)", scripts, flags=re.I))

    def test_cross_skill_tools_are_read_only(self):
        scripts = "\n".join(
            self.read(path)
            for path in (
                "tools/check_skill_install_sync.ps1",
                "tools/validate_skills_utf8.ps1",
            )
        )
        forbidden = ("Copy-Item", "Remove-Item", "Move-Item", "git commit", "git push")
        for token in forbidden:
            self.assertNotIn(token, scripts)

    def test_validation_tool_can_include_runtime_dependencies(self):
        script = self.read("tools/validate_skills_utf8.ps1")
        self.assertIn("IncludeRuntimeDependencies", script)
        self.assertIn("runtime-external", script)


if __name__ == "__main__":
    unittest.main()
