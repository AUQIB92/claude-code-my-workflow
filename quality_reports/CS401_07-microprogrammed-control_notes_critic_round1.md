# Notes vs Beamer Parity Audit: CS401/07-microprogrammed-control

**Beamer source:** `Slides/CS401/07-microprogrammed-control.tex` (24 content frames + title frame + 4 transition slides)
**Notes:** `Notes/CS401/07-microprogrammed-control-notes.tex`
**Round:** 1  **Date:** 2026-08-07

## Verdict: NEEDS REVISION

One MAJOR factual inaccuracy (a numeric miscount introduced during prose expansion, directly contradicting the adjacent verbatim-copied TikZ figure) blocks APPROVED status. No hard-gate (CRITICAL) failures were found — citation parity, notation fidelity, and textbook-page honesty all pass.

## Hard Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| Content parity | Pass | All 24 content frames' core ideas are traceable to a matching Notes passage. |
| No invention | Pass (with one MAJOR accuracy flaw, not a full invention) | See M1 below — a numeric error, not a fabricated claim/example/citation. |
| Citation parity | Pass | Beamer cite keys: `Stallings2015_computer_organization`, `Mano1993_computer_system_architecture`, `Hamacher2002_computer_organization` (3 unique keys, 4 `\cite{}` calls). Notes uses the identical 3-key set (5 `\cite{}` calls — the extra occurrence is a duplicate citation of `Mano1993_computer_system_architecture` split across a figure caption and its surrounding prose, not a new key). No key appears in one file and not the other. |
| Notation fidelity | Pass | `MPC`, `CM`, microaddress, `R2_out`/`R3_out`/`Y_in`/`Z_in`/`Z_out`/`R1_in`, `ALU=add`, `\textsc{End}`, `SC_clear`, `D_i`, `T_1,T_2,\dots`, `R1 \gets R2+R3` all reproduced identically. All four TikZ diagrams are copied verbatim (same coordinates, node styles, colors) from Beamer into Notes. |
| Textbook-page honesty | Pass | Notes adds page numbers not present in the Beamer frames (p.213; p.215–224; p.215–239) only in three figure captions. Cross-checked against `master_supporting_docs/CS401/supporting_books/Mano1993/index.md`: Sec. 7-1 Control Memory = p.213 ✓; Sec. 7-2 Address Sequencing = p.215–224 ✓; Sec. 7-2/7-4 combined range = p.215–239 ✓ (7-4 Design of Control Unit ends p.239). Hamacher2002/Stallings2015 citations are correctly left at chapter-level (no invented page). |

## Critical Issues (MUST FIX)

None.

## Major Issues (SHOULD FIX)

### M1: Numeric inaccuracy — "two active" bits when the figure (and the RTL) show three
- **Location:** Notes, Section 4 ("Horizontal versus Vertical Encoding"), Example "Encoding the Worked Example, Two Ways," the paragraph immediately preceding Figure 7.3 (`fig:horizontal`).
- **Text:** *"Horizontally, each of the eight signals gets its own bit; the two active this row ($R3_{\text{out}}$ and, e.g., the ALU-add and $Z_{\text{in}}$ bits) are set to 1, the rest to 0..."*
- **What's wrong:** The sentence claims "two active" bits but then names three signals (`R3_out`, ALU=add, `Z_in`). This directly contradicts the TikZ figure copied verbatim immediately below it, which encodes exactly three 1-valued bits (`R3_o=1`, `ALU=1`, `Z_i=1`) out of eight, matching CM row 1's RTL (`Z ← [Y]+[R3]`, i.e. `R3_out`, `ALU=add`, `Z_in`). Beamer never makes this "how many bits are active" claim in prose — it only shows the diagram — so this is an inaccuracy introduced during the Notes' own expansion, not traceable to (and inconsistent with) the Beamer source.
- **Fix:** Change "the two active this row" to "the three active this row" (or simply "the active bits this row"), and tidy the parenthetical so it cleanly lists all three signals ($R3_{\text{out}}$, ALU=add, $Z_{\text{in}}$) without the confusing "and, e.g.," phrasing.

## Minor Issues (NICE TO FIX)

### m1: Two subsection headings retain presentation-pacing framing instead of topic-organized textbook titles
- **Location:** Notes §2.1 "The Missing Piece: Where Does MPC Start?" (mirrors Beamer frame "The Missing Piece: Where Does MPC Start?") and §4.1 "The Missing Piece: How Wide Is a Control Word?" (mirrors Beamer frame of the same name).
- **What's wrong:** `single-source-of-truth.md` directs Notes to "drop presentation-pacing headings" and fold that motivating content into topic-organized narrative rather than reusing the live-lecture framing device verbatim. Both headings are lifted directly from Beamer frame titles built around a paired "Socratic question" block, rather than restated as textbook-chapter topic headings. By contrast, the Notes correctly converted Beamer's "Socratic Check: What If Mapping Were Missing?" frame into the topic-style heading "Why Mapping Cannot Be Skipped" — showing the intended pattern was applied inconsistently.
- **Fix:** Rename to topic-style headings, e.g. "Locating an Instruction's Starting Microaddress" and "Sizing the Control Word," consistent with how the analogous Socratic-check frame was already handled elsewhere in the same document.

### m2: Duplicate citation split across caption and prose reads slightly redundant
- **Location:** Notes §3 (Address Sequencing), the `Mano1993_computer_system_architecture` citation appears both in the running text ("...selects between two successors \cite{Mano1993...}.") and again in the caption of Figure 7.2 immediately following it.
- **What's wrong:** Not a parity violation (same key, correctly attributable to Sec. 7-2 in both places), but the back-to-back duplicate citation for adjacent sentences is stylistically redundant compared to the Beamer source, which cites once.
- **Fix:** Optional — no gate is violated; leave as-is or drop the prose-sentence citation since the figure caption already grounds the section.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Beamer frames (content, excl. titlepage) | 24 |
| Beamer transition slides | 4 |
| Notes top-level sections | 5 (`Introduction`, §7.1 Microinstructions and Control Memory, §7.2 Address Sequencing, §7.3 Horizontal vs. Vertical Encoding, §7.4 Synthesis) |
| Citation keys: Beamer / Notes | 3 unique / 3 unique (identical set) |
| Critical / Major / Minor | 0 / 1 / 2 |

**Files reviewed:**
- `Slides/CS401/07-microprogrammed-control.tex`
- `Notes/CS401/07-microprogrammed-control-notes.tex`
- `master_supporting_docs/CS401/supporting_books/Mano1993/index.md`
- `.claude/rules/knowledge-base-CS401.md`
