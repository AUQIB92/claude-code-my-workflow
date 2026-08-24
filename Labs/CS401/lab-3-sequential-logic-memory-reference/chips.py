"""
chips.py -- Instructor-only Python reference oracle for CS401 Lab 3
(Sequential Logic & Memory, Nand2Tetris Project 3).

NOT literal HDL. This is an independent from-scratch behavioural model of
each chip's clocked semantics, used as a correctness oracle for grading,
since the real Nand2Tetris Hardware Simulator (Java) cannot run in this
environment and Lab 1/2's combinational hdl_simulator.py has no clock/state
support (see its own docstring, line 4: "would need a tick/tock extension").
Rather than extend that interpreter for stateful chips (a large undertaking
for one instructor reference), this lab's oracle is a native-Python
behavioural model, checked by hand-derived truth tables in test_chips.py.

Two-phase clock discipline, matching the real Nand2Tetris semantics:
  1. set_input(...)  -- combinational: compute what WOULD be latched, given
     current inputs and current (pre-tock) state. Safe to call repeatedly
     with different trial inputs before committing (mirrors combinational
     settling within a clock phase).
  2. tock()           -- commit: latch the computed next-state into out.
     Only after tock() does .out reflect the new value.

Bit-vector convention (departs from Lab 1/2's tuple convention -- noted in
README.md): every 16-bit value here is a plain Python int in [0, 65535],
masked with & 0xFFFF after every arithmetic op. This is the natural
representation for RAM/PC address and data words and avoids constant
tuple<->int conversion in the address-decode logic below.

Never synced to docs/ by /deploy -- instructor-only.
"""

MASK16 = 0xFFFF


def bit(value, i):
    """Extract bit i (0 = LSB) from a 16-bit int."""
    return (value >> i) & 1


# ---------------------------------------------------------------------------
# DFF -- the sole sequential primitive (single bit, supplied, not built here)
# ---------------------------------------------------------------------------

class DFF:
    def __init__(self):
        self.out = 0
        self._next = 0

    def set_input(self, in_bit):
        self._next = in_bit & 1

    def tock(self):
        self.out = self._next


# ---------------------------------------------------------------------------
# Bit / Register -- Lab 3, Task 1-2
# ---------------------------------------------------------------------------

class Bit:
    """1-bit register: out(t+1) = load(t) ? in(t) : out(t)."""

    def __init__(self):
        self.dff = DFF()

    @property
    def out(self):
        return self.dff.out

    def set_input(self, in_bit, load):
        # Mux: feed in_bit if loading, else feed back the DFF's own current
        # output (hold). This mirrors the HDL's Mux(dff.out, in, load) -> dff.in.
        self.dff.set_input(in_bit if load else self.dff.out)

    def tock(self):
        self.dff.tock()


class Register:
    """16-bit register: 16 independent Bit chips sharing one load line."""

    def __init__(self):
        self.bits = [Bit() for _ in range(16)]

    @property
    def out(self):
        v = 0
        for i, b in enumerate(self.bits):
            v |= (b.out << i)
        return v & MASK16

    def set_input(self, in_value, load):
        for i, b in enumerate(self.bits):
            b.set_input(bit(in_value, i), load)

    def tock(self):
        for b in self.bits:
            b.tock()


# ---------------------------------------------------------------------------
# RAM8 / RAM64 / RAM512 / RAM4K / RAM16K -- Lab 3, Task 3-5
# Recursive pattern: RAM(n) = 8 (or 4, for the top level of RAM16K) x
# RAM(n/8) [or RAM(n/4)], address-selected via a DMux/Mux equivalent.
# ---------------------------------------------------------------------------

class _RAMBase:
    """Generic recursive RAM: `fan` children of type `child_cls`, address
    split into (high bits selecting the child, low bits passed through)."""

    fan = 8          # number of children (8 for all but RAM16K's top level)
    child_cls = None  # Register for RAM8; a smaller RAM class otherwise
    addr_bits = None  # total address width for this level

    def __init__(self):
        self.children = [self.child_cls() for _ in range(self.fan)]
        self._selected = 0

    def _split(self, address):
        low_bits = self.addr_bits - (self.fan - 1).bit_length()
        high = address >> low_bits
        low = address & ((1 << low_bits) - 1)
        return high, low

    @property
    def out(self):
        # Read is combinational: whichever child is currently addressed
        # drives out every cycle (no clock needed to read).
        return self.children[self._selected].out

    def set_input(self, in_value, load, address):
        high, low = self._split(address)
        self._selected = high
        for i, child in enumerate(self.children):
            child_load = load if (i == high) else 0
            if isinstance(child, Register):
                child.set_input(in_value, child_load)
            else:
                child.set_input(in_value, child_load, low)

    def tock(self):
        for child in self.children:
            child.tock()


class RAM8(_RAMBase):
    fan = 8
    child_cls = Register
    addr_bits = 3


class RAM64(_RAMBase):
    fan = 8
    child_cls = RAM8
    addr_bits = 6


class RAM512(_RAMBase):
    fan = 8
    child_cls = RAM64
    addr_bits = 9


class RAM4K(_RAMBase):
    fan = 8
    child_cls = RAM512
    addr_bits = 12


class RAM16K(_RAMBase):
    # Only 16384 = 4 x 4096 registers -> a 4-way (not 8-way) top split,
    # matching the syllabus's note that RAM16K uses DMux4Way/Mux4Way16.
    fan = 4
    child_cls = RAM4K
    addr_bits = 14


# ---------------------------------------------------------------------------
# PC -- Lab 3, Task 6
# ---------------------------------------------------------------------------

class PC:
    """Program counter: reset > load > inc > hold, in that priority order."""

    def __init__(self):
        self.register = Register()

    @property
    def out(self):
        return self.register.out

    def set_input(self, in_value, load, inc, reset):
        current = self.register.out
        if reset:
            next_value = 0
        elif load:
            next_value = in_value & MASK16
        elif inc:
            next_value = (current + 1) & MASK16
        else:
            next_value = current
        self.register.set_input(next_value, load=1)  # always "load" the computed next value

    def tock(self):
        self.register.tock()
