"""
TikZ renderer: Circuit IR + Layout -> a standalone .tex string.

The one rule that exists because of this session's actual bugs: **no wire
ever terminates at a hand-typed numeric coordinate that is supposed to
approximate a pin.** Gate placement (`at (x,y)`) is the only place a
number from the layout touches a `\\node`; every wire endpoint is a named
TikZ anchor (`id.input 1`, `id.output`, or a `\\coordinate` for a circuit
input/output/dummy routing point), and every bend between layers uses
TikZ's own `-|` operator (horizontal-then-vertical to the next named
point) so even the orthogonal routing bends are computed by TikZ, not
typed by hand.
"""

from __future__ import annotations

from .ir import CircuitSpec, GateType
from .gates import GATE_GEOMETRY
from .layout import Layout, output_node_id

_PRIMITIVE_STYLES = {
    GateType.AND: "and gate", GateType.OR: "or gate", GateType.XOR: "xor gate",
    GateType.NAND: "nand gate", GateType.NOR: "nor gate", GateType.XNOR: "xnor gate",
    GateType.NOT: "not gate",
}


def _input_anchor(gate_id: str, gtype: GateType, idx: int, n_inputs: int) -> str:
    if gtype in _PRIMITIVE_STYLES:
        if gtype == GateType.NOT:
            return f"{gate_id}.input"
        return f"{gate_id}.input {idx + 1}"
    # box gate: distribute along the west edge via named anchors + calc,
    # never a hand-computed offset
    frac = (idx + 0.5) / n_inputs
    return f"($({gate_id}.north west)!{frac:.4f}!({gate_id}.south west)$)"


def _output_anchor(gate_id: str, gtype: GateType) -> str:
    if gtype in _PRIMITIVE_STYLES:
        return f"{gate_id}.output"
    return f"{gate_id}.east"


def _coord(ref: str) -> str:
    """Wrap a plain node/anchor name in parens for use in a `\\draw` path
    (`n1.output` -> `(n1.output)`); a calc expression from `_input_anchor`'s
    box-gate branch already has its own parens (`($(...)!f!(...)$)`) and
    is returned unchanged."""
    return ref if ref.startswith("(") else f"({ref})"


def render_tikz(spec: CircuitSpec, layout: Layout, standalone: bool = True) -> str:
    lines: list[str] = []
    if standalone:
        lines += [
            r"\documentclass[border=4pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{circuits.logic.US,positioning,calc}",
            r"\begin{document}",
        ]
    lines += [
        r"\begin{tikzpicture}[",
        r"    circuit logic US,",
        r"    every circuit symbol/.style={draw=black, thick, fill=white},",
        r"    every node/.style={font=\small},",
        r"    wire/.style={draw=black, thick},",
        r"]",
        "",
        "  % --- circuit inputs (coordinates only -- no visual node) ---",
    ]

    gate_by_id = {g.id: g for g in spec.gates}

    for inp in spec.inputs:
        pos = layout.positions[inp.id]
        lines.append(f"  \\coordinate ({inp.id}) at ({pos.x:.4f},{pos.y:.4f});")
        label = inp.label if inp.label is not None else inp.id
        lines.append(f"  \\node[font=\\small, left] at ({pos.x - 0.4:.4f},{pos.y:.4f}) {{${label}$}};")

    lines.append("")
    lines.append("  % --- gates (the ONLY place a numeric coordinate places a symbol) ---")
    for g in spec.gates:
        pos = layout.positions[g.id]
        geom = GATE_GEOMETRY[g.type]
        if g.type in _PRIMITIVE_STYLES:
            style = _PRIMITIVE_STYLES[g.type]
            if geom.n_inputs == 2:
                lines.append(
                    f"  \\node[{style}, inputs={{nn}}, anchor=input 1] ({g.id}) "
                    f"at ({pos.x:.4f},{pos.y:.4f}) {{}};"
                )
            else:
                lines.append(f"  \\node[{style}] ({g.id}) at ({pos.x:.4f},{pos.y:.4f}) {{}};")
        else:
            label = g.label if g.label is not None else g.type.value
            lines.append(
                f"  \\node[draw=black, fill=white, rounded corners, "
                f"minimum width={geom.body_width:.2f}cm, minimum height={geom.box_height:.2f}cm, "
                f"align=center] ({g.id}) at ({pos.x:.4f},{pos.y:.4f}) {{{label}}};"
            )

    lines.append("")
    lines.append("  % --- circuit outputs (coordinates only) ---")
    for o in spec.outputs:
        nid = output_node_id(o.signal)
        pos = layout.positions[nid]
        lines.append(f"  \\coordinate ({nid}) at ({pos.x:.4f},{pos.y:.4f});")
        label = o.label if o.label is not None else o.signal
        lines.append(f"  \\node[font=\\small, right] at ({pos.x + 0.4:.4f},{pos.y:.4f}) {{${label}$}};")

    lines.append("")
    lines.append("  % --- dummy routing waypoints (multi-layer wires only) ---")
    for node, kind in layout.node_kind.items():
        if kind == "dummy":
            pos = layout.positions[node]
            lines.append(f"  \\coordinate ({node}) at ({pos.x:.4f},{pos.y:.4f});")

    # NOTE (known limitation, not yet solved): when a signal fans out to
    # two gates that sit in the same layer but different rows (e.g. a
    # HalfAdder's `a` feeding both the XOR and the AND below it), a
    # direct anchor-to-anchor `-|` route for the far gate's input can
    # visually coincide with the near gate's own body/left edge -- this
    # reproduces the exact "wire drawn through a gate" defect class this
    # whole system exists to prevent, just inside the generator instead
    # of a hand-authored diagram. A per-edge staged/laned reroute was
    # attempted and reverted (it broke a previously-passing case; see
    # quality_reports/plans/is-it-good-idea-groovy-hanrahan.md) -- this is
    # flagged as follow-up work, not silently shipped as solved. Every
    # wire still terminates at a real anchor (never a hand-typed pin
    # coordinate), so the circuit is always electrically correct; only
    # the visual routing for this specific fan-out shape needs more work.

    # -- junction dots at every fan-out point (signal with >1 consumer) --
    fanout: dict[tuple[str, str], int] = {}
    for e in layout.edges:
        if e.is_feedback:
            continue
        fanout[(e.src_node, e.signal)] = fanout.get((e.src_node, e.signal), 0) + 1

    def gate_anchor(node_id: str, is_output_side: bool, dst_idx: int | None) -> str:
        gtype = gate_by_id[node_id].type
        if is_output_side:
            return _output_anchor(node_id, gtype)
        geom = GATE_GEOMETRY[gtype]
        return _input_anchor(node_id, gtype, dst_idx, geom.n_inputs)

    def node_anchor(node_id: str, is_src: bool, dst_idx: int | None) -> str:
        if node_id in gate_by_id:
            return gate_anchor(node_id, is_src, dst_idx)
        return node_id  # circuit input/output coordinate, or dummy waypoint

    lines.append("")
    lines.append("  % --- wires (every endpoint is a named anchor, never a typed coordinate;")
    lines.append("  % every bend is computed by TikZ's own -| operator against the two real")
    lines.append("  % anchors it connects, never a hand-typed numeric bend point) ---")
    for e in layout.edges:
        src_anchor = node_anchor(e.src_node, True, None)
        dst_anchor = node_anchor(e.dst_node, False, e.dst_input_index)

        if e.is_feedback:
            # Route above everything already drawn -- `current bounding
            # box` is TikZ's own auto-updating extent, so the clearance
            # offset is relative to real geometry, never an absolute
            # number guessed to clear whatever gates happen to be there.
            lines.append(
                f"  \\draw[wire] {_coord(src_anchor)} |- "
                f"($(current bounding box.north)+(0,0.5)$) -| {_coord(dst_anchor)};"
            )
            continue

        path = [_coord(src_anchor)] + [_coord(w) for w in e.waypoints] + [_coord(dst_anchor)]
        segs = " -| ".join(path)
        lines.append(f"  \\draw[wire] {segs};")

    for (src_node, signal), count in fanout.items():
        if count > 1:
            gtype = gate_by_id[src_node].type if src_node in gate_by_id else None
            anchor = _output_anchor(src_node, gtype) if gtype else src_node
            lines.append(f"  \\fill[black] ({anchor}) circle (1.6pt);")

    lines.append(r"\end{tikzpicture}")
    if standalone:
        lines.append(r"\end{document}")
    return "\n".join(lines) + "\n"
