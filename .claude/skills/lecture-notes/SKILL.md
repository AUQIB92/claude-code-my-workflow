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

Expand `Slides/<CODE>/<lecture>.tex` into `Notes/<CODE>/<lecture>-notes.tex` — full prose, same content, same relationship Quarto already has to Beamer (derived, never independently edited).

**CRITICAL: The Beamer `.tex` file is the SINGLE SOURCE OF TRUTH.** Notes expand it; they do not add ideas the deck doesn't contain, and they do not drop any.

## Phase 0: Pre-Flight

- Confirm `Slides/<CODE>/<lecture>.tex` exists and has compiled (a `.pdf` alongside it, or the caller confirms compilation just succeeded).
- Read `.claude/rules/knowledge-base-<CODE>.md`'s Anchor Textbooks table to know which chapters have a real page index (`master_supporting_docs/<CODE>/supporting_books/*/index.md`) versus general-treatment-only citations.

## Phase 1: Read the deck end-to-end

Read the full `.tex` source. For each frame, note: the motivating question/example, the definition(s), the derivation steps, the worked example, any TikZ diagram (its coordinate-map comment is the raw material for a prose description — reuse it, don't re-derive), and every citation.

## Phase 2: Expand frame-by-frame into prose

For each frame, in deck order, write a prose section (not a slide-by-slide transcript — sections may combine short frames, e.g. a 2-slide worked example becomes one prose subsection with a heading):

- **Bullets become full sentences.** A slide bullet like "EA = [PC] + disp" becomes a sentence deriving why the effective address is computed that way, in the same notation.
- **Every derivation step gets spelled out**, including steps a slide compresses (a slide may show only the final control-word equation; Notes shows the derivation that produced it).
- **TikZ diagrams get a prose description** drawn from the diagram's coordinate-map comment (per `.claude/rules/tikz-prevention.md` Rule P2) — describe what the diagram shows and why, since a reader of the Notes may not see the rendered figure inline the same way a slide audience does.
- **Citations are preserved 1:1** — same `\cite{}` keys, same attribution. If the cited chapter has an entry in `supporting_books/*/index.md`, add the specific page (per `.claude/rules/textbook-grounding.md`); if not, keep the existing chapter-level/general-treatment phrasing — do not upgrade to a page number you can't back.
- **Transitions between sections are full sentences**, not slide-title juxtaposition.
- **Nothing invented, nothing dropped.** If a frame's content genuinely doesn't need expansion (e.g. a section-transition slide), a short paragraph is fine — don't pad.

## Phase 3: Write the file

`Notes/<CODE>/<lecture>-notes.tex` — XeLaTeX `article` class:

```latex
\documentclass[11pt]{article}
\input{../../Preambles/header}   % same shared palette/macros as Beamer; \key/\good/\bad/\muted
                                   % must degrade gracefully outside Beamer (see header.tex)
\coursecode{<CODE>}               % same macro as the Beamer deck; no-ops in article class if not shown in a footer there

\title{<Deck Title> --- Lecture Notes}
\author{<same as Beamer deck's \author>}
\date{\today}

\begin{document}
\maketitle
% prose sections, one per Phase-2 expansion unit
\bibliography{../../Bibliography_base}
\bibliographystyle{plain}
\end{document}
```

Compile the same way as a Beamer deck but from `Notes/<CODE>/`: `TEXINPUTS`/`BIBINPUTS` need `../../Preambles` / `../..` relative to that cwd (same depth reasoning as `/compile-latex` — TeX writes output next to cwd, not next to the file's own path).

## Phase 4: QA

Run [`/qa-notes`](../qa-notes/SKILL.md) `<CODE>/<lecture>` — the critic→fixer loop-until-dry that checks nothing was invented or dropped relative to the Beamer source.

## Report

State: sections written, citations preserved count, any textbook claims upgraded to page-cited (vs. left general), and the `/qa-notes` outcome.

## Cross-references

- `.claude/rules/single-source-of-truth.md` — Notes as a third derived branch, parallel to Quarto.
- `.claude/skills/qa-notes/SKILL.md`, `.claude/agents/notes-critic.md`, `.claude/agents/notes-fixer.md` — the parity-check loop.
- `.claude/rules/textbook-grounding.md` — page-citation discipline.
- `.claude/skills/translate-to-quarto/SKILL.md` — the sibling derived-artifact pattern this skill copies.
