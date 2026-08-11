# TikZ Snippet Gallery

Copy-paste starting points for common academic diagrams. Every snippet:

- Compiles standalone via `\documentclass{standalone}` — verify quickly with `xelatex snippet.tex`.
- Satisfies [`tikz-prevention.md`](../../.claude/rules/tikz-prevention.md): explicit node dimensions (P1), coordinate map comment (P2), no `scale=` (P3), directional keyword on every edge label (P4).
- Uses color names from [`Preambles/header.tex`](../../Preambles/header.tex) once TX2 ships. Until then, snippets embed their palette inline.

## Inventory

**Econ / social-science.**

| Snippet | Purpose |
| --- | --- |
| [`dag-basic.tex`](dag-basic.tex) | Three-node causal DAG: X → Y with confounder U. |
| [`dag-mediation.tex`](dag-mediation.tex) | X → M → Y with direct path. |
| [`did-two-period.tex`](did-two-period.tex) | Two-period DiD with treatment/control paths and counterfactual. |
| [`event-study.tex`](event-study.tex) | Event-time coefficients with 95% CIs and reference line at t = 0. |
| [`timeline.tex`](timeline.tex) | Horizontal time axis with annotated events. |
| [`regression-scatter.tex`](regression-scatter.tex) | Scatter with OLS fit line and confidence band. |
| [`flowchart-3step.tex`](flowchart-3step.tex) | Vertical process flow with a decision diamond. |
| [`supply-demand.tex`](supply-demand.tex) | Supply and demand with shifted demand. |

**CS.**

| Snippet | Purpose |
| --- | --- |
| [`cs-fsm-automaton.tex`](cs-fsm-automaton.tex) | 3-state DFA over {0,1} with start/accept states — theory of computation, compilers, sequential-circuit state machines. |
| [`cs-logic-circuit.tex`](cs-logic-circuit.tex) | Half-adder gate diagram (XOR/AND) with fan-out — digital logic, computer organization ALU/adder content. |
| [`cs-karnaugh-map.tex`](cs-karnaugh-map.tex) | 4-variable K-map in Gray-code order with a circled implicant — Boolean minimization, control-signal simplification. |
| [`cs-binary-tree.tex`](cs-binary-tree.tex) | 7-node BST with a highlighted search path and level annotations — data structures, algorithms. |
| [`cs-linked-list.tex`](cs-linked-list.tex) | Singly linked list, data/next cells, NULL terminator — pointers, dynamic memory. |
| [`cs-memory-stack-heap.tex`](cs-memory-stack-heap.tex) | Process address space (text/data/heap/stack) with a heap pointer — OS, systems programming, malloc/pointer tracing. |
| [`cs-pipeline-timing.tex`](cs-pipeline-timing.tex) | 5-stage instruction pipeline over 9 cycles with a marked hazard stall — computer architecture, CPI/throughput. |

**Math.**

| Snippet | Purpose |
| --- | --- |
| [`math-function-plot.tex`](math-function-plot.tex) | Annotated Cartesian plot (roots, vertex, axes extending past the data) — calculus, precalculus, numerical methods. |
| [`math-venn-two-set.tex`](math-venn-two-set.tex) | Two-set Venn diagram with all four regions labelled at their centroids — discrete math, probability, logic. |

## Usage

**Via the `/new-diagram` skill** (once TX3 lands):

```text
/new-diagram dag-basic Figures/Lecture02/identification.tex
```

**Manually:**

```bash
cp templates/tikz-snippets/dag-basic.tex Figures/Lecture02/identification.tex
# edit node labels, coordinates; keep the coordinate map up to date
xelatex -interaction=nonstopmode Figures/Lecture02/identification.tex  # standalone compile
```

Embed in Beamer by copying the contents of `\begin{tikzpicture} ... \end{tikzpicture}` into a `frame`. The `standalone` wrapper exists only so you can compile the snippet on its own while editing.

## Adapting a snippet

1. **Keep the coordinate-map comment in sync.** If you rename a node or move coordinates, update the comment block immediately. Stale comment blocks are worse than no comment blocks.
2. **Stay explicit on node sizes.** `minimum width`, `minimum height`, and `text width` are load-bearing — removing them is a violation of prevention rule P1.
3. **Do not add `scale=X`.** If the diagram is too large for its slot, redesign at the intended size. Scaling breaks every label-position calculation (prevention rule P3).
4. **When in doubt, run the six-pass check.** See [`tikz-measurement.md`](../../.claude/rules/tikz-measurement.md) for formulas. The `/extract-tikz` and `/new-diagram` skills run the checks for you.

## Contributing

Adding a new snippet? The bar:

- Generalizes across fields. A new DAG snippet is domain-neutral; a snippet that only makes sense in a single subfield should live in that project's fork, not here.
- Compiles standalone with `xelatex` (the snippets ship as `\documentclass[border=4pt]{standalone}`).
- Passes the P3 and P4 grep pre-checks in [`tikz-prevention.md`](../../.claude/rules/tikz-prevention.md) by construction.
- Has a coordinate-map comment showing every named coordinate and a one-line intent sentence.
- Renders cleanly at Beamer's default frame size (12.8 × 9.6 cm for 4:3, 16 × 9 cm for widescreen) when copied into a `frame`.

Open a PR using the standard workflow (see `.github/CONTRIBUTING.md`).
