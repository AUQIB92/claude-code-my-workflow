"""
chips.py -- Instructor-only Python reference oracle for CS401 Lab 1
(Boolean Logic & Elementary Gates, Nand2Tetris Project 1).

NOT literal HDL. This is an independent from-scratch reimplementation of
each chip's intended behavior, built compositionally from a single NAND
primitive -- the same "everything from Nand" pedagogy the lab teaches --
used as a correctness oracle for grading, since the real Nand2Tetris
Hardware Simulator (Java) cannot run in this environment.

Bit-vector convention: every multi-bit value (in[16], sel[2], sel[3],
in[8]) is a tuple of ints (0/1) with index 0 = the least-significant /
first select bit, matching the low-to-high pin-array indexing used in
the official Nand2Tetris chip API.

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
