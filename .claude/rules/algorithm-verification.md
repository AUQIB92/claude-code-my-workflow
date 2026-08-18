---
paths:
  - "Notes/**/*.tex"
  - "Assignments/**/*-solutions.tex"
  - "CompetitiveExam/**/*-answers.tex"
  - "InstructorHandouts/**/*.tex"
  - "Minors/**/*-solutions.tex"
---

# Algorithm Verification Standards

**Core principle:** pseudocode that looks correct and a complexity claim that pattern-matches to a familiar bound are both claims, not facts, until something runs them. This rule defines how `/verify-algorithm` tests correctness and how it empirically stress-tests complexity claims — and, just as importantly, what it is honest about not being able to prove.

> **Scope:** this rule governs executable algorithms and their complexity claims. For closed-form math (algebra, calculus, derivations), see [`symbolic-verification.md`](symbolic-verification.md) — different verification method entirely (SymPy re-derivation vs. execution + timing).

## Test-case generation (minimum bar)

Every correctness check must include, at minimum:

1. **The artifact's own worked example**, if one is shown — the highest-value case, since a failure here means the artifact's *own claimed output* is wrong, not just the general algorithm.
2. **Boundary sizes**: empty input, single element.
3. **Structure-specific adversarial cases** — do not skip these even when they feel redundant:
   - Sorting: already-sorted, reverse-sorted, all-duplicates.
   - Searching: target at index 0, target at the last index, target absent.
   - Graph algorithms: single node, disconnected graph, a cycle where the algorithm's correctness assumes a DAG.
   - Recursive algorithms: an input that exercises the deepest recursion the test harness can afford (stack-depth sanity, not just correctness).
4. **≥20 random inputs** at a small fixed size, for coverage beyond hand-picked cases.

## Oracle policy

Prefer a well-known standard-library oracle (`sorted()`, etc.) over a hand-written reference implementation. When no cheap oracle exists, a hand-written brute-force reference is acceptable but must be flagged explicitly in the report as hand-written — a bug in the oracle produces a false PASS or false FAIL that looks identical to a bug in the implementation under test, and a reader needs to know which one to distrust first.

## Empirical complexity checking — method and its limits

**This is evidence, not proof.** State this in every report. The method:

1. Time the implementation at geometrically increasing input sizes (e.g. 100, 200, 400, 800, 1600, 3200 — scale the ceiling to keep total runtime reasonable), median of 3-5 runs, discard the first warm-up run.
2. For a polynomial claim $O(n^k)$: fit $\log(\text{time})$ vs. $\log(n)$ by linear regression; the slope estimates $k$.
3. For a claim with a log factor ($O(n \log n)$): compare the doubling ratio $\text{time}(2n)/\text{time}(n)$ against the theoretical prediction for that class, not against a plain polynomial slope.
4. Classify **CONSISTENT** / **INCONSISTENT** / **INCONCLUSIVE** — see the dispositions below. Report the actual measured slope/ratio, not just the verdict word.

**What this method can and cannot catch:**

| Can catch | Cannot reliably catch |
|---|---|
| A claimed $O(n\log n)$ algorithm that is actually $O(n^2)$ (slope $\approx 2$ vs. predicted $\approx 1$) | $O(n\log n)$ vs. $O(n^{1.1})$ — too close to distinguish by timing at feasible sizes |
| A claimed $O(n)$ algorithm that is actually $O(n^2)$ | $O(n^2)$ vs. $O(n^2 \log n)$ — the log factor is a small multiplicative correction, easily lost in measurement noise |
| Gross complexity-class errors (linear vs. quadratic vs. exponential) | Constant-factor or cache-behavior differences — out of scope entirely, this is an asymptotic check only |

If the claimed and next-nearest complexity classes are this close, classify **INCONCLUSIVE** rather than forcing a verdict — a false CONSISTENT is worse than an honest "can't tell empirically."

## Dispositions

- **PASS** (correctness) — implementation matches the oracle/worked-example on every generated test.
- **FAIL** (correctness) — any mismatch. Blocks (`/verify-algorithm` exits 1).
- **CONSISTENT** (complexity) — measured growth falls within the expected band for the claimed class; report the measured slope/ratio and the band, not just the word.
- **INCONSISTENT** (complexity) — measured growth clearly contradicts the claim. Blocks.
- **INCONCLUSIVE** (complexity) — measurement can't distinguish the claimed class from a close neighbor at feasible input sizes. Does not block, but is not a confirmation either.

## Enforcement

Enforced by [`/verify-algorithm`](../skills/verify-algorithm/SKILL.md). Run before releasing any solution key with pseudocode, and pair with `/commit` on solution-bearing files per [`quality-gates.md`](quality-gates.md).

## Cross-references

- [`.claude/skills/verify-algorithm/SKILL.md`](../skills/verify-algorithm/SKILL.md) — the skill this rule governs.
- [`.claude/rules/symbolic-verification.md`](symbolic-verification.md) — the Math sibling, for closed-form claims instead of executable ones.
- [`.claude/agents/domain-reviewer.md`](../agents/domain-reviewer.md) — Lens 2 already reviews Big-O reasoning and recurrence setup *by inspection*; this rule's skill checks the same claims *by execution*. Both are needed — inspection catches a wrong derivation with a coincidentally-plausible growth curve; execution catches an implementation bug that inspection alone would miss.
- [`.claude/rules/model-routing.md`](model-routing.md) — timing runs are mechanical (Haiku-tier); the CONSISTENT/INCONSISTENT/INCONCLUSIVE judgment call and the correctness-vs-oracle-bug triage are not — keep that step on a judgment-tier model.
