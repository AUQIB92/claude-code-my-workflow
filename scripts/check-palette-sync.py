#!/usr/bin/env python3
"""
check-palette-sync.py — compare palette HEX values (not just names) between
Preambles/header.tex and Quarto/theme-template.scss.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CORE_NAMES = ("primary-blue", "primary-gold", "highlight-yellow", "light-bg", "jet")
SEMANTIC_NAMES = ("positive", "negative", "neutral")
HI_NAMES = ("hi-slate", "hi-green", "hi-red")
EXPECTED = CORE_NAMES + SEMANTIC_NAMES + HI_NAMES


DEFINECOLOR_RE = re.compile(
    r"\\definecolor\{(?P<name>[a-zA-Z0-9_-]+)\}\{HTML\}\{(?P<hex>[0-9A-Fa-f]{6})\}"
)
COLORLET_RE = re.compile(
    r"\\colorlet\{(?P<alias>[a-zA-Z0-9_-]+)\}\{(?P<source>[a-zA-Z0-9_-]+)\}"
)
SCSS_VAR_RE = re.compile(
    r"^\$(?P<name>[a-zA-Z0-9_-]+)\s*:\s*(?P<hex>#[0-9A-Fa-f]{3,8})\b",
    re.MULTILINE,
)
SCSS_CLASS_COLOR_RE = re.compile(
    r"^\s*\.(?P<name>[a-zA-Z0-9_-]+)\s*\{[^}]*?color:\s*(?P<hex>#[0-9A-Fa-f]{3,8})",
    re.MULTILINE | re.DOTALL,
)


def parse_latex(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    colors: dict[str, str] = {}
    for m in DEFINECOLOR_RE.finditer(text):
        colors[m.group("name")] = "#" + m.group("hex").upper()
    for m in COLORLET_RE.finditer(text):
        alias, source = m.group("alias"), m.group("source")
        if source in colors:
            colors[alias] = colors[source]
    return colors


def expand_short_hex(h: str) -> str:
    if len(h) == 4:
        return "#" + "".join(c * 2 for c in h[1:]).upper()
    return h[:7].upper()


def parse_scss(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    colors: dict[str, str] = {}
    for m in SCSS_VAR_RE.finditer(text):
        colors[m.group("name")] = expand_short_hex(m.group("hex"))
    wanted = set(SEMANTIC_NAMES) | set(HI_NAMES)
    for m in SCSS_CLASS_COLOR_RE.finditer(text):
        name = m.group("name")
        if name in wanted and name not in colors:
            colors[name] = expand_short_hex(m.group("hex"))
    return colors


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare LaTeX and SCSS palettes by HEX value.")
    ap.add_argument("--latex", type=Path,
                    default=Path(__file__).resolve().parent.parent / "Preambles" / "header.tex")
    ap.add_argument("--scss", type=Path,
                    default=Path(__file__).resolve().parent.parent / "Quarto" / "theme-template.scss")
    args = ap.parse_args()

    if not args.latex.exists():
        print(f"ERROR: {args.latex} not found.", file=sys.stderr)
        return 2
    if not args.scss.exists():
        print(f"ERROR: {args.scss} not found.", file=sys.stderr)
        return 2

    latex = parse_latex(args.latex)
    scss = parse_scss(args.scss)

    print(f"\nPalette sync check\n  LaTeX: {args.latex}\n  SCSS:  {args.scss}\n")

    failures: list[str] = []
    warnings: list[str] = []

    for name in EXPECTED:
        l_hex = latex.get(name)
        s_hex = scss.get(name)

        if l_hex is None and s_hex is None:
            warnings.append(f"{name} - missing from both")
            continue
        if l_hex is None:
            warnings.append(f"{name} - missing from LaTeX (SCSS: {s_hex})")
            continue
        if s_hex is None:
            warnings.append(f"{name} - missing from SCSS (LaTeX: {l_hex})")
            continue

        if l_hex == s_hex:
            print(f"  OK   {name}: {l_hex}")
        else:
            print(f"  DIFF {name}: LaTeX {l_hex} vs SCSS {s_hex}")
            failures.append(f"{name}: LaTeX {l_hex} vs SCSS {s_hex}")

    print("")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
        print("")

    if failures:
        print("Palette out of sync. Fix HEX values in BOTH files:")
        for f in failures:
            print(f"  - {f}")
        print("")
        return 1

    print("Core palette in sync (names and HEX values agree).\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"check-palette-sync.py crashed: {e}", file=sys.stderr)
        sys.exit(0)
