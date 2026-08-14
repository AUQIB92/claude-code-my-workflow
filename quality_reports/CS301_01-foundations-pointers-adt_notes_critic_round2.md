# Notes vs Beamer Parity Audit: CS301/01-foundations-pointers-adt

**Beamer source:** `Slides/CS301/01-foundations-pointers-adt.tex`
**Notes:** `Notes/CS301/01-foundations-pointers-adt-notes.tex`
**Round:** 2  **Date:** 2026-08-13

## Verdict: NEEDS REVISION

0 Critical, 2 Major, 5 Minor. All 4 Critical + 2 Major findings from round 1 confirmed genuinely fixed (not superficial) against the specific Beamer frames they cite.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | Every Beamer frame's core idea traces to a Notes section. |
| No invention | Pass | C1-C4 from round 1 confirmed fixed: motivation example restored verbatim, no `int a[1000000]`, "Disjoint Sets" removed (both occurrences), NULL-pointer example restored to `p` with the p-now/head-later clarification intact. |
| Citation parity | Pass | 5/5 `\cite{}` keys match, no extra keys. |
| Notation fidelity | **Major flag** | M3 below — Exercise 2/Solution 2 used `head` instead of `p` for the Week-1 pointer, contradicting the deck's explicit "here the node is just `p`; `head` starts Week 6" convention (now fixed). |
| Textbook-page honesty | Pass | Wirth p.111, Sedgewick p.64/p.120, Karumanchi p.18 all verified against `supporting_books/*/index.md`; section numbers cross-checked. |

## Major Issues (fixed this round)

### M3: Exercise 2 and Solution 2 used `head` instead of Week 1's actual variable `p`
- **Beamer frame:** "A Pointer Can Reach a Node" (lines ~396-398) explicitly states the list handle is called `head` starting Week 6; "here the node is just `p`." The Notes' own restated rule (Section on the safe empty pointer) preserves this.
- **Notes (pre-fix):** Exercise 2 ("If `head` lives on the stack...") and its Solution ("held `head`, the only pointer to the node") both used `head`, contradicting the Week-1 convention used everywhere else in the file.
- **Fix applied:** Both occurrences changed to `p`.

### M4: Dropped Sedgewick "three collection types" attribution on the bag example
- **Beamer frame:** "Worked Example: A Very Small Bag" muted line: "A bag is one of Sedgewick's three collection types (p.120) \cite{Sedgewick2011_algorithms}."
- **Notes (pre-fix):** The claim survived only as an unattached page reference in the section's "Read alongside" line; the worked-example prose itself dropped it.
- **Fix applied:** Restored the attribution inline in the `example` environment's opening sentence.

## Minor Issues (not fixed — reasonable derived expansions, same judgment as round 1)

- Slightly inexact paraphrase of the Wirth quotation vs. the verified index.md anchor wording.
- "more importantly" editorializing not present in the Beamer roadmap frame.
- `(*p).data` aside — grounded in the Notation Registry, not the Beamer frame itself.
- "not a hand-counted `8` or `12`" — specific numbers not in the Beamer frame.
- "This is precisely why returning a pointer to a local variable is a bug" — reasonable derived corollary, not explicitly stated in the Beamer source.

## Positive Findings

- All round-1 Critical (C1-C4) and Major (M1-M2) fixes verified genuine against the named Beamer frame line ranges, not just superficially patched.
- The two edited heap-growth `example` environments (Step 1, Step 2) read cleanly as prose after the invented-code removal — no dangling references, no orphaned formatting.
- The ADT-implementation diagram section reads correctly after removing the fabricated "labelled implements" claim.
- Citation parity remains full (5/5) after all edits.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Critical / Major / Minor | 0 / 2 (both fixed this round) / 5 (unfixed, non-blocking) |
