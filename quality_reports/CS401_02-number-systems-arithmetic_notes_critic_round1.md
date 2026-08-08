# Notes vs Beamer Parity Audit: CS401/02-number-systems-arithmetic

**Beamer source:** `Slides/CS401/02-number-systems-arithmetic.tex` (25 content frames + title frame + 5 transition slides)
**Notes:** `Notes/CS401/02-number-systems-arithmetic-notes.tex`
**Round:** 1  **Date:** 2026-08-08

## Verdict: APPROVED

The Notes preserve every substantive frame of the deck — all 5 acts (number systems, signed representation, overflow/fixed-point, adder hardware, synthesis) — with identical worked examples, equations, truth table, ripple-carry diagram, and the same three citation keys at the same four sites. The only gap is that the Notes' introduction omits two of the three Week-1 recap bullets (architecture-vs-organization and Amdahl's Law) from the deck's opening recap frame; this is recap context, not new content, and does not affect the lecture's core ideas. No inventions, no notation drift, and every page number traces to the textbook index.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 24 teaching frames' core ideas present in Notes §§1-6 (one recap-frame omission flagged as Minor, m1); transition slides' conceptual pivots reflected in narrative |
| No invention | Pass | Every claim/example/number in Notes traceable to a Beamer frame; no novel facts, examples, or citations found |
| Citation parity | Pass | Same 3 keys, same 4 cite sites on both sides (Beamer L184/L239/L275/L447 ↔ Notes L87/L103/L121/L206); no orphans; all keys resolve in `Bibliography_base.bib` |
| Notation fidelity | Pass | `-x \equiv 2^n - x`; range `-2^{n-1} \le x \le 2^{n-1}-1`; HA/FA equations; Q8.8; truth table rows; 4-bit `0111`/`1101` example — all identical |
| Textbook-page honesty | Pass | Notes body cites only p.188 (P&H Sec. 3.2), which appears in the Beamer frames; preamble comments p.191/p.197 match Beamer preamble and trace to index.md entries 3.3 (p.191) and 3.4 (p.197); Hamacher Ch. 2 / Mano Ch. 1 are chapter-level |

## Critical Issues (MUST FIX)

None.

## Major Issues (SHOULD FIX)

None.

## Minor Issues (NICE TO FIX)

### m1: Week-1 recap bullets partially dropped in the Notes introduction
- **Location:** `Notes/CS401/02-number-systems-arithmetic-notes.tex`, Section 1 "Introduction", line 49.
- **Text:** "Week 1 established the performance equation, $\text{CPU time} = \text{IC} \times \text{CPI} / f$, and with it the assumption that we can count instructions and measure CPI."
- **What's wrong:** Beamer frame 1 ("Where We Left Off", Slides L45-61) recaps three Week-1 points: architecture-vs-organization, the performance equation, and Amdahl's Law. The Notes keep the performance equation and the pivot, but the architecture/organization distinction and Amdahl's Law never appear anywhere in the Notes.
- **Fix:** Optionally add one sentence to the introduction, e.g. "Week 1 also separated architecture (the interface) from organization (the implementation) and introduced Amdahl's Law — the unimproved fraction sets a hard ceiling." This is recap context, so it is a nice-to-have rather than a parity violation of the lecture's core content.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames (content, excl. titlepage) | 25 (incl. References frame) |
| Beamer transition slides | 5 |
| Notes top-level sections | 6 |
| Citation keys: Beamer / Notes | 3 (PattersonHennessy2017, Hamacher2002, Mano1993) / 3 (identical); 4 cite sites each |
| Critical / Major / Minor | 0 / 0 / 1 |

**Files reviewed:**
- `Slides/CS401/02-number-systems-arithmetic.tex`
- `Notes/CS401/02-number-systems-arithmetic-notes.tex`
- `Bibliography_base.bib` (all 3 keys present)
- `master_supporting_docs/CS401/supporting_books/PattersonHennessy2017/index.md` (p.188/191/197 confirmed)
- `master_supporting_docs/CS401/supporting_books/Mano1993/index.md` (chapter-level only, not needed)
