# Repository Innovation Report

**Target:** `D:\Academic-Workload\Academic-Skill` ("My Claude Code Setup") · **Mode:** default (full pipeline) · **Date:** 2026-08-20

**Prior art excluded by design.** This run does not re-propose anything already found and written up in `quality_reports/feature_discovery_2026-08-19/REPORT.md` (maintenance/gap-fill pass — fork-identity bug, GoatCounter ID, unscheduled nightly-repro-check, submission→grading bridge, CI gate-parity) or `quality_reports/feature_discovery_2026-08-19/INNOVATION_REPORT.md` (an earlier hand-run "No. 1" pass — Universal Verification Passport, Public Verification Certificate, Interactive Socratic-Check widgets, profile-pruning onboarding wizard, per-student weak-CO remediation packets, verification-methodology doc, community domain-pack registry, skill regression harness, orchestration observatory, live-reference-week showcase, adopter registry, correction-to-skill-patch loop, standalone-CLI spinout, portable course package, isomorphic assessment variants). Where a new idea below genuinely extends one of those, it says so explicitly rather than silently re-deriving it.

---

## 1. What This Project Could Become

**TODAY:** A mature, unusually well-governed Claude Code academic template — 73 skills / 23 agents / 39 rules / 7 hooks — that builds and quality-gates a full engineering course (Beamer → Quarto → Notes → Assignments → Labs → GATE practice sets → NBA/AICTE accreditation filings) for CS401/CS301 at GCET Ganderbal, an AICTE-affiliated Indian engineering college. It already runs a real fan-out→reduce→judge orchestration runtime with a CoVe-style hallucination guard reused four separate times (`/verify-claims`, `/verify-symbolic`, `/verify-algorithm`, `/student-simulator`), and it already contains — separately, not yet connected — genuine NBA/AICTE compliance domain modeling (`/accreditation`'s 12-PO matrix + attainment formulas) and a page-exact, OCR-recoverable provenance ladder for GATE past-year questions (`CompetitiveExam/Books/index.md`).

**TOMORROW:** The reference implementation for two adjacent, currently-disconnected markets this repo already has one foot in: (1) continuous, evidence-linked NBA/AICTE program accreditation for the ~10,000+ AICTE-affiliated engineering colleges in India that redo this bureaucratic exercise by hand every accreditation cycle, and (2) a working, provenance-guaranteed implementation of the exact research question the repo's own `Papers/` directory just finished surveying — LLM-orchestrated educational video/animation generation — closing the loop from literature review to verified system.

**THE DIFFERENCE:** Two mechanisms this repo already has, but has never pointed at each other or at their obvious next step. `/accreditation` mints correct CO-PO-PSO matrices but only ever for one `<CODE>` at a time, even though NBA accredits *programs*, not courses — nobody has built the cross-course rollup. And `trace-execution` already turns a mechanism into a coordinate-consistent sequence of step diagrams, and `Papers/` already contains a CoVe-verified literature review on turning exactly that kind of content into narrated video — nobody has built the compiler that goes from step-diagram sequence to video. Both gaps are one architectural extension away, not a rebuild.

---

## 2. Repository Superpowers

| Existing Asset | Untapped Potential | Possible Innovation |
|---|---|---|
| `.claude/rules/knowledge-base-<CODE>.md` **Symbol Reference** table (`Symbol \| Meaning \| Introduced`, hand-maintained, e.g. `PC — Week 4 (confirmed)`) | Currently read only by an LLM fan-out reviewer (`/course-arc-audit`) making a judgment call; never mechanically cross-checked against actual first-use locations in `Slides/`/`Notes/`/`Quarto/` | A deterministic prerequisite/scope compiler — grep every symbol's real first use, compare against its declared "Introduced" week, flag violations the way a compiler flags a used-before-declared variable |
| `templates/passport-template.yaml` / `.claude/rules/replication-protocol.md`'s `passport.yaml` provenance ledger | Scoped to numeric claims in **papers only**; read/written by exactly two skills (`/audit-reproducibility`, `/commit`'s advisory check) | Generalize the *mechanism* (not just the schema — a prior report already proposed the schema extension) into a first-class build-graph node other skills can query for staleness, not just a claims table |
| `/accreditation`'s per-course CO-PO-PSO matrix + `/grade --tally`'s attainment data | NBA accredits the **program**, not the course; `Accreditation/<CODE>/` is confirmed single-course-scoped (verified by reading `accreditation/SKILL.md` Phase 5 — one `co-po-attainment.tex` per `<CODE>`, no cross-course rollup anywhere) | A program-level Self-Assessment Report generator that rolls up every `<CODE>`'s PO attainment into one filing, the actual unit NBA evaluates |
| `student-simulator`'s "cold persona, hasn't seen the answers, records its own stumble before reveal, diffs against a prediction" pattern | Wired to exactly one domain: pedagogy playtesting against an instructor handout's predicted misconceptions | The identical pattern applied to a different domain: a cold "NBA peer-reviewer" persona auditing `Accreditation/<CODE>/` filings the way a real assessor would, before the real assessor ever sees it |
| `trace-execution`'s step-diagram TikZ sequences (coordinate-consistent, one figure per state change) + `Papers/prompt-to-render-educational-video-generation.tex` (a CoVe-verified SLR the repo's own owner just wrote, on exactly this topic) | Stops at static SVG/PDF figures; the survey paper studying the target capability lives one directory away from the pipeline that could build it | A verified lecture-to-video compiler that turns an already-existing step sequence into narrated, provenance-guaranteed animation — closing the loop from literature review to working system in the same repo |
| `CompetitiveExam/Books/index.md`'s 3-tier sourcing ladder (verified-book / verified-web / original-pattern) with page-exact citations and an OCR-recovery sub-pipeline | Used only to answer "is this topic locally sourced," never to model question *difficulty* | Real historical-difficulty calibration (IRT-style) driving an adaptive practice schedule, not just topic-scoped question dumps |

---

## 3. Innovation Landscape

*(24 ideas, before filtering.)*

### AI-Native Opportunities
1. **Verified Lecture-to-Video Compiler** — `trace-execution` step sequences + narration, with provenance guarantees against hallucinated content.
2. **NBA Assessor Dry-Run persona** — `student-simulator`'s cold-persona pattern retargeted at `Accreditation/<CODE>` filings.
3. **Concept Dependency Compiler** — deterministic parse of Symbol Reference "Introduced" data vs. real first-use locations.
4. **Adaptive GATE Practice Engine** — spaced-repetition scheduling over `CompetitiveExam/Books`' provenance ladder.

### Architectural Innovations
5. **Program-level NBA SAR generator** — cross-course PO rollup across every `<CODE>` in `Accreditation/`.
6. **Passport-as-build-graph-node** — promote `passport.yaml` from a paper-scoped advisory table to a queryable dependency node other skills read.
7. **Knowledge-Base-as-Schema** — formalize `knowledge-base-<CODE>.md`'s free-text tables into one machine-parseable source every skill reads instead of independently re-parsing prose.
8. **Multi-tenant course-fork isolation** — git-worktree-per-course workflow now that CS301 is mid-buildout alongside CS401.

### Product Moonshots
9. **Accreditation Autopilot** (elevated #5 — continuous, evidence-linked, program-wide, not a one-shot per-course draft).
10. **Proof-Carrying Animation Compiler** (elevated #1 — full narrated pipeline, not just step diagrams).
11. **Cross-Institution NBA Benchmark Network** — opt-in, anonymized aggregation of CO-PO correlation patterns across institutions running this template.
12. **Regulatory Diff Bot** — `textbook-edition-diff`'s pattern applied to NBA/AICTE circulars instead of textbook editions, flagging drift against the encoded 12-PO table/formulas.

### Developer Experience Breakthroughs
13. **Concept-scope debugger** — interactive "why is this symbol undefined here" query mode on top of #3.
14. **Provenance-aware diff viewer** — visualize which derived artifacts (Quarto/Notes/Assignments/GATE/Accreditation) go stale when a source file changes.
15. **Student-facing "Explain This Grade" receipt** — expose the actual SymPy/algorithm verification chain behind a score, not just the score.
16. **Toolchain Doctor** — auto-fingerprint the local MiKTeX/Windows/PDF-renderer environment instead of hand-maintained prose workarounds (`TROUBLESHOOTING.md`, the LaTeX-toolchain-paths MEMORY entry).

### Ecosystem Opportunities
17. **Discipline-agnostic NBA/AICTE compliance tier** — NBA's 12 POs are universal across engineering disciplines, not CS-specific; spin the compliance layer out for Mechanical/Civil/Electrical departments to fork independently of CS401/CS301 content.
18. **GATE PYQ provenance registry as a public good** — publish the topic→page metadata schema (never the copyrighted PDFs) for other GATE-prep tooling to consume.
19. **Cross-course bibliography health map** — which `Bibliography_base.bib` entries are load-bearing across multiple `<CODE>`s, now that more than one course shares it.
20. **Verified-content interop format** — formalize the 3-tier GATE provenance tag as an importable/exportable schema.

### Research Frontier Ideas
21. **Executable formula-lineage graph** — represent every knowledge-base formula as a SymPy node with declared inputs/outputs, so `/verify-symbolic` can mechanically prove cross-week consistency (e.g., Week 11's pipelining speedup formula against Week 1's Amdahl's Law), not just check one claim in isolation.
22. **LLM-video research testbed** — turn the `Papers/` SLR into primary research by building and evaluating the system it surveys.
23. **Counterfactual lecture-ordering simulator** — run `student-simulator` across alternative topic orderings to estimate which reduces predicted stumbles before either is ever taught live.
24. **IRT calibration of the GATE question bank** — real difficulty/discrimination parameters from historical GATE data driving question selection.

---

## 4. Combine (≥5)

- **C1 — Accreditation Autopilot** = #2 (Assessor Dry-Run) + #5 (program-level SAR) + #12 (Regulatory Diff Bot). One connected pipeline: draft the program-level SAR → have a cold assessor persona critique it before a human sees it → watch for the underlying NBA/AICTE rules drifting out from under the encoded 12-PO table.
- **C2 — Course Build Graph** = #3 (Concept Dependency Compiler) + #14 (provenance-aware diff viewer) + #6 (passport-as-build-node). One explicit, queryable DAG over the whole Beamer→Quarto/Notes/Assignments/GATE/Accreditation derivation cascade, instead of three skills each independently re-deriving pieces of the same relationship.
- **C3 — Proof-Carrying Animation Compiler** = #1 (Verified Lecture-to-Video) + #22 (video research testbed) + `trace-execution`'s existing step-sequence generator. Simultaneously a shippable feature and the natural second paper after the repo's own SLR.
- **C4 — Psychometric GATE Trainer** = #4 (adaptive practice engine) + #24 (IRT calibration) + the *already-proposed* (prior report) per-student weak-CO detection — explicitly building on that idea rather than re-deriving it, adding real difficulty calibration instead of flat topic scoping.
- **C5 — Institution Health Telemetry** = #16 (Toolchain Doctor) + #11 (cross-institution benchmark network) — reuses one opt-in anonymized-aggregation pattern for two different data types (build-environment fingerprints, NBA correlation-matrix patterns).
- **C6 — Student-Facing Verification Receipt** = #15 (Explain This Grade) + the existing (unextended) passport concept — every returned grade ships a mini-receipt of exactly how it was mechanically verified.

## Contrarian (≥5)

- **X1 — Invert single-source-of-truth for schema-like content.** Keep Beamer as SoT for narrative lecture content, but for the two most schema-shaped content types (`Accreditation/` matrices, `CompetitiveExam/` question banks), make YAML the authored source and LaTeX a generated render target — inverting CLAUDE.md's own "Beamer is authoritative" rule, deliberately, for exactly the content types where it doesn't fit. Plausible: `templates/` already has YAML-first precedent (rubrics, RUN_CONFIG).
- **X2 — Hard-gate accreditation defensibility at commit time.** Block `/commit` on any `Accreditation/<CODE>` file if a CO has zero PO correlation or missing evidence — treat compliance risk as a quality gate the same class as the 80/100 slide-quality bar. `.githooks/pre-commit` is direct in-repo precedent for exactly this shape.
- **X3 — A live "ask the auditor" kiosk.** During a real NBA visit, let an actual assessor query a read-only terminal over the repo's own committed, passport-verified evidence — no live external users, no auth, just a local citation-backed Q&A surface. Bounded by plausibility (kiosk, not public service) but technically just a read-only chat over already-indexed evidence.
- **X4 — Self-teaching video QA loop.** Chain C3 (Animation Compiler) with `student-simulator`: have a synthetic cold-student "watch" the generated narration transcript, predict where it would stumble, and auto-flag segments for re-cut before a human ever watches the output — automated pre-release QA for AI-generated video, going past correctness verification into predicted-comprehension verification.
- **X5 — Executable formula-lineage graph across the whole semester** (= #21 above, restated as the contrarian frame): not "check this one claim" but "mechanically prove this week's formula is algebraically consistent with a formula three months earlier in the same course."

**Anti-Generic Rule check:** none of the 24 diverge/6 combine/5 contrarian ideas above fall in the banned generic category (dark mode, notifications, analytics, mobile, caching, profiles, dashboards, generic search) — so the four-question clearance test in Anti-Generic Rules never had to be invoked this run.

---

## 5. The Crazy but Plausible Ideas

1. **X1 — Schema-as-source for compliance/GATE content.** *Sounds crazy:* contradicts the repo's own governing rule ("Beamer `.tex` is authoritative"). *Why plausible:* only proposed for the two content types that are already tabular/schema-shaped in practice, not narrative — the rule was written for lecture prose, not for a CO-PO matrix. *Experiment:* pick one already-drafted `Accreditation/CS401/co-po-attainment.tex`, hand-author its YAML equivalent, generate the `.tex` from it, and diff against the original for fidelity loss.
2. **X2 — Hard-gated accreditation commits.** *Sounds crazy:* inserts real compliance risk into the everyday dev loop, unlike a slide-quality score. *Why plausible:* the exact same pattern (warn-first, `--strict` opt-in escalation) already exists for the numeric-claims passport in `/commit`. *Experiment:* run the gate in warn-only mode for one semester on `Accreditation/CS401/`, count false positives.
3. **X3 — Live auditor kiosk.** *Sounds crazy:* implies opening the repo's evidence to a real external assessor's live questions. *Why plausible:* it's a local, read-only chat surface over data that's already committed and already passport-verifiable — no new trust boundary beyond "person is physically in the room." *Experiment:* a single-session Claude Code run pointed at `Accreditation/CS401/` answering 10 canned NBA-style questions, graded for citation accuracy.
4. **X4 — Self-teaching video QA loop.** *Sounds crazy:* AI grading AI-generated video's comprehensibility, two layers of synthetic judgment. *Why plausible:* `student-simulator` already produces exactly this kind of stumble-prediction artifact for static decks; feeding it a transcript instead of slides is a narrow input-format change, not new capability. *Experiment:* run `student-simulator` against one already-authored Socratic-Check block's *prose explanation* instead of the slide, compare stumble predictions.
5. **X5 — Executable formula-lineage graph.** *Sounds crazy:* a full computer-algebra proof spanning an entire semester's formulas. *Why plausible:* `/verify-symbolic` already does single-claim SymPy re-derivation; representing each Symbol Reference formula row as a SymPy expression with typed inputs/outputs is a data-modeling problem, not a new verification technique. *Experiment:* encode just the three chained formulas already in `knowledge-base-CS401.md` (CPU time → MIPS → Amdahl's Law) as SymPy nodes and mechanically substitute one into another.

---

## 6. Top 10 Category-Defining Features

*Only ideas that cleared both the 35% confidence-modified-% floor and the No. 1 Test (≥4/7 YES) appear here as full dossiers — four did. This is not padding to reach ten; the remaining sixteen diverge/combine/contrarian ideas are accounted for in §8, most with a specific, real reason (external validation this skill cannot perform, superseded by a stronger sibling bet, or correctly belongs to `/feature-discovery` instead) rather than a generic rejection.*

### Accreditation Autopilot
*The pipeline that drafts, dry-run-audits, and drift-checks an entire program's NBA/AICTE filing, not one course's.*
**Confidence:** ARCHITECTURAL INFERENCE — grounded in `.claude/skills/accreditation/SKILL.md` (confirmed single-`<CODE>`-scoped), `student-simulator`'s cold-persona mechanism, and `textbook-edition-diff`'s diff-against-prior-index pattern.
**The Problem:** NBA accredits a *program* (e.g., the whole B.Tech CSE degree), not a course, but `Accreditation/<CODE>/co-po-attainment.tex` is generated one course at a time with no cross-course rollup — confirmed by reading Phase 5 of `accreditation/SKILL.md`. The actual filing unit doesn't exist yet, and every three-year re-accreditation cycle at GCET Ganderbal (and every AICTE-affiliated college like it) redoes this compilation by hand.
**The Insight:** The repo already has all three components separately — per-course CO-PO data, a cold-persona critique pattern, and a document-diff pattern for a related domain (textbook editions) — none pointed at the accreditation domain together.
**Why Existing Alternatives Don't Do This:** No comparable Claude Code academic template embeds NBA/AICTE compliance modeling at all, let alone continuously, let alone program-wide; this is institutional-process automation, not slide tooling, and sits outside the category every comparable template competes in.
**Why This Repository Can:** It already has the 12-PO taxonomy encoded, the attainment formula machinery, the never-fabricate-a-number discipline (`[FILL]` convention from `/replication-package`), and a working cold-persona QA pattern to reuse verbatim.
**Architecture Impact:** New `Accreditation/<program>/self-assessment-report.tex` rollup target; a new `nba-assessor` agent (Sonnet tier, read-only, same shape as `student-simulator`); a `Regulatory Diff` phase reusing `textbook-edition-diff`'s diff-against-recorded-mapping logic against an uploaded NBA circular instead of a textbook TOC.
**Magic Moment:** `Faculty coordinator runs: /accreditation-autopilot CSE` → `System automatically: rolls up every accredited course's PO attainment into one program-level SAR draft, then a cold assessor persona flags the three COs with no supporting evidence before the real NBA team ever sees the filing.`
**Why It Could Matter:** This is real, recurring, high-stakes institutional pain at a scale (~10,000+ AICTE-affiliated colleges) no comparable Claude Code template addresses at all.
**Innovation Score:** Novelty 4/5 · Impact 5/5 · Differentiation 5/5 · Defensibility 4/5 · Excitement 4/5 · Architectural Fit 5/5 · Feasibility 4/5
**Confidence-modified %:** 72% (STRATEGIC BET)
**No. 1 Test:** 7/7 passed

---

### Course Build Graph
*A deterministic dependency graph over the whole content-derivation cascade, replacing three independent partial re-derivations with one queried source of truth.*
**Confidence:** ARCHITECTURAL INFERENCE — grounded in `knowledge-base-CS401.md`'s Symbol Reference table (`Symbol \| Meaning \| Introduced`, real data, e.g. `PC — Week 4 (confirmed)`), `replication-protocol.md`'s `passport.yaml`, and the existing `qa-quarto`/`qa-notes` parity-checking precedent.
**The Problem:** Cross-week/cross-artifact consistency today is checked entirely by LLM judgment (`/course-arc-audit`'s fan-out, `/qa-quarto`'s critic) — real, but non-deterministic and attention-limited. The Symbol Reference table already encodes exactly the ground truth (which week a symbol is legitimately first usable) that a mechanical scope checker needs, and nothing reads it that way.
**The Insight:** The repo has independently built three pieces of the same underlying graph — symbol-introduction data, provenance data (passport), and derived-artifact relationships (Beamer→Quarto/Notes/Assignments) — as three separate, un-queryable systems.
**Why Existing Alternatives Don't Do This:** LLM-fan-out review is this repo's own established pattern precisely because deterministic tooling wasn't built for this domain; a real compiler-style pass catches a class of error (used-before-declared symbol) attention-limited review will sometimes miss.
**Why This Repository Can:** The ground-truth data already exists, structured, per course, maintained as a side effect of normal authoring — nothing needs to be newly collected, only newly read mechanically.
**Architecture Impact:** New `scripts/check-concept-scope.py` (Haiku-tier mechanical check, per `model-routing.md`'s 70% bucket); wired into `check-surface-sync.sh`; `passport.yaml`'s mechanism generalized (not its schema, already proposed elsewhere) into a queryable node other skills call instead of re-deriving staleness themselves.
**Magic Moment:** `Instructor runs: /build-week CS401/09` → `System automatically: flags that slide 14 uses "EA" (Effective Address) before its declared Week 5 introduction, three weeks before the intended reveal — a real prerequisite bug caught deterministically, not by chance during review.`
**Why It Could Matter:** Compounds — every new week/course adds more ground-truth data the graph can check against, making it strictly harder for a competitor to replicate the *value*, even though the mechanism itself is simple to describe.
**Innovation Score:** Novelty 4/5 · Impact 4/5 · Differentiation 4/5 · Defensibility 5/5 · Excitement 3/5 · Architectural Fit 5/5 · Feasibility 4/5
**Confidence-modified %:** 66% (STRATEGIC BET)
**No. 1 Test:** 7/7 passed

---

### Proof-Carrying Animation Compiler
*Turns `trace-execution`'s step-diagram sequences into narrated, provenance-guaranteed lecture video — closing the loop on the repo's own literature review.*
**Confidence:** MOONSHOT — technically plausible, requires real experimentation (new external tooling: frame-stitching, optional TTS); never presented as more certain than that.
**The Problem:** `Papers/prompt-to-render-educational-video-generation.tex` is a CoVe-verified systematic literature review, by this repo's own author, on exactly this capability — and the repo already builds most of the primitives such a system needs (step-consistent TikZ diagrams via `trace-execution`, Beamer overlay animation, a verification discipline to prevent narration from saying something the source deck doesn't) without ever connecting them.
**The Insight:** The hardest part of "verified educational video generation" isn't rendering — it's guaranteeing the narration doesn't hallucinate beyond the source material. This repo already solved that exact problem, for a different content type, four times over (CoVe citation-checking, SymPy re-derivation, algorithm execution, numeric-claim audits).
**Why Existing Alternatives Don't Do This:** Generic AI-video tools generate content from a prompt with no source-grounding contract; this repo's differentiator is refusing to narrate anything the underlying Beamer/TikZ source doesn't already state.
**Why This Repository Can:** It has the step-sequence generator, the Beamer/TikZ toolchain, and — uniquely — a completed literature survey of the target capability sitting in the same repository, written with the intent of closing the loop.
**Architecture Impact:** New `/render-lecture-video` skill (fork context, Sonnet-tier for narration drafting) chaining `trace-execution`'s output → a narration-fidelity check (reuse the CoVe pattern, narration claims verified against the source deck) → frame export → `ffmpeg` stitch (new external dependency, MVP scope: silent animation + synced on-screen captions, no audio TTS required for v1).
**Magic Moment:** `Instructor runs: /render-lecture-video CS401/06-hardwired-control "control-unit RTL sequence"` → `System automatically: generates the already-drafted step diagrams as an animated sequence with synced captions, and refuses to render a caption sentence that doesn't trace to the source deck.`
**Why It Could Matter:** The single most demoable, shareable capability on this list — the kind of feature that gets a repo forked just to try it — and it's the natural second research contribution after the repo's own SLR.
**Innovation Score:** Novelty 5/5 · Impact 4/5 · Differentiation 5/5 · Defensibility 3/5 · Excitement 5/5 · Architectural Fit 3/5 · Feasibility 3/5
**Confidence-modified %:** 51.6% (STRONG DIFFERENTIATOR)
**No. 1 Test:** 6/7 passed *(dissent on Q2 — raw AI-video generation is increasingly commoditized externally; the durable differentiator is the source-grounding guarantee specifically, not video generation per se)*

---

### Psychometric GATE Trainer
*Real difficulty-calibrated, spaced-repetition GATE practice, replacing flat topic-scoped question dumps.*
**Confidence:** ARCHITECTURAL INFERENCE — grounded in `CompetitiveExam/Books/index.md`'s page-exact provenance ladder and the prior report's (acknowledged, not re-derived) per-student weak-CO detection gap.
**The Problem:** `/competitive-exam-questions` sources verified real PYQs but treats every question in a topic as interchangeable; no difficulty signal survives from the source book into practice scheduling.
**The Insight:** GATE PYQs carry a real year + question number, which is enough to look up historical difficulty/discrimination statistics and drive an actual spaced-repetition schedule instead of a flat topic list.
**Why Existing Alternatives Don't Do This:** Generic spaced-repetition tools have no access to this repo's page-exact, tier-1-verified provenance data; generic GATE-prep apps don't integrate with a specific course's weak-CO signal.
**Why This Repository Can:** The provenance ladder and (once built, per the prior report) the weak-CO detection both already exist; this is a scheduling layer on top, not new sourcing infrastructure.
**Architecture Impact:** New `scripts/gate-scheduler.py` reading `CompetitiveExam/Books/index.md` provenance + a per-student practice log; no change to the sourcing skill itself.
**Magic Moment:** `Student opens their practice queue` → `System automatically: surfaces the cache-memory question they got wrong three days ago, right before it would otherwise be forgotten, instead of a random new topic.`
**Why It Could Matter:** Direct, measurable student-facing value; the provenance-ladder data underneath is genuinely hard to replicate (a competitor would need the same page-exact book index), even though spaced repetition as a category is well-trodden.
**Innovation Score:** Novelty 3/5 · Impact 4/5 · Differentiation 3/5 · Defensibility 3/5 · Excitement 3/5 · Architectural Fit 4/5 · Feasibility 4/5
**Confidence-modified %:** 52.8% (STRONG DIFFERENTIATOR)
**No. 1 Test:** 4/7 passed *(fails Q3 wow-moment, Q5 defining-feature, Q6 developer-magnet — solid Top 10 entry, correctly not promoted to a Top 3 role; see §6 note below)*

---

## 6. Recommended Bets

*By raw confidence-modified % the order is Accreditation Autopilot (72%) > Course Build Graph (66%) > Psychometric GATE Trainer (52.8%) > Proof-Carrying Animation Compiler (51.6%) — but the top 3 by score don't cleanly fill three distinct roles. Psychometric GATE Trainer passed the No. 1 Test at only 4/7, failing precisely the wow-moment (Q3), defining-feature (Q5), and developer-magnet (Q6) questions the #3 role needs; Proof-Carrying Animation Compiler passed 6/7, including a clean YES on all three of those. **Promoted explicitly:** Animation Compiler fills #3 Developer Magnet; Psychometric GATE Trainer stays a strong Top 10 entry (see §6 above) but is not one of the three bets.*

### #1 THE SIGNATURE FEATURE — Accreditation Autopilot
The pipeline that turns NBA/AICTE program accreditation from a hand-compiled, per-course, once-every-three-years scramble into a continuously-drafted, cross-course, dry-run-audited filing. The single idea most likely to make someone choose this template over any alternative — because no alternative in this category addresses this pain at all.

### #2 THE STRATEGIC MOAT — Course Build Graph
A deterministic dependency graph over the Symbol Reference / passport / derived-artifact relationships this repo already tracks by hand across three separate skills. Gets strictly harder to copy the more courses and weeks accumulate, because the moat *is* the accumulated ground-truth data, not the mechanism.

### #3 THE DEVELOPER MAGNET — Proof-Carrying Animation Compiler
The one feature on this list built to be shared, screenshotted, and forked-just-to-try. Closes the loop between the repo's own completed literature review and a working system, with the source-grounding guarantee as the durable differentiator once raw video generation is commoditized elsewhere.

---

## 7. Build Strategy

### #1 Accreditation Autopilot
- **Phase 1 — PoC:** Manually roll up CS401 + CS301's existing `co-po-attainment.tex` files into one hand-assembled program-level document; confirms the rollup arithmetic and formatting before any automation.
- **Phase 2 — MVP:** `/accreditation-autopilot <program>` skill that automates the rollup mechanically (Read + Write only, no new agent yet).
- **Phase 3 — Differentiation:** Add the `nba-assessor` cold-persona agent (dry-run critique before real submission) and the Regulatory Diff phase (drift-check against an uploaded NBA circular, reusing `textbook-edition-diff`'s pattern).
- **Phase 4 — Platform:** Spin the compliance layer out discipline-agnostically (§3 idea #17) so Mechanical/Civil/Electrical departments at the same or other institutions can fork just this layer — deferred to real demand, not built speculatively.

### #2 Course Build Graph
- **Phase 1 — PoC:** A single-purpose script that parses `knowledge-base-CS401.md`'s Symbol Reference table and greps `Slides/CS401/*.tex` for each symbol's first real use, flagging any mismatch against the declared "Introduced" week — validated by hand against one already-known-correct week and one deliberately-seeded violation.
- **Phase 2 — MVP:** Wire the checker into `check-surface-sync.sh` as an advisory (warn-only) gate.
- **Phase 3 — Differentiation:** Generalize `passport.yaml`'s mechanism into a queryable node; add the provenance-aware diff view (which derived artifacts go stale when a source changes).
- **Phase 4 — Platform:** Expose the graph as a queryable CLI (`scripts/build-graph.py query <symbol>`) other skills call instead of re-deriving relationships independently.

### #3 Proof-Carrying Animation Compiler
- **Phase 1 — PoC:** Take one already-authored `trace-execution` step sequence (CS301 Week 1 stack-growth steps), manually stitch the existing SVGs into a silent animated GIF with `ffmpeg`, confirming the toolchain works in this Windows/MiKTeX environment before any skill automation.
- **Phase 2 — MVP:** `/render-lecture-video` skill automating PoC's manual steps, output = silent animation + synced on-screen captions (no audio TTS in v1).
- **Phase 3 — Differentiation:** Add the CoVe-style narration-fidelity check (every caption sentence must trace to the source deck) — the actual differentiator versus generic AI-video tools.
- **Phase 4 — Platform:** Chain with `student-simulator` for automated pre-release comprehension QA (§5 X4) once the base compiler is proven.

---

## 8. What NOT To Build

- **NBA/AICTE Compliance Template Tier (discipline-agnostic spinout, §3 #17).** Confidence-modified 38.4%, No. 1 Test ~3/7. Real strategic value but premature as a standalone bet — correctly belongs as Accreditation Autopilot's own Phase 4 (Platform), not a separate bet competing for scarce build attention now.
- **Student-Facing "Explain This Grade" Receipt (§3 #15 / C6).** Confidence-modified 59% but No. 1 Test 2/7 — easy to replicate (just exposes data already computed), not a wow moment, not a defining feature. A genuine improvement, but shaped like a `/feature-discovery` quick win, not a category-defining bet; recommend filing there instead.
- **Hard-gated accreditation pre-commit (§5/contrarian X2).** Confidence-modified 38.4%, No. 1 Test ~1/7 standalone. Real and useful, but only as a hardening add-on inside Accreditation Autopilot's Phase 3 — not enough differentiation on its own to be a bet.
- **Cross-Institution NBA Benchmark Network (§3 #11).** Confidence-modified 28% — below the 35% floor, driven by low Feasibility: this genuinely requires real external institutional buy-in and data-sharing trust design that this skill cannot validate (no WebSearch/WebFetch, no market research). Tagged STRATEGIC HYPOTHESIS; good Phase-4 idea for Accreditation Autopilot once real multi-institution adoption exists, not before.
- **GATE PYQ Provenance Registry as a Public Good (§3 #18).** Confidence-modified 40.8%, No. 1 Test ~1-2/7 — a genuinely useful ecosystem contribution but not a wow/defining/shareable bet on its own; more of a documentation/publishing task than an innovation.
- **Toolchain Doctor (§3 #16).** Confidence-modified 43%, No. 1 Test 0/7 — real, evidenced pain (`TROUBLESHOOTING.md`, the LaTeX-toolchain-paths MEMORY entry) but this is squarely a `/feature-discovery`-shaped maintenance fix, not a category-defining bet; explicitly out of scope for this skill by its own stated boundary.
- **Multi-tenant course-fork isolation (§3 #8).** Confidence-modified 38.4%, No. 1 Test ~1/7 — a reasonable engineering-hygiene improvement now that CS301 is mid-buildout, but not differentiated, not exciting, not a moat.
- **Executable Formula-Lineage Graph (§3 #21 / §5 X5).** Confidence-modified 31.6% — below the 35% floor on Feasibility (2/5): this is genuinely substantial new symbolic-modeling engineering, not a small extension of `/verify-symbolic`. Tagged MOONSHOT and kept in §5 as a real long-horizon research direction, not rejected on merit — just not buildable at this run's confidence level.
- **Live "ask the auditor" kiosk (§5 X3).** Not scored — kept as a Crazy-but-Plausible entry only. The trust-boundary question (an external, real NBA assessor querying repo-internal data live) needs institutional sign-off this skill cannot obtain; a genuine idea, deliberately not converted into a scored bet.
- **Schema-as-source inversion for Accreditation/CompetitiveExam content (§5 X1).** Kept Crazy-but-Plausible only — directly contradicts CLAUDE.md's own "Beamer is authoritative" rule, which is a real, documented project decision, not an oversight; would need an explicit owner decision to revisit, the same posture `v2.0-backlog.md` already uses for other scope calls.
