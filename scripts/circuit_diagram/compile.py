"""
Compile harness: xelatex, matching this repo's explicit, repeatedly-stated
convention ("Always use XeLaTeX, never pdflatex" -- compile-latex/SKILL.md)
even though pdflatex/lualatex are also reachable in this environment.

Because gate placement and wire routing are always machine-generated from
a validated IR (see render_tikz.py's anchor-only rule), compile failures
should be rare and structural -- a label needing LaTeX escaping, not a
malformed circuit. The repair loop here fixes the RENDERING ARTIFACT only,
never the circuit logic, per the pipeline's own contract.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

MAX_REPAIR_ATTEMPTS = 5

_LATEX_ESCAPE = {
    "_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$",
}


@dataclass
class CompileResult:
    ok: bool
    pdf_path: Path | None
    log: str
    attempts: int


def escape_label_text(text: str) -> str:
    """Repair helper: escape LaTeX special characters that are legal in a
    circuit signal name but not in raw LaTeX text (e.g. `sel_reg` -> the
    `_` needs escaping outside math mode)."""
    out = []
    for ch in text:
        out.append(_LATEX_ESCAPE.get(ch, ch))
    return "".join(out)


def _run_xelatex(tex_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["xelatex", "-interaction=nonstopmode", tex_path.name],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        timeout=60,
    )


def compile_tikz(tex_path: str | Path, tex_source: str | None = None) -> CompileResult:
    """Compile `tex_path` (writing `tex_source` to it first if given).
    On failure, attempts a bounded number of mechanical repairs to the
    .tex source itself (escaping only) and recompiles."""
    tex_path = Path(tex_path)
    if tex_source is not None:
        tex_path.write_text(tex_source, encoding="utf-8")

    log = ""
    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
        try:
            proc = _run_xelatex(tex_path)
        except FileNotFoundError:
            return CompileResult(False, None, "xelatex not found on PATH", attempt)
        except subprocess.TimeoutExpired:
            return CompileResult(False, None, "xelatex timed out", attempt)
        log = proc.stdout + proc.stderr
        pdf_path = tex_path.with_suffix(".pdf")
        if proc.returncode == 0 and pdf_path.is_file():
            return CompileResult(True, pdf_path, log, attempt)

        # Mechanical repair: an unescaped `_`/`&`/`%`/`#` in plain text is
        # the only class of failure this harness attempts to fix, since
        # every coordinate/anchor in the source is machine-generated and
        # already known-correct.
        if "Misplaced alignment tab" in log or "Undefined control sequence" in log:
            source = tex_path.read_text(encoding="utf-8")
            repaired = re.sub(r"(?<!\\)([_&%#])", r"\\\1", source)
            if repaired == source:
                break  # nothing left to try
            tex_path.write_text(repaired, encoding="utf-8")
            continue
        break  # not a repairable failure class

    return CompileResult(False, None, log, MAX_REPAIR_ATTEMPTS)
