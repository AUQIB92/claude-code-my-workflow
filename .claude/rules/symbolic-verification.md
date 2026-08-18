---
paths:
  - "Notes/**/*.tex"
  - "Assignments/**/*-solutions.tex"
  - "CompetitiveExam/**/*-answers.tex"
  - "InstructorHandouts/**/*.tex"
  - "Minors/**/*-solutions.tex"
---

# Symbolic Verification Standards

**Core principle:** a solution key is a claim that a computation is correct, not evidence that it is. Every closed-form algebraic/calculus claim a student can check their own work against must be independently re-derivable — this rule defines how `/verify-symbolic` re-derives it and what counts as passing.

> **Scope:** this rule governs symbolic/closed-form math (algebra, calculus, matrix operations, equation-solving). For algorithms and complexity claims, see [`algorithm-verification.md`](algorithm-verification.md). For empirical/numeric research claims (regression output, simulation results), see [`replication-protocol.md`](replication-protocol.md) — a different tolerance regime, because floating-point statistical estimates and exact symbolic equality are not the same problem.

## The equivalence-checking method

1. **Exact symbolic simplification first.** `sympy.simplify(computed - claimed) == 0` is the strongest evidence — it holds by construction, not by sampling.
2. **Randomized numeric substitution as fallback**, when `simplify` cannot resolve equivalence (a known limitation of general symbolic simplification, not a bug): substitute 5 random rational values per free symbol, evaluate both sides to ≥15 significant digits, require agreement within `1e-9` at every point. This is standard CAS-testing practice, not a shortcut — but it is *weaker* evidence than exact simplification and must be labeled as such in every report (see "claim strength must match evidence" in `/verify-symbolic`'s SKILL.md).
3. **Substitution-check for equation roots**, not solution-set string comparison — plug the claimed root back into the original equation.

## Tolerance thresholds

| Kind | Tolerance | Rationale |
|---|---|---|
| Exact/rational results (integers, fractions) | Exact match after simplification | No floating-point involved; there is no excuse for "close enough." |
| Irrational closed-form results (`sqrt`, `pi`, `e`, transcendental) | `1e-9` after high-precision numeric evaluation | Matches float64 double-precision headroom with margin. |
| Results the artifact explicitly rounds/approximates (e.g. "≈ 0.577") | `abs(reported - computed) < 5 * 10^(-d-1)` where `d` = stated decimal places | Standard "half of the last reported digit" rounding tolerance. |
| Multi-step derivation intermediate steps | Same as the step's own kind (exact or irrational) | A wrong intermediate step is still a bug even if a later error cancels it out — do not only check the final line. |

## Dispositions

- **PASS** — see the equivalence method above; report which method resolved it (exact vs. numeric-substitution).
- **FAIL** — computed result provably differs from the claimed result. Blocks (`/verify-symbolic` exits 1).
- **UNTRANSLATABLE** — the LaTeX could not be confidently converted to a SymPy expression. Never silently dropped.
- **AMBIGUOUS** — the claim parses to more than one plausible reading that disagree on PASS/FAIL (e.g. `1/2x`). Flag both readings.

There is no `EXPLAINED` disposition here, unlike `replication-protocol.md`'s numeric-claim regime. A "defensible alternative" makes sense for an empirical estimate that depends on a specification choice; it does not make sense for $\int_0^1 x^2\,dx$, which has exactly one correct value. If a genuine ambiguity exists (the problem statement itself is underspecified), that is an `AMBIGUOUS` disposition on the *problem*, not a softened disposition on the *answer*.

## Enforcement

Enforced by [`/verify-symbolic`](../skills/verify-symbolic/SKILL.md). Run before releasing any solution key, and pair with `/commit` on solution-bearing files per [`quality-gates.md`](quality-gates.md).

## Cross-references

- [`.claude/skills/verify-symbolic/SKILL.md`](../skills/verify-symbolic/SKILL.md) — the skill this rule governs.
- [`.claude/rules/replication-protocol.md`](replication-protocol.md) — the numeric/empirical sibling; different tolerance regime, same PASS/FAIL/blocking discipline.
- [`.claude/rules/algorithm-verification.md`](algorithm-verification.md) — the CS sibling, for executable claims instead of closed-form ones.
- [`.claude/rules/textbook-grounding.md`](textbook-grounding.md) — a correct derivation can still be attributed to the wrong textbook page; the two rules are independent checks and both apply to the same solution key.
