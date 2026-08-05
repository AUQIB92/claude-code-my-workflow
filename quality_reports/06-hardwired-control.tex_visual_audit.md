# Visual / Layout Audit — 06-hardwired-control.tex

**File audited:** `Slides/06-hardwired-control.tex`
**Frames:** 31 (including titlepage, 4 `\transitionslide` standouts, and references)
**Format:** Beamer, `aspectratio=169`

## Scorecard

| Category | Rating | Notes |
|---|---|---|
| Overflow risk | ⚠️ Minor concern | Two `\footnotesize` tables are dense enough to warrant a compile-log check; no confirmed overfull hbox from source inspection alone |
| Font consistency | ⚠️ Minor concern | Blanket `\footnotesize` applied to whole frames (not scoped to tables) on 3 frames |
| Box fatigue | ✅ Pass | Max 2 boxes/frame (INV-7 limit), most frames use 0–1 |
| Spacing (vspace hacks) | ✅ Pass (informational) | Consistent `\vspace{0.3–0.4cm}` pattern before blocks (5 instances) — deliberate rhythm, not a defect |
| Overlay commands (`\pause` etc.) | ✅ Pass | None found — complies with INV-6 / `no-pause-beamer.md` |
| Standout/transition slides | ✅ Pass | 4 `\transitionslide` calls, one at each Act boundary |
| Pedagogy (motivation before formalism) | ✅ Pass (mostly) | INV-8 generally honored; one frame is weak in isolation |
| Semantic color use on binary contrasts | ✅ Good example found | `\good{Pro}` / `\bad{Con}` on Trade-offs slide |
| Images/figures | N/A | No `\includegraphics`; all visuals are native TikZ (out of scope for this pass) |
| Itemize nesting depth | ✅ Pass | No nested itemize/enumerate found anywhere in the deck |
| Citation style | ✅ Pass | `\cite{}` used consistently (4 instances), no `\citet`/`\citep` mixing |

**Overall:** No high-severity/breaking issues found by source inspection. The deck is disciplined about box count and overlay-command avoidance. The main actionable items are a repeated font-scoping antipattern and two tables worth a compile-log sanity check.

**Scope note:** the task brief that spawned this review stated the file has "0 tikzpicture blocks" (a detection bug in the calling orchestrator); it actually contains **5** `\begin{tikzpicture}` environments (frames "Control Unit: Inputs and Outputs", "The Sequence Counter (SC)", "Two Decoders Feed the Control Matrix", "The Control Matrix as Actual Logic Gates", "Full Hardwired Control Unit Block Diagram" — lines 120, 229, 332, 428, 468). Diagram-geometry checks (label collisions, bend depth, node sizing per `tikz-measurement.md`) were **not** run here — see the separate `06-hardwired-control.tex_tikz_review.md` for that pass.

---

## Findings (severity-ranked, most severe first)

### Slide: "Recall: We Wrote $T_1, T_2, T_3$ by Hand" (slide 11)
- **Issue:** `\footnotesize` is declared at the top of the frame (line 199) and applies to the *entire* frame body — not just the 4-column `tabular` that needs it. This also shrinks the subsequent `\begin{block}{Socratic question}` prose unnecessarily. The last table column ("What happens") contains long strings like `R3 onto bus $\to$ ALU; ALU adds $Y$; result $\to Z$`, which combined with 3 other populated columns is a plausible overfull-hbox candidate at `aspectratio=169` textwidth.
- **Severity:** Medium
- **Recommendation:** Scope the size reduction to just the table (wrap only the `tabular` in a group), restoring normal size for the block text below. Verify against the actual compile log for overfull-hbox warnings; if present, shorten the "What happens" column text before reaching for `\resizebox`.

### Slide: "Building the State Table for `R1 ← R2+R3`" (slide 19)
- **Issue:** Same blanket-`\footnotesize` pattern as above (line 366) — the 3-column state table is preceded by `\footnotesize` that also shrinks the following `\begin{exampleblock}` text, which doesn't need to be small.
- **Severity:** Medium
- **Recommendation:** Scope `\footnotesize` to the `tabular` only; let the `exampleblock` render at normal size, consistent with other exampleblocks in the deck.

### Slide: "Worked Trace Revisited: Where `SC` Points" (slide 14)
- **Issue:** Third instance of the blanket-`\footnotesize` pattern (line 267) — the 4-column table is fine at this size, but the closing `\key{...}` sentence after the table also renders at `\footnotesize`, breaking visual consistency with equivalent closing-sentence text on other slides.
- **Severity:** Medium
- **Recommendation:** Scope `\footnotesize` to the table only. Once all three instances are fixed, spot-check that the deck no longer mixes "normal-size closing sentence" and "footnotesize closing sentence" patterns across similar frame types.

### Slide: "Definition: Control Unit" (slide 6)
- **Issue:** The frame opens directly with `\begin{block}{Control unit}` (line 91) with no framing sentence on the slide itself before the formal definition. INV-8 is satisfied at the *deck* level (the preceding frame is the motivating Socratic setup), but the definition frame is not self-contained for non-linear navigation (e.g. Q&A).
- **Severity:** Low
- **Recommendation:** Add one short framing clause at the top of this frame before the block.

### Slide: Deck-wide — manual `\vspace` pattern before blocks
- **Issue:** Five frames (lines 43, 62, 209, 277, 376) use a hand-typed `\vspace{0.3cm}`/`\vspace{0.4cm}` before a block/exampleblock. Consistent values, hard-coded five separate times.
- **Severity:** Low
- **Recommendation:** Not a visual defect; for maintainability consider a single macro (e.g. `\newcommand{\boxgap}{\vspace{0.3cm}}`) in `header.tex`.

### Slide: "Where We Left Off (Week 5)" (slide 2)
- **Issue:** Frame uses 2 colored boxes (`block` + `exampleblock`), exactly at the INV-7 cap.
- **Severity:** Low (informational, not a violation)
- **Recommendation:** No action required; flagging only because any future edit adding a third box here would need to split into two frames.

---

## Positive Observations

- No overlay commands anywhere — full compliance with `no-pause-beamer.md` / INV-6.
- Box discipline is strong: 24 of 31 frames use zero or one colored box; only one frame reaches the 2-box cap, none exceed it.
- Good semantic-color usage: "Hardwired Control: Trade-offs" (slide 26) uses `\good{Pro}` / `\bad{Con}` markers correctly.
- Transition slides land at genuine conceptual pivots (Act boundaries), not decoratively.
- No nested itemize/enumerate anywhere.
- Custom semantic macros (`\key`, `\good`, `\bad`, `\muted`) used consistently.

---

**Reviewer:** slide-auditor agent, run manually (outside `/slide-excellence`'s own file-write path) since the session had no Write tool; content saved to disk by the main session afterward.
