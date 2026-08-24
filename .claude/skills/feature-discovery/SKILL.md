---
name: feature-discovery
description: Deeply analyze a software repository — any stack, any domain — and produce a prioritized, evidence-grounded report on what to build next. Reasons as five combined personas (Senior Architect, Staff Engineer, PM, Security/Quality Reviewer, Open-source Maintainer): inventories what exists, traces what's stubbed/dead/underutilized, and scores candidate features on impact/value/fit vs. effort/risk. Use when user says "what should we build next", "find feature opportunities", "audit this repo for gaps", "feature discovery", "what's missing from this codebase", "roadmap this project", or "generate GitHub issues for next features". NOT generic brainstorming — every recommendation must cite repo evidence and carry a Confirmed/Inferred/Speculative confidence tag. NOT for this repo's own academic-content gaps (use `/deep-audit` for infra consistency, `/course-arc-audit` for pedagogy) — this skill targets general software repos of any kind.
argument-hint: "[--quick | --deep] | --roadmap | --spec \"<feature name>\" | --issues [feature names...]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Task"]
effort: high
disable-model-invocation: true
---

# Feature Discovery

Analyze a repository the way a senior architect, a staff engineer, a PM, a security/quality reviewer, and an open-source maintainer would together — then hand back a prioritized, evidence-cited list of what to build next. Read-only against the target codebase in every mode: this skill never edits source files, only writes its own report files.

**Which mode do I want?**
- Just want the standard report → **Discovery** (default, no flags).
- Repo is huge / want a fast pass → `--quick`.
- Want git history, dependency graph, dead-code and coverage signals folded in → `--deep`.
- Already have a report and want milestones/phases/a dependency graph → `--roadmap`.
- Want one feature turned into a build-ready spec → `--spec "<feature name>"`.
- Want draft GitHub issues for specific features (never auto-filed) → `--issues [feature names...]`.

---

## Modes

| Mode | Flag | What it produces | Needs a prior report? |
|---|---|---|---|
| Discovery (default) | *(none)* | Full 7-section Feature Discovery Report + Top 5 | No — runs Phase 0 + Phase 1 (5-lens fan-out) + Phase 2 |
| Quick Analysis | `--quick` | Executive Summary + a single ranked opportunities table, no per-feature dossiers | No — runs Phase 0 only, single-pass reasoning |
| Deep Analysis | `--deep` | Same shape as Discovery, richer Phase 0 recon (git history, dependency listing, dead-code/coverage heuristics) | No |
| Roadmap | `--roadmap` | 4-phase roadmap + Mermaid dependency graph | Uses the latest report under `quality_reports/feature_discovery_*/` if one exists; otherwise runs Discovery first |
| Spec | `--spec "<feature name>"` | One feature's full build spec (problem, requirements, architecture, API/schema changes, acceptance criteria, tasks, tests) | Uses a prior report's dossier for that feature if found; otherwise reasons it fresh |
| GitHub Issue | `--issues [feature names...]` | Issue-ready markdown blocks for the named features (default: current Top 5) — **never posted to GitHub** | Same as Spec |

Default with no flags is always **Discovery**. Do not ask which mode the user wants if a flag is given or if none is needed to proceed — only ask (via `AskUserQuestion`) when a mode genuinely cannot proceed without more input (see **Interaction Design**).

---

## Phase 0 — Repository Recon

Runs in every mode. Single pass, no subagents — mechanical, cheap, deterministic. Build a **Repo Recon Brief** (in-context markdown, not a saved file) that Phase 1's lenses will receive verbatim so they don't each re-scan the repo from zero.

**1. Project understanding.** Read, where present: `README*`, `docs/`, `ARCHITECTURE*`, `CONTRIBUTING*`. Detect the stack generically from whichever manifest(s) exist — do not assume a language: `package.json`, `pyproject.toml`/`setup.py`/`requirements.txt`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`, `*.csproj`, `pom.xml`/`build.gradle`, etc. Also check `Dockerfile*`/`docker-compose*`, CI config (`.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`), DB schema/migration files (`prisma/schema.prisma`, `migrations/`, `alembic/`, `*.sql`), and API definitions (`openapi.y*ml`, `swagger.*`, route/controller files).

**2. Structure map.** Glob 2-3 directory levels deep. Heuristically classify what you find (frontend / backend / services / shared libs / infra / tests / docs) — state the classification as INFERRED, not fact, since directory names are a convention, not a guarantee.

**3. Existing-feature inventory.** Grep/glob for routes and API endpoints, UI pages/components, service or controller files, DB models/entities, CLI command definitions, event handlers, and third-party integrations. Every inventory row needs a file citation. **Do not assume a feature exists because a file exists** — open enough of each candidate to classify it as one of: `Complete`, `Partial`, `Experimental`, `Stubbed`, `Deprecated`, `Unclear`.

**4. Development signals.** Grep for `TODO|FIXME|HACK|XXX|NotImplemented(Error)?|not implemented|placeholder`. Look for empty function/method bodies, large commented-out blocks, feature-flag definitions (and whether the flagged code path is ever reachable), and routes/handlers that are registered but return a stub response.

**5. Git and issue signals.** If `.git/` exists: `git log --oneline -30` and `git branch -a` for direction-of-travel hints (do not treat commit-message intent as a shipped feature). If the `gh` CLI is available *and* configured for this repo, a light `gh issue list --limit 30` adds signal — probe once, degrade silently if it fails or isn't authenticated. Never assume GitHub tooling is present.

Close Phase 0 by writing the Repo Recon Brief inline: project purpose (1-2 sentences, tagged CONFIRMED if the README states it, INFERRED otherwise), stack, structure map, the feature inventory table, the development-signals list, and the git/issue summary. This brief is the shared input to every Phase 1 lens.

---

## Phase 1 — Five-Lens Fan-Out

Runs in Discovery and Deep modes (Quick mode skips this — see **Mode: Quick Analysis**). Five parallel forked subagents, `subagent_type: general-purpose`, launched as **five `Task` calls in a single message** (the fan-out primitive from [`orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — see also **Cross-references**). `general-purpose` is not tool-sandboxed (it has access to every tool), so each prompt below states the read-only constraint explicitly rather than relying on a hard sandbox — the same accepted trade-off `/seven-pass-review` already makes in this repo for its own lens fan-out.

Each of the five personas below owns a primary slice of the six discovery lenses from the user's original spec (User Workflow Gaps, Capability Expansion, Underutilized Infrastructure, Product Completeness, Developer Experience, Security & Reliability) so that all six get covered without needing six separate forks:

| # | Persona | Primary lens focus |
|---|---|---|
| 1 | **Senior Software Architect** | Capability Expansion (what the existing architecture makes easy to add); Underutilized Infrastructure; system boundaries, extension points, and existing abstractions that can carry new features |
| 2 | **Staff Engineer** | Developer Experience; technical debt/quality gaps that block future features; code-level Underutilized Infrastructure (unused DB fields, half-wired services) |
| 3 | **Product Manager** | User Workflow Gaps (incomplete journeys — registration → auth → dashboard → action → persistence → notification → history); Product Completeness (onboarding, settings, search, exports, collaboration) |
| 4 | **Security/Quality Reviewer** | Security & Reliability, **feature-shaped only** — audit logs, rate limiting, authorization gaps, backup/recovery, idempotency. Do not turn every hardening issue into a feature; only the ones that represent a meaningful, buildable improvement |
| 5 | **Open-source Maintainer** | Community/adoption-facing Product Completeness (docs, examples, SDKs); Developer Experience from a contributor's-eye view; contribution friction |

Each `Task` prompt must include: (a) the persona's one-paragraph framing, (b) its lens focus from the table above, (c) the full Repo Recon Brief from Phase 0, (d) the **anti-hallucination rules** verbatim (see below), and (e) an instruction to close its report with a fenced YAML block in this exact shape, one entry per proposed feature. Every entry names its own `lens` (one of the six discovery lenses, not the persona) so Phase 2 can classify Infrastructure-bin features mechanically rather than by re-judging the idea:

```yaml
feature_findings:
  - id: A1                        # persona-letter + sequence, e.g. A1, B2
    persona: "Senior Software Architect"
    lens: capability_expansion    # one of: user_workflow_gaps | capability_expansion |
                                   # underutilized_infrastructure | product_completeness |
                                   # developer_experience | security_reliability
    name: "Short feature name"
    confidence: INFERRED          # CONFIRMED | INFERRED | SPECULATIVE
    evidence: "src/auth/session.ts:42; README.md#L10-14"
    problem_opportunity: "..."
    why_it_fits: "..."
    leverages: ["src/auth/", "prisma/schema.prisma"]
    likely_areas: ["src/auth/rbac.ts (new)", "prisma/schema.prisma"]
    approach: "High-level technical approach, 2-4 sentences."
    dependencies: ["requires feature B2"]
    risks: ["breaking change to session token shape"]
    complexity: M                 # S | M | L
    scores:
      impact: 4
      user_value: 3
      strategic_alignment: 4
      architectural_fit: 5
      implementation_effort: 3
      technical_risk: 2
```

Wait for all five before Phase 2. If a lens's fork returns nothing usable (empty repo area for its focus, e.g. no security-relevant surface at all), that is a valid result — an empty `feature_findings: []` is fine and should not be treated as a fork failure.

---

## Phase 2 — Synthesize & Score

Reduce, don't re-review: read the five `feature_findings` blocks and stack them — do not re-derive feature ideas yourself in this phase.

**1. Dedupe.** Two lenses proposing the same underlying feature (e.g. Architect's "add RBAC" and PM's "add team permissions") are one feature with two supporting citations, not two rows. Multi-lens agreement is itself a (noted) confidence signal, but it never overrides a SPECULATIVE tag into CONFIRMED — only evidence does that.

**2. Score.** For every surviving feature, compute:

```
Priority Score = (Impact + User Value + Strategic Alignment + Architectural Fit)
                 − (Implementation Effort × 0.5 + Technical Risk × 0.5)
```

using the six 1-5 scores the lens already supplied (adjust only if synthesis evidence clearly contradicts a lens's self-score — note the adjustment and why).

**3. Classify.** Every feature gets exactly one bin, using this order (first match wins). All "top half" / "top third" / "bottom quartile" thresholds below are percentiles of Priority Score **within this run's feature set**, not fixed numeric cutoffs:

| Bin | Rule |
|---|---|
| **Quick Win** | Implementation Effort ≤ 2 AND Priority Score in the top half |
| **Strategic** | Implementation Effort ≥ 4 AND Architectural Fit ≥ 4 |
| **Infrastructure** | `lens: underutilized_infrastructure` |
| **Experimental** | Confidence = SPECULATIVE OR Technical Risk ≥ 4 |
| **High Priority** | Priority Score in the top third, not already classified above |
| **Not Recommended Yet** | Priority Score in the bottom quartile, OR an explicit disqualifier (needs a full rewrite, no evidence of user need, excessive complexity, premature scaling, conflicts with a stated project goal) |

Every run must populate **Not Recommended Yet** with at least the ideas that sounded attractive but didn't clear the bar — this section is mandatory output, never silently omitted (see Output Format §7).

**4. Assemble the report** in the exact structure under **Output Format**, then close with:

> **Top 5 Features to Build Next**
> For each: Feature · Why it matters · Priority score · Complexity · Recommended next action (e.g. "run `/feature-discovery --spec \"<name>\"`").

**5. Save.** If `quality_reports/` exists at the target repo's root, write to `quality_reports/feature_discovery_<repo-slug>_<YYYY-MM-DD>/REPORT.md`. Otherwise (this skill must work in repos with no such convention) write `./FEATURE_DISCOVERY_REPORT.md` at the target repo's root. Print the Top 5 to chat regardless of where the full report was saved.

---

## Output Format

```markdown
# Feature Discovery Report

## 1. Executive Summary
What the project is · current maturity · major strengths · biggest gaps · recommended development direction.

---

## 2. Repository Understanding
### Project Purpose
### Target Users
### Technology Stack
### Architecture
### Core Modules
Include a Mermaid architecture diagram only when the repo's structure is clear enough to draw one honestly — omit rather than guess.

---

## 3. Existing Feature Inventory
| Feature | Status | Evidence | Notes |
|---|---|---|---|
Status ∈ {Complete, Partial, Experimental, Stubbed, Deprecated, Unclear}.

---

## 4. Key Workflows
Major workflows found, as a chain (e.g. `User → Auth → API → Service → DB → Response`), with gaps/weak transitions called out.

---

## 5. Discovered Feature Opportunities
One dossier per feature, in Priority Score order:

### <Feature Name>
**Confidence:** Confirmed / Inferred / Speculative
**Problem / Opportunity** — the evidence, not just the idea.
**Why it fits this repository**
**Existing components it leverages**
**Likely implementation areas** — e.g. `src/auth/...`, `prisma/schema.prisma`
**Potential implementation approach** — high-level technical design.
**Dependencies**
**Risks**
**Estimated Complexity:** Small / Medium / Large
**Feature Scores:**
- Impact: X/5 · User Value: X/5 · Strategic Alignment: X/5 · Architectural Fit: X/5
- Implementation Effort: X/5 · Technical Risk: X/5
- **Priority Score: X**

---

## 6. Prioritized Feature Roadmap
### Phase 1 — Quick Wins
### Phase 2 — Core Product Expansion
### Phase 3 — Strategic Features
### Phase 4 — Experimental Opportunities

---

## 7. Features NOT Recommended
Mandatory section. Ideas that sound attractive but aren't justified yet, each with the specific reason (architecture not ready / no evidence of user need / excessive complexity / premature scaling / conflicts with project goals).
```

---

## Mode: Quick Analysis (`--quick`)

Skips Phase 1's fan-out entirely. Reason through all five lenses yourself, single pass, directly from the Phase 0 Repo Recon Brief. Output is short: Executive Summary + one ranked opportunities table (Feature | Confidence | Priority Score | Complexity | One-line why) — no per-feature dossiers, no Mermaid diagram. Still closes with Top 5. Use this when the repo is very large and a full fan-out would be disproportionate, or the user explicitly wants a fast read.

## Mode: Deep Analysis (`--deep`)

Same Phase 1/Phase 2 shape as Discovery, but Phase 0 gains:
- A deeper git scan (`git log --oneline -150`, `git log --stat -20` on the most-changed files) for direction-of-travel and churn hotspots.
- A full dependency listing parsed from the detected manifest(s) — flag notably outdated or abandoned dependencies as INFERRED risk signals, not as features themselves.
- Best-effort dead-code and test-coverage heuristics: grep for exported symbols with no in-repo references, and check for a coverage config/report if one exists. **State plainly that these are static-grep heuristics, not real profiling or coverage tooling** — never report a heuristic finding as CONFIRMED.

## Mode: Roadmap (`--roadmap`)

Look for the most recent `quality_reports/feature_discovery_*/REPORT.md`; if none exists, run Discovery mode first. Convert §6's four phases into milestones/epics, and add a Mermaid dependency graph built from each feature's `dependencies` and `likely_areas` overlap (two features sharing a likely implementation area are drawn as related, not necessarily dependent — only an explicit `dependencies` entry becomes a graph edge).

## Mode: Spec (`--spec "<feature name>"`)

Locate the named feature in the most recent report's §5 dossier if one exists; otherwise reason it fresh from a lightweight Phase 0 + single-lens pass. Produce, using this repo's own MUST/SHOULD/MAY requirements framing (see [`plan-first-workflow.md`](../../rules/plan-first-workflow.md)): problem statement, requirements (MUST/SHOULD/MAY), architecture, API changes, database/schema changes, acceptance criteria, implementation tasks, testing strategy. Save to `quality_reports/feature_discovery_specs/<feature-slug>.md` (or `./<feature-slug>-spec.md` if no `quality_reports/` exists).

## Mode: GitHub Issue (`--issues [feature names...]`)

For each named feature (default: current Top 5 if none named), generate one issue-ready markdown block:

```markdown
### Title
### Problem
### Proposed Solution
### Technical Scope
### Acceptance Criteria
### Files/Modules Likely Affected
### Testing Requirements
### Dependencies
```

**This mode only writes or prints markdown. It never runs `gh issue create` or otherwise posts to GitHub, and never should.** Filing issues is a visible, shared-system action; the user reviews the drafts and files them themselves. If asked to also file them, treat that as a distinct, separately-confirmed request, not part of this mode.

---

## Interaction Design

Default to Full Discovery with no clarifying questions whenever the repo has enough signal to proceed (a README, or enough source files to infer purpose) — this mirrors the rest of this repo's skills, which don't pause when the target is unambiguous. Only use `AskUserQuestion` when a mode genuinely cannot proceed:
- `--spec`/`--issues` named a feature that isn't in any prior report and isn't inferable with reasonable confidence from Phase 0 alone.
- `--roadmap`/`--spec`/`--issues` invoked with no prior report, no feature name, and Phase 0 alone doesn't give enough to reason about (e.g. an almost-empty repo).

Never ask "which mode do you want" if a flag was given, and never ask for permission to *read* the repo — reading is always in scope.

---

## Anti-Hallucination Rules

Every major feature recommendation carries exactly one confidence tag:

- **CONFIRMED** — evidence exists directly in the repository (a file, a line, a config value).
- **INFERRED** — the conclusion follows from strong architectural evidence but isn't stated outright (e.g. "auth exists and is JWT-based" → INFERRED that RBAC would slot into the existing middleware, even though no RBAC code exists yet).
- **SPECULATIVE** — plausible, but not directly supported by anything found in the repo. Speculative features are allowed but must be visibly rare and always land in Experimental or Not Recommended Yet.

Never claim that users need something, that the project supports something, that an API exists, or that a problem exists, unless repository evidence supports the statement. Cite file paths (and line numbers where practical) for every claim that can carry one. When a lens is genuinely uncertain, say so — an honest "couldn't determine from available evidence" beats a confident guess.

---

## What This Skill Does NOT Do

- **Never edits or writes to the target repository's source.** `Write` in `allowed-tools` is scoped to this skill's own report/spec files only, in every mode.
- **Never files GitHub issues** — `--issues` drafts markdown only (see that mode's safety note above).
- **Never recommends a full rewrite** unless the user explicitly asks for that framing — features are chosen for architectural leverage on what already exists.
- **Does not replace this repo's own internal audits** — for this repo's own infrastructure consistency use [`/deep-audit`](../deep-audit/SKILL.md); for its pedagogical continuity across weeks use [`/course-arc-audit`](../course-arc-audit/SKILL.md). `/feature-discovery` is for analyzing *any* software repository as a product/engineering surface, not for auditing this template's own conventions.
- **Does not run tests, builds, or the target repo's code** — analysis is static (Read/Grep/Glob/read-only Bash) in every mode.

---

## Examples

**1. Cold read of an unfamiliar repo:**
> User: "what should we build next in this repo?"
> → `/feature-discovery` (Discovery mode, no flags). Runs Phase 0, fans out the 5 lenses, produces the full report + Top 5.

**2. Large monorepo, want the fast version first:**
> User: "/feature-discovery --quick"
> → Phase 0 only, single-pass reasoning, one ranked table + Top 5. If the user then wants depth on one idea, follow with `--spec`.

**3. Turning a prior finding into a build-ready spec:**
> User: "/feature-discovery --spec \"webhook support\""
> → Looks for "webhook support" in the latest `quality_reports/feature_discovery_*/REPORT.md`; if found, expands that dossier into a full spec (requirements, architecture, API changes, acceptance criteria, tasks, tests) saved to `quality_reports/feature_discovery_specs/webhook-support.md`.

---

## Cross-references

- [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — the fan-out/reduce primitive this skill's Phase 1/Phase 2 reuses.
- [`.claude/references/orchestration-schemas.md`](../../references/orchestration-schemas.md) — the FINDING/SCORECARD/RUN_CONFIG pattern this skill's `feature_findings` schema is modeled on; it diverges (feature-scoring fields instead of severity-only) because this skill proposes features rather than grading an artifact against a pass/fail gate.
- [`.claude/skills/seven-pass-review/SKILL.md`](../seven-pass-review/SKILL.md) — closest structural sibling: parallel forked `general-purpose` lenses with inline persona prompts, synthesized into one report.
- [`.claude/skills/deep-audit/SKILL.md`](../deep-audit/SKILL.md) — closest sibling for a mechanical-recon-then-fan-out shape, applied to this repo's own infrastructure instead of a target codebase's product surface.
- [`.claude/skills/new-skill/SKILL.md`](../new-skill/SKILL.md) — the scaffolding conventions this file follows.
- [`.claude/rules/plan-first-workflow.md`](../../rules/plan-first-workflow.md) — the MUST/SHOULD/MAY requirements framing reused in Spec mode.
