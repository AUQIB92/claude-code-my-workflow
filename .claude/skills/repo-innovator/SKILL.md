---
name: repo-innovator
description: Discover the one or two innovations that could make a repository category-defining — not a feature backlog, a bet on what would make competitors struggle to catch up. Deep-models the repo (architecture, dependencies, workflows, latent capabilities), then runs a disciplined diverge (20+ ideas across 10 lenses) → combine (5+) → contrarian (5+) → converge pipeline, scores every survivor (Novelty/Impact/Differentiation/Defensibility/Excitement/ArchFit), and cuts hard via a 7-question "No. 1 Test" down to 2-3 recommended bets. Use when user says "what would make this project category-defining", "find our moonshot feature", "how do we beat the competition", "what's our unfair advantage", "innovative features to make this No. 1", or invokes `/repo-innovator`. NOT a feature backlog or gap-filling tool (use `/feature-discovery` for evidence-grounded maintenance/quick-wins/Not-Recommended-Yet triage) — this skill explicitly refuses generic features (dark mode, notifications, dashboards, analytics, caching, profiles, search, mobile apps) unless strategically justified, and is optimized to produce fewer, bolder ideas, not a prioritized backlog.
argument-hint: "[quick | moonshot | competitor | ai-native | research | moat | build \"<feature name>\"]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write"]
effort: high
disable-model-invocation: true
---

# Repo Innovator

Answer one question: **given what this repository actually is, what could we build that would make it significantly more useful, technically impressive, differentiated, defensible, and hard for competitors to ignore?**

This is not a feature checklist. Reject the obvious. Optimize for **fewer, radically better** ideas — the whole pipeline exists to cut a large candidate pool down to 2-3 real bets, not to pad a backlog.

**Which mode do I want?**
- The full pipeline, all lenses, real bets → **default** (no flags).
- Fast pass, fewer candidates → `quick`.
- Lean into the craziest-but-plausible ideas → `moonshot`.
- Lean into "what do all competitors assume, and how do we invert it" → `competitor`.
- Reimagine the repo as built AI-native from scratch → `ai-native`.
- Lean into publishable, research-grade ideas → `research`.
- Lean into hard-to-copy, compounding advantage → `moat`.
- Turn one already-found idea into a build spec → `build "<feature name>"`.

Default with no flags is always the full pipeline. Never ask which mode if a flag is given; only ask (`AskUserQuestion`) when `build` names a feature that can't be found or reasonably inferred (see **Interaction Design**, implicit in Mode: build below — this skill has no other blocking case, since Phase 0 always has enough repo signal to proceed).

---

## Modes

| Mode | Flag | Emphasis vs. default | Output shape |
|---|---|---|---|
| Full pipeline (default) | *(none)* | All 10 lenses, full diverge/combine/contrarian quotas | Full 8-section report, Top 10 → Top 3 |
| Quick | `quick` | Same pipeline shape, lower quotas (10 diverge / 3 combine / 3 contrarian) | Top 5 only, no full dossiers — see Mode: quick |
| Moonshot | `moonshot` | Phase 1C (Contrarian) gets the largest share of ideas; Phase 1A/B compressed | Report biased toward MOONSHOT-tagged bets |
| Competitor | `competitor` | Lens 2 (Competitor Inversion) drives most of Phase 1A | Report emphasizes competitive-inversion framing throughout |
| AI-native | `ai-native` | Lens 6 (AI-Native Transformation) drives most of Phase 1A | §1 "Tomorrow" section reframes the repo as built AI-native today |
| Research | `research` | Lens 10 (Research Frontier) drives most of Phase 1A | Every surviving idea also gets an explicit RESEARCH FRONTIER sub-tag where applicable |
| Moat | `moat` | Lens 9 (Defensibility) is the primary filter, not just one of six scoring dimensions | Top 3 all justified primarily on defensibility, not just score |
| Build | `build "<feature name>"` | Skips Phase 0/1/2 entirely for a named, already-found feature | One implementation spec, not a report — see Mode: build |

---

## Phase 0 — Deep Repository Intelligence

Read-only. Reuse the generic, any-stack recon procedure `/feature-discovery`'s Phase 0 already establishes (manifests, CI config, API/schema defs, structure map, development signals, git signals — see [`feature-discovery/SKILL.md`](../feature-discovery/SKILL.md#phase-0-repository-recon) for the mechanics; don't re-derive them here). This skill's model needs more than that recon produces, though — close Phase 0 by explicitly answering, in an in-context **Repository Intelligence Model** (not saved standalone; feeds Phase 1 directly):

1. What problem the project solves, and for whom (CONFIRMED if the README states it, ARCHITECTURAL INFERENCE otherwise).
2. What makes it technically unique — the two or three things a generic version of this project category would not have.
3. What architectural primitives exist (agents, events, logs, graphs, plugin points, execution engines, data models) — list them, don't just note their presence.
4. What capabilities are *partially* present — half-wired, underused, or built for one purpose but structurally capable of more.
5. What extension points exist (documented customization patterns, template files, plugin hooks).
6. What data the system observes or generates as a side effect of normal operation (logs, telemetry, structured output, history) — this is the raw material Lens 1 and Lens 8 need.
7. What workflows users actually perform, as chains (mirrors `/feature-discovery`'s Key Workflows section).
8. What constraints limit the project today (stack, licensing, scale, domain).
9. What the project's category is, and who the 2-4 most obvious comparable projects/approaches are (for Lens 2 — best-effort, WebSearch/WebFetch are not in this skill's tool set, so ground this in what the repo's own docs/README say about its positioning, not external research).
10. What would plausibly become a strategic advantage if pushed further — a first hypothesis, not a conclusion; Phase 1 does the real work.

---

## The 10 Lenses

Used as generation aids in Phase 1A, not a rigid per-lens quota — some ideas will draw on two or three lenses at once, some lenses may contribute nothing for a given repo, and that's fine.

| # | Lens | The provocation |
|---|---|---|
| 1 | Architectural Superpowers | What can this architecture already do that the project isn't exploiting? (Existing capability A + existing capability B + a new abstraction C = a possibly-unique feature D.) |
| 2 | Competitor Inversion | What does every comparable project assume — manual config, reactive behavior, human-only interfaces, opaque internals — and what happens if this repo does the opposite? |
| 3 | Magic Moment | Where's the moment a user thinks "I didn't know this was possible"? Frame as Input → System Intelligence → Unexpected Valuable Outcome. |
| 4 | 10× Features | Not "what feature should we add" but "what would make this 10× better for its single most important user" — autonomy, self-optimization, prediction, zero-config, simulation. |
| 5 | Cross-Domain Transfer | What powerful concept from OS design, distributed systems, compilers, cryptography, game engines, or observability could transform this repo if imported? |
| 6 | AI-Native Transformation | If this repo were designed today, AI-native from day one, what would be fundamentally different? (Not "add a chatbot.") |
| 7 | Developer Love | What would make a developer say "I never want to use the alternative again" — debugging, visual understanding, reproducibility, one-command workflows? |
| 8 | Network Effects | What makes the repo more valuable as more people use it — shared workflows, templates, benchmark sharing, interoperability? Only if it genuinely fits; don't force it. |
| 9 | Defensibility | Could a competitor copy this in one weekend? Prefer ideas that compound: accumulated intelligence, unique data, ecosystem lock-in, protocol/research advantages. |
| 10 | Research Frontier | Could an emerging concept — agent memory, multi-agent coordination, formal verification, zero-knowledge proofs, causal reasoning — become a practical feature here, not just a paper? |

---

## Phase 1 — Diverge → Combine → Contrarian

**Single continuous reasoning pass — deliberately not a parallel fan-out.** Unlike `/feature-discovery`'s 5-persona fan-out (independent lenses mining *different* repo evidence, reduced afterward), this pipeline's Combine step requires holding the *entire* Diverge candidate set in view at once to pair ideas across lenses — fragmenting the 10 lenses across independent forks would break the one step that makes this methodology worth running. Run this directly in the invoking context, not inside a spawned `Task`/fork subagent — **subagents cannot call `Write`** (confirmed by direct testing; a spawned agent's own report-save attempt is refused regardless of subagent type), so only the top-level session can actually persist §7's report. If you need to keep the ~20+ candidate ideas' worth of intermediate reasoning out of a longer-running parent conversation, do the reasoning in a fork and have it **return the full report as text** in its final message, then have the parent `Write` it — never have the fork attempt the save itself (see **Cross-references**).

**A. Diverge.** Generate at least 20 candidate ideas (10 in `quick` mode), spanning six categories: AI-Native Opportunities, Architectural Innovations, Product Moonshots, Developer Experience Breakthroughs, Ecosystem Opportunities, Research Frontier Ideas. Use the 10 lenses above as generation aids. Do not rank or filter yet — quantity and range are the point of this step.

**B. Combine.** Generate at least 5 ideas (3 in `quick` mode) by explicitly pairing or tripling Diverge candidates: `existing capability A + existing capability B + new abstraction C = combined idea D`. Show the combination, not just the result — the reasoning is part of the idea's evidence.

**C. Contrarian.** Generate at least 5 ideas (3 in `quick` mode): the craziest idea that remains *technically plausible* for this specific repo. Bounded by plausibility, not by convention — but never propose something with no technical path from here to there.

**Anti-Generic Rule (applies throughout A/B/C).** Reject outright — do not even list — dark mode, notifications, analytics, mobile apps, caching, user profiles, generic dashboards, or generic search, unless the idea clears all four questions in **Anti-Generic Rules** below. If it can't, cut it in Diverge — don't let it survive to Combine or Contrarian hoping it improves.

---

## Phase 2 — Score, Test, Converge

**Score every idea that survived Phase 1** on seven 1-5 dimensions: Novelty, User Impact, Strategic Differentiation, Architectural Fit, Defensibility, Developer Excitement, and Technical Feasibility. The first six feed the weighted Innovation Score below; Technical Feasibility feeds the confidence modifier instead.

```
Innovation Score (raw, max 5.0) =
    (Novelty × 0.25) + (User Impact × 0.20) + (Strategic Differentiation × 0.20)
  + (Defensibility × 0.15) + (Developer Excitement × 0.10) + (Architectural Fit × 0.10)

Innovation % = (Innovation Score / 5) × 100

Confidence-modified % = Innovation % × (Technical Feasibility / 5)
```

Band the **confidence-modified %**:

| Band | Classification |
|---|---|
| 80–100% | MOONSHOT WORTH BUILDING |
| 65–79% | STRATEGIC BET |
| 50–64% | STRONG DIFFERENTIATOR |
| 35–49% | USEFUL ENHANCEMENT |
| Below 35% | DO NOT PRIORITIZE |

**The No. 1 Test.** For every idea scoring 35% or above, answer 7 yes/no questions:
1. Would this make someone choose this project over alternatives?
2. Would competitors need significant work to replicate it?
3. Does it create a memorable "wow" moment?
4. Does it leverage something unique about this repository?
5. Could it become a defining feature of the project?
6. Would developers discuss, share, or demonstrate it?
7. Does it create a new capability rather than merely improving an existing one?

**Fewer than 4 YES → reject or downgrade to §8 (What NOT to Build), regardless of Innovation Score.** The test is a hard filter, not one more input to average in.

**Converge.**
- Everything clearing the No. 1 Test → ranked by confidence-modified % → **Top 10** (report §4). In `quick` mode, Top 5 instead, and skip the full dossier template (see Mode: quick).
- From the Top 10, select exactly **3** for §6 Recommended Bets, filling three fixed roles — **not** simply the top 3 by score:
  - **#1 Signature Feature** — the single idea most capable of defining the project publicly.
  - **#2 Strategic Moat** — the idea that becomes *harder* to copy the longer it exists (compounding, not static, defensibility).
  - **#3 Developer Magnet** — the idea most likely to make developers adopt, discuss, or contribute because of it specifically.
  If the top 3 by raw score don't cleanly fill distinct roles, promote the next-highest idea that does fit the empty role, and say so explicitly — a role mismatch is worth surfacing, not silently overridden.
- Everything that scored below 35%, or failed the No. 1 Test, or was rejected by the Anti-Generic Rule with a real reason worth recording → §8, each with its specific disqualifying reason.

**Tag every surviving idea's confidence** (see **Evidence and Confidence**) and cite repo evidence for anything not tagged MOONSHOT.

---

## Output Format

```markdown
# Repository Innovation Report

## 1. What This Project Could Become
TODAY: [what it currently does, grounded]
TOMORROW: [the most ambitious *plausible* future version]
THE DIFFERENCE: [the strategic transformation required to get there]

---

## 2. Repository Superpowers
For each strongest existing technical asset:
**Existing Asset** → **Untapped Potential** → **Possible Innovation**

---

## 3. Innovation Landscape
(At least 20 ideas total, before filtering — 10 in `quick` mode.)
### AI-Native Opportunities
### Architectural Innovations
### Product Moonshots
### Developer Experience Breakthroughs
### Ecosystem Opportunities
### Research Frontier Ideas

---

## 4. Top 10 Category-Defining Features
(Top 5 in `quick` mode; abbreviated per Mode: quick.)
One dossier per surviving idea, in confidence-modified-% order:

### <Feature Name>
*One-line vision.*
**Confidence:** Confirmed Opportunity / Architectural Inference / Strategic Hypothesis / Moonshot
**The Problem**
**The Insight**
**Why Existing Alternatives Don't Do This**
**Why This Repository Can**
**Architecture Impact** — likely modules affected; implementation concept.
**Magic Moment** — `Developer runs: <command/input>` → `System automatically: <unexpected valuable outcome>`
**Why It Could Matter**
**Innovation Score:** Novelty X/5 · Impact X/5 · Differentiation X/5 · Defensibility X/5 · Excitement X/5 · Architectural Fit X/5 · Feasibility X/5
**Confidence-modified %:** X% (band)
**No. 1 Test:** X/7 passed

---

## 5. The Crazy but Plausible Ideas
5 ideas. For each: what it does · why it sounds crazy · why it's technically possible · what experiment could validate it.

---

## 6. Recommended Bets
Exactly 3, in fixed roles:
### #1 THE SIGNATURE FEATURE
### #2 THE STRATEGIC MOAT
### #3 THE DEVELOPER MAGNET

---

## 7. Build Strategy
For each of the Top 3:
### Phase 1 — Proof of Concept (smallest experiment that validates the idea)
### Phase 2 — MVP (minimum useful implementation)
### Phase 3 — Differentiation (what competitors are unlikely to have)
### Phase 4 — Platform (how this could create an ecosystem)

---

## 8. What NOT To Build
Mandatory. Every idea that sounded attractive but didn't clear the bar — Anti-Generic Rule, No. 1 Test, or score — with the specific disqualifying reason.
```

Save to `quality_reports/repo_innovator_<repo-slug>_<YYYY-MM-DD>/REPORT.md` if `quality_reports/` exists at the target repo's root; otherwise `./REPO_INNOVATION_REPORT.md`. Print §6 (Recommended Bets) to chat regardless of where the full report was saved.

---

## Mode: quick

Same pipeline shape, lower quotas: 10 Diverge / 3 Combine / 3 Contrarian. Skip §2 (Superpowers) and the full §4 dossier template — instead, one ranked table (Feature | Confidence | Confidence-modified % | No.1 Test score | One-line why). Still produces §6 Recommended Bets and §8 What NOT to Build in full — convergence discipline never gets skipped, only the exposition around it.

## Mode: moonshot

Phase 1C (Contrarian) target raised to at least 10 ideas; Phase 1A/B quotas may compress to make room. §5 (Crazy but Plausible) effectively absorbs most of §4. Every Top 3 pick should be justifiable primarily by novelty and magic-moment strength, not safety.

## Mode: competitor

Phase 1A leans on Lens 2 (Competitor Inversion) for the majority of candidates: name the category's dominant assumption, then generate the inversion. §1's "The Difference" section should read as a direct contrast against the named comparables from Phase 0's intelligence model, point 9.

## Mode: ai-native

Phase 1A leans on Lens 6. §1's "Tomorrow" section is reframed as "if this repository were designed today, AI-native from the start" rather than an incremental addition — the test for every idea in this mode is whether it could exist at all in a non-AI-native version of the repo.

## Mode: research

Phase 1A leans on Lens 10. Every surviving idea that draws on a named research concept (agent memory, formal verification, zero-knowledge proofs, causal reasoning, multi-agent coordination, etc.) gets an explicit **RESEARCH FRONTIER** sub-tag alongside its confidence tag, and §7's Phase 1 (Proof of Concept) should read as an actual experiment design, not just a code spike.

## Mode: moat

Lens 9 (Defensibility) becomes the primary filter applied *before* scoring, not just one of six weighted dimensions — an idea that would score well but that a competitor could plausibly replicate in a weekend is dropped in Phase 1, not merely scored lower. §6's role selection should show real separation between #1 (Signature) and #2 (Moat) — if they'd be the same pick, that itself is worth stating as a finding.

## Mode: build "\<feature name\>"

Skips Phase 0/1/2. Locate `<feature name>` in the most recent `quality_reports/repo_innovator_*/REPORT.md`'s §4 or §6; if found, expand that dossier. If no prior report exists, or the name isn't found, run a lightweight Phase 0 plus a single-idea version of Phase 1A/B focused only on the named feature before proceeding — never fabricate a dossier that was never actually reasoned through.

Produce a full implementation spec: Problem, Insight, Architecture Impact (real modules/files), a build plan reusing §7's exact four-phase shape (PoC → MVP → Differentiation → Platform) scoped to this one feature, and Acceptance Criteria per phase. Save to `quality_reports/repo_innovator_specs/<feature-slug>.md` (or `./<feature-slug>-spec.md` if no `quality_reports/` exists). If the named feature genuinely can't be identified or reasonably inferred, ask via `AskUserQuestion` rather than guessing — this is the one case in this skill where Phase 0's recon alone isn't enough to proceed.

---

## Anti-Generic Rules

Dark mode, notifications, generic analytics, mobile apps, caching, user profiles, generic dashboards, and generic search are rejected by default in Phase 1 (Diverge/Combine/Contrarian). The only way one survives is clearing all four:
- **WHY THIS PROJECT** — what specific, cited fact about this repo makes the generic-sounding feature actually strategic here?
- **WHY NOW** — why does this repo's current state make this the right moment?
- **WHY HARD TO COPY** — what stops a competitor from shipping the same thing next week?
- **WHAT MAKES THIS EXCITING** — the magic-moment framing (Lens 3), not a feature-list bullet.

---

## Evidence and Confidence

Every idea carries exactly one tag:

- **CONFIRMED OPPORTUNITY** — directly supported by repository evidence (a file, a config, a documented workflow).
- **ARCHITECTURAL INFERENCE** — strongly supported by existing architecture, not stated outright.
- **STRATEGIC HYPOTHESIS** — requires market or user validation this skill cannot perform (no WebSearch/WebFetch in this skill's tool set — ground competitive claims in what the repo's own docs say about its positioning, don't invent market research).
- **MOONSHOT** — technically plausible, requires real experimentation; never presented as more certain than that.

Cite files/modules/APIs/dependencies for every tag except MOONSHOT. Never present a STRATEGIC HYPOTHESIS or MOONSHOT as settled fact.

---

## Interaction Design

Never ask which mode is wanted if a flag was given, and never ask permission to *read* the repo. The one legitimate blocking case is `build "<feature name>"` when the name can't be found in a prior report and isn't reasonably inferable — see that mode's own instruction. Every other mode always has enough signal from Phase 0 to proceed without a clarifying question.

---

## What This Skill Does NOT Do

- **Never edits or writes to the target repository's source.** `Write` is scoped to this skill's own report/spec files, in every mode.
- **Never produces a prioritized maintenance backlog.** Quick wins, doc fixes, dependency bumps, and gap-filling triage are `/feature-discovery`'s job, not this skill's — if Phase 1 generates something that shape, it belongs in §8, not §4.
- **Never presents a MOONSHOT or STRATEGIC HYPOTHESIS tag's speculation as settled fact**, in the report or in chat.
- **Never runs external market research.** STRATEGIC HYPOTHESIS ideas are labeled as needing validation this skill cannot itself perform.
- **Does not run tests, builds, or the target repo's code.** Analysis is static (Read/Grep/Glob/read-only Bash) throughout.

---

## Examples

**1. Full pipeline on an unfamiliar repo:**
> User: "what would make this project category-defining?"
> → `/repo-innovator` (default). Full 10-lens diverge/combine/contrarian pass, Top 10 → Top 3 Recommended Bets.

**2. Bias toward the boldest possible ideas:**
> User: "/repo-innovator moonshot"
> → Contrarian phase gets the largest ideas share; §6 picks lean on novelty over safety.

**3. Turn a prior finding into a build spec:**
> User: "/repo-innovator build \"Universal Verification Passport\""
> → Looks for that name in the latest `quality_reports/repo_innovator_*/REPORT.md`; if found (e.g. it was proposed as a Signature Feature bet), expands it into a full Problem/Insight/Architecture/4-phase-build/Acceptance-Criteria spec, saved to `quality_reports/repo_innovator_specs/universal-verification-passport.md`.

---

## Cross-references

- [`.claude/skills/feature-discovery/SKILL.md`](../feature-discovery/SKILL.md) — the sibling evidence-grounded backlog skill; reuses this skill's Phase 0 recon mechanics by reference, and its mandatory not-recommended-section pattern (§8 here), but explicitly does not overlap in output shape — see the frontmatter `description` boundary on both skills. Its own Phase 2 "Save" step is the correct precedent this skill follows: the *orchestrating* context writes the report, forked lenses only ever return text.
- [`.claude/skills/new-skill/SKILL.md`](../new-skill/SKILL.md) — the scaffolding conventions this file follows.
- [`.claude/skills/deep-audit/SKILL.md`](../deep-audit/SKILL.md) — another confirming precedent: its 4 spawned audit agents only ever report findings as text (Phase 1); the orchestrator itself applies every fix (Phase 3) — no spawned agent in that skill ever calls `Write` either.
- [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — the fan-out/reduce primitive this skill *deliberately does not use* for ideation: Phase 1's Combine step needs the full Diverge candidate set in view at once, which independent parallel forks would fragment. Documented here so a future consistency audit doesn't read the absence of `Task` as an oversight — and so the no-subagent-Write constraint (see Phase 1) doesn't get silently reintroduced by a future edit that adds `context: fork` back.
