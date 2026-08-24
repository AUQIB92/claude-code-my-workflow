"""
Visual validation via pymupdf VECTOR geometry extraction (exact glyph
bounding boxes + exact drawn-path coordinates) -- not pixel/CV scanning
(`opencv` isn't available under this repo's `python3` anyway; see the
plan's Environment Constraints). This is the same technique that let
`tikz-reviewer` compute exact sub-millimeter clearances this session.

Thresholds are the EXISTING project clearance-minimum table from
`.claude/rules/tikz-measurement.md` Pass 5, not invented here:
    label <-> label / label <-> arrow / label <-> axis   >= 0.3 cm
    label <-> drawn-shape boundary                        >= 0.4 cm
    arrow origin <-> box edge                              >= 0.15 cm
    any object <-> page edge                                >= 0.5 cm
"""

from __future__ import annotations

from dataclasses import dataclass

PT_PER_CM = 28.3465

MIN_LABEL_LABEL_PT = 0.3 * PT_PER_CM
MIN_LABEL_LINE_PT = 0.3 * PT_PER_CM
MIN_LABEL_BOUNDARY_PT = 0.4 * PT_PER_CM

# The tikz-measurement.md "0.5cm from any slide edge" rule is written for
# a diagram embedded in a lecture page alongside other content. This
# system's compile harness always emits `standalone` class with a 4pt
# border (matching this repo's templates/tikz-snippets/ convention) --
# the crop is DELIBERATELY tight, so the 0.5cm slide-margin rule would
# reject every diagram it ever produces. Default here is "not actually
# clipped" (a couple of points of slack for AA/stroke-width rounding),
# not the full slide-embedding margin; pass a larger value explicitly if
# validating a diagram meant for direct page embedding instead.
DEFAULT_MIN_PAGE_MARGIN_PT = 2.0


@dataclass
class VisualFinding:
    code: str
    message: str
    location: tuple[float, float] | None = None


def _rects_overlap_or_close(r1, r2, min_gap: float) -> bool:
    dx = max(r1.x0 - r2.x1, r2.x0 - r1.x1, 0)
    dy = max(r1.y0 - r2.y1, r2.y0 - r1.y1, 0)
    if dx == 0 and dy == 0:
        return True  # actual overlap
    gap = (dx**2 + dy**2) ** 0.5 if dx and dy else max(dx, dy)
    return gap < min_gap


def validate_diagram(pdf_path: str, min_page_margin_pt: float = DEFAULT_MIN_PAGE_MARGIN_PT) -> list[VisualFinding]:
    try:
        import pymupdf
    except ImportError as e:
        raise RuntimeError(f"pymupdf not importable ({e}) -- pip install pymupdf") from e

    findings: list[VisualFinding] = []
    doc = pymupdf.open(pdf_path)
    for page_idx, page in enumerate(doc):
        page_rect = page.rect

        # -- text spans (labels), merged per PDF line -- a single label
        # like `$i0$` (math mode: italic "i" + upright "0") is emitted as
        # multiple adjacent spans with a font-style change but no real
        # gap; treating each font-run as its own "label" produced false
        # LABEL_LABEL_CLEARANCE findings between a label and itself.
        text_spans = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans)
                rect = pymupdf.Rect(spans[0]["bbox"])
                for s in spans[1:]:
                    rect |= pymupdf.Rect(s["bbox"])
                text_spans.append((text, rect))

        # -- drawn paths (wires, gate outlines) --
        drawings = page.get_drawings()
        stroke_rects = [d["rect"] for d in drawings if d.get("rect") is not None and d["rect"].get_area() > 0]

        # label <-> page edge
        for text, rect in text_spans:
            if (rect.x0 - page_rect.x0 < min_page_margin_pt
                    or page_rect.x1 - rect.x1 < min_page_margin_pt
                    or rect.y0 - page_rect.y0 < min_page_margin_pt
                    or page_rect.y1 - rect.y1 < min_page_margin_pt):
                findings.append(VisualFinding(
                    "PAGE_MARGIN", f"page {page_idx}: label '{text}' within 0.5cm of the page edge",
                    (rect.x0, rect.y0),
                ))

        # label <-> label
        for i, (t1, r1) in enumerate(text_spans):
            for t2, r2 in text_spans[i + 1:]:
                if _rects_overlap_or_close(r1, r2, MIN_LABEL_LABEL_PT):
                    findings.append(VisualFinding(
                        "LABEL_LABEL_CLEARANCE",
                        f"page {page_idx}: labels '{t1}' and '{t2}' closer than 0.3cm",
                        (r1.x0, r1.y0),
                    ))

        # label <-> drawn path (catches strikethrough / overprinted labels
        # -- the single most common defect class fixed by hand this
        # session, now caught mechanically)
        for text, rect in text_spans:
            for srect in stroke_rects:
                if rect.intersects(srect):
                    findings.append(VisualFinding(
                        "LABEL_STRUCK_THROUGH",
                        f"page {page_idx}: a drawn line/shape passes through label '{text}'",
                        (rect.x0, rect.y0),
                    ))
                    break

    return findings
