---
name: lab-manual
description: Generate a per-week lab sheet (LaTeX PDF, course-organized) for the practical/lab component of a course — objective, apparatus/toolchain, step-by-step procedure, expected output, an observation table for students to fill in, viva-voce questions, and a grading rubric. Use when user says "make a lab manual", "create a lab sheet for week N", "build the practical for this lecture", "generate a lab exercise" for a course with an L-T-P (lecture-tutorial-practical) or similar lab component. NOT for a graded written assignment (use /create-assignment) and NOT for a programming assignment with an autograder (use /coding-assignment) — a lab sheet is an in-session, apparatus-driven exercise a student performs and records, typically supervised.
argument-hint: "[CourseCode/lecture], e.g. CS401/02-number-systems-arithmetic (Slides/CourseCode/lecture.tex must already exist and compile)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/lab-manual` — Practical/Lab Sheet Generator

Generate one week's lab sheet for the practical component of a course whose syllabus carries a lab (an L-T-P scheme, a "Practical" assessment line, or an explicit lab session). Closes a documented gap: `syllabi/CS401.md` states outright that its L-T-P 3-0-2 practical component "is run as a separate weekly lab session and is not scheduled above — pair with a lab manual if you want it mapped into this workflow," and the practical line carries 25% of the total grade (50 of 200 marks) with zero tooling behind it before this skill.

**Input:** `<CODE>/<lecture>`, e.g. `CS401/02-number-systems-arithmetic`. The lab sheet is derived from — and stays tied to — the matching lecture, the same relationship `/create-assignment` and `/lecture-notes` have to `Slides/<CODE>/<lecture>.tex`.

## What a lab sheet is (and isn't)

A lab sheet is an **in-session, apparatus-driven exercise**: the student follows a procedure, produces an observable result, records it, and answers viva questions about *why* the procedure works — not a take-home problem set (`/create-assignment`) and not an autograded program (`/coding-assignment`). For a hardware/organization course (CS401-style), the "apparatus" is often a simulator, an HDL toolchain, or a hand-executed trace on paper; for a data-structures course (CS301-style), it is usually a small program the student writes and runs to observe a data structure's behavior directly.

## Phase 0: Pre-Flight

1. Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
2. Read the lecture (prefer `Notes/<CODE>/<lecture>-notes.tex` if it exists — already topic-organized) and `syllabi/<CODE>.md` for the practical component's stated scope and weighting.
3. Identify the **apparatus/toolchain** the lecture's content implies: a logic-gate simulator (Logisim, CircuitVerse) for a digital-logic week; a small C/Python program for a data-structures week; a spreadsheet or hand-trace for a numeric-encoding week. If the syllabus or prior lab sheets already establish a toolchain, reuse it — don't introduce a second tool mid-course without the user's say-so.
4. Produce a short Pre-Flight note: apparatus/toolchain, the 1-2 learning objectives the lab exercises (tie to the lecture's own stated objectives, not invented ones), and estimated session length.

## Phase 1: Write the procedure

- **Objective** — one sentence, an observable verb (build, trace, measure, verify), tied to the lecture's own learning objective.
- **Apparatus/toolchain** — named exactly, with version/setup notes if it matters (e.g. "any C99 compiler," "Logisim Evolution 3.x").
- **Procedure** — numbered steps, each producing a checkable intermediate result. Mirror the lecture's own worked-example method (`content-invariants.md` INV-8: motivate before mechanics) rather than inventing an unrelated exercise.
- **Expected output** — what the student should see if the procedure is followed correctly (a truth table, a program's console output, a waveform, a specific numeric result) — concrete enough that a wrong result is immediately visible to the student, not just to the grader.

## Phase 2: Observation table + viva questions

- **Observation table** — a blank table (LaTeX `tabular`, ruled for handwriting if the lab is done on paper, or a results-to-fill-in table if done at a computer) the student completes during the session. Every row should map to a specific procedure step.
- **Viva-voce questions** (3-5) — short-answer questions a lab instructor would ask to confirm the student understands *why* the procedure works, not just that they followed steps. Pull from the lecture's own conceptual content — a viva question should be answerable from the Notes chapter, never require outside material.

## Phase 3: Rubric

A short table: criteria (procedure followed correctly / observation table complete / viva answered correctly) × point bands, summing to the practical component's per-lab weight if the syllabus specifies one, otherwise a generic 100-point scale the instructor rescales.

## Phase 4: Write the file

`Labs/<CODE>/<lecture>-lab.tex` — XeLaTeX `article` class, same chapter-numbering convention as `/lecture-notes` and `/create-assignment`:

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}
\renewcommand{\thesection}{<N>.\arabic{section}}   % <N> = this lecture's week number

\title{Lab <N>: <Lecture Title>}
\author{<Course Title>}
\date{\today}

\begin{document}
\maketitle
\section{Objective}
\section{Apparatus / Toolchain}
\section{Procedure}
\section{Observation Table}
\section{Viva-Voce Questions}
\section{Rubric}
\end{document}
```

Compile the same way as Notes/Assignments: `TEXINPUTS`/`BIBINPUTS` = `../../Preambles` / `../..` relative to `Labs/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Phase 5: QA

Spot-check:
- Objective ties to a real, stated lecture objective (not invented).
- Every observation-table row maps to an actual procedure step.
- Every viva question is answerable from the lecture's own Notes chapter.
- Toolchain is named specifically enough that a student who has never used it can get started (link/version noted).

## Report

State: apparatus/toolchain, learning objective, procedure step count, and the file path written.

## Cross-references

- `.claude/skills/create-assignment/SKILL.md` — the written-problem-set sibling; shares the Pre-Flight/chapter-numbering conventions this skill reuses.
- `.claude/skills/coding-assignment/SKILL.md` — the autograded-program sibling, for take-home programming work rather than a supervised in-session lab.
- `.claude/skills/syllabus/SKILL.md` — where the practical component's weighting and cadence are declared; read this before Phase 0 if the course's `syllabi/<CODE>.md` doesn't already state the lab schedule.
- `.claude/rules/content-invariants.md` (INV-8) — motivation-before-mechanics discipline applied to the procedure, same as `/create-assignment`.
