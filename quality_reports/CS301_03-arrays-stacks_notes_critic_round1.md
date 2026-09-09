# QA Notes — CS301/03-arrays-stacks — Critic Round 1 (manual; no Task tool in this environment)

Source: `Slides/CS301/03-arrays-stacks.tex` (39 frames) vs `Notes/CS301/03-arrays-stacks-notes.tex` (v1).

## Frame-by-frame parity (39/39 present or legitimately folded)
- Title, 3 questions, calculator, positional-vs-nested, week position → Sec 1. ✓
- Transitions (3×) + section dividers (4×) folded into topic prose per lecture-notes Phase 2. Legitimate. ✓
- Array def + cite, 1D TikZ (verbatim), 1D formula + 2012, bounds, costs, n=1000 check → Sec 2. ✓
- 2D def, 2×3 TikZ (verbatim), row-major + 1024, column-major + 1028, A[2][0]→1032 → Sec 3. ✓
- Stack def + Sedgewick cite, contract + Karumanchi cite, code (semiverbatim→verbatim, content identical), top-move TikZ (verbatim), overflow/underflow + O(1), top-trace check → Sec 4. ✓
- Bracket problem + algorithm + O(n)/O(n) + trace table + `{(()}[` prompt → Sec 5. ✓
- Postfix def + scope + cite, eval algorithm + order note, 2-3-4 trace → Sec 5. ✓
- 3 mistakes, summary, next-week bridge, 3 predictions + keys, references → Sec 6 + Exercises/Solutions. ✓

## Citations: 5/5 keys preserved (HorowitzSahni2008, Wirth2004, Sedgewick2011, Karumanchi2017, AhoHopcroftUllman1983). Page-pointers unchanged from deck; no upgrades. ✓
## Notation: formulas, `top`, O(·) with cases, `\texttt` identifiers all match deck. TikZ P7 audit PASS (edge-terminated arrows only, labels clear/inside boxes). ✓

## Findings
- **MAJOR-1:** Solution 3 (Exercises) prose is muddled — hedges around the `{[( )]}` trace instead of giving a clean token-by-token walk ending in the deck's keyed verdict. Rewrite for a straight trace → deck verdict.
- **CRITICAL-1 (deck-internal, escalated not patched):** the deck's Before-You-Go Q3 key ("no — the `(` meets `]`") does not follow from its own algorithm applied to the literal printed string `{[( )]}` = `{`,`[`,`(`,`)`,`]`,`}`, which traces to empty → balanced. Notes must stay faithful to the deck key (SSOT); flag to user as a deck bug candidate for Week 3 errata. Do NOT "fix" by inventing a different string in Notes.

Verdict Round 1: **CHANGES REQUESTED** (1 major reword; 1 escalation).
