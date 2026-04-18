import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallShellStartupSkillsTest(unittest.TestCase):
    def test_install_codex_shell_startup_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = os.environ.copy()
            env["HOME"] = str(home)

            result = subprocess.run(
                ["bash", "install/install_codex_shell_startup_skill.sh"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".codex" / "skills" / "shell-startup-normalizer" / "SKILL.md").exists())

    def test_install_claude_shell_startup_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = os.environ.copy()
            env["HOME"] = str(home)

            result = subprocess.run(
                ["bash", "install/install_claude_shell_startup_skill.sh"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (home / ".claude" / "skills" / "shell-startup-normalizer" / "claude" / "CLAUDE.md").exists()
            )


if __name__ == "__main__":
    unittest.main()
