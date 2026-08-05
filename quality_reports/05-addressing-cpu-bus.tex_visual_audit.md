# Visual Layout Audit Report

**File:** `Slides/05-addressing-cpu-bus.tex`
**Reviewer:** slide-auditor (Agent A, /slide-excellence)

> Note: this deck actually contains **9 `tikzpicture` environments** (Immediate/Direct/Indirect/Register/Displacement/Autoincrement addressing-mode diagrams, the CPU building-blocks diagram, and the single-bus/three-bus datapath diagrams) — the pre-flight TikZ detection in this run initially misreported 0 due to a shell-escaping bug and was corrected mid-review. This visual audit did not run the full six-pass TikZ measurement protocol (out of its stated text/layout scope), but flagged a couple of diagram-related consistency issues below since they affect layout. A dedicated `tikz-reviewer` pass was run separately to cover collision/overlap/margin correctness.

---

## Critical / High Severity

### Slide: "Worked Trace: R1 ← R2 + R3 on a Single Bus" (~line 530)
- **Issue:** The RTL trace table uses `\begin{tabular}{@{}clll@{}}` — the last three columns are plain `l` (no `p{}` wrap width). Cell content in the "What happens" column (e.g., `R3 onto bus $\to$ ALU; ALU adds $Y$; result $\to Z$`) is long and will NOT wrap, forcing the table to its natural (unwrapped) width — well beyond the ~10.8-11.3 cm text width available on a 16:9 Beamer slide.
- **Recommendation:** Convert the last one or two columns to `p{4.5cm}` / `p{3.5cm}` (wrapped) instead of `l`, and re-balance widths so total ≤ textwidth. Spacing-first alternative: shorten the "What happens" prose (e.g., "R3→bus→ALU; +Y; →Z") before resorting to font shrink.
- **Note:** Verify with an actual `xelatex` compile; this pattern reliably produces "Overfull \hbox" warnings and can spill off the right edge of the slide.

### Slide: "Worked Trace: R1 ← R2 + R3 on Three Buses" (~line 621)
- **Issue:** Same problem as above — `\begin{tabular}{@{}clll@{}}` with an unwrapped `l` column holding "Both operands read *and* the ALU output written back, all in one cycle."
- **Recommendation:** Same fix — wrap the long descriptive column with `p{}`, or split into two shorter sentences/rows. Fix both trace tables consistently so the parallel slides stay visually matched.

### Slide: "Addressing Modes: Side by Side" (~line 330)
- **Issue:** Table columns are `p{2.6cm}p{2.9cm}p{2.6cm}p{3.6cm}` — content widths alone sum to 11.7 cm, plus ~1.3 cm of inter-column padding (3 gaps × ~0.42 cm) ≈ 13 cm total, exceeding the ~10.8-11.3 cm available text width on `aspectratio=169`.
- **Recommendation:** Reduce column widths (e.g., 2.2/2.4/2.2/3.0 cm) or wrap the whole table in `\resizebox{\textwidth}{!}{...}`. This is a 7-row summary table — consider whether "Typical use" needs its own 3.6 cm column or could be shortened to one or two words.
- **Note:** Confirm via compile log for "Overfull \hbox (~X pt too wide)".

### Slide: "Single-Bus vs. Three-Bus: The Full Comparison" (~line 665)
- **Issue:** Table columns `p{3.2cm}p{4.4cm}p{4.4cm}` sum to 12 cm content width + ~0.85 cm padding ≈ 12.85 cm — the widest table in the deck, clearly exceeding text width.
- **Recommendation:** Shrink each column by ~15-20% (e.g., 2.8/3.8/3.8 cm) or apply `\resizebox{\textwidth}{!}{...}`. This is the most overflow-prone slide in the file and should be fixed first. `\footnotesize` is already applied, so a `\resizebox` is a natural next step given the content is already terse.

## Medium Severity

### Slide: "Register and Register-Indirect Addressing" (~line 198)
- **Issue:** Densest single slide in the deck: two-column layout, each column carrying a bold sub-heading + `exampleblock` + 2-item itemize, followed by a centered two-row TikZ diagram (register vs. register-indirect) below the columns. Combined vertical stack is tight for a 7.2 cm-tall slide body.
- **Recommendation:** Spacing-first: trim each itemize to 1 bullet, or shave `\vspace{0.2cm}` further. If still cramped after compiling, consider splitting into two slides (Register alone, then Register-Indirect alone) to match the one-mode-per-slide pattern used elsewhere in Act 1.

## Low Severity

### Slide: "The Single-Bus Datapath" vs. "The Three-Bus Datapath" (~line 461 vs. ~line 597)
- **Issue:** Structural asymmetry — the Three-Bus Datapath slide has 2 lines of explanatory text below its diagram (before the citation), while the Single-Bus Datapath slide has only the diagram + a bare `\cite{...}` with no framing sentence.
- **Recommendation:** Add one short framing sentence under the Single-Bus diagram for parallel structure — e.g., "One shared path connects every register, the ALU, and memory." Not a functional defect (the following slide, "How the Single Bus Works," does supply the explanation) — purely a rhythm/consistency polish.

### Deck-wide: TikZ diagram scale inconsistency
- **Issue:** The addressing-mode diagrams use inconsistent `scale=` factors across otherwise-parallel slides: Immediate (0.8), Direct (0.78), Indirect (0.78), Register/Register-Indirect (0.72), Displacement (0.8), Autoincrement (0.75), CPU building blocks (0.85), Single-bus datapath (0.68), Three-bus datapath (0.85). All correctly pair `scale` with `transform shape`, so this is a visual-rhythm issue, not a collision risk.
- **Recommendation:** Standardize scale within each visual "family" — the 6 addressing-mode diagrams (Immediate through Autoincrement) should probably share one scale (e.g., all 0.78) so diagrams don't appear to shrink/grow between adjacent slides. The single-bus datapath (0.68) is legitimately the most complex diagram and can stay smaller.

### Slide: "Where We Left Off (Week 4)" (~line 29)
- **Issue:** Third bullet in the recap block is unusually dense: "Registers already in play: `PC` (next instruction), `IR` (current instruction), `MAR`/`MDR` (memory address/data), `AC` or a register file `R0..Rn-1`, `SP` (stack)." — likely wraps to 3+ lines inside the block, on a slide that already carries a second `exampleblock` below it.
- **Recommendation:** Spacing-first: break the register-list bullet into two shorter bullets, or move it to a small inline table/columns layout for scannability. Not a hard overflow risk given only 2 boxes are used, just a density/readability nit.

---

## What's Clean (No Issues Found)

- **Box fatigue:** every frame stays at 0-2 colored boxes (`block`/`exampleblock`/`alertblock`). No frame exceeds the limit; transitional remarks are correctly left as plain text, not boxed.
- **Itemize/enumerate nesting:** no nested lists anywhere in the file — every itemize/enumerate is a single flat level.
- **Semantic color usage:** `\good{...}`/`\bad{...}` are used correctly on binary contrasts (e.g., "Direct addressing fails" vs. "Indexed/based addressing wins"; Pro/Con trade-off lists).
- **Motivation before formalism:** both formal-definition slides ("Definition: Addressing Mode" and "Notation: Register Transfer Language (RTL)") are preceded by a Socratic/motivating slide.
- **No `\pause`/overlay commands:** zero uses of `\pause`, `\only`, `\onslide`, `\uncover`, `\visible`.
- **`\footnotesize` usage:** only applied to the 4 wide tables and the References slide — a consistent, purposeful pattern, not scattered ad-hoc font shrinking.
- **`\includegraphics`:** none used (all visuals are native TikZ), so no raster/PDF image-sizing issues.

---

## Summary

**Overall visual quality impression:** Structurally disciplined — the deck consistently follows a one-idea-per-slide, ≤2-boxes-per-slide, flat-list, Socratic-before-formal pattern with no `\pause`/overlay violations and correct semantic-color usage. The real risk is concentrated in a handful of **tables that are simply too wide for a 16:9 Beamer text block** (two of them additionally use unwrapped `l` columns with long prose, which is worse), plus one visually dense two-column slide.

**Issue counts:**
- **Critical/High:** 4 (all table-width/overflow issues — 2 unwrapped-column RTL trace tables, 2 oversized `p{}` summary/comparison tables)
- **Medium:** 1 (Register/Register-Indirect Addressing slide — dense two-column + diagram stack)
- **Low:** 3 (Single-Bus vs. Three-Bus datapath framing-text asymmetry; inconsistent TikZ `scale=` factors; one overly dense recap bullet)
</content>
