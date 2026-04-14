---
paths:
  - "Slides/**/*.tex"
  - "Figures/**/*.tex"
  - "Preambles/**/*.tex"
---

# TikZ Prevention Rules

**Write TikZ that can't collide in the first place.** Complements `tikz-visual-quality.md` (general standards) and `tikz-measurement.md` (repair-time formulas). Load whenever you are authoring or editing a `\begin{tikzpicture}` block.

> Adapted from Scott Cunningham's `tikz_rules.md` in [MixtapeTools](https://github.com/scunning1975/MixtapeTools). Used with attribution.

The LaTeX compiler does **not** warn on label-over-arrow overlaps, labels crossing shape boundaries, or arrows crossing arrows. Every one of these bugs must be caught at authoring time or in review. These rules shift the catch upstream.

---

## Rule P1: Explicit node dimensions (MANDATORY)

Every node that holds text must declare its size explicitly. Implicit sizing means the label can grow past the box edge without anyone noticing.

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

## Rule P3: Prohibition on `scale=X` for complex diagrams

`scale=0.8` shrinks coordinates but not text. A 2 cm gap becomes 1.6 cm; the 1.2 cm label that fit before now overlaps. This failure mode silently produces the exact collisions the measurement rule is designed to prevent.

**Never use `scale=` on a diagram with more than two labeled nodes.** Design at the intended size.

If you *must* scale (e.g., matching a slide layout):

```latex
% If scale is unavoidable, scale everything — but prefer to redesign.
\begin{tikzpicture}[scale=0.8, every node/.style={scale=0.8}]
```

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

## Enforcement

- `/extract-tikz` runs a prevention pre-check (Step 1.5) before compiling. Violations of P1, P2, P3, or P4 halt the pipeline and report the offending block.
- `tikz-reviewer` cites these rules by name when reporting CRITICAL/MAJOR issues.
- Quality score deducts −5 per violation caught post-hoc (see `quality-gates.md` TikZ section).
