# Critic report: CS401 12 — Pipelining, RISC, and CISC notes (round 2)

**Verdict: NEEDS REVISION**

## Scope and method

Compared `Slides/CS401/12-pipelining-risc-cisc.tex` as the source of truth with `Notes/CS401/12-pipelining-risc-cisc-notes.tex`, treating the notes as reorganized prose rather than a frame-by-frame transcript. Checked substantive concepts, equations, tables, examples, checks/review items, references, notation, and the exercise/solution material. Also searched the repository for the indexed P&H/Stallings reference files.

## Findings

1. **Coverage is incomplete.** The notes preserve the main narrative—pipeline motivation and throughput/latency, five-stage datapath, hazards, forwarding/stalls/flushes, branch prediction, superscalar/VLIW, and RISC/CISC comparison—but omit or substantially compress several deck-specific artifacts: the deck’s explicit timing/table material, worked hazard timeline/details, selected review/check prompts, and the full reference/review framing. These omissions are acceptable only if intentionally summarized; for this audit, the requirement was that every substantive frame idea, including tables, examples, checks, review items, and references, be present.
2. **The four notes examples are not fully solved.** They are largely prompts or qualitative discussions, without complete derivations/timing tables and final answers corresponding to the deck’s concrete worked material. The exercises likewise do not consistently provide solutions; at least one item remains an open exercise rather than a solved answer. This fails the explicit examples-and-exercises requirement.
3. **Notation is not fully faithful.** The notes paraphrase the deck’s pipeline timing/hazard notation and use generic stage labels and prose where the deck distinguishes instruction timing, stall/flush effects, and control/data/structural hazards. The result is understandable, but not a faithful reproduction of all equations and tabular relationships.
4. **Citation-key parity is not demonstrated.** The deck’s bibliography/citation keys and the notes’ citation usage are not maintained as a complete matching set. The notes use prose references but do not preserve every deck citation key/reference entry, so the citation-key check cannot pass as written.
5. **Page references are not auditable/honest.** The repository search did not locate a usable indexed P&H/Stallings source matching the notes’ page claims, and the notes do not consistently identify edition/index context. Page assertions therefore need either verification against the indexed files or removal/replacement with stable chapter/section references.

## Positive aspects

The notes are well organized topically, readable, and cover the central teaching arc. The explanations of why pipelining improves throughput rather than single-instruction latency, the main hazard classes, and the RISC/CISC distinction are broadly aligned with the deck.

## Required revision

Add the omitted deck-specific tables/equations/checks/review items/references; preserve the deck’s notation and citation keys; verify every P&H/Stallings page claim against the indexed files (or qualify/remove it); and fully solve all four examples and every exercise, with explicit final answers and timing/derivation work where applicable. Re-run the six requested checks after revision.
