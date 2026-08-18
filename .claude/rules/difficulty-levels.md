---
paths:
  - "Slides/**/*.tex"
  - "Notes/**/*.tex"
  - "Assignments/**/*.tex"
  - "InstructorHandouts/**/*.tex"
  - "CompetitiveExam/**/*.tex"
  - "Minors/**/*.tex"
---

# Difficulty Levels (derived from audience level + semester)

**Two separate axes govern how demanding a piece of course material is. Never collapse them into one flag.**

| Axis | Flag | Scope | What it sets |
|------|------|-------|--------------|
| **Audience level** | `--level undergrad\|grad\|phd` | the whole course, set once by `/syllabus` | the *baseline* — what counts as assumed knowledge, whether proofs appear at all, assessment type |
| **Difficulty** | `--difficulty intro\|core\|advanced` | one artifact, overridable per run | how demanding the treatment is *relative to that baseline* |

An `advanced` undergraduate deck is not a `core` PhD deck. Level fixes the floor; difficulty moves within it.

## Resolving the default

**Do not ask the user for a difficulty when it can be derived.** Resolution order:

1. An explicit `--difficulty` on the invocation — always wins.
2. The `Default difficulty` row of the course's **Course Profile** block in `.claude/rules/knowledge-base-<CODE>.md`.
3. Derived from **audience level + semester** using the table below.
4. `core`, if nothing else is known.

### Level + semester → default difficulty

Semester position within the programme is the signal; the level sets what the tier *means*.

| Audience level | Programme position | Default |
|---|---|---|
| `undergrad` (B.Tech / B.E., 8 semesters) | semesters 1–2 | `intro` |
| | **semesters 3–6** | **`core`** |
| | semesters 7–8 | `advanced` |
| `grad` (M.Tech / MS / MCA) | semester 1 | `core` |
| | semesters 2+ | `advanced` |
| `phd` | coursework year 1 | `core` |
| | beyond coursework | `advanced` |

Rationale: a semester-1 student is still acquiring the vocabulary; a semester-7 student is choosing between techniques. The same three words therefore denote a *harder* treatment at each higher level — `advanced` undergrad means full derivations and edge cases, `advanced` PhD means open problems and proof technique.

**Worked example.** CS301 (Data Structures) is B.Tech CSE, semester 3 → `undergrad` + sem 3 → **`core`**. No flag needed on any `/create-lecture CS301/...` invocation; passing `--difficulty advanced` on one deck overrides it for that deck only.

## What each tier changes, per artifact

| Artifact | `intro` | `core` | `advanced` |
|---|---|---|---|
| **Slides** (`/create-lecture`) | Motivation-heavy; worked example within 1 slide of every definition; results stated with intuition, proofs omitted; one new symbol at a time; more diagrams, shorter bullets | Main results derived, secondary ones sketched; one worked example per definition; INV-8 motivation-before-formalism as usual | Full derivations; edge cases and failure modes; comparative treatment ("why not the other structure"); forward references to later weeks |
| **Notes** (`/lecture-notes`) | **Inherited from the deck — never set independently.** See below. | | |
| **Assignments** (`/create-assignment`, `/scaffold-exercises`) | Recall/apply-weighted; single-concept problems; multi-part steps scaffolded | Balanced conceptual / numerical / design mix | Analysis/design-weighted; multi-concept synthesis; unscaffolded |
| **Instructor handout** (`/instructor-handout`) | Longer "before you teach" reading list; more misconception coverage | Standard | Assumes fluency; depth only on the subtle cases |
| **Exam questions** (`/competitive-exam-questions`) | Calibrated to the **target exam's own** difficulty tags, not this scale | | |

## Notes inherit; they never exceed

`Notes/` is a **derived artifact** (`.claude/rules/single-source-of-truth.md`), and `/qa-notes` enforces a no-invention gate against the Beamer source. Raising a Notes file above its deck's difficulty would require content the deck does not contain — which that gate correctly rejects as a critical finding.

So `/lecture-notes` takes **no `--difficulty` flag**. It inherits the deck's tier and expands within it. To make the Notes harder, make the *deck* harder and regenerate.

## Difficulty is not quality

An `intro` deck and an `advanced` deck both ship at ≥80 on `scripts/quality_score.py`. Difficulty never relaxes a quality gate, a content invariant (INV-1..INV-12), or the textbook-grounding rule.

## Cross-references

- `.claude/rules/knowledge-base-template.md` — the Course Profile block this rule reads.
- `.claude/rules/single-source-of-truth.md` — why Notes inherit rather than set.
- `.claude/rules/content-invariants.md` — INV-7/INV-8 hold at every tier.
- `.claude/skills/syllabus/SKILL.md` — owns `--level`, the other axis.
