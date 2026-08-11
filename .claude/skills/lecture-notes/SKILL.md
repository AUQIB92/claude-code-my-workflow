---
name: lecture-notes
description: Expand a finished, compiled Beamer lecture deck into full prose Lecture Notes (XeLaTeX article-class PDF) — worked derivations spelled out, transitions as full sentences, citations and textbook page-pointers preserved 1:1. Use when user says "generate lecture notes", "write up notes for this lecture", "expand the slides into notes", "make a handout from this deck", or as the automatic Phase 5 step after `/create-lecture` finishes a deck. Beamer `.tex` stays the source of truth; Notes are purely derived — same relationship Quarto already has to Beamer. NOT for co-drafting notes and slides together (not supported); NOT for translating to HTML (`/translate-to-quarto`).
argument-hint: "[CourseCode/lecture], e.g. CS401/07-microprogrammed-control (Slides/CourseCode/lecture.tex must already exist and compile)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
context: fork
model: sonnet
effort: medium
---

# Generate Lecture Notes from a Finished Beamer Deck

Expand `Slides/<CODE>/<lecture>.tex` into `Notes/<CODE>/<lecture>-notes.tex` — a textbook chapter covering the same content, same relationship Quarto already has to Beamer (derived, never independently edited), but reorganized by topic rather than transcribed frame-by-frame (see Phase 2).

**CRITICAL: The Beamer `.tex` file is the SINGLE SOURCE OF TRUTH.** Notes expand it; they do not add ideas the deck doesn't contain, and they do not drop any.

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and has compiled (a `.pdf` alongside it, or the caller confirms compilation just succeeded).
- Read `.claude/rules/knowledge-base-<CODE>.md`'s Anchor Textbooks table to know which chapters have a real page index (`master_supporting_docs/<CODE>/supporting_books/*/index.md`) versus general-treatment-only citations.

## Phase 1: Read the deck end-to-end

Read the full `.tex` source. For each frame, note: the motivating question/example, the definition(s), the derivation steps, the worked example, any TikZ diagram (its coordinate-map comment is the raw material for a prose description — reuse it, don't re-derive), and every citation.

## Phase 2: Reorganize into a textbook chapter, don't transcribe frame-by-frame

**Read every frame, but write by topic, not by frame order.** A Beamer deck is paced for a live audience (Socratic questions, transition slides, "recap" framing, "bridge to next week" hooks); Notes should read like a textbook chapter on the same material. Content parity is still absolute — every fact, citation, diagram, and worked example in the deck must appear in the Notes and trace back to it (`/qa-notes` checks this) — but the *order and headings* should be regrouped by subject, the way a textbook chapter would organize it, not left as a slide-by-slide transcript.

Concretely:

- **Draft a topic outline before writing prose.** Group the deck's frames by subject (e.g., "definitions and motivation," "the core mechanism," "worked derivation," "trade-offs/comparison") rather than walking the deck's Acts/sections in order. Presentation-pacing frame titles ("A Question We Skipped," "Socratic Check: ...," "Bridge to Week N," "Recall: ... by Hand") are lecture devices — fold their content into the surrounding topic section as motivating context, don't keep them as standalone headings.
- **Bullets become full sentences.** A slide bullet like "EA = [PC] + disp" becomes a sentence deriving why the effective address is computed that way, in the same notation.
- **Every derivation step gets spelled out**, including steps a slide compresses (a slide may show only the final control-word equation; Notes shows the derivation that produced it).
- **Every term the deck actually defines gets a formal `Definition` callout** (see Phase 3's template), not just a bolded word mid-paragraph.
- **Every worked example/trace becomes a numbered `Example` environment** (see Phase 3), not an ad hoc "Worked Trace" subsection.
- **TikZ diagrams are embedded as real, numbered figures** — reuse the diagram's exact TikZ code from the Beamer source verbatim (it has already passed `tikz-reviewer`; don't re-derive it), wrapped in a numbered `figure` environment with a page-cited caption (see Phase 3). A reader should see the actual diagram, not just a prose description of it.
- **TikZ overlap audit on every embedded figure (MANDATORY):** before compiling, run the P7 clearance audit (`.claude/rules/tikz-prevention.md`) on each reused `tikzpicture` — no path crossing a box except at a connection point (P7a), no label sitting on a line (P7b), labels ≥0.15 cm clear of box edges (P7c), no curve visibly crossing its own dashed asymptote (P7d). If the Beamer source's diagram violates any of these (or the source was authored before P7 existed), fix the diagram in the Beamer source first and port the corrected code — never paper over an overlap only in the Notes copy, because the deck is the single source of truth and the same diagram ships in the deck, Notes, and handout.
- **Citations are preserved 1:1** — same `\cite{}` keys, same attribution. If the cited chapter has an entry in `supporting_books/*/index.md`, add the specific page (per `.claude/rules/textbook-grounding.md`); if not, keep the existing chapter-level/general-treatment phrasing — do not upgrade to a page number you can't back, and do not imply a source "specifies" or "shows" something more precisely than what's actually indexed.
- **Transitions between sections are full sentences**, not slide-title juxtaposition.
- **Nothing invented, nothing dropped.** If a frame's content genuinely doesn't need its own topic section (e.g. a section-transition slide), fold its motivating sentence into the section it introduces — don't pad with a standalone paragraph just to preserve frame-for-frame correspondence.

## Phase 2.5: The Detail Bar (MANDATORY — "textbook-candidate prose")

The deliverable, judged as a whole, is prose a student could study from **having missed the lecture entirely**. Every slide's compressed trace must be expanded until each intermediate state is written out. Five concrete tests:

- **No elided steps.** Any derivation, memory trace, pointer-lifetime trace, or step-frame sequence in the deck (e.g. "How the Stack Grows — Step 1/2/3", "How the Heap Grows — Step 1/2/3") becomes a numbered, step-by-step walk-through with each intermediate state **before** the next line of reasoning — never "then the stack changes as you'd expect."
- **Every example fully solved.** A numbered `example` ends with its complete answer/solution. No truncated traces, no "this is left as an exercise" inside a worked example.
- **Exercises + a separate Solutions block.** End the chapter with `\subsection*{Exercises}` (3–5 problems, reusing the deck's traces but at least one genuinely new instance) and `\subsection*{Solutions}` giving the full working, so the Notes double as a self-check. Solutions are visually contained (e.g. `\small` + a `\begingroup`/`\endgroup` so a lecturer can suppress them when printing a student copy).
- **Reading guidance.** At each major section start, one line pointing at the anchor reading (page-cited only where a real `supporting_books/*/index.md` entry exists; honest chapter-level otherwise, per `.claude/rules/textbook-grounding.md`).
- **SSOT re-sync clause.** If the deck changed since these Notes were last generated (scope decisions, added/dropped frames, section reorganizations), the Notes **must** be re-aligned first, then `/qa-notes` re-run. A scope change in the deck (e.g. deferring `calloc`/`realloc`) is not an excuse to keep the old coverage.

## Phase 3: Write the file

`Notes/<CODE>/<lecture>-notes.tex` — XeLaTeX `article` class, styled as a textbook chapter (section/figure/example numbers prefixed by the week/lecture number, e.g. `<N>.1`, `Fig. <N>.1`, `Example <N>.1`):

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\input{../../Preambles/header}   % same shared palette/macros as Beamer; \key/\good/\bad/\muted
                                   % must degrade gracefully outside Beamer (see header.tex)
\coursecode{<CODE>}               % same macro as the Beamer deck; no-ops in article class if not shown in a footer there

% Chapter-style numbering: <N> is this lecture's week/lecture number.
\renewcommand{\thesection}{<N>.\arabic{section}}
\renewcommand{\thefigure}{<N>.\arabic{figure}}
\newtheorem{example}{Example}[section]

% Lightweight boxed Definition callout -- visually simple, consistent with
% the project's existing \key/block conventions rather than a new theorem style.
\newenvironment{definitionbox}[1]{%
  \par\noindent\textbf{Definition (#1).}\ \itshape
}{\par\vspace{0.3em}}

\title{<Deck Title> --- Lecture Notes}
\author{<same as Beamer deck's \author>}
\date{\today}

\begin{document}
\maketitle
% topic-organized sections per Phase 2's outline, not a frame-by-frame transcript
\bibliography{../../Bibliography_base}
\bibliographystyle{plain}
\end{document}
```

**Definitions:** `\begin{definitionbox}{Term}...\end{definitionbox}` for every term the deck formally defines.

**Figures:** wrap each reused TikZ diagram in a real `figure` environment, not a bare `center`:
```latex
\begin{figure}[h]
  \centering
  \begin{tikzpicture}[...]
    ... % exact code from the Beamer source, unchanged
  \end{tikzpicture}
  \caption{... --- cf.\ \textit{Book}, Fig.~X-Y, p.NNN \cite{key}.}
\end{figure}
```

**Worked examples:** `\begin{example}...\end{example}` for every worked trace/derivation, so it numbers as `Example <N>.1`, `<N>.2`, ... automatically.

**Exercises + Solutions:** a self-contained block at the end of the chapter implementing the Detail Bar's fourth requirement:
```latex
\subsection*{Exercises}
\begin{enumerate}
  \item ...
  \item ...
\end{enumerate}

\subsection*{Solutions}
\begingroup\small
\begin{enumerate}
  \item ...
  \item ...
\end{enumerate}
\endgroup
```

Compile the same way as a Beamer deck but from `Notes/<CODE>/`: `TEXINPUTS`/`BIBINPUTS` need `../../Preambles` / `../..` relative to that cwd (same depth reasoning as `/compile-latex` — TeX writes output next to cwd, not next to the file's own path). On Windows/MiKTeX use `;` not `:` as the separator (see `.claude/skills/compile-latex/SKILL.md`).

## Phase 4: QA

Run [`/qa-notes`](../qa-notes/SKILL.md) `<CODE>/<lecture>` — the critic→fixer loop-until-dry that checks nothing was invented or dropped relative to the Beamer source.

## Report

State: the topic outline used (how deck frames were regrouped into textbook sections), sections/figures/examples written, citations preserved count, any textbook claims upgraded to page-cited (vs. left general), and the `/qa-notes` outcome.

## Cross-references

- `.claude/rules/single-source-of-truth.md` — Notes as a third derived branch, parallel to Quarto.
- `.claude/skills/qa-notes/SKILL.md`, `.claude/agents/notes-critic.md`, `.claude/agents/notes-fixer.md` — the parity-check loop.
- `.claude/rules/textbook-grounding.md` — page-citation discipline.
- `.claude/skills/translate-to-quarto/SKILL.md` — the sibling derived-artifact pattern this skill copies.
