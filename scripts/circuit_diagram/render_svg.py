"""
SVG renderer: the SAME Circuit IR + Layout the TikZ renderer uses,
producing an equivalent picture -- this is what guarantees the two
outputs represent the same circuit (shared Layout object, shared
GATE_GEOMETRY constants), per the user's requirement that TikZ and SVG
"represent exactly the same circuit."

SVG has no named-anchor system, so (unlike render_tikz.py) this module
DOES compute pixel-space pin offsets -- but always from the single
measured GATE_GEOMETRY table in gates.py, never a per-diagram guess, so
there is no drift risk between what's drawn and what's connected.
"""

from __future__ import annotations

from .ir import CircuitSpec, GateType
from .gates import GATE_GEOMETRY, PIN_PITCH, OUTPUT_DY
from .layout import Layout, output_node_id

SCALE = 40.0   # px per tikz unit
PAD = 40.0     # px margin around the drawing


def _to_svg(x: float, y: float) -> tuple[float, float]:
    return (x * SCALE + PAD, -y * SCALE + PAD)


def _gate_input_local(idx: int) -> tuple[float, float]:
    """Local (relative to input-1-at-origin) pixel offset of input `idx`."""
    return (0.0, idx * PIN_PITCH * SCALE)


def _gate_output_local(body_width: float) -> tuple[float, float]:
    return (body_width * SCALE, -OUTPUT_DY * SCALE)


def _gate_shape(gtype: GateType, body_w_px: float, h_px: float) -> str:
    """A simplified path/polygon approximating the circuits.logic.US
    silhouette, in a local frame with input 1 at (0,0)."""
    top = -h_px / 2
    bot = h_px / 2
    bulge = body_w_px * 0.35
    has_bubble = gtype in (GateType.NAND, GateType.NOR, GateType.XNOR)
    body_w = body_w_px - (8 if has_bubble else 0)

    if gtype in (GateType.AND, GateType.NAND):
        d = (f"M 0 {top} L {body_w*0.5} {top} "
             f"A {body_w*0.5} {h_px/2} 0 0 1 {body_w*0.5} {bot} "
             f"L 0 {bot} Z")
    elif gtype in (GateType.OR, GateType.NOR, GateType.XOR, GateType.XNOR):
        d = (f"M 0 {top} Q {body_w*0.25} 0 0 {bot} "
             f"Q {body_w*0.6} {bot} {body_w} 0 "
             f"Q {body_w*0.6} {top} 0 {top} Z")
    elif gtype == GateType.NOT:
        d = f"M 0 {top} L 0 {bot} L {body_w} 0 Z"
    else:
        d = f"M 0 {top} L {body_w} {top} L {body_w} {bot} L 0 {bot} Z"
    svg = f'<path d="{d}" fill="white" stroke="black" stroke-width="2"/>'
    if gtype in (GateType.XOR, GateType.XNOR):
        d2 = f"M {-body_w_px*0.12} {top} Q {body_w*0.1} 0 {-body_w_px*0.12} {bot}"
        svg += f'<path d="{d2}" fill="none" stroke="black" stroke-width="2"/>'
    if has_bubble:
        svg += f'<circle cx="{body_w+4}" cy="0" r="4" fill="white" stroke="black" stroke-width="2"/>'
    return svg


def render_svg(spec: CircuitSpec, layout: Layout) -> str:
    xs = [p.x for p in layout.positions.values()]
    ys = [p.y for p in layout.positions.values()]
    width = (max(xs) - min(xs) + 4) * SCALE if xs else 200
    height = (max(ys) - min(ys) + 4) * SCALE if ys else 200

    gate_by_id = {g.id: g for g in spec.gates}
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="serif">'
    ]

    # -- circuit inputs --
    for inp in spec.inputs:
        pos = layout.positions[inp.id]
        px, py = _to_svg(pos.x, pos.y)
        label = inp.label if inp.label is not None else inp.id
        parts.append(f'<text x="{px-10:.1f}" y="{py+5:.1f}" text-anchor="end" font-style="italic">{label}</text>')

    # -- gates --
    anchor_px: dict[str, dict[str, tuple[float, float]]] = {}
    for g in spec.gates:
        pos = layout.positions[g.id]
        px, py = _to_svg(pos.x, pos.y)
        geom = GATE_GEOMETRY[g.type]
        h_px = geom.box_height * SCALE if geom.is_box else PIN_PITCH * SCALE * 2.6
        body_w_px = geom.body_width * SCALE

        inputs_px = {}
        for idx in range(len(g.inputs)):
            if geom.is_box:
                n = max(len(g.inputs), 1)
                frac = (idx + 0.5) / n
                lx, ly = 0.0, (frac - 0.5) * h_px
            else:
                lx, ly = _gate_input_local(idx)
            inputs_px[idx] = (px + lx, py + ly)
        if geom.is_box:
            out_local = (body_w_px, 0.0)
        else:
            out_local = _gate_output_local(geom.body_width)
        output_px = (px + out_local[0], py + out_local[1])
        anchor_px[g.id] = {"inputs": inputs_px, "output": output_px}

        parts.append(f'<g transform="translate({px:.1f},{py:.1f})">')
        if geom.is_box:
            label = g.label if g.label is not None else g.type.value
            parts.append(
                f'<rect x="0" y="{-h_px/2:.1f}" width="{body_w_px:.1f}" height="{h_px:.1f}" '
                f'rx="6" fill="white" stroke="black" stroke-width="2"/>'
            )
            parts.append(f'<text x="{body_w_px/2:.1f}" y="5" text-anchor="middle">{label}</text>')
        else:
            parts.append(_gate_shape(g.type, body_w_px, h_px))
        parts.append("</g>")

    # -- outputs --
    for o in spec.outputs:
        nid = output_node_id(o.signal)
        pos = layout.positions[nid]
        px, py = _to_svg(pos.x, pos.y)
        label = o.label if o.label is not None else o.signal
        parts.append(f'<text x="{px+10:.1f}" y="{py+5:.1f}" font-style="italic">{label}</text>')

    # -- wires (reuses the same routed waypoints the TikZ renderer used) --
    def endpoint(node: str, is_output_side: bool, idx: int | None) -> tuple[float, float]:
        if node in gate_by_id:
            return anchor_px[node]["output"] if is_output_side else anchor_px[node]["inputs"][idx]
        pos = layout.positions[node]
        return _to_svg(pos.x, pos.y)

    for e in layout.edges:
        src_px = endpoint(e.src_node, True, None)
        if e.dst_input_index is None:
            dst_px = endpoint(e.dst_node, False, None)
        else:
            dst_px = endpoint(e.dst_node, False, e.dst_input_index)
        pts = [src_px]
        for wp in e.waypoints:
            pos = layout.positions[wp]
            pts.append(_to_svg(pos.x, pos.y))
        pts.append(dst_px)
        path_d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            path_d += f"L {x0:.1f} {y1:.1f} L {x1:.1f} {y1:.1f} "  # horizontal-then-vertical, matching -|
        parts.append(f'<path d="{path_d}" fill="none" stroke="black" stroke-width="2"/>')

    parts.append("</svg>")
    return "\n".join(parts) + "\n"
