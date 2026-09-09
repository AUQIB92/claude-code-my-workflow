# Algorithm Verification: CS301 Week 3 coding reference (stack + P1/P2)

**Date:** 2026-09-09
**Artifact:** `Assignments/CS301/03-arrays-stacks-coding/reference_solution.c` (contract: `stack.h`)
**Language:** C (gcc 13.3 via WSL, `-std=c11 -Wall -Wextra`, zero warnings)

## Summary

| Check | Result |
|---|---|
| Correctness (visible: 18 checks) | PASS: 18 FAIL: 0 |
| Correctness (hidden: 207 checks) | PASS: 207 FAIL: 0 |
| Worked examples in artifact (PDF Ex.1-3) | PASS (all 18 visible checks are the PDF examples verbatim) |
| Complexity claim (P1/P2: O(n) time worst case) | measured growth CONSISTENT (doubling ratios ~2.0 at measurable sizes) |
| **Overall verdict** | **PASS** |

## Correctness — FAIL cases (BLOCKER)

None. Adversarial edges all pass: empty input, single bracket/operand/operator,
100-deep fits vs 101-deep capacity refusal, 150-deep, NULL inputs/NULL out,
`-1` sentinel trap (value -1 round-trips with `STACK_OK`), division/mod-by-zero,
truncation toward zero (`-7 3 /` = -2), `+5`/`++`/letter bad tokens, leftover
operands, whitespace-only, 101-operand overflow, `*out` untouched on all error
paths, 30 seeded random postfix exprs vs unbounded oracle (+60 malformed
variants), 20 seeded random bracket strings + flipped/truncated mutants.

## Translation decisions

Reference implements the contract directly (no pseudocode gap): `top == -1`
empty; `push` refuses at `top + 1 == STACK_MAX` without mutation; `pop`/`peek`
accept NULL `out`; P1 ignores non-brackets, NULL -> 0, over-capacity -> 0
(documented fixed-array price); P2 tokens split on spaces/tabs, lone `-` is the
operator, `+5` rejected, literals range-checked against `INT_MAX`/`MIN`.

## Complexity — empirical detail

`-O2`, best of 5 runs. `is_balanced` on `()`-repeated strings:
20k: ~0s, 40k: ~0s, 80k: 0.0001s, 160k: 0.0002s, 320k: 0.0003s.
`eval_postfix` token counts 29998/59998/119998/239998/479998:
0.0001/0.0003/0.0005/0.0011/0.0022s (ratios 3.0/1.7/2.2/2.0, converging to 2).
CONSISTENT with O(n); small-n readings below clock resolution, stated as evidence only.

## Next steps

None blocking. Ship: student bundle is `stack.h`, `starter_stack.c`,
`test_visible.c`, problem-statement PDF. Instructor-only (gitignored, verified
ignored): `reference_solution.c`, `test_hidden.c`, `autograder.sh`.
