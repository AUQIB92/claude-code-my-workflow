# Source Registry — Competitive-Exam PYQ Books

**Purpose:** single source of truth for *which local PYQ books exist, what they cover, and how to extract from them.* The `/competitive-exam-questions` skill consults this registry in Phase 0 to decide **availability**: a sub-topic is sourced from a local book iff it appears here with a usable PDF page range.

**Indexed:** 2026-08-07

## Availability model (the sourcing ladder)

For every sub-topic of a target lecture, sourcing resolves in this order:

| Tier | Source | When it applies | Provenance tag |
|------|--------|-----------------|----------------|
| 1 | **Local PYQ book** (this registry) | Topic is present below with a page range | `[GATE CS <year> Q<n>, verified — GATEOverflow V3 p.<pdfpage>]` |
| 2 | **Web-sourced PYQ + CoVe** (skill Phase 1 fallback) | Topic NOT in any local volume | `[GATE CS <year>, verified — web]` |
| 3 | **Original GATE-pattern** (skill Phase 2) | No verified real question found anywhere | `[Original, GATE-pattern]` |

Tier 1 is **authentic by construction** (the book is a compilation of real GATE papers with year + question number printed on the page). The **answer** still needs independent verification (see "Answers" below) because this book's answer keys are collapsed and absent from extraction.

## The volumes

| Volume | File | Pages | Subjects (GATE CSE) | Relevancy |
|--------|------|-------|----------------------|-----------|
| 1 | `GATE-PYQs/filter1_volume1.pdf` | 375 | Discrete Math (set theory, combinatorics, relations, group theory, FOL, probability, statistics), Engineering Mathematics (linear algebra, calculus), Aptitude (quantitative, verbal, logical) | Courses using DM/EM/Aptitude (e.g., GATE CS prep, MATH courses) |
| 2 | `GATE-PYQs/filter1_volume2.pdf` | 403 | Algorithms (asymptotics, sorting, graph, DP, greedy), Data Structures (trees, heaps, hashing, lists), Compilers (parsing, SDT, optimization), Theory of Computation (FA, PDA, TM, decidability), C Programming | Courses covering algorithms/DS/compilers/TOC |
| 3 | `GATE-PYQs/filter1_volume3.pdf` | 469 | **Computer Organization & Architecture (CO&A)** (ch. 1, pdf 28-92), plus Digital Logic (pdf 287-361), Operating Systems (pdf 377-467), DBMS (pdf 181-272), Computer Networks (pdf 111-164) | **CS401 weeks 1-12** (CO&A is the primary relevant chapter) |

All three are the **GATEOverflow for GATE CSE** compilation (community-verified past GATE questions, topic-organized, each tagged with year, question number, subject, topic, difficulty). All have a text layer; math values and answers are image/collapsed (see Extraction constraints).

## Topic → page map (Volume 3 — CO&A & CS401-relevant, PDF pages)

Question headings are of the form `1.5.23 Cache Memory: GATE CSE 2008 | Question: 71`. **PDF page numbers are the citation unit** (the book's printed page numbers differ from PDF indices; the heading-based map below is authoritative and page-exact).

| Topic | # Qs | PDF pages | Notes |
|-------|-----:|-----------|-------|
| Addressing Modes | 17 | 28-31 | Covers Week 5 |
| Average Memory Access Time (AMAT) | 3 | 32-33 | Covers Week 9-10 |
| CISC RISC Architecture | 2 | 34 | Covers Week 12 |
| Cache Memory | 61 | 34-48 | Covers Week 9; largest CO&A topic |
| Conflict Misses | 1 | 50 | Week 9 |
| Control Unit | 1 | 50 | Week 6-7 (thin local coverage) |
| DMA | 8 | 50 (also 379 in OS ch.) | Week 8 |
| DRAM | 1 | 52 | Week 9 |
| Data Dependency | 3 | 52-53 | Week 11 |
| Data Hazards | 1 | 53 | Week 11 |
| Data Path | 7 | 54-56 | Week 5-6 |
| Direct Mapping | 5 | 57-58 | Week 9 |
| Hazards | 1 | 58 | Week 11 |
| IO Handling | 13 | 59 (also 395 in OS ch.) | Week 8 |
| Instruction Execution | 7 | 61-62 | Week 4-5 |
| Instruction Format | 11 | 62-64 | Week 4 |
| Instruction Set Architecture | 1 | 65 | Week 4-5 |
| Interrupts | 16 | 65 (also 397 in OS ch.) | Week 8 |
| Machine Instruction | 18 | 67-74 | Week 4-5 |
| Memory Interfacing | 10 | 75 | Week 9 |
| Microprogramming | 7 | 77-78 | Week 7 |
| Pipelining | 33 | 80-89 | Week 11-12; largest after cache |
| Runtime Environment | 2 | 90-91 | Week 4 (operand addressing) |
| Speedup | 4 | 91 | Week 11 |
| Stall | 1 | 92 | Week 11 |
| Virtual Memory | 43 | 92 (also 467 in OS ch.) | Week 10; largest after cache |

## Topic → page map (Volume 1 — Discrete Math / EM / Aptitude)

Complete topic map extracted 2026-08-07 (all PDF pages, heading-verified). Key clusters: Set Theory 121-125, Relations 114-120, Combinatorics/Counting 25-38, Group Theory 100-106, Lattice 106-108, First Order Logic 63-70, Propositional Logic 73-80, Probability 215-221, Linear Algebra (Matrix 173-177, Eigen Value 165-170, Determinant 162-164), Calculus (Limits 145-146, Integration 143-144, Differentiation 140-142), Aptitude (quantitative 265-312, verbal 341-373, reasoning 237-363). See `map` section below for the full per-topic list.

## Topic → page map (Volume 2 — Algorithms / DS / Compilers / TOC)

Complete topic map extracted 2026-08-07 (all PDF pages, heading-verified). Key clusters: Asymptotic Notations 27-31, Recurrence Relation 85-92, Sorting 99-102, Binary Tree 34-224 (spans, earliest cluster 34-60), Binary Search Tree 33-214, Minimum Spanning Tree 72-80, Graph Search 46-50, Time Complexity 104-249, Hashing 53-230, Regular Language 394-400, Finite Automata 349-359, Turing Machine 401, Context Free Language 332-339, Grammar/Parsing 133-171, Programming In C 298-306. See `map` section below for the full per-topic list.

## Extraction constraints (READ FIRST)

1. **Text layer is partial.** Question headings, topic names, GATE years, question numbers, tags, and *most option text* are extractable via `pdftotext`. But **mathematical values are rendered as embedded images** (small 30-95px PNGs) and drop out of the text layer entirely.
2. **Answer keys are collapsed.** Each question carries an `Answer key☟` toggle that is collapsed in the HTML→PDF export; **no answer text exists in the PDF at all** (1435 toggles, ~24 stray "ANS" strings in the whole volume).
3. **This repo's PDF-skill model cannot render PDFs/images** (Read tool returns "model does not support PDF/image input" in the current environment). So the only reliable route to full question text is the **render + OCR sub-pipeline** below.
4. **gateoverflow.in is bot-blocked** (403) to direct fetch in the current environment; answers must be verified via WebSearch in the skill's forked context (which has WebSearch), not via direct page fetch.

### The render + OCR sub-pipeline (Tier-1 question text recovery)

Used whenever a Tier-1 question's math values are needed verbatim (they always are, for numerical GATE questions):

```powershell
$env:Path = "C:\Users\auqib\AppData\Local\Programs\MiKTeX\miktex\bin\x64;" + $env:Path
$f = "...\GATE-PYQs\filter1_volume3.pdf"
mgs -sDEVICE=png16m -r300 -dNOPAUSE -dBATCH -dSAFER -dFirstPage=<N> -dLastPage=<N> "-sOutputFile=C:\temp\p%03d.png" $f
& "C:\Program Files\Tesseract-OCR\tesseract.exe" C:\temp\p001.png C:\temp\p001 --psm 3
```

OCR at 300dpi recovers the full question including math values (verified 2026-08-07 on p.40: "2-way set associative data cache of size 64K bytes … 32 bit virtual addresses … page size 4K bytes … A. 32Kbits B. 34Kbits C. 64Kbits D. 68Kbits"). Cleanup temp PNGs/TXT after transcription; do not commit them.

### Answers

The book's own answers are unrecoverable (collapsed). Verify each Tier-1 question's answer in the skill's forked context:
- `WebSearch` for the GATE year + question number (e.g., `"GATE 2008 CS 71 cache tag answer"`), cross-check 2+ independent sources (GeeksforGeeks, official GATE archives, NPTEL, previous-year solution sets).
- Or use the GATEOverflow **online** question page (same question ID) if reachable from the skill context.
- Only mark `[verified]` when the answer is confirmed; otherwise move the question to `[Original, GATE-pattern]` per the sourcing ladder.

## Full topic map — Volume 1 (PDF pages, heading-verified 2026-08-07)

| Topic | # Qs | PDF pages | Topic | # Qs | PDF pages |
|-------|-----:|-----------|-------|-----:|-----------|
| Set Theory | 23 | 121-125 | Relations | 37 | 114-120 |
| Functions | 32 | 94-279 | Group Theory | 33 | 100-106 |
| Lattice | 9 | 106-108 | Partial Order | 9 | 111-112 |
| Propositional Logic | 38 | 73-80 | First Order Logic | 29 | 63-70 |
| Combinatorics (Counting) | 9 | 25-38 | Generating Functions | 6 | 26-27 |
| Pigeonhole Principle | 2 | 27 | Modular Arithmetic | 2 | 27 |
| Recurrence Relation | 5 | 28 | Balls In Bins | 5 | 20-21 |
| Graph Theory (all) | ~75 | 39-55 | Probability | 33 | 215-298 |
| Conditional Probability | 12 | 205-207 | Bayes Theorem | 3 | 200-269 |
| Expectation | 10 | 208-210 | Random Variable | 5 | 221-222 |
| Uniform Distribution | 9 | 224-225 | Statistics | 4 | 224-305 |
| Linear Algebra (Matrix) | 18 | 173-177 | Eigen Value | 26 | 165-170 |
| Determinant | 9 | 162-164 | Rank of Matrix | 7 | 179-180 |
| System of Equations | 14 | 182-185 | Vector Space | 4 | 186 |
| Calculus (Limits) | 11 | 145-146 | Differentiation | 8 | 140-142 |
| Integration | 10 | 143-144 | Maxima Minima | 11 | 147-286 |
| Aptitude (quantitative) | ~45 | 265-312 | Aptitude (verbal) | ~40 | 341-373 |
| Aptitude (reasoning) | ~40 | 237-363 | Data Interpretation | 2 | 276 |

*(Complete per-topic list was generated by the heading regex; the ~30 smallest/rare topics are folded into the rows above — the skill should re-scan if a topic is not listed.)*

## Full topic map — Volume 2 (PDF pages, heading-verified 2026-08-07)

| Topic | # Qs | PDF pages | Topic | # Qs | PDF pages |
|-------|-----:|-----------|-------|-----:|-----------|
| Asymptotic Notations | 20 | 27-31 | Time Complexity | 30 | 104-249 |
| Recurrence Relation | 33 | 85-92 | Algorithm Design | 8 | 23-24 |
| Sorting | 18 | 99-102 | Quick Sort | 13 | 81-84 |
| Merge Sort | 4 | 70-71 | Heap Sort | 2 | 54 |
| Binary Search Tree | 32 | 33-214 | Binary Tree | 44 | 34-224 |
| AVL Tree | 5 | 197-198 | Binary Heap | 28 | 32-207 |
| Graph Search | 18 | 46-50 | Minimum Spanning Tree | 34 | 72-80 |
| Dijkstras Algorithm | 5 | 37-38 | Shortest Path | 6 | 97-98 |
| Dynamic Programming | 10 | 39-41 | Greedy Algorithms | 5 | 51-52 |
| Hashing | 17 | 53-230 | Linked List | 22 | 232-238 |
| Stack | 15 | 244-248 | Queue | 13 | 240-243 |
| Tree | 13 | 249-252 | Array | 22 | 198-278 |
| Finite Automata | 32 | 349-359 | Regular Language | 31 | 394-400 |
| Regular Expression | 24 | 387-392 | Context Free Language | 29 | 332-339 |
| Grammar | 44 | 133-144 | Parsing | 20 | 166-171 |
| LR Parser | 20 | 149-153 | Syntax Directed Translation | 19 | 180-185 |
| Turing Machine | 1 | 401 | Decidability | 30 | 342-348 |
| Programming In C | 24 | 298-306 | Parameter Passing | 23 | 161-292 |
| Recursion | 23 | 93-314 | Pointer | 15 | 293-298 |

*(Complete per-topic list was generated by the heading regex; the ~30 smallest/rare topics are folded into the rows above — the skill should re-scan if a topic is not listed.)*

## Rebuild / extend

- The topic maps above were generated from the question-heading regex `^\d+\.\d+\.\d+ <Topic>: GATE (?:CSE )?<year> \| Question: <n>$` scanned per PDF page. Re-run to refresh after a new edition is dropped in (regenerate `CompetitiveExam/Books/*/index.md` the same way `/index-textbook` regenerates its per-book index).
- To add a book: drop it in `CompetitiveExam/Books/<ShortName>/`, extract its own topic map, and add a row to the volumes table.

## Cross-references

- `.claude/skills/competitive-exam-questions/SKILL.md` — the skill that consumes this registry (Phase 0 availability check, Tier-1 sourcing).
- `master_supporting_docs/CS401/supporting_books/*/index.md` — the parallel per-course textbook indexes (syllabus content sources).
- `quality_reports/plans/2026-08-07_competitive-exam-sourcing.md` — the design decision record behind this registry.
