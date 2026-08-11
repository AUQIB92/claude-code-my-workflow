---
name: verify-algorithm
description: Verify an algorithm's correctness and empirically stress-test its claimed time complexity — extract pseudocode from slides/notes/a solution key, implement it, run it against generated test cases (including adversarial edge cases), and check whether measured runtime growth is consistent with the claimed Big-O. Use when user says "verify this algorithm", "check the pseudocode", "is this complexity claim right", "test my solution", "does this Big-O hold up", or after generating algorithmic content via /create-lecture, /lecture-notes, /create-assignment, or /competitive-exam-questions for a CS course. NOT for closed-form math (use /verify-symbolic), NOT for proof rigor with no executable claim (a domain-reviewer concern), and NOT a substitute for domain-reviewer's by-eye derivation check — this skill executes the claim, domain-reviewer inspects the reasoning.
argument-hint: "[file path] [language] — language defaults to python; language is c/cpp for RTL-adjacent or explicitly C-style pseudocode"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: high
---

# Verify Algorithm

Extract pseudocode and a complexity claim from a CS artifact, implement it for real, run it against generated test cases, and empirically check whether measured runtime is consistent with the claimed Big-O. This is the CS sibling of `/audit-reproducibility` and `/verify-symbolic` — same PASS/FAIL discipline, applied to executable algorithms instead of numeric research claims or closed-form math.

**Core principle:** a lecture slide showing correct-looking pseudocode with a stated `O(n log n)` is a claim, not a fact, until something actually runs it. This skill runs it — against edge cases a human reviewer skims past (empty input, single element, all-duplicates, already-sorted, reverse-sorted, one adversarial worst-case) and across growing input sizes to see whether the runtime curve looks like the claimed complexity class.

## When to use

- **Before releasing a solution key** with an algorithm's pseudocode and complexity analysis (`/create-assignment`, `/scaffold-exercises`, `/competitive-exam-questions` output).
- **Before releasing Lecture Notes** with a worked algorithm trace (`/lecture-notes` output).
- **When `domain-reviewer` flags a complexity claim as suspicious** by eye — this skill settles it empirically.
- **Quality-gate in `/commit`** for any CS-course file introducing new pseudocode.

## Prerequisites

- Python execution: confirm `python --version` succeeds (invoke as `python`, not `python3` — a broken Windows-Store `python3` alias may shadow the real interpreter on this machine; `which python` vs `which python3` disambiguates).
- C/C++ (only when `$1` = `c`/`cpp`, e.g. RTL-adjacent CS401 content written in C-like pseudocode): confirm `gcc --version` / `g++ --version`.
- No third-party test framework is required — use the standard library (`assert`, `unittest`) rather than adding a `pytest` dependency this repo doesn't otherwise carry.

## Workflow

### Phase 0: Pre-flight

1. Read [`algorithm-verification.md`](../../rules/algorithm-verification.md) for the test-generation and complexity-classification conventions currently in effect.
2. Confirm the target file exists and contains extractable pseudocode/code plus a stated complexity (an explicit Big-O/Big-Theta claim, or a worked cycle-count/comparison-count derivation the complexity follows from).

### Phase 1: Extract the algorithm and its claim

From the artifact, record:

```
{
  algorithm_id: "Q2_merge_sort",
  location: "Assignment 3, Problem 2, Solution",
  pseudocode_or_code: "<verbatim extracted block>",
  language_hint: "pseudocode" | "python" | "c" | "java",
  claimed_complexity: "O(n log n)",
  claimed_complexity_case: "worst-case" | "average-case" | "best-case",
  worked_example: {input: [...], claimed_output: [...]}   # if the artifact shows one
}
```

Write extracted claims to `quality_reports/algorithm_claims_[artifact-name].json` before implementing anything, so the user can catch a bad extraction before it produces a false FAIL.

### Phase 2: Implement

Translate the pseudocode into a runnable implementation in the target language (`$1`, default `python`). **State every translation decision that isn't fully determined by the pseudocode** — e.g. tie-breaking rule in a comparison, 0- vs 1-indexing, in-place vs. new-array — in the report, since a faithfulness gap here produces a misleading result about the *translation*, not the *original algorithm*.

Save the implementation under `quality_reports/verify_algorithm_[artifact-name]/` (gitignored working directory, like `audit-reproducibility`'s extracted-claims JSON) — never overwrite the source artifact.

### Phase 3: Correctness

1. **Generate test cases**, always including:
   - Empty input, single-element input.
   - The artifact's own worked example (if any) — this is the highest-value case, since a mismatch there means the *artifact's own claimed output* is wrong.
   - Structure-specific edge cases: for sorting — already-sorted, reverse-sorted, all-duplicates; for search — target at position 0, target at the last position, target absent; for graph algorithms — a single node, a disconnected graph, a graph with a cycle where the algorithm assumes a DAG (or vice versa).
   - 20–50 random inputs at a small fixed size, for broad coverage.
2. **Compare against an oracle** where one exists cheaply: Python's built-in `sorted()` for sort algorithms, brute-force $O(n^2)$ or $O(2^n)$ reference implementations for algorithms where a naive-but-obviously-correct version is easy to write. When no cheap oracle exists (e.g. a genuinely novel algorithm), fall back to manually verifying the worked example and a small number of hand-traceable cases only — say so explicitly rather than fabricating a false sense of broad coverage.
3. Record every test as PASS/FAIL with its input, expected output, and actual output.

### Phase 4: Empirical complexity check

**This check is evidence, not proof — state that plainly in every report this skill produces.** Distinguishing $O(n \log n)$ from $O(n^{1.1})$, or $O(n^2)$ from $O(n^2 \log n)$, by timing alone is not reliable at feasible input sizes; the goal is to catch a *clearly wrong* complexity claim (a claimed $O(n \log n)$ algorithm that is actually $O(n^2)$), not to certify a subtle one.

1. Generate inputs at geometrically increasing sizes (e.g. $n = 100, 200, 400, 800, 1600, 3200$ — adjust the ceiling so the largest run completes in a few seconds).
2. Time the implementation at each size (median of 3–5 runs; discard the first "warm-up" run).
3. Fit $\log(\text{time})$ against $\log(n)$ by linear regression; the slope estimates the polynomial degree $k$ in $O(n^k)$. For claims with a log factor ($O(n \log n)$), instead check the ratio $\text{time}(2n) / \text{time}(n)$ against the theoretical ratio for the claimed class (e.g. $O(n\log n)$ predicts a ratio of roughly $2 \times \frac{\log(2n)}{\log n}$, not exactly 2).
4. Classify the result:
   - **CONSISTENT** — measured growth is within a reasonable band of the claimed class (state the band and the measured slope/ratio explicitly; do not just say "consistent").
   - **INCONSISTENT** — measured growth clearly does not match (e.g. slope $\approx 2$ measured against a claimed $O(n \log n)$ — this is the case that matters, a real bug or a wrong claim).
   - **INCONCLUSIVE** — measurements too noisy, input sizes too small, or the two candidate classes too close to distinguish empirically at feasible sizes. Say so; do not force a verdict the data doesn't support.

**Claim strength must match evidence** (same discipline as `/verify-symbolic` and `academic-writing.md` §3): report "measured growth is CONSISTENT with the claimed $O(n\log n)$ (slope $\approx 1.02$)," never "confirmed $O(n \log n)$" — confirmation is a proof-tier claim this method cannot make.

### Phase 5: Report

Write `quality_reports/algorithm_audit_[artifact-name].md`:

```markdown
# Algorithm Verification: [Artifact Name]

**Date:** [YYYY-MM-DD]
**Artifact:** [path]
**Language:** [python/c/cpp]

## Summary

| Check | Result |
|---|---|
| Correctness (N test cases) | PASS: n1  FAIL: n2 |
| Worked example in artifact | PASS / FAIL / N/A (none given) |
| Complexity claim | [claimed] |
| Empirical growth | CONSISTENT / INCONSISTENT / INCONCLUSIVE (measured slope/ratio: [value]) |
| **Overall verdict** | **PASS / FAIL** (FAIL iff any correctness test fails, or complexity is INCONSISTENT) |

## Correctness — FAIL cases (BLOCKER)
| Input | Expected | Actual | Notes |
|---|---|---|---|

## Translation decisions (state every ambiguity resolved during implementation)
- [e.g. "pseudocode did not specify tie-breaking on equal keys; implemented as stable (preserve input order)"]

## Complexity — empirical detail
[measured (n, time) pairs, the fitted slope or ratio, and the honest CONSISTENT/INCONSISTENT/INCONCLUSIVE call with its stated evidence limits]

## Next steps
1. Fix every correctness FAIL.
2. If complexity is INCONSISTENT, re-derive the claimed Big-O by hand (or hand off to `domain-reviewer`) before shipping — the empirical signal says something is wrong, but not what.
3. If INCONCLUSIVE, either accept the claim on the strength of the by-hand derivation alone, or re-run at larger input sizes if the algorithm's runtime allows it.
```

## Exit behavior

- **All correctness PASS, complexity CONSISTENT or the artifact makes no complexity claim:** exit 0.
- **Any correctness FAIL, or complexity INCONSISTENT:** exit 1 — usable as a `/commit` pre-commit gate.
- **Complexity INCONCLUSIVE, zero correctness FAIL:** exit 0 with a warning — the complexity claim is unverified, not refuted.

## What this skill does NOT do

- **Prove a Big-O bound.** It gathers empirical evidence consistent or inconsistent with a claim; a rigorous complexity proof is a `domain-reviewer` / human task (see the "Derivation Verification" lens in `.claude/agents/domain-reviewer.md`, which already checks Master Theorem application, recurrence setup, and asymptotic reasoning by inspection — this skill complements that lens, it does not replace it).
- **Verify closed-form mathematical claims.** Use `/verify-symbolic` for algebra, calculus, and derivations.
- **Catch a correct-but-inefficient reference oracle.** If the oracle used for comparison (Phase 3.2) is itself buggy, correctness PASS is misleading — prefer well-known standard-library oracles (`sorted()`, etc.) over hand-written ones where possible, and flag hand-written oracles explicitly in the report.
- **Guarantee real-world performance.** Constant factors, cache behavior, and language-specific overhead are out of scope; this is an asymptotic-growth check only.

## Cross-references

- [`.claude/rules/algorithm-verification.md`](../../rules/algorithm-verification.md) — test-generation conventions + the empirical-complexity method in full.
- [`.claude/skills/audit-reproducibility/SKILL.md`](../audit-reproducibility/SKILL.md) — the econ/empirical sibling this skill mirrors.
- [`.claude/skills/verify-symbolic/SKILL.md`](../verify-symbolic/SKILL.md) — the Math sibling, for closed-form claims instead of executable algorithms.
- [`.claude/agents/domain-reviewer.md`](../../agents/domain-reviewer.md) — Lens 2 (Derivation Verification) already reviews complexity/proof reasoning by inspection; this skill executes the claim instead.
- [`.claude/output-styles/academic-writing.md`](../../output-styles/academic-writing.md) §3 — "claim strength must match evidence," the discipline behind CONSISTENT/INCONSISTENT/INCONCLUSIVE instead of a false "confirmed."
