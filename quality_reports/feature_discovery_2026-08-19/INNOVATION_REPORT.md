# Feature Discovery — Innovation / "Make This No. 1" Pass

**Target:** `D:\Academic-Workload\Academic-Skill` · **Frame:** competitive differentiation, not gap-filling
**Companion to:** `quality_reports/feature_discovery_2026-08-19/REPORT.md` (today's earlier maintenance-focused Discovery run — none of its 17 items are repeated here)
**Date:** 2026-08-19

---

## Executive Summary

Five lenses, explicitly instructed to ignore maintenance items and bet on genuine differentiation, converged on the same underlying thesis **independently**: this repo has already built more real AI-content-verification infrastructure than any comparable template (Chain-of-Verification citation checking, SymPy symbolic re-derivation, empirical algorithm execution, numeric-claim audits) — but every one of those verification results dies in a private, often-gitignored markdown report the moment the skill finishes. **The single highest-leverage move is not building new capability — it's making existing, real capability externally visible and durable.**

The strength of the signal: the Architect lens (working from the orchestration-runtime side) and the Security/Quality lens (working from the verification-skills side) independently proposed the same passport-ledger extension. The Architect, Security, and PM lenses independently proposed the same public trust-page mechanism. Three-lens convergence with no cross-talk between the forks is the strongest confidence signal this methodology can produce.

**The two ideas worth treating as one connected bet, in order:**
1. **Extend the passport** (currently paper-only, numeric-claims-only) to cover every claim type this repo already verifies — citations, symbolic derivations, algorithm correctness, pedagogy playtests — for lecture content, not just papers.
2. **Publish it.** A per-lecture "verification certificate" page, rendered via the exact marker-region mechanism `/publish-course-hub` already uses, showing a skeptical outsider (student, NBA/AICTE reviewer, prospective forker) real, honest, sometimes-unflattering verification state — not a marketing badge.

Everything else below is either a smaller, faster-paying bet (Socratic-check widgets, the onboarding wizard) or a bigger, longer-horizon one (a portable course-exchange format, a community domain-pack registry).

**One thing worth fixing in the next five minutes, found as a side effect of this run:** `gh api repos/AUQIB92/claude-code-my-workflow` shows `topics: []` and `is_template: false` — but `CHANGELOG.md` v2.1.0 claims topics were already set. The claimed fix never actually landed. See E4 below.

---

## Top 5 (Innovation Pass)

| # | Feature | Why it matters | Priority | Complexity |
|---|---|---|---|---|
| 1 | **Universal Verification Passport** | Generalizes a mechanism that already works (paper numeric-claims) to every claim type this repo verifies, for lecture content — the credibility backbone everything else builds on | 17 | L |
| 2 | **Interactive Socratic-Check widgets** | 32 already-authored "commit-then-reveal" blocks exist across CS401's decks; only 1 of 9 lectures ships them interactively. Zero backend, zero new authoring, pure delivery fix | 16.5 | M |
| 3 | **Profile-pruning onboarding wizard** | Removes the "clone all 913 files" adoption tax without touching the upstream-blocked plugin/marketplace path | 16 | M |
| 4 | **Public Verification Certificate** | The passport (above), made externally auditable — the actual "nobody else has this" claim, made checkable by a skeptic with zero tooling | 15.5 | M |
| 5 | **Per-student weak-CO remediation packets** | The grading pipeline already computes exactly which CO a student is weak on, then throws it away at `--tally`. Wiring it to the existing verified-question-generation skill is pure connection, not new capability | 15 | M |

---

## Full Feature List (Priority order)

### 1. Universal Verification Passport `[+2 lenses: Architect, Security/Quality]`
**Confidence:** Inferred · **Priority: 17**
The paper-only passport (`.claude/rules/replication-protocol.md:123-184`) tracks PASS/FAIL/EXPLAINED/STALE per numeric claim and is git-tracked (not gitignored) — the one `quality_reports/` artifact built to be durable. `/verify-claims`, `/verify-symbolic`, `/verify-algorithm`, and `/student-simulator` each independently re-derive/re-execute/re-answer a claim (the same CoVe-style independence trick, four times over) but each writes only a one-off report nobody cross-references. Extend the passport schema with a `claim_kind` field (citation | symbolic | algorithmic | pedagogy) and a `derivation_chain` field (which Quarto/Notes/InstructorHandouts copies inherit this claim, hashed, so translation-introduced drift in a *previously verified* claim gets caught — something `qa-quarto`/`qa-notes` parity checks don't catch today). Each verify-* skill gains an optional Phase-5b write-back. **Leverages:** `replication-protocol.md`, `templates/passport-template.yaml`, all four verify-* skills. **Risk:** schema sprawl if undisciplined; write-back must stay best-effort so it never blocks the underlying verification.

### 2. Interactive Socratic-Check widgets
**Confidence:** Inferred · **Priority: 16.5**
32 "Socratic Check" blocks exist across `Slides/CS401/*.tex` (all 9 built lectures); only `Quarto/CS401/08-io-techniques.qmd` ported the pattern into the deployed, interactive RevealJS site — everywhere else the ask-then-reveal structure is flattened into static slides on publish. Define a `.socratic-check` RevealJS component (question + localStorage-persisted answer box + reveal-only-after-commit button) in `Quarto/theme-template.scss`, roll out to lecture 05 (already has interactive precedent), verify via `qa-quarto`, then batch across the rest. No accounts, no server, no new content authoring — pure delivery of what's already written. **Leverages:** existing Socratic Check content, the 08 precedent, `translate-to-quarto`. **Risk:** `qa-quarto` parity checking has no rule for interactive elements yet — needs one.

### 3. Profile-pruning onboarding wizard (starter vs. full tier)
**Confidence:** Speculative · **Priority: 16**
À-la-carte skill packaging via `.claude-plugin/marketplace.json` is explicitly blocked and a documented non-goal (`v2.0-backlog.md:62-64`, upstream `anthropics/claude-code#11278`). But that blocker is specific to Claude Code's plugin *loader* — it says nothing about a plain file-system prune done once, at fork time, before Claude Code ever opens the repo. A new `/onboard` skill asks discipline + tier (starter: ~15 core skills vs. full: all 72), then a script deletes (or sparse-checkout-excludes) the rest and regenerates the surface-sync counts so the pruned repo still passes its own gates. Reuses `scripts/skill.py`'s existing frontmatter parser to compute the prune set — no second source of truth. **Risk:** destructive deletion has no undo unless sparse-checkout (reversible) is used instead of `rm`.

### 4. Public Verification Certificate `[+2 lenses: Architect, PM]`
**Confidence:** Speculative · **Priority: 15.5**
The natural publication of #1: a static per-lecture page (or a marker-bounded region on the existing course hub, via `/publish-course-hub`'s proven pattern) rendering the passport's claims table — kind, location, verdict, method, date — honestly, including STALE/UNVERIFIED rows shown as such, never hidden. This is the externally-checkable half of the credibility story; #1 without this stays an internal QA artifact. **Explicit design constraint carried over from the lens reports:** must never render an unverified claim in a way that reads as verified — the differentiator is honesty, not a marketing badge. **Depends on:** #1 shipping first with real data.

### 5. Per-student weak-CO remediation packets
**Confidence:** Speculative · **Priority: 15**
`/grade`'s per-question, per-CO detail exists in each student's draft report but is discarded at `--tally` (which only aggregates class-wide for NBA filing). A new skill reads one student's approved-score history, finds COs below threshold, maps them to topics via the CO blueprint `/accreditation` already derives, and calls `/competitive-exam-questions` (or `/scaffold-exercises`) scoped to just those gaps — a private, per-student PDF. Nothing here is new grading, new verification, or new CO taxonomy; it's three already-correct pieces wired together. **Risk:** must degrade gracefully (explicit "insufficient data" message) for low-enrollment courses like CS301's current 1/12-week state, not force a packet from thin data.

### 6. Named, citable verification methodology doc
**Confidence:** Speculative · **Priority: 15** · Complexity: S (near-zero cost)
The repo has independently reinvented the same principle four times (CoVe, SymPy re-derivation, execution-based checking, numeric audit) — each stated locally as "mirrors X" rather than named as one framework. Writing one `.claude/references/verification-methodology.md` — claim-type taxonomy, the shared non-negotiables (fresh/forked context, fail-closed, honest strength-grading, explicit INCONCLUSIVE over a forced verdict) — costs a single doc and makes #1/#4 *citable and adoptable* outside this repo, not just usable inside it. Ships regardless of whether #1/#4 do.

### 7. Community domain-pack registry
**Confidence:** Inferred · **Priority: 15**
`CONTRIBUTING.md:14-16` tells forkers to keep custom `domain-reviewer` content local ("PR back the template not the instance") — but `domain-reviewer.md` is explicitly a "template agent, customize for your field," and `discipline-cards.md` ships a literal copy-paste extension template. The result: psych/sociology/public-health cards are deferred indefinitely, bottlenecked on owner bandwidth (`v2.0-backlog.md:66-74`). A `community/domain-packs/<discipline>/` directory + a schema-only validator (reusing `check-skill-integrity.py`'s mechanical-check pattern — no subject-matter review required to merge) turns this into crowd-contributable breadth without the owner personally vetting sociology methodology. **Risk:** quality variance on mechanically-valid-but-substantively-weak packs; mitigate with a visible "community-contributed, not owner-vetted" label.

### 8. Skill Regression Harness
**Confidence:** Speculative · **Priority: 14**
Motivated by a real, already-documented incident: `.claude/references/model-versions.md:22` records 28/28 structured-tool-call failures on Fable 5's launch day, caught only because a human happened to notice in one session. A golden-fixture behavioral test suite (minimal artifact + RUN_CONFIG + structural assertions on the FINDING/SCORECARD contract) replayed against canary skills on every model bump would catch this class of regression mechanically instead of by luck. No comparable Claude Code project publicly ships this.

### 9. "Live reference week" showcase
**Confidence:** Speculative · **Priority: 14** · Complexity: S
A prospective forker has to read the full 70+-skill README or click through a whole course hub to judge output quality; `HelloWorld` is explicitly marked a throwaway sample, not a showcase. One `docs/index.html` section linking directly to one fully-shipped week's five artifacts (slides, notes, assignment, lab, GATE set) — chosen automatically via `publish-course-hub`'s own "is this week complete" scan, so it can't go stale by hand-typo — costs almost nothing and answers "what does finished output actually look like" in two minutes.

### 10. Orchestration Observatory (fan-out trace dashboard)
**Confidence:** Speculative · **Priority: 13.5**
Every fan-out skill already emits typed `FINDING`/`SCORECARD`/`RUN_CONFIG` blocks (`orchestration-schemas.md`) — and today's earlier report already confirmed the documented spend/round caps are prose-only, nothing persists a run. A trace viewer (retrofit 2-3 high-traffic skills first — `qa-quarto`, `deep-audit`, `seven-pass-review` — to write their stacked findings as JSON, then a small Artifact renders convergence timelines and lens-participation) would be the most demo-able proof the orchestration claim is real, not aspirational. Prerequisite for #14 below.

### 11. Self-service adopter showcase / institution registry
**Confidence:** Speculative · **Priority: 13.5** · Complexity: S
`README.md:433`'s "15+ research groups have forked and adapted this workflow" is unlinked prose with zero mechanism. An opt-in `adopters.yml` (name, institution, discipline, live-site URL) rendered into a `docs/showcase.html` gallery via a PR-based, schema-validated (not human-reviewed) flow replaces an unverifiable claim with a growing, linkable one. **Risk:** cold-start — needs the owner to seed 2-3 real entries at launch or an empty page looks worse than the current sentence.

### 12. Correction-to-Skill-Patch Loop
**Confidence:** Speculative · **Priority: 13**
72 skills exist but none improve from being corrected — every `[LEARN]` entry dead-ends in `MEMORY.md`'s prose index rather than patching the skill that caused the mistake (e.g. the `create-minor-paper` format correction lives only as an index pointer, never folded back into that skill's own file). Tag `[LEARN]` entries with the skill they correct; once a skill accrues ≥2 independent corrections (reusing the existing two-strikes convention from `summary-parity.md`), draft a proposed `SKILL.md` diff via a forked agent — always a plan-mode proposal, never auto-applied, respecting `orchestrator-protocol.md`'s explicit no-self-modifying-daemon boundary.

### 13. Fleet Introspection Loop
**Confidence:** Speculative · **Priority: 11**
A longer-horizon extension of #10: once traces persist, reduce them into per-agent/per-lens hit/hallucination rates and propose (never auto-apply) `model-routing.md` adjustments — turning the 70/20/10 policy from asserted to measured. Needs real run volume to be trustworthy; a slow-burn feature, not day-one value.

### 14. Spin out the skill-authoring toolkit as a standalone CLI
**Confidence:** Speculative · **Priority: 11**
`check-skill-integrity.py` + `new-skill`'s methodology are the least academic-specific pieces of infrastructure in the repo — genuinely useful to any Claude Code project, not just this one. Extracting them (refactor the hardcoded `REPO` path into a CLI arg, publish as a small pip/npx package) would put this template's engineering discipline in front of the entire Claude Code ecosystem, not just academics who find this fork. **Risk:** a second repo to maintain in sync.

### 15. Conformance badge + fix the GitHub topics gap
**Confidence:** Speculative (badge) / **Confirmed** (topics gap) · **Priority: 11**
**Immediate, ~5-minute fix, independent of everything else:** `gh api` confirms `topics: []` and `is_template: false` on the live repo, despite `CHANGELOG.md` v2.1.0 claiming topics were set — the claimed fix never landed. Setting topics + flipping `is_template: true` is a repo-settings change, not code. The larger badge feature (CI job re-running existing gate scripts on a schedule, emitting a shields.io-style "still conformant" badge forkers can embed) is real but secondary to just doing the trivial part now.

### 16. Portable Course Package
**Confidence:** Speculative · **Priority: 10.5**
A course-content-level (not skill-level) export/import format — bundle a whole `<CODE>`'s Slides/Notes/syllabus/Accreditation/knowledge-base-rule into a versioned archive another institution running this template could import and re-verify (not blindly trust) against their own PO set. Deliberately sidesteps the blocked plugin-packaging path since it never touches Claude Code's loader. **Largest scope item on this list** — effectively a mini package manager for course content; textbook-PDF copyright boundaries must be respected in the manifest.

### 17. Verified Isomorphic Assessment Variants
**Confidence:** Speculative · **Priority: 9.5**
Generate N structurally-equivalent exam variants (different numbers/scenario surface, same learning objective and difficulty) using the same SymPy/execution equivalence-checking `/grade` already relies on, to blunt AI-assisted take-home cheating. Genuinely novel, but "difficulty-equivalence" is mechanically well-defined only for Numerical/algorithmic problem types — overclaiming "verified equivalent" on Conceptual/Design problems would undercut the whole honesty-first credibility positioning the rest of this list depends on. Scope to closed-form/algorithmic problems only if built.

---

## Not Recommended (this pass)

- **Building the badge (#15) before fixing the topics gap** — the trivial fix should ship standalone, today, regardless of the larger feature's fate.
- **Isomorphic variants (#17) for Conceptual/Design problem types** — no mechanical ground truth exists for those; forcing a "verified equivalent" claim there conflicts with the honesty-first positioning every other item on this list depends on.
- **Fleet Introspection auto-applying routing changes (#13)** — must stay propose-only; auto-tuning model assignment without human sign-off is exactly the kind of autonomous self-modification `orchestrator-protocol.md` explicitly refuses.
