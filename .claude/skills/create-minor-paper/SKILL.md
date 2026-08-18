---
name: create-minor-paper
description: Assemble an internal institutional sessional "Minor" exam paper (LaTeX PDF, course-organized) spanning a specified range of weeks — the fixed pattern of Section A (three questions x 10 marks, attempt any two = 20) and Section B (three questions x 5 marks, attempt any two = 10), 30 marks total. Every question is freshly written for this paper — a different concrete instance than that week's already-generated /create-assignment or /competitive-exam-questions output, even when grounded in the same concept. Use when user says "make a Minor paper", "generate the sessional exam for weeks N-M", "create Minor 1", "build the internal exam paper for Unit II". NOT for a single-lecture graded assignment (use /create-assignment) and NOT for a GATE-pattern practice set (use /competitive-exam-questions) — both are single-week and their student-facing output is public/tracked; a Minor paper spans multiple weeks and is a real, live exam, so both the paper and its solutions are gitignored end-to-end, never committed, never deployed to docs/.
argument-hint: "<CourseCode>/<PaperLabel> --weeks N-M (or --unit I|II|III) [--no-verify], e.g. CS401/minor-1 --unit I"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
context: fork
model: sonnet
effort: high
---

# `/create-minor-paper` — Multi-Week Sessional Exam Paper

Assemble an internal "Minor" exam paper — a real, live sessional exam, not public study material — spanning a range of weeks rather than one lecture. This is the first skill in this template that sources content across multiple weeks at once; every other course-content skill (`/create-assignment`, `/competitive-exam-questions`) is strictly single-lecture. Both the question paper and its solution key are gitignored end-to-end: they never reach `docs/`, and they never reach a public GitHub repo before or after the exam is administered.

**Input:** `<CODE>/<PaperLabel>` plus exactly one of `--weeks N-M` or `--unit I|II|III`, e.g. `CS401/minor-1 --unit I` or `CS401/mid-sem-a --weeks 4-7`.

## The fixed pattern (reproduce verbatim, never paraphrase)

```
Paper Pattern of Minor — Maximum Marks: 30
Section A: (10 x 2 = 20 marks) — Section A shall comprise three questions; candidates shall attempt any two. Each question carries 10 marks.
Section B: (5 x 2 = 10 marks) — Section B shall comprise three questions; candidates shall attempt any two. Each question carries 5 marks.
```

Three questions set per section, two required, marks as stated. This arithmetic is load-bearing — every phase below exists to produce exactly 3+3 questions that honor it.

## Phase 0: Pre-Flight

1. Parse `$ARGUMENTS`. `PaperLabel` is a free instructor-supplied kebab-case identifier (`minor-1`, `weeks01-03`, `mid-sem-a`) — not tied to any single lecture slug, since this artifact spans several. Reject if neither or both of `--weeks`/`--unit` are given; nothing is written on this error.
2. **Resolving `--unit I|II|III` (sugar over `--weeks`, computed live every run — never hardcoded):**
   - Read `syllabi/<CODE>.md`. Scan the Learning Objectives bullets for `(Weeks? N)` / `(Weeks N-M)` tags to get each objective's week span.
   - Scan the Weekly Schedule table's `Deliverable` column for `**Class Test N**` rows (or this course's equivalent internal-test marker) to find where each Unit's boundary lands.
   - Unit 1 = weeks `1..(first Class Test's week)`; Unit *k* = weeks `(previous Class Test week + 1)..(kth Class Test week)`.
   - If the requested unit letter has no matching Class Test row in *this course's* syllabus, **do not guess a boundary** — stop and tell the user to pass `--weeks` directly instead.
   - Report the resolved range explicitly in the Pre-Flight note, so a misresolution is caught before anything is written.
3. For every week in the resolved range, confirm the syllabus's Week → lecture work-list names a deck, and that `Slides/<CODE>/<deck>.tex` exists with a compiled `.pdf` alongside it. **Any missing week is a hard stop** — list exactly which week(s) are missing and exit; a paper silently drawn from a subset of its stated range is a validity defect, not a usable degraded result. Prefer `Notes/<CODE>/<deck>-notes.tex` over the raw deck when it exists (already topic-organized, citations resolved), matching `/create-assignment`'s own preference rule.
4. Emit a Pre-Flight note: resolved week range (+ unit, if used), the deck list, the paper label, both output paths (flagged as **gitignored, never public**), and the fixed target —3 Section A questions (10 marks each) + 3 Section B questions (5 marks each).

## Phase 1: Multi-week sourcing and topic allocation

This is the genuinely new mechanism this skill introduces — read it carefully, it is not a copy of any existing skill's Phase 0/1.

1. **Per-week subtopic extraction.** For every week in range, read its Slides (+ Notes if present) and extract a distinct-subtopic list, each tagged with its source week — the same granularity `/competitive-exam-questions` already extracts per-lecture, just run once per week in range instead of once per single artifact.
2. **Build the avoid-list.** For every week in range, also read that week's already-generated `Assignments/<CODE>/<deck>-assignment.tex` and `CompetitiveExam/<CODE>/<deck>-questions.tex`, if they exist, and record every concrete question stem — the specific numbers, register names, or scenario asked, not just the topic name. This is the set Phase 2's freshness check tests every drafted question against.
3. **Allocate the 6 slots by largest-remainder apportionment**, not by hand-waving: let `N_w` be week `w`'s distinct-subtopic count and `weight_w = N_w / sum(N)`; apportion 6 total slots across the weeks in range using the largest-remainder (Hamilton) method on those weights. This is an auditable, well-defined rule for turning "some weeks are topically richer than others" into integer slot counts.
4. **Coverage floor.** When the range spans 6 weeks or fewer (true for every CS401 Unit: 3, 4, and 3 weeks respectively), force a minimum of 1 slot per week, topping up any week that rounds to 0 by drawing from the largest-remainder pool first — every week in the requested range is guaranteed at least one question. When the range spans more than 6 weeks, this floor cannot be mathematically guaranteed; any week that ends up with 0 slots must be explicitly disclosed in the Phase-1 report (lowest topic weight, named), never silently dropped.
5. **Concentration flag (advisory, not a block).** If any single week supplies more than half of one section's 3 questions, note this explicitly in the report — a genuinely topic-rich week may deserve it, but it should be visible.
6. **Section routing by depth, not by week parity.** Within each week's allocated slots, route its most derivation/design-depth subtopic (a state-table derivation, an IEEE754 worked conversion, a cache-mapping computation, a control-equation derivation) to Section A; route its more definitional/comparative/short-numerical subtopic to Section B. Calibrate depth to sessional time budgets, not take-home depth: roughly 15-20 minutes of work for a 10-mark Section A item, roughly 7-10 minutes for a 5-mark Section B item.

## Phase 2: Question writing

- Section A: 3 questions, 10 marks each, long-answer/derivation-or-design depth (per Phase 1's routing).
- Section B: 3 questions, 5 marks each, shorter conceptual/definitional/short-numerical depth.
- Apply the same discipline `/create-assignment` Phase 1 already enforces: motivation-before-mechanics (`content-invariants.md` INV-8), notation reuse from the source week's own symbols (never a clashing symbol for an already-defined object), self-contained (no "as discussed in class"), nothing invented beyond the source lecture/Notes/their own citations.
- **Mandatory per-question freshness check against the Phase-1 avoid-list.** For each drafted question, diff its concrete parameters (numbers, register names, the specific scenario asked) against that week's avoid-list entries. If a draft coincides with something already asked in that week's assignment or GATE set, regenerate with different concrete parameters before considering the question final — never ship a question whose worked answer may already be circulating in that week's homework/practice material.
- Apply `.claude/rules/textbook-grounding.md` for any claim naming a specific textbook: page-cited if `master_supporting_docs/<CODE>/supporting_books/<Book>/index.md` covers it, otherwise phrased as general/standard treatment — never a fabricated page.

## Phase 3: Solutions key, verification reused inline

Write a full worked solution for **all 6** questions, both sections — the instructor needs the complete key regardless of which 2-per-section a given student attempts.

**Verification is reused inline via `Bash`, not delegated to a nested skill call** — this skill has no `Task` tool and is not a fan-out skill; the precedent is `.claude/agents/grader.md`, which applies the identical verification method inline rather than spawning a subagent for it, because there is no batch of independent items here needing isolated context, just one coherent paper.

- For every question whose solution is a **closed-form derivation** (algebra, an IEEE754 conversion, a Boolean/control-equation derivation), run the exact equivalence-checking method `.claude/rules/symbolic-verification.md` defines: `sympy.simplify(computed - claimed) == 0` first, the same randomized numeric-substitution fallback (5 rational values per free symbol, agreement within `1e-9`) when `simplify` can't resolve it, and the same tolerance table for rounded/irrational results — implemented as a small inline Python/SymPy script via `Bash`, the same mechanism `/verify-symbolic` itself uses.
- For every question whose solution is an **algorithm or trace** (a control-unit state-table trace, a cache-mapping/replacement trace, a pipeline-hazard trace), run the exact method `.claude/rules/algorithm-verification.md` defines (the artifact's own worked example, boundary cases, structure-specific adversarial cases, ≥20 random inputs where applicable) via `Bash`.
- **Use the identical disposition vocabulary those rules already define** — PASS/FAIL/UNTRANSLATABLE/AMBIGUOUS for symbolic checks, PASS/FAIL/CONSISTENT/INCONSISTENT/INCONCLUSIVE for algorithmic ones. Never invent a new word for the same structural check, matching the discipline `.claude/rules/grading-protocol.md` already states for `/grade`.
- **Any FAIL/INCONSISTENT blocks Phase 4** until the underlying solution is corrected. "Run before releasing any solution key" is not optional here — a wrong key on a real, graded, once-administered exam is a higher-stakes mistake than a wrong key on a take-home assignment.
- `--no-verify` skips this phase entirely, mirroring `/competitive-exam-questions`' own flag semantics — use it when a question genuinely has no closed-form/algorithmic ground truth (pure Conceptual/Design), or when speed is prioritized. Document the skip explicitly in the final report; never skip silently.

## Phase 4: Write the files

`Minors/<CODE>/<PaperLabel>-paper.tex` (student-facing question paper, no answers) and `Minors/<CODE>/<PaperLabel>-solutions.tex` (full solution key) — generalizing the `-assignment`/`-solutions` suffix pattern to `-paper`/`-solutions`, since "paper" is this artifact's own name.

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}
\coursecode{<CODE>}

\title{Minor Examination --- <Paper Title>\\[4pt]\large Weeks <N>--<M>}
\author{<CODE>: <Course Full Title>}
\date{\today}

\begin{document}
\maketitle

\begin{center}
\fbox{\begin{minipage}{0.92\textwidth}
\centering
\textbf{Paper Pattern of Minor --- Maximum Marks: 30}\\[6pt]
\begin{tabular}{@{}p{0.98\textwidth}@{}}
\textbf{Section A:} (10 $\times$ 2 = 20 marks) --- Section A shall comprise three questions; candidates shall attempt any two. Each question carries 10 marks.\\[4pt]
\textbf{Section B:} (5 $\times$ 2 = 10 marks) --- Section B shall comprise three questions; candidates shall attempt any two. Each question carries 5 marks.
\end{tabular}
\end{minipage}}
\end{center}

\vspace{1em}
\noindent\textbf{Time Allowed:} 1 Hour \hfill \textbf{Maximum Marks: 30}

\section*{Section A}
\textit{Attempt any TWO of the following three questions. Each question carries 10 marks.}
\begin{enumerate}
\item
\item
\item
\end{enumerate}

\section*{Section B}
\textit{Attempt any TWO of the following three questions. Each question carries 5 marks.}
\begin{enumerate}
\item
\item
\item
\end{enumerate}

\bibliography{../../Bibliography_base}
\bibliographystyle{plain}
\end{document}
```

**No week-keyed `\thesection` numbering** (unlike `/create-assignment`/`/competitive-exam-questions`) — a Minor paper isn't part of any single week's numbered artifact sequence, so Section A/B use unnumbered `\section*{}` headers matching the mark scheme's own labels instead.

The solutions file mirrors the same Section A/B `\item` numbering, restates each question in one line before its worked solution (never assumes the paper is open side by side, same discipline `/create-assignment`'s solution key already uses), and opens with a marker the public-facing assignment solutions file doesn't need:

```latex
{\centering\large\color{negative}\textbf{INTERNAL --- INSTRUCTOR USE ONLY --- DO NOT DISTRIBUTE}\par}
\vspace{0.5cm}
```

Compile the same way as `/create-assignment`: `TEXINPUTS`/`BIBINPUTS` = `../../Preambles` / `../..` relative to `Minors/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Phase 5: QA / compile-check

- 3-pass XeLaTeX-clean on both files (same convention `/compile-latex` uses).
- Every question traces to its allocated source week's Slides/Notes; no symbol clashes with that week's notation registry (`knowledge-base-<CODE>.md`).
- The paper file contains zero worked solutions or final answers.
- Re-run the Phase-2 freshness check as a final gate, not just a drafting-time check — no verbatim overlap with that week's Assignment/GATE bank.
- Every week in range is represented in the final paper, or its zero-slot exception is explicitly disclosed (Phase 1's coverage-floor rule).
- Phase 3's verification dispositions are all PASS/CONSISTENT, or `--no-verify` was explicitly used and disclosed.
- **Hard constraint:** this skill must never call `/deploy`, `/translate-to-quarto`, or `/publish-course-hub`, and must never write anything under `docs/`.

## Report

State: paper label, resolved range (and unit, if `--unit` was used), the per-week allocation table (week → subtopic count → weight → slots → section), the concentration flag if it triggered, the Section A/B topic list, Phase 3's verification disposition counts (or that `--no-verify` was used), and the two file paths — closing with an explicit line that both files are gitignored and must reach students through the course's existing non-repo channel, never via the repo or GitHub Pages.

## Important

- **Never commit or publish either file.** Both are gitignored wholesale (see `.gitignore`'s Minor exam papers block) — this is a deliberate, stricter posture than `/create-assignment`'s (whose student-facing questions ARE public study material; only its solutions are gitignored). A Minor paper is a real, live exam.
- **Never reuse a question verbatim** from that week's already-generated assignment or GATE set, even when grounded in the same underlying concept — Phase 2's freshness check exists specifically to enforce this.

## Cross-references

- `.claude/skills/create-assignment/SKILL.md` — the compile convention, file-writing phase shape, and Pre-Flight discipline this skill's single-week mechanics are modeled on; that skill is now single-lecture-only, this skill is its multi-week sibling.
- `.claude/skills/competitive-exam-questions/SKILL.md` — the closest exam-pattern-paper analogue (marks-per-question structure); this skill needs no provenance labeling since every question here is 100% original.
- `.claude/agents/grader.md`, `.claude/rules/grading-protocol.md` — the precedent for reusing `symbolic-verification.md`/`algorithm-verification.md`'s exact method inline via `Bash` rather than nesting a skill call or reinventing a check.
- `.claude/rules/{symbolic-verification,algorithm-verification}.md` — the verification methods Phase 3 applies, unmodified.
- `.claude/rules/textbook-grounding.md`, `.claude/rules/difficulty-levels.md` — grounding and depth-calibration discipline Phase 2 applies.
- `.gitignore` — the `Minors/**` block covering every file this skill writes.
- `syllabi/<CODE>.md` — the live source for `--unit` boundary resolution; never hardcode a Unit's week range.
