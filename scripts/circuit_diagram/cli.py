#!/usr/bin/env python3
"""
circuit_diagram CLI -- deterministic logic-gate circuit diagram generation.

Usage:
  python3 scripts/circuit_diagram/cli.py generate <ir.json> --out DIR [--name NAME]
  python3 scripts/circuit_diagram/cli.py validate <ir.json>

Exit codes: 0 = success, 1 = validation/generation failure (details on
stderr), 2 = usage/internal error. Matches this repo's scripts/*.py
convention.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python3 scripts/circuit_diagram/cli.py ...` (no package install)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.circuit_diagram.ir import CircuitSpec
from scripts.circuit_diagram.validate import validate_circuit
from scripts.circuit_diagram.pipeline import generate_circuit


def cmd_validate(args: argparse.Namespace) -> int:
    spec = CircuitSpec.from_json_file(args.ir_json)
    errors = validate_circuit(spec)
    if errors:
        for e in errors:
            print(str(e), file=sys.stderr)
        return 1
    print(f"OK: {len(spec.gates)} gate(s), {len(spec.inputs)} input(s), {len(spec.outputs)} output(s)")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    spec = CircuitSpec.from_json_file(args.ir_json)
    result = generate_circuit(spec, args.out)
    if not result.ok:
        if result.validation_errors:
            for e in result.validation_errors:
                print(str(e), file=sys.stderr)
        if result.visual_findings:
            for f in result.visual_findings:
                print(f"{f.code}: {f.message}", file=sys.stderr)
        if result.compile_log and not result.pdf_path:
            print(result.compile_log[-2000:], file=sys.stderr)
        return 1
    print(f"OK: {result.pdf_path} (round {result.rounds})")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="validate a Circuit IR JSON file")
    p_val.add_argument("ir_json")
    p_val.set_defaults(func=cmd_validate)

    p_gen = sub.add_parser("generate", help="run the full pipeline: validate -> layout -> render -> compile -> visual-validate")
    p_gen.add_argument("ir_json")
    p_gen.add_argument("--out", required=True, help="output directory")
    p_gen.add_argument("--name", default=None, help="override the circuit's output basename")
    p_gen.set_defaults(func=cmd_generate)

    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001 -- CLI boundary, convert to exit code 2
        print(f"internal error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
