---
name: accreditation-autopilot
description: Roll up NBA/AICTE CO-PO-PSO accreditation data across every course in a program into one program-level Self-Assessment Report — generating any missing per-course draft first (by following /accreditation's own phases), then combining all of them under one program heading with a mechanically-computed PO-coverage summary. Use when user says "roll up accreditation for the program", "generate the program self-assessment report", "run accreditation autopilot", "build the CSE self-assessment report", or invokes `/accreditation-autopilot <program>`. NOT a replacement for `/accreditation` (still the per-course generator this skill calls) — this is the cross-course rollup NBA actually evaluates, which no single-course run produces. The output is a faculty/program-coordinator-review DRAFT, never an authoritative filing, same discipline as `/accreditation`.
argument-hint: "<program> (e.g. CSE)"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
effort: high
disable-model-invocation: true
---

# Accreditation Autopilot

NBA accredits a *program* (the whole degree), not a single course. `/accreditation` generates one course's CO-PO-PSO draft at a time; this skill discovers every course in a named program, fills in any course that's missing its draft, and rolls all of them up into one program-level Self-Assessment Report — the actual unit an accreditation body evaluates.

**MVP scope.** Automates the proof-of-concept validated by hand this session (`Accreditation/CS301/co-po-attainment.tex` + `Accreditation/CSE/self-assessment-report.tex`) for however many courses a program actually has, not a hardcoded pair. No cold-persona "NBA assessor dry-run" critique and no "Regulatory Diff" phase yet — both are this feature's Phase 3 (Differentiation), explicitly out of scope here.

## Phase 0 — Discover the program's courses

Grep `syllabi/*.md` for the program token (e.g. `"B.Tech CSE"` — match the exact string the user passed, since that's how courses self-report their program per `syllabi/CS401.md`/`CS301.md`'s own line 1 convention: `"# <Course Name> (<code>) — B.Tech <program>, Semester N"`). Collect every course code that matches. Halt with a clear message if zero courses match — do not guess a program name the syllabi don't state.

## Phase 1 — Fill any missing per-course draft

For each discovered course code, check whether `Accreditation/<CODE>/co-po-attainment.tex` already exists.

- **If it exists:** use it as-is. Do not regenerate a course's draft just because this skill ran — a human may have started reviewing/editing it.
- **If it's missing:** generate it by following [`.claude/skills/accreditation/SKILL.md`](../accreditation/SKILL.md)'s own Phases 0-5 for that course, exactly as written there (pre-flight, CO extraction + Bloom-tagging, CO-PO-PSO matrix draft, assessment-tool mapping, attainment methodology, emit `Accreditation/<CODE>/co-po-attainment.tex`). Do not re-derive or restate those phases here — read that file and execute it. This is the automation of the PoC's manual "run `/accreditation` for the second course" step, generalized to however many courses are actually missing a draft.
- **If that pre-flight halts** (a course's syllabus exists but `.claude/rules/knowledge-base-<CODE>.md` doesn't — a genuinely unstarted course, not just an unbuilt one) — do not halt the whole autopilot run over it. Skip that course, note it by name in the rollup's Program Scope section as "not yet ready for accreditation (no knowledge-base file)," and continue with the rest.

## Phase 2 — Roll up into one program-level report

Write `Accreditation/<program>/self-assessment-report.tex`: same structure as the hand-built `Accreditation/CSE/self-assessment-report.tex` proof of concept —

1. Program scope (program name, which courses are rolled up, and an explicit note that this is partial if the program has courses with no built content yet — e.g. a semester whose lectures aren't authored, so it can't have a syllabus-derived CO table at all).
2. Course Outcomes by course (a short summary per course, pointing at each course's own Table 1 rather than re-copying it).
3. **PO-coverage summary table** — one row per PO touched by at least one CO, with a per-course count and a total.
4. Regulatory note (the 12-PO table is NBA's current standard as encoded in `.claude/skills/accreditation/SKILL.md`; a real Regulatory Diff phase is a documented future step, not run here).
5. "What this proof of concept does not do" → for the MVP, rename this section "What Automation Still Doesn't Cover" and state plainly: no assessor dry-run critique, no attainment numbers (still 100% `[FILL]` — no approved grade ledger exists), no regulatory-drift check.
6. Program coordinator sign-off block.

**Mandatory: compute the PO-coverage table programmatically, never by hand.** The PoC version of this document shipped with two wrong totals (PO2 and PO3), caught only by writing a short Python recount after the fact — a hand-tallied table over more than 2 courses is exactly the kind of arithmetic this skill exists to stop doing by hand. Parse each course's `co-po-attainment.tex` §3 correlation-matrix table (rows = COs, columns = PO1-PO12/PSO1-2, cell = blank or 1/2/3) with a short inline Python snippet (via `Bash`, e.g. `python3 -c "..."` reading the `.tex` table rows with a regex, same shape as the recount used to catch the PoC's own error), and use its printed counts directly in the LaTeX table — do not retype numbers you added up in your head.

## Verify

3-pass XeLaTeX compile every new or regenerated `.tex` file (`TEXINPUTS="../../Preambles;$TEXINPUTS" xelatex -interaction=nonstopmode <file>.tex`, run twice, no bibtex needed — same command shape `/accreditation`'s own output already uses). Report any compile failure; do not consider the run complete until every file compiles clean.

## What This Skill Does NOT Do

- Never invents attainment percentages, PSO values, or a course's CO statements — every unattained numeric slot stays `[FILL]`, and Course Outcomes are copied from each course's syllabus, never guessed.
- Never overwrites an existing `Accreditation/<CODE>/co-po-attainment.tex` a human may already be reviewing.
- Never runs an NBA-assessor dry-run persona or a regulatory-circular diff — both are a later phase of this feature, not this skill.
- Never treats its own output as an authoritative filing — every generated file carries the same faculty/coordinator-review-required notice `/accreditation` already uses.

## Cross-references

- [`.claude/skills/accreditation/SKILL.md`](../accreditation/SKILL.md) — the per-course generator this skill calls for any missing course; the authoritative source for Phases 0-5, not restated here.
- [`.claude/skills/student-simulator/SKILL.md`](../student-simulator/SKILL.md) — the cold-persona blind-review pattern this feature's future Phase 3 (assessor dry-run) will reuse.
- [`.claude/skills/textbook-edition-diff/SKILL.md`](../textbook-edition-diff/SKILL.md) — the diff-against-prior-mapping pattern this feature's future Regulatory Diff phase will reuse.
- `quality_reports/repo_innovator_academic-workload_2026-08-20/REPORT.md` — the originating bet (Signature Feature) and its full 4-phase build strategy.
