import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHELL_STARTUP = REPO_ROOT / "modules" / "shell-startup-normalizer"
SKILL_DIR = SHELL_STARTUP / "skill"


class ShellStartupSkillStructureTest(unittest.TestCase):
    def test_skill_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "layout.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "migration-heuristics.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "examples.md").exists())
        self.assertTrue((SKILL_DIR / "claude" / "CLAUDE.md").exists())

    def test_skill_frontmatter_and_trigger(self):
        raw = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: shell-startup-normalizer", raw)
        self.assertIn("description: Use when", raw)
        self.assertIn(".bashrc", raw)
        self.assertIn(".zshrc", raw)
        self.assertIn("tool-managed", raw)
        self.assertIn("backups", raw)

    def test_readme_documents_skill_install_flow(self):
        readme = (SHELL_STARTUP / "README.md").read_text(encoding="utf-8")
        self.assertIn("bash install/install_codex_shell_startup_skill.sh", readme)
        self.assertIn("bash install/install_claude_shell_startup_skill.sh", readme)
        self.assertIn("~/.codex/skills/shell-startup-normalizer", readme)
        self.assertIn("~/.claude/skills/shell-startup-normalizer", readme)


if __name__ == "__main__":
    unittest.main()
