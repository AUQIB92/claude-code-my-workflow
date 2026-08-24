"""
circuit_diagram — deterministic logic-gate circuit diagram generation.

Natural-language circuit request -> Circuit IR -> validation -> automatic
DAG layout -> TikZ/SVG generation -> compilation -> visual validation ->
self-correction. No coordinate in the generated TikZ/SVG is ever guessed:
gate placement comes from layout.layoutCircuit(); every wire terminates at
a named gate anchor (never a hand-computed pin offset).

Public surface (mirrors the 7 pipeline functions):
    generateCircuit   -- pipeline.generate_circuit
    validateCircuit   -- validate.validate_circuit
    layoutCircuit     -- layout.layout_circuit
    renderTikz        -- render_tikz.render_tikz
    renderSvg         -- render_svg.render_svg
    compileTikz       -- compile.compile_tikz
    validateDiagram   -- visual_validate.validate_diagram

See quality_reports/plans/is-it-good-idea-groovy-hanrahan.md for the design
rationale (this exists because every bug found fixing Labs/CS401's TikZ
gate diagrams this session traced to a hand-computed pin coordinate drifting
out of sync with the circuits.logic.US library's real, undocumented
geometry).
"""

from __future__ import annotations

from .ir import CircuitSpec, GateSpec, InputSpec, OutputSpec, GateType
from .validate import validate_circuit, ValidationError
from .layout import layout_circuit, Layout
from .render_tikz import render_tikz
from .render_svg import render_svg
from .compile import compile_tikz, CompileResult
from .visual_validate import validate_diagram, VisualFinding
from .pipeline import generate_circuit, PipelineResult

__all__ = [
    "CircuitSpec", "GateSpec", "InputSpec", "OutputSpec", "GateType",
    "validate_circuit", "ValidationError",
    "layout_circuit", "Layout",
    "render_tikz",
    "render_svg",
    "compile_tikz", "CompileResult",
    "validate_diagram", "VisualFinding",
    "generate_circuit", "PipelineResult",
]
