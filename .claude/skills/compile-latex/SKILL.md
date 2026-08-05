---
name: compile-latex
description: Compile a Beamer LaTeX slide deck with XeLaTeX (3 passes + bibtex). Use when user says "compile", "build the slides", "rebuild the PDF", "run latex", "render the tex", or asks why a `.tex` file isn't producing a PDF. Operates on `Slides/<CourseCode>/*.tex`.
argument-hint: "[CourseCode/filename without .tex extension], e.g. CS401/05-addressing-cpu-bus"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile Beamer LaTeX Slides

Compile a Beamer slide deck using XeLaTeX with full citation resolution.

## Steps

1. **Navigate all the way into the course subfolder** and compile with 3-pass sequence. `$ARGUMENTS` is course-qualified (e.g. `CS401/05-addressing-cpu-bus`) — split it into the course directory and the bare filename. TeX writes its output (`.aux`/`.log`/`.pdf`) using the *basename* of the input into the **current working directory**, not next to the source file, so `cd` must land exactly where the source lives; `TEXINPUTS`/`BIBINPUTS` then need one extra `../` to reach `Preambles/`/the repo root from that one-level-deeper cwd:

```bash
cd Slides/CS401
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
BIBINPUTS=../..:$BIBINPUTS bibtex 05-addressing-cpu-bus
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
```

In general, with `$ARGUMENTS` = `<CODE>/<lecture>`:

```bash
cd "Slides/$(dirname $ARGUMENTS)"
lecture="$(basename $ARGUMENTS)"
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode "$lecture.tex"
BIBINPUTS=../..:$BIBINPUTS bibtex "$lecture"
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode "$lecture.tex"
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode "$lecture.tex"
```

For a course-less deck at the `Slides/` top level (e.g. `HelloWorld`), `dirname` returns `.`, so `cd Slides/.` is just `cd Slides` and `TEXINPUTS`/`BIBINPUTS` should drop back to `../Preambles`/`..` — check `dirname $ARGUMENTS` before running and adjust the `../` count accordingly.

**Alternative (latexmk):**
```bash
cd "Slides/$(dirname $ARGUMENTS)"
TEXINPUTS=../../Preambles:$TEXINPUTS BIBINPUTS=../..:$BIBINPUTS latexmk -xelatex -interaction=nonstopmode "$(basename $ARGUMENTS).tex"
```

2. **Check for warnings:**
   - Grep output for `Overfull \\hbox` warnings
   - Grep for `undefined citations` or `Label(s) may have changed`
   - Report any issues found

3. **Open the PDF** for visual verification:
   ```bash
   open Slides/$ARGUMENTS.pdf          # macOS
   # xdg-open Slides/$ARGUMENTS.pdf    # Linux
   ```

4. **Report results:**
   - Compilation success/failure
   - Number of overfull hbox warnings
   - Any undefined citations
   - PDF page count

## Why 3 passes?
1. First xelatex: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: Incorporates bibliography
4. Third xelatex: Resolves all cross-references with final page numbers

## Important
- **Always use XeLaTeX**, never pdflatex
- **TEXINPUTS** is required: your Beamer theme lives in `Preambles/`
- **BIBINPUTS** is required: your `.bib` file lives in the repo root
