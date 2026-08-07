# Notes vs Beamer Parity Audit: CS401/07-microprogrammed-control

**Beamer source:** `Slides/CS401/07-microprogrammed-control.tex`
**Notes:** `Notes/CS401/07-microprogrammed-control-notes.tex`
**Round:** 2  **Date:** 2026-08-07

## Verdict: APPROVED

## Round 1 Fix Verification

### M1 (numeric inaccuracy — "two active" vs. three signals): RESOLVED
Current Notes text (line 221):
> "Horizontally, each of the eight signals gets its own bit; the three active this row ($R3_{\text{out}}$, ALU$=$add, and $Z_{\text{in}}$) are set to 1, the rest to 0..."
Confirmed fixed — content and figure are consistent.

### m1 (presentation-pacing subsection headings): RESOLVED
No "Missing Piece," "Socratic Check," or "Bridge to Week N" style headings remain anywhere in the Notes' section structure. Confirmed fixed.

### m2 (duplicate citation): left as-is, per round 1's own "optional" recommendation. Not re-flagged as a defect.

## Hard Gate Status

| Gate | Status |
|------|--------|
| Content parity | Pass — all 24 content frames traced to a matching Notes section/subsection/example/figure |
| No invention | Pass |
| Citation parity | Pass — Beamer keys `{Stallings2015_computer_organization, Mano1993_computer_system_architecture, Hamacher2002_computer_organization}` all present in Notes, same keys, no extras |
| Notation fidelity | Pass |
| Textbook-page honesty | Pass — all page citations trace exactly to `master_supporting_docs/CS401/supporting_books/Mano1993/index.md` |

## Critical / Major Issues

None.

## Minor Issues (NICE TO FIX, not blocking)

### m3 (new, very minor): Aggregated page range in capstone figure caption
- **Location:** Notes, Figure 7.3 caption (`fig:full`): "Sec.~7-2/7-4, Address Sequencing / Design of Control Unit, p.215--239"
- **Issue:** Spans Sec. 7-2 (p.215–224) through Sec. 7-4 (p.230–239) as one continuous range, which also subsumes Sec. 7-3 (p.219–229) not actually cited by this figure. Both endpoints are real, index.md-verified section boundaries — not a fabricated page number, just a cosmetic ambiguity.
- **Fix (optional):** Could be tightened to "Sec.~7-2, p.215--224 and Sec.~7-4, p.230--239."

## Summary Statistics

| Metric | Value |
|--------|-------|
| Critical / Major / Minor (this round, new) | 0 / 0 / 1 |
| Round 1 issues resolved | M1 resolved, m1 resolved; m2 intentionally deferred (not a defect) |

**Verdict rationale:** Zero critical, zero major, one trivial new minor → **APPROVED**.
