# Lab 5 reference solutions — instructor-only

**Never sync this directory to `docs/` via `/deploy`.** It is a grading aid,
not student-facing material.

## Scope decision

As with Labs 3-4, the real Nand2Tetris Hardware Simulator (Java) cannot
run in this environment. `cpu_reference.py` is a from-scratch, bit-level
behavioural model of `CPU.hdl`/`Memory.hdl`/`Computer.hdl` — it decodes
the actual 16-bit instruction word (`a`, `comp`, `dest`, `jump` fields)
exactly as the lab manual's Task 1 specifies, unlike Lab 4's
`hack_interpreter.py`, which executes assembly at the mnemonic level.
This is deliberate: running Lab 4's `Mult.asm`/`Fill.asm` through this
independent, bit-level decoder and getting the *same* answer Lab 4's
mnemonic-level interpreter got is real cross-checked evidence the decode
logic (what a student's `CPU.hdl` actually implements) is correct — not
just that "some interpreter can run Hack assembly."

Students still submit and are graded on real `.hdl` files run through the
actual Hardware Simulator, per the lab manual's own instructions — this
directory is a design/grading aid, not a stand-in for that toolchain.

## Files

- `cpu_reference.py` — `alu()` (the Lab 2 ALU, reimplemented on plain
  ints rather than bit-tuples, since the CPU model works in 16-bit int
  words throughout), `CPU` (Task 1: `combinational()` computes this
  cycle's `addressM`/`outM`/`writeM` and next-state A/D/PC from the
  current instruction and `inM`, without committing them; `tock()`
  commits — the same two-phase discipline as Lab 3's `chips.py`),
  `Memory` (Task 2: address-range routing to RAM/Screen/Keyboard), and
  `Computer` (Task 3: wires ROM + CPU + Memory together, one `step()`
  per clock cycle).
- `test_cpu.py` — assembles Lab 4's `Mult.asm`/`Fill.asm` (via Lab 4's
  own `assemble()`, imported by relative path — Lab 5 does not duplicate
  the assembler) and re-runs them through this bit-level `Computer`
  model, reproducing Lab 4's `test_asm.py` results by a completely
  different code path, plus a direct agreement check between the two
  models on three additional `(a,b)` pairs. Run: `python test_cpu.py` —
  expects `11/11 checks PASS`.

## Datapath diagram

The lab manual's own Figure `fig:lab5-cpu` (in
`Labs/CS401/lab-5-cpu-computer.tex`) is the block-level datapath diagram
this lab's journal deliverable asks students to redraw fully wired — this
reference directory does not duplicate it; `cpu_reference.py`'s field
comments (`a`, `comp`, `dest`, `jump` bit positions) are the bit-level
complement to that diagram.
