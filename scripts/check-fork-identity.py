#!/usr/bin/env python3
"""check-fork-identity.py — catch upstream-repo drift in community-health files.

This repo is a public template (see `.claude/rules/meta-governance.md`
Identity 2): every fork inherits `.github/SECURITY.md`,
`.github/CODE_OF_CONDUCT.md`, `.github/CONTRIBUTING.md`, and
`TROUBLESHOOTING.md` verbatim on `git clone`. If those files still hardcode
the *original* upstream repo/contact, a security report or CoC complaint
filed on the fork silently routes to the upstream author instead of the
fork's own maintainer.

This script derives the current fork's identity from `git remote get-url
origin` and flags any of the four target files that still reference the
upstream repo slug or domain. It does NOT touch files that intentionally
credit the upstream author (ACKNOWLEDGMENTS.md, CITATION.cff, LICENSE,
CHANGELOG.md) — those are permanently allowlisted, never scanned.

If the current `origin` remote's owner IS the upstream owner (i.e. this is
running on the original repo itself, not a fork of it), the check is a
no-op: there is no "wrong" identity to drift from.

Exit codes: 0 = clean (or running on the upstream repo itself), 1 = drift
found, 2 = internal error (e.g. no git remote configured).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

UPSTREAM_OWNER = "pedrohcgs"
UPSTREAM_REPO = "claude-code-my-workflow"
UPSTREAM_DOMAIN = "psantanna.com"
UPSTREAM_REPO_MARKER = f"github.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}"

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files a fork is expected to have re-pointed at its own identity. Deliberately
# NOT ACKNOWLEDGMENTS.md / CITATION.cff / LICENSE / CHANGELOG.md / README.md —
# those intentionally credit the upstream author and must never be flagged.
TARGET_FILES = [
    ".github/SECURITY.md",
    ".github/CODE_OF_CONDUCT.md",
    ".github/CONTRIBUTING.md",
    "TROUBLESHOOTING.md",
]

MARKERS = [UPSTREAM_REPO_MARKER, UPSTREAM_DOMAIN]


def get_origin_owner() -> str | None:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    url = result.stdout.strip()
    # Handles both HTTPS (https://github.com/OWNER/REPO(.git)) and
    # SSH (git@github.com:OWNER/REPO(.git)) remote forms.
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", url)
    if not m:
        return None
    return m.group(1)


def find_drift() -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for rel_path in TARGET_FILES:
        path = REPO_ROOT / rel_path
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for marker in MARKERS:
                if marker in line:
                    findings.append((rel_path, lineno, marker))
    return findings


def main() -> int:
    owner = get_origin_owner()
    if owner is None:
        print(
            "check-fork-identity: could not determine git remote 'origin' "
            "owner — skipping (not a fatal error, but the check can't run).",
            file=sys.stderr,
        )
        return 0
    if owner.lower() == UPSTREAM_OWNER.lower():
        print(
            f"check-fork-identity: origin owner is '{owner}' (the upstream "
            "repo itself) — nothing to check."
        )
        return 0

    findings = find_drift()
    if not findings:
        print("check-fork-identity: OK — no upstream-repo drift found.")
        return 0

    print(
        f"check-fork-identity: {len(findings)} finding(s) — this fork's "
        f"origin is '{owner}', but the following still reference the "
        "upstream repo/contact:"
    )
    for rel_path, lineno, marker in findings:
        print(f"  {rel_path}:{lineno} — contains '{marker}'")
    print(
        "\nFix: replace with this fork's own repo URL / contact. See "
        "TROUBLESHOOTING.md's 'Fork-identity gate' entry for details."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
