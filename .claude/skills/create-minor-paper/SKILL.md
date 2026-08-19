---
name: create-minor-paper
description: Assemble an internal institutional sessional "Minor" exam paper — GCET Ganderbal's exact exam-class two-copies-per-sheet format (crest header, Time/Semester/Max-Marks/Min-Marks line, Section A/B via the exam class's \question environment) — spanning a specified range of weeks. Fixed pattern: Section A (three questions x 10 marks, attempt any two = 20) and Section B (three questions x 5 marks, attempt any two = 10), 30 marks total, min marks 40% (12). Every question blends a conceptual sub-part with a numerical/design sub-part on one topic (matching the institution's own question style), freshly written — a different concrete instance than that week's already-generated /create-assignment or /competitive-exam-questions output, even when grounded in the same concept. Use when user says "make a Minor paper", "generate the sessional exam for weeks N-M", "create Minor 1", "build the internal exam paper for Unit II". This is the fixed, permanent format for every course in this repo, not a one-off — do not revert to a plain article-class layout. NOT for a single-lecture graded assignment (use /create-assignment) and NOT for a GATE-pattern practice set (use /competitive-exam-questions) — both are single-week and their student-facing output is public/tracked; a Minor paper spans multiple weeks and is a real, live exam, so both the paper and its solutions are gitignored end-to-end, never committed, never deployed to docs/.
argument-hint: "<CourseCode>/<PaperLabel> --weeks N-M (or --unit I|II|III) [--month <Month Year>] [--no-verify], e.g. CS401/minor-1 --unit I --month July 2026"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: high
---

# `/create-minor-paper` — Multi-Week Sessional Exam Paper (GCET Ganderbal Format)

Assemble an internal "Minor" exam paper — a real, live sessional exam, not public study material — spanning a range of weeks rather than one lecture, printed in the institution's own two-copies-per-sheet `exam`-class layout. This is the first skill in this template that sources content across multiple weeks at once; every other course-content skill (`/create-assignment`, `/competitive-exam-questions`) is strictly single-lecture. Both the question paper and its solution key are gitignored end-to-end: they never reach `docs/`, and they never reach a public GitHub repo before or after the exam is administered.

**Input:** `<CODE>/<PaperLabel>` plus exactly one of `--weeks N-M` or `--unit I|II|III`, e.g. `CS401/minor-1 --unit I` or `CS401/minor-2 --weeks 6-9`. Optional `--month "<Month Year>"` for the header line (defaults to the current month/year).

## The fixed pattern (reproduce verbatim, never paraphrase)

```
Paper Pattern of Minor — Maximum Marks: 30
Section A: (10 x 2 = 20 marks) — Section A shall comprise three questions; candidates shall attempt any two. Each question carries 10 marks.
Section B: (5 x 2 = 10 marks) — Section B shall comprise three questions; candidates shall attempt any two. Each question carries 5 marks.
```

Three questions set per section, two required, marks as stated. **Min Marks is always 40% of Max Marks, rounded** — 30 marks → 12 min marks — apply this formula every time, even if a future course's Minor paper ever used a different Max Marks total.

## The institutional header format (fixed, permanent — this is not a one-off style choice)

Every Minor paper for every course in this repo uses:
- **Document class:** `exam` (9pt, a4paper, tight 0.25in/0.4in margins) — never `article` for this artifact type. `article` remains correct for `/create-assignment`, `/competitive-exam-questions`, and every other skill; only Minor papers use `exam`.
- **Crest + header block:** `Preambles/CUL.png` (the GCET Ganderbal crest, committed — logos aren't copyrighted student content, unlike textbook PDFs) on the left, institution/department/course/paper-label text centered on the right, exactly as shown in the skeleton below.
- **Institution and department are fixed constants** for this repo: "Govt. College of Engineering \& Technology Ganderbal, J\&K" and "Dept. of Computer Science \& Engineering" — every course here is the same institution and department. Course title, code, and semester are **parsed live from `syllabi/<CODE>.md`'s H1 line** (`# <Title> (<CODE>) — <Program>, Semester <N>` — e.g. `# Computer Organization and Architecture (PCC CS-401) — B.Tech CSE, Semester 4`), never hardcoded per course.
- **Two scaled copies per sheet**, separated by a dashed cutting line with a scissors glyph — a real print-cost convention (two students' papers per physical sheet), reproduced via `\newcommand{\examcontent}{...}` wrapping the whole paper body once, then two `\adjustbox{valign=t,scale=0.88,minipage={\textwidth}}{\examcontent}` invocations with `\cuttingline` between them.
- **Questions use the `exam` class's `\question`/`\begin{questions}...\end{questions}` environment**, not manual `\begin{enumerate}`. Section B's numbering resumes from Section A via `\setcounter{question}{3}` (never restart at 1) — matches the institution's own convention of numbering questions 1-6 straight through both sections despite the `\begin{questions}` environment resetting per section.

## Phase 0: Pre-Flight

1. Parse `$ARGUMENTS`. `PaperLabel` is a free instructor-supplied kebab-case identifier (`minor-1`, `minor-2`) — the human-readable "Minor N" number for the header is extracted from its trailing digits (`minor-2` → "Minor 2"; if the label carries no digit, ask the instructor for the Minor number explicitly rather than guessing). Reject if neither or both of `--weeks`/`--unit` are given; nothing is written on this error.
2. **Resolving `--unit I|II|III`** (sugar over `--weeks`, computed live every run — never hardcoded): read `syllabi/<CODE>.md`, scan Learning Objectives `(Weeks? N[-M])` tags and the Weekly Schedule's `**Class Test N**` rows to derive Unit boundaries (Unit 1 = `1..(1st Class Test week)`, Unit *k* = `(previous Class Test week + 1)..(kth Class Test week)`). If the requested unit letter has no matching Class Test row in *this course's* syllabus, stop and ask for `--weeks` directly rather than guessing.
3. Parse `syllabi/<CODE>.md`'s H1 line for course title, code, and semester (see the format above) — these feed the header block. Stop with a clear error if the H1 doesn't match the expected shape rather than emitting a header with blank fields.
4. For every week in the resolved range, confirm the syllabus's Week → lecture work-list names a deck, and that `Slides/<CODE>/<deck>.tex` exists with a compiled `.pdf` alongside it. **Any missing week is a hard stop.** Prefer `Notes/<CODE>/<deck>-notes.tex` over the raw deck when it exists.
5. Confirm `Preambles/CUL.png` exists (it should, as a tracked repo asset). If it's ever missing, stop and ask the instructor to restore it rather than silently omitting the crest — a Minor paper with a missing image is not a shippable document.
6. Emit a Pre-Flight note: resolved week range (+ unit, if used), deck list, paper label, resolved "Minor N", resolved month/year, resolved course title/code/semester, both output paths (flagged **gitignored, never public**), and the fixed target — 3 Section A questions (10 marks each) + 3 Section B questions (5 marks each).

## Phase 1: Multi-week sourcing and topic allocation

1. **Per-week subtopic extraction.** For every week in range, read its Slides (+ Notes if present) and extract a distinct-subtopic list, each tagged with its source week.
2. **Build the avoid-list.** For every week in range, read that week's already-generated `Assignments/<CODE>/<deck>-assignment.tex` and `CompetitiveExam/<CODE>/<deck>-questions.tex`, and record every concrete question stem — the specific numbers, register names, or scenario asked, not just the topic name.
3. **Allocate the 6 slots by largest-remainder apportionment**: let `N_w` be week `w`'s distinct-subtopic count and `weight_w = N_w / sum(N)`; apportion 6 total slots across the weeks in range using the largest-remainder (Hamilton) method on those weights.
4. **Coverage floor.** For ranges of 6 weeks or fewer, force a minimum of 1 slot per week, topping up any week that rounds to 0 from the largest-remainder pool. For ranges over 6 weeks, disclose any zero-slot week explicitly in the report — never silently drop it.
5. **Concentration flag (advisory).** If any single week supplies more than half of one section's 3 questions, note this explicitly in the report.
6. **One coherent topic per slot, not a depth-split.** Unlike a plain problem set, each allocated slot picks **one topic** from its week and turns it into a single multi-angle question spanning that topic — matching the institution's own style, where a question is never purely abstract nor purely mechanical but walks the topic from explanation through to a worked instance. Do not route "deep" subtopics to Section A and "shallow" ones to Section B as separate buckets; instead, size the SAME kind of multi-angle question to the section's mark budget (Section A gets richer, more heavily-computed topics; Section B gets topics that resolve in one clean concept-plus-quick-computation pass).

## Phase 2: Question writing — the institution's per-question style

Every question blends a **conceptual sub-part** (define/explain/justify, no computation) with a **numerical or design sub-part** (compute a concrete value, convert a specific input, apply an algorithm to fresh data) on the *same* topic, with per-sub-part marks shown via `\hfill (X, Y[, Z] Marks)` summing to the question's total. This mirrors the institution's real papers exactly — reread the shape before writing:

- *Booth's Algorithm*: explain the algorithm (3) + compute a signed 4-bit example (5) + explain a design rationale (2) — **3 parts, 10 marks total**.
- *Amdahl's Law*: explain the law (5) + compute a speedup for stated percentages/processor count (3) + comment on a limiting case (2) — **3 parts, 10 marks total**.
- *Restoring Division*: state the algorithm (2) + perform one signed division (3) — **2 parts, 5 marks total**.
- A pure classification/justification question with no computation at all — **1 part, 5 marks flat** — is also legitimate for Section B (not every Section B question needs a numerical sub-part; the institution's own papers mix both shapes there).

**Section A is always a 2-3 part split summing to 10** (explain-compute[-explain], matching the samples above). **Section B is either a 2-part split summing to 5, or a single flat 5-mark conceptual question** — vary this across the three Section B questions rather than making all three the same shape, matching the real paper's own heterogeneity.

Calibrate the conceptual-vs-numerical mark balance toward roughly half the paper's total marks on each side across all six questions combined (not a rigid per-question 50/50 — the samples split 3/5/2 and 5/3/2, not 5/5) — this is the "keep the paper roughly half simple, half numerical" instruction, applied at the whole-paper level, not forced onto every individual question.

Apply the same discipline `/create-assignment` already enforces: motivation-before-mechanics, notation reuse from the source week's own symbols, self-contained, nothing invented beyond the source lecture/Notes/their own citations. **Mandatory per-question freshness check** against the Phase-1 avoid-list — diff concrete parameters against that week's existing assignment/GATE-set instances; regenerate with different parameters on any collision. Apply `.claude/rules/textbook-grounding.md` for any specific-textbook claim.

## Phase 3: Solutions key, verification reused inline

Write a full worked solution for **all 6** questions, addressing every labeled sub-part. Verification is reused inline via `Bash`, not delegated to a nested skill call — the precedent is `.claude/agents/grader.md`.

- For every **numerical/design sub-part with a closed-form derivation** (an algebra/Boolean/binary-arithmetic result — Booth's algorithm, IEEE754 conversion, restoring/non-restoring division, control-equation derivation), run the exact equivalence-checking method `.claude/rules/symbolic-verification.md` defines, implemented as a small inline Python/SymPy script via `Bash`.
- For every sub-part that is an **algorithm or trace** (a cache/replacement trace, a pipeline-hazard trace), run the exact method `.claude/rules/algorithm-verification.md` defines.
- **Use the identical disposition vocabulary those rules already define.** Never invent a new word for the same structural check.
- **Any FAIL/INCONSISTENT blocks Phase 4** until corrected — a wrong key on a real, once-administered exam is higher-stakes than a wrong key on a take-home.
- A sub-part with no independent mechanical ground truth (a from-scratch structural derivation like a state-table-to-Boolean-equation walkthrough with no numeric answer to check) is verified by careful structural re-derivation against the lecture's own worked method instead — document this honestly as "verified by structural re-derivation" rather than claiming a PASS/FAIL disposition that doesn't apply to it.
- `--no-verify` skips this phase entirely, documented explicitly when used.

## Phase 4: Write the files

`Minors/<CODE>/<PaperLabel>-paper.tex` (student-facing, two copies per sheet, no answers) and `Minors/<CODE>/<PaperLabel>-solutions.tex` (single-copy internal answer key).

### The paper file — reproduce this skeleton exactly, filling only the placeholders

```latex
\documentclass[9pt,a4paper]{exam}
\usepackage{graphicx}
\usepackage[a4paper, top=0.25in, bottom=0.25in, left=0.4in, right=0.4in]{geometry}
\usepackage[normalem]{ulem}
\usepackage{amsmath}
\usepackage{enumitem}
\usepackage{adjustbox}
\usepackage{tikz}
\usepackage{marvosym}

\renewcommand\ULthickness{0.8pt}
\setlength\ULdepth{1.0ex}
\setlist{nosep}
\setlength{\parskip}{0pt}
\setlength{\parindent}{0pt}
\renewcommand{\baselinestretch}{0.88}
\setlength{\topsep}{0pt}

\renewcommand{\labelenumi}{\Alph{enumi}.}
\renewcommand{\labelenumii}{\roman{enumii})}

\newcommand{\examcontent}{%
\noindent
\begin{minipage}[l]{0.10\textwidth}
    \includegraphics[width=\textwidth]{CUL}
\end{minipage}%
\hfill
\begin{minipage}[c]{0.88\textwidth}
    \begin{center}
        { Govt. College of Engineering \& Technology Ganderbal, J\&K \par
        Dept. of Computer Science \& Engineering \par
        \textbf{<Course Full Title> (<CODE-with-prefix>)} \par
        \scriptsize <Minor N>, <Month Year>}
    \end{center}
\end{minipage}

\vspace{0.01in}
\noindent
\uline{\scriptsize Time: 1 Hr \hfill Semester: $<N>^{\text{th}}$ \hfill Max Marks: 30 \hfill Min Marks: 12}

\vspace{0.04in}
\centerline{{\bfseries Section A}}
\centerline{{\scriptsize Attempt any two questions }$(2 \times 10 = 20)$}
\vspace{0.02in}

\begin{questions}
\question <topic-1 conceptual sub-part>. <topic-1 numerical/design sub-part>. <optional third sub-part>. \hfill (<marks>, <marks>[, <marks>] Marks)
\question <topic-2 ...> \hfill (... Marks)
\question <topic-3 ...> \hfill (... Marks)
\end{questions}

\vspace{0.04in}
\centerline{{\bfseries Section B}}
\centerline{{\scriptsize Attempt any two questions }$(2 \times 5 = 10)$}
\vspace{0.02in}

\begin{questions}
\setcounter{question}{3}
\question <topic-4 ...> \hfill (<marks>[, <marks>] Marks)
\question <topic-5, may be a single flat 5-mark conceptual question, no split> \hfill (5 Marks)
\question <topic-6 ...> \hfill (<marks>[, <marks>] Marks)
\end{questions}
}

\newcommand{\cuttingline}{%
\vspace{0.05cm}
\noindent\begin{center}
\begin{tikzpicture}
    \node at (0,0.1) {\scalebox{1.0}{\LeftScissors}};
    \draw[dashed] (0,0) -- (\linewidth,0);
\end{tikzpicture}
\end{center}
\vspace{0.05cm}
}

\begin{document}

\noindent
\adjustbox{valign=t,scale=0.88,minipage={\textwidth}}{%
\examcontent
}

\cuttingline

\noindent
\adjustbox{valign=t,scale=0.88,minipage={\textwidth}}{%
\examcontent
}

\end{document}
```

Notes on the placeholders: `<Course Full Title> (<CODE-with-prefix>)` — e.g. "Computer Organization and Architecture (PCC CS-401)", parsed from the syllabus H1. `<Minor N>` — e.g. "Minor 2". `<Month Year>` — from `--month` or the current date. `<N>` in "Semester $<N>^{\text{th}}$" — the syllabus's own semester number. The cutting-line scissors icon uses `\usepackage{marvosym}`'s `\LeftScissors` command (**not** `\Scissors`, which doesn't exist in that package, and not a raw Unicode character or `\char` codepoint) — Latin Modern (this template's default font, since it deliberately doesn't load `Preambles/header.tex`) has no Dingbats glyphs, so a literal ✂ or `\char"2702` produces a "Missing character" warning; a bare `\Scissors` is an undefined-control-sequence error. `\LeftScissors` is the correct, confirmed-working command in this repo's MiKTeX install.

### The solutions file — plain, single-copy, no crest, no scale/cutting-line duplication

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}   % required for \checkmark -- amsmath alone does not define it
\usepackage{booktabs}
\usepackage{xcolor}

\title{<Minor N> --- Answer Key\\[4pt]\large <Course Full Title>, Weeks <N>--<M>}
\author{<CODE-with-prefix>}
\date{\today}

\begin{document}
\maketitle
{\centering\large\bfseries\color{red}INTERNAL --- INSTRUCTOR USE ONLY --- DO NOT DISTRIBUTE\par}
\vspace{0.5cm}

\section*{Section A}
\subsection*{Q1. <topic-1 title>}
% restate question, then full worked solution for every sub-part
\subsection*{Q2. ...}
\subsection*{Q3. ...}

\section*{Section B}
\subsection*{Q4. ...}
\subsection*{Q5. ...}
\subsection*{Q6. ...}
\end{document}
```

The solutions file deliberately drops back to plain `article` (no `exam` class, no crest, no two-copy layout, no `\coursecode`/`Preambles/header.tex` — this file is a working document for the instructor alone, not a printed artifact) and uses `\color{red}` directly (`xcolor` is loaded by default with `article`'s usual class chain in this repo's toolchain) rather than this repo's `negative` semantic color, since the solutions file no longer includes `Preambles/header.tex` where that color is defined.

Compile convention: `TEXINPUTS`/`BIBINPUTS` = `../../Preambles` / `../..` relative to `Minors/<CODE>/`; Windows/MiKTeX uses `;` not `:`. The paper file needs `TEXINPUTS` pointing at `../../Preambles` specifically so `\includegraphics{CUL}` resolves `Preambles/CUL.png` — this is the only reason that path is still needed, since the paper file no longer `\input`s the shared header.

## Phase 5: QA / compile-check

- 3-pass XeLaTeX-clean on both files.
- Every question traces to its allocated source week's Slides/Notes; no symbol clashes with that week's notation registry.
- The paper file contains zero worked solutions.
- Marks per question sum correctly: every Section A question sums to 10, every Section B question sums to 5.
- Re-run the Phase-2 freshness check as a final gate.
- Every week in range is represented, or its zero-slot exception is explicitly disclosed.
- Phase 3's verification dispositions are all PASS/CONSISTENT, or `--no-verify` was explicit.
- **Hard constraint:** this skill must never call `/deploy`, `/translate-to-quarto`, or `/publish-course-hub`, and must never write anything under `docs/`.

## Report

State: paper label, resolved "Minor N", resolved range (and unit, if used), the per-week allocation table, the concentration flag if triggered, the Section A/B topic list with per-question mark splits, Phase 3's verification disposition counts, and the two file paths — closing with an explicit line that both files are gitignored and must reach students through the course's existing non-repo channel.

## Important

- **Never commit or publish either file.** Both are gitignored wholesale (`.gitignore`'s Minor exam papers block).
- **Never reuse a question verbatim** from that week's already-generated assignment or GATE set, even when grounded in the same underlying concept.
- **This exam-class two-copy format is the permanent standard for every course** in this repo, not a CS401-specific style — do not fall back to a plain `article`-class single-copy layout for the paper file.

## Cross-references

- `.claude/skills/create-assignment/SKILL.md` — the compile convention and Pre-Flight discipline this skill's single-week mechanics are modeled on; that skill is single-lecture-only, this skill is its multi-week sibling, and it keeps `article` class where this one deliberately uses `exam`.
- `.claude/skills/competitive-exam-questions/SKILL.md` — the closest exam-pattern-paper analogue; this skill needs no provenance labeling since every question here is 100% original.
- `.claude/agents/grader.md`, `.claude/rules/grading-protocol.md` — the precedent for reusing verification methods inline via `Bash` rather than nesting a skill call.
- `.claude/rules/{symbolic-verification,algorithm-verification}.md` — the verification methods Phase 3 applies, unmodified.
- `.claude/rules/textbook-grounding.md`, `.claude/rules/difficulty-levels.md` — grounding and depth-calibration discipline Phase 2 applies.
- `.gitignore` — the `Minors/**` block covering every file this skill writes.
- `syllabi/<CODE>.md` — the live source for `--unit` boundary resolution and the header's course title/code/semester; never hardcode either.
- `Preambles/CUL.png` — the committed institutional crest every Minor paper's header uses.
