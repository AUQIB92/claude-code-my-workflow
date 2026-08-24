"""
test_asm.py -- runs Mult.asm and Fill.asm through hack_interpreter.py and
checks their behaviour (CS401 Lab 4 instructor reference).

Run: python test_asm.py
Expects: "N/N checks PASS"
"""

from hack_interpreter import load, assemble, parse, resolve_symbols, MASK

PASS = []
FAIL = []


def check(name, condition, detail=""):
    if condition:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: {detail}")


# ---------------------------------------------------------------------------
# Mult.asm — check RAM[2] == RAM[0] * RAM[1] for a representative value set
# (matching Mult.tst's own precondition: RAM[0], RAM[1] >= 0).
# ---------------------------------------------------------------------------

for a, b in [(0, 0), (0, 5), (5, 0), (1, 1), (3, 4), (7, 6), (12, 12), (255, 2)]:
    m = load("Mult.asm")
    m.RAM[0] = a
    m.RAM[1] = b
    m.run(max_steps=20000)
    expected = (a * b) & MASK
    check(f"Mult.asm: {a} x {b} = {expected}", m.RAM.get(2, 0) == expected,
          f"got RAM[2]={m.RAM.get(2, 0)}")

# ---------------------------------------------------------------------------
# Fill.asm — press a key (KBD != 0), run enough cycles to fill the whole
# screen, confirm every one of the 8192 screen words is fully set (-1);
# release the key (KBD == 0), run enough cycles to whiten, confirm 0.
# ---------------------------------------------------------------------------

m = load("Fill.asm")
m.RAM[24576] = 1  # simulate a key held down
# FILLLOOP's body is 21 instructions/word (counted directly from Fill.asm).
# Budget for THREE full passes, not one: a run started mid-loop (as the
# second call below is, continuing from wherever the first run's step
# budget cut off) may need to finish an in-progress pass under the OLD
# color before it even re-polls KBD and starts the new-color pass.
STEPS_PER_FULL_PASS = 8192 * 21 * 3 + 1000
m.run(max_steps=STEPS_PER_FULL_PASS)
screen_black = all(m.RAM.get(16384 + i, 0) & MASK == MASK for i in range(8192))
check("Fill.asm: screen fully black after key-press fill pass", screen_black,
      "not all 8192 screen words == -1")

m.RAM[24576] = 0  # release the key
m.run(max_steps=STEPS_PER_FULL_PASS)
screen_white = all(m.RAM.get(16384 + i, 0) & MASK == 0 for i in range(8192))
check("Fill.asm: screen fully white after key-release fill pass", screen_white,
      "not all 8192 screen words == 0")

# ---------------------------------------------------------------------------
# Hand-assembly cross-check: the 4-line sample program from the lab manual
# (Table lab4-handasm), assembled here and compared against the manually
# worked binary in hand_assembly_answer_key.md.
# ---------------------------------------------------------------------------

sample = ["@2", "D=A", "@3", "D=D+A"]
instructions, labels = parse(sample)
symbols = resolve_symbols(instructions, labels)
binaries = [assemble(instr, symbols) for instr in instructions]
expected_binaries = [
    "0000000000000010",  # @2
    "1110110000010000",  # D=A
    "0000000000000011",  # @3
    "1110000010010000",  # D=D+A
]
check("Hand-assembly sample matches hand_assembly_answer_key.md",
      binaries == expected_binaries, f"got {binaries}")

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

print(f"{len(PASS)}/{len(PASS) + len(FAIL)} checks PASS")
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print(f"  - {f}")
    raise SystemExit(1)
