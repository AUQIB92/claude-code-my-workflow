# Pedagogical Review: 06-hardwired-control.tex

**Date:** 2026-08-05
**Reviewer:** pedagogy-reviewer agent
**Target file:** `Slides/06-hardwired-control.tex` (613 lines, 27 frames, 5 sections, 4 `\transitionslide` pivots)
**Cross-referenced:** `.claude/rules/knowledge-base-template.md` (Week 6 notation registry), `.claude/rules/no-pause-beamer.md`, `Preambles/header.tex` (color/box semantics)

## Summary
- **Patterns followed:** 9/13
- **Patterns violated:** 0/13
- **Patterns partially applied:** 4/13
- **Deck-level assessment:** A strong, well-architected lecture. The narrative arc (Week 5's "gap we left open" → control-unit functions → SC/step-decoder → opcode decoder/state table/Boolean equations → trade-offs → bridge to Week 7) is explicit and self-referential. Notation matches the course knowledge base with zero drift. Pacing, transitions, and box discipline are all good-to-excellent. The main improvable areas are: visual-before-notation sequencing for the opcode decoder, one unresolved input ("Flags") introduced but never exercised in the worked example, and a slightly high proportion of slides carrying a colored box (though never more than the per-slide max).

## Pattern-by-Pattern Assessment

### Pattern 1: Motivation Before Formalism — Followed
Every formal definition is preceded by an explicit "why." "Where We Left Off" (31) + "The gap we left open" (44-49) motivate the control unit before "Definition: Control Unit" (90-102). "Recall: We Wrote $T_1,T_2,T_3$ by Hand" (198-214) motivates the Sequence Counter (216-248). "The Missing Piece: Opcode Decoding" (306-320) motivates $D_i$ before use. Even the Week 7 bridge is framed before naming microprogrammed control.

### Pattern 2: Incremental Notation — Partially Applied (Low)
Notation generally builds gradually. "Control Unit: Inputs and Outputs" (104-154) puts 8 distinct labeled elements on one diagram simultaneously before most are formally defined. Mitigated by being a black-box overview and by $X_{in}/X_{out}$ being unpacked on the very next slide. Consider trimming the diagram to only the signals used later.

### Pattern 3: Worked Example After Every Definition — Followed
Control unit definition → worked application within 2 slides. $SC$ definition → "Worked Trace Revisited" within 2 slides. $D_i$ definition → state table within 2 slides. Boolean-equation pattern → worked SUB derivation immediately after.

### Pattern 4: Progressive Complexity — Followed
Simple (single $T_i$ reused from Week 5) → relative (bus/control philosophies) → conditional/combinatorial ($D_i \cdot T_j$ AND/OR terms). Deck ends by explicitly connecting bus organization × control-step count on "The Two Threads Meet" (570-587).

### Pattern 5: Fragment Reveals for Problem → Solution — Partially Applied (informational)
Zero `\pause`/overlay usage — correctly compliant with `no-pause-beamer.md`. Problem→solution pacing achieved instead via 4 `\transitionslide` cliffhangers + 5 in-frame Socratic Q&A blocks. Correct adaptation given the project's overlay ban; not a defect.

### Pattern 6: Standout Slides at Conceptual Pivots — Followed
4 `\transitionslide` calls at every major pivot, spacing 3/5/5/8 slides — within or at the edge of the 5-8 guideline.

### Pattern 7: Two-Slide Strategy for Dense Theorems — Partially Applied (Low-Medium)
The core "theorem" (state table → Boolean equations, 365-417) is handled exemplarily across three slides. However, the capstone "Full Hardwired Control Unit Block Diagram" (455-502) has no dedicated unpacking slide — the next frame is a Socratic check, not a walkthrough. A one-sentence captioned walkthrough of the feedback loop would reduce cognitive load on this densest visual.

### Pattern 8: Semantic Color Usage — Followed
Confirmed against `header.tex`: `positive`/`negative` map correctly to `\good{}`/`\bad{}`. TikZ diagrams use consistent `primary-blue` (inputs/state), `primary-gold` (decoders/gates), `positive` (outputs) across all four diagrams — no drift in color-to-role mapping.

### Pattern 9: Box Hierarchy — Followed
`block`/`exampleblock`/`alertblock` applied correctly per their semantic roles throughout.

### Pattern 10: Box Fatigue (Per-Slide) — Followed
No slide exceeds 2 colored boxes; maximum observed is 2.

### Pattern 11: Socratic Embedding — Followed (exceeds target)
9 distinct dialogic moments (5 Socratic blocks + 4 transition cliffhangers) across 27 frames vs. the 2-3/lecture target — a strength.

### Pattern 12: Visual-First for Complex Concepts — Partially Applied (Medium)
Two violations of "diagram before notation": (1) "Definition: Control Unit" (90-102, prose-only) precedes its I/O diagram (104-154). (2) More significantly, $D_i$ is fully defined in text on "The Missing Piece: Opcode Decoding" (306-320) a full slide before the "Two Decoders Feed the Control Matrix" diagram (322-363) that visualizes it. Recommend previewing the two-decoder diagram alongside/before the textual $D_i$ definition.

### Pattern 13: Two-Column Definition Comparisons — Followed
"Two Philosophies for Building a Control Unit" (175-189) and $X_{in}/X_{out}$ (156-164) are each handled as single-slide bulleted comparisons, achieving the goal without page-turning. Optional polish: a literal two-column layout on "Two Philosophies" would visually reinforce the Hardwired | Microprogrammed parallel.

## Deck-Level Analysis

### Narrative Arc
Excellent — one of the strongest examples of full-circle narrative structure in the course. Opens by naming an explicit unresolved gap from Week 5, states a three-question roadmap that maps exactly onto the deck's three body sections, and closes with two synthesis moves reconnecting Week 5's bus-organization choice to Week 6's control-step count before handing off cleanly to Week 7.

### Pacing
Good — no run of more than 2 consecutive theory-dense slides without an intervening diagram, worked example, or Socratic check. Table-based recap slides function as useful low-cognitive-load checkpoints.

### Visual Rhythm
Transition slides land at intervals of 3, 5, 5, and 8 content slides — within/at the edge of the 5-8 guideline. Diagram-heavy slides are well distributed rather than clustered.

### Box Fatigue (Deck-Level)
Per-slide discipline is excellent, but ~68% of content frames (17/25) carry at least one colored box — above the informal ~50% guideline, though never a per-slide violation. No `resultbox`/`highlightbox`/`keybox` environments used at all.

### Notation Consistency
Fully consistent with the course knowledge base. $T_i$ explicitly flagged as reused from Week 5 rather than reintroduced. $SC$, $X_{in}/X_{out}$, $D_i$, "control matrix" all match KB definitions and are correctly marked "new" for Week 6.

### Student Concerns
Trade-offs (526-539) and "Where This Breaks Down" (541-552) directly acknowledge hardwired control's rigidity as a real cost. Two loose threads: (1) Flags (Z,N,C,V) introduced as a CU input (104-154) but never exercised — the running ADD example never branches. (2) ALU function select and Memory Read/Write listed as CU outputs but the worked example only uses ALU=add and never touches memory. Neither is flagged as a deliberate scope limitation.

## Critical Recommendations (Top 3-5)
1. **(Medium)** Preview the two-decoder diagram (322-363) before/alongside the textual $D_i$ definition (306-320), per Pattern 12.
2. **(Medium)** Add a one-sentence acknowledgment that Flags and Memory Read/Write, though listed as CU inputs/outputs, aren't exercised by this lecture's register-only running example.
3. **(Low-Medium)** Add a brief captioned walkthrough sentence under the capstone block diagram (455-502) pointing out the feedback loop ($SC_{clear}$ → SC).
4. **(Low)** Consider a literal two-column layout for "Two Philosophies for Building a Control Unit" (175-189).
5. **(Low, informational)** This deck substitutes `\transitionslide` cliffhangers + Socratic blocks for "fragment reveal" — the correct adaptation given `no-pause-beamer.md`; don't flag as a Pattern 5 violation in future automated scoring.

**Files reviewed:** `Slides/06-hardwired-control.tex`
**Cross-referenced:** `.claude/rules/knowledge-base-template.md`, `.claude/rules/no-pause-beamer.md`, `Preambles/header.tex`
