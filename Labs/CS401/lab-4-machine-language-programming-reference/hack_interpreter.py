"""
hack_interpreter.py -- Instructor-only Hack assembly interpreter for CS401
Lab 4 (Machine Language Programming).

NOT the real Nand2Tetris Assembler/CPU Emulator (Java, cannot run in this
environment). This is a from-scratch, mnemonic-level interpreter: it
resolves labels/variables and executes A-/C-instructions directly from
their text form (it does not go through 16-bit binary encoding at
execution time), used as an independent correctness oracle for Mult.asm
and Fill.asm. The hand-assembly worked example's binary encoding
(hand_assembly_answer_key.md) is derived separately, by the standard Hack
comp/dest/jump bit tables, and cross-checked against this interpreter's
own `assemble()` function below.

Never synced to docs/ by /deploy -- instructor-only.
"""

MASK = 0xFFFF

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for _i in range(16):
    PREDEFINED[f"R{_i}"] = _i

# comp mnemonic -> (a bit, 6-bit c-code, function(d, x) -> unsigned16 value)
COMP_TABLE = {
    "0":   (0, "101010", lambda d, x: 0),
    "1":   (0, "111111", lambda d, x: 1),
    "-1":  (0, "111010", lambda d, x: MASK),
    "D":   (0, "001100", lambda d, x: d),
    "A":   (0, "110000", lambda d, x: x),
    "!D":  (0, "001101", lambda d, x: (~d) & MASK),
    "!A":  (0, "110001", lambda d, x: (~x) & MASK),
    "-D":  (0, "001111", lambda d, x: (-d) & MASK),
    "-A":  (0, "110011", lambda d, x: (-x) & MASK),
    "D+1": (0, "011111", lambda d, x: (d + 1) & MASK),
    "A+1": (0, "110111", lambda d, x: (x + 1) & MASK),
    "D-1": (0, "001110", lambda d, x: (d - 1) & MASK),
    "A-1": (0, "110010", lambda d, x: (x - 1) & MASK),
    "D+A": (0, "000010", lambda d, x: (d + x) & MASK),
    "D-A": (0, "010011", lambda d, x: (d - x) & MASK),
    "A-D": (0, "000111", lambda d, x: (x - d) & MASK),
    "D&A": (0, "000000", lambda d, x: d & x),
    "D|A": (0, "010101", lambda d, x: d | x),
}
# M-variants: identical c-codes, a=1, x becomes RAM[A] at call site.
for _base in ["A", "!A", "-A", "A+1", "A-1", "D+A", "D-A", "A-D", "D&A", "D|A"]:
    _m = _base.replace("A", "M")
    _a, _code, _fn = COMP_TABLE[_base]
    COMP_TABLE[_m] = (1, _code, _fn)

DEST_TABLE = {
    None: "000", "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}

JUMP_TABLE = {
    None: "000", "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def to_signed(v):
    v &= MASK
    return v - 0x10000 if v >= 0x8000 else v


def strip_comment(line):
    idx = line.find("//")
    return (line if idx == -1 else line[:idx]).strip()


def parse(source_lines):
    """First pass: strip comments/blank lines, resolve labels."""
    raw = [strip_comment(l) for l in source_lines]
    raw = [l for l in raw if l]
    instructions = []
    labels = {}
    for line in raw:
        if line.startswith("(") and line.endswith(")"):
            labels[line[1:-1]] = len(instructions)
        else:
            instructions.append(line)
    return instructions, labels


def resolve_symbols(instructions, labels):
    """Second pass: assign RAM addresses to variables (16 upward)."""
    symbols = dict(PREDEFINED)
    symbols.update(labels)
    next_var = 16
    for instr in instructions:
        if instr.startswith("@"):
            operand = instr[1:]
            if not operand.lstrip("-").isdigit() and operand not in symbols:
                symbols[operand] = next_var
                next_var += 1
    return symbols


def assemble(instr, symbols):
    """Assemble one instruction to its 16-bit binary string (for the
    hand-assembly cross-check)."""
    if instr.startswith("@"):
        operand = instr[1:]
        value = int(operand) if operand.lstrip("-").isdigit() else symbols[operand]
        return format(value & MASK, "016b")
    dest, rest = (instr.split("=", 1) if "=" in instr else (None, instr))
    comp, jump = (rest.split(";", 1) if ";" in rest else (rest, None))
    a, code, _ = COMP_TABLE[comp]
    return "111" + str(a) + code + DEST_TABLE[dest] + JUMP_TABLE[jump]


class HackMachine:
    def __init__(self, instructions, symbols):
        self.instructions = instructions
        self.symbols = symbols
        self.A = 0
        self.D = 0
        self.PC = 0
        self.RAM = {}

    def ram_get(self, addr):
        return self.RAM.get(addr, 0)

    def step(self):
        instr = self.instructions[self.PC]
        if instr.startswith("@"):
            operand = instr[1:]
            value = int(operand) if operand.lstrip("-").isdigit() else self.symbols[operand]
            self.A = value & MASK
            self.PC += 1
            return
        dest, rest = (instr.split("=", 1) if "=" in instr else (None, instr))
        comp, jump = (rest.split(";", 1) if ";" in rest else (rest, None))
        _, _, fn = COMP_TABLE[comp]
        x = self.ram_get(self.A) if "M" in comp else self.A
        value = fn(self.D, x) & MASK
        if dest:
            if "A" in dest:
                self.A = value
            if "D" in dest:
                self.D = value
            if "M" in dest:
                self.RAM[self.A] = value
        if jump:
            signed = to_signed(value)
            taken = {
                "JGT": signed > 0, "JEQ": signed == 0, "JGE": signed >= 0,
                "JLT": signed < 0, "JNE": signed != 0, "JLE": signed <= 0,
                "JMP": True,
            }[jump]
            self.PC = self.A if taken else self.PC + 1
        else:
            self.PC += 1

    def run(self, max_steps):
        for _ in range(max_steps):
            self.step()


def load(path):
    with open(path) as f:
        instructions, labels = parse(f.readlines())
    symbols = resolve_symbols(instructions, labels)
    return HackMachine(instructions, symbols)
