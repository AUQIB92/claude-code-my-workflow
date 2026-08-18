# Index: Computer Organization and Architecture — Designing for Performance, **11th edition** (Stallings2015)

**Source:** `master_supporting_docs/CS401/supporting_books/Stallings2015/book.pdf` (1111 PDF pages)
**Indexed:** 2026-08-17
**Extraction method:** text-layer (PyMuPDF); embedded PDF outline (227 entries) + book's own Contents (PDF pp. 7–12)

---

## ⚠️ Read this before citing

### 1. The directory name is a misnomer — this is the **11th edition**

The folder is `Stallings2015`, which implies the 10th edition (2015/2016). It is not. The PDF's own metadata title reads *"Computer Organization and Architecture - Designing for Performance, **Eleventh Edition**"*. The directory name and the `Bibliography_base.bib` key are kept as-is to avoid breaking existing citations in Lectures 06–08, but **every chapter number in this index is 11th-edition numbering**, which differs substantially from the 10th edition the syllabus was originally written against. See the mismatch table below.

### 2. There are two page-number systems, and the offset is **not constant**

This is a reflowed web-capture ebook (Producer: `Acrobat Web Capture 15.0`), not the print layout. Consequences:

- **Body pages carry no printed page number in the text layer** — you cannot read the printed page off a running head the way you can for PattersonHennessy2017.
- The **Contents (PDF pp. 7–12) does list the book's printed page numbers**, so chapter and numbered-section printed pages below are authoritative — taken from the book itself.
- The PDF↔printed offset **grows through the book** (Ch. 4: +37 · Ch. 5: +41 · Ch. 8: +60 · Ch. 19: +136) and drifts even *within* a chapter. **Never apply a fixed offset.**
- **Sub-subsection rows** (things the Contents does not list, e.g. "Mapping Function") give an **exact PDF page** and an **interpolated printed page marked `~`**. When page-citing one of those, cite the PDF page, or open the PDF and confirm the printed page before committing a `~` value to a slide.

**Citation convention for this book:** write `Stallings 11e, §5.2, p.~147 (PDF 188)`. The section number is the stable, checkable anchor; the PDF page makes it independently verifiable by `/verify-claims`.

---

## Syllabus ↔ 11th-edition chapter mismatches (Step 0.5 result)

`syllabi/CS401.md` cites Stallings by 10th-edition chapter numbers. Verified against this edition's Contents:

| Week | Syllabus cites | **Actual 11e location** | Status |
|---|---|---|---|
| 1 | Ch. 1–2 | Ch. 1 Basic Concepts and Computer Evolution; Ch. 2 Performance Concepts | ✅ correct |
| 3 | Ch. 9 (IEEE 754) | **Ch. 11 §11.4–11.5** Floating-Point Representation / Arithmetic | ❌ wrong number |
| 7 | Ch. 16 (microprogrammed control) | **Ch. 19 §19.4** Microprogrammed Control | ❌ wrong number (already flagged in knowledge base) |
| 8 | Ch. 8 (I/O) | Ch. 8 Input/Output | ✅ correct (corrected 2026-08-11) |
| 9 | Ch. 4 (cache) | **Ch. 4** = *Memory Hierarchy* only; **cache is Ch. 5**; ROM types are **Ch. 6 §6.1** | ⚠️ partially wrong — see below |
| 10 | Ch. 8, 6 (VM, secondary storage) | VM/paging/segmentation = **Ch. 9 §9.3–9.5**; secondary storage = **Ch. 7**; internal memory = Ch. 6 | ❌ wrong numbers |
| 11 | Ch. 17–18 (Flynn, pipeline hazards) | Flynn = **Ch. 20 §20.1** (one page, thin); pipeline hazards = **Ch. 16 §16.4** | ❌ wrong numbers |
| 12 | Ch. 13, 18 (pipelining, RISC/CISC) | RISC/CISC = **Ch. 17**; instruction pipelining = **Ch. 16 §16.4**; superscalar/ILP = Ch. 18 | ❌ wrong numbers |

**Fixed in this pass:** Week 9 only (the week being built). Weeks 3, 10, 11, 12 are recorded here and left for their own build passes — correcting them now would edit syllabus rows for unbuilt weeks without verifying the surrounding reading load.

### Week 9 specifically

The syllabus row *"Memory hierarchy characteristics; Main Memory (ROM types); Cache Memory organization and mapping; replacement algorithms"* maps to **three** chapters in this edition, not one:

| Syllabus topic | 11e location | Confirmed present? |
|---|---|---|
| Memory hierarchy characteristics | Ch. 4 (all), esp. §4.2–4.3 | ✅ |
| Main Memory (ROM types) | **Ch. 6 §6.1** (ROM, PROM, EPROM, EEPROM, flash) | ✅ |
| Cache organization and mapping | Ch. 5 §5.1–5.2 | ✅ |
| Replacement algorithms | Ch. 5 §5.2 "Replacement Algorithms" | ✅ **but only LRU/FIFO/LFU/Random** — see gap below |

---

## ❌ Coverage gaps — topics NOT in this book

Verified by full-text search across all 1111 pages. Do **not** page-cite Stallings for these:

| Topic | Hits | Guidance |
|---|---|---|
| **Belady's anomaly** | **0** | Not in this book at all. Not in Stallings' cache treatment (it is a page-replacement result). Keep as general treatment or source elsewhere. |
| **Optimal / OPT replacement** | **0** | Stallings names exactly four cache replacement algorithms: LRU, FIFO, LFU, Random. OPT is absent. |
| Clock / second-chance policy | 0 | Absent. |
| "Associative memory" as a topic | 3 (all glossary/index/key-term) | Week 10's "Associative memory" has no standalone treatment. Closest real content is **content-addressable memory (CAM), §5.2, PDF 193–194** — genuinely useful, but it is CAM-as-cache-hardware, not the classic associative-memory unit. |
| Restoring / non-restoring division | 1 each | Named only in passing (PDF 449, 471). Division is covered but these algorithm names are not the book's framing — stay with Hamacher/Mano. |
| Flynn's taxonomy | 3 (one substantive) | Only §20.1, roughly one page. Too thin to anchor Week 11 — use Hamacher Ch. 12 or P&H Ch. 6. |
| Working set | 1 | Effectively absent. |

**Consequence for the Week 09 deck:** GATE-style questions on Optimal replacement and Belady's anomaly are legitimate exam content, but they **cannot be attributed to Stallings**. Either source them from another indexed book or present them as standard general treatment with no page cite.

---

## Chapter Index

Printed pages are from the book's own Contents. PDF pages are from the embedded outline. **Both are given because the offset is non-constant.**

| Ch | Title | Printed pp. | PDF pp. | Summary | Key terms | Named figures / tables |
|---|---|---|---|---|---|---|
| 1 | Basic Concepts and Computer Evolution | 1–36 | 27–66 | Organization vs. architecture; structure/function; IAS machine; gates, memory cells, chips; x86 and ARM evolution; embedded/IoT | computer architecture, computer organization, ISA, control unit, ALU, MMU, MPU, multicore, microcontroller, Moore's law, system bus | IAS structure figures |
| 2 | Performance Concepts | 37–71 | 67–106 | Designing for performance; multicore/MIC/GPGPU; **Amdahl's law and Little's law (§2.3, pp. 45–47)**; CPI/MIPS; arithmetic vs. harmonic vs. geometric mean; SPEC | Amdahl's law, Little's law, clock rate, CPI, MIPS rate, throughput, benchmark, SPEC, arithmetic/geometric/harmonic mean, speed vs. rate metric | SPEC benchmark tables |
| 3 | A Top-Level View of Computer Function and Interconnection | 72–111 | 107–148 | Components; instruction cycle and interrupts; interconnection structures; bus interconnection; QPI; PCI Express | instruction cycle, fetch/execute cycle, interrupt, ISR, MAR, MBR, system bus, arbitration, PCIe, QPI, lane, flit, phit | Fig. 3.4 (hypothetical machine) |
| **4** | **The Memory Hierarchy: Locality and Performance** | **112–137** | **149–178** | **Week 09 anchor.** Principle of locality (temporal/spatial, instruction/data); memory-system characteristics; the hierarchy; multilevel performance modeling | locality of reference, temporal/spatial locality, data vs. instruction locality, hit ratio, access time, memory cycle time, sequential/direct/random access, memory hierarchy, multilevel cache, L1–L4 | Table 4.1 Key Characteristics of Memory Systems (PDF 156) · Fig. 4.6 The Memory Hierarchy (PDF 160) · Fig. 4.7 Cost/Size/Speed (PDF 161) · Fig. 4.8 Access time vs. hit ratio (PDF 162) · Table 4.2 Memory Device Characteristics (PDF 164) · Fig. 4.14 Multilevel Access Performance Model (PDF 172) |
| **5** | **Cache Memory** | **138–176** | **179–223** | **Week 09 core.** Cache principles; the full elements-of-cache-design treatment (mapping, replacement, write policy, line size, cache count); x86 and z13 organizations; timing models | cache line/block/set, tag, cache hit/miss, direct mapping, associative mapping, set-associative mapping, CAM, replacement algorithm, dirty bit, use bit, write allocate / no write allocate, line size, logical vs. physical cache, unified vs. split cache, victim cache, critical word first | see §5.2 breakdown below |
| **6** | **Internal Memory** | **177–209** | **224–262** | **Week 09 (ROM types) + Week 10.** Semiconductor main memory incl. the full ROM family; Hamming ECC; DDR DRAM; eDRAM; flash; emerging NVM | RAM, DRAM, SRAM, **ROM, PROM, EPROM, EEPROM**, flash (NAND/NOR), read-mostly memory, nonvolatile memory, Hamming code, SEC / SEC-DED, syndrome, soft error, hard failure, SDRAM, DDR, STT-RAM, PCRAM, ReRAM | §6.1 Semiconductor Main Memory (PDF 226–236) — **the ROM-types source** · §6.2 Error Correction (PDF 236–242) |
| 7 | External Memory | 210–244 | 263–304 | **Week 10.** Magnetic disk geometry and timing; **RAID levels 0–6 (§7.2)**; SSDs; optical (CD/DVD/Blu-ray); magnetic tape | magnetic disk, platter, cylinder, head, CAV, CLV, multiple zone recording, RAID, SSD, flash memory, CD-ROM/R/RW, DVD, Blu-ray, pit, land, magnetic tape | §7.1 Magnetic Disk (PDF 265) · §7.2 RAID (PDF 276–288) · §7.3 SSD (PDF 288) · §7.4 Optical (PDF 292) |
| 8 | Input/Output | 245–290 | 305–355 | **Week 08 anchor (already used).** External devices; I/O modules; programmed I/O; interrupt-driven I/O; **DMA (§8.5)**; direct cache access; **I/O channels and processors (§8.7)** | programmed I/O, interrupt-driven I/O, **DMA**, cycle stealing, **I/O channel, I/O processor**, selector/multiplexor channel, memory-mapped vs. isolated I/O, DCA, InfiniBand, Thunderbolt | §8.3 Programmed I/O (PDF 312) · §8.4 Interrupt-Driven I/O (printed 256) · §8.5 DMA (printed 265) · §8.7 Channels/IOP (PDF 342) |
| 9 | Operating System Support | 291–333 | 356–407 | **Week 10 anchor for virtual memory.** OS overview; scheduling; **§9.3 Memory Management — partitioning, paging, virtual memory, segmentation, TLB**; x86 and ARM memory management | virtual memory, paging, **segmentation**, page table, **TLB / translation lookaside buffer**, demand paging, logical vs. physical address, partitioning, swapping, thrashing, memory protection, resident monitor | §9.3 Memory Management (PDF 376–389) · §9.4 Intel x86 Memory Management (PDF 389) · §9.5 ARM Memory Management (PDF 396) |
| 10 | Number Systems | 334–343 | 408–422 | Decimal/positional systems; binary; base conversion; hexadecimal | radix, base, positional number system, radix point, nibble, MSD, LSD | — |
| 11 | Computer Arithmetic | 344–387 | 423–473 | **Week 2–3 anchor (syllabus mis-cites this as "Ch. 9").** ALU; integer representation (sign-magnitude, 1s/2s complement); integer arithmetic incl. **Booth's algorithm (PDF 442–446)**; **IEEE 754 (§11.4, PDF 450+)**; floating-point arithmetic | twos complement, sign-magnitude, biased representation, fixed-point, floating-point, significand, mantissa, exponent, guard bits, rounding, overflow/underflow (exponent and significand), normal/subnormal number, partial product | §11.3 Integer Arithmetic (PDF 432) · §11.4 Floating-Point Representation (PDF 450) · §11.5 Floating-Point Arithmetic (PDF 459) |
| 12 | Digital Logic | 388–431 | 474–525 | Boolean algebra; gates; combinational circuits and minimization; sequential circuits; PLDs | Boolean algebra, gates, combinational circuit, Karnaugh map, Quine–McCluskey, POS, decoder, multiplexer, flip-flops (S–R, D, J–K), counter, register, PLA/PAL/CPLD, excitation table | §12.3 Combinational Circuits (PDF 484) · §12.4 Sequential Circuits (PDF 505) |
| 13 | Instruction Sets: Characteristics and Functions | 432–475 | 526–580 | **Week 4.** Machine instruction characteristics; operand types; x86/ARM data types; operation types; endianness (App. 13A) | machine instruction, operand, opcode, accumulator, stack, push/pop, branch/jump/skip, procedure call/return, reentrant procedure, big/little/bi-endian, packed decimal, arithmetic vs. logical shift | App. 13A Endianness (PDF 577) |
| 14 | Instruction Sets: Addressing Modes and Formats | 476–505 | 581–613 | **Week 5 anchor.** All addressing modes; x86/ARM modes; instruction formats | effective address, immediate, direct, indirect, register, register indirect, displacement, base-register, relative addressing, indexing, autoindexing, pre/postindexing, instruction format | §14.1 Addressing Modes (PDF 582) · §14.3 Instruction Formats (PDF 595) |
| 15 | Assembly Language and Related Topics | 506–536 | 614–652 | Assembly concepts and elements; assemblers (one/two-pass); loading and linking | assembler, one-pass / two-pass assembler, mnemonic, directive, label, macro, relocation, linking, dynamic linker, linkage editor | §15.7 Loading and Linking (PDF 640) |
| 16 | Processor Structure and Function | 537–585 | 653–707 | **Weeks 4, 11–12.** Processor and register organization; instruction cycle; **§16.4 Instruction Pipelining — the pipeline-hazard source**; x86 and ARM processors | instruction pipeline, instruction prefetch, **pipeline hazard**, branch prediction, delayed branch, condition code, PSW, reservation station, functional unit | §16.2 Register Organization (PDF 657) · **§16.4 Instruction Pipelining (PDF 667–685)** |
| 17 | Reduced Instruction Set Computers | 586–628 | 708–757 | **Week 12 anchor.** Instruction execution characteristics; large register files; compiler register optimization; RISC ISA; RISC pipelining; MIPS R4000; SPARC; **§17.9 CISC, RISC and contemporary systems** | RISC, CISC, register file, register window, delayed branch, delayed load, data forwarding, instruction buffer, reorder buffer, SPARC | §17.5 RISC Pipelining (PDF 730) · §17.9 CISC/RISC (PDF 752) |
| 18 | Instruction-Level Parallelism and Superscalar Processors | 629–668 | 758–804 | ILP; superscalar design issues; dependencies and register renaming; Intel Core; ARM Cortex-A8/M3 | superscalar, superpipelined, ILP, true data / procedural / output dependency, antidependency, resource conflict, register renaming, in-order vs. out-of-order issue/completion, instruction window, commit/retire | §18.2 Design Issues (PDF 768) |
| 19 | Control Unit Operation and Microprogrammed Control | 669–700 | 805–844 | **Weeks 6–7 anchor (syllabus mis-cites this as "Ch. 16").** Micro-operations; control of the processor; **§19.3 hardwired implementation**; **§19.4 microprogrammed control** incl. horizontal/vertical microinstructions | micro-operation, control signal, control unit, control path, control bus, hardwired implementation, microinstruction, horizontal/vertical microinstruction, control memory | §19.3 Hardwired Implementation (PDF 826) · §19.4 Microprogrammed Control (PDF 830) |
| 20 | Parallel Processing | 701–735 | 845–883 | **Week 11.** §20.1 Multiple processor organizations — **the only Flynn's-taxonomy content in the book (PDF 847, ~1 page)**; SMPs; **MESI cache coherence**; multithreading; clusters; NUMA | SISD/SIMD/MISD/MIMD, multiprocessor, SMP, cache coherence, MESI protocol, snoopy vs. directory protocol, cluster, failover/failback, NUMA, UMA | §20.1 (PDF 847) · §20.3 MESI (PDF 855) |
| 21 | Multicore Computers | 736–767 | 884–921 | Hardware/software performance issues; Pollack's rule; multicore organization; heterogeneous multicore; i7, Cortex-A15, z13 | multicore processor, chip multiprocessor, Pollack's rule, SMT, fine/coarse/hybrid-grained threading, MOESI, heterogeneous multicore | §21.3 Multicore Organization (PDF 898) |
| A | System Buses | 768–776 | 922–931 | **Week 5 supplement.** Bus structure; multiple-bus hierarchies; elements of bus design | bus structure, multiple-bus hierarchy, bus width, bus arbitration | — |
| B | Victim Cache Strategies | 777–781 | 932–936 | Victim cache; selective victim cache | victim cache, selective victim cache | — |
| C | Interleaved Memory | 782–784 | 937–939 | Memory interleaving | interleaved memory, memory bank | — |
| D | International Reference Alphabet | 785–787 | 940–943 | IRA character code | IRA | — |
| E | Stacks | 788–794 | 944–951 | **Week 4 supplement.** Stacks; stack implementation; expression evaluation | stack, stack pointer, reverse Polish notation | — |
| F | Recursive Procedures | 795–806 | 952–964 | Recursion; activation trees; stack implementation | activation tree, recursion vs. iteration | — |
| G | Additional Instruction Pipeline Topics | 807–825 | 965–988 | Reservation tables; reorder buffers; **Tomasulo's algorithm**; scoreboarding | pipeline reservation table, reorder buffer, Tomasulo's algorithm, scoreboarding | — |
| — | Glossary | 826–834 | 989–1002 | Definitions of all key terms | — | — |
| — | References | 835–843 | 1003–1017 | Bracketed-key bibliography (`[SMIT82]`, `[DENN05]`, …) | — | — |

---

## §5.2 Elements of Cache Design — subsection breakdown (Week 09 GATE core)

`§5.2` runs **printed pp. 143–164 / PDF pp. 184–208**. Printed pages marked `~` are interpolated (see the page-number warning above); PDF pages are exact.

| Subsection | PDF pp. | Printed pp. | What's there |
|---|---|---|---|
| (intro) Table 5.1 Elements of Cache Design | 184 | 143 | The canonical taxonomy table: cache addresses, size, mapping function, replacement algorithm, write policy, line size, number of caches |
| Cache Addresses | 184–186 | 143–~145 | Logical vs. physical cache; Fig. 5.5 Logical and Physical Caches (PDF 185) |
| Cache Size | 186–187 | ~145–~146 | Table 5.2 Cache Sizes of Some Processors (PDF 186); Table 5.3 Cache Access Methods (PDF 187) |
| **Mapping Function** | **187–203** | **~146–~160** | The three schemes in full — see rows below |
| — Direct Mapping | 188–192 | ~147–~151 | Address split into **tag / line (index) / word (offset)**; Fig. 5.6 Mapping Main Memory to Cache (PDF 189); **Fig. 5.7 Direct-Mapping Cache Organization (PDF 190)**; **Fig. 5.8 Direct Mapping Example (PDF 192)** |
| — Content-Addressable Memory | 193–194 | ~151–~152 | CAM search function and cell array; Fig. 5.9 (PDF 194). The hardware that makes associative lookup possible |
| — Fully Associative Mapping | 194–197 | ~152–~154 | Address split into **tag / word** only; **Fig. 5.10 Fully Associative Cache Organization (PDF 195)**; **Fig. 5.11 Associative Mapping Example (PDF 197)** |
| — k-Way Set-Associative Mapping | 197–202 | ~154–~159 | Address split into **tag / set / word**; Fig. 5.12 Mapping to k-Way Set Associative (PDF 198); **Fig. 5.13 k-Way Set-Associative Cache Organization (PDF 200)**; **Fig. 5.14 Two-Way Set-Associative Example (PDF 201)**; Fig. 5.15 Varying Associativity over Cache Size (PDF 202) |
| **Replacement Algorithms** | **203** | **~160** | **LRU** (USE bit for 2-way; index list for fully associative — "the most popular"), **FIFO** (round-robin / circular buffer), **LFU** (per-line counter), **Random** (cites `[SMIT82]`: only slightly inferior). Note: direct mapping needs no replacement algorithm — no choice exists. **OPT and Belady's anomaly are absent.** |
| Write Policy | 203–205 | ~160–~162 | **Write through** vs. **write back** (dirty bit); the I/O-module and multiprocessor coherence problems; writes ≈15% of references `[SMIT82]`, up to 33–50% for HPC |
| Line Size | 205 | ~162 | Block-size vs. hit-ratio trade-off |
| Number of Caches | 205–208 | ~162–~164 | Multilevel caches (Fig. 5.16 L1/L2 total hit ratio, PDF 206); unified vs. split cache |

**Also relevant to Week 09:**

- **§5.1 Cache Memory Principles** (PDF 180–183 / printed 139–142) — Fig. 5.1 Cache and Main Memory, **Fig. 5.2 Cache/Main Memory Structure (PDF 181)**, **Fig. 5.3 Cache Read Operation (PDF 182)**, Fig. 5.4 Typical Cache Organization (PDF 183).
- **§5.5 Cache Performance Models** (PDF 215–218 / printed 169–172) — **Table 5.6 Cache Timing Equations (PDF 216)** and Table 5.7 Cache Performance Improvement Techniques (PDF 217). This is the AMAT-style quantitative material; pairs with **§4.4 Performance Modeling of a Multilevel Memory Hierarchy** (PDF 167–173 / printed 128–134).
- **§5.6 Problems** (PDF 220–223) — worked numerical problems in exactly the GATE style: address-field splitting (5.3, 5.4, 5.6, 5.7, 5.9, 5.11–5.13), LRU implementation in a 4-way set-associative cache (5.14), and the Intel 80486 pseudo-LRU strategy with Fig. 5.19 (5.10, PDF 221–222).

---

## Cross-references

- `.claude/rules/textbook-grounding.md` — the invariant this index satisfies.
- `.claude/rules/knowledge-base-CS401.md` — the source-of-record table; its Stallings2015 row is updated to point here.
- `syllabi/CS401.md` — Week 9's Stallings citation corrected against this index; Weeks 3, 10, 11, 12 still carry 10th-edition numbers (see mismatch table).
- `master_supporting_docs/CS401/supporting_books/Hamacher2002/index.md`, `.../PattersonHennessy2017/index.md` — the other two indexed CS401 textbooks. For Optimal/Belady and Flynn's taxonomy, prefer those.
