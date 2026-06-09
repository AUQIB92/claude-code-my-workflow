---
name: diagnose
description: Root-cause a failing or wrong empirical result with a disciplined reproduce → minimise → hypothesise → instrument → fix loop, instead of guessing-and-poking. Use when the user says "why is my regression wrong", "this number changed", "my script errors out", "the result won't reproduce", "debug this", "this estimate looks wrong", or "it worked yesterday". Tuned for research code (R/Stata/Python): data-type coercion, NA/merge blow-ups, factor levels, clustering/SE choices, seeds, package-version drift.
argument-hint: "[file, script, or short description of the symptom] [--no-fix]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Task"]
effort: high
---

# /diagnose — Root-Cause a Wrong or Failing Result

Find *why* an analysis errors, returns the wrong number, or won't reconcile — with a structured debugging loop rather than scattershot edits. Adapted from the `diagnose` pattern in [mattpocock/skills](https://github.com/mattpocock/skills), reshaped for empirical research code where the bug is usually a *silent* wrong number, not a crash.

The discipline: **never edit before you can reproduce, and never fix before you can explain.** A guessed fix that makes the symptom disappear without a named root cause is how a wrong number gets *laundered* into a published table.

## When to use

- A regression / estimate returns a value you can't explain, or one that changed when nothing should have.
- A script errors out and the stack trace doesn't point at the real cause.
- A result "won't reproduce" — different number on re-run, on another machine, or after a package update.
- A replication claim fails `/audit-reproducibility` and you need to localize *which* step drifted.

**Use a sibling instead when:** you want a code-quality pass with no specific symptom ([`/review-r`](../review-r/SKILL.md)); you want to re-verify *all* numeric claims against code ([`/audit-reproducibility`](../audit-reproducibility/SKILL.md)); or the environment itself is the suspect and you need to snapshot it ([`/capture-environment`](../capture-environment/SKILL.md)).

## Phases

### Phase 0 — Pin the symptom (expected vs. actual)

State the bug as a falsifiable gap before touching anything:

- **Expected:** the value/behaviour you believe is correct, and *why* (a prior run, a paper table, a hand calculation, a theoretical sign).
- **Actual:** the value/error observed now, copied verbatim (full message, not a paraphrase).
- **Tolerance:** for a numeric bug, the threshold that separates "same" from "different" (see [`replication-protocol.md`](../../rules/replication-protocol.md) — don't chase 1e-12 noise; don't wave away a 5% gap).

If expected/actual can't be stated, the task is *understanding*, not diagnosis — stop and clarify first.

### Phase 1 — Reproduce deterministically (get a reliable red)

A bug you can't reproduce on demand can't be fixed, only hidden.

1. Fix every source of nondeterminism: set the seed, pin the working directory, record `sessionInfo()` / `pip freeze` / Stata `version` (lean on [`/capture-environment`](../capture-environment/SKILL.md)).
2. Re-run the smallest unit that exhibits the bug and confirm it fails **every time**. An intermittent failure is its own hypothesis (uninitialised RNG, order-dependent merge, race in parallel code) — note it and carry it into Phase 3.

### Phase 2 — Minimise to an MWE

Shrink until the bug sits in the open:

- **Data:** subset to the smallest rows/columns that still reproduce (often one group, one period, a handful of rows).
- **Code:** strip the pipeline to the shortest path from input to wrong output; comment out everything the symptom survives without.
- Each removal that *keeps* the bug is information; each that *kills* it is a stronger signal — record which.

The MWE is the deliverable even if the fix is later trivial: it's what makes the root cause undeniable.

### Phase 3 — Hypothesise (enumerate, then rank)

List candidate causes *before* testing any — a written list beats poking because it prevents fixating on the first idea. For research code, walk the usual suspects:

- **Types & coercion** — a numeric read as character/factor; integer overflow; date parsed wrong; `TRUE/FALSE` ↔ `1/0`.
- **Missingness** — `NA` dropped silently, `na.rm` flipping a mean, listwise deletion changing the sample mid-pipeline.
- **Joins & shape** — a many-to-many merge inflating rows; duplicate keys; an unbalanced panel where balance was assumed.
- **Specification** — wrong clustering level, fixed-effects absorbed twice, a control that is a bad control, a lag/lead off by one.
- **Sample** — a filter that runs before vs. after a transform; an outlier rule applied inconsistently.
- **Environment** — a package/Stata version bump that changed a default; a seed that moved; locale/encoding.

For a genuinely ambiguous bug, fan out the top competing hypotheses to parallel `Task` subagents (one per hypothesis, `context: fork`), each instructed to *try to confirm its own cause on the MWE* and report back — the loop-first analogue of asking three colleagues at once (see [`orchestrator-protocol.md`](../../rules/orchestrator-protocol.md)).

### Phase 4 — Instrument & localize (bisect, don't stare)

Test the ranked hypotheses cheaply:

- **Bisect the pipeline** — check the intermediate value at the midpoint of the data flow; the bug is upstream or downstream of it. Repeat. Binary search finds the offending line in `log2(n)` steps, not `n`.
- **Bisect history** — if it "worked yesterday", `git bisect` (or compare against the last-good commit/output) to pin the change that introduced it.
- **Instrument** — print/inspect types, row counts, `NA` counts, and the value at each stage; the stage where expected and actual diverge *is* the location.

End Phase 4 with a one-sentence root cause naming the exact line/step and mechanism.

### Phase 5 — Fix & verify (then guard against regression)

Unless `--no-fix` is set:

1. Apply the **minimal** fix at the root cause — not a downstream patch that masks it (prefer fixing the bad merge over filtering its duplicate rows afterward).
2. Re-run the MWE → confirm `actual == expected` within the Phase-0 tolerance.
3. Re-run the **full** unit and any dependent step → confirm the fix didn't move another number. If the result feeds a manuscript claim, re-check it (cross-ref the passport in [`/audit-reproducibility`](../audit-reproducibility/SKILL.md)).
4. Note a **prevention**: the assertion, test, or type-check that would have caught this earlier (a `stopifnot(nrow(df) == n)`, a post-merge row-count check) — propose it, don't silently add a test suite.

With `--no-fix`, stop after the root cause is named and report it for the user to fix by hand.

## Output / report format

Write a short diagnosis to `quality_reports/diagnoses/YYYY-MM-DD_<slug>.md`:

- **Symptom:** expected vs. actual (+ tolerance).
- **MWE:** the minimal input/code that reproduces it.
- **Root cause:** the exact line/step and mechanism.
- **Fix:** the diff applied (or, with `--no-fix`, the recommended change).
- **Verification:** MWE + full-run re-check results.
- **Prevention:** the guard that would have caught it.

Plus a chat summary leading with the one-line root cause.

## Exit behavior

- **Reproduced, root-caused, fixed, re-verified:** exit with the root cause, the diff, and the prevention note.
- **`--no-fix`:** stop at a named root cause; write nothing to source, only the report.
- **Cannot reproduce after Phase 1:** report the nondeterminism as the finding (it *is* the bug class) and propose how to make the analysis deterministic; do not edit blindly.
- **Symptom not statable (no expected/actual):** stop in Phase 0 and ask for the expected value — diagnosis needs a target.

## Flags

- `--no-fix` — Diagnose only: run through naming the root cause (Phases 0–4) and write the report, but make **no** edit to source. Use when you want to apply the fix yourself, or when the file is shared/load-bearing and an automated edit is inappropriate.

## Cross-references

- [`.claude/skills/review-r/SKILL.md`](../review-r/SKILL.md) — code-quality review with no specific symptom (diagnose is symptom-driven).
- [`.claude/skills/audit-reproducibility/SKILL.md`](../audit-reproducibility/SKILL.md) — verify all numeric claims against code; diagnose localizes a *single* failing one.
- [`.claude/skills/capture-environment/SKILL.md`](../capture-environment/SKILL.md) — snapshot the environment when version/seed drift is the suspect.
- [`.claude/rules/replication-protocol.md`](../../rules/replication-protocol.md) — the tolerance contract that defines "same number".
- [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — the fan-out primitive used for competing-hypothesis testing in Phase 3.

## What this skill does NOT do

- **Review code with no symptom** — that is [`/review-r`](../review-r/SKILL.md). Diagnose needs an expected-vs-actual gap to chase.
- **Re-audit every claim in a paper** — that is [`/audit-reproducibility`](../audit-reproducibility/SKILL.md). Diagnose fixes one bug deeply.
- **Build a test suite** — it proposes the single guard that would have caught *this* bug; standing test infrastructure is separate dev work.
- **Commit the fix** — branching / committing is [`/commit`](../commit/SKILL.md)'s job.
