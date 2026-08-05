---
name: create-lecture
description: Create a new Beamer lecture `.tex` from source papers and materials, with notation consistency checks and the project's preamble wired in. Use when user says "create a lecture on X", "new lecture from these papers", "start a deck on topic Y", "scaffold a new Beamer file", "build me a lecture from these PDFs". Scaffolds the full deck — NOT for compiling existing `.tex` (use `/compile-latex`).
argument-hint: "[CourseCode/Topic name], e.g. CS401/07-microprogrammed-control"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
context: fork
disable-model-invocation: true
---

# Lecture Creation Workflow

Create a beautiful, pedagogically excellent Beamer lecture deck.

**This is a collaborative, iterative process. The instructor drives the vision; Claude is a thinking partner.**

---

## CONSTRAINTS (Non-Negotiable)

1. **Read the knowledge base FIRST** — notation registry, narrative arc, applications database
2. Every new symbol MUST be checked against the notation registry
3. Motivation before formalism — no exceptions
4. Worked example within 2 slides of every definition
5. Max 2 colored boxes per slide
6. No `\pause` or overlay commands (check project rules)
7. Transition slides at major conceptual pivots
8. Thread at least 1 running empirical application throughout
9. All citations verified against the bibliography
10. **Work in batches of 5-10 slides** — share for feedback, don't bulk-dump

---

## WORKFLOW

### Phase 0: Intake & Context (Pre-Flight Report required)

**Resolve the course code first.** `$ARGUMENTS` is `<CODE>/<Topic name>` (e.g. `CS401/07-microprogrammed-control`). If no `<CODE>/` prefix is given and it isn't obvious from context (only one course exists in `Slides/`), ask which course this lecture belongs to before proceeding — every lecture lives under `Slides/<CODE>/`, and guessing wrong means scaffolding in the wrong place.

Once `<CODE>` is known, locate `.claude/rules/knowledge-base-<CODE>.md`. If it doesn't exist, this is that course's first lecture: copy `.claude/rules/knowledge-base-template.md`, replace `[COURSE_CODE]`/`[COURSE NAME]`, and write it to `.claude/rules/knowledge-base-<CODE>.md` before continuing (see "First-lecture fallback" below).

Read the inputs, then produce a Pre-Flight Report in your response before Phase 1 starts.

Inputs to read:
- `.claude/rules/knowledge-base-<CODE>.md` — notation registry, narrative arc, applications for this course
- `.claude/rules/content-invariants.md` — INV-1..INV-8 govern slide content
- Any source papers / existing slides the user provided
- The previous lecture's `.tex` in `Slides/<CODE>/` (last section + ending slide) if one exists

Required Pre-Flight Report block:

```markdown
## Pre-Flight Report

**Sources read:**
- [source 1]: [one-line takeaway — what notation, what result, what diagram]
- [source 2]: ...

**Notation registry check:**
- New symbols this lecture will introduce: [list]
- Symbols reused from prior lectures: [list, with the lecture each was introduced in]
- Conflicts detected: [none / specific clashes]

**Narrative position:** [Where does this lecture sit in the course arc? What did the previous lecture end on? What does the next lecture need you to set up?]

**Pedagogical goal:** [one sentence]

**Running application:** [which real-world example threads through this deck]
```

State the pedagogical goal, get user confirmation, then proceed.

**First-lecture fallback (new course, no knowledge base yet).** If `.claude/rules/knowledge-base-<CODE>.md` was just bootstrapped from the template and still has unfilled placeholder tables (no notation registry entries, no applications, no prior lectures in `Slides/<CODE>/`), do NOT halt waiting for it. Instead:

1. Acknowledge this is the course's first lecture and the KB is empty.
2. Propose a **minimal starter knowledge base** from the user's topic: 5-8 key symbols with conventions, 1-2 running applications, a short narrative arc (intro → main idea → implications). Present for approval.
3. Write the approved stub into `.claude/rules/knowledge-base-<CODE>.md` so subsequent lectures in this course inherit it. Its `paths:` frontmatter should already scope it to `Slides/<CODE>/**/*.tex` and `Quarto/<CODE>/**/*.qmd` from the template — don't widen it to match other courses.
4. Continue to Phase 1.

This prevents `/create-lecture` from deadlocking for every new forker or new course.

### Phase 1: Paper Analysis (When Papers Provided)
- Split into chunks, extract key ideas
- Map paper notation → course notation
- Identify slide-worthy content
- Present summary for approval

### Phase 2: Structure Proposal
- Propose outline (5-Act or 3-Part template)
- List TikZ diagrams and R figures needed
- List new notation to introduce
- **GATE: User approves before Phase 3**

### Phase 3: Draft Slides (Iterative)
- Scaffold the file at `Slides/<CODE>/<Topic name>.tex`, with `\coursecode{<CODE>}` set right after `\input{header}` (see `Preambles/header.tex`) so the course code shows in the footer of every slide
- Work in batches of 5-10 slides
- Check notation, apply creation patterns
- Quality checks during drafting

### Phase 4: Figures & Code
- R scripts following conventions
- TikZ diagrams in Beamer source (single source of truth)
- Save RDS for future Quarto integration

### Phase 5: Polish & Compile
- Full 3-pass compilation
- Run Devil's Advocate
- Run Substance Review (if domain reviewer configured)
- Update knowledge base with new notation

---

## Post-Creation Checklist

```
[ ] Lecture compiles without errors
[ ] No overfull hbox > 10pt
[ ] All citations resolve
[ ] Every definition has motivation + worked example
[ ] Max 2 colored boxes per slide
[ ] 2-3 Socratic questions embedded
[ ] Transition slides between sections
[ ] At least 1 running application threaded throughout
[ ] New notation added to knowledge base
[ ] Session log updated
[ ] Devil's Advocate run
```

## Cross-references

- [`.claude/skills/translate-to-quarto/SKILL.md`](../translate-to-quarto/SKILL.md) — port the finished Beamer deck to a Quarto RevealJS mirror.
- [`.claude/skills/qa-quarto/SKILL.md`](../qa-quarto/SKILL.md) — adversarial Beamer↔Quarto parity (loop-until-dry).
- [`.claude/skills/deploy/SKILL.md`](../deploy/SKILL.md) — render + publish the lecture to GitHub Pages.
- [`.claude/skills/scaffold-exercises/SKILL.md`](../scaffold-exercises/SKILL.md) — problem sets + solutions to accompany the lecture.
