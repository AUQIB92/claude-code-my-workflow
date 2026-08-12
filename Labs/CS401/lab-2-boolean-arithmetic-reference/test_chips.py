"""
test_chips.py -- Self-check for chips.py (CS401 Lab 2 reference oracle).

Checks every chip against a native-Python reformulation of its spec
(integer arithmetic / bitwise ops on Python ints, converted to/from the
16-bit two's-complement bit-tuple representation) -- an INDEPENDENT
oracle, not chips.py's own composition, so a shared bug wouldn't
silently validate itself.

HalfAdder/FullAdder: exhaustive (4/8 input combinations). Add16/Inc16:
a representative set of value pairs covering zero, +-1, max/min
16-bit values, and carry-propagation-stress patterns, checked as exact
mod-2^16 integer arithmetic. ALU: exhaustive over all 64 control-bit
combinations (the ALU's logic is well-defined for every combination,
not just the 18 named operations) crossed with a representative set of
x,y value pairs, checked against an independently-written formula for
the official zx/nx/zy/ny/f/no semantics -- the "no shortcuts" standard
the real ALU-nostat.tst enforces.

Fails loudly: prints PASS/FAIL per chip, exits non-zero on any failure.
Run with: python test_chips.py
"""

import itertools
import sys

from chips import ADD16, ALU, FULLADDER, HALFADDER, INC16

failures = []


def check(name, got, expected, context):
    if got != expected:
        failures.append(f"{name}: FAIL at {context} -- got {got}, expected {expected}")
        return False
    return True


def report(name, ok):
    print(f"{'PASS' if ok else 'FAIL'}: {name}")


def to_bits16(v):
    v &= 0xFFFF
    return tuple((v >> i) & 1 for i in range(16))


def to_unsigned(bits):
    return sum(b << i for i, b in enumerate(bits))


def test_half_adder():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        expected = (a ^ b, a & b)
        ok &= check("HalfAdder", HALFADDER(a, b), expected, f"a={a},b={b}")
    report("HalfAdder", ok)
    return ok


def test_full_adder():
    ok = True
    for a, b, cin in itertools.product((0, 1), repeat=3):
        total = a + b + cin
        expected = (total & 1, 1 if total >= 2 else 0)
        ok &= check("FullAdder", FULLADDER(a, b, cin), expected, f"a={a},b={b},cin={cin}")
    report("FullAdder", ok)
    return ok


REPRESENTATIVE_VALUES = [
    0, 1, -1, 2, -2, 100, -100,
    0x7FFF, -0x8000,          # max positive / min negative 16-bit
    0x00FF, 0x0001, 0xFFFF,   # carry-propagation stress patterns
    0x0100, 0x0080, 0x1234, -0x1234,
]


def test_add16():
    ok = True
    for x in REPRESENTATIVE_VALUES:
        for y in REPRESENTATIVE_VALUES:
            a, b = to_bits16(x), to_bits16(y)
            expected = to_bits16(x + y)
            got = ADD16(a, b)
            ok &= check("Add16", got, expected, f"x={x},y={y}")
    report("Add16", ok)
    return ok


def test_inc16():
    ok = True
    for x in REPRESENTATIVE_VALUES:
        a = to_bits16(x)
        expected = to_bits16(x + 1)
        got = INC16(a)
        ok &= check("Inc16", got, expected, f"x={x}")
    report("Inc16", ok)
    return ok


def alu_formula(x, y, zx, nx, zy, ny, f, no):
    """Independent reformulation of the ALU spec in plain Python ints."""
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


ALU_TEST_VALUES = [0, 1, -1, 17, -17, 3, 0x7FFF, -0x8000, 0x00FF, -0x00FF]


def test_alu():
    ok = True
    for zx, nx, zy, ny, f, no in itertools.product((0, 1), repeat=6):
        for xv in ALU_TEST_VALUES:
            for yv in ALU_TEST_VALUES:
                x, y = to_bits16(xv), to_bits16(yv)
                out, zr, ng = ALU(x, y, zx, nx, zy, ny, f, no)
                got = (to_unsigned(out), zr, ng)
                exp_out, exp_zr, exp_ng = alu_formula(xv & 0xFFFF, yv & 0xFFFF, zx, nx, zy, ny, f, no)
                expected = (exp_out, exp_zr, exp_ng)
                ok &= check("ALU", got, expected, f"zx{zx}nx{nx}zy{zy}ny{ny}f{f}no{no},x={xv},y={yv}")
    report("ALU", ok)
    return ok


def main():
    tests = [test_half_adder, test_full_adder, test_add16, test_inc16, test_alu]
    results = [t() for t in tests]
    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} chips PASS")
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
