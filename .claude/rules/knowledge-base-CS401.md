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
      Week 4 (04-registers-instructions) authored 2026-08-07, confirming the
      register/instruction symbols marked "(projected)" below. Weeks 1-3
      (01-intro-performance, 02-number-systems-arithmetic,
      03-ieee754-floating-point) authored 2026-08-07, confirming the
      performance/arithmetic/float symbols below. -->

## Course Profile

| Field | Value |
|---|---|
| Audience level | `undergrad` (B.Tech CSE, semester 4) |
| Programme position | semester 4 of 8 |
| Default difficulty | **`core`** — derived from `undergrad` + semester 4 per `.claude/rules/difficulty-levels.md` |
| Exam target | GATE CS (via `/competitive-exam-questions`) |
| Implementation language | register-transfer notation and assembly; C only where it motivates an addressing mode |

## Anchor Textbooks

| Book (ShortName) | Index | Weeks/Lectures Backed | Page-Verified? |
|-------------------|-------|------------------------|-----------------|
| Hamacher, *Computer Organization and Embedded Systems* — **6th ed. on disk** (Hamacher2002; the file present as of 2026-08-11 is the 6th ed., ISBN 978-0-07-338065-0 — the 2026-08-10 pass indexed a 5th-edition file that is no longer present; edition mismatch documented in the index) | `master_supporting_docs/CS401/supporting_books/Hamacher2002/index.md` — **Ch. 3 (Basic I/O: polling, interrupts) + Ch. 7 §7.1-7.4 (bus/interface hardware) built 2026-08-11** for Week 8 (`CS401/08-io-techniques`), page-verified directly against the 6th-edition file via visual `Read` (Tesseract unavailable on this machine, so the OCR path was skipped for direct visual reading — see index for detail). **This 6th edition never names "DMA" or "IOP" as topics** — §7.3 Arbitration is the functional analogue of DMA (bus mastering by an I/O device) but the book doesn't use that term; DMA/IOP content stays general-treatment. The 2026-08-10 Ch.2/Ch.6 rows describe the old, now-absent 5th-edition file and need re-verification against this 6th-edition file before being trusted. | Week 8 (Ch. 3, Ch. 7 §7.1-7.4, page-verified against the current 6th-ed. file); Weeks 1-2, 4-7, 9-11 per syllabus but **citations built against a different, no-longer-present edition — need re-verification, not just re-indexing** | **Week 8 only: Yes, page-cited against the current file. Rest of book: no — Weeks 1-2/4-7/9-11 citations flagged edition-uncertain (see index Edition notice, 2026-08-11)** |
| Mano, *Computer System Architecture*, 3rd ed. (Mano1993) | `master_supporting_docs/CS401/supporting_books/Mano1993/index.md` — **built 2026-08-06, Ch. 5 (Sec. 5-2/5-4/5-9/5-10 only) + Ch. 7-8** (the chapters Lectures 04-07 need; rest of Ch. 5, Ch. 1-4, 6, 9-13 not indexed) | Week 4 (Ch. 5 Sec. 5-2 common bus + Ch. 8 CPU/registers/stack/formats); Week 5 (Ch. 8 — corrected, was mis-cited as Ch. 7); Week 6 (Ch. 5 — corrected 2026-08-06, was mis-cited as Ch. 7); Week 7 (Ch. 7, confirmed correct) | **Ch. 5 (Sec. 5-2/5-4/5-9/5-10), Ch. 7-8: Yes, page-cited. Rest of book: no.** |
| Patterson & Hennessy, *Computer Organization and Design: The Hardware/Software Interface, ARM Edition*, 5th ed. (PattersonHennessy2017) | `master_supporting_docs/CS401/supporting_books/PattersonHennessy2017/index.md` — **built 2026-08-07, Ch. 1-6 + App. A/C/D in full.** 1074-page text-layer PDF (ARMv8/LEGv8 edition, ISBN 978-0-12-801733-3). **Pagination note: PDF↔printed offset is non-constant** (inserted online "e." pages); resolve printed pages via the running head at the top of each PDF page, never a fixed offset. | Weeks 1-3 (Ch. 1 §1.6, Ch. 3 arithmetic/IEEE 754); Weeks 4-5 (Ch. 2 LEGv8 instructions/operands/formats/addressing); Weeks 6-7 (Ch. 4 §4.3-4.4 datapath + single-cycle control, App. C hardwired→microprogrammed); Weeks 9-10 (Ch. 5 caches/virtual memory/RAID); Weeks 11-12 (Ch. 6 Flynn/multicore/GPU, App. D RISC survey). **Week 8 (I/O) not covered — stay with Hamacher/Stallings.** | **Ch. 1-6, App. A/C/D: Yes, page-cited** |
| Stallings, *Computer Organization and Architecture* (Stallings2015) | `master_supporting_docs/CS401/supporting_books/Stallings2015/index.md` — **not built (no chapter/page index yet), but the PDF has a text layer and was read directly for Week 8 (2026-08-11).** PDF supplied 2026-08-06 is confirmed the **11th edition** ("Designing for Performance"), not the 10th/2015 edition this repo's bib key implies. Confirmed via its own TOC: "Control Unit Operation and Microprogrammed Control" is **Chapter 19** (not Ch. 16 as Lectures 06-07 cite); **I/O is Chapter 8** ("Input/Output," §8.1-8.9 — External Devices, I/O Modules, Programmed I/O, Interrupt-Driven I/O, DMA, Direct Cache Access, I/O Channels/Processors), **not Ch. 7** as the syllabus and Lecture 08's header comment assumed before this correction — cross-edition renumbering, not a content error, and now confirmed (not just flagged) for Ch. 8/19. Other chapters' renumbering vs. the 2015 10th ed. remains unconfirmed. | Weeks 7-8, 11-12 (Lectures 06-08) | **Ch. 8 (I/O) and Ch. 19 (control unit): chapter number confirmed, general/standard-treatment citations only (no page index yet — do not page-cite). Rest of book: edition mismatch still unresolved, do not cite chapter numbers without checking the TOC first.** |

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
| PC | Program Counter — address of the next instruction to fetch | **Week 4 (confirmed: fetch phase)** |
| IC | Instruction Count — number of instructions a program executes | **Week 1 (new)** |
| CPI | Cycles Per Instruction — average clock cycles per instruction | **Week 1 (new)** |
| $f$ | Clock rate (Hz); $T_c = 1/f$ is the clock cycle time | **Week 1 (new)** |
| CPU time | $\text{IC} \times \text{CPI} \times T_c = \text{IC}\times\text{CPI}/f$ — the basic performance equation | **Week 1 (new)** |
| MIPS | $\text{IC}/(\text{time}\times10^6) = f/(\text{CPI}\times10^6)$ — million instructions/sec; misleading when ISAs differ | **Week 1 (new)** |
| Amdahl's Law | $\text{Speedup} = 1/[(1-f)+f/S_f]$ — $f$ = improved fraction, $S_f$ = its speedup; ceiling $1/(1-f)$ | **Week 1 (new)** |
| Two's complement | $-x \equiv 2^n - x$ (mod $2^n$) — ``flip all bits, add 1''; range $-2^{n-1}$ to $2^{n-1}-1$; sign bit = MSB | **Week 2 (new)** |
| Overflow | Result outside the format range; two's complement test = wrong sign after adding same-signed operands (carry-out $\neq$ overflow) | **Week 2 (new)** |
| Fixed point | Number with an agreed binary-point position (e.g. Q8.8); integer ALU adds unchanged | **Week 2 (new)** |
| HA / FA | Half adder ($S=A\oplus B$, $C=A\cdot B$); full adder ($S=A\oplus B\oplus C_{in}$, $C_{out}=A\cdot B + C_{in}(A\oplus B)$); ripple-carry chains FAs | **Week 2 (new)** |
| $A$, $Q$, $Q_{-1}$, $M$ (Booth's algorithm) | $A$: accumulator (init 0); $Q$: multiplier; $Q_{-1}$: extra bit (init 0) holding the previously-shifted-out $Q_0$; $M$: multiplicand. Examine $(Q_0,Q_{-1})$ each cycle: $01\to A{+}{=}M$, $10\to A{-}{=}M$, $00/11\to$ no-op; then arithmetic-shift-right $(A,Q,Q_{-1})$ | **Week 2 (new)** |
| $A$, $Q$, $M$ (division) | $A$: remainder (init 0); $Q$: dividend $\to$ quotient; $M$: divisor. Restoring: shift, $A{-}{=}M$, restore-if-negative. Non-restoring: shift, conditionally add/subtract based on prior sign, no restore, one final correction | **Week 2 (new)** |
| IEEE 754 single | 32 bits = 1 sign + 8 exponent + 23 mantissa; value $=(-1)^S\times(1.M)_2\times2^{E-127}$; bias 127; hidden leading 1 | **Week 3 (new)** |
| Float special values | Zero (exp 0, mant 0), denormal (exp 0, mant $\neq0$), $\pm\infty$ (exp all 1, mant 0), NaN (exp all 1, mant $\neq0$) | **Week 3 (new)** |
| Float add | Align → add → normalize → round; multiply = multiply mantissas, add exponents (minus bias once), normalize, round | **Week 3 (new)** |
| ULP / precision | ~7 significant decimal digits in single precision; rounding error $\le \tfrac12$ ULP; never compare floats with $==$ | **Week 3 (new)** |
| IR | Instruction Register — holds the instruction currently executing | **Week 4 (confirmed)** |
| MAR | Memory Address Register — holds the address for the current memory access | **Week 4 (confirmed)** |
| MDR | Memory Data/Buffer Register — holds data in transit to/from memory (aka MBR) | **Week 4 (confirmed)** |
| AC | Accumulator — implicit operand/result register in single-address ISAs | **Week 4 (confirmed)** |
| R0..Rn-1 | General-purpose register file | **Week 4 (confirmed)** |
| SP | Stack Pointer | **Week 4 (confirmed: stack organization)** |
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
| KIN / DOUT | Program-controlled I/O status flags: `KIN` set when a keystroke is ready in `KBD_DATA`; `DOUT` set when the display is ready for the next character in `DISP_DATA` | **Week 8 (new)** |
| IE | Interrupt-enable bit inside the processor status register (`PS`); `IE=0` masks every interrupt regardless of source | **Week 8 (new)** |
| KIRQ / DIRQ | Per-device interrupt-enable bits (keyboard/display) in that device's control register; a request reaches the CPU only when the device's own enable bit AND `PS.IE` both allow it | **Week 8 (new)** |
| Interrupt-vector table | Table of ISR starting addresses, one entry per device, indexed by a device-supplied identifying code for constant-time interrupt dispatch | **Week 8 (new)** |
| IPENDING / IENABLE | Processor control registers for vectored, priority interrupt dispatch: `IPENDING` latches which device(s) currently have a request pending; `IENABLE` masks which of those are allowed through to the priority encoder | **Week 8 (new)** |
| Master-ready / Slave-ready | Asynchronous-bus full-handshake signals: each changes only in response to the other, giving a skew-immune 4-step interlocked exchange (vs. a synchronous bus's shared clock edge) | **Week 8 (new)** |
| BR / BG | Bus-request / bus-grant arbitration lines: a candidate bus master asserts `BR`; the arbiter asserts `BG` to the winning requester (by priority), letting that device become bus master — the functional basis for DMA | **Week 8 (new)** |
| Exception | Any event that suspends normal control flow — I/O interrupt, divide-by-zero, illegal instruction, page fault, timer tick. Same jump-to-handler machinery as an interrupt; only the source differs (P&H Ch. 4; Hamacher §3.2.6) | **Week 8 (new)** |
| DMA controller registers | Source address, destination address, word count, control/status — written once by the CPU at setup; the DMA controller owns them through the transfer | **Week 8 (new)** |
| Burst / cycle-stealing / transparent (DMA modes) | Burst: DMA holds the bus for the entire block (fastest, starves CPU). Cycle stealing: one word per grant, bus released between words (slower, CPU keeps running). Transparent: transfers only during CPU cycles that don't use the bus (slowest, CPU never notices) | **Week 8 (new)** |

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
| 8 | I/O Techniques | Who watches an I/O device, and how much of the CPU does watching cost? | KIN/DOUT, IE/KIRQ/DIRQ, IPENDING/IENABLE, Master-ready/Slave-ready, BR/BG | Polling vs. interrupts vs. DMA vs. IOP head-to-head; synchronous vs. asynchronous bus timing |

## Practical / Lab Component (Nand2Tetris Track)

**Source of truth:** `syllabi/CS401_Lab_Syllabus_Nand2Tetris.pdf` (uploaded 2026-08-12) — the institute's official lab syllabus for CS401's L-T-P practical component (25% / 50 marks), previously undocumented anywhere in this workflow. Follows Nisan & Schocken's Nand2Tetris hardware track (*The Elements of Computing Systems*, Projects 1-5): five practicals building a full computer from a single Nand gate upward.

| Lab | Weeks (own schedule) | Chips/Tasks | Real source lecture for pre-lab theory | Status |
|---|---|---|---|---|
| 1 — Boolean Logic & Elementary Gates | 1-2 | 15 chips (Not..DMux8Way), all from Nand | *(none — gate-level Boolean algebra is a course prerequisite, not covered by any CS401 lecture; cite P&H App. A.2-A.4 directly, see below)* | Built |
| 2 — Boolean Arithmetic & the ALU | 3-4 | HalfAdder, FullAdder, Add16, Inc16, ALU (18 ops) | Week 2 (`02-number-systems-arithmetic` — two's complement, ripple-carry adders, ALU) | Planned |
| 3 — Sequential Logic & Memory | 5-7 | Bit, Register, RAM8→RAM16K (recursive), PC | Week 4 (`04-registers-instructions` — register organization) | Planned |
| 4 — Machine Language Programming | 8-9 | Hand-assembly; Mult.asm; Fill.asm | Week 4 (`04-registers-instructions` — instruction formats/cycle) | Planned |
| 5 — CPU & Computer (capstone) | 10-12 | CPU, Memory, Computer | Weeks 5-7 (`05-addressing-cpu-bus`, `06-hardwired-control`, `07-microprogrammed-control` — CPU organization, control-unit design) | Planned |

**Week-offset note:** the source PDF's own "CoA Unit Mapped" column names lecture *topics*, not the lecture's actual scheduled week — each lab runs 3-5 weeks after the CS401 lecture that actually teaches its prerequisite theory (e.g. Lab 4's "Instruction Set Architecture" theory is Week 4's content, but Lab 4 itself runs weeks 8-9). Confirmed with the instructor (2026-08-12) as intentional: Nand2Tetris has its own internal build-order (gates → arithmetic → memory → assembly → CPU) that doesn't need to lockstep with the lecture's chapter pacing. Every lab manual's Pre-Lab Reading section cites the lecture that **actually** covers the concept, not the lecture nominally running in the lab's own scheduled week.

**Toolchain:** the free Nand2Tetris software suite (Hardware Simulator, CPU Emulator, Assembler) + JRE 8+, from nand2tetris.org — entirely student-side. Nothing in this repo's own toolchain runs Java or executes `.hdl`/`.asm` files.

**Verification approach:** each lab ships **instructor-only reference solutions** (`Labs/CS401/lab-N-*-reference/`, never synced to `docs/` by `/deploy`) in the actual submission format — real `.hdl` files (`hdl/*.hdl`), written in the syntax confirmed against `syllabi/Hardware_Simulator_Tutorial.pdf` — plus a parallel Python design reference (`chips.py`). Since the real grading tool (the Java Hardware Simulator) can't run in this environment, a small custom HDL interpreter (`hdl_simulator.py`) parses and executes the actual `.hdl` files, and both the `.hdl` and Python references are checked against the same independent oracle (Python's native bitwise operators) via `test_hdl.py` / `test_chips.py` — not against each other, so a shared bug in one implementation wouldn't silently validate the other.

## Empirical Applications

| Application | Paper | Dataset | Lecture(s) | Purpose |
|------------|-------|---------|------------|---------|
| Two-machine comparison on one program ($10^7$ instr.: A = 2 GHz/CPI 2 vs. B = 3 GHz/CPI 3, then B CPI→1.5) | P\&H Ch. 1 Sec. 1.6 (p.28); Hamacher Ch. 1 | n/a (worked performance comparison) | Week 1 | Running thread making the performance equation, factor independence, and Amdahl's Law quantitative; shows a CPI (organization) win vs. a clock-rate win |
| RTL trace of `R1 \gets R2 + R3` | Hamacher Ch. 7; Mano Ch. 8 (Week 5, corrected 2026-08-06 — datapath/bus/addressing content); Mano Ch. 5 (Week 6, corrected 2026-08-06 — hardwired control-logic-gate content, was mis-cited as Ch. 7); Mano Ch. 7 (Week 7, confirmed — control-memory/microinstruction content) | n/a (worked hardware trace) | Week 5, Week 6, Week 7 | Running thread comparing single-bus (3 control steps via Y/Z) vs. three-bus (1 control step) organization — makes the cost/speed trade-off concrete and quantitative. Week 6 extends the same trace into a state table and Boolean control equations ($Y_{in}=D_{\text{ADD}}\cdot T_1$, etc.) for the hardwired control unit that drives it. Week 7 rebuilds the identical 3-step control unit as a microprogram (CM rows + MPC), giving a direct hardwired-vs.-microprogrammed comparison on the same worked example. |
| Compiling `A[i] = A[i] + 1` | Hamacher Ch. 7 | n/a (compiler-codegen example) | Week 5 | Motivates addressing modes from a real toolchain need: immediate (constant), based/indexed (array element), indirect (pointer) |
| Keyboard-input / display-output polling and interrupt worked traces (`KIN`/`DOUT`, `KIRQ`/`DIRQ`, `READWAIT`/`WRITEWAIT` loops, 5-step interrupt scenario); 3-master bus arbitration priority example | Hamacher Ch. 3 (p.95-119, page-verified 2026-08-11) + Ch. 7 SS7.1-7.4 (p.227-242, page-verified 2026-08-11); DMA/IOP general-treatment per Stallings Ch. 7 (no book.pdf on disk, chapter-level only) | n/a (worked I/O programs + hardware trace) | Week 8 | Running thread carrying one keyboard/display pair through polling then interrupts (programmer's view), then a 3-device arbitration example through the sync/async bus and DMA/IOP Acts (hardware view) — same "thread one worked example across the Act" pattern as Weeks 5-7's `R1<-R2+R3` trace |

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
