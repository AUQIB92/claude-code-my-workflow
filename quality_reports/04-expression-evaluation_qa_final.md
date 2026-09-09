# QA Final — CS301/04-expression-evaluation (Quarto vs Beamer)

**Verdict: APPROVED (source-parity) with HTML-render gates BLOCKED — quarto binary missing.**
**Rounds: 1 (converged — 0 CRITICAL/MAJOR findings; loop-until-dry, cap 5 not reached).**
**Date:** 2026-09-09. Benchmark: `Slides/CS301/04-expression-evaluation.tex` (+ compiled PDF
`04-expression-evaluation.pdf`). Mirror: `Quarto/CS301/04-expression-evaluation.qmd`.

## Hard-gate status

| Gate | Status | Evidence |
|---|---|---|
| Content parity | PASS | 31 `\begin{frame}` + 5 `\transitionslide` + 4 `\sectiondivider` = 40 slides; qmd has exactly 40 `##` sections. Titlepage correctly folded into YAML (matches Week-03 convention). All 4 TikZ figures referenced (`tikz_exact_00..03.svg`, 0-based). All 3 `\cite` sites converted to `[@key]` (keys verified in `Bibliography_base.bib`). All 5 `semiverbatim` blocks as fenced code; all 3 tables (precedence, 14-row conversion trace, 7-row Hanoi trace) row-complete; all math verbatim. |
| Notation fidelity | PASS | Every `\key` → `[**..**]{.hi-gold}`, `\bad` → `[..]{.negative}`, `\muted` → `[..]{.neutral}`; `exampleblock` → `highlightbox`, `block` → `methodbox`. Spot-checked recurrence slide, Hanoi pricing, prediction answers. |
| Citation conversion | PASS | HorowitzSahni2008, Karumanchi2017, Wirth2004 all `[@..]`; `footer: "CS301"` + `bibliography:` in YAML; `::: {#refs}` closing slide. |
| Overflow | UNVERIFIABLE | No quarto binary (`Get-Command quarto` → not found, same as Week 03). Cannot render HTML. |
| Visual regression | UNVERIFIABLE | Same blocker — no HTML to compare against Beamer PDF. |
| Slide centering | UNVERIFIABLE | Same blocker. |
| Plot quality | N/A | No R/plotly figures in this deck (TikZ SVGs only, all 4 extracted + valid XML, 15–34 KB). |

## Round 1 (critic — source diff, self-review)

- FINDING-1 (minor, cosmetic): "Infix, Postfix, Prefix" definition block reflows the bold title
  vs tex (`Definitions (standard treatment; ...)`). Content-identical; Week-03 qmd uses the same
  `methodbox` + bold-lead style. No fix applied (intentional style normalization).
- No CRITICAL, no MAJOR. Loop converges per loop-until-dry (0 new CRITICAL/MAJOR).

## Fixer

No fixes required. No re-audit rounds needed.

## Supporting checks

- `scripts/check-tikz-prevention.py`: PASS (P3+P4).
- `extract_tikz.pdf`: 4 pages, compiled clean via XeLaTeX (MiKTeX); SVGs via `pdftocairo -svg`
  per page (`pdf2svg` absent) — valid SVG markup confirmed.
- `scripts/quality_score.py`: **100/100 [EXCELLENCE]** (static checks only; compilation unverified).

## Remaining issues / open

1. **HTML render + browser visual check BLOCKED** — install Quarto
   (`winget install --id Posit.Quarto -e`, then `./scripts/validate-setup.sh`) and run
   `./scripts/sync_to_docs.sh CS301/04-expression-evaluation`, then re-run qa-quarto
   rounds against the HTML for the Overflow / Visual / Centering gates.
2. Course hub page (stage 7) untouched per scope; progress registry untouched per scope.
