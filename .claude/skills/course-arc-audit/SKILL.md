---
name: course-arc-audit
description: Fan out reviewers across consecutive week-pairs (plus one whole-arc pass) to check semester-level pedagogical continuity no current skill checks — does week N's opening handoff line accurately describe what week N-1 actually closed with, is a symbol/term used consistently across every week per the knowledge base's Symbol Reference table, does difficulty escalate sensibly per difficulty-levels.md, and are forward-references ("this is priced in Week 10") actually paid off in the week they promise. Use when user says "course arc audit", "check narrative continuity", "does the course hang together", "audit the semester arc", "check cross-week consistency", "does week N follow from week N-1", typically after several weeks of a course have shipped, or before a full re-teach. Read-only, no fixer — mirrors /deep-audit's fan-out shape for repo mechanics, applied to pedagogical continuity instead. NOT for single-deck pedagogy (use /pedagogy-review) and NOT for repo-mechanical consistency like skill counts or broken links (use /deep-audit).
argument-hint: "[CourseCode] [--weeks N-M] (default: audits every consecutive pair of weeks that have shipped decks, plus one whole-arc pass; --weeks restricts to a sub-range, e.g. --weeks 6-9)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
effort: high
---

# `/course-arc-audit` — Semester-Level Pedagogical Continuity

Every existing review skill in this repo checks one deck at a time. Nothing checks whether the *course*, taken as a sequence of weeks, actually reads as one continuous narrative — whether Week 9's "where we left off" recap is honest about what Week 8 actually closed with, whether a symbol registered in the knowledge base's Symbol Reference table means the same thing every time it reappears six weeks later, whether a "we'll price this in Week 10" promise ever gets paid off. This skill closes that gap with a read-only fan-out audit, structurally identical to `/deep-audit`'s pattern but applied to teaching continuity instead of repository mechanics.

## When to use

- Several weeks of a course have shipped and you want to check they hang together, not just that each one is individually sound.
- Before re-teaching a course, or after a mid-semester content revision that might have broken a downstream handoff or notation promise.

Not for a single deck's internal pedagogy (`/pedagogy-review`) and not for repo-wide mechanical consistency like skill/agent counts or broken links (`/deep-audit`).

## Phase 0: Resolve scope (mechanical, cheap — run before any fork)

1. `$ARGUMENTS` is `<CODE>` optionally followed by the `--weeks` flag and a range (`N-M`). Confirm `syllabi/<CODE>.md` and `.claude/rules/knowledge-base-<CODE>.md` both exist.
2. Scan `Slides/<CODE>/` for shipped decks (`NN-*.tex` with a compiled `.pdf` next to it — a week with only a `.tex` and no `.pdf` hasn't been verified to compile and should be excluded with a note, not silently audited). Build the ordered list of shipped week numbers; apply the `--weeks` range if given.
3. If fewer than 2 shipped weeks are in scope, stop — there is nothing to compare. Report this and exit; do not run a degenerate single-week "audit."
4. Read `.claude/rules/knowledge-base-<CODE>.md`'s **Symbol Reference** and **Lecture Progression** tables in full — these are the arc-mode ground truth.

Emit a short Pre-Flight note: `Weeks in scope: N1..Nk (M shipped, J excluded — no compiled PDF). Fan-out width: (M-1) pairwise forks + 1 arc-mode fork.` This is not a RUN_CONFIG-scale interactive gate (nothing here needs user input before launch) — just a scope confirmation so the user isn't surprised by which weeks got audited.

## Phase 1: Fan-out (the fleet)

Launch, in **one message**, `Task` calls to `arc-continuity-reviewer` (`context: fork`):

- **One fork per consecutive week pair** `(N, N+1)` in scope, mode = `pairwise`, given both weeks' `Slides/<CODE>/*.tex` (and `Notes/<CODE>/*-notes.tex` if present).
- **One additional fork**, mode = `arc`, given the full Symbol Reference + Lecture Progression tables and every shipped deck in scope.

This keeps fan-out width at `M` forks total for an `M`-week course (`M-1` pairwise + 1 arc), not `M × k` lenses — a deliberate width choice, not an oversight: continuity is a property of adjacency and of the whole-course registry, not something that benefits from multiple independent lenses per pair the way a single deck's pedagogy/visual/proofreading review does.

## Phase 2: Reduce

Pool every fork's `FINDING`s. Apply the standard gate predicate (`orchestration-schemas.md` §3): `CRITICAL > 0 → BLOCK`, `MAJOR > 0 → REVISE`, else `PASS`. Since this skill has no fixer, `BLOCK`/`REVISE`/`PASS` are report-level labels describing the audit's verdict, not a build gate — nothing halts because of them.

## Phase 3: Judge + hallucination gate

If a synthesis step introduces any CRITICAL finding not traceable to a specific fork's report, it must survive re-verification by a fresh `claim-verifier` fork before being kept (`orchestrator-protocol.md` §3, unmodified reuse) — dropped to `[JUDGE-HALLUCINATED]` and the verdict recomputed if it can't be grounded.

**No loop-until-dry.** This is a read-only, single-pass audit with no fixer — same shape as `/pedagogy-review`/`/devils-advocate`/`/visual-audit`, not `/qa-quarto`. A finding here is something the instructor acts on by hand (editing a deck, correcting the knowledge base) — running the audit again afterward is a fresh invocation, not an automatic loop.

## Phase 4: Write the report

`quality_reports/course_arc_audit_<CODE>.md`:

```markdown
# Course Arc Audit: <CODE>

**Weeks audited:** N1-Nk (M weeks, J-1 pairwise comparisons + 1 arc-mode pass)
**Verdict:** PASS | REVISE | BLOCK

## Findings

| # | Severity | Mode | Location | Finding | Recommendation |
|---|----------|------|----------|---------|-----------------|
| 1 | MAJOR | pairwise (8,9) | Week 9 opening vs. Week 8 closing | ... | ... |
| 2 | MINOR | arc | Symbol Reference vs. Week 6 deck | ... | ... |

## Scorecard
- N critical, M major, K minor
- Pairwise forks: [list, each with its own mini-verdict]
- Arc-mode fork: [symbol-drift findings, forward-reference payoff findings, registry-accuracy findings]
```

## Automation boundary

Entirely read-only against `Slides/`, `Notes/`, and `.claude/rules/knowledge-base-<CODE>.md` — the report flags issues; the instructor fixes them by hand or via a follow-up `/create-lecture` edit or a direct knowledge-base correction. This skill is **never** wired into `/build-week`'s 7 mandatory stages — it audits an already-shipped arc, not a single week being built, and adding it to the per-week pipeline would require a progress-registry schema change for no clear pipeline-blocking benefit. Invoked standalone, explicit trigger only.

## Report

State: weeks audited, fan-out width, per-severity finding counts, the overall verdict, and the path to the written report.

## Cross-references

- `.claude/agents/arc-continuity-reviewer.md` — the fleet this skill dispatches, in `pairwise` and `arc` modes.
- `.claude/skills/deep-audit/SKILL.md` — the mechanical repo-wide fan-out pattern this skill's structure mirrors, applied to teaching continuity instead of repository consistency.
- `.claude/skills/pedagogy-review/SKILL.md` — single-deck pedagogy; this skill is its semester-level sibling, not a replacement.
- `.claude/rules/difficulty-levels.md` — the tier definitions pairwise mode's local-difficulty-step check is calibrated against.
- `.claude/rules/orchestrator-protocol.md`, `.claude/references/orchestration-schemas.md` — the fan-out/reduce/judge primitives and `FINDING`/`SCORECARD` schema this skill reuses unmodified.
- `.claude/rules/knowledge-base-CS401.md` — a live example of the Symbol Reference / Lecture Progression tables arc mode reads as ground truth.
