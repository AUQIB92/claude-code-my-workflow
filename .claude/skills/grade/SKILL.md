---
name: grade
description: Score a batch of student submissions against a finished assignment's rubric and solution key — LLM judgment for Conceptual/Design answers, and the SAME verification method /verify-symbolic and /verify-algorithm use (SymPy equivalence, algorithm execution against generated test cases) for Numerical/algorithmic answers, so a numerically-wrong answer is caught mechanically, not missed by vibes. Produces a per-student draft report (score per question + brief feedback) for INSTRUCTOR REVIEW — never auto-finalized. A separate --approve step writes reviewed scores to an approved ledger; a separate --tally mode aggregates approved ledgers across a course into attainment-ready numbers for /accreditation, never straight from the raw grading pass. Use when user says "grade these submissions", "score this assignment", "check student answers against the key", "tally approved grades for accreditation", "grade CS401 week 9". NOT for computing CO-PO attainment directly (that's /accreditation, which consumes this skill's --tally output) and NOT a substitute for instructor sign-off — no score is ever written to the approved ledger without an explicit --approve confirmation.
argument-hint: "[CourseCode/lecture] [--approve <StudentID|all>] [--tally] (default mode grades every submission in Submissions/CourseCode/lecture/)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Task"]
effort: high
---

# `/grade` — Verified Grading, Never Auto-Finalized

Closes the gap `/accreditation` and `/build-week` have both explicitly flagged since they were written: "no gradebook integration exists yet — a future `/grade` skill would supply that data." This skill scores student submissions against a finished assignment's solution key, reusing the **exact same** verification methods `/verify-symbolic` and `/verify-algorithm` already define for numerical/algorithmic answers — so a numerically-wrong derivation is caught mechanically, not missed because an LLM skimmed a plausible-looking page of algebra. Every score it produces is a draft; nothing becomes real until the instructor explicitly approves it. Full contract: [`.claude/rules/grading-protocol.md`](../../rules/grading-protocol.md) — read that rule before working on this skill; it defines the schemas this skill's three modes implement.

## Three modes, one skill (not three skills)

Matches the flag-controlled-workflow convention `/build-week` already establishes elsewhere in this template (one command, several modes, a human checkpoint in the middle) rather than proliferating separate skill files for what is really one workflow.

- **Default** (`/grade <CODE>/<lecture>`) — grade a batch, produce draft reports.
- **`--approve <StudentID|all>`** — explicit human step, copy specific already-drafted scores into the approved ledger.
- **`--tally`** — aggregate approved ledgers into `/accreditation`-ready attainment numbers.

## Default mode: grade a batch

### Phase 0: Pre-Flight

1. Confirm `Assignments/<CODE>/<lecture>-assignment.tex` and its (gitignored) `Assignments/<CODE>/<lecture>-solutions.tex` both exist. If the solutions key is missing, stop — there is no ground truth to grade against.
2. Confirm `Submissions/<CODE>/<lecture>/` exists and contains at least one submission file (`<StudentID>.md` or `.tex`, one per student). If the directory doesn't exist, create it with a template `README.md` (tracked, no student data) documenting the expected format, and stop — nothing to grade yet.

### Phase 1: RUN_CONFIG — derive and confirm the rubric (MANDATORY, before any fork)

A forked grader cannot be re-prompted mid-run to ask "is this question mechanically checkable?" — so the rubric is built and confirmed **before** Phase 2 launches, exactly the RUN_CONFIG discipline `orchestrator-protocol.md` establishes for every fan-out skill in this repo.

Read the assignment + solution key. For each question, derive:
- `points`: from the assignment's stated point value (or split evenly across questions if unstated — flag this as an assumption).
- `verify`: `symbolic` if the solution key's answer is a closed-form derivation checkable by `symbolic-verification.md`'s method; `algorithm` if it's a runnable trace/algorithm/complexity claim checkable by `algorithm-verification.md`'s method; `none` for Conceptual/Design questions with no mechanical ground truth.

Echo the derived rubric back to the user as a Pre-Flight Report and get explicit confirmation before proceeding — this is the one interactive gate in the whole default-mode flow, and it exists precisely because nothing downstream can ask again.

```markdown
## Grading Pre-Flight — CS401/09-cache-memory
| Question | Points | Verify method |
|---|---|---|
| Conceptual 1 | 5 | none |
| Numerical 2 | 10 | symbolic |
| Numerical 3 | 10 | algorithm |
| Design 1 | 15 | none |
Total: 40 points. N submissions found in Submissions/CS401/09-cache-memory/.
Confirm this rubric before grading proceeds?
```

### Phase 2: Fan-out (one fork per student)

Launch, in one message, one `Task` call per submission to `grader` (`context: fork`). **Each fork sees only its own student's submission** — never any other student's, never the full class roster — plus the confirmed rubric and the solution key. This isolation is deliberate: it prevents cross-student bias and keeps each fork's context to exactly what it needs.

### Phase 3: Reduce — pool and flag disagreements

Pool the N per-student reports. For any question where a fork flagged a mechanical-vs-conceptual disagreement (per `grader.md`'s instructions), surface it explicitly in the batch summary for instructor attention — never silently resolved either direction, matching `/respond-to-eval`'s "Investigate," never a silent winner.

### Phase 4: Judge + hallucination gate

If any synthesis step flags an integrity concern (e.g. suspected near-identical answers across two submissions) that no individual grader fork raised, it must survive re-verification by a fresh `claim-verifier` fork before being surfaced (`orchestrator-protocol.md` §3) — and even then, it is surfaced as a flag for the instructor, **never an automatic penalty**.

### Phase 5: Write draft reports

`quality_reports/grading/<CODE>/<lecture>/<StudentID>-report.md`, each headed `DRAFT — awaiting instructor approval`, per-question score + feedback + disposition + a total. Write one combined batch summary too: `quality_reports/grading/<CODE>/<lecture>/_batch-summary.md` (mean/median/distribution, any flagged disagreements or integrity concerns).

**Nothing in this mode writes to any approved-scores file.** Default mode's only output is draft reports.

## `--approve <StudentID|all>` mode

A separate, explicit, human-invoked step. Given a `StudentID` (or `all`), read that student's (or every student's) already-drafted report(s) and copy the scores into `Assignments/<CODE>/<lecture>-scores-approved.yaml` per the schema in `grading-protocol.md`. Confirm each score with the instructor before writing if invoked interactively; if invoked with `all` non-interactively, list every score about to be written and require one final explicit confirmation before the write. This is a mechanical file-write gated by an explicit confirmation, not a fresh LLM judgment pass — it does not re-grade anything.

## `--tally` mode

Read **only** `Assignments/<CODE>/*-scores-approved.yaml` files (never raw draft reports — a draft that was never approved must never contribute to attainment numbers). Aggregate per-CO direct-attainment percentages (cross-referencing which question(s) test which CO, from the same mapping `/accreditation` Phase 3 already builds) and write `Accreditation/<CODE>/attainment-data.yaml`. Report which COs now have real attainment data and which still need more approved assignments before a percentage is meaningful.

## Automation boundary (the most load-bearing contract in this skill)

- Default mode: draft reports only, `quality_reports/grading/` (gitignored), never touches an approved file.
- `--approve`: the only path that writes to `*-scores-approved.yaml`, and only for scores that already exist as a draft and are explicitly confirmed.
- `--tally`: reads only approved ledgers, writes `attainment-data.yaml` — consumed by a follow-up `/accreditation` run (see that skill's Phase 4), never computed here directly.
- No hook, no cron, no auto-apply anywhere in this chain.

## Report

State: mode run, N submissions processed (default), or N scores approved (--approve), or which COs got real attainment numbers and from how many approved assignments (--tally). Always restate that draft scores are drafts and approved scores required an explicit confirmation — do not let the summary imply anything was auto-finalized.

## Cross-references

- `.claude/rules/grading-protocol.md` — the full contract (never-auto-finalize gate, rubric/ledger schemas, PII posture) this skill implements.
- `.claude/agents/grader.md` — the per-student fork this skill's default mode dispatches.
- `.claude/rules/{symbolic-verification,algorithm-verification}.md` — the exact verification methods and dispositions reused, never reinvented.
- `.claude/skills/accreditation/SKILL.md` Phase 4 — the consumer of `--tally`'s `attainment-data.yaml` output.
- `.claude/skills/build-week/SKILL.md` — explicitly excludes grading from its 7 stages; this skill is the standalone tool that line has always pointed at.
- `.gitignore` — the Grading block covering every file this skill writes with real student data.
