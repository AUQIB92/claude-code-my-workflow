# Lab 3 reference solutions — instructor-only

**Never sync this directory to `docs/` via `/deploy`.** It is a grading aid,
not student-facing material.

## Scope decision (read this first)

Labs 1-2's reference directories run real `.hdl` text through a small
custom interpreter (`hdl_simulator.py`). That interpreter is explicitly
combinational-only — its own docstring says clocked chips "would need a
tick/tock extension." Building that extension (gate-level clock-edge
semantics, feedback-loop handling for the DFF primitive itself) is a
substantial simulator-engineering task in its own right, well beyond a
single lab's instructor reference.

Instead, this reference is a **native-Python behavioural model**
(`chips.py`) that reproduces each chip's clocked *semantics* — a two-phase
`set_input()` / `tock()` discipline matching the real Hardware Simulator's
clock cycle — checked by hand-derived truth tables in `test_chips.py`,
rather than by re-deriving the logic from `.hdl` source. This is a lighter
verification bar than Labs 1-2's gate-tree interpretation, but it is
sufficient to (a) confirm the intended chip behaviour a student's `.hdl`
should match, and (b) give worked, testable truth tables for grading and
viva prep.

Students still submit and are graded on real `.hdl` files run through the
actual Nand2Tetris Hardware Simulator, per the lab manual's own
instructions — this directory is a design/grading aid, not a stand-in for
that toolchain.

## `chips.py` — the behavioural reference

- `DFF` — the sole sequential primitive: `set_input()` records what
  *would* be latched; `.out` only changes after `tock()`.
- `Bit`, `Register` — Task 1-2 (load-vs-hold 1-bit and 16-bit registers).
- `RAM8` → `RAM16K` — Task 3-5, one generic recursive `_RAMBase` class
  parametrized by fan-out (8, except RAM16K's 4-way top split) and child
  type, matching the syllabus's own recursive-composition instruction.
- `PC` — Task 6, with the `reset > load > inc > hold` priority order the
  lab manual and rubric both call out explicitly.

Bit-vector convention **departs from Lab 1/2's tuple convention**: values
here are plain Python `int`s in `[0, 65535]`, masked with `& 0xFFFF` after
arithmetic — the natural representation for RAM/PC addresses and data
words, and it avoids constant tuple↔int conversion in the address-decode
logic. This is a deliberate, documented choice, not an inconsistency.

## `test_chips.py`

Run: `python test_chips.py` — expects `20/20 checks PASS`. Covers:
`DFF` load/hold-before-tock; `Bit` load/hold; `Register` load/hold;
`RAM8` exhaustive over all 8 addresses plus a targeted no-disturbance
check; `RAM64` spot-checked across `RAM8`-child boundaries; `RAM512`/
`RAM4K` spot-checked (deeper recursion, same proven pattern, checked
lightly to keep instantiation cost down — `RAM4K` alone instantiates
4096 `Register`s = 65536 `Bit` objects); `RAM16K` spot-checked across
all 4 top-level children (confirming the 4-way, not 8-way, split);
`PC`'s full `reset > load > inc > hold` priority chain.
