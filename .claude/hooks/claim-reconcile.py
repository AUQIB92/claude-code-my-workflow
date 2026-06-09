#!/usr/bin/env python3
"""
Numeric-Claim Reconciliation Hook (PostToolUse)

Event-driven half of the cross-artifact dependency graph: the moment an
analysis script or an `_outputs/` artifact changes, the manuscript's
numeric claims that depend on it may be STALE. Instead of waiting for the
nightly reproducibility Routine, this hook surfaces the staleness
immediately so the author re-runs /audit-reproducibility before relying
on the affected tables.

Fires on Write/Edit to:
  - scripts/**/*.{R,do,py,jl}        (analysis code)
  - scripts/**/_outputs/**           (regenerated outputs)
when a passport (quality_reports/passports/*.yaml) exists. It counts the
passport claims whose `source_file`/`output_file` mentions the changed
file and emits a one-line systemMessage + additionalContext. Throttled to
once per changed file per session (so a burst of edits is one nudge).

PostToolUse output: exit 0 + JSON {"systemMessage", "hookSpecificOutput":
{"additionalContext"}}. Fail-open: any error → exit 0, silent.

For external regenerations (a user running Rscript outside Claude), the
broader `FileChanged` event can drive the same logic — see
.claude/references/scheduled-routines.md.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import hashlib
from pathlib import Path

WATCH = re.compile(r"(^|/)scripts/.*\.(R|r|do|py|jl)$|(^|/)scripts/.*/_outputs/")
THROTTLE_S = 300


def state_dir() -> Path:
    pd = os.environ.get("CLAUDE_PROJECT_DIR", "")
    h = hashlib.md5(pd.encode()).hexdigest()[:8] if pd else "default"
    d = Path.home() / ".claude" / "sessions" / h
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    ti = data.get("tool_input", {}) or {}
    fp = ti.get("file_path", "") or ""
    if not fp or not WATCH.search(fp):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "") or data.get("cwd", "")
    if not project_dir:
        return 0
    passports = sorted((Path(project_dir) / "quality_reports" / "passports").glob("*.yaml"))
    if not passports:
        return 0  # no claims tracked → nothing to reconcile

    changed = Path(fp).name

    # Throttle: one nudge per changed file per THROTTLE_S.
    st_path = state_dir() / "claim-reconcile-state.json"
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

    # Count passport claims that reference this file (best-effort text match).
    affected = []
    for p in passports:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        hits = sum(1 for ln in text.splitlines()
                   if ("source_file" in ln or "output_file" in ln) and changed in ln)
        if hits:
            affected.append((p.name, hits))
    if not affected:
        return 0

    total = sum(h for _, h in affected)
    where = ", ".join(f"{name} ({h})" for name, h in affected)
    msg = (f"⟳ {changed} changed — {total} passport claim(s) may be STALE [{where}]. "
           f"Run /audit-reproducibility before relying on the affected tables.")
    json.dump({
        "systemMessage": msg,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"A tracked analysis input ({changed}) was just modified. "
                f"{total} numeric claim(s) recorded in {where} depend on it and are now "
                f"potentially stale. Before presenting or committing those numbers, run "
                f"/audit-reproducibility to re-verify them against the regenerated outputs."
            ),
        },
    }, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # fail open
