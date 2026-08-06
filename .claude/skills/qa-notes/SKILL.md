---
name: qa-notes
description: Adversarial Lecture-Notes-vs-Beamer parity QA. A critic agent (notes-critic) compares the prose Notes against the Beamer source for content/citation parity and derivation completeness; a fixer agent (notes-fixer) applies fixes; loops until APPROVED (max 5 rounds). Use when user says "qa the notes", "check notes parity", "does the notes file match the slides?", or after a `/lecture-notes` run.
argument-hint: "[CourseCode/lecture], e.g. CS401/07-microprogrammed-control"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
context: fork
---

# Adversarial Lecture Notes vs Beamer QA Workflow

Compare `Notes/<CODE>/<lecture>-notes.tex` against `Slides/<CODE>/<lecture>.tex` using an iterative critic/fixer loop — the same primitive `/qa-quarto` uses for Beamer↔Quarto.

**Philosophy:** the Beamer `.tex` is the gold standard. The Notes must contain everything it does (expanded into prose), invent nothing it doesn't, and preserve every citation.

## Workflow

```
Phase 0: Pre-flight → Phase 1: Critic audit → Phase 2: Fixer → Phase 3: Re-audit → loop until APPROVED (max 5 rounds, loop-until-dry: stop after 2 consecutive rounds add 0 new critical/major)
```

## Hard Gates (Non-Negotiable)

| Gate | Condition |
|------|-----------|
| Content parity | Every Beamer frame's core idea appears in the Notes |
| No invention | No claim/example/citation in Notes absent from Beamer |
| Citation parity | Every `\cite{}` key matches, same key |
| Notation fidelity | Every symbol identical to Beamer (INV-2 applies equally to Notes) |
| Textbook-page honesty | Any page number in Notes not in the Beamer frame must trace to a real `supporting_books/*/index.md` entry |

## Phase 0: Pre-flight

1. Locate `Slides/<CODE>/<lecture>.tex` and `Notes/<CODE>/<lecture>-notes.tex`.
2. If Notes doesn't exist yet, stop and point the user at `/lecture-notes` first — this skill only QAs an existing Notes file, it does not generate one.

## Phase 1: Initial Audit

Launch `notes-critic` (via `Task`, `context: fork`) to compare Beamer vs Notes. Report saved to `quality_reports/[CODE]_[lecture]_notes_critic_round1.md`.

## Phase 2: Fix Cycle

If not APPROVED, launch `notes-fixer` to apply fixes (Critical → Major → Minor) to `Notes/<CODE>/<lecture>-notes.tex`.

## Phase 3: Re-Audit

Re-launch `notes-critic` in a fresh fork to verify fixes landed and check for new issues. Loop back to Phase 2 if needed.

## Stopping condition (loop-until-dry, per `.claude/rules/orchestrator-protocol.md`)

Stop after **2 consecutive rounds add 0 new critical/major findings** (deduped on location+finding), or after 5 rounds (fallback cap) — present remaining issues to the user rather than looping indefinitely. A finding that survives rounds N and N+2 unresolved gets escalated to the user, not patched a third time (two-strikes, per `.claude/rules/summary-parity.md`'s general pattern).

## Report

Final verdict (APPROVED / issues remaining after cap), round count, and a link to the latest critic report.

## Cross-references

- `.claude/agents/notes-critic.md`, `.claude/agents/notes-fixer.md` — the critic/fixer pair.
- `.claude/skills/lecture-notes/SKILL.md` — generates the Notes file this skill QAs.
- `.claude/skills/qa-quarto/SKILL.md` — the sibling pattern this skill copies (Beamer↔Quarto instead of Beamer↔Notes).
- `.claude/rules/orchestrator-protocol.md` — the loop-until-dry primitive.
