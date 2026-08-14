# Notes vs Beamer Parity Audit: CS301/01-foundations-pointers-adt

**Beamer source:** `Slides/CS301/01-foundations-pointers-adt.tex` (48 frames incl. title/refs)
**Notes:** `Notes/CS301/01-foundations-pointers-adt-notes.tex`
**Round:** 3  **Date:** 2026-08-13

## Verdict: APPROVED

0 Critical, 0 Major, 2 Minor. Independent frame-by-frame re-audit (not a diff against round 2) confirms M3 and M4 are genuinely fixed and finds no new Critical/Major issues.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 48 frames traced to a Notes section/subsection; Week 1 Summary frame's 5 bullets + "next week" hook both covered (Notes §Summary + §What We Cannot Yet Answer). |
| No invention | Pass | See Minor-2 below for the one borderline case (forward curriculum detail sourced from the course KB, not fabricated). |
| Citation parity | Pass | `grep \cite{}` on both files: identical 5-key set (HorowitzSahni2008, AhoHopcroftUllman1983, Wirth2004, Sedgewick2011, Karumanchi2017), same combinations (e.g. Horowitz+Aho jointly cited in both at the motivation claim). |
| Notation fidelity | Pass | `$T(n)$`, `$O$`/`$\Omega$`/`$\Theta$` identical in both; `\texttt{}` code identifiers match; `NULL`/`->`/`head`/`p` convention preserved. |
| Textbook-page honesty | Pass | Wirth p.111, Sedgewick p.64/p.120, Karumanchi p.18(PDF) all cross-checked against `index.md` verified-anchor tables — every page number in Notes already appears in the corresponding Beamer frame (none invented during expansion). |

## M3 re-verification (stray `head` usage)
`grep -n head` on the full Notes file returns exactly 2 hits, both correct: line 412 ("the list handle will be called `head` starting Week 6; here the node is just `p`") and line 433 (the same rule restated). Exercise 2 and Solution 2 both use `p` throughout. No stray Week-1 use of `head` remains. **Confirmed fixed.**

## M4 re-verification (Sedgewick "three collection types" attribution)
The attribution now appears twice by design — once in the section's "Read alongside" line (798, the reading-guide convention used identically in every section of this file) and once inline in the `example` environment's opening sentence (824-826: "one of Sedgewick \& Wayne's three collection types (p.~120) \cite{Sedgewick2011_algorithms}"). This is the file's established house style (every section repeats its Read-alongside citation in body prose), not a confusing duplication. The sentence is grammatically correct. **Confirmed fixed, no residual issue.**

## Minor Issues (non-blocking)

### m1: Wirth quotation is a paraphrase presented with quotation marks
- Notes (line ~335-340) uses quote marks around "cannot be assigned a fixed amount of storage" / "cannot associate specific addresses with them," but the verified `Wirth2004/index.md` anchor (p.111) reads "it is impossible to assign a fixed amount of storage" / "cannot associate specific addresses **to their components**." Close paraphrase, not exact.
- Fix (optional): either drop the quotation marks (make it indirect prose) or match the index.md wording exactly.

### m2: Forward curriculum specifics not traceable to this Beamer frame
- Notes §"One contract, two possible implementations" (lines ~861-867) states "Weeks 3 and 7 both implement a stack, once over an array and once over a chain of nodes. Weeks 5 and 7 do the same for a queue." This detail is accurate and sourced from `knowledge-base-CS301.md`'s Design Principles table, but the Beamer deck's own roadmap frame only says Weeks 3-5 are "linear structures" and Weeks 6-7 are "linked structures" — it does not itself specify that stack/queue get reimplemented in Week 7. Low-risk (verifiably correct per the course KB, doesn't contradict anything), but strictly not traceable to this specific Beamer file.
- Fix (optional): soften to "a later week revisits this same contract over a linked implementation" or add the KB as an explicit forward-reference source.

## Positive Findings (re-examined, not counted as issues)
- The "more importantly" editorial connector, the `(*p).data` aside, "not a hand-counted `8` or `12`," and "returning a pointer to a local variable is a bug" (all flagged as minors in round 2) are, on independent re-reading, legitimate derivation/expansion — exactly what Notes exists to add — not invented facts or padding. Downgraded from "issue" to "expansion working as intended."
- All 12 TikZ diagrams (stack x3, heap x3, pointer, two-places, malloc/calloc, happened, adt) are narrated in prose immediately before/after their figure, drawn from each diagram's coordinate-map comment -- no "see figure" placeholders.
- Citation-instance count matches near-exactly (8 in Beamer, 8 in Notes), same key combinations.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 48 (incl. title + references) |
| Notes sections | 6 numbered sections + Exercises/Solutions/Summary |
| Citation keys: Beamer / Notes | 5 / 5 |
| Critical / Major / Minor | 0 / 0 / 2 |
