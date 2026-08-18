---
name: accreditation
description: Generate NBA-style Course Outcome (CO) to Program Outcome (PO) mapping and an attainment-calculation template for a course — numbers the syllabus's existing learning objectives as COs, Bloom-tags them, drafts a CO-PO-PSO correlation matrix against NBA's fixed 12 POs, maps each CO to the assessment tool that tests it, and emits the standard attainment formulas, substituting real per-CO percentages wherever `/grade --tally` has already produced `Accreditation/<CODE>/attainment-data.yaml` and leaving `[FILL]` elsewhere. Use when user says "run accreditation", "CO-PO mapping", "NBA attainment", "generate the course file", "map outcomes to POs", or when preparing an NBA/AICTE self-assessment report. NOT for grading student submissions or producing attainment data itself (use `/grade`, whose `--tally` output this skill reads) and NOT an authoritative filing on its own — the CO-PO correlation matrix is a faculty-review draft, never a final submission without instructor sign-off.
argument-hint: "[CourseCode]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob"]
effort: high
---

# Accreditation — CO-PO Mapping & Attainment

Turn a course's already-written learning objectives into the CO-PO-PSO mapping and attainment-calculation scaffold that NBA/AICTE-accredited institutes must file every semester — currently done entirely by hand. `/syllabus` already emits Bloom's-verb-style measurable objectives; this skill numbers them as Course Outcomes, drafts their correlation against NBA's 12 fixed Program Outcomes, and produces the standard attainment formulas ready for real assessment data once it exists.

**Posture:** the CO-PO correlation matrix this skill drafts is a **starting point for faculty review, never an authoritative filing**. Assigning a correlation strength (1/2/3) between a course outcome and a program outcome is a professional judgment call NBA auditors expect the instructor to own — the skill proposes a defensible first draft, not a final answer. Numeric attainment is never fabricated: every attainment cell is `[FILL]` until real assessment scores exist, the same discipline `/replication-package` already uses for missing data.

## When to use

- Preparing a semester's NBA/AICTE self-assessment / course file.
- After `/syllabus` has produced (or updated) a course's learning objectives and you need them formalized as numbered, Bloom-tagged Course Outcomes.
- Setting up the CO-PO-PSO matrix scaffold for a new course before the semester starts, so the attainment-calculation slots are ready once assessments are graded.

Not for: computing real attainment percentages (needs actual student scores — no data source exists in this repo yet); writing the syllabus itself (`/syllabus`); grading individual student submissions (no `/grade` skill exists yet).

## Inputs

- `$0` — the course code (e.g. `CS401`). Required.

| File | Role |
| --- | --- |
| `syllabi/<CODE>.md` | Source of Course Outcomes — its `## Learning objectives` bullets, already Bloom's-verb-phrased, and its `## Assessment` table. |
| `.claude/rules/knowledge-base-<CODE>.md` | Destination for the instantiated "Course Outcomes & Assessment Blueprint" section (template stub already exists at `.claude/rules/knowledge-base-template.md` §6). |

## Phases

### Phase 0: Pre-Flight

Confirm `syllabi/<CODE>.md` exists with a populated `## Learning objectives` section and `.claude/rules/knowledge-base-<CODE>.md` exists. Halt if either is missing — run `/syllabus` first (same gating shape `/syllabus` itself uses for its own inputs). Produce a short Pre-Flight block:

```markdown
## Pre-Flight Report
**Course:** <CODE> — <course title from syllabus>
**Learning objectives found:** N (source: syllabi/<CODE>.md)
**Knowledge base:** .claude/rules/knowledge-base-<CODE>.md exists — Course Outcomes section: [not yet instantiated / already present, will be updated]
**Assessment table found:** [Class Tests / Assignments / lab component names, from the syllabus's own Assessment section]
```

### Phase 1: CO extraction + Bloom-tagging

1. Number the syllabus's existing objective bullets **CO1..CON**, in the order they appear (which is delivery order, since `/syllabus` already ties each objective to its week range).
2. Infer each CO's Bloom's-taxonomy level (Remember / Understand / Apply / Analyze / Evaluate / Create) from its stated observable verb, using the verb the objective already uses (e.g. "compute", "represent" → Apply; "contrast", "justify a design choice" → Analyze/Evaluate; "design and contrast... units" → Evaluate/Create). If a verb doesn't map cleanly to one Bloom level, flag it for the user rather than silently picking one.
3. Write the result into `knowledge-base-<CODE>.md`'s **Course Outcomes & Assessment Blueprint** section (the stub already exists at `knowledge-base-template.md` §6 — `CO | Statement | Bloom level | Lectures | Assessed in` — this is the first time it gets instantiated for a real course). `Lectures` comes directly from the objective's already-stated week range; `Assessed in` is filled in Phase 3, not invented here.

### Phase 2: CO-PO-PSO correlation matrix (DRAFT)

NBA mandates exactly these 12 Program Outcomes for every accredited UG engineering program (not institute-configurable):

| PO | Graduate Attribute |
| --- | --- |
| PO1 | Engineering knowledge |
| PO2 | Problem analysis |
| PO3 | Design/development of solutions |
| PO4 | Conduct investigations of complex problems |
| PO5 | Modern tool usage |
| PO6 | The engineer and society |
| PO7 | Environment and sustainability |
| PO8 | Ethics |
| PO9 | Individual and team work |
| PO10 | Communication |
| PO11 | Project management and finance |
| PO12 | Life-long learning |

For each CO, draft a correlation level against every PO: **1** (slight), **2** (moderate), **3** (substantial), or blank (no correlation). Base the draft on what the CO's statement and its underlying activity actually require — e.g. a CO about deriving a hardware trade-off quantitatively correlates strongly with PO1/PO2, weakly if at all with PO6/PO7/PO8 unless the course explicitly engages those. Do not force every CO to touch every PO; blank cells are the expected, honest default for most pairs.

**PSOs** (Program-Specific Outcomes) are department-defined and not standardized anywhere in this repository yet — leave the PSO columns as `[FILL]` rather than inventing department-specific outcomes.

Mark the entire matrix, visibly in the emitted document, as: *"Draft correlation matrix — requires instructor review and sign-off before submission. Correlation strengths reflect the CO's stated content, not verified pedagogical practice."*

### Phase 3: Assessment-tool-to-CO mapping

Cross-reference each CO against the syllabus's own `## Assessment` table (Class Tests, Assignments, end-semester exam, lab component) — which tool(s) actually test that CO, based on the week(s) and topic(s) the CO covers. No new assessment data is invented; this only cross-references what the syllabus already states. Feed the result back into Phase 1's `Assessed in` column.

### Phase 4: Attainment methodology (formulas, not fabricated numbers)

Emit the standard NBA attainment-calculation methodology, with every numeric slot as `[FILL]`:

- **Direct attainment** (per CO): percentage of students scoring at or above a target threshold (typically 60%) in the assessment(s) mapped to that CO in Phase 3. Attainment level: Level 3 if `[FILL]`% of students ≥ target, Level 2 if `[FILL]`%, Level 1 if `[FILL]`% (institute-specific cutoffs — leave as `[FILL]` unless the syllabus/KB already states them).
- **Indirect attainment** (per CO): from a course-exit survey (student self-assessment), typically normalized to the same 1-3 scale. `[FILL]` — no survey data exists in this repo.
- **Overall CO attainment**: a weighted blend, typically `0.8 × direct + 0.2 × indirect` (weights are institute policy — state them as `[FILL]` if not already fixed elsewhere).
- **PO attainment**: for each PO, the weighted average of the overall CO attainments mapped to it, using the Phase 2 correlation levels as weights.

Include a short "how to fill this in" note: once real assessment scores exist (per-student, per-question, mapped to the CO each question tests), the direct-attainment percentages can be computed and substituted for the `[FILL]` cells. Before emitting `[FILL]`, check whether `Accreditation/<CODE>/attainment-data.yaml` already exists — that file is `/grade --tally`'s output (built only from instructor-approved scores, per `.claude/rules/grading-protocol.md`), and if present, its per-CO direct-attainment percentages replace the corresponding `[FILL]` cells directly. This still carries the same "faculty-review draft, needs sign-off" framing verbatim — a real number from `/grade --tally` is not itself an authoritative filing any more than a `[FILL]` placeholder was.

### Phase 5: Emit deliverable

Write `Accreditation/<CODE>/co-po-attainment.tex` — XeLaTeX article class, `\input{../../Preambles/header}`, `\coursecode{<CODE>}`, same compilation convention as `Labs/`/`Assignments/`. Sections: CO table (Phase 1), CO-PO-PSO matrix (Phase 2, with its review-required notice prominently placed, not buried), assessment-tool mapping (Phase 3), attainment methodology + formulas + `[FILL]` cells (Phase 4), and a one-paragraph faculty sign-off block (name/date line, explicitly for the instructor to complete before this becomes a real filing).

## Output / Report

After writing the deliverable, surface this in the final chat message:

```
## Accreditation summary — <CODE>
COs extracted: N (CO1..CON), all Bloom-tagged
CO-PO-PSO matrix: drafted, DRAFT status — needs faculty review before filing
Assessment mapping: N/N COs mapped to an existing assessment tool
Attainment: methodology + formulas emitted; all numeric cells [FILL] (no score data available)
Deliverable: Accreditation/<CODE>/co-po-attainment.tex (compiled, N pages)
```

## Exit behavior

- A CO with no assessment-tool mapping in Phase 3 is flagged explicitly in the output, not silently left blank — a CO the syllabus never actually assesses is a real gap worth surfacing, not hiding.
- The CO-PO-PSO matrix is never presented as final; every emission carries the review-required notice from Phase 2.
- No attainment number is ever computed or estimated from anything other than real supplied score data — there is currently no such data source, so every attainment cell stays `[FILL]`.
- If a Bloom-level inference is ambiguous for a given CO's verb, it is flagged for the user rather than silently resolved.

## Cross-references

- [`.claude/skills/syllabus/SKILL.md`](../syllabus/SKILL.md) — produces the learning objectives this skill numbers as COs; run first if `syllabi/<CODE>.md` doesn't exist yet.
- [`.claude/rules/knowledge-base-template.md`](../../rules/knowledge-base-template.md) — §6 "Course Outcomes & Assessment Blueprint" is the stub this skill instantiates.
- [`.claude/skills/respond-to-eval/SKILL.md`](../respond-to-eval/SKILL.md) — a structurally similar report-generating skill (cluster → classify → map → draft) this skill's phase shape follows.
- [`.claude/skills/replication-package/SKILL.md`](../replication-package/SKILL.md) — the `[FILL]`-for-missing-data convention this skill reuses for attainment numbers.
- [`.claude/rules/model-routing.md`](../../rules/model-routing.md) — Bloom-tagging and PO-correlation assignment are judgment calls, not mechanical work; this skill stays off the Haiku tier.

## What this skill does NOT do

- It does **not** compute real attainment percentages itself — it reads `/grade --tally`'s output when present; without it, cells stay `[FILL]`.
- It does **not** present the CO-PO-PSO matrix as an authoritative, submission-ready filing — every emission is marked as a faculty-review draft.
- It does **not** invent Program-Specific Outcomes (PSOs) — those are department-defined and left as `[FILL]`.
- It does **not** grade student submissions or generate assessment items — that is `/grade`'s job, a distinct skill this one only consumes the tally output of.
