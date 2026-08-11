---
paths:
  - "Slides/[COURSE_CODE]/**/*.tex"
  - "Quarto/[COURSE_CODE]/**/*.qmd"
---

# Course Knowledge Base: [COURSE NAME] ([COURSE_CODE])

<!-- Per-course knowledge base. One of these lives at
     .claude/rules/knowledge-base-<CODE>.md per course (e.g.
     knowledge-base-CS401.md, knowledge-base-MATH201.md), scoped to that
     course's files only via the paths: frontmatter above. /create-lecture
     bootstraps a new one from this blank template on a course's first
     lecture — replace [COURSE_CODE] and [COURSE NAME], then fill the
     tables as the course grows. Don't let two courses share one KB file;
     unrelated notation registries collapse into a confusing mixed bag. -->

## Course Profile

<!-- Read by every content-producing skill in Phase 0. `Default difficulty` is
     derived from audience level + programme position per
     .claude/rules/difficulty-levels.md — fill it in rather than making each
     /create-lecture invocation pass --difficulty by hand. -->

| Field | Value |
|---|---|
| Audience level | `undergrad` \| `grad` \| `phd` — one token, plus a qualifier, e.g. `undergrad (B.Tech CSE, semester 3)` |
| Programme position | semester N of M |
| Default difficulty | `intro` \| `core` \| `advanced` — derive from the two rows above via `.claude/rules/difficulty-levels.md` |
| Exam target | e.g. GATE CS, or `none` |
| Implementation language | the language slides and labs use; overrides any anchor book's language |

## Anchor Textbooks

| Book (ShortName) | Index | Weeks/Lectures Backed | Page-Verified? |
|-------------------|-------|------------------------|-----------------|
| | `master_supporting_docs/[COURSE_CODE]/supporting_books/<ShortName>/index.md` | | not until `/index-textbook` runs |

<!-- One row per anchor textbook. "Page-Verified?" starts as "not until
     /index-textbook runs" for every book — flip to "yes (as of YYYY-MM-DD)"
     only after /index-textbook has actually indexed it and /verify-claims
     can check citations against real pages. See textbook-grounding.md. -->

## Notation Registry

| Rule | Convention | Example | Anti-Pattern |
|------|-----------|---------|---------------|
| | | | |

## Symbol Reference

| Symbol | Meaning | Introduced |
|--------|---------|------------|
| | | |

## Lecture Progression

| # | Title | Core Question | Key Notation | Key Method |
|---|-------|--------------|-------------|------------|
| | | | | |

## Empirical Applications

| Application | Paper | Dataset | Lecture(s) | Purpose |
|------------|-------|---------|------------|---------|
| | | | | |

## Design Principles

| Principle | Evidence | Lectures Applied |
|-----------|----------|-----------------|
| | | |

## Anti-Patterns (Don't Do This)

| Anti-Pattern | What Happened | Correction |
|-------------|---------------|-----------|
| | | |

## R Code Pitfalls

| Bug | Impact | Fix |
|-----|--------|-----|
| | | |
