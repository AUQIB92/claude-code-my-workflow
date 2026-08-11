# CLAUDE.MD -- Academic Project Development with Claude Code

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Customize Beamer environments and CSS classes for your theme.
     Keep this file under ~150 lines — Claude loads it every session.
     See the guide at docs/workflow-guide.html for full documentation. -->

**Project:** Computer Science & Mathematics Coursework
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile/render and confirm output at the end of every task
- **Single source of truth** -- Beamer `.tex` is authoritative; Quarto `.qmd` derives from it
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to [MEMORY.md](MEMORY.md)

Cross-session context lives in [MEMORY.md](MEMORY.md); past plans, specs, and session logs are in [quality_reports/](quality_reports/).

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.MD                    # This file
├── .claude/                     # Rules, skills, agents, hooks
│   └── rules/knowledge-base-<CODE>.md  # One per course (e.g. -CS401.md)
├── Bibliography_base.bib        # Centralized bibliography (shared across courses)
├── Figures/<CODE>/<lecture>/    # TikZ SVGs, per lecture, namespaced by course
├── Preambles/header.tex         # LaTeX headers (shared)
├── Slides/<CODE>/               # Beamer .tex files, one subfolder per course
├── Quarto/<CODE>/                # RevealJS .qmd mirrors, same course subfolders
├── Notes/<CODE>/                # Prose Lecture Notes, derived from Slides/ (see single-source-of-truth.md)
├── syllabi/<CODE>.md            # One syllabus per course
├── docs/                        # GitHub Pages (auto-generated, mirrors Slides/Quarto nesting)
├── scripts/                     # Utility scripts + R code
├── quality_reports/             # Plans, session logs, merge reports, decision records
├── explorations/                # Research sandbox (see rules)
├── templates/                   # Session log, quality report templates
├── CompetitiveExam/             # Competitive-exam practice sets
│   ├── <CODE>/                 # Per-course sets: <lecture>-questions.tex / -answers.tex
│   └── Books/index.md           # Source registry: PYQ books, availability ladder, topic→page maps
└── master_supporting_docs/<CODE>/{supporting_papers,supporting_slides,supporting_books/<Book>/}
                                  # Course-scoped source material; supporting_books/<Book>/book.pdf
                                  # is gitignored (copyright), index.md is committed
```

**Multi-course convention.** `<CODE>` is a short course code (`CS401`, `MATH201`, ...). Course-less demo decks (e.g. `HelloWorld`) stay at the `Slides/`/`Quarto/` top level. Every skill that takes a lecture argument now takes `<CODE>/<lecture>` (e.g. `CS401/05-addressing-cpu-bus`).

**Course tag inside the deck.** Every Beamer deck sets `\coursecode{CS401}` right after `\input{header}` — it renders in the footer of every slide (see `Preambles/header.tex`), so the course is visible without opening the file path or the title page. The Quarto mirror carries the same tag via its RevealJS YAML `footer:` key.

---

## Commands

```bash
# LaTeX (3-pass, XeLaTeX only) — cd all the way into Slides/<CODE>/ (TeX writes
# output next to cwd using the file's basename, not next to the source path)
cd Slides/CS401 && TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
BIBINPUTS=../..:$BIBINPUTS bibtex file
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex
TEXINPUTS=../../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode file.tex

# Deploy Quarto to GitHub Pages — whole course, one lecture, or omit for everything
./scripts/sync_to_docs.sh CS401
./scripts/sync_to_docs.sh CS401/05-addressing-cpu-bus

# Quality score
python scripts/quality_score.py Quarto/CS401/file.qmd

# Palette sync (LaTeX ↔ SCSS)
./scripts/check-palette-sync.sh

# Surface-count sync (README ↔ CLAUDE.md ↔ guide ↔ landing page)
./scripts/check-surface-sync.sh
```

**Palette contract:** color names in `Preambles/header.tex` must match SCSS variables in `Quarto/theme-template.scss`. See [`Preambles/README.md`](Preambles/README.md).

**Windows/MiKTeX note:** the `:`-joined `TEXINPUTS`/`BIBINPUTS` above works on TeX Live (macOS/Linux). MiKTeX on Windows needs `;` instead (`TEXINPUTS="../../Preambles;"`) — a `:`-joined value silently fails to resolve `header.tex`/the `.bib` file. See `.claude/skills/compile-latex/SKILL.md`.

---

## Quality Thresholds (advisory)

| Score | Checkpoint | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

Enforced by `/commit` (halts + asks for override) **and** — once you run `./scripts/install-hooks.sh` — by a real git pre-commit hook (`.githooks/pre-commit`) that runs the surface-sync + quality (≥80) gates on every commit. Bypass sparingly with `SKIP_QUALITY_GATE=1` or `--no-verify`.

---

## Skills Quick Reference

The full table of all skills lives in [README.md](README.md#skills-claudeskills). Most-used, by workflow:

- **Slides / teaching:** `/create-lecture` `/compile-latex` `/deploy` `/qa-quarto` `/slide-excellence` `/syllabus` `/teach-from-paper` `/scaffold-exercises` `/lecture-notes` `/qa-notes` `/index-textbook`
- **Papers / review:** `/review-paper` (`--peer`) `/seven-pass-review` `/respond-to-referees` `/verify-claims` `/proofread` `/humanize` `/submission-disclosures`
- **Data / reproducibility:** `/data-analysis` `/did-event-study` `/simulation-study` `/audit-reproducibility` `/diagnose` `/replication-package` `/capture-environment` `/power-analysis` `/disclosure-check`
- **Research / writing:** `/interview-me` `/lit-review` `/research-ideation` `/preregister` `/grant-proposal` `/data-management-plan`
- **Meta / workflow:** `/commit` `/learn` `/new-skill` `/checkpoint` `/context-status` `/deep-audit` `/coauthor-brief` `/triage-inbox`

Stata (`/stata-replication`), R packages (`/r-package-check`), TikZ (`/extract-tikz`, `/new-diagram`), and more — see the README for the complete index.

---

## Beamer Custom Environments

| Environment / Macro | Effect | Use Case |
| --- | --- | --- |
| `\coursecode{CODE}` | Sets the footer course tag for the deck | Once per deck, right after `\input{header}` |
| `\key{text}` | Bold gold inline text | Terms/labels worth flagging inline |
| `\good{text}` / `\bad{text}` | Green / red inline text (semantic `positive`/`negative`) | Correct vs. incorrect, observed vs. problematic |
| `\muted{text}` | Neutral gray inline text | De-emphasized context |
| `\transitionslide{Title}` | Full-bleed dark-blue standout frame | Section-break / major conceptual pivot |
| `\sectiondivider{Label}{Title}` | Near-black divider: white label line, gold title, thin gold bottom rule | Numbered section/act break with a striking dark style |
| `block` / `exampleblock` / `alertblock` | Blue / green / gold titled boxes | Definition / worked example / key takeaway — max 2 per slide (INV-7) |

## Quarto CSS Classes

| Class | Effect | Use Case |
| --- | --- | --- |
| `.keybox`, `.highlightbox`, `.methodbox`, `.assumptionbox`, `.quotebox`, `.resultbox`, `.eqbox`, `.softbox` | Titled callout boxes (Quarto equivalents of the Beamer block triad) | Definitions, methods, assumptions, quotes, results — max 2 per slide (INV-7) |
| `.alert`, `.positive`, `.negative`, `.neutral` | Semantic inline colors | Mirrors Beamer's `\good`/`\bad`/`\muted`/alerted-text |
| `.hi`, `.hi-gold`, `.hi-yellow`, `.hi-slate`, `.hi-green`, `.hi-red` | Bold inline highlight family | Ad hoc emphasis beyond the semantic set |

---

## Current Project State

### Courses

| Code | Syllabus | Lectures built | Lectures planned |
| --- | --- | --- | --- |
| `CS401` — Computer Organization and Architecture (PCC CS-401) | [`syllabi/CS401.md`](syllabi/CS401.md) | 01 (Intro/Performance), 02 (Number Systems/Arithmetic), 03 (IEEE 754), 04 (Registers/Instructions), 05 (Addressing/CPU/Bus), 06 (Hardwired Control), 07 (Microprogrammed Control), 08 (I/O Techniques) | 09–12 per the syllabus work-list |
| `CS301` — Data Structures (PCC CS-301) | [`syllabi/CS301.md`](syllabi/CS301.md) | 01 (Foundations/Pointers/ADTs) | 02–12 per the syllabus work-list |

### Non-course demos

| Lecture | Beamer | Quarto | Key Content |
| --- | --- | --- | --- |
| HelloWorld *(sample — delete when ready)* | `Slides/HelloWorld.tex` | `Quarto/HelloWorld.qmd` | Minimal deck to verify setup |
