"""
test_cpu.py -- runs Lab 4's Mult.asm and Fill.asm through the Lab 5
bit-level CPU/Memory/Computer model (cpu_reference.py), as the lab manual's
own Task 4 instructs ("load Mult.asm and Fill.asm from Lab 4 onto the
built Computer and confirm they still run correctly on your own CPU").

This assembles the .asm source using Lab 4's own assemble() (imported via
a relative path -- see the sys.path note below) and re-derives the exact
same RAM[2]/screen results Lab 4's test_asm.py already proved via
mnemonic-level execution, but this time via bit-level instruction decode
-- an independent cross-check of the decode logic students' CPU.hdl must
implement.

Run: python test_cpu.py
Expects: "N/N checks PASS"
"""

import sys
import os

# Lab 4's reference folder holds the only assembler in this repo (Lab 5
# does not duplicate it) -- import it via a relative sibling path.
_LAB4_REF = os.path.join(os.path.dirname(__file__), "..",
                          "lab-4-machine-language-programming-reference")
sys.path.insert(0, os.path.abspath(_LAB4_REF))

from hack_interpreter import parse, resolve_symbols, assemble  # noqa: E402
from cpu_reference import Computer, MASK  # noqa: E402

PASS = []
FAIL = []


def check(name, condition, detail=""):
    if condition:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: {detail}")


def assemble_file(path):
    with open(path) as f:
        instructions, labels = parse(f.readlines())
    symbols = resolve_symbols(instructions, labels)
    return [int(assemble(instr, symbols), 2) for instr in instructions]


# ---------------------------------------------------------------------------
# Mult.asm on the bit-level Computer model
# ---------------------------------------------------------------------------

mult_rom = assemble_file(os.path.join(_LAB4_REF, "Mult.asm"))

for a, b in [(0, 0), (0, 5), (5, 0), (1, 1), (3, 4), (7, 6), (12, 12), (255, 2)]:
    computer = Computer(mult_rom)
    computer.memory.ram[0] = a
    computer.memory.ram[1] = b
    computer.run(max_steps=20000)
    expected = (a * b) & MASK
    check(f"Computer running Mult.hack: {a} x {b} = {expected}",
          computer.memory.ram.get(2, 0) == expected,
          f"got RAM[2]={computer.memory.ram.get(2, 0)}")

# ---------------------------------------------------------------------------
# Fill.asm on the bit-level Computer model
# ---------------------------------------------------------------------------

fill_rom = assemble_file(os.path.join(_LAB4_REF, "Fill.asm"))
computer = Computer(fill_rom)
STEPS_PER_FULL_PASS = 8192 * 21 * 3 + 1000

computer.memory.keyboard = 1
computer.run(max_steps=STEPS_PER_FULL_PASS)
screen_black = all(computer.memory.screen.get(i, 0) & MASK == MASK for i in range(8192))
check("Computer running Fill.hack: screen fully black after key-press",
      screen_black, "not all 8192 screen words == -1")

computer.memory.keyboard = 0
computer.run(max_steps=STEPS_PER_FULL_PASS)
screen_white = all(computer.memory.screen.get(i, 0) & MASK == 0 for i in range(8192))
check("Computer running Fill.hack: screen fully white after key-release",
      screen_white, "not all 8192 screen words == 0")

# ---------------------------------------------------------------------------
# Cross-check: the bit-level Computer model and Lab 4's mnemonic-level
# interpreter must agree on Mult -- two independently-built models,
# same answer, is the actual evidence of correctness here.
# ---------------------------------------------------------------------------

from hack_interpreter import load as load_mnemonic  # noqa: E402

agree = True
for a, b in [(6, 7), (0, 9), (15, 3)]:
    bitlevel = Computer(mult_rom)
    bitlevel.memory.ram[0] = a
    bitlevel.memory.ram[1] = b
    bitlevel.run(max_steps=20000)

    mnemonic = load_mnemonic(os.path.join(_LAB4_REF, "Mult.asm"))
    mnemonic.RAM[0] = a
    mnemonic.RAM[1] = b
    mnemonic.run(max_steps=20000)

    if bitlevel.memory.ram.get(2, 0) != mnemonic.RAM.get(2, 0):
        agree = False
check("Bit-level CPU model agrees with Lab 4's mnemonic-level interpreter",
      agree)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

print(f"{len(PASS)}/{len(PASS) + len(FAIL)} checks PASS")
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print(f"  - {f}")
    raise SystemExit(1)
