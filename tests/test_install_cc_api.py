import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallCcApiTest(unittest.TestCase):
    def test_install_cc_api_copies_script_and_provider_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            (home / ".claude" / "settings.json").write_text(
                '{"env": {"PATH": "/usr/bin"}}\n',
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(home)

            result = subprocess.run(
                ["bash", "install/install_cc_api.sh"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".local" / "bin" / "cc_api").exists())
            provider_list = json.loads((home / ".claude" / "provider_list.json").read_text(encoding="utf-8"))
            self.assertEqual(provider_list["cubence"]["ANTHROPIC_AUTH_TOKEN"], "<fill-me>")
            settings = (home / ".claude" / "settings.json").read_text(encoding="utf-8")
            self.assertIn('"PATH": "/usr/bin"', settings)


if __name__ == "__main__":
    unittest.main()
