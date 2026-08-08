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

**Windows / MiKTeX variant** (separator is `;`; set the env var inline for the command only):
```cmd
cd Slides\CS401
set TEXINPUTS=../../Preambles;
set BIBINPUTS=../..;
xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
bibtex 05-addressing-cpu-bus
xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
```
Or from Git Bash (PowerShell is not recommended for env-var-prefix commands):
```bash
cd Slides/CS401
TEXINPUTS="../../Preambles;" BIBINPUTS="../..;" xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
BIBINPUTS="../..;" bibtex 05-addressing-cpu-bus
TEXINPUTS="../../Preambles;" xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
TEXINPUTS="../../Preambles;" xelatex -interaction=nonstopmode 05-addressing-cpu-bus.tex
```
If `xelatex` is not on PATH, add MiKTeX's bin dir first (typically `C:\Users\<you>\AppData\Local\Programs\MiKTeX\miktex\bin\x64`): `set PATH=%PATH%;C:\Users\<you>\AppData\Local\Programs\MiKTeX\miktex\bin\x64`.

2. **Check for warnings:**
   - Grep output for `Overfull \\hbox` warnings
   - Grep for `undefined citations` or `Label(s) may have changed`
   - Report any issues found

3. **Open the PDF** for visual verification:
   ```bash
   open Slides/$ARGUMENTS.pdf          # macOS
   # xdg-open Slides/$ARGUMENTS.pdf    # Linux
   ```
   Windows: `start Slides\$ARGUMENTS.pdf` (forward the path as-is) or just open the PDF in your default viewer.

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
- **Path separator is platform-dependent.** TeX Live (macOS/Linux) accepts `:` (as shown above). **MiKTeX on Windows requires `;`** — `TEXINPUTS="../../Preambles;"` / `BIBINPUTS="../..;"` — a `:`-joined value silently fails to find `header.tex`/the `.bib` file with no clear error (verified: MiKTeX 25.12 on Windows). If a compile can't find `header.tex` despite the file existing at the expected relative path, try the other separator before debugging further.
- **`\bibliography{}` and `\input{}` calls inside a `.tex` file use literal relative paths, not TEXINPUTS/BIBINPUTS resolution** — e.g. `\bibliography{../../Bibliography_base}` from `Slides/<CODE>/`. If a deck is ever moved to a different nesting depth, these hardcoded paths inside the file must be updated too, separately from any TEXINPUTS/BIBINPUTS env var.
