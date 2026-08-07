---
name: create-assignment
description: Scaffold a graded assignment (LaTeX PDF, course-organized) for a finished lecture — Conceptual, Numerical, and Design problems, sourced from the Beamer deck and Notes, with a clean student set and a separate solution key. Use when user says "make an assignment for this lecture", "create a problem set for week N", "build an assignment course-wise", "generate homework with an answer key" for a CS401-style engineering course. NOT for economics/empirical coursework (use `/scaffold-exercises` for that — analytical/empirical/coding problem types, R/Stata solutions).
argument-hint: "[CourseCode/lecture], e.g. CS401/06-hardwired-control (Slides/CourseCode/lecture.tex must already exist and compile)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/create-assignment` — Engineering Problem-Set Scaffolder

Generate a graded assignment for a finished lecture as two LaTeX files: a clean **student set** (problems only, no answers) and a **solution key** (worked solutions). Sibling to `/scaffold-exercises`, which does the same job for economics coursework (analytical/empirical/coding, R/Stata) — this skill is for engineering courses (CS401-style: digital logic, computer organization, and similar), where the natural problem types are **Conceptual, Numerical, and Design**, not derive/estimate/code.

**Input:** `<CODE>/<lecture>`, e.g. `CS401/06-hardwired-control`.

## Problem types

| Type | What the student does | Solution artifact |
|---|---|---|
| **Conceptual** | Explain, justify, or compare (why a design choice was made, what a component does and doesn't do, trade-off reasoning) | A full-sentence explanation, same rigor as the Notes' prose |
| **Numerical** | Compute a concrete value (an effective address, a cycle count, a control-word bit pattern, a Boolean-equation truth value) | The worked arithmetic/derivation, step by step, ending in the number |
| **Design** | Derive a state table, a set of Boolean control equations, or sketch a datapath/control-unit decision for a *new* instruction or scenario not explicitly worked in the lecture | The derivation, following the same method the lecture used on its own worked example |

Every assignment should mix at least two of the three types; Design problems are the most valuable for testing whether a student can extend the lecture's method to a new case, not just recall it.

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles (a `.pdf` alongside it).
- Read `Slides/<CODE>/<lecture>.tex` end-to-end (or `Notes/<CODE>/<lecture>-notes.tex` if it already exists — prefer the Notes chapter since it is already topic-organized and has the citations resolved).
- Note: every definition, worked example, and notation the lecture actually introduces (problems must reuse this notation, never introduce a clashing symbol); every citation the lecture carries (a Design problem that extends a book-grounded method should carry the same citation, not a new unverified one).
- Produce a short Pre-Flight note: topic, problem count by type (default 6: 2 Conceptual, 2 Numerical, 2 Design), and the 2-4 learning objectives the set should exercise (these should map to the lecture's own stated objectives, not invented ones).

## Phase 1: Generate problems

For each problem: a number, the prompt, and any data/notation it needs.

- **Motivation before mechanics** — one clause on why the problem matters, matching the lecture's own motivate-before-formalize convention (`content-invariants.md` INV-8).
- **Notation reuse** — match symbols to the source lecture exactly (`SC`, `D_i`, `T_j`, `EA`, register names, etc.) — never introduce a clashing symbol for an already-defined object.
- **Self-contained** — each problem states its own assumptions; no "as discussed in class" dangling references. A student should be able to answer it from the Notes chapter alone.
- **Extend, don't repeat** — a Design or Numerical problem should apply the lecture's method to a *new* instruction/scenario/register set the lecture didn't itself work through (e.g., if the lecture traced `R1 <- R2+R3`, the assignment might ask for `R4 <- R5-R6`), not re-ask the exact worked example verbatim.
- **Nothing invented** — every fact a problem relies on (a book-cited convention, a specific figure's structure) must trace to the source lecture or its own citations; do not assert a textbook claim the lecture doesn't already carry.

## Phase 2: Generate worked solutions

For every problem, write a full worked solution in the same derivation style as the lecture's own worked examples (step-by-step, ending in the answer for Numerical/Design; a complete paragraph for Conceptual) — no shortcuts, no "left as an exercise."

## Phase 3: Write the files

`Assignments/<CODE>/<lecture>-assignment.tex` (student set) and `Assignments/<CODE>/<lecture>-solutions.tex` (solution key) — XeLaTeX `article` class, same chapter-style numbering convention as `/lecture-notes` (see `.claude/skills/lecture-notes/SKILL.md` Phase 3):

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}
\renewcommand{\thesection}{<N>.\arabic{section}}   % <N> = this lecture's week number

\title{Assignment <N>: <Lecture Title>}
\author{PCC CS-401: Computer Organization and Architecture}
\date{\today}

\begin{document}
\maketitle
\section{Conceptual}
% numbered problems, no answers
\section{Numerical}
\section{Design}
\bibliography{../../Bibliography_base}
\bibliographystyle{plain}
\end{document}
```

The solution key mirrors the same section/problem numbering, restating each problem in one line before its worked solution — never assume the reader has the student file open side by side.

**The split is load-bearing: never leak a solution into the student file.**

Compile the same way as Notes: `TEXINPUTS`/`BIBINPUTS` = `../../Preambles` / `../..` relative to `Assignments/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Phase 4: QA

Spot-check (no separate critic/fixer loop needed for a first pass — this is lower-stakes than Lecture Notes since it's new content, not a derivation of existing content that must preserve parity):
- Every problem is answerable from the source lecture/Notes chapter alone.
- No symbol clashes with the lecture's notation registry (`knowledge-base-<CODE>.md`).
- The student file contains zero worked solutions or final answers.

## Report

State: problem count by type, learning objectives exercised, and the two file paths written.

## Cross-references

- `.claude/skills/scaffold-exercises/SKILL.md` — the sibling pattern this borrows the Pre-Flight/split-file discipline from (economics-flavored; this skill is the engineering-course counterpart).
- `.claude/skills/lecture-notes/SKILL.md` — the source-reading convention and chapter-style LaTeX numbering this skill reuses.
- `.claude/rules/textbook-grounding.md`, `.claude/rules/content-invariants.md` (INV-8) — sourcing and motivation-before-formalism discipline applied to problems, not just lecture content.
