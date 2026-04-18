import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "shell-startup-normalizer"


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


if __name__ == "__main__":
    unittest.main()
