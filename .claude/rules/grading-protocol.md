---
paths:
  - "Submissions/**"
  - "Assignments/**/*-scores-approved.yaml"
  - "Accreditation/**/attainment-data.yaml"
---

# Grading Protocol

**A draft grade is not a grade.** This rule is the cross-cutting contract `/grade` (and any future autograder-integration skill) must follow: the never-auto-finalize gate, the PII/gitignore posture, the rubric schema, the mechanical-vs-judgment split per question type, and the approved-ledger schema. It exists as its own rule file — not buried in one skill's body — because a future skill (an LMS import, a Gradescope bridge) would need the same contract without re-deriving it.

## The never-auto-finalize gate (the one rule that matters most here)

No score reaches a durable, gitignored ledger file without an explicit, separate, human-invoked confirmation step. A grading pass produces **draft reports only**. A later, distinct, explicitly-invoked step copies specific already-drafted scores into the approved ledger. This is the same posture already established elsewhere in this repo for consequential-but-fixable output:

- `/audit-reproducibility`'s UNMATCHED claims are "never auto-downgradable" — a human auditor adjudicates.
- `/disclosure-check` suggestions "never auto-apply" — the analyst owns the disclosure decision.
- `/respond-to-eval` numeric/text conflicts become "Investigate," never a silently-resolved winner.

Grading a real student's real transcript-affecting score is at least as consequential as any of those — the gate here is not weaker than the precedent, it is the same gate applied to higher stakes.

## PII posture

Everything under `Submissions/`, every draft report under `quality_reports/grading/`, every approved ledger (`Assignments/**/*-scores-approved.yaml`), and every tally output (`Accreditation/**/attainment-data.yaml`) contains real student identifiers and is **gitignored, never committed, never published to `docs/`** — the same posture this repo already applies to `Assignments/CS401/*-solutions.tex` and any Timetable/roster content. See `.gitignore`'s Grading block.

## The rubric schema

A rubric is derived per-run from the assignment + solution key (there is no persistent rubric file format yet — this is a v1 simplification; a future `/create-assignment` enhancement could emit a `<lecture>-rubric.yaml` stub, but is not required for `/grade` to function). Shape:

```yaml
rubric:
  - question_id: "Conceptual 1"
    points: 5
    verify: none              # none | symbolic | algorithm
  - question_id: "Numerical 2"
    points: 10
    verify: symbolic
  - question_id: "Design 1"
    points: 15
    verify: none
```

`verify: symbolic` and `verify: algorithm` questions are the ones where a mechanical ground truth exists — the rubric must be confirmed by the instructor (as part of `/grade`'s RUN_CONFIG pre-flight) before any fork launches, since a forked grader cannot be re-prompted mid-run to ask "is this question mechanically checkable?"

## Mechanical-vs-judgment split — reuse, never reinvent

A `verify: symbolic` question is graded by the **identical** equivalence method `.claude/rules/symbolic-verification.md` defines (exact simplification first, randomized numeric-substitution fallback, the same tolerance table) — applied to one `(solution_key_answer, student_answer)` pair, not a whole-artifact audit. A `verify: algorithm` question uses the **identical** method `.claude/rules/algorithm-verification.md` defines (the same test-case generation minimums, the same oracle policy). Both reuse the **same disposition vocabulary** those rules already define (PASS/FAIL/UNTRANSLATABLE/AMBIGUOUS; CONSISTENT/INCONSISTENT/INCONCLUSIVE) — a grading pass must never invent a new disposition word for what is structurally the same check.

A mechanical FAIL/INCONSISTENT disposition is not automatically zero credit — the grader may still award partial credit for a right method with a downstream slip, but must say so explicitly rather than let the mechanical disposition silently become the final score.

## The approved-ledger schema

`Assignments/<CODE>/<lecture>-scores-approved.yaml` (gitignored):

```yaml
assignment: "<CODE>/<lecture>"
approved_date: "YYYY-MM-DD"
approved_by: "<instructor name>"
scores:
  - student_id: "<id>"
    per_question: { "Conceptual 1": 5, "Numerical 2": 10, "Design 1": 12 }
    total: 27
    total_possible: 50
```

Only entries written by an explicit `--approve` invocation belong here — never a raw draft copied in by any other path.

## The tally output

`Accreditation/<CODE>/attainment-data.yaml` (gitignored) is built **only** from approved ledgers, never from raw draft reports, and is the file `/accreditation` Phase 4 checks for when substituting real numbers for its `[FILL]` attainment cells. Building it from anything but the approved ledger would let an un-reviewed draft score silently become a "real" attainment number — exactly the failure the never-auto-finalize gate exists to prevent.

## Cross-references

- `.claude/skills/grade/SKILL.md` — the skill this rule governs.
- `.claude/skills/accreditation/SKILL.md` Phase 4 — the consumer of `attainment-data.yaml`.
- `.claude/rules/{symbolic-verification,algorithm-verification}.md` — the verification methods and disposition vocabularies `/grade` reuses rather than reinvents.
- `.claude/rules/quality-gates.md` — the general pattern of an instructor-facing draft that requires sign-off before it becomes authoritative, applied here to grades specifically.
- `.gitignore` — the Grading block covering `Submissions/`, `quality_reports/grading/`, `*-scores-approved.yaml`, `attainment-data.yaml`.
