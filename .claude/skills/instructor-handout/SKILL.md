---
name: instructor-handout
description: Build a complete, self-contained instructor teaching guide (LaTeX PDF, course-organized) for a finished lecture — full topic-by-topic explanations woven together with diagram walkthroughs (what to draw and how to present it), worked examples, common-misconception callouts, and a page-cited "before you teach this" self-study reading list, all in one document an instructor can teach directly from without needing the slides or Notes open. Use when user says "make an instructor handout for this lecture", "instructor prep notes course-wise", "complete teaching guide for week N", "what should I read and how should I teach this". NOT student-facing material (use `/lecture-notes` for that) and NOT a source of new facts — explanations, diagrams, and citations must trace to the lecture/indexed textbooks; only the delivery commentary (misconceptions, board sequencing, live questions) is instructor judgment, and it is visually distinguished from the explanatory content, not a separate bolted-on section.
argument-hint: "[CourseCode/lecture], e.g. CS401/06-hardwired-control (Slides/CourseCode/lecture.tex and, ideally, Notes/CourseCode/lecture-notes.tex should already exist)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: medium
---

# `/instructor-handout` — One Complete, Self-Contained Teaching Document

Generate a single instructor-only LaTeX handout that is genuinely sufficient to teach the lecture from directly — no slides, no separate Notes file needed open at the same time. This is **not** a light supplement that assumes the instructor already has the Notes and slides in front of them; it is the full explanation, woven together with presentation guidance, in one place.

**Input:** `<CODE>/<lecture>`.

## Why this is one document, not several

An earlier iteration of this skill split "extra worked examples," "teaching notes," and diagram-presentation guidance into separate, terser sections, and a second iteration split diagram-presentation into an entirely separate "board script" document. Both were rejected: the instructor wants to open **one file** and have everything — the explanation, the diagram, how to draw it, what students get confused about, what to ask — for a given topic, together, before moving to the next topic. Structure the handout by **topic**, not by content-type.

## The topic unit (repeat this shape for every major topic in the lecture)

For each topic/diagram/derivation, in the order the lecture presents them, write one self-contained block containing, woven into continuous prose (not separate labeled subsections unless the material genuinely needs the separation):

1. **The full explanation** — the same depth and rigor as `/lecture-notes` would write (every derivation step spelled out, motivation before formalism), because the instructor should not need to also have the Notes open.
2. **The diagram, embedded** — reuse the exact TikZ code from the Beamer source verbatim (already `tikz-reviewer`-approved; don't re-derive it), as a real numbered figure. **Run the P7 clearance audit** (`.claude/rules/tikz-prevention.md`) on each embedded diagram before compiling: no path crossing a box except at a connection point (P7a), no label on a line (P7b), labels ≥0.15 cm clear of box edges (P7c), no curve visibly crossing its own dashed asymptote (P7d). Fix any finding in the Beamer source first, then port the corrected diagram to the handout — the deck is the single source of truth, and the corrected diagram must ship in all three copies (deck, Notes, handout) identically.
3. **How to present it** — folded in immediately after or alongside the diagram, not deferred to an end-of-document section: what to draw first vs. second (reuse the diagram's own coordinate-map comment, `tikz-prevention.md` Rule P2, as the real build order), and the line of explanation that goes with each stage, written as continuous guidance an instructor can read once and internalize, not a terse bullet.
4. **Where students get stuck** — a specific, concrete misconception or error pattern for *this* topic, folded in at the point it's relevant, not batched into a generic list.
5. **A question worth asking live** — where it naturally fits the explanation's flow (often right before revealing an answer the explanation is about to give).
6. **An extra worked example**, if this topic already has one worked example in the Notes — a genuinely different instance (different registers/instructions), so the instructor has a second one ready without inventing it live.

## Grounding rules (unchanged from before)

- **Explanations, diagrams, and worked examples must trace to the lecture** (Slides/Notes) — nothing invented, no new facts. This is still, structurally, a derived artifact like Notes, just instructor-voiced and delivery-annotated.
- **The self-study reading list is still page-cited** exactly per `.claude/rules/textbook-grounding.md`: real pages only for what's actually indexed in `supporting_books/*/index.md`; honest chapter-level phrasing for anchor readings that aren't indexed yet. Never invent a page number.
- **Delivery commentary (misconceptions, live questions, board sequencing) is instructor judgment**, not fact-checkable content — but instead of isolating it in its own section, distinguish it visually inline (e.g., an indented, differently-styled aside) so it's still clearly separable from the sourced explanation, without breaking the single-document, single-read-through experience.

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
- Read it end-to-end, plus `Notes/<CODE>/<lecture>-notes.tex` if it exists (reuse its prose and topic organization as the explanatory backbone — don't re-derive from scratch what Notes already got right).
- Read the anchor-reading comment block and cross-check `supporting_books/*/index.md` for what's actually page-indexed.

## Phase 1: Write the file, one topic block at a time

`InstructorHandouts/<CODE>/<lecture>-instructor-handout.tex` — XeLaTeX `article`, same chapter-style section numbering as `/lecture-notes`:

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}
\renewcommand{\thesection}{<N>.\arabic{section}}
\renewcommand{\thefigure}{<N>.\arabic{figure}}
\newtheorem{example}{Example}[section]
\newenvironment{definitionbox}[1]{\par\noindent\textbf{Definition (#1).}\ \itshape}{\par\vspace{0.3em}}
% A visually distinct "teaching aside" for delivery commentary, inline with
% the topic it belongs to rather than batched into a separate section.
\newenvironment{teachingaside}{\begin{quote}\small\color{primary-gold}\textbf{Teaching note:}\ }{\end{quote}}

\title{Instructor Handout <N>: <Lecture Title>}
\author{PCC CS-401: Computer Organization and Architecture}
\date{\today}

\begin{document}
\maketitle
{\centering\large\color{negative}\textbf{Instructor Copy --- Not for Student Distribution}\par}
\vspace{0.5cm}

\section{Before You Teach This Lecture}
% self-study reading list, page-cited where indexed

\section{<Topic 1>}
% full explanation, embedded figure with presentation guidance woven in,
% \begin{teachingaside}...\end{teachingaside} asides at the points they're
% relevant, an extra worked \begin{example}...\end{example} if applicable

\section{<Topic 2>}
% ...

\section{Summary}
% a one-page-scale recap: key definitions, equations, and results, for a
% fast pre-class refresh
\end{document}
```

No `\bibliography`/`\cite` needed unless quoting a specific textbook claim; prefer prose citations in the reading list.

Compile the same way as Notes: `TEXINPUTS`/`BIBINPUTS` relative to `InstructorHandouts/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Report

State: topics covered, extra worked examples added, teaching asides included, self-study sections page-cited vs. general, and the file path written.

## Cross-references

- `.claude/skills/lecture-notes/SKILL.md` — the explanatory backbone and chapter-numbering convention this skill reuses and extends with delivery guidance.
- `.claude/skills/create-assignment/SKILL.md`, `.claude/skills/competitive-exam-questions/SKILL.md` — sibling course-wise, per-lecture deliverables.
- `.claude/rules/textbook-grounding.md` — the citation-honesty discipline for the self-study reading list.
- `.claude/rules/tikz-prevention.md` Rule P2 — the coordinate-map-comment convention used for "how to present it" diagram build order.
