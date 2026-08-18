---
name: textbook-edition-diff
description: When a new edition/printing of an already-indexed textbook is dropped into master_supporting_docs/<CODE>/supporting_books/<Book>/ (replacing the old book.pdf), re-extract its chapter/TOC structure, diff the new numbering against the OLD index.md's recorded chapter mapping, then grep every citation of that book across the whole course to produce one consolidated "citations needing re-verification" report. Use when user says "swap in the new edition", "diff the textbook edition", "did the chapter numbers change", "re-check citations after replacing the PDF", "is this the same edition we indexed", or after dropping a replacement book.pdf into supporting_books/. NOT for indexing a book for the first time (use `/index-textbook` — this skill requires an existing index.md to diff against) and NOT for auto-fixing the stale citations it finds — it reports; a human applies the fix, lecture by lecture, the same way Stallings/Hamacher/Mano edition corrections have always been made in this repo.
argument-hint: "[CourseCode/ShortName], e.g. CS401/Stallings2015 (a NEW book.pdf must already be at master_supporting_docs/CourseCode/supporting_books/ShortName/book.pdf, replacing the old one; an existing index.md for ShortName is required)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Task"]
context: fork
model: sonnet
effort: medium
---

# `/textbook-edition-diff` — Catch a Swapped Edition Before It Corrupts Citations

Closes a real, repeated failure mode in this repo: an instructor drops a *replacement* PDF into `supporting_books/<Book>/` — a newer printing, a different edition entirely — and nothing automatically notices that the old chapter/page citations sprinkled across a dozen lecture files no longer point at the right place. In this exact codebase, that has already happened three separate times (Hamacher, Mano, Stallings), each caught and fixed by hand, lecture-by-lecture, over multiple sessions, because nothing consolidated the check into one pass. This skill is that consolidated pass.

## When to use

- You've just replaced `master_supporting_docs/<CODE>/supporting_books/<ShortName>/book.pdf` with a different edition/printing of the same book, and `index.md` for that book already exists (built by a prior `/index-textbook` run).
- You suspect — from a mismatched chapter title, a table of contents that doesn't line up, or a citation that reads oddly — that the PDF on disk is not the edition the existing citations assume, and want a single pass across the whole course instead of checking lecture-by-lecture.

Not for a book that has never been indexed — run `/index-textbook <CODE>/<ShortName>` first; this skill diffs against an existing `index.md`, it does not create one from nothing.

## Phase 0: Snapshot the old index (MANDATORY, before anything else touches the file)

`/index-textbook`'s own re-indexing behavior is "overwrite `index.md` in place" — so the old chapter mapping must be captured *before* Phase 1 runs, or it's gone.

1. Confirm `master_supporting_docs/<CODE>/supporting_books/<ShortName>/index.md` exists. If it doesn't, stop and tell the user to run `/index-textbook <CODE>/<ShortName>` first — there is nothing to diff against.
2. Copy the current Chapter Index table verbatim to `quality_reports/textbook_diff_<CODE>_<ShortName>_old.md` (gitignored scratch — this is a working file, not a committed artifact).
3. Note the old file's **Indexed** date and **Source** page count from the `index.md` header — these anchor the "before" side of the diff report.

## Phase 1: Re-extract the new edition

Delegate to `/index-textbook <CODE>/<ShortName>` via one `Task` fork (`context: fork`) — do not reimplement chapter/TOC extraction here. That skill's Steps 1-4 (text-layer detection, chapter-range split, per-chapter extraction, `index.md` write) run unchanged against whatever PDF is now at `book.pdf`. Confirm the fork's report before proceeding to Phase 2 — if extraction failed for any chapter, that chapter's citations cannot be diffed and must be flagged as `UNVERIFIABLE`, not silently skipped.

## Phase 2: Diff old → new chapter mapping

Compare the Phase 0 snapshot against the freshly-written `index.md`. **Match by title and key-term similarity, not by chapter position** — a real edition swap can renumber non-contiguously (the Stallings 10th→11th edition case in this exact repo: Ch. 9 → Ch. 11, Ch. 8/6 → Ch. 9/7 — position-matching would have silently mapped the wrong chapters onto each other).

For each old chapter, determine:
- **UNCHANGED** — same chapter number, same title/key-terms, in the new edition.
- **RENUMBERED** — content clearly matches an old chapter by title/key-terms, but the chapter number moved. Record `old_N -> new_M`.
- **RANGE-SHIFT** — chapter number unchanged, but page numbers shifted (common when front matter or a preface grew/shrank). Record the printed-page delta.
- **REMOVED** — no chapter in the new edition matches this old chapter's title/key-terms at all.
- **NEW** — a chapter exists in the new edition with no old-edition counterpart (informational; nothing currently cites it, so no action needed, but worth reporting).

Write `chapter_mapping.yaml` (scratch, gitignored, alongside the Phase 0 snapshot) recording every row. **Explicitly flag any book whose printed-page offset is non-constant across the diff** (the Stallings precedent: the PDF↔printed offset grew through the book, Ch. 4 +37 → Ch. 19 +136) — never assume a fixed offset carries over from the old edition's notes into the new one.

## Phase 3: Grep every citation of this book across the course

Search for the book's bib key / ShortName across:

```
Slides/<CODE>/*.tex
Notes/<CODE>/*-notes.tex
InstructorHandouts/<CODE>/*.tex
CompetitiveExam/<CODE>/*.tex
Assignments/<CODE>/*.tex
syllabi/<CODE>.md
.claude/rules/knowledge-base-<CODE>.md
```

For every match, extract the specific chapter/section/page reference nearby, using these patterns:

```
Ch\.?\s*\d+              # "Ch. 5", "Ch 5"
Chapter \d+
§\s?\d+(\.\d+)?           # "§5.2"
\\S\{?\d+(\.\d+)?         # LaTeX \S command variants
p\.?~?\d+                 # "p. 190", "p.~190"
pp\.?\s*\d+-\d+           # "pp. 187-203"
```

For each citation found, look up its chapter number in the Phase 2 mapping and classify:
- **OK** — cited chapter is UNCHANGED in the new edition.
- **NEEDS UPDATE** — cited chapter was RENUMBERED or RANGE-SHIFTED; report the exact old→new correction.
- **BROKEN** — cited chapter was REMOVED in the new edition; this citation now points at nothing and needs a different source, not just a renumber.
- **AMBIGUOUS** — the citation's chapter number couldn't be confidently matched to a Phase 2 row (e.g. a bare page number with no nearby chapter context); flag for manual check rather than guessing.

## Phase 4: Write the consolidated report

`quality_reports/textbook_edition_diff_<CODE>_<ShortName>.md`:

```markdown
# Textbook Edition Diff: <ShortName> (<CODE>)

**Old index:** [date], [N] pages — snapshot at quality_reports/textbook_diff_<CODE>_<ShortName>_old.md
**New index:** [date], [M] pages
**Chapter mapping:** [K] unchanged, [R] renumbered, [S] range-shifted, [X] removed, [Y] new (see chapter_mapping.yaml)

## Citations needing re-verification

| File | Line | Old citation | Status | Correction |
|------|------|---------------|--------|------------|
| Slides/CS401/09-cache-memory.tex | 412 | "Ch. 4" | NEEDS UPDATE | Ch. 4 -> Ch. 5 (content moved) |
| Notes/CS401/03-ieee754...tex | 88 | "Ch. 9" | OK | unchanged |

## Summary
- [N] citations checked across [M] files
- [R] need a correction, [B] are broken (source removed), [A] ambiguous — manual check required
```

## Automation boundary

**Fully read-only against every citing file.** This skill never edits `Slides/`, `Notes/`, `InstructorHandouts/`, `CompetitiveExam/`, `Assignments/`, or `syllabi/<CODE>.md` — it produces the consolidated report; a human (or a follow-up, explicitly-scoped `/create-lecture`/direct-edit pass) applies each correction. This matches `/audit-reproducibility`'s posture on UNMATCHED claims: a wrong auto-correction on an ambiguous renumbering is worse than a flagged gap.

The one exception: with explicit user confirmation, this skill **may** add an edition-change tracking note to `.claude/rules/knowledge-base-<CODE>.md`'s textbook table — the same hand-written style already used for the Stallings/Hamacher/Mano corrections (e.g. "the PDF supplied [date] is confirmed the Nth edition, not the Mth edition the bib key implies"). This is a metadata/provenance note, not a citation fix, and is proposed as a diff for approval, never auto-applied.

## Report

State: which chapters were UNCHANGED / RENUMBERED / RANGE-SHIFTED / REMOVED / NEW, total citations checked and their status breakdown, the path to the consolidated report, and whether a `knowledge-base-<CODE>.md` tracking-note update was proposed and (if the user approved it) applied.

## Cross-references

- `.claude/skills/index-textbook/SKILL.md` — Phase 1 delegates to this skill's extraction steps unchanged; this skill never reimplements chapter/TOC extraction.
- `.claude/rules/textbook-grounding.md` — the invariant a stale citation violates; this skill exists to catch violations introduced by an edition swap specifically.
- `.claude/rules/pdf-processing.md` — the text-layer/OCR extraction path `/index-textbook` uses underneath Phase 1.
- `.claude/rules/knowledge-base-CS401.md` — the real Stallings/Hamacher/Mano edition-mismatch history this skill is designed against; its textbook table is the optional Phase-4 tracking-note target.
