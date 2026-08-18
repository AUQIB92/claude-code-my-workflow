---
name: student-simulator
description: Before a lecture week ships, spawn a cold-student persona that has not seen the instructor handout's answers, works through the deck's Socratic Checks / live-interaction-hook questions in order using only the deck and prerequisite weeks' material, and reports its actual answer and reasoning before being shown the real answer. A second pass diffs the persona's stumbles against the instructor handout's predicted "where students get stuck" misconceptions — confirming the ones it actually hit, and flagging any new stumble the handout didn't predict. Use when user says "playtest this lecture", "run the student simulator", "what would a cold student get wrong here", "check the handout's misconception predictions", "playtest the deck", typically after a deck and its instructor handout both exist. Read-only, single-pass — not adversarial critic/fixer. NOT for deck-level pedagogy structure (use /pedagogy-review) and NOT for editing the deck or handout — output is a report only.
argument-hint: "[CourseCode/lecture], e.g. CS401/06-hardwired-control (Slides/CourseCode/lecture.tex required; InstructorHandouts/CourseCode/lecture-instructor-handout.tex recommended — degrades to raw-stumbles-only mode if absent)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
context: fork
model: sonnet
effort: high
---

# `/student-simulator` — Playtest a Lecture Instead of Just Inspecting It

Every existing reviewer in this repo critiques a deck **by inspection** — reading it and judging whether the pedagogy looks sound. This skill tests it **by simulated execution**: a persona that has genuinely not seen the answers works through the deck's own Socratic Checks and live-interaction hooks cold, the way a real student would, and reports what it actually got wrong. That empirical result is then checked against the instructor handout's own predicted "where students get stuck" misconceptions — confirming the predictions that land, and surfacing anything the handout didn't anticipate.

## When to use

- A deck and its instructor handout both exist, and you want to know whether the handout's predicted misconceptions are the ones a cold student would actually hit — not just whether they're plausible-sounding.
- Before teaching a lecture for the first time, as a cheap empirical check that complements (never replaces) `/pedagogy-review`'s structural inspection.

Not for deck-level pedagogy structure (motivation-before-formalism, box fatigue, pacing — use `/pedagogy-review`). Not for editing anything — this produces a report, never a diff.

## Phase 0: Pre-Flight

1. Confirm `Slides/<CODE>/<lecture>.tex` exists (and, ideally, already compiles — a deck that doesn't compile isn't ready to playtest).
2. Determine prerequisite weeks: every `Slides/<CODE>/<earlier-lecture>.tex` and `Notes/<CODE>/<earlier-lecture>-notes.tex` that the syllabus's work-list places before this week.
3. Check `InstructorHandouts/<CODE>/<lecture>-instructor-handout.tex`. If absent, ask the user whether to (a) proceed in **raw-stumbles-only mode** — Phase 3's diff is skipped, the report lists the persona's stumbles with no handout comparison, or (b) halt with a suggestion to run `/instructor-handout` first for the full comparison. Do not silently choose either — this changes what the report can tell the instructor.
4. Confirm the audience level/prerequisite assumption to give the persona (e.g. "B.Tech Sem 4, no architecture coursework beyond prerequisite weeks") — pull this from `syllabi/<CODE>.md`'s Course Profile / `.claude/rules/knowledge-base-<CODE>.md` rather than guessing.

## Phase 1: Build the redacted working copy (main thread, mechanical — MANDATORY before the fork)

**The one architecturally load-bearing step in this skill.** `context: fork` on the persona agent hides *conversation history* from it — it does **not** hide the filesystem. If the persona fork is simply pointed at the real deck file, it can `Read` past a Socratic Check's own alertblock straight into the bullets that answer it, sitting in the very same frame. A forked context is not a blind context by itself; the blindness has to be built in.

So before spawning anything: read the real deck, find every Socratic Check / `\begin{alertblock}{Question}` / explicitly-marked live-interaction-hook point, and write a **redacted working copy** to `quality_reports/playtest_scratch_<CODE>_<lecture>.tex` (gitignored scratch) with every answer-revealing bullet/sentence immediately following such a question replaced with `[ANSWER REDACTED FOR PLAYTEST]`. Leave the question itself, and everything before it, untouched — only the reveal is redacted. Do this for every such point in the deck; a persona that stumbles into even one unredacted answer partway through invalidates the whole run for that question.

## Phase 2: Spawn the persona (one fork, no review fan-out)

One `Task` call to `student-persona` (`context: fork`), given:
- The redacted working copy's path (never the real deck's path).
- The prerequisite weeks' real `Slides`/`Notes` files (unredacted — those are fair game, the persona has "already taken" those weeks).
- The audience-level statement from Phase 0.4.

This reuses the same blind-context trick `claim-verifier`/CoVe already establishes elsewhere in this repo (a fresh context that never sees the thing it's being tested against) — applied to pedagogy instead of citations.

## Phase 3: Diff against the handout's predictions (main thread)

Skip this phase entirely in raw-stumbles-only mode (Phase 0.3(a)).

Otherwise: read the real (unredacted) deck plus the instructor handout's `\begin{teachingaside}` blocks in full. For each of the persona's wrong/partial/uncertain answers from Phase 2:

- **CONFIRMED** — the handout's teachingaside content for that topic already names this exact misconception (or a close paraphrase of it).
- **NEW-MISS** — the persona stumbled somewhere the handout's misconception coverage doesn't mention at all. This is the genuinely new signal this skill exists to produce.
- **N/A** — the persona actually answered correctly; no misconception to check.

## Phase 4: Write the report

`quality_reports/playtest_<CODE>_<lecture>.md`:

```markdown
# Student Playtest: <CODE>/<lecture>

**Mode:** full comparison | raw-stumbles-only (handout absent)
**Persona audience level:** [stated level]

## Results

| Question | Persona answer | Real answer | Verdict | Handout coverage |
|----------|-----------------|-------------|---------|-------------------|
| Socratic Check: The Memory Wall | "...cost, not physics" | "cost, capacity, and speed all trade off" | Partial | CONFIRMED (handout's Topic 1 teachingaside names this) |
| Socratic Check: Choosing an Organisation | "..." | "..." | Wrong | NEW-MISS |

## New misses (worth adding to the instructor handout)
- [list, with enough context to write the new teachingaside]

## Summary
- N questions playtested, K correct, M partial, J wrong
- Of the non-correct answers: C confirmed by the handout, N new misses
```

## Automation boundary

Fully read-only. This skill never edits the deck's Socratic Checks or the handout's misconception list — the persona's stumbles and the CONFIRMED/NEW-MISS diff are reported for the instructor to act on (e.g. by hand-adding a new teachingaside, or deciding the deck needs a clarifying frame). The redacted scratch copy is a working file only, never committed.

## Report

State: how many questions were playtested, the correct/partial/wrong breakdown, how many stumbles were CONFIRMED vs. NEW-MISS (or that the run was raw-stumbles-only and why), and the path to the written report.

## Cross-references

- `.claude/agents/student-persona.md` — the blind persona this skill dispatches.
- `.claude/agents/claim-verifier.md` — the existing agent that establishes the same "fresh, blind fork" architectural pattern this skill reuses for a different purpose.
- `.claude/skills/instructor-handout/SKILL.md` — the source of the `teachingaside` predicted-misconception content Phase 3 diffs against; degrade gracefully, don't fail, if it hasn't been run yet.
- `.claude/skills/pedagogy-review/SKILL.md` — single-deck structural pedagogy; this skill's empirical sibling, not a replacement.
- `.claude/rules/post-flight-verification.md` — the forked-verifier mechanism whose blind-context principle this skill's Phase 1 redaction step exists to actually enforce (not just assume).
