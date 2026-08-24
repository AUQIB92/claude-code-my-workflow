#!/usr/bin/env python3
"""
render-pdf-preview.py — rasterize a PDF to PNG(s) for visual QA.

Shared rendering utility so agents/skills that need to actually *look* at a
compiled artifact (tikz-reviewer's Pass 6, any "does this actually look
right" verification) don't retype the pymupdf incantation inline. Uses
pymupdf (confirmed pip-installed on this machine — see MEMORY.md), not
poppler/pdftoppm: poppler on this machine ships only pdfinfo/pdftocairo,
not pdftoppm.

Usage:
  python3 scripts/render-pdf-preview.py FILE.pdf [--dpi 150] [--pages 1,3,5] [--out-dir DIR]

  FILE.pdf     Path to the compiled PDF.
  --dpi        Raster resolution (default 150; use 200-300 to check small text).
  --pages      Comma-separated 1-indexed page numbers to render (default: all pages).
  --out-dir    Directory to write PNGs into (default: FILE's own directory).

Output: one PNG path per line on stdout, one per rendered page, named
<basename>_p<N>.png with N 0-indexed (matches the convention already used
by /extract-tikz's tikz_exact_NN.svg naming).

Exit codes:
  0 = rendered successfully (paths printed on stdout)
  2 = usage / input error (file missing, bad --pages, pymupdf import failure)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_pages(spec: str, page_count: int) -> list[int]:
    """Parse a comma-separated 1-indexed page spec into 0-indexed page numbers."""
    out = []
    for tok in spec.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            n = int(tok)
        except ValueError:
            raise ValueError(f"not an integer: {tok!r}")
        if n < 1 or n > page_count:
            raise ValueError(f"page {n} out of range (PDF has {page_count} pages)")
        out.append(n - 1)
    if not out:
        raise ValueError("--pages given but no page numbers parsed")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="path to the PDF to rasterize")
    ap.add_argument("--dpi", type=int, default=150, help="raster DPI (default 150)")
    ap.add_argument("--pages", default=None, help="comma-separated 1-indexed page numbers (default: all)")
    ap.add_argument("--out-dir", default=None, help="output directory (default: a scratch dir under the system temp dir — never the repo)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_file():
        print(f"error: no such file: {pdf_path}", file=sys.stderr)
        return 2

    try:
        import pymupdf
    except ImportError as e:
        print(f"error: pymupdf not importable ({e}) — pip install pymupdf", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir) if args.out_dir else pdf_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"error: failed to open {pdf_path}: {e}", file=sys.stderr)
        return 2

    try:
        if args.pages:
            page_indices = parse_pages(args.pages, len(doc))
        else:
            page_indices = list(range(len(doc)))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    base = pdf_path.stem
    for idx in page_indices:
        page = doc[idx]
        pix = page.get_pixmap(dpi=args.dpi)
        out_path = out_dir / f"{base}_p{idx}.png"
        pix.save(str(out_path))
        print(str(out_path))

    return 0


if __name__ == "__main__":
    sys.exit(main())
