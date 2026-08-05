# Proofreading Report: 06-hardwired-control.tex

**File:** `Slides/06-hardwired-control.tex`
**Reviewed:** 613 lines / 26 frames
**Citations checked against:** `Bibliography_base.bib` (all 3 keys — `Hamacher2002_computer_organization`, `Mano1993_computer_system_architecture`, `Stallings2015_computer_organization` — resolve correctly and match the topics they're attached to)

## Scorecard

| Category | Score | Notes |
|---|---|---|
| Grammar | 90/100 | One garbled/ungrammatical sentence (missing relative pronoun) |
| Typos | 92/100 | One stray empty LaTeX subscript artifact |
| Overflow | 97/100 | No confirmed overfull hbox risk; one equation flagged as a compile-time watch item |
| Consistency | 82/100 | Notation-registry violation (missing brackets around register contents) + terminology drift ("state" vs. "control step") + minor `\texttt{}` formatting inconsistency |
| Academic Quality | 90/100 | One informal contraction, one informal "OR'd" construction |
| **Overall** | **83/100** | **Commit-ready (≥80), not yet PR-ready (<90)** per `quality-gates.md` thresholds |

No critical issues (no compilation-breaking errors, no undefined citations, no confirmed overfull-hbox >10pt). All issues below are Medium/Low severity polish items.

---

## Issue 1: Ungrammatical sentence — missing relative pronoun
- **Location:** Line 511, frame "Socratic Check: Adding a New Instruction"
- **Current:** "Every equation for a signal \texttt{MUL} needs (e.g.\ $Z_{\text{in}}$) must be \textbf{re-derived}..."
- **Proposed:** "Every equation for a signal that \texttt{MUL} needs (e.g., $Z_{\text{in}}$) must be \textbf{re-derived}..."
- **Category:** Grammar — **Severity:** High
- **Rationale:** The missing "that" makes the clause read as two collided verb phrases; could confuse students on a Socratic-check slide meant to test understanding.

## Issue 2: Stray empty LaTeX subscript (typo/artifact)
- **Location:** Line 80, frame "A Question We Skipped"
- **Current:** "$Y_{}$ loaded from the bus at $T_1$..."
- **Proposed:** "$Y$ loaded from the bus at $T_1$..."
- **Category:** Typo — **Severity:** Medium
- **Rationale:** Leftover empty-subscript artifact, likely from a find/replace on `Y_{\text{...}}` patterns. Renders harmlessly but inconsistent with the adjacent `$Z$`.

## Issue 3: Notation-registry violation — missing brackets for register contents
- **Location:** Line 205, frame "Recall: We Wrote $T_1, T_2, T_3$ by Hand" (table, $T_2$ row)
- **Current:** "ALU adds $Y$; result $\to Z$"
- **Proposed:** "ALU adds $[Y]$; result $\to Z$"
- **Category:** Consistency (Notation) — **Severity:** Medium
- **Rationale:** Per the course notation registry, `[X]` denotes "contents of register X." The same row's RTL column already writes `$Z \gets [Y] + [R3]$`; the bare `$Y$` breaks that pattern within the same row.

## Issue 4: Terminology drift — "states" vs. the established term "control steps"
- **Location:** Lines 573, 575, frame "The Two Threads Meet"
- **Current:** "Single-bus: 3 states ($T_1, T_2, T_3$)..." / "Three-bus: 1 state..."
- **Proposed:** "Single-bus: 3 control steps..." / "Three-bus: 1 control step..."
- **Category:** Consistency (Terminology) — **Severity:** Medium
- **Rationale:** Every other occurrence in this deck and Week 5 calls $T_1,T_2,\dots$ a "control step," never a "state." Risks conflating with the deck's separately-defined term "state table."

## Issue 5: Inconsistent `\texttt{}` formatting of the running example instruction
- **Location:** Lines 64-65, frame "Roadmap: Three Questions, One Thread"
- **Current:** "\texttt{R1} $\gets$ \texttt{R2} + \texttt{R3}"
- **Proposed:** "\texttt{R1} $\gets$ \texttt{R2+R3}"
- **Category:** Consistency (Typography) — **Severity:** Low
- **Rationale:** Every other occurrence renders `R2+R3` as one `\texttt{}` block with no spaces; this instance splits it.

## Issue 6: Informal contraction, inconsistent with earlier formal phrasing of the same idea
- **Location:** Line 279, frame "Worked Trace Revisited: Where \texttt{SC} Points"
- **Current:** "...turns ``now it's $T_2$''..."
- **Proposed:** "...turns ``it is now $T_2$''..."
- **Category:** Academic Quality / Consistency — **Severity:** Low
- **Rationale:** Line 46 phrases the identical recurring idea formally as "it is now $T_2$"; matching the two would fix the contraction and reinforce the callback.

## Issue 7: Informal verb construction "OR'd"
- **Location:** Line 397, frame "From State Table to Boolean Equations"
- **Current:** "...its term gets \textbf{OR}'d into the same equation..."
- **Proposed:** "...its term gets \textbf{OR-ed} into the same equation..." (or "is combined into the same equation via OR")
- **Category:** Academic Quality — **Severity:** Low

## Issue 8: Potential overflow watch item — consolidated Boolean equation
- **Location:** Lines 412-414, frame "Worked Example: Deriving $Z_{\text{in}}$ by Hand"
- **Current:** `\[ Z_{\text{in}} = (D_{\text{ADD}} \cdot T_2) + (D_{\text{SUB}} \cdot T_2) = T_2 \cdot (D_{\text{ADD}} + D_{\text{SUB}}) \]`
- **Category:** Overflow — **Severity:** Low
- **Rationale:** Single longest inline display equation in the file — all others are one `D_i \cdot T_j` term per line. Worth a compile-time check for overfull hbox; if it overflows, break into an `align*` with the simplification on its own line.

---

## Positive notes
- Citation usage consistent; all 3 keys resolve correctly and are attached to matching source chapters.
- Core notation ($T_i$, `SC`, $SC_{\text{clear}}$, $D_i$, $X_{\text{in}}/X_{\text{out}}$, control matrix) consistent throughout except Issues 3-4.
- No overlay commands present.
- All TikZ diagrams use symmetric scaling; all boxed nodes declare explicit dimensions — no P1/P3 violations found by this pass (see the dedicated `tikz_review.md` for a full geometric audit, which found otherwise-hidden issues).
- Box usage stays within 1-2 per frame throughout.

**File reviewed:** `Slides/06-hardwired-control.tex`
**Bibliography cross-referenced:** `Bibliography_base.bib`
**Comparison file used for cross-lecture terminology check:** `Slides/05-addressing-cpu-bus.tex`
