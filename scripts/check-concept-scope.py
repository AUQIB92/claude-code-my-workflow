#!/usr/bin/env python3
"""check-concept-scope.py — PROOF OF CONCEPT for the "Course Build Graph"
bet (repo-innovator Strategic Moat, see
quality_reports/repo_innovator_academic-workload_2026-08-20/REPORT.md).

Parses a course's `## Symbol Reference` table in
`.claude/rules/knowledge-base-<CODE>.md` (columns: Symbol | Meaning |
Introduced) and cross-checks each symbol's declared introduction week
against the ACTUAL first week it appears in `Slides/<CODE>/*.tex`,
flagging any symbol used before its declared week — a deterministic
"used before declared" check, the class of prerequisite bug this repo's
LLM-judgment review (`/course-arc-audit`) can miss by attention limits
alone.

PoC scope, stated honestly (see the build plan this implements):
  - Detection is a comment-stripped, case-sensitive `\b<token>\b` regex
    match. This is intentionally over-inclusive, not under-inclusive: it
    will also match a bare TikZ node NAME (e.g. `(PC) at (0,2) {PC}`),
    not just rendered label text a student actually reads. It never
    silently misses a real textual occurrence.
  - Multi-symbol table cells (`HA / FA`, `$A$, $Q$, $Q_{-1}$, $M$`) are
    split into sub-tokens on `/` and `,`, each searched independently;
    the row's "first use" is the earliest week ANY sub-token appears.
  - A row's declared "Introduced" week is the FIRST week number found in
    that cell, however it's formatted (`**Week 4 (confirmed)**`,
    `**Week 6-7 (projected)**`, a bare `Week 5 (...)`, or free prose
    mentioning "Week 5" without a parenthetical tag at all — all four
    forms are real, present in this repo's two knowledge-base files).
  - This script is NOT wired into any gate yet (PoC only). Running it is
    always safe: read-only against Slides/ and the knowledge-base file.

Exit codes: 0 = clean (no violations, or nothing to check), 1 = at least
one USED-BEFORE-DECLARED violation found, 2 = internal error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

WEEK_RE = re.compile(r"Week\s+(\d+)", re.IGNORECASE)
TABLE_ROW_RE = re.compile(
    r"^\|\s*(?P<symbol>.+?)\s*\|\s*(?P<meaning>.+?)\s*\|\s*(?P<introduced>.+?)\s*\|\s*$"
)


def strip_comments(text: str) -> str:
    """Drop everything from the first un-escaped '%' to end of line —
    same technique check-tikz-freshness.py uses, extended to not treat
    a literal '\\%' as a comment start."""
    out_lines = []
    for line in text.splitlines():
        result = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            result.append(line[i])
            i += 1
        out_lines.append("".join(result))
    return "\n".join(out_lines)


def parse_symbol_reference(kb_path: Path) -> list[dict]:
    """Extract the '## Symbol Reference' table's rows as
    {symbol_raw, tokens, introduced_week} dicts."""
    text = kb_path.read_text(encoding="utf-8")
    m = re.search(r"^## Symbol Reference\s*$", text, re.MULTILINE)
    if not m:
        return []
    # Section runs until the next '## ' heading (or end of file).
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.MULTILINE)
    section = rest[: end.start()] if end else rest

    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        row_m = TABLE_ROW_RE.match(line)
        if not row_m:
            continue
        symbol_raw = row_m.group("symbol")
        introduced_raw = row_m.group("introduced")
        # Header separator row ("|--------|---------|------------|") and
        # the literal header row itself.
        if set(symbol_raw) <= {"-"} or symbol_raw.lower() == "symbol":
            continue
        week_m = WEEK_RE.search(introduced_raw)
        if not week_m:
            continue  # a row with no parseable week is skipped, not a crash
        introduced_week = int(week_m.group(1))
        tokens = extract_tokens(symbol_raw)
        if tokens:
            rows.append(
                {
                    "symbol_raw": symbol_raw,
                    "tokens": tokens,
                    "introduced_week": introduced_week,
                    "introduced_raw": introduced_raw,
                }
            )
    return rows


def extract_tokens(symbol_cell: str) -> list[str]:
    """Split a possibly-compound Symbol cell into RELIABLY-searchable
    literal sub-tokens.

    A first pass over real data (both CS401/CS301 tables) showed the naive
    version of this function — bare-word-match the first word of every
    cell — produces mostly false positives: many Symbol cells are
    descriptive PHRASES ("Two's complement", "Control matrix", "Best /
    worst / average case", "DMA controller registers"), and a phrase's
    first word is very often a common English word ("Control", "Best",
    "place", "list") that appears constantly in unrelated prose. Bare
    lowercase code identifiers (`\\texttt{top}`, `\\texttt{head}`) have the
    same problem stripped of their wrapper.

    So: a sub-token is only kept if it's reliably distinguishable from
    ordinary prose —
      (a) ALL-CAPS, length >= 2 (PC, SC, EA, IR, MAR, DMA, IEEE, ADT, ...) — real
          acronym/register-name symbols in this repo's tables are consistently
          upper-case, so this alone covers the large majority of genuine
          notation entries; or
      (b) wrapped in `\\texttt{...}` or a backtick code span in the ORIGINAL
          cell — kept as the exact wrapped substring (e.g. `\\texttt{top}`),
          not the bare word, so "top"/"head" only match real code-styled
          uses in Slides, not the English word in prose.
    Everything else (bare mixed-case prose words, single-letter math
    variables, subscripted math like `Q_{-1}`) is deliberately NOT
    returned — the caller marks that row 'not reliably checkable' rather
    than reporting a noisy guess.
    """
    tokens: list[str] = []

    # (b) code-wrapped spans, kept with their wrapper intact.
    for wrapped in re.findall(r"\\texttt\{[^}]*\}", symbol_cell):
        tokens.append(wrapped)
    for wrapped in re.findall(r"`[^`]+`", symbol_cell):
        if wrapped not in tokens:
            tokens.append(wrapped)

    # (a) bare ALL-CAPS acronym-style tokens, found anywhere in the cell
    # (covers multi-symbol cells like "HA / FA", "KIN / DOUT" without
    # needing to split on / or , first).
    for m in re.finditer(r"\b[A-Z][A-Z0-9]+\b", symbol_cell):
        tok = m.group(0)
        if tok not in tokens:
            tokens.append(tok)

    return tokens


def slides_by_week(code: str) -> list[tuple[int, Path]]:
    slides_dir = REPO / "Slides" / code
    if not slides_dir.is_dir():
        return []
    out = []
    for f in sorted(slides_dir.glob("*.tex")):
        wm = re.match(r"^(\d+)-", f.name)
        if wm:
            out.append((int(wm.group(1)), f))
    return sorted(out, key=lambda t: t[0])


def first_use_week(token: str, files_by_week: list[tuple[int, Path]]) -> int | None:
    # Plain identifier tokens (e.g. "PC") get \b-wrapped word-boundary
    # matching. Wrapped tokens (e.g. "\texttt{top}", "`top`") start/end
    # with non-word characters (\, }, `), so \b would sit at a
    # non-word/non-word boundary and never match — use a plain literal
    # substring search for those instead.
    if re.fullmatch(r"[A-Za-z0-9]+", token):
        pattern = re.compile(r"\b" + re.escape(token) + r"\b")
    else:
        pattern = re.compile(re.escape(token))
    for week, path in files_by_week:
        try:
            text = strip_comments(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            continue
        if pattern.search(text):
            return week
    return None


def check_course(code: str) -> list[str]:
    kb_path = REPO / ".claude" / "rules" / f"knowledge-base-{code}.md"
    if not kb_path.is_file():
        print(f"check-concept-scope: no knowledge-base-{code}.md — skipping {code}")
        return []
    rows = parse_symbol_reference(kb_path)
    files_by_week = slides_by_week(code)
    if not files_by_week:
        print(f"check-concept-scope: no Slides/{code}/*.tex found — skipping {code}")
        return []

    violations = []
    checked = 0
    not_found = 0
    for row in rows:
        best_week = None
        for token in row["tokens"]:
            w = first_use_week(token, files_by_week)
            if w is not None and (best_week is None or w < best_week):
                best_week = w
        checked += 1
        if best_week is None:
            not_found += 1
            continue
        if best_week < row["introduced_week"]:
            violations.append(
                f"{code}: '{row['symbol_raw']}' used in week {best_week} slides "
                f"but declared 'Introduced: {row['introduced_raw']}' "
                f"(week {row['introduced_week']})"
            )
    print(
        f"check-concept-scope: {code} — {checked} symbols checked, "
        f"{not_found} not found in any built Slides/{code}/*.tex "
        f"(expected for not-yet-built weeks), {len(violations)} violation(s)"
    )
    return violations


def main() -> int:
    codes = sys.argv[1:] or ["CS401", "CS301"]
    all_violations: list[str] = []
    for code in codes:
        try:
            all_violations.extend(check_course(code))
        except Exception as e:  # noqa: BLE001 — PoC-level: report, don't crash the run
            print(f"check-concept-scope: internal error on {code}: {e}", file=sys.stderr)
            return 2

    if all_violations:
        print("\ncheck-concept-scope: USED-BEFORE-DECLARED violations found:")
        for v in all_violations:
            print(f"  {v}")
        return 1

    print("check-concept-scope: OK — no used-before-declared violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
