# TikZ Measurement Audit — `Slides/05-addressing-cpu-bus.tex`

**Reviewer:** `tikz-reviewer` (six-pass measurement protocol, `.claude/rules/tikz-measurement.md`)
**Source:** `Slides/05-addressing-cpu-bus.tex`
**Diagrams reviewed:** 9 `tikzpicture` environments (lines 112, 146, 179, 228, 260, 307, 401, 473, 606)
**Verdict:** **NEEDS REVISION** — 1 CRITICAL, 13 MAJOR

## Geometry baseline used throughout

| Quantity | Value | Source |
|---|---|---|
| Paper | 16.00 x 9.00 cm | `aspectratio=169` |
| `\textwidth` | **14.00 cm** (16.00 - 2 x 1.0 cm default beamer text margins) | `Preambles/header.tex` sets no `\setbeamersize` |
| Frame body height (after frametitle + footline) | ~ 6.8-7.1 cm | footline template at `header.tex:99-100` |
| Default node `inner sep` | 0.3333 em ~ **0.117 cm** at `\small` (10 pt) | TikZ default |
| Char widths | `\scriptsize` 0.10, `\small` 0.15 cm; mono +15% | `tikz-measurement.md` Pass 2 table |

> **Correction to the prior visual audit:** that report assumed "~10.8-11.3 cm text width available on a 16:9 Beamer slide." 10.8 cm is the **4:3** figure (12.8 - 2). For `aspectratio=169` it is **14.0 cm**. All width findings below use 14.0 cm; several of that report's table-overflow claims may be softer than stated. Heights are unaffected.

## Pass 1 & Pass 5b — global clean results

- `grep "bend"` -> **0 matches.** No Bezier/curved arrows anywhere in the deck. Pass 1 vacuously clean.
- `grep "plot"` -> **0 matches.** No plotted curves. Pass 5b vacuously clean.
- **Pass 3 (directional keywords):** all 10 edge-attached labels (lines 121, 154, 190, 191, 235, 242, 314, 317, 612, 613, 614) carry `above` / `below` / `right`. **Zero P4 violations.**
- **P3 (bare `scale=`):** all 9 use `scale=X, transform shape`. **Zero violations** (confirms prior audit).

---

# Diagram 1 — Immediate addressing (lines 112-122, `scale=0.8`)

### Issue 1: Diagram renders 0.36 cm left of slide centre (bounding-box asymmetry)
- **Severity:** MINOR
- **Location:** `\draw[->, thick] (instr.south) -- (alu.north) node[midway, right, font=\scriptsize] {no EA --- value used directly};` (line 121)
- **Problem:** Pass 2 width estimate — the label is 28 chars at `\scriptsize` = 28 x 0.10 = **2.80 units**. Anchored `right` at x = 0.117, it spans x in [0.117, 2.917]. The boxes span x in [-2.017, 2.017] (`text width=3.8` + 2 x 0.117 = 4.034, overriding `minimum width=4.0`). Composite bbox is x in [-2.017, 2.917], centre 0.45 units = **0.36 cm** physical. `\begin{center}` centres that bbox, so both boxes visibly sit 0.36 cm left of slide centre while the caption dangles right.
- **Fix:** Add `align=left, text width=1.7cm` to the label node — it wraps to 2 lines (2 x 0.28 = 0.56 units, comfortably inside the 1.70-unit shaft gap) and the bbox right edge drops from 2.917 to ~1.95, cutting the offset to ~0.03 cm.

### Issue 2: `instr` text at 97% of its `text width` — one-word wrap risk
- **Severity:** MINOR
- **Location:** line 116, `text width=3.8cm`, content `Instruction: \texttt{ADD R1, \#5}`
- **Problem:** Pass 2 width: "Instruction: " = 13 x 0.15 = 1.95 cm; `ADD R1, #5` = 10 x 0.15 x 1.15 (mono) = 1.73 cm. Total **3.68 cm** against 3.80 cm — 0.12 cm (3%) of slack. Any font-metric shift wraps `#5` alone onto line 2, growing the node to ~1.06 cm and breaking the stated 0.9 cm height.
- **Fix:** `text width=4.2cm, minimum width=4.4cm`.

---

# Diagram 2 — Direct addressing (lines 146-156, `scale=0.78`)

### Issue 3: `EA = 1000` caption sits 0.091 cm from the `mem` box edge
- **Severity:** MAJOR
- **Location:** line 155, `\node[below, font=\scriptsize] at (mem.south) {$\text{EA} = 1000$};`
- **Problem:** **Pass 4, Boundary Rule.** `mem` = `minimum height=1.0cm` at y = 0 -> bottom boundary y = **-0.500**. `below` places the node's north anchor exactly on that boundary; the glyph top is inset only by `inner ysep` = 0.117 units -> y = -0.617. Edge-to-text clearance = 0.117 units x 0.78 = **0.091 cm**. Pass 4 requires **0.4 cm**. Shortfall 0.31 cm (23% of requirement met). The caption reads as glued to the box.
- **Fix:** `\node[below=0.4cm, font=\scriptsize] at (mem.south) {...};` -> 0.4 x 0.78 = 0.31 cm + inner sep 0.09 = 0.40 cm OK. (Or `below=0.55cm` for a comfortable 0.52 cm.)

### Issue 5 (see also Diagram 3): family width/pitch drift
- **Severity:** MINOR
- **Location:** `mem` at line 153 is `minimum width=3.4cm`, pitch 5.6; the structurally identical `mem300`/`mem500` (lines 186, 189) are `3.2cm` at pitch 5.2 — both at `scale=0.78`.
- **Problem:** Pass 0 layout consistency. Direct and Indirect are presented as the one-hop / two-hop version of the same picture on consecutive slides, but the "memory" box changes from 2.68 cm to 2.52 cm wide and the hop length changes from 4.37 cm to 4.06 cm between them. Boxes appear to breathe between slides.
- **Fix:** Standardise the memory-mode family on `minimum width=3.2cm, text width=3.0cm` and pitch 5.2 in both.

---

# Diagram 3 — Indirect addressing (lines 179-193, `scale=0.78`)

### Issue 4: `EA = 500` caption sits 0.091 cm from the `mem500` box edge
- **Severity:** MAJOR
- **Location:** line 192, `\node[below, font=\scriptsize] at (mem500.south) {$\text{EA} = 500$};`
- **Problem:** Identical Pass 4 violation to Issue 3. `mem500` bottom boundary = -0.500; text top = -0.617; clearance 0.117 x 0.78 = **0.091 cm** vs. the 0.4 cm minimum.
- **Fix:** `below=0.4cm`.

**Measured clean on this diagram:**
- Pass 2, `address` label: available gap = 5.2 - 1.617 - 1.617 = 1.966; usable = 1.966 - 0.6 = **1.366**; label 7 x 0.10 = **0.70**. 51% utilisation OK
- Pass 2, `pointer` label: same gap, 7 chars = 0.70 OK
- Pass 5, width: bbox x in [-1.617, 12.017] = 13.63 units x 0.78 = **10.63 cm** in a 14.0 cm text block -> 1.68 cm margins OK

---

# Diagram 4 — Register / Register-indirect (lines 228-244, `scale=0.72`)

### Issue 6: Row-1 caption clears the box edge by 0.26 cm, not the 0.4 cm the code comment claims
- **Severity:** MAJOR
- **Location:** line 236, `\node[font=\scriptsize] at (2.3,0.4) {register --- operand \emph{in} R2};` vs. `ALU1` at (4.6, 1.3), `minimum height=0.8cm`
- **Problem:** **Pass 4.** Row-1 boxes' bottom boundary = 1.3 - 0.4 = **0.900**. The caption is centred at y = 0.4; `\scriptsize` half text height ~ 0.14 units -> glyph top at **0.540**. Clearance = 0.900 - 0.540 = 0.360 units x 0.72 = **0.26 cm**, against the 0.4 cm Pass 4 minimum. Horizontally the caption is 26 x 0.10 = 2.60 units wide -> x in [1.00, 3.60], which overlaps `ALU1`'s x-range [3.29, 5.91] over [3.29, 3.60], so the shortfall is a real overlap corridor, not a theoretical one.
- **Root cause:** the inline comment at line 227 states "Captions sit 0.9 below each row's node centers (clears box half-height + 0.4cm margin)." The arithmetic omits (a) the caption's own 0.14-unit half-height and (b) that `scale=0.72` shrinks the nominal 0.4 units to 0.29 cm. Actual delivered clearance is 0.26 cm.
- **Fix:** move the caption to `y = 0.15`. New glyph top 0.29; clearance (0.900 - 0.290) x 0.72 = **0.44 cm** OK. Update the comment to state the physical clearance after scaling.

### Issue 7: Row-2 caption — same 0.26 cm shortfall
- **Severity:** MAJOR
- **Location:** line 243, `\node[font=\scriptsize] at (2.4,-2.2) {register-indirect --- R2 \emph{holds} the address};` vs. row-2 boxes' bottom boundary y = -1.700
- **Problem:** Pass 4. Glyph top at -2.060; clearance 0.340 units x 0.72 = **0.245 cm** vs. 0.4 cm. Caption is 41 x 0.10 = 4.10 units wide -> x in [0.35, 4.45], overlapping **both** `R2ind` (x in [-0.94, 0.94]) and `Mem` (x in [3.39, 6.21]) in x. Two overlap corridors.
- **Fix:** move to `y = -2.45` -> clearance (2.45 - 0.14 - 1.70) x 0.72 = **0.44 cm** OK

### Issue 8: Colour semantics inverted — `positive` marks the source register here, the destination everywhere else
- **Severity:** MAJOR
- **Location:** line 230 `(R2reg)` = `draw=positive`; line 232 `(ALU1)` = `draw=primary-blue`; line 238 `(R2ind)` = `draw=primary-gold`
- **Problem:** **Pass 0, cross-slide consistency ("Colors must match").** Across the addressing-mode family the convention is: `primary-blue` = instruction/intermediate, on the left; `positive` (green) = the final operand, on the right.
  - Immediate: `instr` blue (left) -> result `positive` (right) OK
  - Direct: `instr` blue -> `mem` `positive` OK
  - Indirect: `instr` blue -> `mem300` blue -> `mem500` `positive` OK
  - Displacement: `Rbase`/`Rindex` blue -> `EAnode` `positive` OK
  - Autoincrement: `R2b` blue -> `Mem` `positive` OK
  - **Register row (this diagram): `R2reg` `positive` on the LEFT, `ALU1` blue on the RIGHT — inverted.**
  Worse, within this one tikzpicture the same register `R2` is green in row 1 and gold in row 2, on a slide whose whole point is that the two rows differ only in how R2 is interpreted.
- **Fix:** `R2reg` -> `draw=primary-gold, fill=white` (matching `R2ind`, since both are "the register named in the instruction"); `ALU1` -> `draw=positive, fill=light-bg` (matching every other diagram's right-hand operand node).

### Issue 9: The two rows' right-hand boxes are ragged
- **Severity:** MINOR
- **Location:** `ALU1` at (4.6, .) width = max(2.6, 2.4 + 0.234) = 2.634 -> x in [3.283, 5.917]; `Mem` at (4.8, .) width = max(2.8, 2.6 + 0.234) = 2.834 -> x in [3.383, 6.217]
- **Problem:** Left edges differ by 0.100 units (0.072 cm), right edges by 0.300 units (0.216 cm). Two stacked parallel rows read as misaligned.
- **Fix:** put both at x = 4.7 with `minimum width=2.9cm, text width=2.7cm`.

---

# Diagram 5 — Displacement addressing (lines 260-273, `scale=0.8`)

**The cleanest diagram in the deck.** All Pass 2/4 checks pass:
- Caption at (3.6, -2.4) vs. `Rindex` bottom boundary -1.750: glyph top -2.260, clearance 0.510 x 0.8 = **0.41 cm** OK (Pass 4 satisfied — and the author's comment at line 259 is correct here).
- Caption x-span [2.35, 4.85] does not overlap `Rindex` x in [-1.4, 1.4] at all OK
- `adder` circle (3.6, 0), `minimum size=0.9cm` -> boundary r = 0.45; all three arrows terminate on the computed border via named-node syntax OK
- No edge labels -> Pass 3 vacuous OK

### Issue 10: Vertical mass sits above the bounding-box centre
- **Severity:** MINOR
- **Location:** bbox y in [1.750, -2.525]; centre = **-0.388**
- **Problem:** The primary row (`adder`, `EAnode`) is at y = 0, i.e. 0.39 units (0.31 cm) above the bbox centre, because the caption is the only element below y = -1.75. Inside `\begin{center}` the diagram will read as top-heavy.
- **Fix:** raise the caption to y = -2.25 (clearance recomputes to (2.25 - 0.14 - 1.75) x 0.8 = 0.29 cm — too tight), or better, shift the whole diagram: `Rbase` y = 1.55, `Rindex` y = -1.05, caption y = -2.25. Alternatively accept it; this is pure polish.

---

# Diagram 6 — Autoincrement (lines 307-318, `scale=0.75`)

### Issue 11: `Step 1` label at 80% of usable gap — no headroom, and it sits inside the boxes' vertical band
- **Severity:** MINOR (borderline MAJOR)
- **Location:** line 314, `node[midway, above, font=\scriptsize] {Step 1: $\text{EA}=[\text{R2}]$}`
- **Problem:** **Pass 2.** `R2b` half-width 1.000; `Mem` half-width = max(2.6, 2.4 + 0.234)/2 = 1.317. Available gap = 4.8 - 1.000 - 1.317 = **2.483**; usable = 2.483 - 0.6 = **1.883**. Label = 15 chars at `\scriptsize` = **1.500**. Utilisation 80%; margin 0.19 units = 0.14 cm per side.
  The consequence matters because the label's vertical band is y in [1.20, 1.45] and the boxes' band is y in [0.80, 1.60] — they overlap in y. So any growth in the label (font substitution, adding "(EA)") produces a direct box overlap rather than harmless overhang.
- **Fix:** shorten to `Step 1: EA` (11 chars = 1.10, 58% utilisation) and put the formula in the prose, or raise the label with `above=0.25cm` so its band clears the box top (y = 1.60).

### Issue 12: `Step 2` label 0.088 cm from its own shaft (consistency)
- **Severity:** MINOR
- **Location:** line 317, `node[midway, right, font=\scriptsize] {Step 2: $R2 \mathrel{+}= 4$}`
- **Problem:** Bare `right` gives only `inner xsep` = 0.117 units x 0.75 = **0.088 cm** between the vertical shaft at x = 0 and the glyph. Same pattern as Diagram 1 line 121 (0.094 cm). Not a collision, but under the Pass 5 label<->arrow 0.3 cm guideline and visually cramped against a `thick` shaft.
- **Fix:** `right=0.25cm` on both this and line 121 (0.25 x 0.75 = 0.19 + 0.09 inner = 0.28 cm; use `right=0.3cm` for a clean 0.32 cm).

---

# Diagram 7 — CPU building blocks (lines 401-417, `scale=0.85`)

### Issue 13: Bus-stub arrows are 0.51 cm long with arrowheads at both ends — no visible shaft
- **Severity:** MAJOR
- **Location:** lines 411-413, `\draw[<->, thick] (CU.south) -- (0,-1.1);` and the two siblings at x = 2.6 and x = 5.2
- **Problem:** Box bottom boundary y = -0.500 (`minimum height=1.0cm`); bus line at y = -1.100. Shaft length = 0.600 units x 0.85 = **0.51 cm**. TikZ's default `to` tip at `thick` (0.8 pt) is ~ 0.20 cm per head; `<->` draws two -> ~ **0.40 cm of the 0.51 cm segment is arrowhead**, leaving ~0.11 cm of visible line. The three connectors render as arrowheads meeting nose-to-tail, not as wires.
- **Fix:** move the bus to y = -1.7 (shaft 1.20 units x 0.85 = **1.02 cm**, ~ 0.6 cm of visible shaft), and move the `internal bus` label with it. Or reduce to single-headed `->` if bidirectionality is not the teaching point.

### Issue 14: `internal bus` label 0.099 cm from the bus line
- **Severity:** MAJOR
- **Location:** line 410, `\node[font=\scriptsize, below left] at (-1.0,-1.1) {internal bus};` vs. `\draw[thick] (-1.0,-1.1) -- (6.1,-1.1);` (line 409)
- **Problem:** **Pass 5, label <-> axis line, minimum 0.3 cm.** `below left` = `anchor=north east` placed exactly on the bus line's left endpoint. Text is inset by `inner sep` 0.117 units in both directions -> nearest glyph corner at (-1.117, -1.217); nearest line point (-1.0, -1.1). Separation = 0.117 units in each axis -> 0.165 units diagonal x 0.85 = **0.14 cm** vs. the 0.3 cm minimum. The label visually collides with the line's end cap.
- **Fix:** `\node[font=\scriptsize, below left=0.15cm and 0.05cm] at (-1.0,-1.1) {internal bus};` -> 0.15 x 0.85 = 0.13 + 0.10 inner = 0.23 cm vertical; use `below left=0.25cm and 0.1cm` for 0.31 cm OK

### Issue 15: ALU is `primary-blue` here but `primary-gold` in both datapath diagrams
- **Severity:** MAJOR
- **Location:** line 405 `(ALU) draw=primary-blue, fill=light-bg`; vs. line 497 `(ALU) draw=primary-gold, fill=white` (single-bus) and line 610 `(ALU) draw=primary-gold, fill=white` (three-bus)
- **Problem:** **Pass 0 rule 1: "Colors must match. A node labeled X in `slate` on slide 31 must stay `slate` on slide 32."** This diagram is explicitly the establishing shot for the two datapath diagrams — the slide text at line 419 says "Everything on the next several slides zooms into the box you have not seen yet." The ALU changes both stroke colour and fill between the establishing shot and the zoom-in, which breaks the visual thread the slide claims to be drawing.
- **Fix:** line 405 -> `draw=primary-gold, fill=white`.

### Issue 16: Bus line terminates at x = 6.1 while `MEM` sits at x = 8.6, connected around the bus
- **Severity:** MINOR
- **Location:** line 409 (bus x in [-1.0, 6.1]) vs. line 415 `(MEM) at (8.6,0)` and line 416 `\draw[->, thick] (REG.east) -- (MEM.west);`
- **Problem:** The MAR/MDR block is the only component not tapped into the "internal bus," and its connection bypasses the bus entirely via a point-to-point arrow at y = 0. On a slide introducing the bus as the shared interconnect this is a semantic mismatch. It also leaves the bus stopping 3.6 units (3.06 cm) short of the diagram's right edge, which reads as an unfinished line.
- **Fix:** extend the bus to `(-1.0,-1.1) -- (8.6,-1.1)` and add a fourth `<->` tap at x = 8.6 (contingent on Issue 13's re-spacing), replacing or supplementing the REG->MEM arrow.

### Issue 17: P1 — multi-line boxed nodes without `text width`
- **Severity:** MINOR
- **Location:** lines 404 `(CU) {Control\\Unit}`, 408 `(REG) {Register\\File}`, 415 `(MEM) {MAR / MDR\\$\leftrightarrow$ Memory}`
- **Problem:** **`tikz-prevention.md` P1:** "`text width` is required for any multi-line content (anything containing `\\`)." Should have been caught by the `/extract-tikz` Step 1 pre-check. Measurement confirms no current overflow — widest line is `$\leftrightarrow$ Memory` ~ 0.5 + 7 x 0.15 = 1.55 + 0.234 = 1.78 cm against `minimum width=2.2cm` OK — so this is a latent, not an active, defect.
- **Fix:** add `text width=1.8cm` (CU, REG) and `text width=2.0cm` (MEM).

---

# Diagram 8 — Single-bus datapath (lines 473-509, `scale=0.68`) — worst diagram in the deck

### Issue 18: [CRITICAL] Bus-operand arrow terminates inside the ALU rectangle
- **Severity:** CRITICAL
- **Location:** line 500, `\draw[->, thick] (6.5,0.08) |- (5.9,-2.85);` vs. line 497-498, `(ALU) at (5.2,-3.2)` with `minimum width=1.6cm, minimum height=1.0cm`
- **Problem:** **Pass 5, "Arrow origin <-> box edge: 0.15 cm".** Compute the ALU boundary explicitly:
  - x in [5.2 - 0.8, 5.2 + 0.8] = **[4.400, 6.000]**
  - y in [-3.2 - 0.5, -3.2 + 0.5] = **[-3.700, -2.700]**

  The `|-` operator routes vertical-then-horizontal: (6.5, 0.08) -> (6.5, -2.85) -> (5.9, -2.85). The terminal point (5.9, -2.85) satisfies 4.400 < 5.9 < 6.000 and -3.700 < -2.85 < -2.700 -> it is strictly interior to the ALU box. The horizontal segment crosses the right border at x = 6.000 and continues 0.100 units (0.068 cm) inside; the arrowhead (~ 0.20 cm) is therefore drawn entirely on top of the ALU's `fill=white` interior and its `primary-gold` stroke. Required clearance +0.15 cm; actual -0.068 cm — a 0.22 cm error in the wrong direction.
- **Fix (also resolves Issue 19):** route both ALU inputs onto the top edge, symmetric about x = 5.2:
  ```latex
  \draw[->, thick] (Y.south) -- (4.7,-2.7);
  \draw[->, thick] (6.5,0.08) -- (6.5,-2.4) -| (5.7,-2.7);
  ```
  Both then terminate exactly on the boundary y = -2.700, at x = 4.7 and x = 5.7 (+-0.5 from centre).

### Issue 19: ALU inputs enter different faces at different heights
- **Severity:** MAJOR
- **Location:** line 499 `(Y.south) -- (4.6,-2.7)` and line 500 `... |- (5.9,-2.85)`
- **Problem:** Input 1 lands on the top edge at (4.6, -2.700) — only 0.200 units (0.136 cm) from the top-left corner at (4.400, -2.700), so the arrowhead (~0.2 cm wide) straddles the corner. Input 2 lands on the right face at y = -2.850. A two-input ALU drawn with one input on the top-near-corner and one on the side, 0.15 units apart in y, does not read as a symmetric operand pair — which is the exact pedagogical point of the Y register on this slide.
- **Fix:** as in Issue 18 — (4.7, -2.7) and (5.7, -2.7).

### Issue 20: `common bus` label 0.12 cm from the bus line
- **Severity:** MAJOR
- **Location:** line 486, `\node[font=\scriptsize, below left] at (-1.0,-0.1) {common bus};` vs. line 485, `\draw[very thick, jet] (-1.0,0) -- (10.8,0);`
- **Problem:** **Pass 5, label <-> axis line, 0.3 cm.** `below left` -> `anchor=north east` at (-1.0, -0.1); glyph corner inset by `inner sep` 0.117 -> **(-1.117, -0.217)**. The bus is `very thick` = 1.6 pt -> half-width 0.028 cm = 0.041 units, so its lower edge is at y = **-0.041**. Vertical separation = 0.217 - 0.041 = 0.176 units x 0.68 = **0.12 cm**; horizontal separation from the line's left end cap = 0.117 x 0.68 = 0.08 cm. Both under 0.3 cm.
- **Fix:** `\node[font=\scriptsize, below left=0.3cm and 0.05cm] at (-1.0,0) {common bus};` -> (0.3 + 0.117) x 0.68 = 0.28 cm; use `below left=0.35cm and 0.05cm` for 0.32 cm OK

### Issue 21: Vertical budget exhausted — zero slack against the frame body
- **Severity:** MAJOR
- **Location:** whole diagram, lines 473-509, plus `\cite{Mano1993_computer_system_architecture}` at line 511
- **Problem:** **Pass 5, "Any object <-> slide edge: 0.5 cm."** Compute the composite bbox:
  - Top: `PC` at y = 2, `minimum height=0.9cm` -> **y = +2.450**
  - Bottom: line 508 `\node[..., below] at (7.9,-5.7)`; glyph top -5.817, `\scriptsize` depth ~ 0.28 -> **y = -6.100**
  - Height = 8.550 units x 0.68 = **5.81 cm**

  Add `center` environment `\topsep` above and below (~ 0.25 cm each) and the citation line (`\normalsize` ~ 0.45 cm) -> ~ 6.76 cm of content against a frame body of ~ 6.8-7.1 cm. Slack is 0.0-0.35 cm — i.e. the bottom label sits within 0.35 cm of the footline, violating the 0.5 cm slide-edge minimum, and may overflow outright.
  Width is fine: bbox x in [-2.117, 10.800] = 12.92 units x 0.68 = **8.79 cm** in a 14.0 cm block -> 2.6 cm side margins OK
- **Fix:** compress the vertical stack. Moving `Y` to (3.8, -1.4), `ALU` to (5.2, -2.7), `Z` to (5.2, -4.0), and the feedback rail to y = -4.9 shortens the bbox to y in [2.45, -5.30] = 7.75 units x 0.68 = **5.27 cm**, restoring 0.54 cm of slack. Do not simply drop `scale` further — 0.68 is already the smallest in the deck and `\scriptsize` labels at 0.68 render at ~5.4 pt effective.

### Issue 22: 41% of the canvas is empty while the operand path stacks vertically
- **Severity:** MAJOR
- **Location:** whole diagram
- **Problem:** **Pass 5, spacing/proportion.** Below the bus (y < 0) the occupied x-range is [3.0, 6.5] plus the return rail at x = 10.5. The entire region x in [-2.1, 3.0], y in [0, -6.1] (~ 5.1 x 6.1 units = 3.5 x 4.1 cm physical) is blank, as is x in [6.6, 10.4] below y = -1.2. Meanwhile Y -> ALU -> Z occupies a 3.2-unit vertical column, which is what drives the Issue 21 height problem. The diagram is tall-and-empty rather than wide-and-full, in a 14.0 cm x ~7 cm frame that is much wider than tall.
- **Fix:** exploit the horizontal axis. E.g. put `Y` at (2.4, -1.5), `ALU` at (5.2, -2.7), `Z` at (8.0, -1.5), and return `Z` to the bus with a short riser at x = 8.0 instead of the 5.3-unit rail at y = -5.7. This removes the rail, the long riser at x = 10.5, and ~2 units of height simultaneously.

### Issue 23: `Y` and `Z` — the same class of object in two different colours
- **Severity:** MAJOR
- **Location:** line 493 `(Y) draw=primary-gold, fill=white`; line 503 `(Z) draw=positive, fill=light-bg`
- **Problem:** **Pass 0 / visual semantics.** Y and Z are introduced as a matched pair — the deck devotes an entire frame to it (line 548, "Why `Y` and `Z` Exist", and the summary at line 746 treats them as "`Y`/`Z` buffering"). Rendering them in different colours implies a distinction the text explicitly denies. Additionally `positive` (green) is used elsewhere in this deck to mean "the final operand / the good outcome," which Z is not.
- **Fix:** `(Z)` -> `draw=primary-gold, fill=white`, matching Y.

### Issue 24: Free path labels at 0.07 cm from the wires they annotate
- **Severity:** MINOR
- **Location:** line 501 `\node[font=\scriptsize, above right] at (6.5,-1.2) {bus operand};` and line 508 `\node[font=\scriptsize, below] at (7.9,-5.7) {Z $\to$ bus (write-back)};`
- **Problem:** Both are free `\node`s (not path nodes), offset only by `inner sep` 0.117 units x 0.68 = **0.080 cm** from the wire at x = 6.5 and the rail at y = -5.7 respectively. Not collisions — geometry confirms `bus operand` spans x in [6.62, 7.72], y in [-1.15, -0.87], clear of `RF` (x in [6.70, 8.90], y in [1.55, 2.45]) and of the RF tap at x = 7.8 (y in [0.08, 1.55]) — but visually glued.
- **Fix:** `above right=0.05cm and 0.2cm` and `below=0.2cm` respectively.

### Issue 25: Bus taps stop 0.026 cm short of the bus edge
- **Severity:** MINOR
- **Location:** lines 488-491 (`-- (0,0.08)` etc.), 495 (`(3.8,-0.08) --`), 500 (`(6.5,0.08)`)
- **Problem:** Taps terminate at |y| = 0.08 units = 0.054 cm from the bus centreline. The bus is `very thick` -> half-width 0.028 cm (line widths are not scaled by `scale=`/`transform shape`). Residual white gap = 0.054 - 0.028 = **0.026 cm**. At projector scale this is a visible hairline; on a connectivity diagram a hairline gap reads as "not connected."
- **Fix:** terminate the taps at exactly `(x, 0)` — TikZ overlap is harmless here and guarantees electrical-looking contact.

### Issue 26: `ALU.south -> Z.north` shaft is 0.48 cm, ~42% arrowhead
- **Severity:** MINOR
- **Location:** line 505, `\draw[->, thick] (ALU.south) -- (Z.north);` — `ALU.south` = (5.2, -3.700), `Z.north` = (5.2, -4.400)
- **Problem:** 0.700 units x 0.68 = **0.48 cm**, of which ~ 0.20 cm is the arrow tip. Same failure mode as Issue 13 but single-headed, so borderline.
- **Fix:** resolved automatically by the Issue 22 re-layout; otherwise increase the ALU-Z separation to 1.0 unit.

---

# Diagram 9 — Three-bus datapath (lines 606-615, `scale=0.85`)

**Measured clean — this is the best-constructed datapath diagram:**
- `RF` boundary: x in [-1.0, 1.0], y in [-1.3, 1.3]. Bus A origin (1.0, 0.6) lies exactly on the right boundary OK; Bus B origin (1.0, -0.6) OK; Bus C terminus (0, -1.3) lies exactly on the bottom boundary OK
- `ALU` boundary: x in [3.5, 4.9], y in [-0.7, 0.7]. Bus A terminus (3.5, 0.45) on the left boundary OK; Bus B terminus (3.5, -0.45) OK; Bus C origin (4.9, 0) on the right-boundary midpoint OK — no penetration anywhere (contrast Issue 18)
- Bus A/B endpoints are exact mirrors about y = 0 OK
- **Pass 2:** gap = 3.5 - 1.0 = 2.500; usable = 1.900; `Bus A` = 5 x 0.10 = 0.500 -> 26% utilisation OK
- **Pass 3:** `Bus C`'s `node[midway, above]` binds to the just-completed segment (4.9,-2.2)--(0,-2.2), so midway = (2.45, -2.2), label spanning x in [1.95, 2.95], y in [-2.08, -1.83]. Nearest object is `RF` (x <= 1.0) -> 0.95 units = **0.81 cm** clearance OK
- **Pass 5:** bbox x in [-1.0, 4.9] = 5.9 x 0.85 = **5.02 cm**; y in [-2.2, 1.3] = 3.5 x 0.85 = **2.98 cm**. Fits with ~4.5 cm of horizontal and ~3.8 cm of vertical slack OK

### Issue 27: `RF` box is 63% taller than its content
- **Severity:** MINOR
- **Location:** line 609, `minimum height=2.6cm`, content = `R0..R3` (`\small`) + `\\[2pt]` + two `\scriptsize` lines
- **Problem:** Content height ~ 0.42 + 0.07 + 0.32 + 0.32 = 1.13, plus 2 x `inner ysep` 0.117 = **1.36 units**. Against `minimum height=2.6` that leaves 0.62 units (**0.53 cm physical**) of blank space above and below the text inside the box. The box reads as arbitrarily oversized rather than as "a register file is big."
- **Fix:** `minimum height=1.9cm` (leaves 0.27 units ~ 0.23 cm of internal padding), or add a fourth content line if the extra height is deliberate.

### Issue 28: Component sizes change between the two datapath slides
- **Severity:** MINOR
- **Location:** this diagram (`scale=0.85`) vs. Diagram 8 (`scale=0.68`)
- **Problem:** **Pass 0 rule 2: "Layout must match. Same nodes at same positions, same spacing, same font sizes."** Physical rendered sizes of the same named components:

  | Component | Single-bus (0.68) | Three-bus (0.85) | Delta |
  |---|---|---|---|
  | `ALU` | 1.09 x 0.68 cm | 1.19 x 1.19 cm | +9% w, +75% h |
  | `R0..R3` | 1.50 x 0.61 cm | 1.70 x 2.21 cm | +13% w, +261% h |
  | `\scriptsize` labels | ~ 5.4 pt effective | ~ 6.8 pt effective | +26% |

  The slide text at line 634 asserts "Same instruction, same ALU, different wiring" — but the ALU visibly changes size and shape between the two slides, and the labels change legibility. The 26% font-size jump also means the two slides read as different typographic registers.
- **Fix:** standardise both datapath diagrams on `scale=0.75` and make the `ALU` box identical (`minimum width=1.5cm, minimum height=1.2cm`) in both. Combined with the Issue 22 re-layout, Diagram 8 will fit at 0.75.

### Issue 29: P1 — `RF` multi-line node without `text width`
- **Severity:** MINOR
- **Location:** line 609, content contains `\\[2pt]` and `\\`
- **Problem:** `tikz-prevention.md` P1 multi-line clause. Measurement confirms no overflow (widest line `2 read ports` = 12 x 0.10 = 1.20 + 0.234 = 1.43 cm vs. `minimum width=2.0cm` OK) — latent only.
- **Fix:** add `text width=1.8cm`.

---

# Summary of findings

| Diagram | Line | Scale | CRITICAL | MAJOR | MINOR |
|---|---|---|---|---|---|
| 1 Immediate | 112 | 0.80 | 0 | 0 | 2 |
| 2 Direct | 146 | 0.78 | 0 | 1 | 1 |
| 3 Indirect | 179 | 0.78 | 0 | 1 | 0 |
| 4 Register / Reg-indirect | 228 | 0.72 | 0 | 3 | 1 |
| 5 Displacement | 260 | 0.80 | 0 | 0 | 1 |
| 6 Autoincrement | 307 | 0.75 | 0 | 0 | 2 |
| 7 CPU building blocks | 401 | 0.85 | 0 | 3 | 2 |
| 8 Single-bus datapath | 473 | 0.68 | **1** | 5 | 3 |
| 9 Three-bus datapath | 606 | 0.85 | 0 | 0 | 3 |
| **Total** | | | **1** | **13** | **15** |

## Recurring patterns (fix once, apply everywhere)

1. **Bare `below` / `below left` next to a drawn shape or line** (Issues 3, 4, 6, 7, 14, 20, 24) — delivers only `inner sep` ~ 0.117 units, which after `scale ~ 0.7-0.85` is **0.08-0.12 cm**, against Pass 4's 0.4 cm (shapes) and Pass 5's 0.3 cm (lines). Always write an explicit distance: `below=0.4cm`. This is 7 of the 29 findings.
2. **Scale-blind clearance arithmetic** (Issues 6, 7) — the coordinate-map comments compute clearances in TikZ units and label them "cm," forgetting both the label's own half-height and the `scale=` factor. Coordinate-map comments should state the physical clearance.
3. **Path endpoints not checked against computed box boundaries** (Issues 18, 19) — the CRITICAL finding. Every literal-coordinate arrow terminus must be checked against `[cx +- w/2, cy +- h/2]`. Prefer named-node syntax (`(ALU.north)`, `(ALU.west)`), which TikZ resolves against the real boundary — Diagram 9 uses this discipline and is clean.
4. **Colour used decoratively, not semantically** (Issues 8, 15, 23) — `primary-gold` currently means pointer register, adder, updated register, memory interface, buffer register, and ALU. Fix the three specific Pass 0 conflicts, then document what gold means.
5. **Short arrows swallowed by their own heads** (Issues 13, 26) — any shaft under ~0.7 cm physical needs re-spacing; `<->` needs ~1.0 cm minimum.

## Verdict

**NEEDS REVISION.** Blocking before approval:

- **Issue 18 (CRITICAL)** — arrow terminating inside the ALU box, Diagram 8 line 500.
- **All 13 MAJOR issues**, in priority order: 18/19 (ALU wiring), 21/22 (single-bus vertical budget and proportion), 3/4/6/7 (Pass 4 boundary clearances), 8/15/23 (Pass 0 colour), 13/14/20 (arrow and axis-label geometry).

MINOR issues are recommended but not blocking. Re-review after fixes — per `tikz-measurement.md`, "After any TikZ fix, re-audit every TikZ figure in the deck," since patterns 1-5 above recur by construction.

---

## Reviewer's summary

- **Diagrams reviewed:** 9 of 9 (`tikzpicture` at lines 112, 146, 179, 228, 260, 307, 401, 473, 606).
- **Issues found:** 29 total — 1 Critical, 13 Medium (MAJOR), 15 Low (MINOR).
- **The one Critical:** line 500, `\draw[->, thick] (6.5,0.08) |- (5.9,-2.85);` in the single-bus datapath terminates at a point that is strictly inside the ALU rectangle (x in [4.400, 6.000], y in [-3.700, -2.700]) — the arrowhead is drawn over the box fill, 0.068 cm past the boundary, versus the +0.15 cm Pass 5 requirement.
- **Cleanest diagrams:** #5 Displacement and #9 Three-bus (zero Critical/Medium; #9 is the only one that uses named-node anchors throughout, which is why its endpoints are all exact).
- **Worst diagram:** #8 Single-bus datapath (1 Critical + 5 Medium + 3 Low), including a vertical-budget finding: its bbox is 5.81 cm tall and, with the `center` skips and the citation line, totals ~ 6.76 cm against a ~ 6.8-7.1 cm frame body.
- **Clean passes deck-wide:** Pass 1 (no `bend` anywhere), Pass 5b (no `\draw plot`), Pass 3 / prevention-rule P4 (all 10 edge labels carry a directional keyword), prevention-rule P3 (all 9 pair `scale=` with `transform shape`).
- **One correction to the earlier visual audit:** it used 10.8-11.3 cm as the available text width; for `aspectratio=169` with beamer's default 1 cm margins it is **14.0 cm**. No TikZ diagram in this deck exceeds it (widest is #3 Indirect at 10.63 cm) — all margin risk here is vertical, not horizontal.
</content>
