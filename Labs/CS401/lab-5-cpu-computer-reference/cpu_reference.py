"""
cpu_reference.py -- Instructor-only bit-level behavioural reference for
CS401 Lab 5 (Computer Architecture -- CPU & Computer, Nand2Tetris Project 5).

NOT literal HDL and NOT the same verification path as Lab 4's
hack_interpreter.py. Lab 4's interpreter executes assembly at the MNEMONIC
level ("D=D+A"); this model executes at the BIT level -- it decodes the
actual 16-bit instruction word (as CPU.hdl itself must) into
zx/nx/zy/ny/f/no ALU control bits, dest bits and jump bits, exactly as
specified in the lab manual's Task 1. This is deliberately a second,
independent verification path: Lab 4's Mult.hack/Fill.hack (assembled from
the same Mult.asm/Fill.asm) are re-run through THIS bit-level CPU model in
test_cpu.py, and must reproduce the identical RAM[2]/screen results Lab 4
already proved via mnemonic-level execution -- if the two independently-
built models agree, that is real cross-checked evidence the bit-level
decode logic (which is what students' CPU.hdl actually implements) is
correct, not just that "some interpreter" runs Hack assembly.

Never synced to docs/ by /deploy -- instructor-only.
"""

MASK = 0xFFFF


def alu(x, y, zx, nx, zy, ny, f, no):
    """The Lab 2 ALU, reimplemented here on plain ints (not bit tuples)
    since the CPU model works in 16-bit int words throughout."""
    if zx:
        x = 0
    if nx:
        x = (~x) & MASK
    if zy:
        y = 0
    if ny:
        y = (~y) & MASK
    out = (x + y) & MASK if f else (x & y)
    if no:
        out = (~out) & MASK
    zr = 1 if out == 0 else 0
    ng = 1 if (out >> 15) & 1 else 0
    return out, zr, ng


def bit(value, i):
    return (value >> i) & 1


class CPU:
    """Behavioural model of Lab 5's CPU.hdl (Task 1)."""

    def __init__(self):
        self.A = 0
        self.D = 0
        self.PC = 0

    def combinational(self, instruction, inM, reset):
        """Compute this cycle's outputs and next-state values, without
        committing them (mirrors combinational settling before a clock
        edge -- see tock())."""
        is_c_instruction = bit(instruction, 15)

        if not is_c_instruction:
            # A-instruction: load A directly, ALU/D untouched, no jump.
            next_A = instruction & MASK
            next_D = self.D
            outM = 0
            writeM = 0
            addressM = self.A & 0x7FFF  # this cycle's address is the OLD A
            next_PC = 0 if reset else (self.PC + 1) & MASK
            return {
                "addressM": addressM, "outM": outM, "writeM": writeM,
                "next_A": next_A, "next_D": next_D, "next_PC": next_PC,
            }

        # C-instruction: bits 12=a, 11..6=comp (zx,nx,zy,ny,f,no), 5..3=dest
        # (A,D,M), 2..0=jump (j1=LT, j2=EQ, j3=GT).
        a = bit(instruction, 12)
        zx, nx, zy, ny, f, no = (bit(instruction, i) for i in (11, 10, 9, 8, 7, 6))
        d_A, d_D, d_M = bit(instruction, 5), bit(instruction, 4), bit(instruction, 3)
        j1, j2, j3 = bit(instruction, 2), bit(instruction, 1), bit(instruction, 0)

        y_input = inM if a else self.A
        out, zr, ng = alu(self.D, y_input, zx, nx, zy, ny, f, no)

        next_A = out if d_A else self.A
        next_D = out if d_D else self.D
        writeM = d_M
        outM = out
        addressM = self.A & 0x7FFF  # combinational: OLD A, before this cycle's dest=A update

        jump = (j1 and ng) or (j2 and zr) or (j3 and (not zr) and (not ng))
        if reset:
            next_PC = 0
        elif jump:
            next_PC = next_A & MASK  # the (possibly just-updated) A value
        else:
            next_PC = (self.PC + 1) & MASK

        return {
            "addressM": addressM, "outM": outM, "writeM": writeM,
            "next_A": next_A, "next_D": next_D, "next_PC": next_PC,
        }

    def tock(self, updates):
        self.A = updates["next_A"] & MASK
        self.D = updates["next_D"] & MASK
        self.PC = updates["next_PC"] & MASK


class Memory:
    """Behavioural model of Lab 5's Memory.hdl (Task 2): routes
    0-16383 to RAM16K, 16384-24575 to Screen, 24576 to Keyboard."""

    def __init__(self):
        self.ram = {}
        self.screen = {}
        self.keyboard = 0

    def read(self, address):
        if address < 16384:
            return self.ram.get(address, 0)
        if address < 24576:
            return self.screen.get(address - 16384, 0)
        return self.keyboard

    def write(self, address, value):
        value &= MASK
        if address < 16384:
            self.ram[address] = value
        elif address < 24576:
            self.screen[address - 16384] = value
        # writes to the Keyboard address are ignored, as on real hardware


class Computer:
    """Behavioural model of Lab 5's Computer.hdl (Task 3): ROM32K + CPU +
    Memory, wired per the lab manual's Task 3 description."""

    def __init__(self, rom):
        self.rom = rom  # list of 16-bit ints (the loaded program)
        self.cpu = CPU()
        self.memory = Memory()

    def step(self, reset=0):
        instruction = self.rom[self.cpu.PC] if self.cpu.PC < len(self.rom) else 0
        # addressM this cycle is the CPU's OLD A (pre-update) -- read it
        # via a throwaway combinational call is wasteful; instead read A
        # directly, matching the real chip's same-cycle wiring.
        addressM = self.cpu.A & 0x7FFF
        inM = self.memory.read(addressM)
        updates = self.cpu.combinational(instruction, inM, reset)
        if updates["writeM"]:
            self.memory.write(updates["addressM"], updates["outM"])
        self.cpu.tock(updates)

    def run(self, max_steps, reset=0):
        for _ in range(max_steps):
            self.step(reset=reset)
