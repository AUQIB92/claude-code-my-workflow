# qa-notes: CS301/05-queues — Critic Report (Round 2, final)

Date: 2026-09-17 | Stage 2 of /build-week CS301/05
Beamer: Slides/CS301/05-queues.tex (29 frames/38 pages, compiled clean)
Notes: Notes/CS301/05-queues-notes.tex → 05-queues-notes.pdf (8 pages)

## Method

No Task subagent facility in this session; critic/fixer performed inline
against the qa-notes hard gates (content parity, no invention, citation
parity, notation fidelity, textbook-page honesty).

## Round 1 findings

- MINOR (Exercises/Solutions): Ex.2 solution said "wraps at both enqueues
  of Y and Z" — wrong on both ends: the X enqueue (rear 3→0) is also a
  wrap, and Z is refused (full), so Z wraps nothing.
- No critical or major findings. All 29 frames + 5 transitions + references
  frame traced to a Notes location (see mapping in session transcript).
- Citation parity: 4 \cite commands, identical keys/groupings in both files.
- Notation: front/rear, Q[0..n-1], mod wraparound, O(·) always with worst
  case, \texttt verbs — all faithful.
- Page honesty: Karumanchi Ch.5 pp.205–223, Ch.7 pp.369–408, Sedgewick p.120
  / p.308 all inherited 1:1 from deck header; Horowitz& Sahni / AHU stay
  chapter-level. No upgrades.
- TikZ P7 overlap audit: all 4 reused diagrams keep deck coordinates; arrows
  join node anchors only, labels ≥0.3 cm clear, scan/arc lines run in gaps.

## Fix applied

Ex.2 solution now reads: "wraps at the enqueues of X (3→0) and Y (0→1);
Z refused". Recompiled: 8 pages, zero undefined citations/references.

## Round 2 re-audit

0 new critical/major findings (deduped). Loop-until-dry satisfied
(2nd consecutive round with 0 new critical/major).

## Verdict: APPROVED

Cosmetic only (inherited class, not gates): 3 sub-point overfull hboxes,
3 'h'→'ht' float promotions, 1 TU/lmtt font-shape substitution — same
profile as 04-expression-evaluation-notes.
