import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallCodexApiTest(unittest.TestCase):
    def test_install_codex_api_copies_script_and_merges_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            (home / ".codex" / "config.toml").write_text(
                'model_provider = "old-provider"\n'
                'model = "gpt-5.4"\n'
                '\n'
                '[projects."/tmp/project"]\n'
                'trust_level = "trusted"\n',
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(home)

            result = subprocess.run(
                ["bash", "install/install_codex_api.sh"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".local" / "bin" / "codex_api").exists())
            auth_list = json.loads((home / ".codex" / "auth_list.json").read_text(encoding="utf-8"))
            self.assertEqual(auth_list["packycode"], "<fill-me>")
            config = (home / ".codex" / "config.toml").read_text(encoding="utf-8")
            self.assertIn('model_provider = "codex-for-me"', config)
            self.assertIn('[projects."/tmp/project"]', config)
            self.assertIn('trust_level = "trusted"', config)
            self.assertIn('[model_providers.cubence]', config)


if __name__ == "__main__":
    unittest.main()
