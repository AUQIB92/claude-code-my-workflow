# Notes vs Beamer Parity Audit: CS401/02-number-systems-arithmetic

**Beamer source:** `Slides/CS401/02-number-systems-arithmetic.tex` (32 content frames + title + references, across 8 sections/Acts)
**Notes:** `Notes/CS401/02-number-systems-arithmetic-notes.tex`
**Round:** 1
**Date:** 2026-08-10

> Note: a prior round-1 audit of this pair (dated 2026-08-08, APPROVED with 1 minor) is superseded by this report — the Beamer deck has grown from 25 to 32 content frames since then (new adder-coordinate fix, expanded division example commentary), and the Notes were not resynced.

## Verdict: REJECTED (hard gate failure)

Two hard gates fail: **Content parity** (Week-1 recap content still dropped; a division worked example that the Beamer explicitly delegates to the Notes is not delivered) and **Notation/diagram fidelity** (the ripple-carry-adder TikZ figure in the Notes is a stale, pre-fix, documented-buggy copy of the Beamer diagram, not the current source). Citation-key parity and textbook-page honesty both pass cleanly.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | **FAIL** | (1) Beamer frame "Where We Left Off (Week 1)" lists three bullets — architecture vs. organization, the performance equation, and Amdahl's Law (line 49-57). Notes §1 Introduction (line 52) only restates the performance equation; "architecture vs organization" and "Amdahl's Law" are absent from the entire Notes file (grep confirms zero hits for "Amdahl"). (2) Beamer's "Worked Example: 13÷3, Both Algorithms" frame (line 689) explicitly says *"Full per-cycle traces are in this week's Lecture Notes and Instructor Handout"* — but Notes' corresponding example (line 336-338) gives only the setup and final answer, exactly mirroring the Beamer slide's own summary, never delivering the promised per-cycle trace (contrast with the Booth's-algorithm example, which *does* get a full 5-row cycle table in both files). |
| No invention | Pass (with caveats, see Minor) | No new numeric examples, no fabricated claims of consequence; two minor additions noted below (Q₋₁ role description; two extra citation instances that reuse already-valid keys/pages) |
| Citation parity | Pass | Beamer uses 3 unique keys across 6 `\cite{}` instances (`PattersonHennessy2017_computer_organization_design`, `Hamacher2002_computer_organization`, `Mano1993_computer_system_architecture`); Notes uses the identical 3-key set across 7 `\cite{}` instances (7th and 8th are duplicate reuses in figure captions, no new keys) |
| Notation fidelity | **FAIL** | The ripple-carry-adder TikZ diagram in Notes (lines 178-201) reproduces coordinates that the Beamer source's own coordinate-map comment (lines 396-408) documents as the **pre-fix, buggy** version — labels at `2.6i-0.85` with arrows `2.6i-0.6 → 2.6i-0.7` (Beamer comment: "was ... which left ~0 clearance and rendered as label+arrowhead fused together"), and the carry-out annotation at `y=-0.8` (Beamer comment: "was y=-0.8 ... rendered as a strike-through 'carry-out'"). The current Beamer diagram fixed both to `2.6i-1.2`/`2.6i-0.9→2.6i-0.72` and `y=-1.3` respectively. Every other symbol/equation in the Notes matches the Beamer verbatim. |
| Textbook-page honesty | Pass | All page numbers appearing in Notes (p.188, p.191, p.197 for P&H; p.380, p.390-392 for Hamacher) are identical to page numbers already present in the corresponding Beamer frames — none are new. Cross-checked against `master_supporting_docs/CS401/supporting_books/Hamacher2002/index.md`. |

## Critical Issues (MUST FIX)

### C1: Ripple-carry-adder diagram is a stale, documented-buggy copy, not the current Beamer source
- Beamer frame "Ripple-Carry Adder: Chaining the Full Adders" (lines 392-433) documents a bug-fix history (labels moved from `2.6i-0.85`/arrows `2.6i-0.6→2.6i-0.7` to `2.6i-1.2`/`2.6i-0.9→2.6i-0.72`; carry-out annotation from `y=-0.8` to `y=-1.3`).
- Notes (lines 178-201) reproduces the OLD buggy coordinates.
- Fix: Replace Notes' TikZ block with a verbatim copy of current Beamer TikZ code (lines 409-429).

### C2: Promised full per-cycle division trace never delivered in Notes
- Beamer "Worked Example: 13 ÷ 3, Both Algorithms" (lines 678-691) explicitly defers full per-cycle traces to the Notes.
- Notes (lines 336-338) only reproduces the slide's summary, no trace.
- Fix: Add 4-cycle trace tables for both restoring and non-restoring division, Q=1101, M=0011, mirroring the Booth's-algorithm example's level of detail (cf. Hamacher2002 index.md Fig 6.22/6.23).

## Major Issues (SHOULD FIX)

### M1: Week-1 recap content (architecture/organization distinction, Amdahl's Law) dropped from Introduction
- Beamer "Where We Left Off (Week 1)" (lines 49-65) lists architecture-vs-organization and Amdahl's Law; Notes §1 (line 52) omits both.
- Fix: Extend opening paragraph of §1 Introduction to recap all three Week-1 pillars.

## Minor Issues (NICE TO FIX)

- m1: Two citations added to figure captions where Beamer frame carries none (harmless, same key/page).
- m2: Full-adder I/O block diagram dropped in Notes (equations-only).
- m3: Q₋₁ role description expanded slightly beyond Beamer wording (factually consistent).
- m4: Booth recoding pair notation reformatted from bare digits to ordered pairs.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames (content, excl. title/references) | 32 |
| Citation keys: Beamer / Notes | 3 / 3 (identical) |
| Critical / Major / Minor | 2 / 1 / 4 |
