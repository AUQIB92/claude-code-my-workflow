# Algorithm Verification: CS301 Week 3 Coding Assignment (P1 + P2)

**Date:** 2026-09-02
**Artifact:** `Assignments/CS301/03-arrays-stacks-coding-assignment.tex` (problem statement) +
`Assignments/CS301/03-arrays-stacks-coding/{p1,p2}_reference_solution.c`
**Language:** C

## Summary — P1 (`is_balanced`, balanced-bracket check)

| Check | Result |
|---|---|
| Correctness (67 hidden checks: worked examples, boundaries, structure-specific adversarial cases, 40 random inputs vs. hand-written oracle) | PASS: 67  FAIL: 0 |
| Correctness (5 visible checks) | PASS: 5  FAIL: 0 |
| Worked example in artifact | PASS |
| Complexity claim | O(n), n = length of `expr` |
| Empirical growth | CONSISTENT (measured slope ≈ 0.79 on a log(time) vs. log(n) fit, n ∈ {50,100,200,400,500}) |
| **Overall verdict** | **PASS** |

## Summary — P2 (`eval_postfix`, postfix evaluation)

| Check | Result |
|---|---|
| Correctness (45 hidden checks: worked examples, boundaries, all four operators, negative results, multi-digit operands, a capacity-stress sum-of-1..20 case, 25 random valid postfix expressions vs. independent strtok-based oracle) | PASS: 45  FAIL: 0 |
| Correctness (4 visible checks) | PASS: 4  FAIL: 0 |
| Worked example in artifact | PASS |
| Complexity claim | O(n), n = number of tokens |
| Empirical growth | CONSISTENT (measured slope ≈ 1.19 on a log(time) vs. log(n) fit, tokens ∈ {9,19,39,69,99}) |
| **Overall verdict** | **PASS** |

## Correctness — FAIL cases (BLOCKER)

None. 0 of 121 total checks (67+5 for P1, 45+4 for P2) failed.

## Translation decisions

- **P1:** bracket-type matching implemented as a small table function (`matches_opener`) rather than a chain of `if/else` per type — a design choice, not an ambiguity in the lecture's algorithm (the lecture's own pseudocode already generalizes cleanly from one bracket type to three; the *extension* to three types was the assignment's own addition, spelled out explicitly in the problem statement rather than left implicit).
- **P2:** tokenizer implemented by hand (`isdigit`/`isspace`-style manual scan) rather than `strtok`, so parsing decisions (single space between tokens, no sign on operand tokens) are fully explicit in the reference solution rather than hidden behind a standard-library state machine. This was a stated constraint in the problem statement (`p2_postfix.h`'s documented input format), not an ambiguity resolved during implementation.
- **P2:** division truncation direction is a non-issue by construction — the problem statement's guaranteed precondition (every division divides its dividend by its divisor with zero remainder) means C's truncate-toward-zero `/` and mathematical integer division agree on every test case, including the negative-dividend case (`10 15 - 5 /` → `-1`, verified).

## Complexity — empirical detail

**This is evidence, not proof** (per `algorithm-verification.md`); both algorithms are also provably O(n) by inspection (a single left-to-right pass, with `push`/`pop` each doing a fixed amount of work — one boundary check, one index update, one array access, exactly as `Slides/CS301/03-arrays-stacks.tex` derives for the array-backed stack in general).

**P1 — `is_balanced`:** timed at n ∈ {50, 100, 200, 400, 500} (best-of-7 over 400,000 reps per size, `clock()`-based CPU timing, MinGW gcc 10.3.0 on Windows). Raw best times (ms): 184, 401, 605, 1176, 1259. Log-log linear-regression slope ≈ 0.79. n is capped at `MAX_EXPR_LEN` = 500 by the assignment's own constraint, so this is a narrow, noisy range (`clock()`'s tick resolution on this Windows/MinGW toolchain is coarse relative to a single call's cost, hence the timing loop and best-of-7 discard-noise protocol) — a slope of 0.79 is not a clean 1.0, but it sits nowhere near the ≈2.0 a quadratic algorithm would show, which is the actual thing this check needs to catch. **Classified CONSISTENT** with the O(n) claim, band: slope well below 1.5 across a 10× size range.

**P2 — `eval_postfix`:** timed at token counts {9, 19, 39, 69, 99} (best-of-7 over 200,000 reps, same toolchain/timing method; token count capped by `MAX_TOKENS` = 100). Raw best times (ms): 7, 19, 40, 127, 94 (last point is a downward outlier, consistent with OS scheduling jitter at this timing resolution, not a real complexity signal). Log-log slope ≈ 1.19. **Classified CONSISTENT** with the O(n) claim — again, the discriminating question is linear vs. quadratic, and 1.19 is far from 2.0.

**Honest limitation stated per the skill's discipline:** neither reported CONSISTENT verdict is a proof; both algorithms' O(n) bound is additionally supported by direct inspection (single pass, O(1) per-token work), which is the stronger argument here — the empirical timing is corroborating evidence at a size range too narrow and too noisy (Windows `clock()` resolution) to stand alone.

## Next steps

None required — both correctness suites are 100% PASS and both complexity claims are CONSISTENT. No FAIL cases to fix, no INCONSISTENT complexity to re-derive.

## Verification method note

Run directly (fan-out to a subagent was not needed for a bounded, already-implemented pair of O(n) reference solutions): hidden/visible test suites executed via `Assignments/CS301/03-arrays-stacks-coding/autograder.sh`; timing harnesses written to the session scratchpad, compiled with `gcc -O2`, and discarded after use (not part of the shipped assignment).
