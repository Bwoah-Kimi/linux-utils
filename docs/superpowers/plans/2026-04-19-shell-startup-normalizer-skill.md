# Shell Startup Normalizer Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a canonical shell-startup-normalizer skill to `linux-utils`, plus Codex and Claude Code installers, so both tools can install guidance for actively normalizing messy Bash and Zsh startup files into a cleaner split layout.

**Architecture:** Store the canonical skill under `skills/shell-startup-normalizer/`, keep references alongside it, add a Claude-facing companion file in the same skill tree, and provide copy-based installers under `install/`. Validate the skill structure and installers with Python standard-library tests using temporary homes instead of mutating real `~/.codex` or `~/.claude` directories.

**Tech Stack:** Markdown, Bash, Python 3 standard library (`pathlib`, `tempfile`, `subprocess`, `shutil`, `re`), Git

---

## File Structure

**Files:**
- Create: `skills/shell-startup-normalizer/SKILL.md`
- Create: `skills/shell-startup-normalizer/references/layout.md`
- Create: `skills/shell-startup-normalizer/references/migration-heuristics.md`
- Create: `skills/shell-startup-normalizer/references/examples.md`
- Create: `skills/shell-startup-normalizer/claude/CLAUDE.md`
- Create: `install/install_codex_shell_startup_skill.sh`
- Create: `install/install_claude_shell_startup_skill.sh`
- Create: `tests/test_shell_startup_skill_structure.py`
- Create: `tests/test_install_shell_startup_skills.py`
- Modify: `README.md`

### Task 1: Add A Failing Structure Test For The Skill Package

**Files:**
- Create: `tests/test_shell_startup_skill_structure.py`

- [ ] **Step 1: Write the failing structure test**

```python
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills/shell-startup-normalizer"

class ShellStartupSkillStructureTest(unittest.TestCase):
    def test_skill_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "references/layout.md").exists())
        self.assertTrue((SKILL_DIR / "references/migration-heuristics.md").exists())
        self.assertTrue((SKILL_DIR / "references/examples.md").exists())
        self.assertTrue((SKILL_DIR / "claude/CLAUDE.md").exists())

    def test_skill_frontmatter_and_trigger(self):
        raw = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: shell-startup-normalizer", raw)
        self.assertIn("description: Use when", raw)
        self.assertIn(".bashrc", raw)
        self.assertIn(".zshrc", raw)
        self.assertIn("tool-managed", raw)
        self.assertIn("backups", raw)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_shell_startup_skill_structure.py`
Expected: FAIL because the skill directory and files do not exist yet

### Task 2: Write The Canonical Skill And Claude Companion

**Files:**
- Create: `skills/shell-startup-normalizer/SKILL.md`
- Create: `skills/shell-startup-normalizer/references/layout.md`
- Create: `skills/shell-startup-normalizer/references/migration-heuristics.md`
- Create: `skills/shell-startup-normalizer/references/examples.md`
- Create: `skills/shell-startup-normalizer/claude/CLAUDE.md`

- [ ] **Step 3: Write the minimal Codex skill**

Implement `skills/shell-startup-normalizer/SKILL.md` with:
- frontmatter:

```yaml
---
name: shell-startup-normalizer
description: Use when Bash or Zsh startup files are messy, mixed together, shell-specific, or need to be actively reorganized into a cleaner split layout while preserving tool-managed blocks.
---
```

- body sections that cover:
  - when to use
  - inspection order for Bash and Zsh startup files
  - classification categories
  - normalized target layout
  - safety rules
  - rewrite workflow
  - migration summary expectations
  - when to read each reference file

- [ ] **Step 4: Write the reference files**

Implement:
- `references/layout.md`
  - target cross-shell file layout
  - Bash vs Zsh file roles
- `references/migration-heuristics.md`
  - how to identify aliases, functions, env, path, login bootstrap, interactive setup
  - how to detect and preserve tool-managed blocks
  - warnings about shell-specific syntax
- `references/examples.md`
  - before/after examples for:
    - Linux Bash with `.bash_aliases` and `.bash_functions`
    - messy single-file `.zshrc`
    - preserving Conda or oh-my-posh blocks

- [ ] **Step 5: Write the Claude companion**

Implement `skills/shell-startup-normalizer/claude/CLAUDE.md` as a concise companion playbook that:
- points Claude Code at the same normalization workflow
- tells Claude to inspect shell startup files first
- preserves tool-managed blocks
- follows the same target layout and safety rules
- references the same `references/` files using relative paths

- [ ] **Step 6: Run the structure test to verify it passes**

Run: `python3 tests/test_shell_startup_skill_structure.py`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add skills/shell-startup-normalizer tests/test_shell_startup_skill_structure.py
git commit -m "feat: add shell startup normalizer skill"
```

### Task 3: Add Installer Tests For Codex And Claude Skill Installs

**Files:**
- Create: `tests/test_install_shell_startup_skills.py`

- [ ] **Step 8: Write the failing installer tests**

```python
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
            self.assertTrue((home / ".codex/skills/shell-startup-normalizer/SKILL.md").exists())

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
            self.assertTrue((home / ".claude/skills/shell-startup-normalizer/claude/CLAUDE.md").exists())
```

- [ ] **Step 9: Run test to verify it fails**

Run: `python3 tests/test_install_shell_startup_skills.py`
Expected: FAIL because the installer scripts do not exist yet

### Task 4: Implement Skill Installers

**Files:**
- Create: `install/install_codex_shell_startup_skill.sh`
- Create: `install/install_claude_shell_startup_skill.sh`

- [ ] **Step 10: Write the minimal Codex installer**

Implement `install/install_codex_shell_startup_skill.sh` to:
- resolve repo root
- create `~/.codex/skills/`
- back up an existing `~/.codex/skills/shell-startup-normalizer` if present
- copy `skills/shell-startup-normalizer/` into `~/.codex/skills/shell-startup-normalizer/`
- print install location and a short usage hint

- [ ] **Step 11: Write the minimal Claude installer**

Implement `install/install_claude_shell_startup_skill.sh` to:
- resolve repo root
- create `~/.claude/skills/`
- back up an existing `~/.claude/skills/shell-startup-normalizer` if present
- copy the same canonical skill directory into `~/.claude/skills/shell-startup-normalizer/`
- print install location and a short usage hint mentioning the Claude companion file

- [ ] **Step 12: Make the installers executable**

Run:
- `chmod 755 install/install_codex_shell_startup_skill.sh`
- `chmod 755 install/install_claude_shell_startup_skill.sh`

Expected: both scripts are runnable from bash

- [ ] **Step 13: Run the installer tests to verify they pass**

Run: `python3 tests/test_install_shell_startup_skills.py`
Expected: PASS

- [ ] **Step 14: Commit**

```bash
git add install/install_codex_shell_startup_skill.sh install/install_claude_shell_startup_skill.sh tests/test_install_shell_startup_skills.py
git commit -m "feat: add shell startup skill installers"
```

### Task 5: Document Install And Usage In README

**Files:**
- Modify: `README.md`

- [ ] **Step 15: Add a failing README expectation check**

Extend `tests/test_shell_startup_skill_structure.py` to require:
- `bash install/install_codex_shell_startup_skill.sh`
- `bash install/install_claude_shell_startup_skill.sh`
- `~/.codex/skills/shell-startup-normalizer`
- `~/.claude/skills/shell-startup-normalizer`

- [ ] **Step 16: Run the structure test to verify it fails**

Run: `python3 tests/test_shell_startup_skill_structure.py`
Expected: FAIL because README does not mention the new skill install flow yet

- [ ] **Step 17: Update README**

Document:
- what the shell-startup-normalizer skill does
- where the canonical skill lives in the repo
- how to install it for Codex
- how to install it for Claude Code
- the intended usage pattern after installation
- that the installers do not mutate shell startup files by themselves

- [ ] **Step 18: Run the structure test to verify it passes**

Run: `python3 tests/test_shell_startup_skill_structure.py`
Expected: PASS

- [ ] **Step 19: Commit**

```bash
git add README.md tests/test_shell_startup_skill_structure.py
git commit -m "docs: add shell startup skill install guide"
```

### Task 6: Run Full Verification

**Files:**
- Keep: `skills/shell-startup-normalizer/SKILL.md`
- Keep: `skills/shell-startup-normalizer/references/layout.md`
- Keep: `skills/shell-startup-normalizer/references/migration-heuristics.md`
- Keep: `skills/shell-startup-normalizer/references/examples.md`
- Keep: `skills/shell-startup-normalizer/claude/CLAUDE.md`
- Keep: `install/install_codex_shell_startup_skill.sh`
- Keep: `install/install_claude_shell_startup_skill.sh`
- Keep: `tests/test_shell_startup_skill_structure.py`
- Keep: `tests/test_install_shell_startup_skills.py`

- [ ] **Step 20: Run the full verification suite**

Run:
- `python3 tests/test_shell_startup_skill_structure.py`
- `python3 tests/test_install_shell_startup_skills.py`

Expected:
- both commands exit 0
- skill package exists and contains the required guidance files
- both installers copy the skill into temp-home Codex and Claude locations

- [ ] **Step 21: Commit any last documentation-only adjustments**

```bash
git status --short
```

If there are intended final changes, commit them with a focused message.
