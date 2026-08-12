"""
test_hdl.py -- executes the actual hdl/*.hdl files (the real submittable
artifacts) via hdl_simulator.py and checks them against Python's native
bitwise operators as an independent ground-truth oracle -- the same
oracle test_chips.py uses, so both the Python reference (chips.py) and
the HDL reference (hdl/*.hdl) are checked against the same standard,
not against each other.

Fails loudly: prints PASS/FAIL per chip, exits non-zero on any failure.
Run with: python test_hdl.py
"""

import itertools
import os
import sys

from hdl_simulator import eval_chip

HDL_DIR = os.path.join(os.path.dirname(__file__), "hdl")

failures = []


def check(name, got, expected, context):
    if got != expected:
        failures.append(f"{name}: FAIL at {context} -- got {got}, expected {expected}")
        return False
    return True


def report(name, ok):
    print(f"{'PASS' if ok else 'FAIL'}: {name}")


def run(chip, **inputs):
    """inputs: pin_name -> int (scalar) or tuple[int] (bus, index 0 = LSB)."""
    input_bits = {}
    for k, v in inputs.items():
        input_bits[k] = [v] if isinstance(v, int) else list(v)
    return eval_chip(HDL_DIR, chip, input_bits)


def bit(name, out):
    return out[name][0]


def bus(name, out):
    return tuple(out[name])


# ---------------------------------------------------------------------------
# 1-bit gates: exhaustive.
# ---------------------------------------------------------------------------

def test_not():
    ok = True
    for a in (0, 1):
        out = run("Not", **{"in": a})
        ok &= check("Not", bit("out", out), 1 - a, f"in={a}")
    report("Not", ok)
    return ok


def test_and():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        out = run("And", a=a, b=b)
        ok &= check("And", bit("out", out), a & b, f"a={a},b={b}")
    report("And", ok)
    return ok


def test_or():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        out = run("Or", a=a, b=b)
        ok &= check("Or", bit("out", out), a | b, f"a={a},b={b}")
    report("Or", ok)
    return ok


def test_xor():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        out = run("Xor", a=a, b=b)
        ok &= check("Xor", bit("out", out), a ^ b, f"a={a},b={b}")
    report("Xor", ok)
    return ok


def test_mux():
    ok = True
    for a, b, sel in itertools.product((0, 1), repeat=3):
        out = run("Mux", a=a, b=b, sel=sel)
        expected = b if sel else a
        ok &= check("Mux", bit("out", out), expected, f"a={a},b={b},sel={sel}")
    report("Mux", ok)
    return ok


def test_dmux():
    ok = True
    for inp, sel in itertools.product((0, 1), repeat=2):
        out = run("DMux", **{"in": inp, "sel": sel})
        expected = (inp, 0) if sel == 0 else (0, inp)
        got = (bit("a", out), bit("b", out))
        ok &= check("DMux", got, expected, f"in={inp},sel={sel}")
    report("DMux", ok)
    return ok


# ---------------------------------------------------------------------------
# 16-bit-bus gates: per-bit-position + background-pattern coverage
# (same strategy as test_chips.py's Python oracle checks).
# ---------------------------------------------------------------------------

def bus16(value_at_i, i, background):
    return tuple(value_at_i if k == i else background for k in range(16))


def test_not16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i in (0, 1):
                a = bus16(a_i, i, background)
                out = run("Not16", **{"in": a})
                expected = bus16(1 - a_i, i, 1 - background)
                ok &= check("Not16", bus("out", out), expected, f"bit={i},bg={background},a_i={a_i}")
    report("Not16", ok)
    return ok


def test_and16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i, b_i in itertools.product((0, 1), repeat=2):
                a = bus16(a_i, i, background)
                b = bus16(b_i, i, background)
                out = run("And16", a=a, b=b)
                expected = bus16(a_i & b_i, i, background & background)
                ok &= check("And16", bus("out", out), expected, f"bit={i},bg={background},a_i={a_i},b_i={b_i}")
    report("And16", ok)
    return ok


def test_or16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i, b_i in itertools.product((0, 1), repeat=2):
                a = bus16(a_i, i, background)
                b = bus16(b_i, i, background)
                out = run("Or16", a=a, b=b)
                expected = bus16(a_i | b_i, i, background | background)
                ok &= check("Or16", bus("out", out), expected, f"bit={i},bg={background},a_i={a_i},b_i={b_i}")
    report("Or16", ok)
    return ok


def test_mux16():
    ok = True
    for sel in (0, 1):
        for background in (0, 1):
            for i in range(16):
                for a_i, b_i in itertools.product((0, 1), repeat=2):
                    a = bus16(a_i, i, background)
                    b = bus16(b_i, i, background)
                    out = run("Mux16", a=a, b=b, sel=sel)
                    expected = bus16(b_i if sel else a_i, i, background)
                    ok &= check("Mux16", bus("out", out), expected, f"sel={sel},bit={i},bg={background},a_i={a_i},b_i={b_i}")
    report("Mux16", ok)
    return ok


def test_or8way():
    ok = True
    for bits in itertools.product((0, 1), repeat=8):
        out = run("Or8Way", **{"in": bits})
        expected = 1 if any(bits) else 0
        ok &= check("Or8Way", bit("out", out), expected, f"in={bits}")
    report("Or8Way", ok)
    return ok


ALL0 = (0,) * 16
ALL1 = (1,) * 16


def test_mux4way16():
    ok = True
    labels = ["a", "b", "c", "d"]
    for chosen in range(4):
        vals = [ALL0] * 4
        vals[chosen] = ALL1
        for sel in itertools.product((0, 1), repeat=2):
            index = sel[1] * 2 + sel[0]
            expected = ALL1 if index == chosen else ALL0
            out = run("Mux4Way16", a=vals[0], b=vals[1], c=vals[2], d=vals[3], sel=sel)
            ok &= check("Mux4Way16", bus("out", out), expected, f"chosen={labels[chosen]},sel={sel}")
    report("Mux4Way16", ok)
    return ok


def test_mux8way16():
    ok = True
    labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for chosen in range(8):
        vals = [ALL0] * 8
        vals[chosen] = ALL1
        for sel in itertools.product((0, 1), repeat=3):
            index = sel[2] * 4 + sel[1] * 2 + sel[0]
            expected = ALL1 if index == chosen else ALL0
            out = run(
                "Mux8Way16",
                a=vals[0], b=vals[1], c=vals[2], d=vals[3],
                e=vals[4], f=vals[5], g=vals[6], h=vals[7],
                sel=sel,
            )
            ok &= check("Mux8Way16", bus("out", out), expected, f"chosen={labels[chosen]},sel={sel}")
    report("Mux8Way16", ok)
    return ok


def test_dmux4way():
    ok = True
    for inp in (0, 1):
        for sel in itertools.product((0, 1), repeat=2):
            index = sel[1] * 2 + sel[0]
            expected = tuple(inp if k == index else 0 for k in range(4))
            out = run("DMux4Way", **{"in": inp, "sel": sel})
            got = (bit("a", out), bit("b", out), bit("c", out), bit("d", out))
            ok &= check("DMux4Way", got, expected, f"in={inp},sel={sel}")
    report("DMux4Way", ok)
    return ok


def test_dmux8way():
    ok = True
    for inp in (0, 1):
        for sel in itertools.product((0, 1), repeat=3):
            index = sel[2] * 4 + sel[1] * 2 + sel[0]
            expected = tuple(inp if k == index else 0 for k in range(8))
            out = run("DMux8Way", **{"in": inp, "sel": sel})
            got = tuple(bit(p, out) for p in "abcdefgh")
            ok &= check("DMux8Way", got, expected, f"in={inp},sel={sel}")
    report("DMux8Way", ok)
    return ok


def main():
    tests = [
        test_not, test_and, test_or, test_xor, test_mux, test_dmux,
        test_not16, test_and16, test_or16, test_mux16, test_or8way,
        test_mux4way16, test_mux8way16, test_dmux4way, test_dmux8way,
    ]
    results = [t() for t in tests]
    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} .hdl chips PASS")
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
