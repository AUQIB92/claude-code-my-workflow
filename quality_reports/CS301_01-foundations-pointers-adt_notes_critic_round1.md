# Notes vs Beamer Parity Audit: CS301/01-foundations-pointers-adt

**Beamer source:** `Slides/CS301/01-foundations-pointers-adt.tex` (53 `\begin{frame}`-equivalent blocks: titlepage + 5 `\sectiondivider`s + 5 `\transitionslide`s + references frame + ~34 substantive content frames)
**Notes:** `Notes/CS301/01-foundations-pointers-adt-notes.tex`
**Round:** 1  **Date:** 2026-08-13

## Verdict: REJECTED

Two hard gates fail: **No invention** and **Notation fidelity**. Both failures are independent of the otherwise-solid Detail Bar treatment given to the two new content areas (Structured Programming, calloc/realloc), which was confirmed to meet the expansion bar.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | Every Beamer frame's core idea traces to a Notes section. |
| No invention | **FAIL** | C1 (fabricated motivation narrative), C2 (fabricated `int a[1000000]` example), C3 (fabricated "Disjoint Sets" list item attributed to a real citation, ×2 occurrences). |
| Citation parity | Pass | All 5 Beamer `\cite{}` keys appear as real `\cite{}` commands in the Notes. No extra keys invented. |
| Notation fidelity | **FAIL** | C4: "The Safe Empty Pointer" section renames the Beamer's `struct node *p = NULL;` example to `struct node *head = NULL;` and changes its stated meaning, contradicting the deck's own explicit Week-1 naming clarification in the immediately preceding frame. |
| Textbook-page honesty | Pass (one flagged borderline, Minor) | No page number attributed to HorowitzSahni2008 or AhoHopcroftUllman1983 anywhere. Sedgewick2011 p.64/p.120 and Karumanchi2017 p.18 match verified anchors. Wirth2004 p.111 matches verified anchor; p.109 additionally cited (Minor). |

## Critical Issues (MUST FIX)

### C1: Fabricated motivation narrative replaces the Beamer's actual example
- **Beamer frame:** "Motivation: Correct Is Not Always Fast Enough" (lines 47-61). Content: a loop that scans student records one by one, instant with 5 records, far too slow with 10 million records; arrangement of data is the difference.
- **Notes:** Section 1.1 replaces this with an invented scenario: college roll-number lookup, "about ten lines of C," "a thousand students," "ten million records and a new query arriving every millisecond," plus invented forward-looking numeric claims ("roughly twenty-four comparisons," "roughly one") for Weeks 8/10.
- **Fix:** Rewrite to expand only the Beamer frame's actual example (5 records instant / 10 million too slow), without inventing a new scenario or numeric forward-projections.

### C2: Fabricated `int a[1000000];` example and "guessing a maximum" argument
- **Beamer frame:** "Why Do We Need the Heap?" (lines 309-323) — no mention of guessing a maximum array size.
- **Notes:** Section 1.3 inserts "Guessing a maximum does not rescue us. Declaring `int a[1000000];` wastes memory..." — not in the Beamer source.
- **Fix:** Remove the invented paragraph.

### C3: Fabricated "Disjoint Sets" addition to a directly-cited enumeration (2 occurrences)
- **Beamer frame:** "This Course Is a Tour of ADTs" (lines 730-738). Exact list: "Linked Lists, Stacks, Queues, Priority Queues, Binary Trees, Hash Tables, and Graphs" — 7 items, no "Disjoint Sets."
- **Notes:** Both in "This course is a tour of ADTs" subsection and again in the closing Summary, "Disjoint Sets" is inserted into the list, attributed to the same Karumanchi2017 p.18 citation the Beamer uses for the 7-item list.
- **Fix:** Remove "Disjoint Sets" from both occurrences; restore the exact 7-item list.

### C4: NULL-pointer worked example's variable and meaning altered
- **Beamer frames:** "A Pointer Can Reach a Node" explicitly states the list handle will be called `head` starting Week 6; "here the node is just `p`." The next frame, "The Safe Empty Pointer," follows this: `struct node *p = NULL;` means "this pointer reaches nothing yet."
- **Notes:** "The safe empty pointer" subsection drops the Week-1 p-vs-head clarification, then renames the example: `struct node *head = NULL;` says "the list is empty" — both variable name and semantic gloss changed.
- **Fix:** Restore the Beamer's actual example variable (`p`) and its actual stated meaning ("this pointer reaches nothing yet"); restore the dropped p-now/head-later clarification.

## Major Issues (SHOULD FIX)

### M1: Diagram narration invents a label absent from the diagram
- **Beamer frame:** "One Contract, Two Possible Implementations" — TikZ draws plain, unlabeled arrows (`\draw[->, thick] (adt) -- (array);` etc.).
- **Notes:** Figure `fig:adt` caption/prose states the arrows are "labelled 'implements.'" No such label exists in the embedded TikZ.
- **Fix:** Remove "labelled 'implements'" claim; describe arrows as plain/unlabeled.

### M2: Invented C statements inserted into the heap-growth worked examples (3 instances)
- **Beamer frames:** "How the Heap Grows — Step 1/2/3" — TikZ diagrams show values in labeled boxes; no assignment-statement code appears.
- **Notes:** Inserts invented code (`p[0] = 10; p[1] = 20; p[2] = 30;`, `q[0] = 40; q[1] = 50;`) not present in Beamer.
- **Fix:** Remove the invented assignment-statement lines; keep only the values as narrated prose matching the diagrams (the existing `free(p); p = NULL;` snippet in Step 3 is fine, it is taken verbatim from the Beamer's "Returning the Memory" frame content already used elsewhere).

## Minor Issues (NICE TO FIX)

- Roadmap framing drift: "The course answers two questions over twelve weeks" is unsourced framing not in the Beamer roadmap frame.
- "(The equivalent `(*p).data` is correct C but noisier...)" aside is grounded in the Notation Registry, not the Beamer frame itself.
- "not a hand-counted `8` or `12`" — specific numbers not in the Beamer frame.
- "This is precisely why returning a pointer to a local variable is a bug" — reasonable derived corollary, but not explicitly stated in the Beamer source.
- "What We Cannot Yet Answer" section drops $T(n)$ and best/worst/average case from the Week-2 preview, which the Beamer's closing exampleblock names alongside $O/\Omega/\Theta$.
- Wirth p.109 citation in "The Memory of a Running Program" Read-alongside line exceeds the single page-verified anchor (p.111); should be phrased more cautiously.

## Positive Findings (worth preserving through revision)

- Structured Programming (new Act 1) got full Detail Bar treatment: the `larger(int a, int b)` worked example is traced pattern-by-pattern; "Why structure the program before structuring the data" expands all three Beamer bullets with real derivation.
- calloc/realloc (new content in One Heap Block) also got full Detail Bar treatment: both new worked examples are fully solved step-by-step, matching the deck's diagrams exactly.
- Karumanchi2017 is correctly never cited for structured programming or malloc/calloc/realloc/free content, matching the knowledge base's Step-0.5 finding — the one exception being the C3 "Disjoint Sets" list-insertion error.
- Section/figure/example numbering correctly follows the chapter-style convention.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 53 (title + 5 sectiondividers + 5 transitionslides + references + ~34 content frames) |
| Notes sections | 7 `\section`s (1.1-1.7), 19 `\subsection`s, 2 `\subsection*` (Exercises, Solutions) |
| Citation keys: Beamer / Notes | 5 / 5 (full parity) |
| Critical / Major / Minor | 4 / 2 / 6 |
