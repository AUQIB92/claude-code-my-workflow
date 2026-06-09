#!/usr/bin/env python3
"""
Git & Path Guardrails Hook (PreToolUse)

Blocks the small set of operations that are destructive or that the
template's own conventions forbid — before they run, not after. Adapted
from the `git-guardrails` pattern in mattpocock/skills, scoped so the
normal workflow (`/commit` pushes, stages specific files) still works.

Two checks, by tool:

  Bash — deny destructive / convention-violating git:
    - git reset --hard            (silently discards work)
    - git clean -f / -fd / -fdx   (deletes UNTRACKED files — incl. data)
    - git push --force / -f       (clobbers remote history; --force-with-lease is allowed)
    - git add -A / --all / git add .   (the commit skill forbids blanket staging)
    - git checkout -- . / git restore .   (mass discard of working changes)

  Write/Edit/MultiEdit — warn on hardcoded machine paths in code:
    - absolute home paths (/Users/<u>, /home/<u>, C:\\Users\\) written into
      .R / .qmd / .do / .py files break replication packages. Warn by
      default; set CLAUDE_STRICT_PATHS=1 to hard-deny.

Decision protocol (modern PreToolUse): exit 0 + JSON
  {"hookSpecificOutput": {"hookEventName": "PreToolUse",
    "permissionDecision": "deny", "permissionDecisionReason": "..."}}.
Fail-open: any error → exit 0 with no decision (allow).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# (compiled pattern, human reason, safe alternative)
GIT_DENY = [
    (re.compile(r"\bgit\s+reset\s+--hard\b"),
     "git reset --hard discards uncommitted work irrecoverably.",
     "Use `git stash` (recoverable) or reset specific paths."),
    (re.compile(r"\bgit\s+clean\s+-[a-z]*f"),
     "git clean -f deletes UNTRACKED files — including data not yet committed.",
     "Inspect with `git clean -n` first; delete specific paths by hand."),
    (re.compile(r"\bgit\s+push\b.*(--force\b|(?<!-)\s-f\b)"),
     "git push --force clobbers remote history.",
     "Use `git push --force-with-lease` if you truly must rewrite a branch."),
    (re.compile(r"\bgit\s+add\s+(-A\b|--all\b|\.(?:\s|$))"),
     "Blanket staging (git add -A / . ) can stage data, secrets, or settings.local.json. "
     "The /commit skill forbids it.",
     "Stage specific files: `git add path/to/file ...`."),
    (re.compile(r"\bgit\s+(checkout|restore)\s+(--\s+)?\.(?:\s|$)"),
     "Mass discard of working-tree changes is irreversible.",
     "Discard specific files, or `git stash` to keep them recoverable."),
]

HARDCODED_PATH = re.compile(r"(/Users/[^/\s'\")]+|/home/[^/\s'\")]+|[A-Za-z]:\\\\Users\\\\[^\\\s'\"]+)")
CODE_EXT = {".R", ".r", ".qmd", ".do", ".py", ".Rmd"}


def deny(reason: str) -> None:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, sys.stdout)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Bash":
        cmd = ti.get("command", "") or ""
        for pat, reason, alt in GIT_DENY:
            if pat.search(cmd):
                deny(f"Blocked by git-guardrails: {reason} {alt} "
                     f"(override: run it in a terminal yourself, outside Claude Code.)")
                return 0
        return 0

    if tool in ("Write", "Edit", "MultiEdit"):
        fp = ti.get("file_path", "") or ""
        if Path(fp).suffix not in CODE_EXT:
            return 0
        content = ti.get("content") or ti.get("new_string") or ""
        if isinstance(content, str):
            m = HARDCODED_PATH.search(content)
            if m:
                msg = (f"Hardcoded machine path '{m.group(0)}' in {Path(fp).name} "
                       f"breaks replication packages. Use here::here(), relative paths, "
                       f"or a config variable.")
                if os.environ.get("CLAUDE_STRICT_PATHS", "") == "1":
                    deny(f"Blocked (CLAUDE_STRICT_PATHS=1): {msg}")
                else:
                    sys.stderr.write(f"[git-guardrails] WARNING: {msg}\n")
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # fail open
