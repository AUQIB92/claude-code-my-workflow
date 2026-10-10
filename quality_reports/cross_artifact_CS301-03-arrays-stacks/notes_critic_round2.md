# Notes vs Beamer Parity Audit: CS301/03-arrays-stacks

**Beamer source:** `Slides/CS301/03-arrays-stacks.tex` (43 frames)
**Notes:** `Notes/CS301/03-arrays-stacks-notes.tex`
**Round:** 2  **Date:** 2026-09-02

## Verdict: APPROVED

Full frame-by-frame re-walk (not a spot-check of the round-1 deltas) confirms all three round-1 fixes (C1, M1, m2, m3) were applied cleanly with no new fabrication, no new missing content, and no citation/notation drift. One new cosmetic issue was introduced by the m2 fix (sentence redundancy) and one previously-flagged optional item (m1) was left unchanged as instructed — both are Minor and within the ≤3-minor APPROVED threshold.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 43 Beamer frames re-traced individually to a matching Notes section/example/figure; no gaps found beyond round 1's original finding set. |
| No invention | Pass | C1's fabricated citation clause is gone — Figure 3.1's caption (Notes lines 206–210) now ends at "...follows the same one-line formula." with no citation, matching frame 10's uncited status. No new fabricated claims or citations found anywhere else in a fresh full read. |
| Citation parity | Pass | Identical 4-key set in both files (`HorowitzSahni2008_fundamentals_data_structures`, `AhoHopcroftUllman1983_data_structures_algorithms`, `Sedgewick2011_algorithms`, `Karumanchi2017_data_structures_algorithms_made_easy`). Notes' additional "Read alongside" reading-guidance blocks (§3.1, §3.2, §3.3.1 openers) reuse the same keys already cited by frames later in each section — not new sources, a legitimate expansion per the file's own "reading guidance per section" Detail Bar. |
| Notation fidelity | Pass | `base`, `w`, `i`, `j`, `r`, `c`, `n`, `top`, `capacity`, `addr(A[i])`, `addr(A[i][j])`, `T(n)`, `O/Ω/Θ` all appear identically; no drift. |
| Textbook-page honesty | Pass | Only page-verified anchor used is Sedgewick2011 p.120 (Stack ADT frame), matching Beamer exactly and matching `knowledge-base-CS301.md`'s confirmed anchor. Karumanchi2017 stays chapter-level (Ch.4, pp.163–204) throughout — no invented per-claim page number despite the KB noting Karumanchi has page-verified anchors "throughout"; the Notes correctly does not round that up to individual-claim page citation. Horowitz & Sahni / Aho-Hopcroft-Ullman stay chapter-level only, consistent with the KB's explicit instruction that these two must never get page numbers. |

## Round-1 Fix Verification

| Fix | Verified Location | Status |
|---|---|---|
| C1 (fabricated citation on Fig. 3.1 caption) | Notes lines 206–210 | **Clean** — clause deleted, caption now uncited, matches frame 10 |
| M1 (unhedged "overflow disappears" claim) | Notes lines 850–853 ("Looking further ahead" paragraph) | **Clean** — now phrased as a question ("is stack overflow therefore a failure mode that survives the switch, or one that disappears?"), consistent with sibling Q1 treatment |
| m2 (missing "two structures down" transition echo) | Notes §3.4 opening, lines 810–813 | **Applied, but introduces a new cosmetic issue** — see Minor finding m1 below |
| m3 (Exercise 2(c) "correct" clarification) | Notes Solutions §, item 2(c), lines 916–919 | **Clean** — clarifying sentence added exactly as instructed, arithmetic re-verified correct |
| m1 (postfix "backwards" elaboration, left unchanged) | Notes lines 759–760 | **Still present, still acceptable** — see note below |

**On m1 being left unchanged:** re-confirmed independently. "Getting this order backwards silently computes $b - a$ where $a - b$ was intended, for a non-commutative operator such as subtraction or division" is a direct, correct, low-risk logical consequence of the algorithm stated one sentence earlier in the same frame (frame 36's "the operand popped first is the right operand — it was pushed last"). It does not introduce a new fact, textbook claim, or citation. Leaving it unchanged remains defensible; round 1 correctly marked it fully optional.

## Critical Issues (MUST FIX)

None.

## Major Issues (SHOULD FIX)

None.

## Minor Issues (NICE TO FIX)

### m1 (new this round): Sentence redundancy introduced by the m2 fix in §3.4
- **Beamer frame:** Transition slide (line 717): "Two structures down. Time to consolidate before Week 4 converts infix to postfix."
- **Notes:** §3.4 opening (lines 810–813) now reads: *"Two structures are now in place --- the array and the stack built on top of it --- so before moving to Week 4's infix-to-postfix conversion, it is worth naming the mistakes that recur most often with this material. Three mistakes recur often enough with this material to name explicitly."* The newly-inserted sentence and the pre-existing sentence both assert essentially the same thing ("mistakes that recur most often" / "mistakes recur often enough ... to name explicitly"), producing a redundant, mechanically-stitched-together pair rather than one clean transition sentence.
- **Fix:** Merge into one sentence, e.g.: "Two structures are now in place --- the array and the stack built on top of it --- so before moving to Week 4's infix-to-postfix conversion, it is worth naming the three mistakes that recur most often with this material." Delete the now-redundant second sentence.

### m2 (carried forward, still optional per round 1): Postfix "backwards" elaboration not literally in frame 36
- No change needed; see verification note above. Retained here only for completeness/traceability of the round-1 finding set.

### m3 (new, very low risk): "malloc and allocation sizes" adds unstated specificity
- **Beamer frame:** Frame 7, "What an Array Really Is": "Every slot has the same size $w$ (in bytes) --- \texttt{sizeof} the element type, a notion already familiar from Week 1."
- **Notes:** §3.1.1 (lines 127–130): "...this is exactly the \texttt{sizeof} the element type, a notion already familiar from Week 1's discussion of \texttt{malloc} and allocation sizes." The parenthetical "malloc and allocation sizes" is not stated in frame 7 itself, though it is a correct, low-risk pointer to Week 1 content per `knowledge-base-CS301.md`'s Symbol Reference (`malloc`/`sizeof` both listed as Week 1 (new)).
- **Fix:** Optional. If tightened, revert to "a notion already familiar from Week 1" without the added specificity, or keep as-is — this is not a fabrication risk, just an unnecessary embellishment.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 43 |
| Notes sections | 5 numbered sections (3.1–3.5 topics, rendered as §3.1–3.4 + unnumbered Exercises/Solutions/Summary), ~25 subsections |
| Citation keys: Beamer / Notes | 4 / 4 (identical key set; 0 invented citation instances — C1 resolved) |
| Critical / Major / Minor | 0 / 0 / 3 (1 new cosmetic, 1 carried-forward-and-reaffirmed-optional, 1 new very-low-risk) |

## Notes on strengths (unchanged from round 1, reaffirmed)

Every worked example's arithmetic was independently re-verified in this round (Examples ex:a4, ex:two-orders, ex:predict-order, ex:push, ex:pop, ex:stack-trace, ex:balance-algo/trace/fail, ex:postfix-algo/trace, and all 5 end-of-chapter Exercise solutions including the non-trivial Exercise 5 diagonal/non-square-array proof) — all correct. All four transition slides are now echoed as full connective sentences at their corresponding section boundaries. All five TikZ diagrams are narrated from their coordinate-map comments rather than "see figure." No section is thinner than its source frame(s) warrant.
