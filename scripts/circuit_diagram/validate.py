"""
Mechanical Circuit IR validation -- every check the spec requires, each
returning a typed error (never raising), so the caller sees every problem
at once instead of stopping at the first one. Matches the "report every
issue" convention scripts/check-tikz-prevention.py already uses in this
repo.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ir import CircuitSpec, GateSpec
from .gates import GATE_GEOMETRY, arity


@dataclass
class ValidationError:
    code: str          # short machine-readable tag, e.g. "DUPLICATE_ID"
    message: str
    gate_id: str | None = None

    def __str__(self) -> str:
        loc = f" [{self.gate_id}]" if self.gate_id else ""
        return f"{self.code}{loc}: {self.message}"


def validate_circuit(spec: CircuitSpec) -> list[ValidationError]:
    errors: list[ValidationError] = []

    # -- duplicate gate IDs --
    seen_ids: set[str] = set()
    for g in spec.gates:
        if g.id in seen_ids:
            errors.append(ValidationError("DUPLICATE_ID", f"gate id '{g.id}' used more than once", g.id))
        seen_ids.add(g.id)

    # -- every signal has exactly one source (input or gate output) --
    input_ids = spec.input_ids()
    output_sources: dict[str, list[str]] = {}
    for g in spec.gates:
        output_sources.setdefault(g.output, []).append(g.id)
    for signal, producers in output_sources.items():
        if signal in input_ids:
            errors.append(ValidationError(
                "SIGNAL_SHADOWS_INPUT",
                f"signal '{signal}' is produced by gate(s) {producers} but is also a circuit input",
            ))
        if len(producers) > 1:
            errors.append(ValidationError(
                "MULTIPLE_DRIVERS",
                f"signal '{signal}' is driven by more than one gate: {producers}",
            ))

    # -- no undefined-input references --
    known_signals = set(input_ids) | set(output_sources.keys())
    for g in spec.gates:
        for sig in g.inputs:
            if sig not in known_signals:
                errors.append(ValidationError(
                    "UNDEFINED_SIGNAL",
                    f"gate '{g.id}' references undefined signal '{sig}'",
                    g.id,
                ))

    # -- every declared output is connected --
    for o in spec.outputs:
        if o.signal not in known_signals:
            errors.append(ValidationError(
                "UNCONNECTED_OUTPUT",
                f"declared output '{o.signal}' has no source gate or input",
            ))

    # -- gate input-arity matches the registry --
    for g in spec.gates:
        expected = arity(g.type)
        if expected is not None and len(g.inputs) != expected:
            errors.append(ValidationError(
                "ARITY_MISMATCH",
                f"gate '{g.id}' of type {g.type.value} expects {expected} input(s), got {len(g.inputs)}",
                g.id,
            ))
        if g.type not in GATE_GEOMETRY:
            errors.append(ValidationError(
                "UNKNOWN_GATE_TYPE",
                f"gate '{g.id}' has unregistered type {g.type!r}",
                g.id,
            ))
        for fb in g.feedback_inputs:
            if fb not in g.inputs:
                errors.append(ValidationError(
                    "BAD_FEEDBACK_MARK",
                    f"gate '{g.id}' marks '{fb}' as a feedback input but it is not in its inputs list",
                    g.id,
                ))

    # -- combinational-cycle check (DFS), ignoring edges marked feedback --
    # Build: signal -> gate that consumes it (edge), skip edges the
    # producing gate's consumer marked as `feedback_inputs`.
    gate_by_output = spec.gate_by_output()

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {g.id: WHITE for g in spec.gates}

    def dfs(gate: GateSpec, path: list[str]) -> list[str] | None:
        color[gate.id] = GRAY
        for sig in gate.inputs:
            if sig in gate.feedback_inputs:
                continue  # explicitly allowed feedback edge, skip
            producer = gate_by_output.get(sig)
            if producer is None:
                continue  # circuit input, not a gate -- no cycle possible through it
            if color[producer.id] == GRAY:
                return path + [producer.id]
            if color[producer.id] == WHITE:
                cyc = dfs(producer, path + [producer.id])
                if cyc is not None:
                    return cyc
        color[gate.id] = BLACK
        return None

    for g in spec.gates:
        if color[g.id] == WHITE:
            cyc = dfs(g, [g.id])
            if cyc is not None:
                errors.append(ValidationError(
                    "COMBINATIONAL_CYCLE",
                    "illegal combinational cycle (no gate in the loop marks its "
                    f"feedback edge): {' -> '.join(cyc)}",
                ))

    return errors
