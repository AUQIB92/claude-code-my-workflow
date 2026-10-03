# QA Final — CS301/07-linked-lists-doubly-applications (Quarto vs Beamer)

**Verdict: APPROVED (source-parity) with HTML-render gates BLOCKED — quarto binary missing.**
**Rounds: 1 (converged — 0 CRITICAL/MAJOR findings; loop-until-dry, cap 5 not reached).**
**Date:** 2026-10-03. Benchmark: `Slides/CS301/07-linked-lists-doubly-applications.tex`
(+ compiled PDF `07-linked-lists-doubly-applications.pdf`, 39 frames).
Mirror: `Quarto/CS301/07-linked-lists-doubly-applications.qmd`.

## Hard-gate status

| Gate | Status | Evidence |
|---|---|---|
| Content parity | PASS | 29 `\begin{frame}` + titlepage + 5 `\transitionslide` + 4 `\sectiondivider` = 39 slides; qmd has 38 `##` sections + YAML title slide = 39. Title sequence matches the deck 1:1 in order. All 7 TikZ figures referenced (`tikz_exact_00..06.svg`, 0-based). All 5 `\cite` sites converted to `[@key]` (all keys verified in `Bibliography_base.bib`). All 6 `semiverbatim` blocks as fenced code; all 4 tables row-complete; all math verbatim. |
| Notation fidelity | PASS | `\key`→`[**..**]{.hi-gold}` 14/14, `\bad`→`{..}{.negative}` 3/3, `\muted`→`{..}{.neutral}` 5/5, `\good` 0/0. Spot-checked price-list, polynomial-node, worked-addition and prediction slides. |
| Citation conversion | PASS | Karumanchi2017, Wirth2004, Sedgewick2011, HorowitzSahni2008, AhoHopcroftUllman1983 all `[@..]`; `footer: "CS301"` + `bibliography:` in YAML; `::: {#refs}` closing slide. |
| Overflow | UNVERIFIABLE | No quarto binary (`Get-Command quarto` → not found, same as Weeks 03/04). Cannot render HTML. |
| Visual regression | UNVERIFIABLE | Same blocker — no HTML to compare against Beamer PDF. |
| Slide centering | UNVERIFIABLE | Same blocker. |
| Plot quality | N/A | No R/plotly figures in this deck (TikZ SVGs only, all 7 extracted + valid XML, 25–75 KB). |

## Fallback statement (critic/fixer subagents unavailable)

The `qa-quarto` skill calls for spawning `quarto-critic` then `quarto-fixer`. This session
has no Task/subagent tool, so the **source-parity diff was done manually, frame-by-frame
against the `.tex` deck** (mechanical counts + title-sequence comparison + notation sweep).
No fixer was needed: round 1 produced 0 CRITICAL and 0 MAJOR findings. Full report:
`quality_reports/07-linked-lists-doubly-applications_qa_critic_round1.md`.

## Round 1 (manual critic — source diff)

- FINDING-1 (minor, cosmetic, no fix): literal `\quad` retained between prediction options,
  matching the Week-04 mirror convention. Content-identical to Beamer.
- FINDING-2 (minor, notation, FIXED): `$\to$` trapped in a code span on the polynomial-node
  example; moved outside backticks.
- No CRITICAL, no MAJOR. Loop converges per loop-until-dry (0 new CRITICAL/MAJOR).

## Fixer

One minor notation fix applied (FINDING-2: `$\to$` trapped in a code span on the
polynomial-node example → moved outside backticks). Does not affect any hard gate; no
re-audit rounds needed.

## Supporting checks

- `scripts/check-tikz-prevention.py`: **PASS** (P3+P4).
- `extract_tikz.pdf`: **7 pages**, compiled clean via XeLaTeX (MiKTeX); SVGs via
  `dvisvgm --pdf` per page (`pdf2svg`/`inkscape` absent, Ghostscript absent — dvisvgm 3.1.1
  handled PDF→SVG natively) — valid SVG markup confirmed.

## Deployment

- `bash scripts/sync_to_docs.sh CS301/07-linked-lists-doubly-applications` → **exit 0**.
- `quarto render` warned + skipped (no binary); Beamer/Notes/Assignment/CompetitiveExam
  PDFs and Figures synced.
- Published `07-` artifacts: `docs/slides/CS301/07-linked-lists-doubly-applications.pdf`,
  `docs/notes/CS301/07-…-notes.pdf`,
  `docs/assignments/CS301/07-…-assignment.pdf` + `07-…-coding-assignment.pdf`,
  `docs/competitive-exam/CS301/07-…-questions.pdf` + `07-…-answers.pdf`,
  `docs/Figures/CS301/07-linked-lists-doubly-applications/tikz_exact_00..06.svg`.
- Instructor-only files confirmed **NOT** published (`*-solutions*`, `reference_solution.c`,
  `test_hidden.c`, `autograder.sh` all absent under `docs/`).

## Remaining issues / open

1. **HTML render + browser visual check BLOCKED** — install Quarto
   (`winget install --id Posit.Quarto -e`, then `./scripts/validate-setup.sh`) and run
   `./scripts/sync_to_docs.sh CS301/07-linked-lists-doubly-applications`, then re-run
   qa-quarto rounds against the HTML for the Overflow / Visual / Centering gates.
2. Course hub page (Stage 7) untouched per scope; progress registry untouched per scope.
