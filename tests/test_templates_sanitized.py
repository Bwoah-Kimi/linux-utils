import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TemplateSanitizationTest(unittest.TestCase):
    def test_codex_auth_list_uses_placeholders(self):
        data = json.loads((REPO_ROOT / "templates/codex/auth_list.json").read_text(encoding="utf-8"))
        self.assertEqual(
            data,
            {
                "packycode": "<fill-me>",
                "cubence": "<fill-me>",
                "codex-for-me": "<fill-me>",
            },
        )

    def test_claude_provider_list_contains_no_real_tokens(self):
        raw = (REPO_ROOT / "templates/claude/provider_list.json").read_text(encoding="utf-8")
        self.assertNotIn("sk-", raw)
        self.assertNotIn("clp_", raw)
        self.assertNotIn("G5XPWz", raw)

    def test_readme_documents_install_workflow(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("bash install/install_codex_api.sh", readme)
        self.assertIn("bash install/install_cc_api.sh", readme)
        self.assertIn("bash install/install_proxy.sh", readme)
        self.assertIn("~/.codex", readme)
        self.assertIn("~/.claude", readme)
        self.assertIn("fill in real secrets", readme.lower())


if __name__ == "__main__":
    unittest.main()
