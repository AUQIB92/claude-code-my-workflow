# Plan: Import from MixtapeTools + Next Evolution

**Status:** DRAFT (awaiting approval)
**Date:** 2026-04-13
**Author context:** "we are the go-to so we must keep evolving"

---

## Context

Three parallel audits compared our workflow against Scott Cunningham's [MixtapeTools](https://github.com/scunning1975/MixtapeTools), audited our existing TikZ infrastructure, and mapped the broader evolution opportunity. This plan sequences the highest-leverage work so we pull ahead on TikZ (user's explicit priority) **and** close other gaps identified by the deep audits — without scope creep.

### Headline findings

**MixtapeTools has genuinely superior TikZ infrastructure:**

- **Two-layer prevention + repair.** Our `tikz-reviewer` is repair-only. Scott's system also prevents bad TikZ at generation time (explicit node dimensions, coordinate-map comments, prohibition on `scale` for complex diagrams, canonical safe templates).
- **Measurement-based collision detection.** Scott's `tikz_rules.md` gives concrete formulas — Bézier curve max depth `= (chord_length/2) × tan(bend_angle/2)`, character-width tables by font size, minimum-clearance reference table, 6-pass protocol including cross-slide consistency and debug bounding-box visualization. Our `tikz-reviewer` uses qualitative heuristics.
- **Palette in LaTeX, tested.** Four named palettes with HEX codes and WCAG-AA contrast validation. Our palette lives in SCSS only — no LaTeX/TikZ equivalent, so colors drift.
- **Populated Preambles.** Scott ships a production Beamer preamble (`compiledeck`) with 10 named colors, font theme, footer, bullet styles, and `\transitionslide` macro. Our `Preambles/` has only `.gitkeep`.
- **Rhetoric of Decks as operational rules.** Not aspirational — three laws + Aristotelian balance table + title-as-assertion + domain structural patterns. Already referenced in our guide's ecosystem section; not operationalized in our skills.

**Our TikZ gaps (beyond MixtapeTools comparison):**

- No TikZ-from-scratch scaffold; users must seed a Beamer frame first.
- No snippet library for common diagrams (DAGs, DiD plots, timelines, regression scatters, supply/demand).
- No color-palette sync between SCSS (Quarto) and LaTeX (Beamer/TikZ) — guarantees drift.
- No animation/multi-frame reveal support.
- No accessibility (color-blind) or contrast validation.

**Other evolution opportunities (from the broader audit):**

- Only 1 skill uses `effort:`, only 4 use `context: fork` — 2026 Claude Code features underused.
- Missing adjacent workflows: grant proposals, thesis chapters (identified in earlier plan but deferred).
- `/review-paper` is single-agent; could orchestrate multiple reviewer personas in parallel via forked subagents.
- No end-to-end reproducibility audit skill (paper ↔ analysis ↔ slides).

### Intended outcome

After this plan lands, our TikZ story beats MixtapeTools (we keep the extraction pipeline they don't have **and** adopt their prevention/measurement rigor), the Preambles directory is production-ready, palettes stay in sync, and two high-leverage new skills (`/new-diagram`, parallel `/review-paper`) fill gaps the audit surfaced.

---

## Phase TX1 — TikZ Prevention Layer (~2h, highest leverage)

**Goal:** Write TikZ that can't collide in the first place.

### TX1.1. New rule: `.claude/rules/tikz-prevention.md`

Port the *prevention* half of Scott's system (path-scoped to `Slides/**` and `Figures/**`). Content:

- **Explicit node dimensions mandate** — every TikZ node must declare `minimum width`/`minimum height` or `text width`; no implicit sizing.
- **Coordinate map comments** — each `\begin{tikzpicture}` is preceded by a comment block listing named coordinates and a 1-line diagram-intent sentence.
- **Prohibition on `scale=X` for complex diagrams** — coordinates shrink, text doesn't, labels collide. Use explicit coordinates instead.
- **Directional keywords on every edge label** — `above`, `below`, `left`, `right`, `above left`, etc. Bare labels are a CRITICAL finding.
- **Canonical safe templates** referenced (see TX1.3).

### TX1.2. New rule: `.claude/rules/tikz-measurement.md`

Port the *measurement-based collision* formulas from Scott's `tikz_rules.md` — this is the mathematical core. Content:

- **Bézier curve max depth:** `max_depth = (chord_length / 2) × tan(bend_angle / 2)` — add 0.5cm safety zone. Include a pre-computed table for bend angles 20°→45° with tan values.
- **Character-width table** by font size (`\tiny`, `\scriptsize`, `\footnotesize`, `\small`, `\normalsize`) in cm-per-character.
- **Label gap calculation:** `available = center-to-center − halfwidth(A) − halfwidth(B); usable = available − 0.6cm`.
- **Minimum clearances:** 0.3cm label-to-label, 0.4cm label-to-drawn-shape, 0.5cm object-to-slide-edge.

This becomes the reference the `tikz-reviewer` agent cites.

### TX1.3. New directory: `templates/tikz-snippets/`

Copy-paste gallery of diagrams with the prevention rules baked in. Initial set (each a standalone `.tex` fragment with comment-map header + inline rationale):

- `dag-basic.tex` — 3-node causal DAG (X → Y with confounder U).
- `dag-mediation.tex` — X → M → Y with direct path.
- `did-two-period.tex` — treatment/control paths pre/post, counterfactual dashed.
- `event-study.tex` — event-time coefficients with 95% CIs and reference line at t = 0.
- `timeline.tex` — horizontal time axis with annotated events.
- `regression-scatter.tex` — scatter with fit line + confidence band (coordinate data via `\foreach`).
- `flowchart-3step.tex` — vertical process flow with decision nodes.
- `supply-demand.tex` — equilibrium diagram with shifted curves.

A `templates/tikz-snippets/README.md` explains the conventions (comment map, coordinate naming, how to adapt).

### TX1.4. Upgrade `.claude/skills/extract-tikz/SKILL.md`

Insert a new Step 1.5 **before** compilation: verify the extracted TikZ blocks comply with `tikz-prevention.md` (explicit dimensions, coordinate map present, directional keywords on labels, no `scale=` on complex diagrams). Flag violations and loop back to the Beamer source for fixes — catches issues before the expensive compile + SVG + review cycle.

### TX1.5. Upgrade `.claude/agents/tikz-reviewer.md`

Reference `tikz-measurement.md` in the "What You Check" section and require citing the specific formula (curve depth, character width, clearance) when reporting CRITICAL/MAJOR issues. This moves reviews from vibes to math.

---

## Phase TX2 — Palette + Preamble Foundation (~1h)

**Goal:** One palette, two surfaces (LaTeX + SCSS). No drift.

### TX2.1. Populate `Preambles/header.tex`

Adapt Scott's `compiledeck` preamble. Generic version (no Emory/Mixtape branding) with:

- 10 named colors (`\definecolor{primary}{HTML}{012169}`, `\definecolor{accent}{HTML}{B9975B}`, plus neutral/success/warning/danger/muted/bg-light/bg-dark variants). Match the existing `theme-template.scss` names so they're interchangeable.
- Font theme: `\usefonttheme{professionalfonts}`.
- Custom footer (minimal, page number).
- TikZ library loads: `arrows.meta, positioning, calc, decorations.pathreplacing, fit, shapes.geometric, backgrounds`.
- A small TikZ styles library: `\tikzset{dag-node/.style={...}, dashed-path/.style={...}, observed/.style={...}, counterfactual/.style={...}}`.

Comments clearly mark sections users should customize.

### TX2.2. New doc: `Preambles/README.md`

Explain the palette contract — if you change a color name, change it in `Quarto/theme-template.scss` too. Include a tiny sync-check script example.

### TX2.3. New script: `scripts/check-palette-sync.sh`

Extracts color names from `Preambles/header.tex` and `Quarto/theme-template.scss`, reports any names defined in one but missing from the other. Non-blocking (exits 0 with warnings), wired into `validate-setup.sh` as an optional section.

### TX2.4. Update `HelloWorld.tex` and `theme-template.scss`

Have them *use* the new palette names (e.g., `\textcolor{accent}{...}`), proving the end-to-end pipeline works.

### TX2.5. CLAUDE.md + guide notes

Short section in both pointing to `Preambles/header.tex` and the palette contract.

---

## Phase TX3 — New Skill: `/new-diagram` (~1.5h)

**Goal:** From-scratch TikZ creation with prevention baked in. Fills the biggest gap vs MixtapeTools.

Create `.claude/skills/new-diagram/SKILL.md`:

```yaml
---
name: new-diagram
description: Scaffold a new TikZ diagram from a snippet template with explicit node dimensions, coordinate map, and palette-synced colors. Runs the measurement pre-check before committing.
argument-hint: "[snippet-name] [output-file.tex]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Task"]
effort: medium
---
```

Workflow:

1. List available snippets from `templates/tikz-snippets/` if `$0` is omitted.
2. Copy the chosen snippet to `$1` (default `Figures/new_diagram.tex`) and replace placeholders from the user's description.
3. Run `tikz-prevention.md` checks (Step 1.5 logic reused).
4. Compile standalone via `xelatex`.
5. Spawn `tikz-reviewer` with references to `tikz-measurement.md`.
6. Loop on revisions (max 5 rounds).
7. Optionally convert to SVG if the user wants Quarto use.

Cross-link from `/create-lecture` and `/extract-tikz`.

---

## Phase PR1 — Parallel `/review-paper` (~1h, quick win)

**Goal:** Deeper reviews via multiple personas, using the 2026 `context: fork` feature we already have but underuse.

### PR1.1. Refactor `.claude/skills/review-paper/SKILL.md`

Add a new mode (keep the single-agent default for short reviews):

- **Standard mode** (current): one forked review agent, full paper.
- **Panel mode** (new): spawn three independent forked reviewers in parallel — `domain-reviewer` (field-specific), `methods-reviewer` (econometric/empirical rigor), `generalist-reviewer` (clarity, contribution framing). Synthesize into a single prioritized report with each persona's top 3 concerns. Use `effort: high` on the synthesis step.

Note: `methods-reviewer` and `generalist-reviewer` are *personas* implemented by reusing the existing `domain-reviewer` agent with different system-prompt overrides in the `Task` invocation — no new agent files needed unless adoption proves the personas benefit from separate specs.

### PR1.2. Guide update

Pattern 15 already describes sequential adversarial audits; add a sub-pattern "Parallel Panel Review" pointing to the new mode.

---

## Phase EV1 — 2026 Feature Adoption Sweep (~1h, low-risk polish)

**Goal:** Use the Claude Code features we already have but underutilize.

### EV1.1. Add `effort:` frontmatter where meaningful

Audit all 23 skills and assign:

- `effort: high` — `create-lecture`, `translate-to-quarto`, `qa-quarto`, `slide-excellence`, `deep-audit`, `interview-me`, `new-diagram` (the skills that benefit most from deeper reasoning).
- `effort: medium` — `proofread`, `visual-audit`, `review-r`, `review-paper` (standard mode), `data-analysis`, `lit-review`, `devils-advocate`, `respond-to-referees`.
- No change (default low) for simple mechanical skills (`commit`, `compile-latex`, `extract-tikz`, `deploy`, `validate-bib`, `context-status`, `learn`, `research-ideation`).

### EV1.2. Verify `context: fork` usage

Currently 4 skills fork. Audit and add to any skill that would benefit from isolation (spawns adversarial agents, does many independent reads). Likely candidates: `new-diagram`, `review-paper` panel mode.

---

## Phase EV2 — Reproducibility Audit Skill (~1.5h, optional stretch)

**Goal:** End-to-end pipeline verification — paper numbers match analysis outputs match slide tables.

Create `.claude/skills/audit-reproducibility/SKILL.md`:

1. Scan `Slides/*.tex`, `Quarto/*.qmd`, and `master_supporting_docs/` for numbered claims (coefficients, p-values, N, R², counts).
2. Locate matching R scripts in `scripts/R/` and their outputs.
3. Cross-check: do the numbers match to a declared tolerance (from `quality-gates.md`)?
4. Flag orphan analyses (script runs but output never cited), orphan claims (cited but no script), and drift (numbers don't match).
5. Output a report to `quality_reports/reproducibility-audit.md`.

Reuses `replication-protocol.md` rule as spec.

**Mark this stretch.** Phases TX1–EV1 are the core; EV2 ships only if the top phases land cleanly.

---

## Phase SH — Ship + Re-audit (~30min)

1. After each phase merges, run `/deep-audit` and check Copilot comments on the PR; fix any issues.
2. Update `CHANGELOG.md` with a `v1.3.0` entry covering all phases.
3. Tag `v1.3.0`.

Each phase is its own PR so the user can approve/stop/reorder at any boundary.

---

## Files to Modify / Create

| Phase | Path | Action |
|-------|------|--------|
| TX1 | `.claude/rules/tikz-prevention.md` | Create |
| TX1 | `.claude/rules/tikz-measurement.md` | Create |
| TX1 | `templates/tikz-snippets/*.tex` (×8) + `README.md` | Create |
| TX1 | `.claude/skills/extract-tikz/SKILL.md` | Edit (Step 1.5) |
| TX1 | `.claude/agents/tikz-reviewer.md` | Edit (cite measurement rule) |
| TX2 | `Preambles/header.tex` | Create |
| TX2 | `Preambles/README.md` | Create |
| TX2 | `scripts/check-palette-sync.sh` | Create |
| TX2 | `scripts/validate-setup.sh` | Edit (call palette-sync) |
| TX2 | `Slides/HelloWorld.tex`, `Quarto/theme-template.scss` | Edit (use new palette names) |
| TX2 | `CLAUDE.md`, `guide/workflow-guide.qmd` | Edit (palette contract doc) |
| TX3 | `.claude/skills/new-diagram/SKILL.md` | Create |
| TX3 | `.claude/skills/create-lecture/SKILL.md`, `.claude/skills/extract-tikz/SKILL.md` | Edit (cross-link) |
| TX3 | `CLAUDE.md`, README, `docs/index.html`, guide appendix | Skill count 23 → 24 |
| PR1 | `.claude/skills/review-paper/SKILL.md` | Edit (panel mode) |
| PR1 | `guide/workflow-guide.qmd` | Edit (Pattern 15 sub-pattern) |
| EV1 | All 23 `.claude/skills/*/SKILL.md` | Add `effort:` field where meaningful |
| EV2 (stretch) | `.claude/skills/audit-reproducibility/SKILL.md` | Create |
| SH | `CHANGELOG.md`, `git tag v1.3.0` | Edit + tag |

## Existing Utilities to Reuse

- `tikz-reviewer` agent — referenced by new rules and `/new-diagram`.
- `domain-reviewer` agent — reused as personas in `/review-paper` panel mode.
- `quality_score.py` — no change needed; measurement rule complements it.
- `validate-setup.sh` — extended with palette-sync check.
- `replication-protocol.md` rule — spec for the reproducibility audit skill.

## What We Are NOT Doing (Explicit Non-Goals)

- **Not cloning MixtapeTools wholesale.** Only importing the TikZ measurement/prevention system and palette discipline. The Rhetoric of Decks essays are already referenced in our ecosystem section; operationalizing them is out of scope for this round (would be its own large project).
- **Not adding grant-proposal or thesis-chapter skills yet.** Surfaced in the earlier audit but parked — revisit after this round.
- **Not touching MCP integrations.** Large, uncertain dependency on external servers.
- **Not rewriting existing hooks.** They're all clean per the last deep audit.

## Verification

After each phase:

- `./scripts/validate-setup.sh` exits 0.
- `python3 scripts/quality_score.py` on HelloWorld files still 80+.
- `quarto render guide/workflow-guide.qmd` succeeds.
- `/deep-audit` returns CLEAN on 4 parallel agents.
- A manual TikZ walkthrough: pick one snippet from the gallery, run `/new-diagram`, confirm compile+review loop produces a clean SVG.

After the final phase merges, verify:

- All counts (23 → 24 skills, 18 → 20 rules after TX1, agents unchanged, hooks unchanged) agree across CLAUDE.md, README, docs/index.html, guide.
- `CHANGELOG.md` has v1.3.0 entry; `git tag v1.3.0` pushed.

---

## Sequencing

Ship as **separate PRs per phase**: TX1 → TX2 → TX3 → PR1 → EV1 → EV2 (stretch) → SH. Each produces a self-contained, reviewable change with its own verification. User can stop at any boundary.

**Target duration:** TX phases + PR1 + EV1 ≈ 6.5h of focused work. EV2 adds ~1.5h if taken.
