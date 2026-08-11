---
name: verify-symbolic
description: Verify every algebraic/symbolic claim in a math or CS-theory artifact (lecture slides, notes, a solution key, a worked example) by independently re-deriving it with SymPy and comparing against the claimed result. Report PASS/FAIL per claim, the way /audit-reproducibility does for numeric research claims — but for algebra, calculus, and closed-form derivations instead of regression output. Use when user says "verify these solutions", "check this solution key", "did I get the algebra right", "verify the math", "check my derivation", or after generating a solution key via /create-assignment or /scaffold-exercises. NOT for numeric research claims (use /audit-reproducibility), NOT for proof rigor with no computable final claim (that is a domain-reviewer concern), and NOT for algorithm correctness/complexity (use /verify-algorithm).
argument-hint: "[file path] — a .tex/.qmd/.md file with worked math: equations, derivations, solved problems, a solution key"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: high
---

# Verify Symbolic Math

Extract every algebraic/symbolic claim from a math artifact, independently re-derive each one with SymPy, and report which claims check out and which don't. This is the direct analogue of `/audit-reproducibility` — same PASS/FAIL discipline, same "the artifact is not the oracle" posture — applied to closed-form mathematics instead of empirical estimates.

**Core principle:** if the solution key says $\int_0^1 x^2\,dx = \tfrac{1}{3}$, we verify that — symbolically or by high-precision numeric substitution — rather than trusting that it "looks right." A wrong answer in a solution key ships to every student who checks their work against it; nothing in this repo currently catches that before it ships.

## When to use

- **Before releasing any solution key** (`/create-assignment`, `/scaffold-exercises` output) — the single highest-value use. A wrong answer key is worse than no answer key.
- **Before releasing Lecture Notes** with worked derivations (`/lecture-notes` output).
- **On a GATE/competitive-exam answer set** (`/competitive-exam-questions` output) — numeric answer keys are exactly the kind of claim this catches.
- **Quality-gate in `/commit`** — pair with a pre-commit invocation whenever a solution-bearing file changed.

## Inputs

- `$0` — path to the artifact. Required.
- `$1` — tolerance override (optional; default per the table in [`symbolic-verification.md`](../../rules/symbolic-verification.md)).

## Prerequisites

Confirm `python -c "import sympy"` succeeds before starting (SymPy ships via `pip`, already present on this machine — invoke as `python`, not `python3`, since a broken Windows-Store `python3` alias may shadow the real interpreter; verify with `which python` vs `which python3` if in doubt). If SymPy is missing, stop and ask the user to `pip install sympy` rather than silently skipping verification.

## Workflow

### Phase 0: Pre-flight

1. Read [`symbolic-verification.md`](../../rules/symbolic-verification.md) for the equivalence-checking method and tolerance thresholds currently in effect.
2. Confirm the target file exists and contains extractable math (LaTeX math mode, `align`/`gather`/`equation` environments, or Markdown `$...$`/`$$...$$`).

### Phase 1: Extract claims

Parse the artifact for computable symbolic/numeric claims. Patterns to match:

- **Final answers**: `= \frac{1}{3}`, boxed results (`\boxed{...}`), the last line of an `align` block.
- **Multi-step derivations**: every `=` transition inside `align`/`gather`/`eqnarray` is itself a claim — step $k$ equals step $k+1$.
- **Named operations**: derivatives (`\frac{d}{dx}`, `f'(x)`), integrals (`\int`), limits (`\lim`), summations (`\sum`), matrix operations (determinant, inverse, eigenvalues), simplifications, factorizations.
- **Numbered worked examples / solutions**: each `\item` in a solutions block that ends in a specific numeric or closed-form answer.

Record each claim as:

```
{
  claim_id: "Q3_integral",
  location: "Problem 3, Solutions, line 4",
  kind: "integral" | "derivative" | "limit" | "algebraic_simplification" | "equation_solve" | "summation" | "matrix_op",
  expression_latex: "\\int_0^1 x^2\\,dx",
  claimed_result_latex: "\\frac{1}{3}",
  raw_context: "the definite integral evaluates to 1/3"
}
```

Write extracted claims to `quality_reports/symbolic_claims_[artifact-name].json` so the user can review the extraction before verification — LaTeX→SymPy translation is the failure-prone step, and a bad translation produces a false FAIL, not a true one.

### Phase 2: Translate to SymPy

For each claim, translate `expression_latex` into a SymPy expression using `sympy.parsing.latex.parse_latex` where it succeeds; fall back to hand-written SymPy for constructs the LaTeX parser doesn't cover (piecewise definitions, custom notation, multi-line derivations that don't reduce to one parseable expression).

**If a claim cannot be confidently translated, do not guess.** Mark it `UNTRANSLATABLE` and move on — a wrong translation produces a misleading FAIL that erodes trust in the whole report faster than an honest skip.

### Phase 3: Independent re-derivation

Re-derive each translated claim using SymPy's own machinery — `sympy.integrate`, `sympy.diff`, `sympy.limit`, `sympy.solve`, `sympy.simplify`, `sympy.factor`, `sympy.Matrix` methods — **never** by re-parsing the claimed answer and checking it parses; the check must independently compute the result from the *problem*, not validate the *answer*'s syntax.

**Equivalence check (the technique, not just `simplify`):**

1. Compute `diff = sympy.simplify(computed_expr - claimed_expr)`. If `diff == 0`, PASS.
2. `simplify` can fail to recognize equivalence for non-trivial expressions (a known SymPy limitation, not a bug in this skill). When step 1 doesn't resolve to exactly `0`, fall back to **randomized numeric substitution**: substitute 5 random rational values for every free symbol (avoiding domain edge cases — division by zero, log of a negative, etc.), evaluate both `computed_expr` and `claimed_expr` at each point to ≥15 significant digits, and require agreement within `1e-9` at every point. This is the standard CAS-testing technique for confirming symbolic equality when direct simplification stalls — document in the report which method resolved each claim (`simplify` vs. `numeric-substitution`), since a random-substitution PASS is weaker evidence than a `simplify`-to-zero PASS and the report should say so honestly (see "Claim strength must match evidence" below).
3. For **equation-solving claims** (claimed root(s) of an equation), verify by substitution: plug the claimed root back into the original equation and confirm it evaluates to zero (within tolerance for irrational roots), rather than independently re-solving and string-comparing solution sets — solution sets can be equal while written in different but equivalent forms (`sqrt(2)` vs `2**0.5`, different orderings).

### Phase 4: Disposition — PASS / FAIL / UNTRANSLATABLE / AMBIGUOUS

- **PASS** — computed result matches claimed result within tolerance, by either method in Phase 3.
- **FAIL** — computed result provably differs from the claimed result. **Blocks** (exit 1).
- **UNTRANSLATABLE** — the claim could not be confidently converted to a SymPy expression (Phase 2). Never silently dropped — always listed for manual review.
- **AMBIGUOUS** — the claim translates, but to more than one equally plausible reading (e.g. `1/2x` as $\frac{1}{2x}$ vs $\frac{1}{2}x$) and the readings disagree on PASS/FAIL. Flag both readings; never silently pick one.

**Claim strength must match evidence** (same discipline as `academic-writing.md`'s §3): a PASS resolved by exact symbolic simplification is stronger evidence than a PASS resolved only by randomized numeric substitution at finitely many points — the report must distinguish them, not flatten both to an unqualified "PASS."

### Phase 5: Report

Write `quality_reports/symbolic_audit_[artifact-name].md`:

```markdown
# Symbolic Verification: [Artifact Name]

**Date:** [YYYY-MM-DD]
**Artifact:** [path]
**SymPy version:** [version]

## Summary

| Status | Count |
|---|---|
| PASS (exact simplification) | N |
| PASS (numeric substitution only) | N2 |
| FAIL | M |
| UNTRANSLATABLE | K |
| AMBIGUOUS | A |
| **Overall verdict** | **PASS / FAIL** (FAIL iff M > 0) |

## FAIL — BLOCKER
| Claim | Location | Claimed | Computed | Note |
|---|---|---|---|---|

## PASS (numeric substitution only — weaker evidence, spot-check manually)
| Claim | Location | Expression |
|---|---|---|

## UNTRANSLATABLE / AMBIGUOUS (manual review needed)
| Claim | Location | Reason |
|---|---|---|

## Next steps
1. Fix every FAIL — correct the artifact (or, rarely, confirm SymPy mis-simplified and record why).
2. Spot-check every numeric-substitution-only PASS by hand for expressions where equivalence isn't obvious.
3. Manually verify every UNTRANSLATABLE/AMBIGUOUS row.
```

## Exit behavior

- **All PASS:** exit 0.
- **Any FAIL:** exit 1 — usable as a `/commit` pre-commit gate on solution-bearing files.
- **UNTRANSLATABLE/AMBIGUOUS > 0, zero FAIL:** exit 0 with a warning — manual review required before treating the artifact as fully verified.

## What this skill does NOT do

- **Check proof rigor.** A proof with a genuine logical gap but a correct final numeric answer will PASS here — that's a `domain-reviewer` / human-referee concern, not a computable check. See `discipline-cards.md`'s `math` card.
- **Verify pseudocode or algorithm correctness.** Use `/verify-algorithm` for recurrences, Big-O claims, and code correctness — this skill is closed-form math only.
- **Replace the human on genuinely open mathematical questions.** SymPy proves equivalence of two *given* expressions; it does not discover whether the *problem itself* was set up correctly.
- **Handle proofs by induction, contradiction, or exhaustive case analysis.** Those aren't computable claims in SymPy's sense — flag as UNTRANSLATABLE and route to human review.

## Cross-references

- [`.claude/rules/symbolic-verification.md`](../../rules/symbolic-verification.md) — the equivalence-checking method + tolerance thresholds.
- [`.claude/skills/audit-reproducibility/SKILL.md`](../audit-reproducibility/SKILL.md) — the econ/empirical sibling this skill mirrors; same PASS/FAIL/blocking discipline, different domain.
- [`.claude/skills/create-assignment/SKILL.md`](../create-assignment/SKILL.md), [`.claude/skills/scaffold-exercises/SKILL.md`](../scaffold-exercises/SKILL.md) — the skills whose solution-key output this skill verifies.
- [`.claude/skills/verify-algorithm/SKILL.md`](../verify-algorithm/SKILL.md) — the CS sibling (pseudocode correctness + empirical complexity), for algorithmic rather than closed-form claims.
- [`.claude/output-styles/academic-writing.md`](../../output-styles/academic-writing.md) §3 — "claim strength must match evidence," the discipline behind distinguishing exact-simplification PASS from numeric-substitution-only PASS.
