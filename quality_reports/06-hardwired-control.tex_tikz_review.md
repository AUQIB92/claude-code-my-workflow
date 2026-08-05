# TikZ Review: 06-hardwired-control.tex

**Reviewer:** tikz-reviewer agent
**Rules applied:** `.claude/rules/tikz-measurement.md`, `.claude/rules/tikz-prevention.md`, `.claude/rules/tikz-visual-quality.md`
**Scope:** all 5 `tikzpicture` blocks (a slide-excellence orchestrator's automated detection incorrectly reported 0 TikZ blocks and skipped review; this is the manual follow-up)

Diagram index: **D1** L120 (CU I/O), **D2** L229 (SC + step decoder), **D3** L332 (two decoders → matrix), **D4** L428 (AND-OR gates), **D5** L468 (full block diagram).

Text width = 14.0 cm (16 − 2×1cm margins); body height after frametitle ≈ 6.3 cm. Beamer default 11pt → `\small`=9pt, `\scriptsize`=7pt. Conversion rule: with `scale=s, transform shape`, a coded gap `g` renders as `g × s` cm — several blocks were authored as if the coded numbers were the physical ones.

## VERDICT: REJECTED

Four CRITICAL and nine MAJOR issues. D4 (the AND-OR gate diagram) needs to be rebuilt rather than patched — its box boundaries, wire y-values, and gate colors are all wrong simultaneously, and it is the pedagogical payoff slide for "this is literally what hardwired means." D3's duplicated arrowheads and the deck-wide 4.3–7.2pt type are also disqualifying on their own.

---

## CRITICAL

### Issue 1: D4 — AND-gate input wires are collinear with box edges, terminate on rounded corners
L433-435, L439-441. `AND1` at `(3.0,1.5)`, 1.0×1.0cm → boundary y∈[1.0,2.0]. Input wires at y=2.0 and y=1.0 are exactly on the box's top/bottom edges — rendered as one continuous line crossing the gate rather than two inputs entering it. Rounded corners (4pt) put the arrowhead ~0.045cm outside the drawn outline. Mirrored on AND2.
**Fix:** `minimum height=1.4cm`, feed wires at interior y-values (1.9/1.1), route straight in via `(AND1.west |- 0,1.9)`.

### Issue 2: D4 — OR-gate input wires backtrack (drop below target, climb back up)
L444-445. Path descends to y=0.4 then reverses upward to reach `OR.north west` (y=0.8) — a visible V-kink. Mirrored below. Both land on rounded corners.
**Fix:** route to the straight west-edge segment with no reversal, at x=5.3.

### Issue 3: All five diagrams — effective font 4.3–7.2pt from over-aggressive downscaling
Every block leaves 4-7cm of the 14cm text width empty and 2.3-4.1cm of the 6.3cm body height empty, yet shrinks type below 8pt (down to 4.3pt on the capstone D5). Unreadable from the back of a room.

| Blk | scale | rendered W×H | unused width | `\small`→ | `\scriptsize`→ |
|---|---|---|---|---|---|
| D1 | 0.72 | 9.81×2.84cm | 4.2cm | 6.5pt | — |
| D2 | 0.80 | 7.04×2.16cm | 7.0cm | 7.2pt | — |
| D3 | 0.68 | 10.00×3.30cm | 4.0cm | 6.1pt | 4.8pt |
| D4 | 0.78 | 8.11×3.12cm | 5.9cm | 7.0pt | 5.5pt |
| D5 | 0.62 | 8.25×3.99cm | 5.8cm | 5.6pt | 4.3pt |

**Fix:** raise scales to width/height-limited maxima: D1 0.95, D2 1.30, D3 0.90, D4 1.25, D5 0.90 (0.88 if Issue 8's fix is also applied).

### Issue 4: D3 — spurious mid-wire arrowheads pointing into empty space
L340+351, L347+352. `(ODEC.east) -- (8.0,1.8);` terminates with an arrowhead aimed at nothing; the next path restarts from that point. Reads as a broken/severed connection. Duplicated on the SC branch.
**Fix:** merge into single paths: `\draw[->, thick] (ODEC.east) -- (8.0,1.8) |- (MAT.west |- 0,0.9);` (delete L340, L347). Do not route straight in at y=±1.8 — that lands on MAT's rounded corner.

---

## MAJOR

### Issue 5: D1 — output boxes clear each other by 0.14cm
L139-142. `out1`'s text wraps to 2 lines (actual height ≈0.91cm) while `minimum height=0.7cm` assumes 1 line. Gap to `out2` = 0.14cm < 0.3cm minimum.
**Fix:** widen `text width` to 3.6cm to keep `out1` single-line, or fix via Issue 6's respacing.

### Issue 6: D1 — output column off-center by 0.3, `out4` wire leaves the CU box's rounded corner
L139-150 vs L122-124. Inputs centroid at y=0.0 (symmetric); outputs centroid at y=-0.3 (hangs below with no stated reason). `out4`'s wire origin `(6.5,-1.8)` is exactly the CU box's SE corner — 0.042cm outside the drawn outline after rounding.
**Fix:** mirror the input column (outputs at y=1.5/0.5/-0.5/-1.5), re-center, move wire origins onto the straight part of the east edge.

### Issue 7: D4 — input labels sit 0.19-0.25cm from the wires they label
L430,431,436,437. `$D_{\text{ADD}}$` and `$T_2$` labels both under the 0.3cm minimum from their wires.
**Fix:** move all four labels to x=-0.75.

### Issue 8: D5 — "feedback into SC" caption is 0.11cm from the wire it captions
L497-498. Gold caption under a gold wire at 0.11cm gap — unreadable at the Issue-3 font sizes.
**Fix:** move to y=-3.85 (prefer scale 0.88 over 0.90 to keep the new bbox within the 6.3cm body).

### Issue 9: Pass 0 — same components change name and color between slides
D1 vs D5: decoder input boxes are `draw=neutral,fill=white` in D1 but `draw=primary-blue,fill=light-bg` in D5 for identical components. Decoder names abbreviate inconsistently ("Step decoder" vs "Step dec.").
**Fix:** standardize on D5's convention (blue/light-bg = register/source; gold/white = decoder; positive/light-bg = control-signal output); back-port to D1; restore full decoder names in D5 at the corrected scale.

### Issue 10: D4 — vertical wire runs 0.078cm alongside the OR box edge
L444-445 vs L442-443. Two near-touching parallel strokes over y∈[0.4,0.8].
**Fix:** same x=5.3 change as Issue 2.

### Issue 11: D5 — inconsistent wire routing into the control matrix
L487-490. Two inputs route straight-horizontal; two others have a gratuitous 0.19cm diagonal jog for no reason (both target y-values are well inside the straight edge span).
**Fix:** route all four horizontally via `(MAT.west |- 0,y)`.

### Issue 12: Rule P2 — three coordinate-map comments disagree with the code
D1: comment says outputs at x=10.2; code uses 10.6. D3: three separate coordinate mismatches. D5: five separate coordinate mismatches. A wrong coordinate map is worse than none.
**Fix:** regenerate all three comment blocks from final coordinates after fixes land.

### Issue 13: D4 — gate colors contradict the deck's established color semantics
L432-433,438-439 vs 442-443. Deck-wide convention: blue=register/matrix, gold=decoder, positive=output. D4 reassigns gold=AND gate, blue=OR gate — and draws two objects of the same class (logic gates) in different colors with no semantic reason.
**Fix:** draw both AND gates and the OR gate in one neutral style (`draw=neutral, fill=white`); keep `draw=positive` on the $Z_{\text{in}}$ output.

---

## MINOR

14. **D1/D2 stacked boxes** — sub-threshold 0.216-0.24cm gaps between stacked input/T-boxes. Cleared automatically by the Issue 3 rescale.
15. **D3 decoder-output labels** 0.27cm above their wires (10% under). Cleared by the Issue 3 rescale.
16. **D5 feedback wire** passes 0.28cm under the step decoder. Cleared by the Issue 3 rescale, or route the return at y=-3.4.
17. **D1 "ALU function select"** is within 0.15cm of wrapping — one font-metric hair from a visible overlap with `out1`. Set `text width=3.4cm` on all four output nodes, or shorten to "ALU select" (already used in D5).
18. **D5 arrow stub into `SC.south`** is only 0.31cm, mostly consumed by the arrowhead. Drop the return line to y=-3.5.
19. **D4 coordinate-map comment** describes a "shared label" that doesn't exist in the code (there are two independent `$T_2$` nodes). Rewrite to match and add label coordinates.
20. **Hard-coded box-edge coordinates instead of anchors** (D1 L134-137/147-150, D2 L242-244, D4 L434-435/440-441) — any future `minimum width` change silently detaches these arrows. Use the `X.west |- 0,y` idiom already used correctly in D3/D5.

---

## Additional note
No `Figures/**/extract_tikz.tex` exists for this deck, so there is no stale-SVG risk yet — but per `single-source-of-truth.md`, fix the Beamer source first and only then run `/extract-tikz`.

## Required before re-review
1. Rebuild D4 — non-collinear wire entry into resized AND boxes, monotone routing into the OR gate, unified gate color, labels at x=-0.75.
2. Merge D3's split paths into single `->` paths (delete L340, L347).
3. Raise all five scales to the computed maxima.
4. Re-center D1's output column, move wire origins off the CU corners.
5. Move D5's feedback caption to y=-3.85, straighten the two diagonal jogs into MAT.
6. Restore full decoder names, unify input-box colors between D1 and D5.
7. Regenerate the three drifted coordinate-map comments.

After those land, re-run all six passes on **all five** blocks — the same faulty corner-attachment construction (Issues 1, 6) recurs across blocks, so a full-deck re-audit is required, not a spot-check.

**File reviewed:** `Slides/06-hardwired-control.tex`
