# QA Notes Report — CS301 Week 04 (04-expression-evaluation)

Source: `Slides/CS301/04-expression-evaluation.tex` (41 frames, compiled clean).
Notes: `Notes/CS301/04-expression-evaluation-notes.tex` (9 pages, XeLaTeX 3-pass + bibtex, MiKTeX `;` separators).

## Method

No Task subagent facility in this environment; critic/fixer passes performed
inline against the qa-notes hard gates (content parity, no invention,
citation parity, notation fidelity, textbook-page honesty).

## Round 1 — audit (all 41 frames checked)

- Content parity: 41/41 frames' core ideas present. All 5 Socratic checks and
  the 3 Before-You-Go predictions folded as worked checks with deck answers.
  All 4 TikZ diagrams reused verbatim (pipeline, expression tree, runtime
  frames, Hanoi pegs). Both algorithms + `fact` + Hanoi pseudocode verbatim.
  Full 14-row `a+b*c-(d+e/f)` trace, 7-move Hanoi trace, recurrence unfolding
  all match deck values.
- Finding (minor, 1): Lab tags `(Lab P3)` x2 / `(Lab P4)` x1 and the
  Before-You-Go "check in the lab (P3, P4)" pointer had no corresponding line.
- No invention, citation parity (3 `\cite` keys, same as deck), notation
  fidelity, page-honesty (Karumanchi pp.163-204 / pp.62-73, Wirth pp.87-108
  all inherited from deck header; Horowitz&Samni/AHU chapter-level only).

## Fix applied

One line under `\subsection*{Exercises}`: "both infix conversions are Lab P3,
prefix to postfix is Lab P4." Recompiled clean.

## Round 2 — re-audit: APPROVED, 0 new findings.

Verdict: **APPROVED after 2 rounds.** Loop stopped per loop-until-dry
(2nd consecutive round adds 0 new critical/major findings).
