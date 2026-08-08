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

**Sourcing principle (availability-first):** prefer the **local PYQ books** in `CompetitiveExam/Books/` over web search whenever the topic is available there — see `CompetitiveExam/Books/index.md` for the availability registry, the sourcing ladder, and the extraction constraints. Tier 1 (local book) → Tier 2 (web + CoVe) → Tier 3 (original).

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and compiles.
- Read `Slides/<CODE>/<lecture>.tex` and, if it exists, `Notes/<CODE>/<lecture>-notes.tex` to build a list of the lecture's specific sub-topics (e.g., for `06-hardwired-control`: sequence counter design, opcode decoding, state-table-to-Boolean-equation derivation, AND-OR gate realization, hardwired vs. microprogrammed trade-offs).
- **Check source availability:** read `CompetitiveExam/Books/index.md` and for each sub-topic look up whether a local volume covers it (topic name match in the volume's topic map → PDF page range). Mark each sub-topic as **LOCAL-AVAILABLE** (tier 1) or **LOCAL-MISSING** (tiers 2-3). If a topic name is not in the map, re-scan the volume's question headings (see index.md's heading regex) before concluding it's missing — the map folds rare topics into cluster rows.
- Produce a short Pre-Flight note: topic list with availability tags, target exam (default GATE-CS), and target count (default 6-8 questions, mixing MCQ and Numerical-Answer-Type if the target exam uses both — GATE CS does).

## Phase 1: Source real past-year questions (local-first)

### Step 1a — Tier 1: local PYQ book (preferred)

For each **LOCAL-AVAILABLE** sub-topic:

1. Open the volume's PDF page range from the registry (e.g., `GATE-PYQs/filter1_volume3.pdf` pp. 28-31 for Addressing Modes).
2. `pdftotext` that page range; locate question headings of the form `X.Y.Z <Topic>: GATE CSE <year> | Question: <n>`. Record the exact **PDF page** where each question lives — this is the citation unit.
3. **Recover full question text** (math values are embedded images, dropped by pdftotext): render the page with Ghostscript and OCR with Tesseract — see `CompetitiveExam/Books/index.md` → "The render + OCR sub-pipeline". Transcribe the question + options verbatim, including numeric values.
4. Record the question identity: GATE year, question number, topic, difficulty tag (easy/normal) from the book's tag line.
5. **Verify the answer** (the book's own answers are collapsed/absent): `WebSearch` the year + question number, cross-check 2+ independent sources. Only then tag `[verified]`.
6. Provenance: `[GATE CS <year> Q<n>, verified — GATEOverflow V3 p.<pdfpage>]`.

If a Tier-1 question's answer cannot be independently verified, **do not ship it as verified** — either drop it or rewrite as an original (Phase 2).

### Step 1b — Tier 2: web search + CoVe (for LOCAL-MISSING topics)

For each **LOCAL-MISSING** sub-topic, `WebSearch` for a matching real question (e.g., `"GATE CS" "sequence counter" OR "control unit" previous year question`). A candidate is only a **draft** claim at this point, not a fact.

**Extract claims, then verify independently (CoVe):**

1. For each candidate PYQ, extract the claim precisely: exact question text (or close paraphrase if the source paraphrases it), the exam year, and the correct answer/option.
2. Spawn `claim-verifier` via `Task` (`subagent_type: claim-verifier`, `context: fork`) with the claims + source URLs — never pass a draft narrative, only the claims table and pointers, per `.claude/rules/post-flight-verification.md`.
3. **CONFIRMED** → include as `[GATE CS <year>, verified — web]`.
4. **CANNOT-VERIFY or CONTRADICTED** → do not include it as a real PYQ. Either drop it or, if the underlying topic is still worth testing, rewrite it from scratch as an original question (Phase 2) — never ship a "verified" label on a claim that didn't actually verify.

## Phase 2: Fill remaining topics with original, exam-pattern questions

For sub-topics with no verified real match (whether the local book lacked them or the web search couldn't confirm), write an original question in the target exam's own format (for GATE CS: single-correct MCQ or Numerical-Answer-Type, calibrated to real GATE difficulty for that topic — GATE CS control-unit/datapath questions are typically 1-2 mark numerical or short-reasoning items, not multi-part derivations). Label these `[Original, GATE-pattern]` — never attribute a specific year or claim it appeared in a real exam.

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
% \textbf{Q1} \textit{[GATE CS 2008 Q71, verified — GATEOverflow V3 p.40]} ...
% \textbf{Q2} \textit{[GATE CS 2019, verified — web]} ...
% \textbf{Q3} \textit{[Original, GATE-pattern]} ...
\end{document}
```

The provenance tag is not optional decoration — it is the load-bearing distinction between "this is authentic" and "this is practice material in the same style." Compile the same way as Notes/Assignments: `TEXINPUTS`/`BIBINPUTS` relative to `CompetitiveExam/<CODE>/`; Windows/MiKTeX uses `;` not `:`.

## Phase 4: Report

State: question count by provenance (verified PYQ vs. original), the years/sources of any verified PYQs, the CoVe outcome (PASS/PARTIAL/FAIL per `post-flight-verification.md`'s output contract), and the two file paths written.

## Flags

- `--exam <name>` — target competitive exam (default `GATE-CS`). Determines the question format used in Phase 2 (GATE CS: single-correct MCQ and Numerical-Answer-Type) and the search terms used in Phase 1. Change this to point the skill at a different exam for a different course/context.
- `--no-verify` — skip answer verification (Tier 1 web cross-check and Tier 2 CoVe) entirely and write the set as-is, sourcing from the local book where available. Use when speed matters more than authenticity, or the topic is too niche for PYQs to plausibly exist.
- `--no-ocr` — for Tier-1 topics, use only the `pdftotext` text layer (question text/options where extractable) and do not run the render+OCR sub-pipeline. Use when a question's numeric values aren't load-bearing or OCR is unavailable.

## Cross-references

- `CompetitiveExam/Books/index.md` — the **source registry**: availability ladder, per-volume topic→page maps, extraction constraints, render+OCR sub-pipeline. Consult in Phase 0 and Phase 1a.
- `.claude/rules/post-flight-verification.md` — the CoVe protocol this skill's Phase 1b implements directly (same pattern as `/lit-review`).
- `.claude/skills/lit-review/SKILL.md` — the sibling skill this borrows the search-then-verify discipline from.
- `.claude/agents/claim-verifier.md` — the forked verifier spawned in Phase 1b.
- `.claude/skills/create-assignment/SKILL.md` — the sibling skill for graded (non-competitive-exam) practice material.
- `.claude/rules/textbook-grounding.md` — the same "cite what you can back, phrase honestly otherwise" principle, applied to exam provenance instead of textbook pages.
