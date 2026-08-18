---
name: build-week
description: Chain the entire per-lecture pipeline for one course week under a single plan and quality gate — resolve a <CourseCode>/<week> to its deck from the syllabus work-list, then run the 7 canonical stages (slides → notes → assignment → lab → GATE practice set → Quarto/deploy → course hub), delegating each to the existing skill via Task, reconciling a per-course syllabi/<CODE>.progress.yaml registry after every stage, and pausing for checkpoint approval between stages. Use when user says "build this week", "build-week", "run the full pipeline for week N", "generate everything for CS401/09", "autopilot week 9", "produce all materials for this lecture", or after adding a week to a syllabus. NOT for a single stage (invoke /create-lecture, /lecture-notes, etc. directly) and NOT for grading or attainment — grading a shipped assignment is `/grade`'s job, standalone, once real student submissions exist; it is not one of this skill's 7 stages.
argument-hint: "[CourseCode/week], e.g. CS401/09 [--stages slides,notes,assignment] [--skip gate,quarto] [--no-pause] [--dry-run]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
disable-model-invocation: true
effort: high
---

# `/build-week` — Semester Autopilot (one command per week)

Turns the repo's eight-per-week manual skill sequence into a single, gate-enforced pipeline. Given `<CODE>/<week>`, it resolves the week's deck name from the syllabus work-list, walks the 7 canonical stages in order, delegates each to the existing skill via `Task` (the same delegation pattern `/grant-proposal` uses for its DMP/facilities phases), reconciles a per-course progress registry after every stage, and pauses for your approval between stages — you stay the auditor, per [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) ("the loop is always human-initiated").

**Core principle:** the individual skills stay the source of truth for *how* each artifact is made. This skill composes them — it never re-implements a stage, never invents content, and never fabricates a score.

## The 7 canonical stages (order is load-bearing)

| # | Stage | Delegates to | Gate / verification |
|---|-------|--------------|---------------------|
| 1 | `slides` | `/create-lecture` + `/compile-latex` | 3-pass XeLaTeX clean; P7 TikZ audit (inside create-lecture) |
| 2 | `notes` | `/lecture-notes` + `/qa-notes` | loop-until-dry Beamer↔Notes parity PASS |
| 3 | `assignment` | `/create-assignment` + compile | compiles; solutions key present |
| 4 | `lab` | `/lab-manual` **or** `/coding-assignment` per `lab_mode` | compiles / reference solution verified |
| 5 | `gate` | `/competitive-exam-questions` | provenance-labeled; CoVe on PYQs |
| 6 | `quarto` | `/translate-to-quarto` + `/qa-quarto` + `/deploy` | loop-until-dry Beamer↔Quarto parity; deployed to `docs/` |
| 7 | `hub` | `/publish-course-hub <CODE>` | tag-balance + link-resolution check (course-wide) |

The `lab` stage delegates by the registry's `lab_mode`: `lab-manual` (supervised apparatus exercises, e.g. Nand2Tetris), `coding-assignment` (autograded programming work), or `none` (skip — labs are a separate numbered track run via `/lab-manual` directly).

## When to use

- Building a full week of a course that is already scaffolded in `syllabi/<CODE>.md` (its "Week → lecture work-list" table).
- Resuming a half-built week (stages already `deployed` are skipped idempotently).
- Establishing the Quarto mirror for a course that so far shipped PDF-only (stage 6).

## When NOT to use

- One stage only — invoke `/create-lecture`, `/lecture-notes`, `/create-assignment`, `/lab-manual`, `/coding-assignment`, `/competitive-exam-questions`, or `/translate-to-quarto` directly.
- A course with no syllabus work-list yet — run `/syllabus` first; this skill resolves weeks from it.
- Grading, attendance, or CO-PO attainment — grading is `/grade`'s job (standalone, once submissions exist, not a pipeline stage); attainment mapping is `/accreditation`'s.

## Phase 0: Resolve + load the registry

1. Parse `$0` as `<CODE>/<week>`. Require both parts; `CODE` is a course code matching `syllabi/<CODE>.md`, `week` is a two-digit week string (`09`, `12`, or `00` for an intro deck).
2. Read `syllabi/<CODE>.md` and find the week's row in the "Week → lecture work-list" table (the `| Week | Deck name | ...` table). Extract the deck name (e.g. `09-cache-memory`). If the week isn't in the work-list but the deck exists on disk (an intro `00` deck), use the on-disk stem and note it.
3. Load `syllabi/<CODE>.progress.yaml`. If missing (first run for a new course), seed it from the syllabus work-list (one entry per week, all stages `absent`, deck names filled) and infer `lab_mode` from the syllabus (a Nand2Tetris-style "Lab schedule" → `lab-manual` track or `none`; a "P1–P13 C programming" practical list → `coding-assignment`). Ask the user to confirm `lab_mode` if neither signal is present — do not guess silently.

## Phase 1: Pre-Flight — reconcile registry against disk, plan the stage set

Disk is authoritative for *existence*; the registry holds *scores and notes*. For the resolved week, scan `Slides/<CODE>/`, `Notes/<CODE>/`, `Assignments/<CODE>/`, `Labs/<CODE>/`, `Quarto/<CODE>/`, and `docs/` (the same scan `/publish-course-hub` Phase 1 performs) and set each stage's status to the furthest milestone reached:

- `absent` — no source artifact (`NN-*.tex` / `.qmd`).
- `present` — source exists, no compiled/rendered output.
- `compiled` — local output (`.pdf` / HTML) exists, not in `docs/`.
- `deployed` — published output exists in `docs/`.

Then compute the **target stage set**: all 7 stages in order, minus (a) any stage in `--skip`, (b) any stage not listed in `--stages` (when `--stages` is given), and (c) any stage already `deployed` (idempotent — re-running reuses, doesn't rebuild). `lab` is dropped entirely when `lab_mode: none`.

Emit the Pre-Flight Report and, unless `--dry-run` or `--no-pause`, wait for confirmation before the first stage:

```markdown
## Pre-Flight Report
- Week: CS401/09  Deck: 09-cache-memory  lab_mode: none
- Registry state: slides absent · notes absent · assignment absent · lab skipped · gate absent · quarto absent
- Target stages (in order): slides → notes → assignment → gate → quarto → hub
- Already deployed (skipped): —
- Disk/registry mismatches: [none / specific]
```

With `--dry-run`, print this report and the registry diff, then exit 0 — write nothing.

## Phase 2: Stage loop

For each target stage in order:

1. **Delegate via `Task`** (one fork per stage). The prompt names the stage's skill file(s) and the `<CODE>/<deck>`, instructs the subagent to read and follow that SKILL.md end-to-end, and to return a structured result: artifacts created (paths), the gate verdict/score (from the skill's own gate — `quality_score.py`, `/qa-notes`, `/qa-quarto`, etc.), and any open issues. The subagent does the compiling/deploying itself (it has `Bash`); this skill does not re-run compilation.
2. **Gate check.** If the subagent reports a failing gate (compile errors, parity FAIL), surface it and stop that stage for the user to decide (fix-and-continue vs. override) — do not silently advance to the next stage.
3. **Reconcile.** Update the registry entry for that stage: `status` from the disk scan (step 1's milestone), `score` (numeric if the gate produced one, else `null`), `note` (verdict string + any override).
4. **Checkpoint.** Unless `--no-pause`, present the stage result + updated status and wait for the user to approve, override, or halt before the next stage. Under `--no-pause`, continue without pausing (a combined summary is produced at the end).

Skip-check is enforced at entry: if a stage is already `deployed`, log "already deployed — skipping" and continue (never re-runs unless the user removes the artifact or requests a rebuild outside this skill).

## Phase 3: Reconcile + report

1. After the last target stage, write the final `syllabi/<CODE>.progress.yaml` (update `last_updated`, every stage status, scores, and notes).
2. Report the combined summary:

```markdown
## Build-Week Summary — CS401/09 (09-cache-memory)
| Stage | Status | Score | Verdict / note |
|---|---|---|---|
| slides | deployed | — | 3-pass compile clean |
| notes | deployed | — | qa-notes PASS (2 rounds) |
| assignment | deployed | — | solutions key present |
| lab | skipped | — | lab_mode: none |
| gate | deployed | — | GATE-CS, PYQs CoVe-verified |
| quarto | deployed | — | qa-quarto PASS; HTML live |
| hub | deployed | — | link + tag check pass |

Next pending week(s): [list]
```

## Exit behavior

- **All target stages `deployed`:** exit 0 with the summary; registry committed to disk (git commit is still `/commit`'s job).
- **A stage gate FAILs:** stop at that stage, report the finding, and exit 1 — do not advance. The user fixes or overrides, then re-runs (idempotent stages make resuming safe).
- **`<CODE>/<week>` unresolvable** (no work-list row, no on-disk deck): exit 1 with the reason; write nothing.
- **`--dry-run`:** print Pre-Flight + registry diff, write nothing, exit 0.

## Flags

- `--stages` `<csv>` — Run only the listed stages (e.g. `slides,notes,assignment`). Unlisted stages are left untouched.
- `--skip` `<csv>` — Skip the listed stages (e.g. `gate,quarto`). Convenient inverse of `--stages`.
- `--no-pause` — Run all target stages without checkpoint approval; emit one combined summary at the end.
- `--dry-run` — Resolve the week, print the Pre-Flight Report and registry diff, write nothing.

## Cross-references

- [`templates/course-progress.yaml`](../../../templates/course-progress.yaml) — the registry schema this skill reads and writes.
- [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — the "loop is human-initiated" boundary; this skill is a user-invoked composition, not a daemon.
- [`.claude/rules/single-source-of-truth.md`](../../rules/single-source-of-truth.md) — Beamer/syllabus as source; every stage this skill runs produces a derived artifact.
- [`.claude/skills/grant-proposal/SKILL.md`](../grant-proposal/SKILL.md) — the delegation-via-`Task` pattern this skill copies at stage scope.
- [`.claude/skills/publish-course-hub/SKILL.md`](../publish-course-hub/SKILL.md) — the disk scan whose "published" detection this skill reuses for `deployed` status.
- Stage skills: [`../create-lecture`](../create-lecture/SKILL.md) · [`../compile-latex`](../compile-latex/SKILL.md) · [`../lecture-notes`](../lecture-notes/SKILL.md) · [`../qa-notes`](../qa-notes/SKILL.md) · [`../create-assignment`](../create-assignment/SKILL.md) · [`../lab-manual`](../lab-manual/SKILL.md) · [`../coding-assignment`](../coding-assignment/SKILL.md) · [`../competitive-exam-questions`](../competitive-exam-questions/SKILL.md) · [`../translate-to-quarto`](../translate-to-quarto/SKILL.md) · [`../qa-quarto`](../qa-quarto/SKILL.md) · [`../deploy`](../deploy/SKILL.md).

## What this skill does NOT do

- **Re-implement a stage.** Every stage delegates to its owning skill; this skill only sequences, gates, and records.
- **Run unattended on a schedule.** No daemon; it is user/skill-invoked (the documented non-goal in `orchestrator-protocol.md`).
- **Commit.** Branch / PR / merge is [`/commit`](../commit/SKILL.md)'s job.
- **Grade or compute attainment.** Grading is `/grade`'s job (standalone, once submissions exist); `/accreditation` owns CO-PO mapping, and reads `/grade --tally`'s output when present.
- **Build a course from scratch.** It needs a syllabus work-list (`/syllabus`); it only executes weeks the syllabus already defines.
