# Notes vs Beamer Parity Audit — CS301/01-foundations-pointers-adt (Round 1)

**Beamer source:** `Slides/CS301/01-foundations-pointers-adt.tex`
**Notes:** `Notes/CS301/01-foundations-pointers-adt-notes.tex`
**Date:** 2026-08-11
**Verdict:** REJECTED — 2 Critical, 3 Major, 2 Minor

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | **Fail** | Roadmap frame's "one artifact, all term" expression-processor example (Beamer 72–77) absent from Notes; Notes line 366 references "our expression processor" with no antecedent. |
| No invention | **Fail** | Two figure captions attach citations the Beamer never makes for those diagrams (C1, C2); Notes 230–231 adds a "Weeks 6, 7, 11" forward-reference with no Beamer source (M2). |
| Citation parity | **Fail** | Key-set diff clean (2/2, keys match exactly), but Notes attaches each key to a *new* figure-caption claim. |
| Notation fidelity | Pass | All symbols, identifiers, and both code listings verbatim. 0-based indexing preserved. |
| Textbook-page honesty | Pass | No page number anywhere; chapter-level attribution only, consistent with no index built for either anchor text. |

## Critical

### C1 — Invented citation on the memory-layout figure caption
- **Notes:** 134–138 (`fig:memlayout` caption) — `Cf.\ Horowitz \& Sahni, Ch.~1 (general treatment) \cite{HorowitzSahni2008_...}`
- **Beamer:** frame "The Memory of a Running Program" (144–182) contains **no `\cite{}`**. The key is legitimate at Beamer line 119, attached to a *different* claim.
- **Fix:** delete the `Cf.\ ...` clause from the caption. To keep it, add it to the Beamer frame first, then propagate down.

### C2 — Invented citation on the ADT figure caption
- **Notes:** 356–359 (`fig:adt` caption) — `Cf.\ Aho, Hopcroft \& Ullman, Ch.~1 (general treatment) \cite{AhoHopcroftUllman1983_...}`
- **Beamer:** frame "One Contract, Many Structures" (393–425) contains **no `\cite{}`**. Key is legitimate at Beamer line 389.
- **Fix:** delete the `Cf.\ ...` clause from the caption.

## Major

### M1 — Course running example dropped, leaving a dangling reference
- **Beamer:** 59–78, `\alertblock{One artifact, all term}` — the `(a+b)*c` expression processor, plus the five-part twelve-week roadmap.
- **Notes:** entirely absent. Only trace is line 366 ("our expression processor"), used as if previously introduced.
- **Fix:** introduce the expression-processor artifact (and fold in the roadmap's week breakdown) in Section 1.1, restoring the antecedent.

### M2 — Invented forward-reference in node-lifetime narration
- **Notes:** 230–231 — "the diagram this course returns to in Weeks 6, 7, and 11."
- **Beamer:** frame "The Lifetime of One Node" (281–314) makes no such claim. The week list traces to `knowledge-base-CS301.md`, which is not the Beamer deck and is not a licensed source for Notes content under SSOT.
- **Fix:** delete the clause.

### M3 — Memory-layout narration is a "see figure" restatement, not an expansion
- **Notes:** 96–97 — names none of the five regions in prose. Code (text) and Static/globals are never described anywhere in the file.
- **Beamer:** 144–182 labels all five regions inside the TikZ diagram.
- **Fix:** name and briefly characterize each of the five regions in prose around the figure.

## Minor

### m1 — Straight ASCII quotes
- **Notes:** 90–91 — `"it felt fast,"` should be ` ``it felt fast,'' ` (cf. correct usage at lines 269, 376).

### m2 — Hardcoded section cross-reference
- **Notes:** 285 — literal "Section~1.2". Currently correct but drift-prone.
- **Fix:** `\label{sec:memory}` on the Section 2 heading; `Section~\ref{sec:memory}` at the call site.

## Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 22 content + titlepage + references + 4 transitionslides |
| Notes sections | 6 numbered (1.1–1.6) + subsections + 2 `example` environments |
| Citation keys Beamer / Notes | 2 / 2 (same key-set) |
| Critical / Major / Minor | 2 / 3 / 2 |
