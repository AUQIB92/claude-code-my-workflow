---
paths:
  - ".claude/agents/**/*.md"
  - ".claude/skills/**/SKILL.md"
---

# Per-Agent Model Routing (architect/editor split)

**Match model tier to the cognitive demand of the work.** Reserve Opus for high-judgment work; route mechanical work to Haiku; default review/critique to Sonnet. Anthropic's [Apr 8 2026 "Decoupling brain from hands"](https://www.anthropic.com/engineering) endorses this pattern; Aider's architect/editor split is the canonical community shape.

## The 70/20/10 routing pattern

| Share | Tier | Use for |
|---:|---|---|
| ~70% | **Haiku 4.5** | Mechanical work — file renames, citation-format conversion, TikZ extraction, bib validation, proofread-fix application, simple grep / file lookups |
| ~20% | **Sonnet 4.6** | Review and critique — `r-reviewer`, `slide-auditor`, `proofreader`, `quarto-fixer`, `humanize-auditor` |
| ~10% | **Opus 4.8** | High-judgment work — `editor`, `methods-referee`, `domain-referee`, `claim-verifier`, `quarto-critic`, `tikz-reviewer`, `domain-reviewer`, `verifier` for non-trivial gates |

Set per-agent via `model:` in the agent's YAML frontmatter:

```yaml
---
name: quarto-fixer
model: sonnet      # was: inherit
---
```

Set per-skill via the same field in `SKILL.md` frontmatter. Inheritance is fine for skills whose work spans tiers (e.g., `/review-paper --peer` dispatches a mix).

## The effort axis (the first cost lever)

Model tier is the second cost lever; **effort is the first.** Every model runs at an effort level (`low / medium / high / xhigh / max`), and lowering effort is cheaper than dropping a tier — reach for it first.

- **Opus 4.8 defaults to `high`**, and its `high` does roughly what Opus 4.7's `xhigh` did, for fewer tokens. Do **not** reflexively set `xhigh`.
- **Mechanical work** (Haiku tier) → `low` / `medium`.
- **Review and judgment** (Sonnet / Opus) → `high` (the default).
- **The hardest runs** (deep refactors, the toughest `/review-paper --peer`) → `xhigh`; `ultracode` (xhigh + dynamic workflows) for repo-scale autonomous tasks.
- Reserve `max` for the rare case where you've verified `xhigh` was insufficient.

Set per skill/agent with the `effort:` frontmatter field. Several skills ship at `effort: high` for genuinely hard gates (e.g. `/seven-pass-review`, `/simulation-study`, `/r-package-check`). Match effort to the cognitive demand the same way you match model tier — and tune effort before you swap models.

## Why this matters

Cost reduction on routed skills is typically **50–80%** with no quality loss on the mechanical tier. The cache-TTL change (5-min default in 2026; Claude subscriptions get 1-hour automatically, API keys opt in) made multi-turn pipelines on API keys materially more expensive; per-agent routing recovers that lost ground without sacrificing the high-judgment lens where it matters.

## Routing recipe per task type

### Mechanical (Haiku 4.5)

- **TikZ → SVG extraction** (`extract-tikz`'s execution agent).
- **Bib formatting / citation rewrites** (`validate-bib`'s mechanical fix path).
- **Quarto fixer applying critic's diff** (`quarto-fixer` — separate from `quarto-critic`).
- **Proofread fix application** (when the fix is "replace X with Y" mechanically).
- **File rename / search-and-replace operations.**

### Review / critique (Sonnet 4.6)

- **R code review** (`r-reviewer`).
- **Slide layout audit** (`slide-auditor`).
- **Proofread inspection** (`proofreader`).
- **Quarto fix application** when the fix is a `quarto-critic`-driven edit.
- **AI-voice audit** (`humanize-auditor`).
- **Beamer ↔ Quarto translation** (`beamer-translator`) — translation is bounded enough to live here unless the source TeX has unusual TikZ.

### High-judgment (Opus 4.8)

- **Editor for `/review-paper --peer`** (`editor`).
- **Both referee agents** (`domain-referee`, `methods-referee`).
- **Claim verifier in fresh-context mode** (`claim-verifier`).
- **Quarto critic** (`quarto-critic`) — adversarial parity QA needs the high-judgment lens to catch subtle visual drift.
- **TikZ reviewer** (`tikz-reviewer`) — measurement-rule enforcement requires precise spatial reasoning.
- **Domain reviewer** (`domain-reviewer`).
- **Verifier** (`verifier`) when gating non-trivial commits.

## When inheritance still makes sense

- A new agent you haven't profiled yet — start with `model: inherit`, run once, then route.
- An agent whose work spans tiers in the same invocation (rare; usually a sign the agent should be split).
- One-shot test agents you'll discard.

## Anti-pattern: pushing Opus down a tier

Do **not** demote `claim-verifier`, `methods-referee`, or `editor` to Sonnet to save cost. These are the agents that protect the paper from hallucinated citations / weak identification / desk-reject mistakes. The cost of one false-positive PASS from a too-cheap verifier is materially higher than the cost of running Opus on every paper.

## Anti-pattern: self-as-architect-and-editor pairing

Aider's pattern uses one model as both planner and executor. We deliberately do not — same-model self-pairings produce correlated errors. Our split runs **different tier** on architect (Opus) vs. editor (Haiku/Sonnet); the diversity is part of the cost story.

### Corollary: challenger ≠ auditor tier (guardrail, not a build)

If a future contributor ever adds an explicit *challenger → auditor* step (e.g., an "audit-then-score" / "ground truth is a process" verifier where one agent argues against a claim and a second adjudicates), the challenger **must** run on a different tier than the auditor — two same-tier LLMs share blind spots, so a same-tier challenger launders correlated errors as independent confirmation. This costs nothing to honor today; it exists so the diversity property isn't quietly lost when the split is built. **This is a constraint on a hypothetical future step, not a green light to build it** — the current verification path uses the cheaper EXPLAINED-with-named-alternative mechanism (see `replication-protocol.md` and `verify-claims`), which adds no second agent and no cost multiplier.

## How `/commit` uses this rule

`/commit`'s pre-commit verifier currently runs at the orchestrator's tier. When this rule's pattern matures (Sonnet 4.6 reliably catches most issues), the verifier can be routed to Sonnet by default with Opus reserved for `--strict` mode. Pending evaluation.

## Cross-references

- [`.claude/rules/cross-artifact-review.md`](cross-artifact-review.md) — paper ↔ code dependency graph (orthogonal to routing but invoked at similar moments).
- [`.claude/rules/post-flight-verification.md`](post-flight-verification.md) — CoVe / forked verifier (claim-verifier should stay on Opus per "anti-pattern: pushing Opus down" above).
- Guide section "Cost-Conscious Composition" — user-facing cost guidance that points at this rule.
