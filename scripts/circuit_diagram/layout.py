"""
Deterministic Sugiyama-style layered graph layout, pure Python (no
networkx -- confirmed unavailable under the `python3` this repo's tooling
actually invokes; see the plan's Environment Constraints section).

    1. Layering       -- longest-path layering from a topological sort.
    2. Dummy nodes     -- multi-layer edges get one virtual routing node
                          per intermediate layer, so long wires are
                          first-class routable objects instead of
                          diagonal shortcuts.
    3. Crossing min.   -- barycenter heuristic, alternating sweeps.
    4. Coordinates     -- x = layer * horizontal_spacing,
                          y = slot * vertical_spacing, centred per layer.

Feedback edges (GateSpec.feedback_inputs) are excluded from layering and
crossing minimization entirely -- they're drawn by the renderer as a
direct back-route around the diagram, the same way every hand-fixed
sequential circuit this session (Bit, PC, the CPU datapath) routes its
own feedback wire, and they must never be allowed to pull a gate backward
in the layer order.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .ir import CircuitSpec, GateSpec
from .gates import GATE_GEOMETRY, GateGeometry, PIN_PITCH

DEFAULT_HORIZONTAL_SPACING = 3.0
DEFAULT_VERTICAL_SPACING = 2.0
CROSSING_MIN_PASSES = 8


def output_node_id(signal: str) -> str:
    return f"__output__{signal}"


@dataclass
class NodePos:
    x: float
    y: float


@dataclass
class EdgeRoute:
    signal: str
    src_node: str
    dst_node: str
    dst_input_index: int | None   # None for a circuit-output sink
    waypoints: list[str] = field(default_factory=list)  # dummy node ids, src->dst order
    is_feedback: bool = False


@dataclass
class Layout:
    positions: dict[str, NodePos]
    node_kind: dict[str, str]           # 'input' | 'gate' | 'output' | 'dummy'
    node_layer: dict[str, int]
    edges: list[EdgeRoute]
    gate_geometry: dict[str, GateGeometry]   # gate id -> resolved geometry
    horizontal_spacing: float
    vertical_spacing: float

    def widen_gap(self, layer: int, extra: float) -> None:
        """Targeted repair: push every node at `layer` and beyond further
        right by `extra`, used by the self-correction loop instead of a
        full re-layout when validateDiagram finds one clearance failure."""
        for node, pos in self.positions.items():
            if self.node_layer.get(node, -1) >= layer:
                pos.x += extra


def _topological_order(spec: CircuitSpec) -> list[str]:
    """Gate ids in dependency order, ignoring feedback-marked edges."""
    gate_by_id = {g.id: g for g in spec.gates}
    gate_by_output = spec.gate_by_output()
    order: list[str] = []
    state: dict[str, str] = {}

    def visit(gid: str) -> None:
        if state.get(gid) == "done":
            return
        state[gid] = "visiting"
        gate = gate_by_id[gid]
        for sig in gate.inputs:
            if sig in gate.feedback_inputs:
                continue
            producer = gate_by_output.get(sig)
            if producer is not None and state.get(producer.id) != "done":
                visit(producer.id)
        state[gid] = "done"
        order.append(gid)

    for g in spec.gates:
        visit(g.id)
    return order


def _compute_signal_layers(spec: CircuitSpec, order: list[str]) -> dict[str, int]:
    layer: dict[str, int] = {i.id: 0 for i in spec.inputs}
    gate_by_id = {g.id: g for g in spec.gates}
    for gid in order:
        gate = gate_by_id[gid]
        max_in = -1
        for sig in gate.inputs:
            if sig in gate.feedback_inputs:
                continue
            max_in = max(max_in, layer.get(sig, 0))
        layer[gate.output] = max_in + 1
    return layer


def layout_circuit(
    spec: CircuitSpec,
    horizontal_spacing: float = DEFAULT_HORIZONTAL_SPACING,
    vertical_spacing: float = DEFAULT_VERTICAL_SPACING,
) -> Layout:
    gate_by_id = {g.id: g for g in spec.gates}
    gate_by_output = spec.gate_by_output()
    order = _topological_order(spec)
    sig_layer = _compute_signal_layers(spec, order)

    node_kind: dict[str, str] = {}
    node_layer: dict[str, int] = {}
    for i in spec.inputs:
        node_kind[i.id] = "input"
        node_layer[i.id] = 0
    for g in spec.gates:
        node_kind[g.id] = "gate"
        node_layer[g.id] = sig_layer[g.output]
    for o in spec.outputs:
        nid = output_node_id(o.signal)
        node_kind[nid] = "output"
        node_layer[nid] = sig_layer.get(o.signal, 0) + 1

    max_layer = max(node_layer.values(), default=0)
    layers: dict[int, list[str]] = {L: [] for L in range(max_layer + 1)}
    for node, L in node_layer.items():
        layers[L].append(node)

    # -- build edges, inserting dummy nodes for any span > 1 layer --
    edges: list[EdgeRoute] = []
    dummy_counter = 0

    def producer_node(sig: str) -> str | None:
        if sig in gate_by_output:
            return gate_by_output[sig].id
        return sig if any(sig == i.id for i in spec.inputs) else None

    def route(src: str, dst: str, dst_idx: int | None, signal: str, feedback: bool) -> None:
        nonlocal dummy_counter
        if feedback:
            edges.append(EdgeRoute(signal, src, dst, dst_idx, [], True))
            return
        src_layer = node_layer[src]
        dst_layer = node_layer[dst]
        waypoints: list[str] = []
        prev = src
        for L in range(src_layer + 1, dst_layer):
            dummy_counter += 1
            dnode = f"__dummy__{dummy_counter}"
            node_kind[dnode] = "dummy"
            node_layer[dnode] = L
            layers[L].append(dnode)
            waypoints.append(dnode)
            prev = dnode
        edges.append(EdgeRoute(signal, src, dst, dst_idx, waypoints, False))

    for g in spec.gates:
        for idx, sig in enumerate(g.inputs):
            is_fb = sig in g.feedback_inputs
            src = producer_node(sig)
            if src is None:
                continue  # dangling signal -- validate_circuit() should have caught this already
            route(src, g.id, idx, sig, is_fb)

    for o in spec.outputs:
        src = producer_node(o.signal)
        if src is None:
            continue
        route(src, output_node_id(o.signal), None, o.signal, False)

    # -- crossing minimization: barycenter heuristic --
    def neighbors(layer_from: int, layer_to: int) -> dict[str, list[str]]:
        """node -> list of the node ids it connects to in the OTHER named layer,
        walking through dummy-node chains one hop at a time."""
        adj: dict[str, list[str]] = {}
        for e in edges:
            if e.is_feedback:
                continue
            chain = [e.src_node] + e.waypoints + [e.dst_node]
            for a, b in zip(chain, chain[1:]):
                la, lb = node_layer[a], node_layer[b]
                if {la, lb} == {layer_from, layer_to}:
                    lo, hi = (a, b) if la < lb else (b, a)
                    adj.setdefault(lo, []).append(hi)
                    adj.setdefault(hi, []).append(lo)
        return adj

    for _pass in range(CROSSING_MIN_PASSES):
        forward = _pass % 2 == 0
        layer_range = range(1, max_layer + 1) if forward else range(max_layer - 1, -1, -1)
        for L in layer_range:
            fixed_L = L - 1 if forward else L + 1
            if fixed_L < 0 or fixed_L > max_layer:
                continue
            fixed_pos = {n: idx for idx, n in enumerate(layers[fixed_L])}
            adj = neighbors(L, fixed_L)
            # Snapshot the pre-sort order for the fallback branch below.
            # CPython's list.sort() detaches the list's backing array for
            # the duration of the call (so a re-entrant read of the SAME
            # list from inside its own key function sees it as empty,
            # not merely unsorted) -- reading `layers[L]` here, not inside
            # `barycenter`, is what makes the fallback see real data.
            current_order = {n: idx for idx, n in enumerate(layers[L])}

            def barycenter(node: str, _fixed_pos=fixed_pos, _adj=adj, _current_order=current_order) -> float:
                nbrs = [_fixed_pos[n] for n in _adj.get(node, []) if n in _fixed_pos]
                if not nbrs:
                    return _current_order[node]  # keep current relative position
                return sum(nbrs) / len(nbrs)

            layers[L].sort(key=barycenter)

    # -- coordinate assignment --
    tallest = max((len(v) for v in layers.values()), default=1)
    positions: dict[str, NodePos] = {}
    gate_geometry: dict[str, GateGeometry] = {}
    for L, nodes in layers.items():
        n = len(nodes)
        offset = (tallest - n) * vertical_spacing / 2.0
        for slot, node in enumerate(nodes):
            y = offset + (n - 1 - slot) * vertical_spacing
            positions[node] = NodePos(x=L * horizontal_spacing, y=y)
            if node_kind[node] == "gate":
                gtype = gate_by_id[node].type
                gate_geometry[node] = GATE_GEOMETRY[gtype]

    return Layout(
        positions=positions,
        node_kind=node_kind,
        node_layer=node_layer,
        edges=edges,
        gate_geometry=gate_geometry,
        horizontal_spacing=horizontal_spacing,
        vertical_spacing=vertical_spacing,
    )
