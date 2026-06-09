#!/usr/bin/env python3
"""
Check cross-document count consistency for the template's public surfaces.

Prevents the drift pattern that hit PRs #70, #76, #78 — where adding a skill
(agent, rule, hook) updates `.claude/` but leaves stale counts in README,
CLAUDE.md, the guide source, the rendered guide, or the landing page.

Two kinds of check:
  1. COUNT assertions — prose like "13 agents, 27 skills, 21 rules" must
     match the on-disk inventory (the original check).
  2. TABLE-ROW assertions — an enumerative markdown table preceded by a
     `<!-- surface-sync-table: <kind> -->` marker must have exactly one
     data row per item of <kind> on disk. This catches the drift the
     count check misses: e.g. the v1.5.0 peer-review trio that was added
     to `.claude/` but left OUT of the README/CLAUDE.md skills tables for
     three releases (the counts were right; the table rows were stale).

Run via `./scripts/check-surface-sync.sh` pre-commit, or `/commit` will
invoke it automatically.

Exit codes:
    0 — all counts consistent
    1 — drift detected (prints a diff)
    2 — internal error (missing surface file, unreadable directory)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Ground truth: count entries on disk.
GROUND_TRUTH = {
    "skills":       len(list((REPO / ".claude/skills").glob("*/SKILL.md"))),
    "agents":       len(list((REPO / ".claude/agents").glob("*.md"))),
    "rules":        len(list((REPO / ".claude/rules").glob("*.md"))),
    "hooks":        (
        len(list((REPO / ".claude/hooks").glob("*.py"))) +
        len(list((REPO / ".claude/hooks").glob("*.sh")))
    ),
}

# Surfaces to scan + the phrasings that count as "making a claim."
# Each phrasing is a (regex-extracting-the-count, name-of-thing-being-counted) pair.
# The regex MUST have exactly one capture group that yields an integer.
SURFACES = [
    REPO / "README.md",
    REPO / "CLAUDE.md",
    REPO / "guide/workflow-guide.qmd",
    REPO / "docs/workflow-guide.html",
    REPO / "docs/index.html",
    REPO / "templates/skill-template.md",
]

# Phrasings that assert THIS TEMPLATE's counts. We deliberately require
# compound patterns (multiple counts in the same line) or a highly specific
# scaffold ("this template's N") so we don't false-positive on unrelated
# usages like "3 parallel agents", "17 specialized agents" (clo-author's
# count, different template), or "start with 2-3 skills".
#
# Each entry is (regex, ordered list of (group_index, kind)). Group index is
# 1-based. The regex MUST match the compound assertion, not just one count.
COMPOUND_PHRASINGS: list[tuple[str, list[tuple[int, str]]]] = [
    # "13 agents, 27 skills, 21 rules, 6 hooks" (README's <summary>)
    (
        r"(\d+)\s+agents?,\s+(\d+)\s+skills?,\s+(\d+)\s+rules?,\s+(\d+)\s+hooks?",
        [(1, "agents"), (2, "skills"), (3, "rules"), (4, "hooks")],
    ),
    # "13 agents, 27 skills, and 21 rules" (guide's Bottom Line + "full system")
    (
        r"(\d+)\s+agents?,\s+(\d+)\s+skills?,?\s+and\s+(\d+)\s+rules?",
        [(1, "agents"), (2, "skills"), (3, "rules")],
    ),
    # "13 agents, 27 skills, 21 rules" (no 'and', no 'hooks')
    (
        r"(\d+)\s+agents?,\s+(\d+)\s+skills?,\s+(\d+)\s+rules?(?!\s*,)",
        [(1, "agents"), (2, "skills"), (3, "rules")],
    ),
    # og:description: "27 skills, 13 specialized agents, 21 rules"
    (
        r"(\d+)\s+skills?,\s+(\d+)\s+specialized\s+agents?,\s+(\d+)\s+rules?",
        [(1, "skills"), (2, "agents"), (3, "rules")],
    ),
    # Landing page bullet: "27 slash commands + 21 context-aware rules"
    (
        r"(\d+)\s+slash\s+commands?\s*\+\s*(\d+)\s+context-aware\s+rules?",
        [(1, "skills"), (2, "rules")],
    ),
]

# Singular phrasings. These ONLY fire when the match is clearly about this
# template (not attribution, not a generic count). Each must be a scaffold
# specific enough that false positives are unlikely.
SINGULAR_PHRASINGS: list[tuple[str, str]] = [
    # "this template's 27" (prose shortcut in Built-In Skills callout)
    (r"this template's\s+(\d+)\b",                  "skills"),
    # "(N skills for LaTeX..." (templates/skill-template.md trailing note)
    (r"\((\d+)\s+skills?\s+for\b",                  "skills"),
]

# Enumerative-table markers. A surface opts a markdown table into the
# row-count gate by placing this comment immediately before it:
#
#     <!-- surface-sync-table: skills -->
#     | Skill | What It Does |
#     |-------|--------------|
#     | `/compile-latex` | ... |   <- one data row per skill on disk
#
# <kind> must be a key of GROUND_TRUTH. The data-row count (header and the
# `|---|` separator excluded) must equal the on-disk count for that kind.
# Only markdown sources should carry the marker — do NOT add it to the
# rendered .html surfaces (their tables are <table>, not pipe rows).
TABLE_MARKER_RE = re.compile(r"<!--\s*surface-sync-table:\s*([a-z]+)\s*-->")


def _is_table_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def scan_file(path: Path) -> list[tuple[int, str, int, str]]:
    """
    Return [(line_number, kind, asserted_count, raw_match)] for every
    assertion found. `kind` is one of GROUND_TRUTH.keys().
    """
    if not path.exists():
        return []
    hits: list[tuple[int, str, int, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        # Compound assertions: one match yields multiple (group, kind) hits.
        for pattern, group_kinds in COMPOUND_PHRASINGS:
            for m in re.finditer(pattern, line):
                for group_idx, kind in group_kinds:
                    try:
                        n = int(m.group(group_idx))
                    except (ValueError, IndexError):
                        continue
                    hits.append((lineno, kind, n, m.group(0)))
        # Singular assertions: one match, one hit.
        for pattern, kind in SINGULAR_PHRASINGS:
            for m in re.finditer(pattern, line):
                try:
                    n = int(m.group(1))
                except (ValueError, IndexError):
                    continue
                hits.append((lineno, kind, n, m.group(0)))
    return hits


def scan_tables(path: Path) -> list[tuple[int, str, int | None, str]]:
    """
    Find every `<!-- surface-sync-table: <kind> -->` marker and count the
    data rows of the markdown table that immediately follows it.

    Returns [(marker_line_number, kind, data_row_count, marker_raw)].
    `data_row_count` is None when no well-formed table follows the marker.
    """
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    n = len(lines)
    hits: list[tuple[int, str, int | None, str]] = []
    i = 0
    while i < n:
        m = TABLE_MARKER_RE.search(lines[i])
        if not m:
            i += 1
            continue
        kind = m.group(1)
        marker_lineno = i + 1
        marker_raw = lines[i].strip()

        # Advance to the header row: the first pipe-line after the marker,
        # skipping intervening blanks/prose (a heading often sits between).
        j = i + 1
        while j < n and not _is_table_row(lines[j]) and not TABLE_MARKER_RE.search(lines[j]):
            j += 1

        # Need: header pipe-line, then a `|---|` separator, then data rows.
        if (
            j >= n
            or not _is_table_row(lines[j])
            or j + 1 >= n
            or "---" not in lines[j + 1]
        ):
            hits.append((marker_lineno, kind, None, marker_raw))
            i = j + 1
            continue

        k = j + 2  # first data row
        count = 0
        while k < n and _is_table_row(lines[k]):
            count += 1
            k += 1
        hits.append((marker_lineno, kind, count, marker_raw))
        i = k
    return hits


def main() -> int:
    rel = lambda p: p.relative_to(REPO)
    drift: list[str] = []

    # Sanity: every surface file listed must exist.
    missing = [p for p in SURFACES if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: surface file missing: {rel(p)}", file=sys.stderr)
        return 2

    print("Ground truth (counted from disk):")
    for k, v in GROUND_TRUTH.items():
        print(f"  {k:<8} {v}")
    print()

    per_file: dict[Path, list[tuple[int, str, int, str]]] = {}
    for path in SURFACES:
        per_file[path] = scan_file(path)

    for path, hits in per_file.items():
        for lineno, kind, asserted, raw in hits:
            expected = GROUND_TRUTH[kind]
            if asserted != expected:
                drift.append(
                    f"  {rel(path)}:{lineno}  "
                    f"asserts {asserted} {kind} "
                    f"(actual: {expected})  "
                    f"[matched: {raw!r}]"
                )

    # Enumerative-table row-count assertions (marker-driven).
    table_hits = 0
    for path in SURFACES:
        for lineno, kind, count, raw in scan_tables(path):
            table_hits += 1
            if kind not in GROUND_TRUTH:
                drift.append(
                    f"  {rel(path)}:{lineno}  unknown table kind {kind!r} "
                    f"(expected one of {', '.join(sorted(GROUND_TRUTH))})  "
                    f"[marker: {raw!r}]"
                )
                continue
            if count is None:
                drift.append(
                    f"  {rel(path)}:{lineno}  marker {raw!r} is not "
                    f"immediately followed by a well-formed markdown table"
                )
                continue
            expected = GROUND_TRUTH[kind]
            if count != expected:
                drift.append(
                    f"  {rel(path)}:{lineno}  '{kind}' table has {count} "
                    f"data row(s) (actual {kind} on disk: {expected})  "
                    f"[marker: {raw!r}]"
                )

    if drift:
        print("DRIFT DETECTED:", file=sys.stderr)
        for d in drift:
            print(d, file=sys.stderr)
        print(
            f"\nFix by updating the asserted counts, or if the assertion is "
            f"a false positive (e.g., historical CHANGELOG entry), move it "
            f"to a phrasing this script does not match.",
            file=sys.stderr,
        )
        return 1

    total_assertions = sum(len(v) for v in per_file.values())
    print(f"All {total_assertions} count assertions + {table_hits} enumerative-"
          f"table row counts match ground truth across {len(SURFACES)} surfaces.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
