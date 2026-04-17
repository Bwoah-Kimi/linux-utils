# Linux Utils Helper Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package `codex_api`, `cc_api`, and `proxy` into the `linux-utils` repo with sanitized templates and copy-based installer scripts so a fresh machine can clone the repo, run the installers, add secrets manually, and use the helpers.

**Architecture:** Store portable executables under `bin/`, helper-owned sanitized config under `templates/`, installer entrypoints under `install/`, and shared install/merge logic under `lib/`. Use Python standard-library tests and temp-HOME integration fixtures so installers and merge logic can be verified without touching the real `~/.codex`, `~/.claude`, or shell files.

**Tech Stack:** Bash, Python 3 standard library (`json`, `pathlib`, `tempfile`, `subprocess`, `textwrap`, `tomllib`), Git

---

## File Structure

**Files:**
- Create: `bin/codex_api`
- Create: `bin/cc_api`
- Create: `bin/proxy`
- Create: `install/install_codex_api.sh`
- Create: `install/install_cc_api.sh`
- Create: `install/install_proxy.sh`
- Create: `lib/install_common.sh`
- Create: `lib/merge_codex_config.py`
- Create: `templates/codex/auth_list.json`
- Create: `templates/codex/config.providers.toml`
- Create: `templates/claude/provider_list.json`
- Create: `tests/test_templates_sanitized.py`
- Create: `tests/test_merge_codex_config.py`
- Create: `tests/test_install_codex_api.py`
- Create: `tests/test_install_cc_api.py`
- Create: `tests/test_install_proxy.py`
- Modify: `README.md`

### Task 1: Stage Portable Scripts And Sanitized Templates

**Files:**
- Create: `bin/codex_api`
- Create: `bin/cc_api`
- Create: `bin/proxy`
- Create: `templates/codex/auth_list.json`
- Create: `templates/codex/config.providers.toml`
- Create: `templates/claude/provider_list.json`
- Create: `tests/test_templates_sanitized.py`

- [ ] **Step 1: Write the failing template-sanitization test**

```python
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_codex_auth_list_uses_placeholders():
    data = json.loads((REPO_ROOT / "templates/codex/auth_list.json").read_text())
    assert data == {
        "packycode": "<fill-me>",
        "cubence": "<fill-me>",
        "codex-for-me": "<fill-me>",
    }

def test_claude_provider_list_contains_no_real_tokens():
    raw = (REPO_ROOT / "templates/claude/provider_list.json").read_text()
    assert "sk-" not in raw
    assert "clp_" not in raw
    assert "G5XPWz" not in raw
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_templates_sanitized.py`
Expected: FAIL because repo scripts/templates do not exist yet

- [ ] **Step 3: Copy the current helper scripts into repo-owned executables**

Implement:
- copy `/root/.local/bin/codex_api` to `bin/codex_api`
- copy `/root/.local/bin/cc_api` to `bin/cc_api`
- copy `/root/.local/bin/proxy` to `bin/proxy`
- preserve shebangs and executable-friendly content
- do not change behavior yet beyond repo relocation

- [ ] **Step 4: Create sanitized helper-owned templates**

Implement:
- `templates/codex/auth_list.json` with provider names and `"<fill-me>"` values
- `templates/codex/config.providers.toml` with only:

```toml
model_provider = "codex-for-me"

[model_providers.packycode]
name = "packycode"
base_url = "https://codex-api.packycode.com/v1"
wire_api = "responses"
requires_openai_auth = true

[model_providers.cubence]
name = "cubence"
base_url = "https://api.cubence.com/v1"
wire_api = "responses"
requires_openai_auth = true

[model_providers.codex-for-me]
name = "codex-for-me"
base_url = "https://hello.vangularcode.asia/v1"
wire_api = "responses"
requires_openai_auth = true
```

- `templates/claude/provider_list.json` with the current provider keys but placeholder secret values, for example:

```json
{
  "cubence": {
    "ANTHROPIC_AUTH_TOKEN": "<fill-me>",
    "ANTHROPIC_BASE_URL": "https://api.cubence.com"
  },
  "autodl_claude": {
    "ANTHROPIC_AUTH_TOKEN": "<fill-me>",
    "ANTHROPIC_BASE_URL": "https://www.autodl.art/api/v1/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6-cc",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6-cc",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6-cc"
  }
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 tests/test_templates_sanitized.py`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add bin/codex_api bin/cc_api bin/proxy templates/codex/auth_list.json templates/codex/config.providers.toml templates/claude/provider_list.json tests/test_templates_sanitized.py
git commit -m "feat: add portable helper scripts and sanitized templates"
```

### Task 2: Implement Shared Install Logic And Codex Config Merge

**Files:**
- Create: `lib/install_common.sh`
- Create: `lib/merge_codex_config.py`
- Create: `tests/test_merge_codex_config.py`

- [ ] **Step 7: Write the failing Codex merge test**

```python
import subprocess
import tempfile
from pathlib import Path

def test_merge_replaces_only_helper_managed_codex_keys():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        local_config = tmp_path / "config.toml"
        provider_config = tmp_path / "config.providers.toml"
        local_config.write_text(
            'model_provider = "old-provider"\n'
            'model = "gpt-5.4"\n'
            '[model_providers.old-provider]\n'
            'name = "old-provider"\n'
            '[projects."/tmp/project"]\n'
            'trust_level = "trusted"\n'
        )
        provider_config.write_text(
            'model_provider = "cubence"\n'
            '[model_providers.cubence]\n'
            'name = "cubence"\n'
            'base_url = "https://api.cubence.com/v1"\n'
            'wire_api = "responses"\n'
            'requires_openai_auth = true\n'
        )
        result = subprocess.run(
            ["python3", "lib/merge_codex_config.py", str(local_config), str(provider_config)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        merged = local_config.read_text()
        assert 'model_provider = "cubence"' in merged
        assert '[projects."/tmp/project"]' in merged
        assert '[model_providers.old-provider]' not in merged
```

- [ ] **Step 8: Run test to verify it fails**

Run: `python3 tests/test_merge_codex_config.py`
Expected: FAIL because merge utility does not exist yet

- [ ] **Step 9: Write minimal shared install helpers**

Implement `lib/install_common.sh` with focused functions such as:
- `ensure_dir`
- `backup_file`
- `copy_file`
- `set_executable`
- `require_existing_dir`
- `print_step`

Keep it shell-only and reusable by all installer entrypoints.

- [ ] **Step 10: Write the minimal Codex merge utility**

Implement `lib/merge_codex_config.py` to:
- read local `config.toml`
- read `templates/codex/config.providers.toml`
- replace top-level `model_provider`
- replace all `[model_providers.*]` blocks
- preserve every non-helper-managed section from the local config
- write the merged result back to the target path

- [ ] **Step 11: Run test to verify it passes**

Run: `python3 tests/test_merge_codex_config.py`
Expected: PASS

- [ ] **Step 12: Commit**

```bash
git add lib/install_common.sh lib/merge_codex_config.py tests/test_merge_codex_config.py
git commit -m "feat: add shared installer helpers and codex config merge"
```

### Task 3: Implement `install_codex_api.sh`

**Files:**
- Create: `install/install_codex_api.sh`
- Create: `tests/test_install_codex_api.py`

- [ ] **Step 13: Write the failing Codex installer integration test**

```python
import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_install_codex_api_copies_script_and_merges_config():
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / ".codex").mkdir()
        (home / ".codex/config.toml").write_text(
            'model_provider = "old-provider"\n'
            'model = "gpt-5.4"\n'
            '[projects."/tmp/project"]\n'
            'trust_level = "trusted"\n'
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
        assert result.returncode == 0
        assert (home / ".local/bin/codex_api").exists()
        auth_list = json.loads((home / ".codex/auth_list.json").read_text())
        assert auth_list["packycode"] == "<fill-me>"
        config = (home / ".codex/config.toml").read_text()
        assert 'model_provider = "codex-for-me"' in config
        assert '[projects."/tmp/project"]' in config
```

- [ ] **Step 14: Run test to verify it fails**

Run: `python3 tests/test_install_codex_api.py`
Expected: FAIL because installer does not exist yet

- [ ] **Step 15: Write minimal installer implementation**

Implement `install/install_codex_api.sh` to:
- source `lib/install_common.sh`
- require `~/.codex/`
- ensure `~/.local/bin/`
- copy `bin/codex_api` to `~/.local/bin/codex_api`
- copy `templates/codex/auth_list.json` to `~/.codex/auth_list.json`
- back up existing `~/.codex/auth_list.json` and `~/.codex/config.toml`
- run `python3 lib/merge_codex_config.py ~/.codex/config.toml templates/codex/config.providers.toml`
- print manual follow-up reminding the user to fill in real API keys

- [ ] **Step 16: Run test to verify it passes**

Run: `python3 tests/test_install_codex_api.py`
Expected: PASS

- [ ] **Step 17: Commit**

```bash
git add install/install_codex_api.sh tests/test_install_codex_api.py
git commit -m "feat: add codex_api installer"
```

### Task 4: Implement `install_cc_api.sh`

**Files:**
- Create: `install/install_cc_api.sh`
- Create: `tests/test_install_cc_api.py`

- [ ] **Step 18: Write the failing Claude installer integration test**

```python
import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_install_cc_api_copies_script_and_provider_template():
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / ".claude").mkdir()
        (home / ".claude/settings.json").write_text('{"env": {"PATH": "/usr/bin"}}\n')
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
        assert result.returncode == 0
        assert (home / ".local/bin/cc_api").exists()
        provider_list = json.loads((home / ".claude/provider_list.json").read_text())
        assert provider_list["cubence"]["ANTHROPIC_AUTH_TOKEN"] == "<fill-me>"
        settings = (home / ".claude/settings.json").read_text()
        assert '"PATH": "/usr/bin"' in settings
```

- [ ] **Step 19: Run test to verify it fails**

Run: `python3 tests/test_install_cc_api.py`
Expected: FAIL because installer does not exist yet

- [ ] **Step 20: Write minimal installer implementation**

Implement `install/install_cc_api.sh` to:
- source `lib/install_common.sh`
- require `~/.claude/`
- ensure `~/.local/bin/`
- copy `bin/cc_api` to `~/.local/bin/cc_api`
- copy `templates/claude/provider_list.json` to `~/.claude/provider_list.json`
- back up existing `~/.claude/provider_list.json` if present
- leave `~/.claude/settings.json` untouched
- print manual follow-up reminding the user to fill in real provider tokens

- [ ] **Step 21: Run test to verify it passes**

Run: `python3 tests/test_install_cc_api.py`
Expected: PASS

- [ ] **Step 22: Commit**

```bash
git add install/install_cc_api.sh tests/test_install_cc_api.py
git commit -m "feat: add cc_api installer"
```

### Task 5: Implement `install_proxy.sh`

**Files:**
- Create: `install/install_proxy.sh`
- Create: `tests/test_install_proxy.py`

- [ ] **Step 23: Write the failing proxy installer integration test**

```python
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def test_install_proxy_copies_script_and_managed_wrapper_block():
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / ".local").mkdir()
        (home / ".bashrc").write_text('if [ -f ~/.bash_functions ]; then . ~/.bash_functions; fi\n')
        (home / ".bash_functions").write_text("existing_func() { :; }\n")
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
        assert result.returncode == 0
        assert (home / ".local/bin/proxy").exists()
        bash_functions = (home / ".bash_functions").read_text()
        assert "BEGIN linux-utils proxy wrapper" in bash_functions
        assert "command proxy status" in bash_functions
        assert "existing_func()" in bash_functions
```

- [ ] **Step 24: Run test to verify it fails**

Run: `python3 tests/test_install_proxy.py`
Expected: FAIL because installer does not exist yet

- [ ] **Step 25: Write minimal installer implementation**

Implement `install/install_proxy.sh` to:
- source `lib/install_common.sh`
- ensure `~/.local/bin/`
- copy `bin/proxy` to `~/.local/bin/proxy`
- create `~/.bash_functions` if missing
- insert or replace a clearly delimited managed block, for example:

```bash
# BEGIN linux-utils proxy wrapper
proxy() {
    local action="${1:-status}"
    local shell_snippet=""
    case "${action}" in
        on|set)
            shift
            shell_snippet="$(command proxy on "$@")" || return $?
            eval "${shell_snippet}"
            command proxy status
            ;;
        off|unset)
            shift
            shell_snippet="$(command proxy off)" || return $?
            eval "${shell_snippet}"
            command proxy status
            ;;
        status)
            shift
            command proxy status "$@"
            ;;
        resolve)
            shift
            command proxy resolve "$@"
            ;;
        *)
            echo "Usage: proxy {on|off|status|resolve|set|unset} [--host HOST] [--port PORT] [--scheme SCHEME]" >&2
            return 1
            ;;
    esac
}
# END linux-utils proxy wrapper
```

- [ ] **Step 26: Run test to verify it passes**

Run: `python3 tests/test_install_proxy.py`
Expected: PASS

- [ ] **Step 27: Commit**

```bash
git add install/install_proxy.sh tests/test_install_proxy.py
git commit -m "feat: add proxy installer"
```

### Task 6: Update Documentation And Run Full Verification

**Files:**
- Modify: `README.md`

- [ ] **Step 28: Write the failing README expectation check**

Use a simple script or direct assertion in one of the existing tests to require:
- quick install commands
- prerequisites for `~/.codex/` and `~/.claude/`
- manual secret-entry reminder

- [ ] **Step 29: Run the failing documentation check**

Run: `python3 tests/test_templates_sanitized.py`
Expected: FAIL once the README assertions are added and before README is updated

- [ ] **Step 30: Update README with install workflow**

Document:
- repo layout
- `bash install/install_codex_api.sh`
- `bash install/install_cc_api.sh`
- `bash install/install_proxy.sh`
- manual secret editing after install
- shell reload guidance for `proxy`

- [ ] **Step 31: Run the full verification suite**

Run:
- `python3 tests/test_templates_sanitized.py`
- `python3 tests/test_merge_codex_config.py`
- `python3 tests/test_install_codex_api.py`
- `python3 tests/test_install_cc_api.py`
- `python3 tests/test_install_proxy.py`

Expected:
- every command exits 0
- no real secrets appear in tracked template files

- [ ] **Step 32: Commit**

```bash
git add README.md tests/test_templates_sanitized.py
git commit -m "docs: add helper installation guide"
```
