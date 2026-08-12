"""
chips.py -- Instructor-only Python reference oracle for CS401 Lab 2
(Boolean Arithmetic & the ALU, Nand2Tetris Project 2).

NOT literal HDL. This is an independent from-scratch reimplementation of
each chip's intended behavior, built compositionally from the Lab 1 gate
library (which itself reduces to a single NAND primitive) -- used as a
correctness oracle for grading, since the real Nand2Tetris Hardware
Simulator (Java) cannot run in this environment.

Bit-vector convention: every multi-bit value (in[16]) is a tuple of ints
(0/1) with index 0 = the least-significant bit, matching the low-to-high
pin-array indexing used in the official Nand2Tetris chip API.

Never synced to docs/ by /deploy -- instructor-only.
"""


def NAND(a, b):
    return 1 - (a & b)


def NOT(a):
    return NAND(a, a)


def AND(a, b):
    return NOT(NAND(a, b))


def OR(a, b):
    return NAND(NOT(a), NOT(b))


def XOR(a, b):
    return OR(AND(a, NOT(b)), AND(NOT(a), b))


def MUX(a, b, sel):
    return OR(AND(a, NOT(sel)), AND(b, sel))


def DMUX(inp, sel):
    a = AND(inp, NOT(sel))
    b = AND(inp, sel)
    return a, b


def NOT16(inp):
    return tuple(NOT(b) for b in inp)


def AND16(a, b):
    return tuple(AND(x, y) for x, y in zip(a, b))


def OR16(a, b):
    return tuple(OR(x, y) for x, y in zip(a, b))


def MUX16(a, b, sel):
    return tuple(MUX(x, y, sel) for x, y in zip(a, b))


def OR8WAY(inp):
    result = 0
    for bit in inp:
        result = OR(result, bit)
    return result


def MUX4WAY16(a, b, c, d, sel):
    ab = MUX16(a, b, sel[0])
    cd = MUX16(c, d, sel[0])
    return MUX16(ab, cd, sel[1])


def MUX8WAY16(a, b, c, d, e, f, g, h, sel):
    abcd = MUX4WAY16(a, b, c, d, (sel[0], sel[1]))
    efgh = MUX4WAY16(e, f, g, h, (sel[0], sel[1]))
    return MUX16(abcd, efgh, sel[2])


def DMUX4WAY(inp, sel):
    ab_in, cd_in = DMUX(inp, sel[1])
    a, b = DMUX(ab_in, sel[0])
    c, d = DMUX(cd_in, sel[0])
    return a, b, c, d


def DMUX8WAY(inp, sel):
    abcd_in, efgh_in = DMUX(inp, sel[2])
    a, b, c, d = DMUX4WAY(abcd_in, (sel[0], sel[1]))
    e, f, g, h = DMUX4WAY(efgh_in, (sel[0], sel[1]))
    return a, b, c, d, e, f, g, h


# ---------------------------------------------------------------------------
# Lab 2: Boolean Arithmetic & the ALU
# ---------------------------------------------------------------------------

ZERO16 = (0,) * 16
ONE16 = (1,) + (0,) * 15


def HALFADDER(a, b):
    s = XOR(a, b)
    c = AND(a, b)
    return s, c


def FULLADDER(a, b, cin):
    s1, c1 = HALFADDER(a, b)
    s, c2 = HALFADDER(s1, cin)
    c = OR(c1, c2)
    return s, c


def ADD16(a, b):
    result = []
    carry = 0
    for ai, bi in zip(a, b):
        s, carry = FULLADDER(ai, bi, carry)
        result.append(s)
    return tuple(result)


def INC16(a):
    return ADD16(a, ONE16)


def ALU(x, y, zx, nx, zy, ny, f, no):
    if zx:
        x = ZERO16
    if nx:
        x = NOT16(x)
    if zy:
        y = ZERO16
    if ny:
        y = NOT16(y)
    if f:
        out = ADD16(x, y)
    else:
        out = AND16(x, y)
    if no:
        out = NOT16(out)
    zr = 1 if out == ZERO16 else 0
    ng = out[15]
    return out, zr, ng
