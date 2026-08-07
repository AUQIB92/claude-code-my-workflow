---
name: instructor-handout
description: Build an instructor-only prep handout (LaTeX PDF, course-organized) for a finished lecture — extra worked examples beyond the student Notes, delivery/teaching notes (emphasis points, common misconceptions, board-work suggestions), and a page-cited "before you teach this" self-study reading list. Use when user says "make an instructor handout for this lecture", "instructor prep notes course-wise", "teaching notes for week N", "what should I read before teaching this". NOT student-facing material (use `/lecture-notes` for that) and NOT a source of new facts — worked examples and citations must trace to the lecture/indexed textbooks; only the delivery-notes section is instructor judgment, and it is labeled as such.
argument-hint: "[CourseCode/lecture], e.g. CS401/06-hardwired-control (Slides/CourseCode/lecture.tex and, ideally, Notes/CourseCode/lecture-notes.tex should already exist)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/instructor-handout` — Teaching Prep, Not Student Material

Generate a single instructor-only LaTeX handout for a finished lecture: extra worked examples the instructor can draw on beyond what students see, concrete delivery notes, and a page-cited list of what to read before teaching. This is a sibling to `/lecture-notes` (student-facing textbook chapter), `/create-assignment`, and `/competitive-exam-questions` (both course-wise, both student/answer-key split) — this skill has no split, because there is no student-facing half to keep separate from.

**Input:** `<CODE>/<lecture>`, e.g. `CS401/06-hardwired-control`.

## The three sections, and what governs each

| Section | Content | Grounding rule |
|---|---|---|
| **Extra worked examples** | 1-2 additional worked examples per major topic, beyond what the Notes/Assignment already cover — different registers/instructions, same method | Same discipline as `/lecture-notes`: nothing invented, every method traces to the lecture; a genuinely new instance, not a copy of an existing worked example with names changed superficially |
| **Delivery notes** | Emphasis points, common misconceptions, board-work sequence, live discussion questions, pacing cues | **Instructor judgment, not fact** — grounded in the lecture's own content and this project's teaching-craft conventions (motivation-before-formalism, Socratic questioning — `content-invariants.md` INV-8), but explicitly not citation-checkable, and labeled as such so it is never confused with textbook-sourced content |
| **Self-study reading list** | Which indexed textbook sections to read before teaching, and why | `.claude/rules/textbook-grounding.md`, exactly as everywhere else: page-cite only what's in `supporting_books/*/index.md`; for anchor readings with no index yet (this course's Hamacher/Stallings), phrase as chapter-level/general, never invent a page |

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
- Read `Slides/<CODE>/<lecture>.tex` end-to-end.
- Read `Notes/<CODE>/<lecture>-notes.tex` if it exists — this tells you what worked examples and definitions students already have, so Phase 1's additions are genuinely additive, not redundant.
- Read `Assignments/<CODE>/<lecture>-*.tex` if it exists, for the same reason (don't duplicate an assignment problem as an "extra worked example").
- Read the lecture's anchor-reading comment block and cross-check against `master_supporting_docs/<CODE>/supporting_books/*/index.md` to know exactly which sections/pages are indexed (real page citations available) versus general-treatment-only.

## Phase 1: Extra worked examples

For each major topic that already has one worked example in the Notes, write one \emph{additional} worked example: same method, a different concrete instance (different registers, a different instruction from the same family, a boundary case). Write it at instructor-prep depth — include a sentence or two of reasoning an instructor might need to field an unplanned student question about it, not just the final answer.

## Phase 2: Delivery notes

For each major section, write 2-4 short bullets under a clearly-labeled "Teaching Notes" heading:
- A misconception students commonly bring to this specific point (grounded in what the concept is most often confused with, e.g., confusing $D_i$ with $T_j$, or confusing indirect with register-indirect addressing).
- A board-work suggestion (what to physically draw, and in what order, so the diagram builds up the way the reasoning does).
- A question worth posing to the class live, distinct from the Socratic questions already in the slide deck (don't just copy the deck's own Socratic-check frames verbatim).
- A pacing note where relevant (which derivation typically needs a second pass).

Prefix this section (once, at the top of the document) with a one-line disclaimer: *these are instructional suggestions, not facts to be tested — adapt freely to your own classroom.*

## Phase 3: Self-study reading list

At the top of the document, before the worked examples, a **"Before You Teach This Lecture"** box: for each anchor textbook, list the specific indexed section(s) (with page range, from `index.md`) worth reading in full, and one sentence on what depth/context it adds beyond the slides. For anchor readings without an index yet, list the citation honestly at chapter level with a note that it's not yet page-indexed (matching how the Beamer decks themselves already phrase unindexed citations) — never fabricate a page number to make this section look more complete than it is.

## Phase 4: Write the file

`InstructorHandouts/<CODE>/<lecture>-instructor-handout.tex` — XeLaTeX `article` class, same chapter-style numbering convention as `/lecture-notes`/`/create-assignment`:

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}
\renewcommand{\thesection}{<N>.\arabic{section}}   % <N> = this lecture's week number

\title{Instructor Handout <N>: <Lecture Title>}
\author{PCC CS-401: Computer Organization and Architecture}
\date{\today}

\begin{document}
\maketitle
{\centering\large\color{negative}\textbf{Instructor Copy --- Not for Student Distribution}\par}
\vspace{0.5cm}

\section{Before You Teach This Lecture}
% self-study reading list (Phase 3)

\section{Extra Worked Examples}
% Phase 1 content, organized by the same topics Notes/<lecture>-notes.tex uses

\section{Teaching Notes}
% Phase 2 content, one subsection per major topic
\end{document}
```

No `\bibliography`/`\cite` is needed unless a worked example directly quotes a textbook claim not already covered by the Notes' own citations — prefer citing textbook sections in prose (as in Phase 3's reading list) over BibTeX machinery for this document.

Compile the same way as Notes/Assignments: `TEXINPUTS`/`BIBINPUTS` relative to `InstructorHandouts/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Report

State: number of extra worked examples added, number of teaching-note bullets, which anchor-reading sections were page-cited vs. left general, and the file path written.

## Cross-references

- `.claude/skills/lecture-notes/SKILL.md` — the source-reading and chapter-numbering convention this skill reuses; also the definitive list of what students already have, so this skill doesn't repeat it.
- `.claude/skills/create-assignment/SKILL.md`, `.claude/skills/competitive-exam-questions/SKILL.md` — sibling course-wise, per-lecture deliverables.
- `.claude/rules/textbook-grounding.md` — the citation-honesty discipline for Phase 3.
- `.claude/rules/content-invariants.md` (INV-8) — motivation-before-formalism, the same principle behind this course's Socratic-question convention that Phase 2's delivery notes draw on.
