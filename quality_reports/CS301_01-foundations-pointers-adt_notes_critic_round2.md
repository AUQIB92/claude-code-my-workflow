# Notes vs Beamer Parity Audit — CS301/01-foundations-pointers-adt (Round 2)

**Date:** 2026-08-11
**Verdict:** REJECTED — 1 Critical, 1 Major, 1 Minor (6 of 7 round-1 fixes confirmed)

## Status of Round-1 Fixes

| Item | Status |
|------|--------|
| C1 — no Horowitz & Sahni cite on `fig:memlayout` caption | CONFIRMED FIXED |
| C2 — no Aho/Hopcroft/Ullman cite on `fig:adt` caption | CONFIRMED FIXED |
| M1 — roadmap + expression-processor paragraph in Section 1 | CONFIRMED FIXED (traces item-for-item to Beamer 59–78, no added facts) |
| M2 — "Weeks 6, 7, and 11" forward-reference removed | CONFIRMED FIXED |
| M3 — five memory regions named in prose | **PARTIAL** — regions named, but two unsourced properties introduced (see C-NEW1) |
| m1 — LaTeX quotes around "it felt fast" | CONFIRMED FIXED |
| m2 — `\label{sec:memory}` + `\ref` | CONFIRMED FIXED |

## Critical

### C-NEW1 — Invented properties in the Figure 1.1 lead-in
- **Notes:** 109–114 — "the code (text) region, holding the compiled instructions; static storage for globals, fixed at load time"
- **Beamer:** frame "The Memory of a Running Program" (144–182) contains only bare TikZ box labels ("Code (text)", "Static / globals") plus the orientation note. Neither "compiled instructions" nor "fixed at load time" appears anywhere in the deck.
- **Fix:** trim to region names and low-to-high ordering only.
- **Resolution:** FIXED — lead-in now reads "the code (text) region; static storage for globals; the heap; free space between the two; and the stack, with the heap growing up and the stack growing down toward each other."

## Major

### M-NEW1 — Dropped "catalogue of arrangements / judgement to choose" framing
- **Beamer:** 54–56 — "This course is a catalogue of those arrangements --- and, more importantly, the judgement to choose between them."
- **Notes:** absent from Section 1 entirely.
- **Fix:** restore the framing sentence in the opening paragraph.
- **Resolution:** FIXED — added at Notes line 55–56.

## Minor

### m-NEW1 — Vague "see figure" lead-ins for Figures 1.2 and 1.3
- Non-blocking; captions themselves carry adequate description. Not actioned.

## Gate Status

| Gate | Status |
|------|--------|
| Content parity | Pass (1 Major note) |
| No invention | **Fail** (C-NEW1) |
| Citation parity | Pass — 2/2 keys, attached to the same claims as Beamer |
| Notation fidelity | Pass |
| Textbook-page honesty | Pass |
