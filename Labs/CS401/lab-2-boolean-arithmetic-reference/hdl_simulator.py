"""
hdl_simulator.py -- a minimal Nand2Tetris HDL interpreter, combinational
chips only (sufficient for Labs 1-2; sequential chips from Lab 3 onward
would need a tick/tock extension).

This exists because the real grading tool -- the official Nand2Tetris
Hardware Simulator (Java) -- cannot run in this environment. It parses
and EXECUTES the actual .hdl files in hdl/, the same files a student
would load into the real simulator, so test_hdl.py can verify them
against an independent oracle (Python's native bitwise operators)
rather than just eyeballing the HDL text for correctness.

Supports: CHIP/IN/OUT/PARTS, BUILTIN Nand (the sole primitive), part
invocation with pin=value connections, bus declarations pin[width],
bus indexing pin[i], bus range slicing pin[lo..hi], the true/false
constant literals (added for Lab 2's Inc16/ALU), and LHS (part-output)
pin slicing -- the same part's output pin can appear multiple times in
one invocation with different slices, e.g.
    Mux16(a=x, b=y, sel=s, out=out, out[0..7]=lo, out[8..15]=hi, out[15]=ng);
fanning one computed value out to several targets in a single call. This
was added after discovering the ALU's first draft read back from its
own already-written `out` pin via a separate part invocation -- valid
in this interpreter, but rejected by the real Hardware Simulator, which
treats a chip's declared OUT pins as write-only within the chip. The
canonical fan-out form above is the correct, simulator-conformant
pattern. Does NOT support: CLOCKED chips, or internal buses referenced
before their width is established by a prior connection.
"""

import os
import re

_chip_cache = {}


def _strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)
    return text


def _parse_pin_decl(decl):
    pins = []
    for tok in decl.split(","):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r"^(\w+)(?:\[(\d+)\])?$", tok)
        if not m:
            raise ValueError(f"bad pin declaration: {tok!r}")
        name, width = m.group(1), m.group(2)
        pins.append((name, int(width) if width else 1))
    return pins


def _parse_signal_ref(text):
    m = re.match(r"^(\w+)(?:\[(\d+)(?:\.\.(\d+))?\])?$", text)
    if not m:
        raise ValueError(f"bad signal reference: {text!r}")
    name, lo, hi = m.group(1), m.group(2), m.group(3)
    if lo is None:
        return name, None
    lo = int(lo)
    hi = int(hi) if hi is not None else lo
    return name, (lo, hi)


def _parse_hdl(path):
    text = _strip_comments(open(path, encoding="utf-8").read())
    chip_match = re.search(r"CHIP\s+(\w+)\s*\{(.*)\}", text, re.S)
    if not chip_match:
        raise ValueError(f"no CHIP block found in {path}")
    name = chip_match.group(1)
    body = chip_match.group(2)

    in_match = re.search(r"\bIN\s+([^;]+);", body)
    out_match = re.search(r"\bOUT\s+([^;]+);", body)
    ins = _parse_pin_decl(in_match.group(1)) if in_match else []
    outs = _parse_pin_decl(out_match.group(1)) if out_match else []

    builtin_match = re.search(r"\bBUILTIN\s+(\w+)\s*;", body)
    builtin = builtin_match.group(1) if builtin_match else None

    parts = []
    parts_match = re.search(r"PARTS:(.*)", body, re.S)
    if parts_match:
        for part_match in re.finditer(r"(\w+)\s*\(([^)]*)\)\s*;", parts_match.group(1)):
            part_name = part_match.group(1)
            # A list, not a dict: the same LHS pin name can legitimately
            # appear more than once (sliced differently each time) when
            # a part's output is fanned out to several targets.
            conns = []
            for conn in part_match.group(2).split(","):
                conn = conn.strip()
                if not conn:
                    continue
                lhs, rhs = conn.split("=")
                lhs_name, lhs_slice = _parse_signal_ref(lhs.strip())
                conns.append((lhs_name, lhs_slice, rhs.strip()))
            parts.append((part_name, conns))

    return {"name": name, "ins": ins, "outs": outs, "parts": parts, "builtin": builtin}


def _load_chip_def(hdl_dir, name):
    key = (hdl_dir, name)
    if key in _chip_cache:
        return _chip_cache[key]
    path = os.path.join(hdl_dir, name + ".hdl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"chip definition not found: {path}")
    chip = _parse_hdl(path)
    _chip_cache[key] = chip
    return chip


def eval_chip(hdl_dir, name, input_bits):
    """
    input_bits: dict pin_name -> list[int] (index 0 = LSB / bit 0),
    one entry per the chip's declared IN pins.
    Returns dict pin_name -> list[int], one entry per declared OUT pin.
    """
    if name == "Nand":
        a = input_bits["a"][0]
        b = input_bits["b"][0]
        return {"out": [1 - (a & b)]}

    chip = _load_chip_def(hdl_dir, name)
    if chip["builtin"] == "Nand":
        a = input_bits["a"][0]
        b = input_bits["b"][0]
        return {"out": [1 - (a & b)]}

    signals = {}
    for pin_name, _width in chip["ins"]:
        signals[pin_name] = list(input_bits[pin_name])
    for pin_name, width in chip["outs"]:
        signals[pin_name] = [0] * width

    def get_slice(ref_name, rng):
        if ref_name not in signals:
            raise ValueError(f"{name}: reference to undefined signal '{ref_name}'")
        bits = signals[ref_name]
        if rng is None:
            return list(bits)
        lo, hi = rng
        return bits[lo:hi + 1]

    for part_name, conns in chip["parts"]:
        if part_name == "Nand":
            part_in_widths = {"a": 1, "b": 1}
            part_out_widths = {"out": 1}
        else:
            part_def = _load_chip_def(hdl_dir, part_name)
            part_in_widths = dict(part_def["ins"])
            part_out_widths = dict(part_def["outs"])

        part_input_bits = {}
        for lhs_name, _lhs_slice, rhs in conns:
            if lhs_name in part_in_widths:
                if rhs == "true":
                    part_input_bits[lhs_name] = [1] * part_in_widths[lhs_name]
                elif rhs == "false":
                    part_input_bits[lhs_name] = [0] * part_in_widths[lhs_name]
                else:
                    ref_name, rng = _parse_signal_ref(rhs)
                    part_input_bits[lhs_name] = get_slice(ref_name, rng)

        out_bits = eval_chip(hdl_dir, part_name, part_input_bits)

        for lhs_name, lhs_slice, rhs in conns:
            if lhs_name in part_out_widths:
                produced_full = out_bits[lhs_name]
                if lhs_slice is None:
                    produced = produced_full
                else:
                    lo, hi = lhs_slice
                    produced = produced_full[lo:hi + 1]

                ref_name, rng = _parse_signal_ref(rhs)
                if ref_name not in signals:
                    target_width = (rng[1] - rng[0] + 1) if rng else len(produced)
                    signals[ref_name] = [0] * target_width
                if rng is None:
                    signals[ref_name] = list(produced)
                else:
                    lo, hi = rng
                    for i, v in zip(range(lo, hi + 1), produced):
                        signals[ref_name][i] = v

    return {pin_name: signals[pin_name] for pin_name, _width in chip["outs"]}
