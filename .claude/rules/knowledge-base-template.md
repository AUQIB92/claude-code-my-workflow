---
paths:
  - "Slides/**/*.tex"
  - "Quarto/**/*.qmd"
  - "scripts/**/*.R"
---

# Course Knowledge Base: Computer Organization and Architecture (PCC CS-401)

<!-- Starter KB bootstrapped by /create-lecture on 2026-08-04 while drafting
     Week 5 (05-addressing-cpu-bus). No lecture .tex files existed yet in
     Slides/ other than the HelloWorld sample, so this registry projects
     backward from syllabus.md (Weeks 1-4 topics) to give Week 5 consistent
     notation to build on, then forward for the rest of the course arc.
     Amend freely as Weeks 1-4 get authored for real — treat rows marked
     "(projected)" as provisional until a Week 1-4 .tex confirms them. -->

## Notation Registry

| Rule | Convention | Example | Anti-Pattern |
|------|-----------|---------|-------------|
| Registers | Uppercase abbreviation, `\texttt{}` in prose, no spelled-out re-expansion after first use | `\texttt{PC}`, `\texttt{MAR}` | Lowercase `pc`; re-spelling "Program Counter" every slide |
| Register transfer | `\gets` for transfer, `[X]` for "contents of register/location X" | `\texttt{R1} \gets \texttt{[R2]}` | Using `=` for transfer (reserve `=` for equality/definition) |
| Memory reference | `M[address]` | `M[\text{EA}]`, `M[1000]` | `MEM(EA)`, `Mem[EA]` (inconsistent casing) |
| Effective address | `EA`, always the *computed* address after applying the addressing mode | `EA = [\text{PC}] + \text{disp}` | Conflating EA (an address) with the operand value stored there |
| Bus naming | Single-bus organization: "the common bus" (unlabeled, one bus). Multi-bus: `Bus A`, `Bus B` (ALU inputs), `Bus C` (ALU output) | "Bus A carries `[R2]`" | Calling buses "wire 1 / wire 2"; renaming buses mid-deck |
| Binary / hex literals | Subscript base notation in prose/math; `0x` prefix only inside verbatim/code blocks | $1010_2$, $1A_{16}$ | `0x1A` in running prose text |
| Bit widths | "$n$-bit", always with the value of $n$ stated at first use | "16-bit address bus" | Unhyphenated/inconsistent "16 bit" vs "16-bit" |

## Symbol Reference

| Symbol | Meaning | Introduced |
|--------|---------|------------|
| PC | Program Counter — address of the next instruction to fetch | Week 4 (projected: registers/instruction cycle) |
| IR | Instruction Register — holds the instruction currently executing | Week 4 (projected) |
| MAR | Memory Address Register — holds the address for the current memory access | Week 4 (projected) |
| MDR | Memory Data/Buffer Register — holds data in transit to/from memory (aka MBR) | Week 4 (projected) |
| AC | Accumulator — implicit operand/result register in single-address ISAs | Week 4 (projected) |
| R0..Rn-1 | General-purpose register file | Week 4 (projected) |
| SP | Stack Pointer | Week 4 (projected: stack organization) |
| EA | Effective Address — actual operand address after applying an addressing mode | **Week 5 (new)** |
| Y, Z | Internal hidden registers in the single-bus CPU datapath that buffer ALU operands/results | **Week 5 (new)** |
| Bus A / Bus B / Bus C | Three parallel buses in the multiple-bus datapath: A, B feed ALU inputs, C carries the ALU output | **Week 5 (new)** |
| $T_1, T_2, \dots$ | Control step — one clock cycle's worth of RTL transfers | Week 5 (introduced in the RTL-notation slide; reused and made "automatic" via `SC` in Week 6) |
| SC | Sequence Counter — a counter register that holds the current control-step number; a step decoder converts it into one-hot $T_1, T_2, \dots$ lines. $SC_{clear}$ resets it to $T_1$ at an instruction's last step. | **Week 6 (new)** |
| $X_{in}$ / $X_{out}$ | Register-gating control signal: $X_{in}=1$ loads register X from the bus this cycle; $X_{out}=1$ drives X's contents onto the bus this cycle | **Week 6 (new)** |
| $D_i$ | One-hot opcode-decoder output — $D_i = 1$ exactly when the IR holds instruction $i$'s opcode | **Week 6 (new)** |
| Control matrix | The combinational logic block that ANDs opcode-decode ($D_i$) with step-decode ($T_j$) lines, and ORs across instructions, to produce each control signal | **Week 6 (new)** |

## Lecture Progression

| # | Title | Core Question | Key Notation | Key Method |
|---|-------|--------------|-------------|------------|
| 1 | Intro & Performance | How do we measure and compare computer performance? | Basic Performance Equation, Amdahl's Law | Clock-rate/CPI arithmetic |
| 2 | Number Systems & Arithmetic | How does hardware represent and add/subtract numbers? | Two's complement, ALU | Ripple-carry / adder design |
| 3 | IEEE754 Floating Point | How does hardware represent real numbers? | sign/exponent/mantissa | Normalization, rounding |
| 4 | Registers, Instructions, Instruction Cycle | What does an instruction look like, and how does the CPU step through one? | PC, IR, MAR, MDR, opcode/operand fields | Fetch-decode-execute cycle |
| 5 | Addressing Modes, CPU Organization, Bus Structures | Where do operands live, and what hardware moves them? | EA, Y/Z, Bus A/B/C | RTL micro-operation traces |
| 6 | Hardwired Control | How does hardware generate the control-step sequence automatically? | SC (sequence counter), $X_{in}/X_{out}$, $D_i$, control matrix (T1, T2, ... reused from Week 5, not new) | State-table / sequencer design |
| 7 | Microprogrammed Control | How does a control unit driven by stored microinstructions work? | Control word, microaddress | Horizontal/vertical microcode |

## Empirical Applications

| Application | Paper | Dataset | Lecture(s) | Purpose |
|------------|-------|---------|------------|---------|
| RTL trace of `R1 \gets R2 + R3` | Hamacher Ch. 7; Mano Ch. 7 | n/a (worked hardware trace) | Week 5, Week 6 | Running thread comparing single-bus (3 control steps via Y/Z) vs. three-bus (1 control step) organization — makes the cost/speed trade-off concrete and quantitative. Week 6 extends the same trace into a state table and Boolean control equations ($Y_{in}=D_{\text{ADD}}\cdot T_1$, etc.) for the hardwired control unit that drives it. |
| Compiling `A[i] = A[i] + 1` | Hamacher Ch. 7 | n/a (compiler-codegen example) | Week 5 | Motivates addressing modes from a real toolchain need: immediate (constant), based/indexed (array element), indirect (pointer) |

## Design Principles

| Principle | Evidence | Lectures Applied |
|-----------|----------|-----------------|
| Motivate every addressing mode with the C/assembly idiom it implements, not the mode name first | Prevents "list of modes to memorize" fatigue; ties notation to code students already reason about | Week 5 |
| Thread one worked instruction trace across competing hardware designs to make trade-offs quantitative (cycle counts), not just qualitative (adjectives like "faster") | Cost/speed trade-offs are the recurring theme of CPU-organization content (Weeks 5-7) | Week 5, continued in Week 6 (state table + Boolean equations for hardwired control), and by design should continue into Week 7 (same trace, microprogrammed control) |

## Anti-Patterns (Don't Do This)

| Anti-Pattern | What Happened | Correction |
|-------------|---------------|-----------|
| | | |

## R Code Pitfalls

| Bug | Impact | Fix |
|-----|--------|-----|
| | | |

<!-- This course has no R/statistical component in Weeks 1-12 per syllabus.md;
     the R Code Pitfalls table is left empty by design, not an oversight.
     For research projects, add: Estimand Registry, DGP Configs, Tolerance Thresholds -->
