#!/usr/bin/env python3
"""
Check that every extracted TikZ diagram (Figures/<CODE>/<lecture>/extract_tikz.tex)
still matches the TikZ blocks in its Beamer source (Slides/<CODE>/<lecture>.tex).

Closes a real gap: single-source-of-truth.md's "TikZ Freshness Protocol"
describes this exact check as mandatory, but nothing enforced it. A Beamer
diagram got fixed (a label/border overlap) while its Quarto-embedded SVG kept
the old, broken coordinate — silently, because the extraction source had
drifted and nothing caught it. This script is the mechanical version of the
diff a human did by hand to find that bug.

What it checks, per lecture with BOTH a Beamer source and an extraction dir:
  - Same number of \\begin{tikzpicture}...\\end{tikzpicture} blocks.
  - Each block matches its counterpart byte-for-byte after (a) stripping
    comment-only lines and (b) collapsing whitespace — i.e. the actual
    TikZ content, not incidental formatting/comment differences.

A lecture with no extract_tikz.tex is skipped (not every lecture has been
through /extract-tikz — that is not an error, just not applicable).

Run via ./scripts/check-tikz-freshness.sh (chained into check-surface-sync.sh),
or /commit invokes it automatically as part of the pre-commit surface-sync gate.

Exit codes:
    0 - all extraction sources fresh (or no lectures have one)
    1 - drift detected (prints a diff)
    2 - internal error
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def strip_comments(text: str) -> str:
    """Drop pure-comment lines (leading %, ignoring whitespace)."""
    return "\n".join(
        line for line in text.split("\n") if not re.match(r"^\s*%", line)
    )


def extract_tikz_blocks(path: Path) -> list[str]:
    """Return every \\begin{tikzpicture}...\\end{tikzpicture} block, in order."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  ERROR: cannot read {path}: {e}", file=sys.stderr)
        return []
    blocks = []
    start = 0
    begin_tag, end_tag = r"\begin{tikzpicture}", r"\end{tikzpicture}"
    while True:
        i = text.find(begin_tag, start)
        if i == -1:
            break
        j = text.find(end_tag, i)
        if j == -1:
            print(f"  WARNING: unclosed tikzpicture in {path} at offset {i}", file=sys.stderr)
            break
        blocks.append(text[i : j + len(end_tag)])
        start = j + 1
    return blocks


def normalize(block: str) -> str:
    return re.sub(r"\s+", " ", strip_comments(block)).strip()


def find_lecture_pairs() -> list[tuple[str, Path, Path]]:
    """
    Return (label, slides_path, extract_path) for every lecture that has both
    a Beamer source under Slides/ and an extraction dir under Figures/ with
    the same <CODE>/<lecture> nesting.
    """
    pairs = []
    slides_dir = REPO / "Slides"
    figures_dir = REPO / "Figures"
    if not slides_dir.is_dir() or not figures_dir.is_dir():
        return pairs

    for tex_path in sorted(slides_dir.glob("**/*.tex")):
        rel = tex_path.relative_to(slides_dir)
        lecture_stem = rel.stem  # e.g. "01-foundations-pointers-adt"
        # Course-qualified (Slides/<CODE>/<lecture>.tex) vs course-less
        # (Slides/<lecture>.tex) decks both map onto Figures/ the same way
        # extract-tikz's own convention does: Figures/<...same nesting.../>.
        extract_path = figures_dir / rel.parent / lecture_stem / "extract_tikz.tex"
        if extract_path.is_file():
            label = str(rel.with_suffix(""))
            pairs.append((label, tex_path, extract_path))
    return pairs


def check_pair(label: str, slides_path: Path, extract_path: Path) -> list[str]:
    """Return a list of human-readable drift descriptions (empty = fresh)."""
    findings = []
    slides_blocks = extract_tikz_blocks(slides_path)
    extract_blocks = extract_tikz_blocks(extract_path)

    if len(slides_blocks) != len(extract_blocks):
        findings.append(
            f"{label}: block count mismatch — Slides has {len(slides_blocks)}, "
            f"extraction has {len(extract_blocks)}. Re-run /extract-tikz."
        )
        return findings

    for idx, (s, e) in enumerate(zip(slides_blocks, extract_blocks)):
        if normalize(s) != normalize(e):
            findings.append(
                f"{label}: block {idx} has drifted — the extraction source "
                f"({extract_path.relative_to(REPO)}) no longer matches "
                f"{slides_path.relative_to(REPO)}. Re-run /extract-tikz."
            )
    return findings


def main() -> int:
    pairs = find_lecture_pairs()
    if not pairs:
        print("check-tikz-freshness: no lectures with both a Beamer source and an extract_tikz.tex — nothing to check.")
        return 0

    all_findings: list[str] = []
    for label, slides_path, extract_path in pairs:
        all_findings.extend(check_pair(label, slides_path, extract_path))

    if all_findings:
        print(f"check-tikz-freshness: DRIFT DETECTED ({len(all_findings)} finding(s)):")
        for f in all_findings:
            print(f"  {f}")
        print(
            "\nFix by re-running /extract-tikz for each affected lecture, or if the "
            "assertion is a false positive, check whether the two files use different "
            "comment styles this script doesn't normalize."
        )
        return 1

    print(f"OK: {len(pairs)} lecture(s) with extracted TikZ are fresh (Slides matches Figures/.../extract_tikz.tex).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
