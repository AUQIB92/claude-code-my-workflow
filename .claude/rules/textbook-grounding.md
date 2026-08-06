---
paths:
  - "Slides/**/*.tex"
  - "Notes/**/*.tex"
  - "master_supporting_docs/**"
---

# Textbook Grounding (page-cited or honestly general)

**A claim attributed to a specific textbook must trace to an indexed page, or be phrased as general/standard treatment — never asserted as book-specific without a page to back it.**

## Why this exists

Citing `\cite{Mano1993_computer_system_architecture}` in a `.tex` file proves the *bibliographic entry* exists in `Bibliography_base.bib`. It proves nothing about whether the slide's content actually matches what that book says on the page implied. Before this rule, lecture content routinely got written from general knowledge of what a standard textbook "probably says," then cited as if it had been read — a real, previously undetected gap (see `[LEARN]` note in `knowledge-base-CS401.md` on Lectures 5-7).

## The rule

For every claim on a slide (or in a Notes file) that names a specific textbook:

1. **If `master_supporting_docs/<CODE>/supporting_books/<ShortName>/index.md` exists and covers the relevant chapter** — cite the specific page (e.g., "Mano, p. 342") and ensure the claim is actually supported by that page's indexed content (definitions/theorems/key-terms). Do not round up from "index has this chapter" to "index verifies this exact sentence" — if in doubt, phrase it as the chapter's general treatment rather than a page-precise quote.
2. **If no index exists for that book yet, or the book isn't in this course's `supporting_books/`** — do NOT invent a page number. Phrase the claim as standard/general treatment: "This is the standard single-bus datapath design (see Hamacher Ch. 7)" rather than "Hamacher shows on p. 218 that...". A chapter-level citation without a page number is honest; a fabricated page number is not.
3. **Never claim a theorem/proposition number, exact quote, or specific page** unless it traces to `index.md`'s chapter/page/key-terms table for that book.

## Verification

`/verify-claims` (via the `claim-verifier` agent) checks textbook-attributed claims the same way it checks paper citations: given a claim naming a book and a page, it looks up that page's entry in the book's `index.md` and confirms the claim is plausible given the indexed content — fresh-context, same Chain-of-Verification discipline as any other citation check.

## Retroactive status

Lectures authored before a course's textbooks were indexed should have their textbook citations marked in `knowledge-base-<CODE>.md`'s Anchor Textbooks table as "standard treatment, not page-verified" rather than silently left looking more authoritative than they are. Re-verify once `/index-textbook` runs for real.

## Cross-references

- `.claude/skills/index-textbook/SKILL.md` — builds the `index.md` this rule checks against.
- `.claude/rules/pdf-processing.md` — textbook extraction mechanics (chapter splitting, OCR fallback).
- `.claude/skills/verify-claims/SKILL.md`, `.claude/agents/claim-verifier.md` — the verification mechanism.
- `.claude/rules/knowledge-base-template.md` — the Anchor Textbooks table convention.
