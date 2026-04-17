import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallProxyTest(unittest.TestCase):
    def test_install_proxy_copies_script_and_managed_wrapper_block(self):
        with tempfile.TemporaryDirectory() as tmp:
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

            env = os.environ.copy()
            env["HOME"] = str(home)

            result = subprocess.run(
                ["bash", "install/install_proxy.sh"],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".local" / "bin" / "proxy").exists())
            bash_functions = (home / ".bash_functions").read_text(encoding="utf-8")
            self.assertIn("BEGIN linux-utils proxy wrapper", bash_functions)
            self.assertIn("command proxy status", bash_functions)
            self.assertIn("existing_func()", bash_functions)


if __name__ == "__main__":
    unittest.main()
