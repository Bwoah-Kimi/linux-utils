import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROXY = REPO_ROOT / "modules" / "proxy"
PROXY_INSTALL = "modules/proxy/install"


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


class InstallProxyTest(unittest.TestCase):
    def test_install_proxy_copies_script_and_managed_wrapper_block(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            home = Path(tmp)
            (home / ".local").mkdir()
            (home / ".bashrc").write_text(
                "if [ -f ~/.bash_functions ]; then . ~/.bash_functions; fi\n",
                encoding="utf-8",
            )
            (home / ".bash_functions").write_text(
                "existing_func() { :; }\n",
                encoding="utf-8",
            )

            result = run_bash_with_home(f"{PROXY_INSTALL}/install_proxy.sh", home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".local" / "bin" / "proxy").exists())
            bash_functions = (home / ".bash_functions").read_text(encoding="utf-8")
            self.assertIn("BEGIN linux-utils proxy wrapper", bash_functions)
            self.assertIn("command proxy status", bash_functions)
            self.assertIn("existing_func()", bash_functions)


if __name__ == "__main__":
    unittest.main()
