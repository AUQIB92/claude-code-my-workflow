# Lab 4 reference solutions — instructor-only

**Never sync this directory to `docs/` via `/deploy`.** It is a grading aid,
not student-facing material.

## Scope decision

The real Nand2Tetris Assembler and CPU Emulator are Java tools and cannot
run in this environment. `hack_interpreter.py` is an independent,
from-scratch Hack-assembly interpreter — not the real toolchain — used as
a correctness oracle for `Mult.asm` and `Fill.asm`, and to mechanically
cross-check the lab manual's hand-assembly worked example. It resolves
labels/variables (first pass) and executes A-/C-instructions directly from
their mnemonic text (second pass) rather than going through binary
encoding at execution time; `assemble()` (used only for the hand-assembly
cross-check) does perform the real bit-level encoding, via the standard
Hack `comp`/`dest`/`jump` tables.

Students still submit and are graded on programs run through the actual
CPU Emulator, per the lab manual's own instructions — this directory is a
design/grading aid, not a stand-in for that toolchain.

## Files

- `Mult.asm` — reference solution: `RAM[2] = RAM[0] * RAM[1]` via repeated
  addition, with early-exit short-circuits for `RAM[0]==0` or `RAM[1]==0`.
- `Fill.asm` — reference solution: polls `KBD` (24576); blackens the
  screen's 8192 memory-mapped words while a key is held, whitens it
  otherwise, via an inner `FILLLOOP` over a `SCREEN + i` address computed
  through a scratch `addr` variable (needed because a C-instruction's
  `dest=A` step would otherwise clobber the `D` register the color value
  is waiting in).
- `hack_interpreter.py` — the interpreter/oracle (see Scope decision).
- `hand_assembly_answer_key.md` — the completed 4-line hand-assembly
  table from the lab manual, with the bit-field derivation spelled out.
- `test_asm.py` — runs both programs and the hand-assembly cross-check.
  Run: `python test_asm.py` — expects `11/11 checks PASS`. Covers:
  `Mult.asm` over 8 representative `(a,b)` pairs including the `0` edge
  cases; `Fill.asm` filling all 8192 screen words black on key-press and
  all 8192 white on key-release (budgeted at 3 full inner-loop passes per
  stage, since a fixed step budget can land mid-loop under the *old*
  color before the new poll takes effect — this is a test-harness
  budgeting detail, not a bug in the assembly logic itself); the
  hand-assembly table's binary matching `assemble()`'s mechanical
  encoding.
