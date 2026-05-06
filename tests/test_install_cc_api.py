import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
API_SWITCHER = REPO_ROOT / "modules" / "api-switcher"
API_SWITCHER_INSTALL = "modules/api-switcher/install"


def bash_path(path: Path) -> str:
    value = path.resolve().as_posix()
    if len(value) >= 3 and value[1:3] == ":/":
        return f"/mnt/{value[0].lower()}/{value[3:]}"
    return value


def run_bash_with_home(script: str, home: Path) -> subprocess.CompletedProcess:
    command = f"HOME={shlex.quote(bash_path(home))} bash {shlex.quote(script)}"
    return subprocess.run(
        ["bash", "-lc", command],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class InstallCcApiTest(unittest.TestCase):
    def test_install_cc_api_copies_script_and_provider_template(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            (home / ".claude" / "settings.json").write_text(
                '{"env": {"PATH": "/usr/bin"}}\n',
                encoding="utf-8",
            )

            result = run_bash_with_home(f"{API_SWITCHER_INSTALL}/install_cc_api.sh", home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".local" / "bin" / "cc_api").exists())
            provider_list = json.loads((home / ".claude" / "provider_list.json").read_text(encoding="utf-8"))
            self.assertEqual(provider_list["cubence"]["ANTHROPIC_AUTH_TOKEN"], "<fill-me>")
            settings = (home / ".claude" / "settings.json").read_text(encoding="utf-8")
            self.assertIn('"PATH": "/usr/bin"', settings)


if __name__ == "__main__":
    unittest.main()
