"""
test_chips.py -- Self-check for chips.py (CS401 Lab 1 reference oracle).

Checks every chip against Python's native bitwise operators (&, |, ^, not)
as an independent ground-truth oracle -- NOT against chips.py's own NAND
composition, which would be circular. Exhaustive truth-table enumeration
for every chip whose input space is small enough (all 1-2-bit gates,
Mux/DMux, Or8Way's 2**8 = 256 combinations); for the 16-bit-bus chips,
exhaustive per-bit-position + background-pattern coverage instead of a
literal 2**16 sweep (see per-test docstrings for the exact strategy).

Fails loudly: prints PASS/FAIL per chip, exits non-zero on any failure.
Run with: python test_chips.py
"""

import itertools
import sys

from chips import (
    AND, AND16, DMUX, DMUX4WAY, DMUX8WAY, MUX, MUX4WAY16, MUX8WAY16,
    MUX16, NAND, NOT, NOT16, OR, OR16, OR8WAY, XOR,
)

failures = []


def check(name, got, expected, context):
    if got != expected:
        failures.append(f"{name}: FAIL at {context} -- got {got}, expected {expected}")
        return False
    return True


def report(name, ok):
    print(f"{'PASS' if ok else 'FAIL'}: {name}")


# ---------------------------------------------------------------------------
# 1-bit gates: exhaustive over all 2**n input combinations.
# ---------------------------------------------------------------------------

def test_nand():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        expected = 0 if (a and b) else 1
        ok &= check("Nand", NAND(a, b), expected, f"a={a},b={b}")
    report("Nand", ok)
    return ok


def test_not():
    ok = True
    for a in (0, 1):
        expected = 1 - a
        ok &= check("Not", NOT(a), expected, f"a={a}")
    report("Not", ok)
    return ok


def test_and():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        expected = a & b
        ok &= check("And", AND(a, b), expected, f"a={a},b={b}")
    report("And", ok)
    return ok


def test_or():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        expected = a | b
        ok &= check("Or", OR(a, b), expected, f"a={a},b={b}")
    report("Or", ok)
    return ok


def test_xor():
    ok = True
    for a, b in itertools.product((0, 1), repeat=2):
        expected = a ^ b
        ok &= check("Xor", XOR(a, b), expected, f"a={a},b={b}")
    report("Xor", ok)
    return ok


def test_mux():
    ok = True
    for a, b, sel in itertools.product((0, 1), repeat=3):
        expected = b if sel else a
        ok &= check("Mux", MUX(a, b, sel), expected, f"a={a},b={b},sel={sel}")
    report("Mux", ok)
    return ok


def test_dmux():
    ok = True
    for inp, sel in itertools.product((0, 1), repeat=2):
        expected = (inp, 0) if sel == 0 else (0, inp)
        ok &= check("DMux", DMUX(inp, sel), expected, f"in={inp},sel={sel}")
    report("DMux", ok)
    return ok


# ---------------------------------------------------------------------------
# 16-bit-bus gates: per-bit-position + background-pattern coverage.
# Each of the 16 bit positions is verified against every 1-bit truth-table
# row while every OTHER bit is held first at an all-0 background, then an
# all-1 background -- this proves both per-bit correctness AND that no
# bit position leaks into/depends on another (bus independence), without
# needing a literal 2**16 sweep.
# ---------------------------------------------------------------------------

def bus16(value_at_i, i, background):
    return tuple(value_at_i if k == i else background for k in range(16))


def test_not16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i in (0, 1):
                a = bus16(a_i, i, background)
                expected = bus16(1 - a_i, i, 1 - background)
                got = NOT16(a)
                ok &= check("Not16", got, expected, f"bit={i},bg={background},a_i={a_i}")
    report("Not16", ok)
    return ok


def test_and16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i, b_i in itertools.product((0, 1), repeat=2):
                a = bus16(a_i, i, background)
                b = bus16(b_i, i, background)
                expected = bus16(a_i & b_i, i, background & background)
                got = AND16(a, b)
                ok &= check("And16", got, expected, f"bit={i},bg={background},a_i={a_i},b_i={b_i}")
    report("And16", ok)
    return ok


def test_or16():
    ok = True
    for background in (0, 1):
        for i in range(16):
            for a_i, b_i in itertools.product((0, 1), repeat=2):
                a = bus16(a_i, i, background)
                b = bus16(b_i, i, background)
                expected = bus16(a_i | b_i, i, background | background)
                got = OR16(a, b)
                ok &= check("Or16", got, expected, f"bit={i},bg={background},a_i={a_i},b_i={b_i}")
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
                    bg_out = b_i if sel and False else background  # backgrounds equal on both buses
                    expected = bus16(b_i if sel else a_i, i, background)
                    got = MUX16(a, b, sel)
                    ok &= check("Mux16", got, expected, f"sel={sel},bit={i},bg={background},a_i={a_i},b_i={b_i}")
    report("Mux16", ok)
    return ok


def test_or8way():
    ok = True
    for bits in itertools.product((0, 1), repeat=8):
        expected = 1 if any(bits) else 0
        ok &= check("Or8Way", OR8WAY(bits), expected, f"in={bits}")
    report("Or8Way", ok)
    return ok


# ---------------------------------------------------------------------------
# Wide multiplexers/demultiplexers: exhaustive over sel, with each data
# input given a distinct all-same-bit 16-bit pattern so routing is
# unambiguous (e.g. a=0000...0, b=1111...1, c=0000...0 at a shifted lane,
# etc. -- here we just use the constant patterns 0x0/0x1/0x2/.../0x7 broadcast
# to all 16 bits isn't distinct per bit, so instead tag each input with its
# own constant all-1 or all-0 pattern and confirm the selected one is the
# only one that can appear in the output).
# ---------------------------------------------------------------------------

ALL0 = (0,) * 16
ALL1 = (1,) * 16


def test_mux4way16():
    ok = True
    inputs = {"a": ALL1, "b": ALL0, "c": ALL1, "d": ALL0}
    # distinguish same-valued neighbours by testing each input as the
    # unique ALL1 among three ALL0 siblings, one at a time.
    labels = ["a", "b", "c", "d"]
    for chosen in range(4):
        vals = [ALL0] * 4
        vals[chosen] = ALL1
        for sel in itertools.product((0, 1), repeat=2):
            index = sel[1] * 2 + sel[0]  # sel[1] MSB, sel[0] LSB per official API
            expected = ALL1 if index == chosen else ALL0
            got = MUX4WAY16(*vals, sel)
            ok &= check("Mux4Way16", got, expected, f"chosen={labels[chosen]},sel={sel}")
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
            got = MUX8WAY16(*vals, sel)
            ok &= check("Mux8Way16", got, expected, f"chosen={labels[chosen]},sel={sel}")
    report("Mux8Way16", ok)
    return ok


def test_dmux4way():
    ok = True
    for inp in (0, 1):
        for sel in itertools.product((0, 1), repeat=2):
            index = sel[1] * 2 + sel[0]
            expected = tuple(inp if k == index else 0 for k in range(4))
            got = DMUX4WAY(inp, sel)
            ok &= check("DMux4Way", got, expected, f"in={inp},sel={sel}")
    report("DMux4Way", ok)
    return ok


def test_dmux8way():
    ok = True
    for inp in (0, 1):
        for sel in itertools.product((0, 1), repeat=3):
            index = sel[2] * 4 + sel[1] * 2 + sel[0]
            expected = tuple(inp if k == index else 0 for k in range(8))
            got = DMUX8WAY(inp, sel)
            ok &= check("DMux8Way", got, expected, f"in={inp},sel={sel}")
    report("DMux8Way", ok)
    return ok


def main():
    tests = [
        test_nand, test_not, test_and, test_or, test_xor, test_mux, test_dmux,
        test_not16, test_and16, test_or16, test_mux16, test_or8way,
        test_mux4way16, test_mux8way16, test_dmux4way, test_dmux8way,
    ]
    results = [t() for t in tests]
    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} chips PASS")
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
