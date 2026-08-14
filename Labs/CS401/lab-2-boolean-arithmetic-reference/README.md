# Lab 2 reference solutions — instructor-only

**Never sync this directory to `docs/` via `/deploy`.** It is a grading aid,
not student-facing material.

## `hdl/` — the actual reference solutions

Real Nand2Tetris HDL for `HalfAdder`, `FullAdder`, `Add16`, `Inc16`, and
`ALU` (the 5 new Lab 2 chips), plus copies of the 9 Lab 1 gates this lab's
chips depend on (`Not`, `And`, `Or`, `Xor`, `Mux`, `Not16`, `And16`, `Mux16`,
`Or8Way`) — each lab's reference directory is self-contained.

`ALU.hdl` implements the literal 18-operation spec (zero/negate x and y,
add-vs-and via `f`, negate via `no`) rather than a lookup table, matching
the rubric's "adders correctly reused... no redundant gates" criterion.
`Inc16.hdl` and `ALU.hdl` use the `true`/`false` constant literals, which
required a small addition to `hdl_simulator.py` beyond Lab 1's version
(see its docstring).

`ALU.hdl`'s `zr`/`ng` computation originally read bits back off its own
already-written `out` pin via a separate part invocation — this interpreter
accepted it, but the real Hardware Simulator does not (an OUT pin is
write-only within the chip that declares it). Fixed to the canonical form:
the final `Mux16` fans its result out to `out`, `outLow`, `outHigh`, and
`ng` all in one invocation (`out=out, out[0..7]=outLow, out[8..15]=outHigh,
out[15]=ng`), which required extending `hdl_simulator.py` to support LHS
(part-output) pin slicing — the same part-pin can now appear multiple
times in one call, sliced differently each time.

- `hdl_simulator.py` — the minimal HDL interpreter (own copy, extended
  with `true`/`false` literal support and LHS output-pin slicing for this
  lab's needs — see its docstring for both).
- `test_hdl.py` — runs every chip through the interpreter and checks it
  against an independently-written native-Python reformulation of the
  spec (not against `chips.py`). `HalfAdder`/`FullAdder` are exhaustive;
  `Add16`/`Inc16` use a representative value set; `ALU` is exhaustive over
  all 64 control-bit combinations (the logic is well-defined for all of
  them, not just the 18 named operations) crossed with a representative
  x,y set. Run: `python test_hdl.py` — expects `5/5 .hdl chips PASS`.

## `chips.py` — the Python design reference

A parallel pure-Python implementation, checked against the same
independent oracle as `hdl/`. `test_chips.py` uses a larger x,y sample for
the ALU check since it runs much faster than the HDL interpreter (no gate
tree to re-walk on every call). Run: `python test_chips.py` — expects
`5/5 chips PASS`.
