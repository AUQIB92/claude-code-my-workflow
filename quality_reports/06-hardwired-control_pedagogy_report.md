# Pedagogical Review: 06-hardwired-control.tex

**Date:** 2026-08-07
**Reviewer:** pedagogy-reviewer agent
**Status:** Review complete; **all 5 critical recommendations applied** (2026-08-07). Box density 68% → 58%; SC-sizing + `I` flip-flop inconsistencies resolved; two-column tables added; alertblock hierarchy tightened. Remaining boxes are semantic (definitions / questions / worked examples).

## Summary

- **Patterns followed:** 11/13
- **Patterns violated:** 0/13
- **Patterns partially applied:** 2/13 (P9 Box Hierarchy, P13 Two-Column Comparisons)
- **Deck-level assessment:** A strong, well-motivated Week-6 deck that leverages Week 5's single-bus trace as a running example and carries a clear problem→solution arc through the sequence counter, opcode decoder, and control matrix. The main weaknesses are an internal inconsistency in how large SC is presented (4-bit counter vs. 2-bit statement), an overloaded `block`/`alertblock` box hierarchy, and deck-level box density above the 50% guideline. One notation symbol (`I` flip-flop) appears in a diagram with only a passing mention.

## Pattern-by-Pattern Assessment

### Pattern 1: Motivation Before Formalism
- **Status:** Followed
- **Evidence:** Every new construct is preceded by a "why". The deck opens by framing the entire lecture as the gap Week 5 left open ("The gap we left open", lines 60-65) and a three-question roadmap (lines 68-77). The control unit is motivated by "A Question We Skipped" (lines 94-104) before its "Definition" (lines 106-118). SC is motivated by the Socratic block on the recall table (lines 227-230) before "The Sequence Counter (SC)" (lines 233-276). The opcode decoder is motivated by "The Missing Piece: Opcode Decoding" (lines 334-348) before the control matrix.
- **Recommendation:** None — this is the deck's greatest strength.
- **Severity:** Low

### Pattern 2: Incremental Notation
- **Status:** Followed (one Low note)
- **Evidence:** New symbols are introduced one per frame, each with a dedicated block: `X_in`/`X_out` (lines 173-190, explicitly "added to the course registry", mirroring Week 5's RTL-registry frame at 05-addressing-cpu-bus.tex:362), `SC` (lines 233-276), `D_i` (lines 342-347). `SC_clear` is introduced within "How SC Advances" (line 283) right where it is used. No slide dumps 5+ symbols.
- **Recommendation:** The `I` flip-flop appears as a bare "$I$" node in the "Two Decoders Feed the Control Matrix" diagram (line 380) with only a passing prose mention ("the $I$ flip-flop ... for indirect-addressing-sensitive signals", line 403). Give it one explicit sentence (tie it to Week 5's indirect addressing / bit 15) on or immediately before that frame so students meet it before the diagram.
- **Severity:** Low

### Pattern 3: Worked Example After Every Definition
- **Status:** Followed
- **Evidence:** `SC` definition (line 233) is followed one frame later by the worked exampleblock "Applied to our trace" (lines 288-291) and the "Worked Trace Revisited" table (lines 294-309). `D_i` definition (lines 342-347) is applied in "Building the State Table" (lines 409-427). The state table is immediately turned into derivations ("From State Table to Boolean Equations", lines 429-443) and a full worked example ("Worked Example: Deriving $Z_{in}$ by Hand", lines 445-461). No two consecutive definition-only frames exist.
- **Recommendation:** None.
- **Severity:** Low

### Pattern 4: Progressive Complexity
- **Status:** Followed
- **Evidence:** Clean ordering: recap → control-unit role (Act 1) → generating the step sequence / SC (Act 2) → opcode decoding and the control matrix (Act 3) → trade-offs and the Week-7 bridge (Act 4). Within Act 3 the ladder is explicit: one opcode line (`D_ADD`) → one signal's equation → two instructions OR'd into one equation → physical AND-OR gates (lines 429-501).
- **Recommendation:** None.
- **Severity:** Low

### Pattern 5: Fragment Reveals for Problem → Solution
- **Status:** Followed
- **Evidence:** The conceptual equivalent is strong and is the deck's spine. Problem → solution pairs: "A Question We Skipped" (lines 94-104) → control unit; "What physical component keeps track of 'which step we are on'?" (lines 227-230) → SC revealed on the next frame; "SC alone cannot know which instruction is running" (lines 335-340) → `D_i`; and two Socratic Checks that pose-then-answer within a frame ("What Happens After $T_3$?", lines 311-325; "Adding a New Instruction", lines 559-572). The four transition slides (lines 87, 208, 327, 574) are phrased as questions, funneling the student forward.
- **Recommendation:** None.
- **Severity:** Low

### Pattern 6: Standout Slides at Conceptual Pivots
- **Status:** Followed
- **Evidence:** Four `\transitionslide` frames mark every major break: recap→Act 1 (line 87), Act 1→2 (line 208), Act 2→3 (line 327), Act 3→4 (line 574). Section lengths between dividers are 5, 5, 8, and 5 frames — within the 5-8 guidance, with Act 3 at the upper bound.
- **Recommendation:** None.
- **Severity:** Low

### Pattern 7: Two-Slide Strategy for Dense Theorems
- **Status:** Followed
- **Evidence:** The densest material — the state table → Boolean equations → gate realization — is decomposed across three frames rather than crammed into one: state table (lines 409-427), equations (lines 429-443), worked derivation of $Z_{in}$ (lines 445-461), and the AND-OR gate diagram (lines 463-501).
- **Recommendation:** None.
- **Severity:** Low

### Pattern 8: Semantic Color Usage
- **Status:** Followed
- **Evidence:** `\good{Pro}` / `\bad{Con}` carry the semantic positive/negative contrast on the trade-offs frame (lines 584-590) — one binary contrast in one frame, correctly differentiated by color, not overloaded. `\muted{}` de-emphasizes the caption on the gate diagram (lines 499-500). `\key{}` is used consistently for term labels.
- **Recommendation:** None.
- **Severity:** Low

### Pattern 9: Box Hierarchy
- **Status:** Partially Applied
- **Evidence:** The mapping between box type and purpose is loose. `block` does triple duty: definitions ("Control unit", line 107; `X_in`/`X_out`, line 174; `SC`, line 234), Socratic questions (lines 95, 227, 335), and recap content ("Where We Left Off", line 48). `alertblock` is used both for genuine questions (lines 311-315, 559-563) and for pure emphasis that is not an alert: "Running thread for today" (lines 79-84) and "This week vs. next week" (lines 201-205). `exampleblock` covers worked examples (lines 288, 421) but also the motivational bridge to Week 7 (line 610).
- **Recommendation:** Reserve `block` for definitions, `alertblock` strictly for Socratic questions/warnings, and move the two emphasis alertblocks (lines 79, 201) to `exampleblock` or plain emphasized text so a student can read a box's type and predict its content.
- **Severity:** Medium

### Pattern 10: Box Fatigue (Per-Slide)
- **Status:** Followed
- **Evidence:** Maximum is two colored boxes on a single slide ("Where We Left Off", lines 48-65, has one `block` + one `exampleblock`). Every other boxed slide carries exactly one. No slide reaches the 3-box red flag.
- **Recommendation:** None per-slide (see deck-level box-fatigue finding below).
- **Severity:** Low

### Pattern 11: Socratic Embedding
- **Status:** Followed
- **Evidence:** Five explicit Socratic/Check questions (lines 95, 227, 311, 335, 559) plus four question-phrased transition slides (lines 87, 208, 327, 574) — comfortably above the 2-3 target, and each question is answered (either on the same frame or the next).
- **Recommendation:** None. If anything, this slightly exceeds the target, but the density is justified by the topic's difficulty.
- **Severity:** Low

### Pattern 12: Visual-First for Complex Concepts
- **Status:** Followed
- **Evidence:** Diagrams lead or accompany the formalism precisely where the concept is spatial/hardware: CU I/O contract immediately after the (simple) definition (lines 120-171), SC + step decoder on the definition frame itself (lines 240-273), and — most importantly — the "Two Decoders Feed the Control Matrix" diagram (lines 350-407) comes *before* the state table and equations, giving students the map before the algebra. The AND-OR realization (lines 463-501) and full block diagram (lines 503-557) close the arc.
- **Recommendation:** None.
- **Severity:** Low

### Pattern 13: Two-Column Definition Comparisons
- **Status:** Partially Applied
- **Evidence:** Two comparisons that are clearly "the point" are co-located on single slides (good — not split across consecutive frames) but rendered as bullet lists rather than true two-column tables: hardwired vs. microprogrammed (lines 192-206) and single-bus vs. three-bus (lines 625-642, "The Two Threads Meet"). The trade-offs frame (lines 581-594) is also bullets with `\good`/`\bad`.
- **Recommendation:** Convert "Two Philosophies" (line 192) and "The Two Threads Meet" (line 625) to tabular two-column layouts (attribute rows: speed, change-ability, gate count, cycles) so students compare attributes directly rather than mentally reconstructing a table from bullets.
- **Severity:** Low-Medium

## Deck-Level Analysis

### Narrative Arc
Excellent. The deck opens by naming the precise gap from Week 5 — "Nothing in the hardware yet decides 'it is now $T_2$'" (lines 60-65) — and closes by fully closing it: the Summary (lines 644-660) restates the control unit's role and the Week-7 bridge, and "The Two Threads Meet" (lines 625-642) ties the control-unit size back to Week 5's datapath choice. The running thread (`R1 <- R2+R3` on the single-bus datapath) is stated in the Roadmap (lines 79-84) and reused verbatim in every act, so the story is one continuous question answered in three parts.

### Pacing
Strong. Theory is always capped at ~2 consecutive slides before a worked example, table, or diagram breather. The one theory-dense run is Act 3 frames "Building the State Table" (409) → "From State Table to Boolean Equations" (429) → "Worked Example: Deriving $Z_{in}$" (445), but the middle frame is a direct, nearly self-evident transcription of the table, so the run reads as two easy steps into a worked example, not three walls of formalism. Act 3 is the longest (8 frames between transitions), which is at the upper bound but acceptable given every second frame is a diagram.

### Visual Rhythm
Good. Four transition slides mark the acts; five TikZ diagrams (CU I/O, SC+decoder, two-decoder+matrix, AND-OR gates, full block diagram) are distributed one per dense stretch rather than clustered. The flow alternates text → diagram → table → diagram consistently.

**Deck-level box fatigue is the one flag:** 17 of 25 content frames (68%) carry a colored box, exceeding the ≤50% guideline. The per-slide rule is respected (never 3+), but the *frequency* is high, especially in Act 0-1 where blocks appear on 6 of the first 7 frames. No `resultbox` is used (0, within the ≤3 cap).

### Notation Consistency
Week 5's established notation is preserved 1:1 — RTL transfers (`Y <- [R2]`, `Z <- [Y]+[R3]`, `R1 <- [Z]`) appear verbatim in the Week-6 tables (lines 221-223, 415-417) matching 05-addressing-cpu-bus.tex:477-479; `T_1/T_2/T_3`, `EA`, `M[EA]`, Y/Z buffers all carry over unchanged. New symbols (`X_in`/`X_out`, `SC`, `D_i`) each get a dedicated notation frame, and `X_in`/`X_out` is explicitly registered to the course registry like Week 5's RTL block.

**One genuine internal inconsistency:** "The Sequence Counter" frame presents a **4-bit counter** feeding a **4×16 decoder** producing **`T1..T16`** (diagram at lines 255-272), while "The Two Threads Meet" states the single-bus trace needs **SC with 2 bits and a step decoder with 3 outputs** (lines 628-629). The worked trace table uses SC values 0,1,2 (lines 300-302), which is consistent with the minimal sizing, not the 4-bit diagram. The source comments explain the 4-bit choice as a Mano Fig. 5-6 mapping (lines 243-249), but a student sees "4-bit counter" and "SC needs 2 bits" and will ask why. Reconcile by either (a) labeling the diagram's 4-bit/16-output version as "the general ISA case" with `SC_clear` at count 2 making `T3` the last used state, or (b) drawing the minimal 2-bit/3-output version for the worked trace.

### Student Concerns
Largely well pre-empted: the "what if `SC_clear` is forgotten" scenario is explicitly asked and answered (lines 311-325); "Where This Breaks Down" (lines 596-607) acknowledges the worked example is a toy ISA and states the verification-cost explosion honestly; the single-bus assumption is declared up front (lines 79-84); the trade-offs frame explicitly names what you lose (rewiring, gate growth). Remaining gaps: the `I` flip-flop is never formally introduced before appearing in a diagram (see P2), and the 4-bit-vs-2-bit SC sizing invites exactly the kind of "wait, why 16 states?" objection that the deck otherwise anticipates so well.

## Critical Recommendations (Top 3-5)

1. **Reconcile the SC sizing inconsistency.** "The Sequence Counter" diagram (lines 255-272) shows a 4-bit counter / 4×16 decoder / `T1..T16`, but "The Two Threads Meet" (lines 628-629) says the trace needs SC with 2 bits and a decoder with 3 outputs. Present the diagram as the general ISA-sized version with `SC_clear` at count 2 (or draw the minimal 2-bit version), and say so in one line of student-visible text so the two frames agree.
2. **Introduce the `I` flip-flop explicitly before the control-matrix diagram.** It appears as a bare `$I$` node (line 380) with only a passing prose mention (line 403). Add one explicit sentence (bit 15, indirect addressing from Week 5, feeds the matrix for indirect-sensitive signals) so the symbol is met before the diagram, not inside it.
3. **Tighten the box hierarchy.** `block` currently serves definitions, Socratic questions, and recaps; `alertblock` serves both questions and non-alert emphasis ("Running thread", line 79; "This week vs. next week", line 201). Reserve `alertblock` for questions/warnings and move the two emphasis alertblocks to `exampleblock` or plain text so box type reliably predicts content.
4. **Reduce deck-level box density (68% of content frames boxed, above the 50% guideline).** Convert the non-semantic boxes — e.g., the recap `block` on "Where We Left Off" (lines 48-58) and the Roadmap alertblock (lines 79-84) — to unboxed emphasized text, keeping boxes only where they signal definition / question / worked-example.
5. **Use true two-column layouts for the two comparisons.** Convert "Two Philosophies for Building a Control Unit" (line 192) and "The Two Threads Meet" (line 625) from bullet lists into attribute-by-row tables (speed, change-ability, gate/circuit cost, cycles) so the hardwired-vs-microprogrammed and single-bus-vs-three-bus contrasts are visible at a glance.
