# Notes vs Beamer Parity Audit: CS301/03-arrays-stacks

**Beamer source:** `Slides/CS301/03-arrays-stacks.tex` (43 frames)
**Notes:** `Notes/CS301/03-arrays-stacks-notes.tex`
**Round:** 1  **Date:** 2026-09-02

## Verdict: REJECTED

Hard-gate failure on **No invention** — a single fabricated citation attachment (Finding C1). The rest of the document is unusually strong (see Summary), and the fix is a one-line deletion, so this should clear to APPROVED or NEEDS REVISION (minor only) in round 2 once C1 and M1 are addressed.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 43 Beamer frames trace to a Notes section (walked frame-by-frame; only the transition-slide framing at frame 39 is thinner than ideal — Minor, not a parity failure). |
| No invention | **Fail** | Figure 3.1's caption (Notes line 210) attaches `\cite{HorowitzSahni2008_fundamentals_data_structures}` to the 1D-address diagram, but the corresponding Beamer frame ("Picture: the 1D Address Formula," frame 10) carries **no citation at all** — see C1. |
| Citation parity | Pass | Both files use the identical 4-key set: `HorowitzSahni2008_fundamentals_data_structures`, `AhoHopcroftUllman1983_data_structures_algorithms`, `Sedgewick2011_algorithms`, `Karumanchi2017_data_structures_algorithms_made_easy`. No key is missing or renamed. |
| Notation fidelity | Pass | `base`, `w`, `i`, `j`, `r`, `c`, `addr(A[i])`, `addr(A[i][j])`, `top`, `capacity`, `T(n)`, `O/Ω/Θ`, `n` all appear identically in both files; no symbol renaming or subscript drift found. |
| Textbook-page honesty | Pass | Only page-verified anchor used is Sedgewick2011 p.120 (Stack ADT definition, Notes §3.3.2), matching the Beamer frame exactly. Karumanchi2017 stays chapter-level (Ch.4, pp.163–204) in both files. Horowitz & Sahni / Aho-Hopcroft-Ullman stay chapter-level, no invented page numbers anywhere in the Notes. |

## Critical Issues (MUST FIX)

### C1: Invented citation on Figure 3.1's caption
- **Beamer frame:** Frame 10, "Picture: the 1D Address Formula" (lines 149–178). This frame is pure diagram + two bullet points; it carries **zero** `\cite{}` commands. (Frame 8, "The 1D Address Formula," which the diagram illustrates, is likewise uncited.)
- **Notes:** `Notes/CS301/03-arrays-stacks-notes.tex`, Figure 3.1 caption (lines 206–211): "...every other slot's address follows the same one-line formula --- general/standard treatment, cf.\ Horowitz \& Sahni Ch.~2--3 \cite{HorowitzSahni2008_fundamentals_data_structures}." This is the only place in the entire Notes file where a citation is attached to content whose source frame has none — it directly contradicts the Notes' own stated policy in its header comment: "citation presence and absence are preserved 1:1 with the Beamer source, frame by frame."
- **Fix:** Delete the "--- general/standard treatment, cf.\ Horowitz \& Sahni Ch.~2--3 \cite{HorowitzSahni2008_fundamentals_data_structures}" clause from the Figure 3.1 caption. The caption should end at "...follows the same one-line formula." (matching the uncited status of frames 8 and 10).

## Major Issues (SHOULD FIX)

### M1: "Before You Go: Predict" over-answers Question 2 instead of leaving it forward-looking
- **Beamer frame:** Frame 42, "Before You Go: Predict" (lines 756–771). Three genuinely open Socratic questions about the Week 7 linked-list stack implementation: (1) which operation gets more expensive, (2) "Which problem — overflow, or something else — does a linked list implementation remove entirely?", (3) does the ADT contract change. No answers are given in the Beamer deck; question 3 gets only a hint ("revisit 'Naming the ADT, Naming the Implementation'").
- **Notes:** "Looking further ahead..." paragraph near the end of Section 3.5. The Notes correctly (a) defers Q1 explicitly ("a question this chapter's tools do not yet answer... deliberately left as a prediction to test"), and (b) answers Q3 via a defensible inference from the deck's own ADT/implementation-separation argument (echoing the Beamer's own hint). But for Q2 it states a **definitive, unhedged answer**: "A linked-list implementation, having no fixed capacity to exhaust, removes stack overflow as a possibility... stack underflow remains." This resolves a question the Beamer deck deliberately poses as an unanswered self-test to be worked out only after Week 7's material is taught. It is not fabricating a false fact (the claim is correct), but it does convert a "Predict" frame's open question into a stated conclusion, which is inconsistent with how the Notes correctly handles Q1, and pre-empts a forward-looking pedagogical device the deck intentionally leaves for the student.
- **Fix:** Reframe the overflow claim as a hypothesis/question rather than an assertion — e.g., "A linked-list implementation has no fixed capacity to exhaust in the way an array does; is stack overflow therefore a failure mode that survives the switch, or one that disappears? Underflow, by contrast, is a property of the empty stack itself, independent of implementation — does that same reasoning apply to it?" This keeps the section "forward-looking narrative" for all three questions, matching the treatment already given to Q1.

## Minor Issues (NICE TO FIX)

### m1: Postfix example adds an illustrative claim not present in its source frame
- **Beamer frame:** Frame 36, "Postfix Evaluation Algorithm". States only: "Order matters: the operand popped first is the right operand --- it was pushed last."
- **Notes:** Example (postfix evaluation algorithm) adds: "Getting this order backwards silently computes $b - a$ where $a - b$ was intended, for a non-commutative operator such as subtraction or division." This is a correct, low-risk elaboration directly implied by the stated algorithm (legitimate "derivation completeness" expansion, not a fabricated fact), but it is not literally traceable to frame 36's text. Acceptable as expansion; flagging only so it's attributed as Notes-added elaboration rather than silently presented as if from the deck.
- **Fix:** Optional — no change required, or add a soft attribution phrase ("a direct consequence of this ordering rule is that...") to make clear this is elaboration rather than restated slide content.

### m2: Transition-slide 39's explicit "two structures down" framing is not echoed
- **Beamer frame:** Frame 39 (transition slide): "Two structures down. Time to consolidate before Week 4 converts infix to postfix."
- **Notes:** Section 3.5 ("Common Mistakes and What Comes Next") opens directly with "Three mistakes recur often enough..." — the consolidative function is present (mistakes + summary + next-week preview all follow), but the specific "two structures completed so far" framing from the transition slide isn't stated anywhere in the section's prose.
- **Fix:** Add one sentence opening §3.5, e.g., "Two structures are now in place — the array and the stack built on top of it — so before moving to Week 4's infix-to-postfix conversion, it is worth naming the mistakes that recur most often with this material."

### m3: Exercise 2(c) solution relies on an unstated interpretation of "leaves the final top correct"
- **Beamer frame:** Frame 28, "Check Your Prediction" (stack trace), question 3: "Which single operation, if it were removed... would still leave the final `top` correct but change the returned value of `peek()`?"
- **Notes:** Solution to Exercise 2 works through all four non-`peek` removals and concludes `push(3)` is unique. Checking the arithmetic: removing any of `push(5)`, `push(8)`, or `pop()` yields final `top = 0`, `0`, or `2` respectively (not the original sequence's `top = 1`), so "correct" cannot mean "numerically identical to the original." The Notes' resolution implicitly interprets "correct" as "the sequence still executes without underflow" rather than "matches the original numeric value" — a reasonable reading, but it is never stated explicitly before the four cases are worked, which could read as if all four candidates literally reproduced `top=1` (they don't).
- **Fix:** Add one clarifying sentence before the four-case walk-through: "Here 'correct' means the sequence still executes validly (no underflow) and produces some legitimate final `top`, not that the numeric value of `top` must match the original trace's `top=1`."

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 43 |
| Notes sections | 5 numbered sections (3.1–3.5), ~25 subsections, plus Exercises (5 problems) / Solutions / Summary appendix |
| Citation keys: Beamer / Notes | 4 / 4 (identical key set; 1 extra, unsourced citation *instance* in Notes — see C1) |
| Critical / Major / Minor | 1 / 1 / 3 |

## Notes on strengths (for calibration)

This is a well-constructed expansion, not a padded restatement: every worked example is carried through full arithmetic, every TikZ diagram is narrated in prose tied to its caption rather than "see figure," transition-slide one-liners are folded into full connective sentences, the chapter-style `3.x` section/figure/example numbering and `definitionbox` environment comply with the Notes-specific conventions in `single-source-of-truth.md`, and the two Socratic "Check Your Prediction" frames (array-indexing and five-operation stack trace) are resolved using only formulas/algorithms the Beamer deck itself already supplies — verified independently.
