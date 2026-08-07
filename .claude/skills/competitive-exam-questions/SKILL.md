---
name: competitive-exam-questions
description: Build a course-organized competitive-exam practice set (default GATE CS) for a finished lecture — real past-year questions verified via Chain-of-Verification, plus original exam-pattern questions to fill topic gaps, each labeled by provenance. Use when user says "add GATE questions for this lecture", "competitive exam questions course-wise", "make a GATE practice set for week N", "PYQs for this topic". NOT for graded coursework (use `/create-assignment`) and NOT for inventing "past" questions without verification — every real-PYQ claim must be independently checked before it ships.
argument-hint: "[CourseCode/lecture] [--exam GATE-CS (default)] [--no-verify]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Task", "WebSearch", "WebFetch"]
context: fork
model: sonnet
effort: medium
---

# `/competitive-exam-questions` — Verified PYQs + Original Exam-Pattern Questions

Generate a competitive-exam practice set for a finished lecture as two LaTeX files: a **questions** file (no answers) and an **answers** file (correct option/value + a one-line justification). The exam target defaults to **GATE (Computer Science)** for this course — the relevant competitive exam for a B.Tech CS student — but is a parameter, not hard-coded, so a forked instance of this template can point it at a different exam.

**Input:** `<CODE>/<lecture>`, optionally `--exam <name>` (default `GATE-CS`).

**The core discipline: never present an unverified claim as a real past-year question.** Every question labeled as a real PYQ must survive independent verification (Chain-of-Verification, same pattern `/lit-review` uses for citations); every question that doesn't find a verified match is labeled as original, never silently passed off as authentic.

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
- Read `Slides/<CODE>/<lecture>.tex` and, if it exists, `Notes/<CODE>/<lecture>-notes.tex` to build a list of the lecture's specific sub-topics (e.g., for `06-hardwired-control`: sequence counter design, opcode decoding, state-table-to-Boolean-equation derivation, AND-OR gate realization, hardwired vs. microprogrammed trade-offs).
- Produce a short Pre-Flight note: topic list, target exam (default GATE-CS), and target count (default 6-8 questions, mixing MCQ and Numerical-Answer-Type if the target exam uses both — GATE CS does).

## Phase 1: Search for and verify real past-year questions

For each sub-topic, `WebSearch` for a matching real question (e.g., `"GATE CS" "sequence counter" OR "control unit" previous year question`). A candidate is only a **draft** claim at this point, not a fact.

**Extract claims, then verify independently (CoVe):**

1. For each candidate PYQ, extract the claim precisely: exact question text (or close paraphrase if the source paraphrases it), the exam year, and the correct answer/option.
2. Spawn `claim-verifier` via `Task` (`subagent_type: claim-verifier`, `context: fork`) with the claims + source URLs — never pass a draft narrative, only the claims table and pointers, per `.claude/rules/post-flight-verification.md`.
3. **CONFIRMED** → include as `[GATE CS <year>, verified]`.
4. **CANNOT-VERIFY or CONTRADICTED** → do not include it as a real PYQ. Either drop it or, if the underlying topic is still worth testing, rewrite it from scratch as an original question (Phase 2) — never ship a "verified" label on a claim that didn't actually verify.

## Phase 2: Fill remaining topics with original, exam-pattern questions

For sub-topics with no verified real match, write an original question in the target exam's own format (for GATE CS: single-correct MCQ or Numerical-Answer-Type, calibrated to real GATE difficulty for that topic — GATE CS control-unit/datapath questions are typically 1-2 mark numerical or short-reasoning items, not multi-part derivations). Label these `[Original, GATE-pattern]` — never attribute a specific year or claim it appeared in a real exam.

## Phase 3: Write the files

`CompetitiveExam/<CODE>/<lecture>-questions.tex` (student-facing, no answers) and `CompetitiveExam/<CODE>/<lecture>-answers.tex` (correct option/value + a one-line justification per question) — same chapter-style LaTeX conventions as `/lecture-notes` and `/create-assignment`:

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}
\renewcommand{\thesection}{<N>.\arabic{section}}   % <N> = this lecture's week number

\title{Competitive Exam Practice <N>: <Lecture Title>\\\large GATE (Computer Science) Pattern}
\author{PCC CS-401: Computer Organization and Architecture}
\date{\today}

\begin{document}
\maketitle
% each question prefixed with its provenance tag, e.g.:
% \textbf{Q1} \textit{[GATE CS 2019, verified]} ...
% \textbf{Q2} \textit{[Original, GATE-pattern]} ...
\end{document}
```

The provenance tag is not optional decoration — it is the load-bearing distinction between "this is authentic" and "this is practice material in the same style." Compile the same way as Notes/Assignments: `TEXINPUTS`/`BIBINPUTS` relative to `CompetitiveExam/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Phase 4: Report

State: question count by provenance (verified PYQ vs. original), the years/sources of any verified PYQs, the CoVe outcome (PASS/PARTIAL/FAIL per `post-flight-verification.md`'s output contract), and the two file paths written.

## Flags

- `--exam <name>` — target competitive exam (default `GATE-CS`). Determines the question format used in Phase 2 (GATE CS: single-correct MCQ and Numerical-Answer-Type) and the search terms used in Phase 1. Change this to point the skill at a different exam for a different course/context.
- `--no-verify` — skip Phase 1's web search entirely and write an all-original, exam-pattern set. Use when speed matters more than authenticity, or the topic is too niche for PYQs to plausibly exist.

## Cross-references

- `.claude/rules/post-flight-verification.md` — the CoVe protocol this skill's Phase 1 implements directly (same pattern as `/lit-review`).
- `.claude/skills/lit-review/SKILL.md` — the sibling skill this borrows the search-then-verify discipline from.
- `.claude/agents/claim-verifier.md` — the forked verifier spawned in Phase 1.
- `.claude/skills/create-assignment/SKILL.md` — the sibling skill for graded (non-competitive-exam) practice material.
- `.claude/rules/textbook-grounding.md` — the same "cite what you can back, phrase honestly otherwise" principle, applied to exam provenance instead of textbook pages.
