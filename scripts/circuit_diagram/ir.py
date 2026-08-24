"""
Circuit Intermediate Representation.

Plain dataclasses mirroring the user-facing JSON schema exactly. This is
the ONLY layer an LLM (or any natural-language front end) is responsible
for producing -- everything downstream (validation, layout, rendering,
compilation, visual validation) is deterministic Python with no coordinate
guessing anywhere.

Example:
    {
      "inputs": [{"id": "a", "label": "a"}, {"id": "b", "label": "b"}],
      "gates": [
        {"id": "xor1", "type": "XOR", "inputs": ["a", "b"], "output": "SUM"},
        {"id": "and1", "type": "AND", "inputs": ["a", "b"], "output": "CARRY"}
      ],
      "outputs": [{"signal": "SUM"}, {"signal": "CARRY"}]
    }
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class GateType(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    NAND = "NAND"
    NOR = "NOR"
    XNOR = "XNOR"
    MUX = "MUX"
    DEMUX = "DEMUX"
    ADDER = "ADDER"
    DFF = "DFF"
    REGISTER = "REGISTER"
    CUSTOM_BLOCK = "CUSTOM_BLOCK"


@dataclass
class InputSpec:
    id: str
    label: str | None = None

    def to_dict(self) -> dict:
        return {"id": self.id, "label": self.label}

    @staticmethod
    def from_dict(d: dict) -> "InputSpec":
        return InputSpec(id=d["id"], label=d.get("label"))


@dataclass
class OutputSpec:
    signal: str
    label: str | None = None

    def to_dict(self) -> dict:
        return {"signal": self.signal, "label": self.label}

    @staticmethod
    def from_dict(d: dict) -> "OutputSpec":
        return OutputSpec(signal=d["signal"], label=d.get("label"))


@dataclass
class GateSpec:
    id: str
    type: GateType
    inputs: list[str]
    output: str
    label: str | None = None
    # Names (subset of `inputs`) whose source->this-gate edge is a
    # legitimate sequential feedback path (e.g. a DFF/REGISTER's own
    # output feeding back into a Mux ahead of itself), exempted from the
    # combinational-cycle check in validate.py. Matches the user's own
    # "no illegal combinational cycles unless explicitly allowed" spec.
    feedback_inputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "type": self.type.value if isinstance(self.type, GateType) else self.type,
            "inputs": list(self.inputs),
            "output": self.output,
        }
        if self.label is not None:
            d["label"] = self.label
        if self.feedback_inputs:
            d["feedback_inputs"] = list(self.feedback_inputs)
        return d

    @staticmethod
    def from_dict(d: dict) -> "GateSpec":
        return GateSpec(
            id=d["id"],
            type=GateType(d["type"]),
            inputs=list(d["inputs"]),
            output=d["output"],
            label=d.get("label"),
            feedback_inputs=list(d.get("feedback_inputs", [])),
        )


@dataclass
class CircuitSpec:
    inputs: list[InputSpec]
    gates: list[GateSpec]
    outputs: list[OutputSpec]
    name: str | None = None

    def to_dict(self) -> dict:
        d = {
            "inputs": [i.to_dict() for i in self.inputs],
            "gates": [g.to_dict() for g in self.gates],
            "outputs": [o.to_dict() for o in self.outputs],
        }
        if self.name is not None:
            d["name"] = self.name
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @staticmethod
    def from_dict(d: dict) -> "CircuitSpec":
        return CircuitSpec(
            inputs=[InputSpec.from_dict(i) for i in d.get("inputs", [])],
            gates=[GateSpec.from_dict(g) for g in d.get("gates", [])],
            outputs=[OutputSpec.from_dict(o) for o in d.get("outputs", [])],
            name=d.get("name"),
        )

    @staticmethod
    def from_json(text: str) -> "CircuitSpec":
        return CircuitSpec.from_dict(json.loads(text))

    @staticmethod
    def from_json_file(path: str | Path) -> "CircuitSpec":
        return CircuitSpec.from_json(Path(path).read_text(encoding="utf-8"))

    def gate_by_output(self) -> dict[str, GateSpec]:
        """Map every signal name to the gate that produces it."""
        return {g.output: g for g in self.gates}

    def input_ids(self) -> set[str]:
        return {i.id for i in self.inputs}
