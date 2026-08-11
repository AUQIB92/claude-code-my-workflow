# Pedagogy Report — CS301 Week 1: Pointers, Dynamic Memory, and Simple Contracts

**File:** `Slides/CS301/01-foundations-pointers-adt.tex`
**Audience:** B.Tech CSE, semester 3 (undergrad, core-lite difficulty)
**Date:** 2026-08-11
**Mode:** Review + applied fixes (weaknesses fulfilled at user request)

---

## Verdict

**Patterns followed: 12 / 13** after fixes. One pattern (worked-example proximity) was
partially violated pre-review and is now satisfied by reordering. Deck is
pedagogically sound: strong story arc, consistent memory-diagram orientation, good
retrieval checkpoints, and clean engineering framing for a 3rd-semester class.

---

## 13-Pattern Check

| # | Pattern | Status | Notes |
|---|---------|--------|-------|
| 1 | Clear learning objectives stated up front | ✅ | "Today's Three Questions" + Plan box |
| 2 | Motivation before formalism (INV-8) | ✅ | Heap motivated ("Why Do We Need the Heap?") before any heap API detail; address = house-number analogy before pointer definition |
| 3 | Worked example near every definition | ✅ | Fixed: heap-growth demos now sit immediately after the `malloc` pattern is taught; pointer def → pointer picture; NULL → example; ADT → bag example |
| 4 | One new symbol at a time | ✅ | Fixed: `p[0]=...` indexing removed from heap slides (now data cells); single `sizeof(TYPE)` idiom used throughout |
| 5 | Prerequisites checked, no unmotivated jumps | ✅ | Assumes functions/structs/arrays from sem-1/2 C; no forward-references the learner cannot yet read |
| 6 | Narrative arc (open → body → bridge) | ✅ | Questions → stack/heap → pointers → one heap block → ADT → Week-2 bridge |
| 7 | Deck-level pacing | ✅ | Long but broken into 6 short visual steps (3 stack + 3 heap); each growth slide carries one message |
| 8 | Progressive disclosure, no overlays (INV-6) | ✅ | No `\pause`/`\only`/`\visible`/`\onslide`; multi-slide builds instead |
| 9 | Colored-box discipline (INV-7) | ✅ | No frame exceeds 2 colored boxes |
| 10 | Anticipates student objections / misconceptions | ✅ | Leak vs dangling pointer, `NULL` deref, "pointer is not the object", failure-path audit checklist |
| 11 | Retrieval practice / checkpoints | ✅ | Check Your Prediction, Trace It Before Running It, Contract-or-Implementation?, Challenge boxes |
| 12 | Bridge to next lesson | ✅ | Summary → "next week: how much work an operation needs" |
| 13 | Notation consistency (KB registry) | ✅ | `\texttt{NULL}`, `head`, 0-based indexing, stack-down/heap-up orientation all match `knowledge-base-CS301.md` |

---

## Deck-Level Assessments

- **Narrative arc:** Strong. The opening "three questions" are answered in order:
  Q1 (where data lives) by Memory + Pointers, Q2 (run-time memory) by One Heap
  Block, Q3 (ADT contract) by Simple Contracts. Summary re-pairs each answer.
- **Visual rhythm:** Good. Alternates diagram-led slides (stack/heap growth,
  pointer picture, What Happened?) with code-led slides (malloc pattern, node
  allocation) and text-led slides (mistakes, checklist). No two dense-text slides
  in a row.
- **Memory-model consistency:** Fixed orientation throughout — high addresses at
  top, stack grows down, heap grows up; the growth arrows and the pointer-picture
  slides agree with the same mental model. This matches the KB rule and will be
  reused in Weeks 6/7/11.
- **Cognitive load:** Two idioms problem removed (`sizeof *p` vs `sizeof(int)`
  merged to `sizeof(TYPE)` everywhere). `->` arrow notation is now explicitly
  defined at first use.
- **Student perspective:** The deck correctly treats "heap block survives the
  allocating function" as the pivotal insight and returns to it three times
  (heap-growth Step 1, Check Your Prediction, Returning the Memory).

---

## Weaknesses Found and Fixed

1. **Heap-growth slides used `malloc`/`sizeof`/`free` before those were taught**
   (violation of patterns 3 and 4; INV-8 risk).
   → Moved all three "How the Heap Grows" slides from the Memory section into the
   "One Heap Block" section, placed immediately after "What Happened?" (where the
   `malloc(sizeof(int))` pattern is established) and before "Returning the
   Memory" (which formalizes `free`).
2. **Premature array-index notation** in the heap diagrams (`p[0]=10 p[1]=20 p[2]=30`).
   → Replaced with plain data-cell rows (`10  20  30`, `40  50`) and reworded the
   bullets so the visuals show *values in blocks* rather than new indexing syntax.
3. **Two conflicting allocation idioms** (`sizeof(int)` vs `sizeof *p`).
   → Unified on `sizeof(TYPE)`: node allocation now reads
   `malloc(sizeof(struct node))`, consistent with every other allocation in the deck.
4. **`->` dereference used before being explained** ("Allocate a Complete Node").
   → Added a one-line definition: "`p->data` means: the `data` field of the node
   `p` points at."
5. **Undeclared preview** — "Check Your Prediction" showed `malloc(sizeof(int))`
   with no signal that the exact call comes later.
   → Added a muted note: "The exact call for this — `malloc` and `sizeof` — comes
   in a few slides."

---

## Critical Recommendations (remaining, optional)

1. **Add two `\transitionslide` breaks** at the Pointers and Simple Contracts
   section starts to give the 30-page deck more breathing room (visual/pacing
   choice; flagged here for pedagogy, best applied alongside `/visual-audit`).
2. **Preview the running expression-processor** (Week 0's anchor) on one slide,
   e.g., the `struct node` slide, so Week 1 visibly feeds the course thread.
3. **Consider a "why stack and heap grow toward each other" one-liner** on the
   Step-3 slides — answers the common "why are they opposite?" question without
   adding a slide.

---

## Verification

- Recompiled: `xelatex` + `bibtex` + two further `xelatex` passes — clean, 30 pages,
  no unresolved references, no `Overfull`/`LaTeX Warning` lines.
- Quality gate: `quality_score.py` = 100/100 (EXCELLENCE).
- Invariants re-checked: INV-6 (no overlays), INV-7 (≤2 boxes/slide), INV-8
  (motivation first) all hold.
