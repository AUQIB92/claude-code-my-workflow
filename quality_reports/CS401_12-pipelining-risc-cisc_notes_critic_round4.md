# Notes vs Beamer Parity Audit: CS401/12-pipelining-risc-cisc

**Beamer source:** `Slides/CS401/12-pipelining-risc-cisc.tex`  
**Notes:** `Notes/CS401/12-pipelining-risc-cisc-notes.tex`  
**Round:** 4  **Date:** 2026-09-05

## Verdict: APPROVED

This audit treats the Notes as a topic-reorganized article, as required by
`lecture-notes/SKILL.md`; exact frame-title matching is not a valid parity test
for this artifact.

## Hard Gate Status

| Gate | Status | Evidence |
|---|---|---|
| Content parity | Pass | Four Notes sections cover the course bridge/roadmap, pipeline model and both timing examples, RISC/CISC comparison and workload examples, and the complete course review/checklist. The six-instruction timing table, load-use table, RISC/CISC table, workload table, design-knob table, and ISA-boundary table are present. |
| No invention | Pass | Expanded prose and arithmetic are traceable to the deck's stated assumptions, equations, examples, tables, and review claims. The only new exercise instance is explicitly permitted by the Notes detail-bar requirement and uses the deck's performance model. |
| Citation parity | Pass | Citation-key set is identical: `PattersonHennessy2017_computer_organization_design`. No Notes-only `\cite{}` keys. |
| Notation fidelity | Pass | `T_{CPU}`, `\mathrm{IC}`, `\mathrm{CPI}`, $f$, $T_c$, $k$, $n$, IF/ID/EX/MEM/WB, RAW, RISC/CISC, and all instruction/register notation are retained. |
| Textbook-page honesty | Pass | P&H pages trace to `PattersonHennessy2017/index.md`; Stallings section/PDF-page references trace to `Stallings2015/index.md`. No unsupported page number was introduced. |

## Coverage Map

- Course bridge, motivation, roadmap, and running operation: §12.1.
- Five-stage model, latency/throughput distinction, fill/drain arithmetic,
  load-use bubble, Socratic check, and design knobs: §12.2.
- RISC/CISC definitions, `A[i] = A[i] + 1` table, regularity and
  expressiveness trade-offs, Socratic correction, workload table, total-time
  comparison, and ISA-boundary table: §12.3.
- Performance thread, six diagnostic questions, integrator scenario, exam
  checklist, closing takeaway, references, four worked examples, and four
  complete exercise solutions: §12.4 and the end matter.

## Summary Statistics

| Metric | Value |
|---|---:|
| Explicit Beamer `frame` environments | 24 |
| Topic-organized Notes sections | 4 |
| Worked examples | 4 |
| Exercises with solutions | 4 |
| Citation keys: Beamer / Notes | 1 / 1 |
| Embedded TikZ figures | 0 / 0 |
| Critical / Major / Minor | 0 / 0 / 0 |

## Build Verification

XeLaTeX + BibTeX + two final XeLaTeX passes completed successfully. The final
PDF is 8 pages with zero LaTeX errors, zero undefined citations/references,
zero overfull boxes, and zero underfull boxes.