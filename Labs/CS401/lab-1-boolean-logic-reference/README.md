# Lab 1 reference solutions — instructor-only

**Never sync this directory to `docs/` via `/deploy`.** It is a grading aid,
not student-facing material.

## `hdl/` — the actual reference solutions

`hdl/*.hdl` are real Nand2Tetris HDL reference solutions for all 15 Lab 1
chips, written in the syntax confirmed against `syllabi/Hardware_Simulator_Tutorial.pdf`
(CHIP/IN/OUT/PARTS, `pin=value` connections, `bus[i]`/`bus[lo..hi]` slicing,
`BUILTIN Nand` as the sole primitive). These are the files a student would
load into the real Nand2Tetris Hardware Simulator — the same tool referenced
in the lab manual's Toolchain Setup section.

Since the real Java Hardware Simulator can't run in this environment, these
`.hdl` files are executed and verified here with a small custom interpreter:

- `hdl_simulator.py` — parses and evaluates Nand2Tetris HDL (combinational
  chips only, sufficient for Lab 1). Recursively resolves `PARTS` wiring,
  including bus-range slicing, with `Nand` as the only true primitive.
- `test_hdl.py` — runs every chip in `hdl/` through the interpreter and
  checks it against Python's native bitwise operators as an independent
  ground-truth oracle. Run: `python test_hdl.py` — expects
  `15/15 .hdl chips PASS`, exit code 0.

## `chips.py` — the Python design reference

A parallel pure-Python implementation of the same 15 chips, also built
compositionally from a single `NAND` primitive. Useful as a readable design
blueprint (no HDL parsing involved) and as a second, independent
correctness check — `chips.py`/`test_chips.py` and `hdl/`/`test_hdl.py` are
checked against the *same* oracle (Python's native bitwise operators), not
against each other, so a shared bug in one wouldn't silently validate the
other.

Run: `python test_chips.py` — expects `16/16 chips PASS` (15 chips + the
`NAND` primitive itself), exit code 0.
