# Notes Critic Report — CS301/06-linked-lists-singly — Round 1

**Beamer:** `Slides/CS301/06-linked-lists-singly.tex` (26 frames, 35pp, compiles clean)
**Notes:** `Notes/CS301/06-linked-lists-singly-notes.tex` (8pp PDF, compiles clean, 0 errors, 0 overfull)
**Date:** 2026-09-26

## Gate checks

| Gate | Result |
|------|--------|
| Content parity | PASS — every frame's core idea present (see frame map below) |
| No invention | PASS — body traces apply deck algorithms to deck data; only Exercises contain a new instance (5-15-25 search/display), as mandated by the lecture-notes Detail Bar |
| Citation parity | PASS — deck has 2 `\cite` instances / 2 distinct keys (`Sedgewick2011_algorithms`, `Karumanchi2017_data_structures_algorithms_made_easy`); Notes contains exactly those 2 keys, no new keys |
| Notation fidelity | PASS — `\texttt{head}`, `\texttt{p->next}`/`\texttt{p->prev}`, `\texttt{NULL}`, `\texttt{malloc}`/`\texttt{free}`, `$T(n)$`, `$O/\Theta$` all match deck + Notation Registry |
| Textbook-page honesty | PASS — pp.74–162 (Karumanchi Ch.3) and p.142 (Sedgewick Sec.1.3) inherited 1:1; Horowitz & Sahni Ch.4 / AHU Ch.2 kept chapter-level; no invented page numbers |

## Frame map (deck → notes)

- Titlepage → `\title`/`\author` ✓
- Today's Four Questions → Sec 6.1 para 1 (all 4 + plan) ✓
- Handoff Week 5 → Sec 6.1 para 2 (contract, mod fix, count/Lab P5, deques, Lab P6, Unit I, slots, promise quote) ✓
- Calculator symbol table → Sec 6.1 para 3 (pipeline, `(a+b)*c`, OS/browser/playlist/Wk7, design principle) ✓
- Where This Week Sits → Sec 6.1 para 4 (Wk1/Wk2/Wk7/Wk10 pointers, `head`/`p->next`, muted arc) ✓
- 4× transitionslide/sectiondivider → folded into section intros (per skill, no standalone needed) ✓
- Slot Tax → Sec 6.2 (n moves, shift, malloc/copy/free, position tax, buying question) ✓
- Array-vs-nodes TikZ → Fig 6.1, verbatim ✓
- Node definition → definitionbox + both cites + malloc trace + head/leak + NULL ✓
- Build 10-20-30 → Example (4 steps + arrows-not-addresses + malloc/free) ✓
- Honest Bill table → reproduced + asterisk + workload rule ✓
- Three Shapes TikZ → Fig 6.2 + shape definitionbox ✓
- Applications → rule-of-thumb definitionbox + cite + symbol table / OS / polynomials ✓
- Editor prediction → Example (A/B/C + answer B) ✓
- Front-insert code → verbatim + order lesson + O(1) + NULL check ✓
- Front-insert TikZ → Fig 6.3 + finger trace + worked 5-trace Example ✓
- Position/End insert → verbatim walk-then-splice + O(n) + both guards ✓
- Delete code → verbatim + bypass/reclaim/never-touch + Week-1 dangling + O(n)/O(1) ✓
- Delete-middle TikZ → Fig 6.4 + step-by-step + leak/dangling ✓
- Search/Display → verbatim loops + cases + head-stays-put + worked Example ✓
- Reverse motivation → playlist 500 + re-point + Socratic pause + answer ✓
- Reverse loop → verbatim + T(n) + full 3-iteration Example ✓
- Reverse mid-pass TikZ → Fig 6.5 + frontier prose ✓
- Price list table → reproduced + house rule ✓
- Three mistakes → all 3 + revise line ✓
- Summary + Next week → all 3 keys + Wk7 pointer ✓
- Before You Go → Example with deck's 3 answers ✓
- References → `\bibliography{../../Bibliography_base}` ✓

## TikZ / P7 audit

- 5/5 diagrams reused; mechanical count `\draw`+`\node[` deck 76 = notes 76 → verbatim.
- P7 clearance: labels carry ≥0.15cm offsets inherited from deck source; no path crosses a box except at connection points; no label on a line. PASS.

## Worked-solution verification (independent re-derivation)

- Pos-2 insert of 25 (Ex.2): p stops on 10, splice order correct, final chain 20→10→25→30 ✓
- Head-delete 10 + tail-delete 30 (Sol.3): bypass/free pairs correct ✓
- Reverse iters (Sol.5): prev/curr/next states re-derived, match ✓

## Findings

- Critical: 0. Major: 0. Minor: 0.

## Verdict: APPROVED (round 1)
