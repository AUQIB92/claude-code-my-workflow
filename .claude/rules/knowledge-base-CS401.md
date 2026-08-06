---
paths:
  - "Slides/CS401/**/*.tex"
  - "Quarto/CS401/**/*.qmd"
---

# Course Knowledge Base: Computer Organization and Architecture (PCC CS-401)

<!-- Starter KB bootstrapped by /create-lecture on 2026-08-04 while drafting
     Week 5 (05-addressing-cpu-bus). No lecture .tex files existed yet in
     Slides/ other than the HelloWorld sample, so this registry projects
     backward from syllabi/CS401.md (Weeks 1-4 topics) to give Week 5 consistent
     notation to build on, then forward for the rest of the course arc.
     Amend freely as Weeks 1-4 get authored for real — treat rows marked
     "(projected)" as provisional until a Week 1-4 .tex confirms them. -->

## Anchor Textbooks

| Book (ShortName) | Index | Weeks/Lectures Backed | Page-Verified? |
|-------------------|-------|------------------------|-----------------|
| Hamacher, *Computer Organization*, 5th ed. (Hamacher2002) | `master_supporting_docs/CS401/supporting_books/Hamacher2002/index.md` — **not built yet, no longer blocked.** PDF supplied 2026-08-06 has no text layer (scanned); `pdftoppm` (Poppler) and `tesseract` are now both installed on this machine (2026-08-06), so `/index-textbook CS401/Hamacher2002` can run the OCR fallback path. Not yet run. | Weeks 1-5, 8-11 per syllabus; Lectures 05-07 built so far | **No — standard treatment, not page-verified** |
| Mano, *Computer System Architecture*, 3rd ed. (Mano1993) | `master_supporting_docs/CS401/supporting_books/Mano1993/index.md` — **built 2026-08-06, Ch. 5 (Sec. 5-4/5-9/5-10 only) + Ch. 7-8** (the chapters Lectures 05-07 need; rest of Ch. 5, Ch. 1-4, 6, 9-13 not indexed) | Week 5 (Ch. 8 — corrected, was mis-cited as Ch. 7); Week 6 (Ch. 5 — corrected 2026-08-06, was mis-cited as Ch. 7); Week 7 (Ch. 7, confirmed correct) | **Ch. 5 (Sec. 5-4/5-9/5-10), Ch. 7-8: Yes, page-cited. Rest of book: no.** |
| Stallings, *Computer Organization and Architecture* (Stallings2015) | `master_supporting_docs/CS401/supporting_books/Stallings2015/index.md` — **not built.** PDF supplied 2026-08-06 is confirmed the **11th edition** ("Designing for Performance"), not the 10th/2015 edition this repo's bib key implies. Confirmed via its own TOC: "Control Unit Operation and Microprogrammed Control" is **Chapter 19** in this 11th-edition file, not Chapter 16 as Lectures 06-07 currently cite — plausibly a cross-edition renumbering, not necessarily a content error, but unconfirmed without the actual 2015 edition in hand. | Weeks 7-8, 11-12 (Lecture 06-07) | **No — edition mismatch flagged, not indexed. Do not page-cite from the 11th-edition file against the "Ch. 16" citations without resolving the edition question first.** |

<!-- [LEARN:textbook-grounding] Lectures 05, 06, 07 cite these three books by
     chapter (per syllabi/CS401.md's anchor-reading column), but the actual
     slide content (definitions, control-word tables, RTL traces) was authored
     from general knowledge of what these standard textbooks cover, not from
     reading an actual page of any of them. No book.pdf exists yet under
     master_supporting_docs/CS401/supporting_books/. Per textbook-grounding.md,
     this is honest chapter-level attribution, not a fabricated page citation
     -- but it is NOT page-verified, and should not be treated as such until
     /index-textbook runs against real files and /verify-claims can check
     these lectures' claims against the indexed pages. Drop the PDFs into
     master_supporting_docs/CS401/supporting_books/<ShortName>/book.pdf and
     run /index-textbook CS401/<ShortName> to close this gap. -->

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
| Control word (microinstruction) | One stored row of control information: the signals to assert this cycle plus next-address information; a microprogram is the ordered sequence of control words implementing one instruction | **Week 7 (new)** |
| Microaddress | The address of a control word inside control memory | **Week 7 (new)** |
| CM (Control Memory) | Small ROM/RAM holding control words, indexed by microaddress; the microprogrammed analogue of Week 6's control matrix | **Week 7 (new)** |
| MPC (Microprogram Counter) | Register holding the microaddress of the control word being read this cycle; the microprogrammed analogue of Week 6's `SC` | **Week 7 (new)** |
| Mapping (address sequencing) | The unit that converts an opcode in `IR` into the starting microaddress of that instruction's microprogram, loaded into `MPC` on fetch; the microprogrammed analogue of Week 6's opcode decoder | **Week 7 (new)** |
| Horizontal / vertical microinstruction | Horizontal: one bit per control signal, no decode delay, wide control word. Vertical: mutually-exclusive signals grouped into encoded fields expanded by a decoder, narrower control word, adds decode delay | **Week 7 (new)** |

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
| RTL trace of `R1 \gets R2 + R3` | Hamacher Ch. 7; Mano Ch. 8 (Week 5, corrected 2026-08-06 — datapath/bus/addressing content); Mano Ch. 5 (Week 6, corrected 2026-08-06 — hardwired control-logic-gate content, was mis-cited as Ch. 7); Mano Ch. 7 (Week 7, confirmed — control-memory/microinstruction content) | n/a (worked hardware trace) | Week 5, Week 6, Week 7 | Running thread comparing single-bus (3 control steps via Y/Z) vs. three-bus (1 control step) organization — makes the cost/speed trade-off concrete and quantitative. Week 6 extends the same trace into a state table and Boolean control equations ($Y_{in}=D_{\text{ADD}}\cdot T_1$, etc.) for the hardwired control unit that drives it. Week 7 rebuilds the identical 3-step control unit as a microprogram (CM rows + MPC), giving a direct hardwired-vs.-microprogrammed comparison on the same worked example. |
| Compiling `A[i] = A[i] + 1` | Hamacher Ch. 7 | n/a (compiler-codegen example) | Week 5 | Motivates addressing modes from a real toolchain need: immediate (constant), based/indexed (array element), indirect (pointer) |

## Design Principles

| Principle | Evidence | Lectures Applied |
|-----------|----------|-----------------|
| Motivate every addressing mode with the C/assembly idiom it implements, not the mode name first | Prevents "list of modes to memorize" fatigue; ties notation to code students already reason about | Week 5 |
| Thread one worked instruction trace across competing hardware designs to make trade-offs quantitative (cycle counts), not just qualitative (adjectives like "faster") | Cost/speed trade-offs are the recurring theme of CPU-organization content (Weeks 5-7) | Week 5 (bus organization), Week 6 (state table + Boolean equations for hardwired control), Week 7 (same trace rebuilt as a microprogram — CM rows + MPC — closing the three-week arc with a direct hardwired-vs.-microprogrammed head-to-head) |

## Anti-Patterns (Don't Do This)

| Anti-Pattern | What Happened | Correction |
|-------------|---------------|-----------|
| | | |

## R Code Pitfalls

| Bug | Impact | Fix |
|-----|--------|-----|
| | | |

<!-- This course has no R/statistical component in Weeks 1-12 per syllabi/CS401.md;
     the R Code Pitfalls table is left empty by design, not an oversight.
     For research projects, add: Estimand Registry, DGP Configs, Tolerance Thresholds -->
