# QA Final — CS301/03-arrays-stacks (Quarto vs Beamer)

Date: 2026-09-09 | Mode: static audit (quarto binary absent — render-dependent gates unverified)

## Hard gates

| Gate | Status |
|------|--------|
| Content parity | PASS — 31 `\begin{frame}` + titlepage + 5 `\transitionslide` + 4 `\sectiondivider` all mapped; 40 H2 slides + YAML title slide |
| Notation fidelity | PASS — 1D / row-major / column-major formulas + worked values (2012, 1024, 1028, 5052) verbatim |
| Citation conversion | PASS — 5 keys (`HorowitzSahni2008`, `Wirth2004`, `Sedgewick2011`, `Karumanchi2017`, `AhoHopcroftUllman1983`) → `[@...]`; all exist in `Bibliography_base.bib` |
| TikZ refs | PASS — `tikz_exact_00/01/02.svg` exist (13–22 KB), referenced in slide order |
| Env mapping | PASS — block→methodbox, exampleblock→highlightbox, alertblock→keybox; `\key/\good/\bad/\muted` → hi-gold/positive/negative/neutral |
| Overflow | UNVERIFIED — no quarto render |
| Visual regression / centering | UNVERIFIED — no quarto render |

## Rounds

- R1 critic: 6 LaTeX-escape leaks (`vs.\`, `et.\`/`al.\`, `Ch.~`) + confirmed counts.
- Fixer: replaced with plain markdown (`vs.`, `et al.`, `Ch. N`); re-audit R2: 0 findings → converge.

## Verdict

CONDITIONAL PASS — ship QMD + PDFs; re-run full render QA once quarto is installed
(`winget install --id Posit.Quarto -e`, then `./scripts/validate-setup.sh`).
Beamer PDF benchmark: 42 pages (refs span 2 via allowframebreaks; QMD refs slide scrolls — acceptable).
