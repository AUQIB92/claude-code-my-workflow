---
paths:
  - "Slides/**/*.tex"
  - "Notes/**/*.tex"
  - "InstructorHandouts/**/*.tex"
  - "Figures/**/*.tex"
  - "Preambles/**/*.tex"
---

# TikZ Prevention Rules

**Write TikZ that can't collide in the first place.** Complements `tikz-visual-quality.md` (general standards) and `tikz-measurement.md` (repair-time formulas). Load whenever you are authoring or editing a `\begin{tikzpicture}` block.

> Adapted from Scott Cunningham's `tikz_rules.md` in [MixtapeTools](https://github.com/scunning1975/MixtapeTools). Used with attribution.

The LaTeX compiler does **not** warn on label-over-arrow overlaps, labels crossing shape boundaries, or arrows crossing arrows. Every one of these bugs must be caught at authoring time or in review. These rules shift the catch upstream.

---

## Rule P1: Explicit dimensions on **boxed** nodes (MANDATORY)

Every *boxed* text-bearing node — one drawn with `draw`, `fill`, a custom node style from the TikZ styles library (e.g. `dag-node`, `flow-node`, `decision-node`), or any shape style like `rectangle`, `diamond`, `circle` with `draw`/`fill` — must declare its size explicitly. Implicit sizing means the label can grow past the box edge without anyone noticing.

```latex
% BAD — node size grows silently with text length
\node[draw, rounded corners] (X) {Pre-trends assumption};

% GOOD — explicit box; text wraps or the author notices
\node[draw, rounded corners, minimum width=3.2cm, minimum height=1.0cm,
      text width=3.0cm, align=center] (X) {Pre-trends assumption};
```

Use either:

- `minimum width` + `minimum height` — for boxes whose size should not depend on the text.
- `text width` + `align=center` (or `left`) — for boxes whose height should grow with text.

`text width` is required for any multi-line content (anything containing `\\`).

### Scope — what P1 does **not** cover

Plain labels, axis ticks, axis titles, and free-floating annotations (`\node[above] {label}`, `\node[below, font=\footnotesize] at (\x, -0.1) {\x}`, etc.) are intentionally **not** subject to P1. Forcing dimensions on them would make every axis tick a syntax burden and conflict with the snippet gallery's own usage.

For those unboxed labels, correctness is enforced by P4 (directional keywords) and by the measurement rules (gap calculation, boundary clearance) in `tikz-measurement.md`.

---

## Rule P2: Coordinate map comment (MANDATORY for ≥3 nodes)

For any diagram with three or more nodes, precede `\begin{tikzpicture}` with a comment block that lists the named coordinates and a one-line intent sentence. This is the reader's legend; it also forces the author to think in absolute coordinates rather than relative drift.

```latex
% Diagram: Confounded DAG — X caused by U, Y caused by X and U.
% Coordinates: (x, y)
%   U at (3, 2)   -- confounder, top center
%   X at (0, 0)   -- treatment, lower left
%   Y at (6, 0)   -- outcome, lower right
\begin{tikzpicture}
  \node (U) at (3, 2) {U};
  ...
\end{tikzpicture}
```

---

## Rule P3: `scale=X` alone is banned — scale nodes with it

The real failure mode is **asymmetric scaling**: `scale=0.8` shrinks coordinates but *not* text. A 2 cm gap becomes 1.6 cm; the 1.2 cm label that fit before now overlaps. This silently produces the exact collisions the measurement rule exists to prevent.

**Ban.** `\begin{tikzpicture}[scale=X]` with no accompanying node scaling. This is the unsafe pattern.

**Allowed — the symmetric forms.** These scale coordinates *and* nodes together, so gap/label geometry survives:

```latex
% Full-width diagrams — recommended default in tikz-visual-quality.md
\begin{tikzpicture}[scale=1.1, every node/.style={scale=1.1}]

% Or use transform shape to scale node contents with coordinates
\begin{tikzpicture}[scale=0.85, transform shape]
```

When you stick to those forms, the `[scale=1.1]` convention from `tikz-visual-quality.md` is fine. When you write a bare `scale=` without node scaling, the prevention pre-check in `/extract-tikz` (Step 1) halts the pipeline.

---

## Rule P4: Directional keyword on every edge label

Every label attached to an edge must carry a positional keyword (`above`, `below`, `left`, `right`, or a compound). Bare `node {label}` places text *on* the arrow — reliably collides, silently compiles.

```latex
% BAD — label sits on the arrow line
\draw[->] (A) -- (B) node[midway] {confounded};

% GOOD — explicit direction
\draw[->] (A) -- (B) node[midway, above] {confounded};
```

| Arrow orientation | Preferred keyword |
|-------------------|-------------------|
| Horizontal | `above` or `below` |
| Vertical | `left` or `right` |
| Diagonal | side with more whitespace |
| Curved (`bend left/right`) | `above` on the outside of the bend |

For parallel arrows, stagger labels: use `pos=0.3` on one and `pos=0.7` on the other, or alternate `above`/`below`.

---

## Rule P5: Use the canonical snippets

`templates/tikz-snippets/` contains verified starting points for common academic diagrams (DAG, DiD plot, event study, timeline, flowchart, supply-demand, regression scatter, mediation). Each snippet embeds rules P1–P4 and includes a coordinate map.

Preferred workflow:

1. `/new-diagram <snippet-name>` — see the `/new-diagram` skill once TX3 ships; it scaffolds from the gallery.
2. Or copy the snippet manually: `cp templates/tikz-snippets/dag-basic.tex Figures/LectureN/my-dag.tex`.
3. Edit node labels and coordinates to fit your case. **Keep the coordinate map up to date.**
4. Only then invoke `/extract-tikz` or `/compile-latex`.

Writing a novel diagram from scratch is allowed but must still satisfy P1–P4 *and* the measurement rules in `tikz-measurement.md`.

---

## Rule P6: One tikzpicture per idea

A single `\begin{tikzpicture}` should encode one idea. If you need to show a sequence (stepwise reveal of a DAG, before/after comparison), use multiple tikzpictures — one per frame or subfigure — rather than one tikzpicture overloaded with conditionals or overlay layers.

This keeps each diagram small enough that the measurement rules are tractable.

---

## Rule P7: Geometric clearance — every edge must stay clear of every box and line (MANDATORY)

The coordinate map (P2) plus this clearance check is the only thing that stops the two most common real collisions: a bus/arrow passing *through* a box, and a label sitting *on* a line. Apply both checks to every diagram after drafting, before compiling:

**P7a — Every path must clear every box.** Compute each box's span from its `minimum width/height` and center; verify no `\draw` line crosses that rectangle except at a legitimate connection point (an edge anchor or a drawn perpendicular join). Watch for the classic failure: a horizontal "bus" drawn at a y that passes through the vertical span of a box above it.

```latex
% BAD — the bus at y=-0.4 passes THROUGH the CPU box (which spans y -0.8..0.8)
\node (CPU) at (0,0) [minimum width=2.6cm, minimum height=1.6cm] {...};
\draw (-1.3,-0.4) -- (4.3,-0.4);   % y=-0.4 is inside the CPU's y-span → overlap

% GOOD — the bus runs BELOW every box (y=-1.4 is below CPU bottom at -0.8),
% and each box connects to it with a short vertical drop at its own x.
\draw (-1.3,-1.4) -- (6.1,-1.4);
\draw (0,-0.8) -- (0,-1.4);        % CPU.south → bus
```

**P7b — No label may sit on a line.** An edge label must carry a directional keyword (P4) AND be offset so the text does not overlap the line it annotates. The most common miss is a label placed at the arrow's own y: `\node at (x, 0.35) {S}` next to `\draw (a,0.35)--(b,0.35)` puts the text on the line. Place such labels above/below the line, not at its midline, or shift the node off the line's y.

```latex
% BAD — S label sits exactly on the horizontal arrow at y=0.35
\node[font=\scriptsize] at (2.6*\i + 0.85, 0.35) {$S_\i$};
\draw[->] (2.6*\i + 0.7, 0.35) -- (2.6*\i + 1.1, 0.35);

% GOOD — label placed above the line, clear of it
\node[font=\scriptsize] at (2.6*\i + 0.9, 0.6) {$S_\i$};
\draw[->] (2.6*\i + 0.7, 0.35) -- (2.6*\i + 1.1, 0.35);
```

**P7c — Labels must clear box edges.** An unboxed label sitting within ~0.1 cm of a box edge visually collides. Leave at least 0.15 cm between a label's anchor point and the nearest box border.

**P7d — Curves/asymptotes must respect their own dashed reference lines.** When a curve is drawn next to a dashed threshold/asymptote (e.g. Amdahl's ceiling), the curve's maximum must *approach* that line from below — it must never visibly cross it. Tune the plot's scale factor so `max(curve) < dashed line y`, and place annotations below the flat region, not under the rising part.

```latex
% BAD — curve asymptote 4.0 but ceiling drawn at 2.0 → curve crosses the ceiling
\draw[dashed] (0,2.0) -- (6.6,2.0);
\draw plot (\x, {4.0*(1 - exp(-\x/1.2))});

% GOOD — ceiling is the curve's asymptote; curve approaches it from below
\draw[dashed] (0,3.5) -- (6.6,3.5);
\draw plot (\x, {3.5*(1 - exp(-\x/1.1))});
```

---

## Enforcement

- `/extract-tikz` runs a prevention pre-check as **Step 1** before compiling. Violations of P1 (boxed nodes only), P3 (bare `scale=`), or P4 (missing directional keyword on edge labels) halt the pipeline and report the offending block. P2 (coordinate map) and P5–P6 are reviewer concerns, not grep-checkable.
- **P7 is a hard authoring gate, not a reviewer concern.** Every `tikzpicture` with ≥ 2 nodes or ≥ 1 line must carry a P2 coordinate map, and that map must be audited for P7a–P7d (box clearance, label-off-line, edge clearance, curve-vs-dashed-asymptote) before the file is compiled. `/create-lecture` (Phase 4), `/lecture-notes` (Phase 3), and `/instructor-handout` (Phase 1) each run this audit inline on every diagram they embed; `/new-diagram` runs the same audit before its standalone compile.
- `/new-diagram` runs the same Step 1 grep patterns before its standalone compile — both skills use identical regexes so behavior doesn't drift.
- `tikz-reviewer` cites these rules by name when reporting CRITICAL/MAJOR issues.
- Quality scoring is defined in [`quality-gates.md`](quality-gates.md). The TikZ section there deducts −5 for a label-overlap finding (which is typically the symptom of a P1/P3/P4 violation that reached production); it does **not** currently deduct per-rule. That may change — consult `quality-gates.md` for the authoritative scoring rubric.
