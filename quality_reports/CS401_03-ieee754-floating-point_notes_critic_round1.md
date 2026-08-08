# Notes vs Beamer Parity Audit: CS401/03-ieee754-floating-point

**Beamer source:** `Slides/CS401/03-ieee754-floating-point.tex` (23 content frames + title frame + 5 transition slides)
**Notes:** `Notes/CS401/03-ieee754-floating-point-notes.tex`
**Round:** 1  **Date:** 2026-08-08

## Verdict: APPROVED

All five hard gates pass. The Notes cover every Beamer frame's core idea (recap → scientific notation → single precision → special values/rounding → FP arithmetic → synthesis), preserve all formula symbols and numeric constants exactly (bias 127, `0x412C0000`, `1.18e-38`/`3.4e38`, shift-by-7, `S1⊕S2`, etc.), and carry no claims absent from the deck. One minor finding: a citation present in the Beamer "Rounding and Precision Loss" frame is not carried into the Notes section.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 23 content frames traced to a Notes section/example/definitionbox (frame-by-frame map below). Running thread (10.75 → 0x412C0000 → add 0.1) preserved throughout. |
| No invention | Pass | Every numeric claim, example, and elaboration in Notes traces to a Beamer frame; no new facts, figures, or formulas introduced. |
| Citation parity | Pass | Both files use exactly the key set {PattersonHennessy2017_computer_organization_design, Hamacher2002_computer_organization}; both entries exist in `Bibliography_base.bib`; no orphan keys on either side. |
| Notation fidelity | Pass | Bias 127, E_true −126..+127, 1010.11₂ = 1.01011₂ × 2³, E_stored = 130 = 1000 0010₂, 0.1 ≈ 1.100110…₂ × 2⁻⁴, ½ ULP, S=S₁⊕S₂ / M=M₁×M₂ / E=E₁+E₂−bias — all identical to Beamer. |
| Textbook-page honesty | Pass | Only page-cited source is P&H p.205, which appears in the Beamer frames and traces to `PattersonHennessy2017/index.md` ("3.5 Floating Point (p.205 — IEEE 754 single/double, add/multiply datapath)"). Hamacher/Stallings cited at chapter level only. |

## Critical Issues (MUST FIX)

None.

## Major Issues (SHOULD FIX)

None.

## Minor Issues (NICE TO FIX)

### m1: P&H citation dropped in the Rounding and Precision Loss section
- **Location:** Notes §5.2 "Rounding and Precision Loss", paragraph ending at line 138.
- **What's wrong:** The Beamer counterpart frame (lines 282–296, "Rounding and Precision Loss") closes with `(P&H, Sec.~3.5, p.205) \cite{PattersonHennessy2017_computer_organization_design}`. The Notes section summarizes the same content (0.1 repeats, ties to even, 24-bit ≈ 7 digits, ½ ULP, equality danger) but carries no P&H citation. Key sets still match, so Gate 3 passes; this is a per-location citation-parity gap.
- **Fix:** Append `(P&H, Sec.~3.5, p.205) \cite{PattersonHennessy2017_computer_organization_design}` to the end of that Notes paragraph, matching the sibling sections.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames (content, excl. titlepage) | 23 (incl. References) |
| Beamer transition slides | 5 |
| Notes top-level sections | 6 (Intro, Sci Notation, Single Precision, Special/Rounding, FP Arithmetic, Synthesis) |
| Citation keys: Beamer / Notes | 2 / 2 (identical sets) |
| Critical / Major / Minor | 0 / 0 / 1 |

**Frame → Notes trace map (content parity):**
- Where We Left Off → Notes §1 Introduction (line 49)
- Roadmap → Notes §1 (line 49, four questions + thread)
- Motivation: One Sign/Mantissa/Exponent → Notes §3.1
- Definition: Floating-Point Value → Notes Definitionbox (line 60)
- Worked Example: Binary Sci Notation → Notes Example "Binary scientific notation" (line 64)
- Socratic: What Does Normalization Buy? → Notes §3.2
- The 32-Bit Layout → Notes §4.1 (+ Figure)
- Why Bias the Exponent? → Notes §4.2
- Worked Example: Encoding 10.75 → Notes Example "Encoding 10.75" (line 111)
- Socratic: Decoding Back → Notes §4.3
- Special Values → Notes §5.1
- Worked Example: Smallest/Largest → Notes Example (line 132)
- Rounding and Precision Loss → Notes §5.2
- Worked Example: Where Precision Is Lost → Notes Example (line 140)
- Socratic: Why Not Compare Floats → Notes §5.3
- Motivation: Adding Two Exponents → Notes §6.1
- The Floating-Point Add Algorithm → Notes §6.2
- Worked Example: Adding 10.75 + 0.1 → Notes Example (line 167)
- Socratic: Multiplication, One Line → Notes §6.3
- The Thread, Closed → Notes §7.1
- Bridge to Week 4 → Notes §7.2
- Summary → Notes §7.3
- References → Notes bibliography (line 196)

**Files reviewed:**
- `Slides/CS401/03-ieee754-floating-point.tex`
- `Notes/CS401/03-ieee754-floating-point-notes.tex`
- `Bibliography_base.bib` (both cited entries present)
- `master_supporting_docs/CS401/supporting_books/PattersonHennessy2017/index.md` (p.205 verified)
