#!/usr/bin/env python3
"""
Unit tests for scripts/circuit_diagram -- stdlib unittest (no pytest: not
installed under the `python3` this repo's tooling actually invokes; see
quality_reports/plans/is-it-good-idea-groovy-hanrahan.md).

Run: python3 -m unittest tests.test_circuit_diagram -v   (from repo root)

Each circuit test runs the FULL pipeline end-to-end (IR -> validate ->
layout -> render TikZ + SVG -> compile -> validateDiagram) and asserts
zero validation errors and zero visual findings. This is the suite's
actual value: proving the pipeline is correct-by-construction on exactly
the circuit types this session spent hours hand-fixing (Labs/CS401's
gate-level diagrams).
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.circuit_diagram.ir import CircuitSpec, GateSpec, InputSpec, OutputSpec, GateType
from scripts.circuit_diagram.validate import validate_circuit
from scripts.circuit_diagram.pipeline import generate_circuit

XELATEX_AVAILABLE = shutil.which("xelatex") is not None


def _gate(id_, type_, inputs, output, **kw):
    return GateSpec(id=id_, type=GateType(type_), inputs=inputs, output=output, **kw)


class CircuitPipelineTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="circuit_diagram_test_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run(self, spec: CircuitSpec):
        errors = validate_circuit(spec)
        self.assertEqual(errors, [], f"validation errors: {errors}")
        if not XELATEX_AVAILABLE:
            self.skipTest("xelatex not on PATH in this environment")
        result = generate_circuit(spec, self._tmp)
        self.assertTrue(result.ok, f"pipeline failed: errors={result.validation_errors} "
                                    f"findings={result.visual_findings} log={result.compile_log[-500:]}")
        self.assertEqual(result.visual_findings, [])
        return result

    # -- primitive gates --

    def test_not(self):
        spec = CircuitSpec(
            inputs=[InputSpec("a")],
            gates=[_gate("n1", "NOT", ["a"], "OUT")],
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    def test_and(self):
        spec = CircuitSpec(
            inputs=[InputSpec("a"), InputSpec("b")],
            gates=[_gate("g1", "AND", ["a", "b"], "OUT")],
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    def test_or(self):
        spec = CircuitSpec(
            inputs=[InputSpec("a"), InputSpec("b")],
            gates=[_gate("g1", "OR", ["a", "b"], "OUT")],
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    def test_xor(self):
        spec = CircuitSpec(
            inputs=[InputSpec("a"), InputSpec("b")],
            gates=[_gate("g1", "XOR", ["a", "b"], "OUT")],
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    # -- composite circuits (built from primitives, matching the user's
    # own JSON example convention -- this IR has no monolithic "ADDER"
    # gate with two outputs, since GateSpec supports exactly one `output`
    # per gate, same as the schema's own worked example) --

    def test_half_adder(self):
        spec = CircuitSpec(
            name="half_adder",
            inputs=[InputSpec("a"), InputSpec("b")],
            gates=[
                _gate("xor1", "XOR", ["a", "b"], "SUM"),
                _gate("and1", "AND", ["a", "b"], "CARRY"),
            ],
            outputs=[OutputSpec("SUM"), OutputSpec("CARRY")],
        )
        self._run(spec)

    def test_full_adder(self):
        spec = CircuitSpec(
            name="full_adder",
            inputs=[InputSpec("a"), InputSpec("b"), InputSpec("cin")],
            gates=[
                _gate("xor1", "XOR", ["a", "b"], "s1"),
                _gate("and1", "AND", ["a", "b"], "c1"),
                _gate("xor2", "XOR", ["s1", "cin"], "SUM"),
                _gate("and2", "AND", ["s1", "cin"], "c2"),
                _gate("or1", "OR", ["c1", "c2"], "CARRY"),
            ],
            outputs=[OutputSpec("SUM"), OutputSpec("CARRY")],
        )
        self._run(spec)

    def test_mux_2to1(self):
        # out = (a AND NOT sel) OR (b AND sel) -- built from primitives,
        # matching Labs/CS401/lab-1-boolean-logic.tex's fig:mux-from-gates
        spec = CircuitSpec(
            name="mux2to1",
            inputs=[InputSpec("a"), InputSpec("b"), InputSpec("sel")],
            gates=[
                _gate("n1", "NOT", ["sel"], "nsel"),
                _gate("and1", "AND", ["a", "nsel"], "p1"),
                _gate("and2", "AND", ["b", "sel"], "p2"),
                _gate("or1", "OR", ["p1", "p2"], "OUT"),
            ],
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    def test_mux_4to1(self):
        # 4:1 mux from three 2:1 muxes (standard composition)
        def mux2(prefix, a, b, sel, out, gates):
            gates.append(_gate(f"{prefix}_n", "NOT", [sel], f"{prefix}_nsel"))
            gates.append(_gate(f"{prefix}_a1", "AND", [a, f"{prefix}_nsel"], f"{prefix}_p1"))
            gates.append(_gate(f"{prefix}_a2", "AND", [b, sel], f"{prefix}_p2"))
            gates.append(_gate(f"{prefix}_or", "OR", [f"{prefix}_p1", f"{prefix}_p2"], out))

        gates: list[GateSpec] = []
        mux2("m0", "i0", "i1", "s0", "lo", gates)
        mux2("m1", "i2", "i3", "s0", "hi", gates)
        mux2("m2", "lo", "hi", "s1", "OUT", gates)
        spec = CircuitSpec(
            name="mux4to1",
            inputs=[InputSpec("i0"), InputSpec("i1"), InputSpec("i2"), InputSpec("i3"),
                    InputSpec("s0"), InputSpec("s1")],
            gates=gates,
            outputs=[OutputSpec("OUT")],
        )
        self._run(spec)

    def test_alu_zero_negative_flags(self):
        # ALU subcomponent, scoped per the plan: zero-flag (NOR-reduce 2
        # representative bits) and negative-flag (sign-bit tap), not a
        # full 16-bit ALU.
        spec = CircuitSpec(
            name="alu_flags",
            inputs=[InputSpec("out0"), InputSpec("out1"), InputSpec("sign")],
            gates=[
                _gate("or1", "OR", ["out0", "out1"], "any_set"),
                _gate("n1", "NOT", ["any_set"], "zr"),
                _gate("n2", "NOT", ["sign"], "not_sign"),  # ng = sign bit directly; not_sign kept for symmetry
            ],
            outputs=[OutputSpec("zr"), OutputSpec(signal="sign", label="ng")],
        )
        self._run(spec)

    # -- IR / validation edge cases (no compile needed) --

    def test_validate_catches_undefined_signal(self):
        spec = CircuitSpec(
            inputs=[InputSpec("a")],
            gates=[_gate("g1", "AND", ["a", "ghost"], "OUT")],
            outputs=[OutputSpec("OUT")],
        )
        errors = validate_circuit(spec)
        self.assertTrue(any(e.code == "UNDEFINED_SIGNAL" for e in errors))

    def test_validate_catches_combinational_cycle(self):
        spec = CircuitSpec(
            inputs=[],
            gates=[
                _gate("g1", "AND", ["x", "b"], "a"),
                _gate("g2", "AND", ["a", "b"], "x"),
            ],
            outputs=[OutputSpec("x")],
        )
        errors = validate_circuit(spec)
        self.assertTrue(any(e.code == "COMBINATIONAL_CYCLE" for e in errors))

    def test_feedback_edge_is_allowed(self):
        # Mirrors Labs/CS401/lab-3's Bit chip: a feedback loop explicitly
        # marked, must NOT be flagged as an illegal cycle.
        spec = CircuitSpec(
            inputs=[InputSpec("load"), InputSpec("din")],
            gates=[
                _gate("mux_out", "OR", ["din", "load"], "q", feedback_inputs=["load"]),
            ],
            outputs=[OutputSpec("q")],
        )
        # "load" isn't actually q's own feedback here (contrived), so
        # exercise the real self-loop shape instead:
        spec2 = CircuitSpec(
            inputs=[InputSpec("din")],
            gates=[
                _gate("g1", "OR", ["din", "q"], "q", feedback_inputs=["q"]),
            ],
            outputs=[OutputSpec("q")],
        )
        errors = validate_circuit(spec2)
        self.assertFalse(any(e.code == "COMBINATIONAL_CYCLE" for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
