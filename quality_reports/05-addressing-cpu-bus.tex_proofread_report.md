# Proofreading Report — 05-addressing-cpu-bus.tex

**File:** `Slides/05-addressing-cpu-bus.tex` (761 lines)
**Reviewer:** proofreader (Agent C, /slide-excellence)
**Cross-checked against:** `Bibliography_base.bib`

---

### Issue 1: Terminology drift — "multi-bus" vs. "three-bus"
- **Location:** Line 544, "Socratic Check: Counting Cycles"
- **Current:** "Keep this number --- we compare it to the multi-bus trace shortly."
- **Proposed:** "Keep this number --- we compare it to the three-bus trace shortly."
- **Category:** Consistency — **Severity:** Medium
- **Rationale:** Every subsequent frame title and body reference in this section uses "three-bus" specifically (The Three-Bus Datapath, Worked Trace: ... on Three Buses, Three-Bus Organization: Trade-offs). "Multi-bus" appears nowhere else as user-facing prose (only once in a source comment, line 393). A student could read this as promising a fourth, more general "multi-bus" design rather than the concrete three-bus datapath that follows.

### Issue 2: Unexplained shift from two-operand to three-operand instruction format
- **Location:** Act 1 (lines 102-246, e.g. `ADD R1, #5`, `ADD R1, R2`) vs. Act 2 onward (lines 59, 376, 441, 530, 621: `ADD R1, R2, R3` / `R1 <- R2+R3`)
- **Current:** Addressing-mode examples throughout Act 1 use two-operand syntax where the destination is also a source (e.g., `ADD R1, #5` => `R1 <- [R1] + 5`, line 119). Act 2 onward switches without comment to three-operand syntax where the destination is distinct from both sources (`R1 <- R2 + R3`).
- **Proposed:** Add one clause acknowledging the format change, e.g. in "From 'Where' to 'How'" (line 374): "An instruction like `ADD R1, R2, R3` (note: three-operand form, distinct from the two-operand addressing-mode examples above) needs a register file, an ALU, and a path connecting them..."
- **Category:** Academic Quality — **Severity:** Medium
- **Rationale:** The instruction format is a load-bearing detail for reading the RTL traces correctly; an unflagged notational shift between sections risks confusing students who are tracking the running example literally.

### Issue 3: Naming drift — "Displacement Addressing" introduced, then called "indexed addressing" without reconciling terms
- **Location:** Line 248 (frame title "Displacement Addressing --- How Arrays Actually Work") vs. lines 288, 291-292 ("Indexed/based addressing wins"; "This is why indexed addressing exists")
- **Proposed:** "\item \good{Displacement (indexed/based) addressing wins}: ..." (or explicitly note "indexed" and "based" are the two common special cases of displacement addressing when first introduced at line 249).
- **Category:** Consistency — **Severity:** Medium
- **Rationale:** The mode is formally named "Displacement Addressing" two slides earlier (with "indexed" listed only as a sub-family member, line 249), then the Socratic-check slide and comparison table (line 341, which only has a "Displacement" row, no "Indexed" row) treat "indexed addressing" as if it were the primary/standalone term.

### Issue 4: Informal contraction "doesn't"
- **Location:** Line 81. **Current:** "The instruction format alone doesn't say." **Proposed:** "...does not say." — **Category:** Academic Quality — **Severity:** Low

### Issue 5: Informal contraction "Let's"
- **Location:** Line 451. **Current:** "Let's build both and count." **Proposed:** "Let us build both and count." (or "We will build both and count.") — **Category:** Academic Quality — **Severity:** Low

### Issue 6: Informal contraction "What's"
- **Location:** Line 732. **Current:** `\begin{exampleblock}{What's still missing}` **Proposed:** `{What Is Still Missing}` — **Category:** Academic Quality — **Severity:** Low

### Issue 7: Unnecessary hyphen after "-ly" adverb
- **Location:** Line 163. **Current:** "statically-allocated global variables." **Proposed:** "statically allocated global variables." — **Category:** Grammar — **Severity:** Low
- **Rationale:** Standard style guidance (Chicago, APA) does not hyphenate an "-ly" adverb + participle compound modifier.

### Issue 8: Unexpanded acronym "ISA" on first use
- **Location:** Line 734. **Current:** "for every instruction in the ISA, every time it runs." **Proposed:** expand on first use, or verify ISA was already defined in Lectures 1-4. — **Category:** Academic Quality — **Severity:** Low

### Issue 9: Structural inconsistency — "Compiler use:" bullet present in only some addressing-mode slides
- **Location:** Present at lines 130 (Immediate) and 163 (Direct); absent from Indirect (167-196), Register/Register-indirect (198-246), Displacement (248-277), Autoincrement (296-328).
- **Proposed:** Either add a parallel "Compiler use: ..." bullet to the remaining slides, or remove it from the two that have it. — **Category:** Consistency — **Severity:** Low

### Issue 10: Comparison table omits Autodecrement as a distinct row
- **Location:** Line 296 (frame title covers both Autoincrement/Autodecrement) vs. Line 342 (table has only an "Autoincrement" row).
- **Proposed:** Add a note/second row for autodecrement, or rename the row "Autoincrement/Autodecrement." — **Category:** Consistency — **Severity:** Low

### Issue 11: Undefined symbol "n" in comparison table
- **Location:** Line 342. **Current:** "$[R2]$, then $R2 {+}{=} n$" — introduced with no prior definition; the preceding worked slide uses a concrete "+4" instead.
- **Proposed:** "$R2 \mathrel{+}= n$ (operand size)" or reuse the concrete "4" with a footnote. — **Category:** Academic Quality — **Severity:** Low

### Issue 12: Awkward/informal trailing phrase
- **Location:** Line 690. **Current:** "cost grows roughly with the number of buses, not for free." **Proposed:** "...it is never free." — **Category:** Academic Quality — **Severity:** Low

### Issue 13: Terse/awkward closing sentence
- **Location:** Line 44. **Current:** "That is this week." **Proposed:** "That is this week's topic." — **Category:** Academic Quality — **Severity:** Low

### Issue 14: Awkward apposition
- **Location:** Line 735. **Current:** "...control unit --- hardwired control, next week." **Proposed:** "...control unit --- specifically, hardwired control, which we build next week." — **Category:** Academic Quality — **Severity:** Low

### Issue 15: Definition slide does not foreshadow the immediate-addressing exception
- **Location:** Lines 86-100 ("Definition: Addressing Mode") vs. line 127 ("Immediate Addressing").
- **Current:** General EA definition given first; two slides later, "EA does not apply" for immediate addressing — a technical contradiction if read literally.
- **Proposed:** Add a one-clause caveat/forward-pointer in the definition slide. — **Category:** Academic Quality — **Severity:** Low

### Issue 16: Overflow risk — dense recap slide
- **Location:** Lines 29-46, "Where We Left Off (Week 4)". Block with 3 itemize bullets (3rd spans PC/IR/MAR/MDR/AC/R0..Rn-1/SP, likely wraps 2-3 lines) immediately followed by a 3-line exampleblock, only 0.3cm vspace between.
- **Proposed:** Verify against compiled PDF; trim item 3 if tight. — **Category:** Overflow — **Severity:** Low

### Issue 17: Overflow risk — dense synthesis slide
- **Location:** Lines 707-721, "The Two Threads Meet". 4-line block immediately followed by an itemize with two long, dense sentences.
- **Proposed:** Verify against compiled PDF; consider shortening the longest bullet. — **Category:** Overflow — **Severity:** Low

### Issue 18: Sparse citation coverage for textbook-derived technical claims
- **Location:** Whole deck — only 3 `\cite{}` calls total (line 98: Hamacher2002; line 511 and 618: Mano1993/Hamacher2002).
- **Current:** Frames such as "How the Single Bus Works" (514-528), "Why Y and Z Exist" (548-559), "Single-Bus Organization: Trade-offs" (561-573), "Why Three Buses Are Faster" (638-649), "Three-Bus Organization: Trade-offs" (651-663) present canonical textbook analysis without citation.
- **Proposed:** Add trailing `\cite{}` calls to these analysis frames consistent with the datapath-diagram frames. — **Category:** Academic Quality — **Severity:** Low

---

## Positive Findings (no action needed)
- Citation keys resolve correctly against `Bibliography_base.bib`; each citation matches its source content (Mano1993 -> single-bus datapath; Hamacher2002 -> addressing modes / three-bus datapath).
- Register/notation terminology (`PC`, `IR`, `MAR`, `MDR`, `AC`, `SP`, `R0..Rn-1`, `EA`, `Y`, `Z`, `Bus A/B/C`) is used consistently throughout.
- Hyphenation of compound adjectives ("single-bus organization," "three-bus datapath") vs. bare noun phrases is applied correctly and consistently.
- No `\pause`/`\onslide`/`\only`/`\uncover` overlay commands found.
- No frame exceeds 2 colored boxes (checked all 33 frames).
- No duplicated words or obvious misspellings found.

---

## Summary

Overall writing quality is strong: well-structured (Socratic-question pattern, consistent RTL notation, correct compound-adjective hyphenation, clean citation-key/paper matches). Issues are mostly polish-level — a few terminology-drift spots that could genuinely confuse students (the "multi-bus"/"three-bus" slip, "displacement" vs. "indexed" naming, and the unflagged 2-operand -> 3-operand instruction-format switch), plus informal contractions, one hyphenation nit, and two frames worth a visual overflow check.

- **Critical/High severity:** 0
- **Medium severity:** 3 (terminology drift "multi-bus"/"three-bus"; unexplained instruction-format shift; "displacement" vs. "indexed" naming drift)
- **Low severity:** 15 (contractions x3, hyphenation, unexpanded ISA, structural "Compiler use" inconsistency, missing autodecrement table row, undefined symbol n, three awkward-phrasing spots, definition/exception mismatch, two overflow-risk slides, sparse citation coverage)
</content>
