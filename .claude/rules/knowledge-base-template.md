---
name: knowledge-base-[COURSE_CODE]
description: Course-scoped knowledge base for [COURSE NAME] ([COURSE_CODE]) — notation, textbook grounding, lecture history, misconceptions, and hard-won corrections. Loaded automatically when editing this course's slides, notes, or assessments.
course_code: "[COURSE_CODE]"
course_name: "[COURSE NAME]"
term: "[e.g. Autumn 2026]"
level: "[UG-3 / PG-1 / ...]"
status: bootstrapping            # bootstrapping | active | frozen | archived
schema_version: 2
kb_version: 0.1.0                # bump minor on new lecture, patch on corrections
last_updated: YYYY-MM-DD
lectures_recorded: 0
paths:
  - "Slides/[COURSE_CODE]/**/*.tex"
  - "Slides/[COURSE_CODE]/**/*.md"
  - "Quarto/[COURSE_CODE]/**/*.qmd"
  - "Notes/[COURSE_CODE]/**"
  - "Assessments/[COURSE_CODE]/**"
  - "master_supporting_docs/[COURSE_CODE]/**"
---

# Course Knowledge Base: [COURSE NAME] ([COURSE_CODE])

<!-- ONE FILE PER COURSE. Lives at .claude/rules/knowledge-base-<CODE>.md and is
     scoped to that course only via `paths:`. Never let two courses share a KB —
     merged notation registries produce silent, confusing collisions.
     /create-lecture bootstraps this from the blank template on a course's first
     lecture: replace [COURSE_CODE] / [COURSE NAME], set `term`, then let the
     tables grow lecture by lecture. -->

---

## 0. Operating Contract (read this first, every session)

**Precedence.** This file > general teaching-skill defaults > model priors. If a
lecture request conflicts with a rule here, follow the rule and say so in one line.

**Before writing any lecture content:**
1. Read §2 (notation) + §3 (symbols) + §4 (terminology) and obey them verbatim.
2. Read §5 (lecture progression) — reuse prior notation, examples, and figures
   instead of inventing parallel ones; never re-derive something already built.
3. Read §7 (misconceptions) and §9 (anti-patterns) before drafting explanations.
4. Cite textbooks only per §1's verification protocol.

**After a lecture is finalized (same session, not "later"):**
- Append one row to §5; add any new symbol to §3, new rule to §2.
- Add any misconception surfaced in class to §7; any mistake made while drafting
  to §9 — the correction, not the apology.
- Update frontmatter `last_updated`, `lectures_recorded`, `kb_version`.

**Write rules.**
- Every row carries a stable ID (`NOT-03`, `LEC-07`, `MIS-02`…). IDs are never
  reused or renumbered — retire with `[superseded by NOT-11]`, don't delete.
- One fact per row. Convention/Correction cells ≤ 20 words. If it needs a
  paragraph, it belongs in a linked doc, not here.
- Never invent a page number, edition, dataset, DOI, or CO mapping. Unknown → `TBD`.
- Only record what actually happened or was actually decided. No aspirations.

**Curation caps** (keep this file loadable; consolidate when exceeded):
notation ≤ 25 · symbols ≤ 40 · misconceptions ≤ 30 · anti-patterns ≤ 20 ·
design principles ≤ 12. Delete any section this course will never use.

---

## 1. Anchor Textbooks & Citation Protocol

| ID | Book (ShortName) | Ed. | Index path | Lectures backed | Verification |
|----|------------------|-----|-----------|-----------------|--------------|
| BK-01 | | | `master_supporting_docs/[COURSE_CODE]/supporting_books/<ShortName>/index.md` | | `unindexed` |

<!-- Verification state machine — a claim's citation is only as good as this:
     unindexed          → /index-textbook has never run. NO page numbers may be
                          cited from this book. Cite chapter/section names only.
     indexed YYYY-MM-DD → /index-textbook completed; page cites now permitted.
     verified YYYY-MM-DD→ /verify-claims has checked this course's citations
                          against real pages.
     stale              → book re-indexed or edition changed after last verify;
                          re-run /verify-claims before trusting page numbers.
     See textbook-grounding.md. Rule: a page number that has never passed
     through /index-textbook is a hallucination risk, not a citation. -->

**Citation format in slides/notes:** `[ShortName, §4.2, pp. 118–121]`.
**Divergences from the book** (where this course deliberately differs — different
proof, different notation, different ordering) go in §2 or §9, flagged so students
aren't confused when they read the text.

| ID | Book | Where the course diverges | Why | Told to students in |
|----|------|---------------------------|-----|---------------------|
| DIV-01 | | | | LEC-?? |

---

## 2. Notation Registry

| ID | Rule | Convention | Example | Anti-pattern | Since | Status |
|----|------|-----------|---------|--------------|-------|--------|
| NOT-01 | | | | | LEC-01 | active |

<!-- "Rule" = the thing being decided (e.g. "vectors", "index variables",
     "cycle counts"). "Status" ∈ active | superseded by NOT-xx | book-divergent.
     Changing an active rule mid-course is expensive: if you must, mark the old
     row superseded, add the new row, and list every lecture needing a fix in
     §12. Never silently switch. -->

---

## 3. Symbol Reference

| Symbol | Meaning | Type/Units | Introduced | Collides with |
|--------|---------|-----------|------------|---------------|
| | | | LEC-?? | |

<!-- "Collides with" is the point of this table: flag symbols reused with a
     different meaning in another subfield/lecture (e.g. T for period vs
     throughput vs transpose) so a disambiguating word is added at reuse. -->

---

## 4. Terminology & Style Decisions

| ID | Decision | Use | Avoid | Reason |
|----|----------|-----|-------|--------|
| TRM-01 | | | | |

<!-- Vocabulary the course commits to (node vs vertex, memory word vs location,
     "control step" vs "clock cycle"), spelling variant, capitalization of
     algorithm names, and language-of-instruction choices. Small, but it is what
     makes fourteen weeks of material read as one voice. -->

---

## 5. Lecture Progression

| ID | Wk | Title | Core question | Assumes | Introduces | Key notation | Key method | COs | Artifacts |
|----|----|-------|---------------|---------|------------|--------------|-----------|-----|-----------|
| LEC-01 | 1 | | | — | | | | CO1 | |

<!-- "Assumes" = prior LEC-ids or named prerequisites; this column is the
     dependency graph and the single best defence against a lecture that quietly
     uses something never taught. "Artifacts" = slide file, figure ids, notebook,
     handout. One row per delivered lecture, in delivery order. -->

---

## 6. Course Outcomes & Assessment Blueprint

| CO | Statement | Bloom level | Lectures | Assessed in |
|----|-----------|------------|----------|-------------|
| CO1 | | | | |

<!-- OBE/NBA-facing. Fill CO statements once from the approved syllabus; do not
     paraphrase them freely afterwards. Keep Bloom levels consistent with the
     verbs actually used in exam items. -->

| Unit / Module | Weightage | Lectures | Bloom spread (Re/Un/Ap/An/Ev/Cr) | Item bank |
|---------------|-----------|----------|----------------------------------|-----------|
| | | | | |

---

## 7. Misconception Registry

| ID | Misconception students hold | Why it's wrong | Diagnostic / ConcepTest | Surfaced in |
|----|-----------------------------|----------------|-------------------------|-------------|
| MIS-01 | | | | LEC-?? |

<!-- The highest-value table here. Record what students ACTUALLY got wrong — in
     class, in quizzes, in doubts — not what a textbook predicts they might.
     Each row should eventually earn a diagnostic question that catches it early.
     Reuse these when writing assessments: good distractors come from this table. -->

---

## 8. Running Examples, Applications & Datasets

| ID | Example / application | Source (paper, spec, dataset) | Lectures | Purpose | Reuse note |
|----|----------------------|-------------------------------|----------|---------|-----------|
| EX-01 | | | | | |

<!-- Prefer a small number of spine examples carried across many lectures over a
     fresh example every week — continuity is worth more than novelty. "Reuse
     note" records the state the example is left in, so the next lecture picks it
     up rather than restarting it. Datasets: record size, license, and where the
     file lives. -->

---

## 9. Anti-Patterns (Don't Do This)

| ID | Anti-pattern | What happened | Correction | Recurred? |
|----|-------------|---------------|-----------|-----------|
| AP-01 | | | | |

<!-- Course-specific failures only — pedagogical (a derivation that lost the room),
     structural (too many slides for 50 minutes), or authoring (a figure that
     didn't compile in the projector's resolution). Tick "Recurred?" when the same
     mistake reappears; two ticks means the correction is too vague — rewrite it. -->

---

## 10. Design Principles

| ID | Principle | Evidence / where it came from | Lectures applied | Confidence |
|----|-----------|-------------------------------|------------------|-----------|
| DP-01 | | | | tentative |

<!-- Confidence ∈ tentative | working | settled. Promote only after it has held up
     across several lectures; demote rather than delete when it stops working. -->

---

## 11. Toolchain & Code Pitfalls

| ID | Tool | Bug / trap | Impact | Fix |
|----|------|-----------|--------|-----|
| TC-01 | | | | |

<!-- Tool ∈ LaTeX/Beamer · TikZ · Quarto · Marp · R · Python · Manim · ffmpeg ·
     build script. Only real, encountered breakages with a verified fix — a
     compile error you've hit twice, a package clash, a font that fails on the
     lecture-hall machine, a seed that changes plot output. Delete rows that a
     toolchain upgrade has made obsolete. -->

---

## 12. Open Items & Change Log

| Date | KB ver. | Change | Follow-up needed |
|------|---------|--------|------------------|
| YYYY-MM-DD | 0.1.0 | KB bootstrapped | Fill §1, §6 from syllabus |

<!-- One line per meaningful change: notation switches, superseded rules,
     re-indexed books, lectures needing retrofit. This is where "we already
     decided this in week 3" gets settled without re-arguing it. -->