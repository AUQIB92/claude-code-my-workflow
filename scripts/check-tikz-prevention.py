#!/usr/bin/env python3
"""
check-tikz-prevention.py — shared multi-line-aware prevention pre-check.

Invoked by /extract-tikz and /new-diagram as their Step 1 gate.
Reports P3 and P4 violations from tikz-prevention.md.

- P3: bare `scale=X` in a tikzpicture options block without accompanying node
      scaling (`every node/.style={scale=X}` or `transform shape`).
- P4: edge label (`node {...}` attached to a `\\draw`) without a directional
      keyword (`above`, `below`, `left`, `right`, or a compound).

Unlike a line-oriented grep, this handles:
  - Multi-line tikzpicture option blocks: `\\begin{tikzpicture}[\\n scale=0.8\\n]`
  - Multi-line draw commands where `node {...}` is on a different line than `\\draw`.

Usage:
  python3 scripts/check-tikz-prevention.py FILE.tex [FILE2.tex ...]

Exit codes:
  0 = all files pass
  1 = one or more P3/P4 violations (details on stderr)
  2 = usage / input error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DIRECTION_RE = re.compile(r"\b(above|below|left|right)\b")

TIKZPICTURE_OPENER_RE = re.compile(
    r"\\begin\{tikzpicture\}\s*\[(.*?)\]",
    re.DOTALL,
)

DRAW_STATEMENT_RE = re.compile(
    r"\\draw\b(?P<body>.*?);",
    re.DOTALL,
)

NODE_IN_DRAW_RE = re.compile(
    r"\bnode\b(?P<options>\s*\[[^\]]*\])?\s*\{",
    re.DOTALL,
)


def strip_comments(text: str) -> str:
    """Strip TeX line comments so a `%` in prose doesn't hide real violations."""
    out_lines = []
    for line in text.splitlines(keepends=True):
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            i += 1
        out_lines.append(line[:i] + ("\n" if line.endswith("\n") else ""))
    return "".join(out_lines)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_p3(stripped: str) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    for m in TIKZPICTURE_OPENER_RE.finditer(stripped):
        options = m.group(1)
        if re.search(r"\bscale\s*=\s*[0-9.]+", options):
            has_node_scale = bool(
                re.search(r"every\s+node\s*/\s*\.style\s*=\s*\{[^}]*scale\s*=", options)
                or re.search(r"\btransform\s+shape\b", options)
            )
            if not has_node_scale:
                ln = line_of(stripped, m.start())
                snippet = re.sub(r"\s+", " ", options).strip()
                violations.append((ln, f"\\begin{{tikzpicture}}[{snippet}]"))
    return violations


def check_p4(stripped: str) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    for m in DRAW_STATEMENT_RE.finditer(stripped):
        body = m.group("body")
        for n in NODE_IN_DRAW_RE.finditer(body):
            options = n.group("options") or ""
            if not DIRECTION_RE.search(options):
                node_offset = m.start() + n.start()
                ln = line_of(stripped, node_offset)
                snippet_raw = body[n.start() : min(n.end() + 40, len(body))]
                snippet = re.sub(r"\s+", " ", snippet_raw).strip()
                violations.append((ln, f"\\draw ... {snippet}"))
    return violations


def check_file(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"ERROR: cannot read {path}: {e}", file=sys.stderr)
        return 1

    stripped = strip_comments(text)
    p3 = check_p3(stripped)
    p4 = check_p4(stripped)

    if not p3 and not p4:
        return 0

    print(f"\n{path} — prevention violations", file=sys.stderr)
    for ln, snippet in p3:
        print(f"  P3 @ line {ln}: bare scale= without node scaling", file=sys.stderr)
        print(f"      {snippet}", file=sys.stderr)
    for ln, snippet in p4:
        print(f"  P4 @ line {ln}: edge label without directional keyword", file=sys.stderr)
        print(f"      {snippet}", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    rc = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"ERROR: not found: {arg}", file=sys.stderr)
            rc = 2
            continue
        rc = max(rc, check_file(p))

    if rc == 0:
        print(f"OK: {len(sys.argv) - 1} file(s) pass P3+P4 prevention checks.")
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"check-tikz-prevention.py crashed: {e}", file=sys.stderr)
        sys.exit(0)
