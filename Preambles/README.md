# Preambles

Shared LaTeX/Beamer preamble for lectures in this project.

## Usage in a lecture

```latex
\documentclass{beamer}
\input{header}   % resolves via TEXINPUTS=../Preambles:$TEXINPUTS

\title{Your Lecture}
\author{You}
\date{\today}

\begin{document}
\frame{\titlepage}
% ...
\end{document}
```

Compile with `/compile-latex <file>` — the skill sets `TEXINPUTS` for you. For manual compilation:

```bash
cd Slides
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode YourLecture.tex
```

## The palette contract

Color names in `header.tex` **must** match the SCSS variable names in [`../Quarto/theme-template.scss`](../Quarto/theme-template.scss) so Beamer and Quarto renderings use the same palette.

The `scripts/check-palette-sync.sh` script greps both files and reports any divergence:

```bash
./scripts/check-palette-sync.sh
```

It's also invoked (non-blocking) from `./scripts/validate-setup.sh`.

When you customize the palette for your project:

1. Edit HEX values in both `Preambles/header.tex` (LaTeX) **and** `Quarto/theme-template.scss` (SCSS).
2. Keep the names aligned: `primary-blue`, `primary-gold`, `highlight-yellow`, `light-bg`, `jet`, `positive`, `negative`, `neutral`, `hi-slate`, `hi-green`, `hi-red`.
3. Run `./scripts/check-palette-sync.sh` — it should report "in sync".

## What's inside

- **Palette** — 11 named colors matching the SCSS.
- **Beamer theme assignments** — structure, titles, itemize, alert, blocks, minimal footer. Applied only under Beamer (`\@ifundefined{beamertemplate}`).
- **TikZ libraries** — `arrows.meta, positioning, calc, decorations.pathreplacing, fit, shapes.geometric, backgrounds`.
- **Shared TikZ styles** — `dag-node`, `decision-node`, `observed-edge`, `counterfactual-edge`, `confound-edge`, `observed-dot`, `counterfactual-dot`. Used by `templates/tikz-snippets/` and reusable in hand-written diagrams.
- **Convenience macros** — `\muted{...}`, `\key{...}`, `\good{...}`, `\bad{...}`, `\transitionslide{...}`.

## Extending

Add packages your lectures need *after* your `\input{header}` in each lecture, not in this file — that keeps the preamble small and auditable. Only add to `header.tex` if you are certain every lecture in the project needs it.

For a lecture-specific preamble (rare), create `Preambles/lectureN-addon.tex` and `\input` it after `header.tex`.
