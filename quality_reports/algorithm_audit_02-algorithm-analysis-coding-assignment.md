# Algorithm Verification: CS301 Week 2 Coding Assignment — Reference Solution

**Date:** 2026-08-24
**Artifact:** `Assignments/CS301/02-algorithm-analysis-coding/reference_solution.c`
**Language:** C (gcc, tdm64-1 10.3.0)
**Extracted claims:** `quality_reports/algorithm_claims_02-algorithm-analysis-coding-assignment.json`

Three functions were extracted from the reference solution, each a direct
translation of the corresponding frame in `Slides/CS301/02-algorithm-analysis.tex`
(no translation ambiguity to resolve — the lecture's own pseudocode maps to C
1:1 for all three). No pseudocode-to-C translation decisions were required.

## Summary

| Check | linear_search | binary_search | has_duplicate |
|---|---|---|---|
| Correctness (127 hidden checks total, shared suite) | PASS | PASS | PASS |
| Worked example in artifact | PASS | PASS | PASS |
| Complexity claim | O(n) worst case | O(log n) worst case | O(n^2) worst case (no-duplicate input) |
| Empirical growth | **CONSISTENT** (slope ≈ 1.06) | **CONSISTENT** (see note) | **CONSISTENT** (slope ≈ 2.00) |
| **Overall verdict** | **PASS** | **PASS** | **PASS** |

## Correctness

All three functions were compiled against `test_hidden.c` (the assignment's
own hidden suite — see `Assignments/CS301/02-algorithm-analysis-coding/test_hidden.c`),
which meets the `algorithm-verification.md` minimum bar for all three
functions at once:

- The artifact's own worked examples (Group 1).
- Boundary sizes: empty array, single element (Group 2).
- Structure-specific adversarial cases: front/middle/tail/absent for
  `linear_search` (Group 3); target at index 0 / last index / absent, plus
  every position of two hand-built sorted arrays, for `binary_search`
  (Group 4); all-duplicates, no-duplicates, duplicate-at-the-first-pair, and
  duplicate-at-the-last-pair for `has_duplicate` (Group 5).
- 30 random trials (n = 1..40, values drawn from a small range to force
  collisions) checked against independent brute-force oracles for all three
  functions simultaneously (Group 6).
- A moderate-size sanity pass at n = 2000 (Group 7).

**Result: 127/127 checks PASS, 0 FAIL.** Oracle policy: `linear_search`'s and
`has_duplicate`'s oracles in `test_hidden.c` are hand-written (flagged here
per the oracle policy) — each is an independently written second
implementation of the same logic (a plain linear scan / nested loop),
not a copy of `reference_solution.c`'s own code, so a bug shared between the
oracle and the implementation is unlikely but not impossible; `binary_search`
trials are checked by *membership* (the returned index's value equals the
probed key) rather than by an independent oracle, which sidesteps the
tie-breaking ambiguity when duplicates are sorted into the probe array.

As a negative control, `autograder.sh` was also run against the **unfinished
starter stub** (`starter_analysis.c`, all three functions returning
placeholder values) and correctly reported 109/127 failures with a non-zero
exit code — confirming the harness fails loudly rather than silently
reporting "0 tests, assignment fine" on a broken submission.

## Translation decisions

None required — all three functions are a direct, unambiguous line-for-line
translation of the lecture's own pseudocode (same loop bounds, same
tie-breaking via `mid = lo + (hi - lo) / 2`, same early-return-on-first-match
semantics).

## Complexity — empirical detail

Method: `timing_harness.c` was compiled at `-O2` against `reference_solution.c`
and run **5 times**; the first run was discarded as a warm-up and the
remaining 4 runs' `ms/call` were combined by **median** per (function, n),
per `algorithm-verification.md`'s "median of 3-5 runs, discard warm-up" rule.
$\log(\text{time})$ vs.\ $\log(n)$ slope was fit by linear regression for the
two polynomial claims; the near-constant reading for `binary_search` is
reported directly since a log-factor claim isn't a polynomial slope.

**`linear_search`** (worst case: key absent), median ms/call:

| n | 100000 | 200000 | 400000 | 800000 | 1600000 | 3200000 |
|---|---|---|---|---|---|---|
| ms/call | 0.075 | 0.1575 | 0.360 | 0.7175 | 1.3425 | 3.075 |

Fitted slope ≈ **1.06** against a predicted degree of 1 for $O(n)$.
**CONSISTENT** — the measured growth is close to linear and clearly rules out
a quadratic (slope ≈ 2) or worse alternative, which is the failure mode this
check exists to catch.

**`has_duplicate`** (worst case: no duplicate present), median ms/call:

| n | 500 | 1000 | 2000 | 4000 | 8000 | 16000 |
|---|---|---|---|---|---|---|
| ms/call | 0.1225 | 0.43 | 1.775 | 7.10 | 30.0 | 120.0 |

Fitted slope ≈ **2.00** against a predicted degree of 2 for $O(n^2)$ — a
near-exact match; each doubling of $n$ roughly quadruples the time, exactly
as the lecture's nested-loop analysis predicts.
**CONSISTENT.**

**`binary_search`** (worst case: key absent), median ms/call:

| n | 100000 | 200000 | 400000 | 800000 | 1600000 | 3200000 |
|---|---|---|---|---|---|---|
| ms/call | 0.000035 | 0.000035 | 0.00004 | 0.00004 | 0.00004 | 0.00004 |

Mean 3.83e-5 ms, population stdev 2.36e-6 ms (≈6% relative noise). Over a
32x range of $n$, $O(\log n)$ predicts only a $\log_2(3200000)/\log_2(100000)
\approx 21.6/16.6 \approx 1.30\times$ increase — a signal this small is
indistinguishable from measurement noise at this clock resolution.
**CONSISTENT** with $O(\log n)$, with an honest caveat: at this range and
resolution the data cannot distinguish $O(\log n)$ from $O(1)$ — it can only
rule out $O(n)$ or worse, which it does unambiguously (a linear or
quadratic implementation would have shown a clearly rising curve here, as
`linear_search` and `has_duplicate` both do above).

## Next steps

None required — all three correctness suites pass with zero failures, and no
complexity claim came back INCONSISTENT. The reference solution is cleared
for use in hidden-test generation and for release as the autograder's oracle.
