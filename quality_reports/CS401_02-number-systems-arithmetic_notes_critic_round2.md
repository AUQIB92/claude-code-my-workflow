# Notes vs Beamer Parity Audit: CS401/02-number-systems-arithmetic (Round 2)

**Beamer source:** `Slides/CS401/02-number-systems-arithmetic.tex` (37 `\begin{frame}` environments + title page + 7 `\transitionslide` standouts)
**Notes:** `Notes/CS401/02-number-systems-arithmetic-notes.tex`
**Round:** 2  **Date:** 2026-08-10

## Verdict: NEEDS REVISION

Both round-1 CRITICAL findings (C1 ripple-carry TikZ, C2 division traces) and the MAJOR finding (M1 Week-1 recap) are verified genuinely resolved — division traces were independently re-derived and are arithmetically correct. However this pass surfaced two new MAJOR issues.

## Verification of Round-1 Fixes

- C1 (ripple-carry TikZ) — CONFIRMED RESOLVED, byte-identical to Beamer.
- C2 (13÷3 traces) — CONFIRMED RESOLVED, arithmetic independently re-derived and correct (restoring: A=0001,Q=1010 → A=0000,Q=0101 → A=0000,Q=1010 → A=0001,Q=0100; non-restoring converges to quotient 4, remainder 1).
- M1 (Week-1 recap) — CONFIRMED RESOLVED.

## Major Issues (SHOULD FIX)

### M2: Half-Adder/Full-Adder block diagram missing entirely from the Notes
- Beamer "Definition: Half Adder and Full Adder" (lines 338-368) has a TikZ block diagram (FA box, A/B/Cin in, S/Cout out) with a coordinate-map comment (lines 346-351).
- Notes §3 "Adder Hardware" (lines 134-150) has the equations/truth table but no figure/TikZ/prose for the block diagram — the only one of the deck's four TikZ diagrams not reproduced in the Notes.
- Fix: Add a `\begin{figure}` reproducing the Beamer's full-adder block TikZ verbatim (with coordinate-map comment) plus a sentence narrating the I/O layout.

### M3: "Socratic Check" / "Bridge to Week N" presentation-pacing headings retained verbatim
- Rule violated: `single-source-of-truth.md` — Notes must fold pacing beats into topic-organized narrative, not keep them as standalone headings. User memory (`feedback_lecture_notes_textbook_format.md`) reinforces this.
- Notes retains these as `\subsection` headings verbatim in 7 places: lines 78, 97, 130, 222, 286, 387 ("Socratic Check: ...") and 400 ("Bridge to Week 3").
- Fix: Retitle each descriptively by topic and fold "Bridge to Week 3" into the closing paragraph of Synthesis rather than a standalone heading.

## Minor Issues (NICE TO FIX)

- m1: Two citations added to figure captions (lines 282, 347) not present in corresponding Beamer frames — page-honest, reused keys/pages, low priority.
- m2: `\thetable` not renewed to match `2.\arabic{...}` convention used for section/figure — full-adder truth table will render as "Table 1" not "Table 2.1". Fix: add `\renewcommand{\thetable}{2.\arabic{table}}`.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames | 37 (+ title page, + 7 transition standouts) |
| Citation keys: Beamer / Notes | 3 / 3 (identical) |
| Critical / Major / Minor (this round) | 0 / 2 / 2 |
| Round-1 findings verified resolved | 3 / 3 (C1, C2, M1) |
