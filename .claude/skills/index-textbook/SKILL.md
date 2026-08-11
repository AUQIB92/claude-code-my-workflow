---
name: index-textbook
description: Build a persistent chapter -> page-range -> key-terms index for an anchor textbook, so future lectures can cite a specific page instead of "standard treatment," and those citations become independently checkable by `/verify-claims`. Use when user says "index this textbook", "add this book as a source", "index Hamacher/Mano/Stallings", "let create-lecture cite pages from this book", or after dropping a textbook PDF into `master_supporting_docs/<CODE>/supporting_books/`. NOT for papers (`/lit-review`, direct Read) — this is for 100+ page course textbooks specifically.
argument-hint: "[CourseCode/ShortName], e.g. CS401/Mano1993 (book.pdf must already exist at master_supporting_docs/CourseCode/supporting_books/ShortName/book.pdf)"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
model: haiku
effort: medium
---

# Index a Textbook for Page-Cited Lecture Content

Turn a dropped-in textbook PDF into a persistent, page-cited index so `/create-lecture` and `/lecture-notes` can attribute claims to a specific page instead of memory, and `/verify-claims` can independently check those claims later.

## When to use

- A course's anchor textbook (e.g. Hamacher, Mano, Stallings) exists as a PDF but every lecture so far has cited it only by chapter number, from general knowledge — not from the actual page.
- You want future `/create-lecture` runs for this course to pull page-cited definitions/theorems instead of "standard treatment" phrasing.

Not for a single paper — use `/lit-review` or a direct `Read` with a `pages` range (`.claude/rules/pdf-processing.md`) for anything under ~100 pages.

## Steps

### Step 0: Locate the book

`$ARGUMENTS` is `<CODE>/<ShortName>` (e.g. `CS401/Mano1993`). The file must already exist at:

```
master_supporting_docs/<CODE>/supporting_books/<ShortName>/book.pdf
```

If it doesn't exist, stop and ask the user to drop the PDF there first — this skill never fetches a textbook itself (copyright; the file must come from the user).

### Step 0.5: Cross-check syllabus coverage (MANDATORY)

Before indexing, read `syllabi/<CODE>.md` and find the row(s) — usually one week, but check the "Weeks/Lectures Backed" a course's knowledge base already assigns to this book — that this book is supposed to back. Extract the syllabus's own topic phrase verbatim (e.g. "interrupts, polling, DMA, IOP").

After Steps 1-4 produce the chapter/section breakdown, **explicitly check each syllabus topic word/phrase against what was actually found in the book** — don't just index the assumed chapter and call it done. Concretely:

- If the syllabus names a specific technique/term (e.g. "DMA", "IOP", "cache", "paging"), search for that term's actual presence in the extracted chapter content, not just the chapter title. Chapter titles are frequently wrong or ambiguous (see the Hamacher2002/CS401 case below); the syllabus's specific nouns are the ground truth to check against, and a title match is not the same as a content match.
- If a named topic is **not found anywhere in the indexed pages**, do not silently omit it. Record it in `index.md` as an explicit gap (e.g. "this edition never uses the term 'DMA'/'IOP' — see §7.3 Arbitration for the closest functional analogue") so `/create-lecture` knows to phrase that specific topic as general/standard treatment (citing a different book) rather than assuming the whole syllabus line is covered because *some* of it page-cited cleanly.
- If the assumed chapter (from the syllabus's existing citation, e.g. "Ch. 4") turns out not to contain the syllabus's topics at all, search the table of contents for the chapter(s) that actually do, and index those instead — don't index the wrong chapter just because it was named in an unverified citation. Correct the syllabus's citation once you've verified the right chapter (small, directly-scoped fix — same discipline as any other textbook-grounding correction).

**Concrete precedent:** CS401 Week 8's syllabus row said "interrupts, polling, DMA, IOP" and cited "Hamacher Ch. 4." Indexing found Ch. 4 doesn't exist as I/O content in the edition on disk, the real I/O chapters were Ch. 3 + Ch. 7, and — critically — that even the *correct* chapters never use the terms "DMA" or "IOP" anywhere in the table of contents or body. A title/chapter-number check alone would have missed this; only checking each syllabus noun against actual content surfaced it.

### Step 1: Detect text-layer vs. scanned

```bash
pdfinfo "master_supporting_docs/<CODE>/supporting_books/<ShortName>/book.pdf" | grep "Pages:"
pdftotext -f 1 -l 3 "master_supporting_docs/.../book.pdf" - | wc -c
```

If the first few pages extract to near-zero text, treat it as a scanned book with no text layer and fall back to OCR (Tesseract) per `.claude/rules/pdf-processing.md`'s textbook OCR path. If text extracts cleanly, proceed directly.

### Step 2: Chapter-range split

Per `.claude/rules/pdf-processing.md`, a textbook-sized PDF (100+ pages) goes straight to Ghostscript page-range splitting — do not attempt a direct whole-book `Read` first. Identify chapter boundaries from the table of contents (first ~15-20 pages) before splitting, so ranges align with real chapters rather than arbitrary page blocks.

### Step 3: Extract per-chapter content

For each chapter range, extract text (or OCR text) and identify:
- **Key terms/definitions** introduced in that chapter (the vocabulary a lecture would need to cite precisely).
- **Named theorems/algorithms/figures** with their page number.
- A one-line chapter summary.

Do NOT write the extracted full text to a committed file — only the structured index below. Raw extracted text (if kept as an intermediate working file) must land somewhere covered by `.gitignore`'s `supporting_books/**/extracted/` rule, and should be deleted once the index is written unless the user asks to keep it for repeated indexing runs.

### Step 4: Write `index.md`

```
master_supporting_docs/<CODE>/supporting_books/<ShortName>/index.md
```

Format:

```markdown
# Index: [Book Title] ([ShortName])

**Source:** master_supporting_docs/<CODE>/supporting_books/<ShortName>/book.pdf ([N] pages)
**Indexed:** [YYYY-MM-DD]
**Extraction method:** [text-layer / OCR via Tesseract]

## Chapter Index

| Chapter | Pages | Summary | Key Terms/Definitions | Named Theorems/Algorithms/Figures |
|---------|-------|---------|------------------------|-------------------------------------|
| 7 | 320-360 | Addressing modes and CPU/bus organization | effective address, single-bus datapath, RTL notation | Fig 7.13 (three-bus organization) |
```

One row per chapter (or logical sub-unit for long chapters). Page numbers are the book's own printed page numbers, not PDF page indices — note any offset between the two if they differ.

### Step 5: Report

State: book indexed, chapter count, any chapters that failed extraction (flag, don't silently skip), whether OCR was needed, and the **syllabus-coverage check result** from Step 0.5 — which syllabus topics were confirmed present, and which (if any) were not found in the book at all and must stay general-treatment.

## Important

- **Never commit the PDF or raw full-text extraction** — both are gitignored (see `.gitignore`'s textbook rules). Only `index.md` is committed.
- **Independent per-course index.** If the same book edition is used by two courses, each course gets its own `master_supporting_docs/<CODE>/supporting_books/<ShortName>/` — no cross-course sharing (matches this repo's per-course isolation elsewhere: `Slides/<CODE>/`, `knowledge-base-<CODE>.md`).
- **Re-indexing** (new edition, corrected OCR): overwrite `index.md` in place; note the change in the report, don't silently diverge from what lectures already cite.

## Cross-references

- `.claude/rules/pdf-processing.md` — the textbook-sized-PDF splitting path and OCR fallback this skill uses.
- `.claude/rules/textbook-grounding.md` — the invariant this index exists to satisfy: a textbook-attributed claim must trace to an indexed page.
- `syllabi/<CODE>.md` — the syllabus-coverage ground truth Step 0.5 checks indexed content against.
- `.claude/skills/create-lecture/SKILL.md` — Phase 0 reads `supporting_books/*/index.md` for this course.
- `.claude/skills/verify-claims/SKILL.md` and `.claude/agents/claim-verifier.md` — check a slide's page-cited claim against this index's chapter/page mapping.
