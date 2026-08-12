"""
test_hdl.py -- executes the actual hdl/*.hdl files (the real submittable
artifacts) via hdl_simulator.py and checks them against an independent
native-Python reformulation of each chip's spec -- the same oracle
test_chips.py uses, so both the Python reference (chips.py) and the
HDL reference (hdl/*.hdl) are checked against the same standard, not
against each other.

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
    input_bits = {}
    for k, v in inputs.items():
        input_bits[k] = [v] if isinstance(v, int) else list(v)
    return eval_chip(HDL_DIR, chip, input_bits)


def to_bits16(v):
    v &= 0xFFFF
    return [(v >> i) & 1 for i in range(16)]


def to_unsigned(bits):
    return sum(b << i for i, b in enumerate(bits))


def test_half_adder():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        out = run("HalfAdder", a=a, b=b)
        expected = (a ^ b, a & b)
        got = (out["sum"][0], out["carry"][0])
        ok &= check("HalfAdder", got, expected, f"a={a},b={b}")
    report("HalfAdder", ok)
    return ok


def test_full_adder():
    ok = True
    for a, b, c in itertools.product((0, 1), repeat=3):
        out = run("FullAdder", a=a, b=b, c=c)
        total = a + b + c
        expected = (total & 1, 1 if total >= 2 else 0)
        got = (out["sum"][0], out["carry"][0])
        ok &= check("FullAdder", got, expected, f"a={a},b={b},c={c}")
    report("FullAdder", ok)
    return ok


REPRESENTATIVE_VALUES = [
    0, 1, -1, 2, -2, 100, -100,
    0x7FFF, -0x8000,
    0x00FF, 0x0001, 0xFFFF,
    0x0100, 0x0080, 0x1234, -0x1234,
]


def test_add16():
    ok = True
    for x in REPRESENTATIVE_VALUES:
        for y in REPRESENTATIVE_VALUES:
            out = run("Add16", a=to_bits16(x), b=to_bits16(y))
            expected = to_bits16(x + y)
            got = out["out"]
            ok &= check("Add16", got, expected, f"x={x},y={y}")
    report("Add16", ok)
    return ok


def test_inc16():
    ok = True
    for x in REPRESENTATIVE_VALUES:
        out = run("Inc16", **{"in": to_bits16(x)})
        expected = to_bits16(x + 1)
        got = out["out"]
        ok &= check("Inc16", got, expected, f"x={x}")
    report("Inc16", ok)
    return ok


def alu_formula(x, y, zx, nx, zy, ny, f, no):
    if zx:
        x = 0
    if nx:
        x = (~x) & 0xFFFF
    if zy:
        y = 0
    if ny:
        y = (~y) & 0xFFFF
    if f:
        out = (x + y) & 0xFFFF
    else:
        out = x & y
    if no:
        out = (~out) & 0xFFFF
    zr = 1 if out == 0 else 0
    ng = 1 if out & 0x8000 else 0
    return out, zr, ng


# Smaller than test_chips.py's set -- the HDL interpreter re-walks the
# full gate tree (down to Nand) on every call with no value memoization,
# so this is a deliberate cost/coverage tradeoff. The control-bit space
# stays fully exhaustive (all 64 combinations); only the x,y sample
# count shrinks, and the logic itself was already proven exhaustively
# by test_chips.py's larger sample -- this file's job is to confirm the
# real .hdl artifact matches, not to re-discover a bug class no test
# above it could have caught.
ALU_TEST_VALUES = [0, 1, -1, 17, -17, 0x7FFF]


def test_alu():
    ok = True
    for zx, nx, zy, ny, f, no in itertools.product((0, 1), repeat=6):
        for xv in ALU_TEST_VALUES:
            for yv in ALU_TEST_VALUES:
                out = run(
                    "ALU",
                    x=to_bits16(xv), y=to_bits16(yv),
                    zx=zx, nx=nx, zy=zy, ny=ny, f=f, no=no,
                )
                got = (to_unsigned(out["out"]), out["zr"][0], out["ng"][0])
                expected = alu_formula(xv & 0xFFFF, yv & 0xFFFF, zx, nx, zy, ny, f, no)
                ok &= check("ALU", got, expected, f"zx{zx}nx{nx}zy{zy}ny{ny}f{f}no{no},x={xv},y={yv}")
    report("ALU", ok)
    return ok


def main():
    tests = [test_half_adder, test_full_adder, test_add16, test_inc16, test_alu]
    results = [t() for t in tests]
    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} .hdl chips PASS")
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures[:20]:
            print(f"  {f}")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
