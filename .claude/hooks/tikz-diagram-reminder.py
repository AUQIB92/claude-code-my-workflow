#!/usr/bin/env python3
"""
TikZ Diagram Review Reminder Hook (PostToolUse)

Mechanical nudge for the render-based visual QA gap: tikz-reviewer only
catches font-metric/anchor-specific overlaps if it's actually invoked, and
today's shipped Lab-manual bugs (see quality_reports/session_logs/
2026-08-20_auto.md) happened because nothing reminded the authoring skill
to run it. Purely-instructional rules (e.g. proofreading-protocol.md) are
trust-based; this hook gives a real, mechanical trigger instead, mirroring
claim-reconcile.py's shape for the reproducibility-claims pipeline.

Fires on Write/Edit/MultiEdit to any `.tex` file whose resulting content
contains `\begin{tikzpicture}`. Emits a one-line systemMessage + fuller
additionalContext pointing at /new-diagram, /extract-tikz, or a direct
Task subagent_type=tikz-reviewer call. Throttled to once per file per
session (a burst of edits to the same diagram is one nudge).

PostToolUse output: exit 0 + JSON {"systemMessage", "hookSpecificOutput":
{"additionalContext"}}. Fail-open: any error → exit 0, silent.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import hashlib
from pathlib import Path

TIKZ_BEGIN = re.compile(r"\\begin\{tikzpicture\}")
THROTTLE_S = 300


def state_dir() -> Path:
    pd = os.environ.get("CLAUDE_PROJECT_DIR", "")
    h = hashlib.md5(pd.encode()).hexdigest()[:8] if pd else "default"
    d = Path.home() / ".claude" / "sessions" / h
    d.mkdir(parents=True, exist_ok=True)
    return d


def extract_content(tool_input: dict) -> str:
    """Best-effort text of what the file now contains, from tool_input alone
    (works for Write's `content`; for Edit/MultiEdit falls back to the
    edited fragment(s), which is enough to detect a newly-added tikzpicture
    even though it won't see unrelated pre-existing content)."""
    if "content" in tool_input:
        return tool_input.get("content", "") or ""
    if "new_string" in tool_input:
        return tool_input.get("new_string", "") or ""
    edits = tool_input.get("edits", None)
    if isinstance(edits, list):
        return "\n".join(e.get("new_string", "") or "" for e in edits if isinstance(e, dict))
    return ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    ti = data.get("tool_input", {}) or {}
    fp = ti.get("file_path", "") or ""
    if not fp or not fp.endswith(".tex"):
        return 0

    if not TIKZ_BEGIN.search(extract_content(ti)):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "") or data.get("cwd", "")
    try:
        changed = str(Path(fp).resolve().relative_to(Path(project_dir).resolve())) if project_dir else fp
    except Exception:
        changed = Path(fp).name

    # Throttle: one nudge per changed file per THROTTLE_S.
    st_path = state_dir() / "tikz-diagram-reminder-state.json"
    try:
        st = json.loads(st_path.read_text())
    except Exception:
        st = {}
    now = time.time()
    if now - st.get(changed, 0) < THROTTLE_S:
        return 0
    st[changed] = now
    try:
        st_path.write_text(json.dumps(st))
    except Exception:
        pass

    msg = (f"⟳ {changed} has a TikZ diagram — run tikz-reviewer (via /new-diagram, "
           f"/extract-tikz, or Task subagent_type=tikz-reviewer directly) and visually "
           f"confirm the render before shipping.")
    json.dump({
        "systemMessage": msg,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"A tikzpicture block was just written/edited in {changed}. Source-only "
                f"review misses font-metric and library-anchor-specific overlaps (the exact "
                f"bug class fixed in Labs/CS401/lab-2 and lab-3 on 2026-08-20). Before "
                f"presenting or committing this diagram, compile it, spawn tikz-reviewer "
                f"(Task subagent_type=tikz-reviewer) with the compiled .pdf path, and loop "
                f"until it returns APPROVED — it will rasterize and actually look at the "
                f"render (Pass 6) before reasoning from source."
            ),
        },
    }, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # fail open
