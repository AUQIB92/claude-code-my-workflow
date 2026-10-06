---
paths:
  - "Figures/**/*"
  - "Quarto/**/*.qmd"
  - "Slides/**/*.tex"
  - "Notes/**/*.tex"
---

# Single Source of Truth: Enforcement Protocol

**The Beamer `.tex` file is the authoritative source for lecture-slide content.**
Lecture Notes are the standard derived artifact. Quarto course mirrors are
legacy artifacts and are not created or maintained as part of course work.

## The SSOT Chain

```
Beamer .tex (SOURCE OF TRUTH)
  ├── extract_tikz.tex → PDF → SVGs (when requested)
  ├── Notes/<CODE>/*-notes.tex → article-class PDF (standard derived artifact;
  │       checked via /qa-notes)
  ├── Bibliography_base.bib (shared)
  └── Figures/LectureN/*.rds → plotly charts (data source)

NEVER edit derived artifacts independently.
Propagate changes to standard derived artifacts. Do not update legacy Quarto
course mirrors during course work.
```

**Lecture Notes are the standard derived artifact.** Their fidelity is about
**content parity, not structural mirroring**: every fact, citation, diagram, and
worked example in the Beamer deck must appear somewhere in the Notes and trace
back to it (checked by `/qa-notes`, nothing invented, nothing dropped) — but the
Notes are free to, and by default *should*, reorganize that content into a
textbook-chapter shape rather than following the deck's slide-by-slide/Act-by-Act
presentation order. A Beamer deck is paced for a live audience (Socratic
questions, transition slides, "recap" framing, "bridge to next week" hooks); a
textbook chapter is organized by topic. Concretely, Notes should:

- **Number sections by lecture/week**, e.g. `5.1, 5.2, ...` for Week 5, not plain `1, 2, 3` (`\renewcommand{\thesection}{<week>.\arabic{section}}` right after `\input{header}`).
- **Number figures and worked examples the same way** — `Fig. 5.1`, `Example 5.1` — via `\renewcommand{\thefigure}{...}` and a `\newtheorem{example}{Example}[section]`-style counter, not ad hoc "Worked Trace" subsection headings.
- **Use a formal `Definition` callout** for the handful of terms a lecture actually defines, rather than just bolding the term inline mid-paragraph.
- **Drop presentation-pacing headings** ("A Question We Skipped," "Socratic Check," "Bridge to Week N") — fold that motivating content into the surrounding topic-organized narrative instead of leaving it as a standalone lecture-pacing beat.

Notes are still never co-drafted and never edited independently of a Beamer change: if the Beamer deck changes, re-run `/lecture-notes` (or hand-propagate) and re-check with `/qa-notes`. See `.claude/skills/lecture-notes/SKILL.md` for the full template.

---

## TikZ Freshness Protocol (MANDATORY)

**For existing site or guide maintenance that uses a TikZ SVG, verify it matches
the current Beamer source before use.**

**This is now mechanically enforced, not just manually followed.** `scripts/check-tikz-freshness.py` (chained into `scripts/check-surface-sync.sh`, which runs on every `/commit` and every direct `git commit` once the pre-commit hook is installed) diffs every `\begin{tikzpicture}...\end{tikzpicture}` block between a Beamer source and its `Figures/<CODE>/<lecture>/extract_tikz.tex`, comment-stripped and whitespace-normalized. Added after a real near-miss: a Beamer diagram's label/border overlap got fixed in `Slides/`, but the already-extracted SVG kept the old, broken coordinate, and nothing caught it until a user explicitly asked to check. The manual procedure below is still the right way to *fix* a drift the gate flags — the gate only tells you *that* something drifted, not what changed.

### Diff-Check Procedure

1. Read the TikZ block from the Beamer `.tex` file
2. Read the corresponding block from `Figures/LectureN/extract_tikz.tex`
3. Compare EVERY coordinate, label, color, opacity, and anchor point
4. If ANY difference exists: update `extract_tikz.tex` from Beamer, recompile, regenerate SVGs
5. Only then reference the SVG in the existing site or guide artifact

### When to Re-Extract

Re-extract ALL TikZ diagrams when:
- The Beamer `.tex` file has been modified since last extraction
- Any TikZ-related quality issue is reported

---

## Environment Parity (LEGACY QUARTO)

This applies only when maintaining existing site or guide assets, not when
building course materials.

1. Scan the Beamer source for all custom environments
2. Check each against your theme SCSS file
3. If ANY environment is missing from SCSS, create it BEFORE translating

---

## Legacy Quarto Content Fidelity Checklist

Use only when a change to an existing site or guide artifact specifically
requires content parity:
```
[ ] Frame count: Beamer frames == Quarto slides
[ ] Math check: every equation appears with identical notation
[ ] Citation check: every \cite has a @key in Quarto
[ ] Environment check: every Beamer box has CSS equivalent
[ ] Figure check: every \includegraphics has SVG or plotly equivalent
[ ] No added content: Quarto does not invent slides not in Beamer
[ ] No dropped content: every Beamer idea appears in Quarto
```
