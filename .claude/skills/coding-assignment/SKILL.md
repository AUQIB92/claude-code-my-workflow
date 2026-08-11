---
name: coding-assignment
description: Scaffold a programming assignment (problem statement PDF + reference solution + hidden test suite + autograder harness) for a finished lecture. Use when user says "make a coding assignment", "create a programming problem for week N", "build an autograded exercise", "generate a coding homework with tests" for a CS course where students submit code, not written derivations. Sibling to /create-assignment (written Conceptual/Numerical/Design problems) — this skill is specifically for take-home programming work with automated grading. NOT for a supervised in-session apparatus-driven exercise (use /lab-manual), and NOT for verifying an existing solution's correctness after the fact (use /verify-algorithm — this skill's own reference solution should itself be run through /verify-algorithm before release).
argument-hint: "[CourseCode/lecture] [language, default python], e.g. CS301/03-linked-lists python"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/coding-assignment` — Programming Assignment Scaffolder

Generate a take-home programming assignment for a finished lecture: a student-facing problem statement (function signature, constraints, worked examples), a reference solution, a **hidden** test suite the student never sees, and a small autograder harness that runs both. The CS-native sibling to `/create-assignment`, which assumes written Conceptual/Numerical/Design problems — this skill is for courses where the deliverable is code (CS301-style data structures/algorithms, or a CS401 lab-adjacent coding exercise).

**Input:** `<CODE>/<lecture>` and an optional language (`$1`, default `python`).

## Phase 0: Pre-Flight

1. Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
2. Read the lecture (prefer `Notes/<CODE>/<lecture>-notes.tex` if it exists).
3. Identify a concrete, self-contained programming task the lecture's content supports — implement the data structure/algorithm the lecture just covered, applied to a scenario not identical to the lecture's own worked example (same "extend, don't repeat" discipline as `/create-assignment`).
4. Produce a short Pre-Flight note: the task, function signature, and the 1-2 learning objectives it exercises.

## Phase 1: Write the problem statement

- **Task description** — what the function/program must do, in plain language, motivated before the mechanics (INV-8).
- **Function signature** — exact name, parameter types, return type, stated precisely enough that the autograder's test calls are unambiguous.
- **Constraints** — input size bounds, value ranges, anything that bounds the acceptable time/space complexity (if the lecture's content implies an expected complexity, state it as a constraint, e.g. "your solution must run in O(n log n) or better" — and note that `/verify-algorithm` can check this empirically after the reference solution is written).
- **Worked examples** — 2-3 example input/output pairs, shown to the student (these become the *visible* tests, distinct from the hidden ones).
- **Starter code / stub** — an empty function signature with a docstring, so the student has an unambiguous file to fill in.

## Phase 2: Reference solution

Write a correct, idiomatic reference solution in the target language. **Before finalizing, this reference solution should itself be run through `/verify-algorithm`** (correctness against generated/adversarial test cases + empirical complexity check against the constraint stated in Phase 1) — a wrong reference solution silently poisons every hidden test built from it in Phase 3.

## Phase 3: Test suite — visible and hidden

- **Visible tests** (shown to the student, in the starter file or an accompanying `test_visible.py`) — the worked examples from Phase 1, so a student can sanity-check locally before submitting.
- **Hidden tests** (`test_hidden.py`, never shown to the student, autograder-only) — must include, at minimum, the same adversarial-coverage bar `/verify-algorithm`'s rule sets: boundary sizes (empty input, single element), structure-specific edge cases (already-sorted/reverse-sorted/all-duplicates for sorting; target-absent for search; disconnected/cyclic for graphs, as applicable), and a batch of random inputs. A hidden test suite that only re-checks the visible examples with different numbers is not adequate coverage.
- Use the standard library's `unittest` (or the target language's equivalent) rather than adding a `pytest` dependency this repo doesn't otherwise carry — matches `/verify-algorithm`'s convention.

## Phase 4: Autograder harness

A small script (`autograder.py` or language-equivalent) that:
1. Imports the student's submission.
2. Runs the hidden test suite against it.
3. Reports a pass/fail count and, optionally, a partial-credit score if the rubric weights individual tests.
4. Fails loudly (non-zero exit, clear message) on a missing function, import error, or infinite loop (wrap execution with a timeout) — a crashed autograder run must never silently read as "0 tests passed, assignment fine."

## Phase 5: Write the files

```
Assignments/<CODE>/<lecture>-coding-assignment.tex   # problem statement PDF (student-facing)
Assignments/<CODE>/<lecture>-coding/
  ├── starter.<ext>            # stub the student fills in
  ├── reference_solution.<ext> # NEVER shipped to students — instructor-only
  ├── test_visible.<ext>       # shown to students, in the assignment PDF's appendix or the starter file
  ├── test_hidden.<ext>        # NEVER shipped to students
  └── autograder.<ext>         # runs hidden tests against a submission
```

The problem-statement `.tex` file uses the same `article`-class, chapter-numbering convention as `/create-assignment`'s student file (see that skill's Phase 3 template) — Phase 1's content only, no reference solution or hidden tests anywhere in it.

**The split is load-bearing, same as `/create-assignment`: never leak `reference_solution` or `test_hidden` content into the student-facing `.tex` or `starter` file.** Treat `Assignments/<CODE>/<lecture>-coding/reference_solution.*` and `test_hidden.*` as instructor-only from the moment they're written — flag this explicitly in the completion report so the user doesn't accidentally publish them (e.g. via `/deploy`, which syncs `Assignments/` PDFs to `docs/` but should never sync the `-coding/` code directory's hidden-test contents).

## Phase 6: QA

Spot-check:
- The reference solution passes its own hidden test suite (run it before reporting done).
- Visible and hidden tests do not overlap (a hidden test that's just a renamed visible test provides no additional coverage).
- The problem statement is answerable from the source lecture alone — no undocumented assumption the student can't infer from the signature + examples.
- The autograder harness runs cleanly end-to-end against the reference solution.

## Report

State: task description, language, hidden-test count, whether `/verify-algorithm` was run on the reference solution (and its verdict), and the file paths written — flagging which are instructor-only.

## Cross-references

- `.claude/skills/create-assignment/SKILL.md` — the written-problem-set sibling; shares the Pre-Flight/split-file/"extend don't repeat" discipline this skill reuses.
- `.claude/skills/verify-algorithm/SKILL.md` — run against the reference solution before release (Phase 2); also usable directly by students/instructors to check a submission's complexity claim.
- `.claude/skills/lab-manual/SKILL.md` — the supervised in-session sibling, for apparatus-driven work rather than take-home autograded code.
- `.claude/rules/algorithm-verification.md` — the adversarial-test-coverage bar this skill's hidden-test suite must meet.
- `.claude/rules/content-invariants.md` (INV-8) — motivation-before-mechanics applied to the problem statement.
