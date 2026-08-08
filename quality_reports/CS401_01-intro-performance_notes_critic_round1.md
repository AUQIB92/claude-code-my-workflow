# Notes vs Beamer Parity Audit: CS401/01-intro-performance

**Beamer source:** `Slides/CS401/01-intro-performance.tex` (27 content frames + title frame + 5 transition slides)
**Notes:** `Notes/CS401/01-intro-performance-notes.tex`
**Round:** 1  **Date:** 2026-08-08

## Verdict: APPROVED

Every Beamer frame's core idea appears in the Notes, and the Notes invent nothing the deck does not carry. Citation sets match exactly (both `PattersonHennessy2017_computer_organization_design` and `Hamacher2002_computer_organization`), and every page number traces to the PattersonHennessy2017 index. Only a few harmless prose elaborations remain, all Minor.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 27 content frames map to Notes sections/examples/figures (frame-by-frame table below); both TikZ diagrams reproduced 1:1 |
| No invention | Pass | No novel claims, examples, or citations; only 3 benign definitional/synthesis elaborations (see m1–m3) |
| Citation parity | Pass | Beamer unique keys `{PattersonHennessy2017_computer_organization_design, Hamacher2002_computer_organization}` == Notes unique keys; both exist in `Bibliography_base.bib` (lines 63, 39) |
| Notation fidelity | Pass | `IC`, `CPI`, `T_c`, `f=1/T_c`, MIPS formula, CPU-time equation, and Amdahl's Law `Speedup = 1/[(1-f)+f/S_f]` all identical to Beamer |
| Textbook-page honesty | Pass | Only pages p.3 (Sec 1.1), p.16 (Sec 1.4), p.28 (Sec 1.6) used — all present in Beamer frames and all in `PattersonHennessy2017/index.md` line 26; Hamacher cited at Ch. 1 chapter-level only |

## Critical Issues (MUST FIX)

None.

## Major Issues (SHOULD FIX)

None.

## Minor Issues (NICE TO FIX)

### m1: Definitional elaboration in basic-structure prose
- **Location:** `01-intro-performance-notes.tex` line 78 (§1.3, The Basic Structure of a Computer)
- **Text:** "The CPU is where computation happens; memory holds instructions and data; I/O connects the machine to the outside world"
- **What's wrong:** Beamer frame 6 (Basic Structure) states only the three-part structure and the bus connection; the CPU/memory/I/O role sentence is added by the Notes.
- **Fix:** Either leave as acceptable textbook-flavored expansion (it is consistent with the P&H Sec. 1.4 citation and the diagram), or trim to match the Beamer text exactly.

### m2: Synthesis elaboration in "The Thread, Closed"
- **Location:** `01-intro-performance-notes.tex` line 259 (§5.1)
- **Text:** "The comparison used every tool in the chapter: the performance equation to compute time, the factor table to see which lever was pulled, and time (not MIPS) as the comparison metric."
- **What's wrong:** The Beamer "The Thread, Closed" frame does not name the factor table; the Notes adds it as an interpretive summary.
- **Fix:** Optional; harmless synthesis, or drop the "factor table" mention to stay literal.

### m3: Stylistic flourish in Introduction
- **Location:** `01-intro-performance-notes.tex` line 54 (§1 Introduction)
- **Text:** "The thread is quantitative throughout --- speed is a number, not an adjective."
- **What's wrong:** Rhetorical addition absent from the Beamer welcome frame.
- **Fix:** Optional; keep if the author wants the prose voice, delete for strict parity.

## Frame-to-Section Content Map (evidence for Content parity = Pass)

| Beamer frame | Notes location |
|---|---|
| Welcome: What This Course Is | §1 Introduction (line 54) |
| Roadmap: Four Questions, One Thread | §1 Introduction (line 54, thread) + section structure |
| Architecture vs. Organization | §1.1 (line 60) |
| Why the Distinction Matters | §1.1 (line 70) |
| Classes of Computers | §1.2 (line 74) |
| The Basic Structure of a Computer | §1.3 + Figure 1.1 (lines 78–101) |
| The Instruction Cycle Preview | §1.4 (line 105) |
| Motivation: What Does "Faster" Mean? | §2.1 (line 112) |
| Definition: Execution Time and Its Three Factors | §2.2 definitionbox (lines 114–121) |
| Who Controls Each Factor? | §2.2 + Table 1.1 (lines 123–140) |
| Worked Example: Two Machines, One Program | Example 1.1 (lines 146–153) |
| Worked Example: Breaking the Tie | Example 1.2 (lines 155–162) |
| Socratic Check: Which Component Should You Improve? | §2.4 (line 166) |
| What Do We Measure? | §3.1 (line 172) |
| MIPS: A Metric to Be Careful With | §3.2 (lines 176–181) |
| Worked Example: The MIPS Trap | Example 1.3 (lines 183–190) |
| Socratic Check: Why Not Just Count Instructions? | §3.3 (line 194) |
| Motivation: Speeding Up One Part | §4.1 (line 201) |
| Amdahl's Law | §4.2 definitionbox (lines 203–209) |
| Amdahl's Law: The Ceiling | Figure 1.2 + prose (lines 211–229) |
| Worked Example: Applying Amdahl's Law | Example 1.4 (lines 233–240) |
| Worked Example: The Ceiling in Action | Example 1.5 (lines 242–249) |
| Socratic Check: The Parallelism Twist | §4.4 (line 253) |
| The Thread, Closed | §5.1 (line 259) |
| Bridge to Week 2 | §5.2 (line 263) |
| Summary | §5.3 (line 267) |

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames (content, excl. titlepage) | 27 |
| Beamer transition slides | 5 |
| Notes top-level sections | 6 |
| Citation keys: Beamer / Notes | 2 / 2 (both shared) |
| Critical / Major / Minor | 0 / 0 / 3 |

**Files reviewed:**
- `Slides/CS401/01-intro-performance.tex`
- `Notes/CS401/01-intro-performance-notes.tex`
- `Bibliography_base.bib`
- `master_supporting_docs/CS401/supporting_books/PattersonHennessy2017/index.md`
