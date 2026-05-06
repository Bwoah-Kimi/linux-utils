import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
API_SWITCHER = REPO_ROOT / "modules" / "api-switcher"


class TemplateSanitizationTest(unittest.TestCase):
    def test_codex_auth_list_uses_placeholders(self):
        data = json.loads((API_SWITCHER / "templates" / "codex" / "auth_list.json").read_text(encoding="utf-8"))
        self.assertTrue(data)
        for provider, value in data.items():
            with self.subTest(provider=provider):
                self.assertEqual(value, "<fill-me>")

    def test_claude_provider_list_contains_no_real_tokens(self):
        raw = (API_SWITCHER / "templates" / "claude" / "provider_list.json").read_text(encoding="utf-8")
        self.assertNotIn("sk-", raw)
        self.assertNotIn("clp_", raw)
        self.assertNotIn("G5XPWz", raw)

    def test_readme_documents_install_workflow(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        api_readme = (API_SWITCHER / "README.md").read_text(encoding="utf-8")
        docs = readme + "\n" + api_readme
        self.assertIn("bash install/install_codex_api.sh", docs)
        self.assertIn("bash install/install_cc_api.sh", docs)
        self.assertIn("bash install/install_proxy.sh", readme)
        self.assertIn("~/.codex", docs)
        self.assertIn("~/.claude", docs)
        self.assertIn("fill in real secrets", docs.lower())


if __name__ == "__main__":
    unittest.main()
