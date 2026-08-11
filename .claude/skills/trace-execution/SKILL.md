---
name: trace-execution
description: Generate a step-by-step execution trace as a sequence of TikZ diagrams — memory diagrams (stack/heap growth), call stacks, pointer/box-and-arrow mutations, or data-structure operations (BST insert, linked-list splice) — where each step is its own coordinate-consistent figure showing exactly what changed since the previous step. Use when user says "trace this execution", "show the stack step by step", "diagram this pointer mutation", "make a step-by-step trace for this algorithm", or when a lecture/notes file explains a mechanism in prose that would be clearer as a sequence of before/after pictures. Automates the pattern already hand-built for CS301 Week 1 (stack-growth Steps 1-3, heap-growth Steps 1-3). NOT for a single static diagram (use /new-diagram) and NOT for a Karnaugh map, FSM, or circuit (those are single-figure snippets in templates/tikz-snippets/, not step sequences).
argument-hint: "[CourseCode/lecture] [what to trace, e.g. 'stack growth for foo(); bar(); baz()' or 'BST insert of 15,8,20,4,12']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/trace-execution` — Step-by-Step Execution Trace Generator

Generate a sequence of TikZ diagrams tracing a mechanism through its steps — one figure per step, every step sharing the same coordinate layout so only the deliberate change is visible between consecutive figures. This is the general form of a pattern already hand-built once: CS301 Week 1's Notes carry a full stack-growth trace (Steps 1-3, Figs 1.2-1.4) and heap-growth trace (Steps 1-3, Figs 1.7-1.9), built by hand because nothing automated it. This skill automates that pattern for any step-wise mechanism: memory layout mutation, pointer rewiring, call-stack growth, or a data-structure operation (BST insert/delete, linked-list splice, stack push/pop).

## When to use

- A lecture or Notes chapter explains a multi-step mechanism in prose ("first the caller pushes the return address, then the callee allocates its frame, then...") that a reader has to hold in their head — a trace makes each state concrete.
- Building the board-drawable examples an `/instructor-handout` needs (see that skill's Board-Drawable Example standard) — a trace sequence is the source material for a live board-walk.
- Extending the CS301-style stack/heap trace pattern to a new lecture or a new example.

## Phase 0: Pre-Flight

1. Read the source lecture/Notes file (or accept a description of the mechanism directly via `$1` if no file exists yet).
2. Identify the **state** being traced (a memory region, a call stack, a data structure) and its **operations** (the sequence of pushes/pops/inserts/mutations that produce each step).
3. Decide the number of steps — usually 3-5; more than 6 steps in one sequence should be split into two labeled phases (e.g. "growth" and "return") rather than one long sequence, matching the CS301 precedent's Steps 1-3 / Steps 1-3 split between stack-growth and heap-growth.
4. Pick the base TikZ snippet to derive from: `cs-memory-stack-heap.tex` for stack/heap traces, `cs-linked-list.tex` for pointer/list mutation traces, `cs-binary-tree.tex` for tree-operation traces — or a from-scratch layout if none fits, still satisfying `tikz-prevention.md` P1-P7.

## Phase 1: Fix the coordinate layout ONCE, before drawing any step

**This is the load-bearing discipline (`tikz-measurement.md` Pass 0 — cross-slide consistency, generalized to cross-step consistency):** every node that persists across steps must sit at the *identical* coordinate in every step's figure. Write the coordinate map once, in a comment block, and reuse it verbatim in every step's `tikzpicture` — do not recompute layout per step. If step 3 needs a new node that steps 1-2 didn't have, add it at a coordinate that doesn't disturb any existing node's position.

```latex
% Coordinate map (fixed across all N steps in this trace — do not vary):
%   Stack region: y in [1.5, 3.2]; frame N+1 stacks directly above frame N
%   Frame box: minimum width 3.0cm, minimum height 0.9cm
%   New nodes this step, if any: [name] at [(x,y)] -- added in Step [k]
```

## Phase 2: Draw each step

For each step $k = 1, \dots, N$:

1. Copy the fixed layout from Phase 1.
2. Render the state *as of the end of step $k$* — every node/edge that exists at this point, using the identical style (`draw`, `fill`, `minimum width/height`) it had in the previous step where it persists.
3. **Highlight only what changed this step** — the new/mutated node or edge in `positive` (added) or `negative` (removed) from the course palette (`Preambles/header.tex`); everything unchanged stays in its normal color. This is what makes a sequence readable at a glance — a reader should be able to tell what happened between step $k{-}1$ and step $k$ without re-reading every node.
4. A one-line caption under each figure stating the operation that produced this state (e.g. "Step 2: `malloc(sizeof(int))` returns a block; `p` now holds its address").
5. Run every step's diagram through the same P1-P7 checks any TikZ authoring does (`tikz-prevention.md`) — a trace sequence with $N$ steps is $N$ diagrams, and a collision in step 3 is exactly as real a bug as a collision in a one-off diagram.

## Phase 3: Full-sequence consistency pass

After all $N$ steps are drawn, re-check **across** them, not just within each:

- Every persisting node is at the exact same coordinate in every step it appears (grep the coordinate values across the file — they should be identical strings, not just visually close).
- Colors are used consistently for the same semantic meaning across steps (a node highlighted `positive` for "just added" in step 2 should not still be `positive` in step 3 once it's no longer the newest change).
- The step count matches what Phase 0 decided; no step was silently dropped or merged.

## Phase 4: Write the file

`Figures/<CODE>/<lecture>/<mechanism-name>-trace.tex` — one file containing all $N$ `tikzpicture` environments in sequence (each wrapped for standalone compile-testing, matching the `templates/tikz-snippets/` convention), plus the shared coordinate-map comment once at the top. If the trace is being embedded directly into a Beamer deck or Notes chapter, copy each `tikzpicture` block individually to its destination frame/figure, following `single-source-of-truth.md`'s TikZ-in-Beamer convention.

## Phase 5: QA

Compile every step standalone; visually confirm (render to PNG, actually look at it — a clean compile does not guarantee no overlap, per this project's own recent history) that no step has a label/arrow collision and that the highlighted change is visually obvious.

## Report

State: mechanism traced, step count, base snippet/layout used, and the file path written. Flag any step where the "only what changed" highlighting discipline required a judgment call (e.g. a multi-part change in one step).

## Cross-references

- [`templates/tikz-snippets/cs-memory-stack-heap.tex`](../../../templates/tikz-snippets/cs-memory-stack-heap.tex), [`cs-linked-list.tex`](../../../templates/tikz-snippets/cs-linked-list.tex), [`cs-binary-tree.tex`](../../../templates/tikz-snippets/cs-binary-tree.tex) — the base layouts this skill derives step sequences from.
- [`.claude/rules/tikz-measurement.md`](../../rules/tikz-measurement.md) Pass 0 — the cross-slide (generalized here to cross-step) consistency rule this skill's Phase 1/3 discipline is built on.
- [`.claude/rules/tikz-prevention.md`](../../rules/tikz-prevention.md) — P1-P7, applied to every individual step's diagram.
- [`.claude/skills/new-diagram/SKILL.md`](../new-diagram/SKILL.md) — for a single static diagram instead of a step sequence.
- [`.claude/skills/instructor-handout/SKILL.md`](../instructor-handout/SKILL.md) — the Board-Drawable Example standard this skill's output feeds directly.
