"""
Per-gate-type registry: pin count, circuits.logic.US style name, and
measured bounding-box geometry.

Every number below was measured, not guessed: a probe .tex placed each
gate type with `anchor=input 1` and a tiny filled dot on every named
anchor (`.input 1`, `.input 2`, `.output`), compiled with xelatex, and the
dot coordinates were read back from the compiled PDF's vector geometry
with pymupdf (the same technique `tikz-reviewer`'s Pass 6 uses). This is
the "bootstrap step" the design plan calls for -- the opposite of this
session's actual bug pattern (a coordinate assumed to match a pin
position, that silently drifted out of sync with the library).

Confirmed identical across every 2-input gate (AND/OR/XOR/NAND/NOR/XNOR):
    PIN_PITCH   = 0.205    (input 2 is this far *below* input 1)
    OUTPUT_DY   = -0.1025  (output.y = input1.y - 0.1025, i.e. exactly
                            half the pin pitch -- the output sits centred
                            between the two inputs)

NOT confirmed identical -- this was the actual new finding from the probe
(no prior fix this session needed it, because every wire this session
terminated at a named anchor, never a hand-computed offset): gate BODY
WIDTH (the output's x-offset from input 1) varies by type, because the
inversion bubble (NAND/NOR/XNOR) and the extra back-curve (XOR/XNOR) each
add real width:

    AND / OR   : 0.797
    XOR        : 0.899
    NAND       : 0.934
    NOR        : 0.932
    XNOR       : 1.034
    NOT        : 0.903 (single input/output, no y-offset)

These widths are the layout engine's per-gate bounding box (`gates.py`'s
`GATE_GEOMETRY` table below) -- used only for collision/clearance math and
canvas sizing. They are NEVER used to compute a wire's connection point;
every wire in the renderer terminates at the gate's own named TikZ anchor
(`<id>.input 1`, `<id>.output`, ...), exactly so a small measurement error
here can never produce a mis-wired diagram the way a hand-typed offset did
repeatedly this session.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ir import GateType

PIN_PITCH = 0.205
OUTPUT_DY = -0.1025


@dataclass(frozen=True)
class GateGeometry:
    tikz_style: str          # circuits.logic.US node style, e.g. "and gate"
    n_inputs: int            # 1 or 2 (MUX/DEMUX/ADDER/CUSTOM_BLOCK are drawn as boxes, not gate symbols)
    body_width: float        # measured output.x - input1.x, at scale=1
    is_box: bool = False     # True for MUX/DEMUX/ADDER/REGISTER/DFF/CUSTOM_BLOCK: drawn as a
                              # rounded rectangle (like this repo's HA/FA/Register blocks),
                              # not a circuits.logic.US gate symbol
    box_height: float = 1.1  # box types only: minimum height, matches this repo's existing
                              # Mux16/Register/FullAdder block diagrams (Labs/CS401/lab-3, lab-2)


GATE_GEOMETRY: dict[GateType, GateGeometry] = {
    GateType.AND:  GateGeometry("and gate",  2, 0.797),
    GateType.OR:   GateGeometry("or gate",   2, 0.797),
    GateType.XOR:  GateGeometry("xor gate",  2, 0.899),
    GateType.NAND: GateGeometry("nand gate", 2, 0.934),
    GateType.NOR:  GateGeometry("nor gate",  2, 0.932),
    GateType.XNOR: GateGeometry("xnor gate", 2, 1.034),
    GateType.NOT:  GateGeometry("not gate",  1, 0.903),
    # Box-style blocks: width/height chosen generously (not measured --
    # these are plain `rounded corners` rectangles like this repo's
    # existing HA/FA/Register diagrams, sized to fit a short label, not a
    # fixed-geometry library symbol). Inputs/outputs are distributed along
    # the box's west/east edge via TikZ's own `north west`/`south west`
    # anchors and calc-interpolation, never a hand-computed offset.
    GateType.MUX:      GateGeometry("", 3, 1.6, is_box=True, box_height=1.1),
    GateType.DEMUX:    GateGeometry("", 2, 1.6, is_box=True, box_height=1.1),
    GateType.ADDER:    GateGeometry("", 3, 1.8, is_box=True, box_height=1.2),
    GateType.DFF:      GateGeometry("", 1, 1.2, is_box=True, box_height=0.8),
    GateType.REGISTER: GateGeometry("", 2, 1.6, is_box=True, box_height=1.1),
    GateType.CUSTOM_BLOCK: GateGeometry("", 0, 1.6, is_box=True, box_height=1.2),
}


def input_pin_y(gate_index_from_top: int) -> float:
    """Relative y of the gate_index_from_top-th input pin (0-indexed from
    the top), measured downward from input 1, in tikz-space (negative =
    down, matching this repo's existing y-up coordinate convention)."""
    return -gate_index_from_top * PIN_PITCH


def output_pin(geom: GateGeometry) -> tuple[float, float]:
    """Output anchor position relative to input 1, in tikz-space."""
    return (geom.body_width, OUTPUT_DY)


def arity(gate_type: GateType) -> int | None:
    """Expected input count for a gate type, or None if variable (box types)."""
    geom = GATE_GEOMETRY.get(gate_type)
    if geom is None:
        return None
    if geom.is_box:
        return None  # box types (MUX/ADDER/...) validated by name convention, not a fixed count here
    return geom.n_inputs
