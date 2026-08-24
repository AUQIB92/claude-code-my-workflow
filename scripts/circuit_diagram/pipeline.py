"""
generateCircuit: orchestrates the full pipeline with a targeted
self-correction loop.

    IR -> validate -> [FAIL: return errors, do not proceed]
    IR -> layout -> render (tikz + svg) -> compile
      [compile FAIL] -> compile.py's own repair loop (max 5)
      [compile OK] -> rasterize -> validateDiagram
        [FAIL] -> widen the offending layer's spacing -> re-render -> recompile -> re-validate
        [PASS] -> done

Layout adjustment is targeted (widen only the layer a finding pointed at),
never a full re-layout -- mirrors this session's actual hand-fix pattern
(widen one rail's pitch, not rescale the whole diagram). Per the pipeline
contract: never regenerate the Circuit IR itself here -- only validate()
failures do that (by returning control to the caller), matching "do not
regenerate the logical circuit unless the Circuit IR itself is invalid."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .ir import CircuitSpec
from .validate import validate_circuit, ValidationError
from .layout import layout_circuit, Layout
from .render_tikz import render_tikz
from .render_svg import render_svg
from .compile import compile_tikz, CompileResult
from .visual_validate import validate_diagram, VisualFinding

MAX_VISUAL_REPAIR_ROUNDS = 5
SPACING_WIDEN_STEP = 0.5


@dataclass
class PipelineResult:
    ok: bool
    validation_errors: list[ValidationError] = field(default_factory=list)
    visual_findings: list[VisualFinding] = field(default_factory=list)
    tikz_source: str | None = None
    svg_source: str | None = None
    pdf_path: str | None = None
    compile_log: str = ""
    rounds: int = 0


def generate_circuit(spec: CircuitSpec, out_dir: str | Path) -> PipelineResult:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = spec.name or "circuit"

    errors = validate_circuit(spec)
    if errors:
        return PipelineResult(ok=False, validation_errors=errors)

    layout: Layout = layout_circuit(spec)

    for round_idx in range(1, MAX_VISUAL_REPAIR_ROUNDS + 1):
        tikz_src = render_tikz(spec, layout)
        svg_src = render_svg(spec, layout)
        tex_path = out_dir / f"{name}.tex"
        (out_dir / f"{name}.svg").write_text(svg_src, encoding="utf-8")

        compiled: CompileResult = compile_tikz(tex_path, tikz_src)
        if not compiled.ok:
            return PipelineResult(
                ok=False, tikz_source=tikz_src, svg_source=svg_src,
                compile_log=compiled.log, rounds=round_idx,
            )

        findings = validate_diagram(str(compiled.pdf_path))
        if not findings:
            return PipelineResult(
                ok=True, tikz_source=tikz_src, svg_source=svg_src,
                pdf_path=str(compiled.pdf_path), compile_log=compiled.log,
                rounds=round_idx,
            )

        # Targeted repair: widen every layer at/after the layer nearest the
        # first finding's x-position, then re-render and re-check.
        loc = findings[0].location
        if loc is None:
            return PipelineResult(
                ok=False, tikz_source=tikz_src, svg_source=svg_src,
                visual_findings=findings, pdf_path=str(compiled.pdf_path),
                compile_log=compiled.log, rounds=round_idx,
            )
        px = loc[0]
        approx_layer = round(px / (layout.horizontal_spacing * 28.3465))
        layout.widen_gap(approx_layer, SPACING_WIDEN_STEP)

    return PipelineResult(
        ok=False, tikz_source=tikz_src, svg_source=svg_src,
        visual_findings=findings, pdf_path=str(compiled.pdf_path),
        compile_log=compiled.log, rounds=MAX_VISUAL_REPAIR_ROUNDS,
    )
