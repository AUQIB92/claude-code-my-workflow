---
name: did-event-study
description: Thin wrapper that runs a staggered difference-in-differences / event-study using canonical, maintained packages and surfaces their native diagnostics — it never reimplements an estimator. R via `did::att_gt`+`aggte` (Callaway–Sant'Anna), `fixest::sunab` (Sun–Abraham), and `HonestDiD` (Rambachan–Roth) for parallel-trends sensitivity; Stata via `csdid` / `eventstudyinteract` / `honestdid`. Use when the user says "run a staggered DiD", "event-study", "Callaway Sant'Anna", "Sun Abraham", "group-time ATT", "pre-trends test", "HonestDiD", or "honest parallel trends".
argument-hint: "[panel data path] [--outcome Y --unit id --time t --gvar first_treat] [--control never|notyet]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: high
---

# `/did-event-study` — Staggered DiD / Event-Study (thin wrapper)

Run a staggered-adoption DiD / event-study by **calling a canonical package**, then surface that package's **native diagnostics** verbatim. This is a *proof-of-concept that launders no authority*: every number traces to a maintained estimator, and the skill writes back the exact package calls so the user owns the code.

**Input:** `$ARGUMENTS` — a panel-data path (`.csv` / `.rds` / `.dta`) plus the column roles (`--outcome`, `--unit`, `--time`, `--gvar` = first-treated period, `0`/`Inf` for never-treated), optional `--covariates`, and the contested `--control` choice (`never` vs `notyet`).

**Core principle:** ONE estimator family per run, run *correctly*, beats a five-estimator fleet run carelessly. The skill does not hand-roll a TWFE event-study, a fake placebo, or a bespoke aggregation — those are exactly the steps the canonical packages exist to get right.

## When to use

- You have **panel/repeated-cross-section data with staggered treatment timing** and want group-time ATTs and an event-study aggregation.
- You want the **native pre-trends test and event-study plot** from `did`/`fixest`, not a reimplementation.
- You want **HonestDiD (Rambachan–Roth) sensitivity** — the breakdown `M` / relative-magnitudes bound for the parallel-trends assumption.
- You're scoping the **never-treated vs not-yet-treated comparison-group** decision and want the contrast staged explicitly (the choice the EXPLAINED disposition in [`audit-reproducibility`](../audit-reproducibility/SKILL.md) was built around).

## When NOT to use

- **2×2 (single treatment period, two groups).** A plain `feols(y ~ treat | unit + time)` is the right tool — no staggering, no aggregation needed.
- **You need the finite-sample properties of an estimator** (bias / coverage under a known DGP) — that's [`/simulation-study`](../simulation-study/SKILL.md), not a single empirical run.
- **Continuous / dose treatment, IV-DiD, or non-absorbing treatment.** These need a different canonical package (e.g. `did_multiplegt_dyn`); this skill covers the absorbing-treatment, binary case.

---

## Workflow Phases

### Phase 0: Pre-flight — pin the design, warn on the contested choice

Before running anything, produce a **Pre-Flight Report**. The single most consequential — and most contested — decision is the **comparison group**; surface it loudly.

```markdown
## Pre-Flight Report — DiD / Event-Study

**Data:** [path] — [N units × T periods, balanced? gaps?]
**Roles:** outcome=[Y], unit=[id], time=[t], cohort/gvar=[first_treat] (never-treated coded as [0|Inf])
**Covariates:** [list or "none — unconditional parallel trends"]
**Comparison group:** never-treated │ not-yet-treated  ← CONTESTED, see warning
**Estimator(s):** Callaway–Sant'Anna (did) │ Sun–Abraham (fixest) │ +HonestDiD
**Anticipation / base period:** [e.g. e = -1 normalized; anticipation = 0]
```

> ⚠️ **Comparison-group warning.** Never-treated vs not-yet-treated is a substantive identification choice, not a default. If there are **few or no never-treated units**, not-yet-treated is usually required (and `did` will warn). If treatment effects are dynamic, not-yet-treated controls are themselves treated later — `did` handles this correctly, a naive TWFE does not. **State the choice, do not silently pick one.** This is the canonical [EXPLAINED](../audit-reproducibility/SKILL.md) named alternative: the same paper can report −1.19 (not-yet-treated) and −1.187 (never-treated) and *both* be defensible — record which one the headline uses.

If outcome/unit/time/gvar cannot be inferred from the data, **stop and ask** before estimating.

### Phase 1: Run the canonical estimator(s)

Call the package — do **not** reimplement. Follow [`r-code-conventions.md`](../../rules/r-code-conventions.md) (header, `library()` at top, `set.seed()` once, relative paths) and write outputs to `scripts/R/_outputs/` (or `scripts/stata/_outputs/`).

**R — Callaway–Sant'Anna (`did`):**
```r
library(did)
att <- att_gt(yname = "Y", tname = "t", idname = "id", gname = "first_treat",
              xformla = ~ x1 + x2,              # covariates; ~1 for unconditional
              control_group = "notyettreated",  # or "nevertreated" — the Phase-0 choice
              data = panel)
es  <- aggte(att, type = "dynamic")             # event-study aggregation
grp <- aggte(att, type = "group")               # cohort-specific ATTs
saveRDS(list(att = att, es = es, grp = grp), "scripts/R/_outputs/did_main.rds")
```

**R — Sun–Abraham (`fixest::sunab`), as a cross-check on the same data:**
```r
library(fixest)
sa <- feols(Y ~ sunab(first_treat, t) | id + t, data = panel, cluster = ~id)
```

**Stata equivalents** (mirrors, same estimands): `csdid Y x1 x2, ivar(id) time(t) gvar(first_treat) notyet` → `estat event`; `eventstudyinteract Y rel_*, cohort(first_treat) control_cohort(never) absorb(id t) vce(cluster id)`.

### Phase 2: Surface the NATIVE diagnostics

Do not invent diagnostics — print the ones the packages already compute:

1. **Pre-trends test** — `did`'s universal pre-test `Wpval` (and per-period pre-event estimates from `es`); `fixest`'s pre-period coefficients. Report the p-value *and* the caveat that a passed pre-test is not proof of parallel trends.
2. **Event-study plot** — `ggdid(es)` / `iplot(sa)`. Save to `scripts/R/_outputs/`; pass `bg = "transparent"` for Beamer (per `r-code-conventions.md` §4).
3. **Group-time ATT table** — `summary(att)`: the full `ATT(g,t)` matrix, with the aggregation weights that produce the overall ATT.
4. **HonestDiD breakdown `M`** — Rambachan–Roth sensitivity over the relative-magnitudes (`Mbar`) or smoothness (`M`) restriction:
   ```r
   library(HonestDiD)
   honest <- honest_did(es, type = "relative_magnitude", Mbarvec = seq(0, 2, by = 0.5))
   ```
   Report the **breakdown value** — the `M`/`Mbar` at which the CI first includes zero. A small breakdown means the result is fragile to pre-trend violations.

### Phase 3: Write the results block + the exact calls

Write `scripts/R/_outputs/did_event_study_summary.md`:

```markdown
# DiD / Event-Study Results — [outcome] on [treatment]

**Estimator:** Callaway–Sant'Anna (did vX.Y.Z) │ comparison group: not-yet-treated
**Overall ATT:** -1.187 (SE 0.42, [95% CI ...]) — aggte(type="dynamic")
**Pre-trends:** universal pre-test p = 0.31 (not rejected; ≠ proof of PT)
**HonestDiD:** CI excludes 0 up to Mbar = 1.0; breakdown Mbar ≈ 1.3
**Sun–Abraham cross-check:** -1.20 (SE 0.44) — consistent

## Exact package calls (you own this code)
[paste the att_gt / aggte / sunab / honest_did calls run above]

## Comparison-group sensitivity (the contested choice)
| Control group   | Overall ATT | SE   |
|-----------------|-------------|------|
| not-yet-treated | -1.19       | 0.42 |
| never-treated   | -1.187      | 0.43 |
```

Embed the **literal package calls** so the run is fully reproducible and editable by hand. The user, not the skill, is the author of the specification.

---

## Output / Report format

- `scripts/R/_outputs/did_main.rds` — the `att_gt` object + both aggregations (re-aggregatable, auditable).
- `scripts/R/_outputs/event_study.{pdf,png}` — the native event-study plot.
- `scripts/R/_outputs/did_event_study_summary.md` — headline ATT, native diagnostics, HonestDiD breakdown, the contested-control sensitivity table, and the exact calls.

## Exit behavior

- **Estimation + diagnostics succeed:** exit 0; print the headline ATT, pre-test p-value, and HonestDiD breakdown to the user.
- **Package emits a substantive warning** (e.g. no never-treated units under `nevertreated`; collinear covariates; unbalanced cohorts dropped): surface it verbatim — **do not swallow it** — and pause for the user to confirm the design.
- **Outcome/unit/time/gvar unresolved, or the required package is not installed:** stop and ask before estimating; never fall back to a hand-rolled TWFE substitute.

## Cross-references

- [`.claude/skills/simulation-study/SKILL.md`](../simulation-study/SKILL.md) — for the *finite-sample* behavior of these estimators under a known DGP (TWFE-vs-CS bias, coverage); this skill is one empirical run, not a Monte Carlo.
- [`.claude/skills/audit-reproducibility/SKILL.md`](../audit-reproducibility/SKILL.md) — the never-treated vs not-yet-treated contrast is its canonical **EXPLAINED** named alternative; audit the ATT this skill produces against the manuscript.
- [`.claude/skills/preregister/SKILL.md`](../preregister/SKILL.md) — pin the comparison group, anticipation window, and event-study horizon *before* estimating to avoid specification-searching.
- [`.claude/rules/r-code-conventions.md`](../../rules/r-code-conventions.md) — R script standards (seed, paths, figure theme).
- [`.claude/rules/replication-protocol.md`](../../rules/replication-protocol.md) — tolerance thresholds for matching the ATT against a paper.

## What this skill does NOT do

- **Reimplement any estimator.** No bespoke TWFE event-study, no hand-rolled aggregation, no DIY placebo. Every number comes from `did` / `fixest` / `HonestDiD` (or their Stata twins). If you need an estimator these packages don't provide, this is the wrong skill.
- **Choose your comparison group for you.** It stages never-treated vs not-yet-treated and warns; the identification call is yours.
- **Certify parallel trends.** A passed pre-test is necessary-not-sufficient; HonestDiD quantifies fragility but does not *prove* the assumption.
- **Run a five-estimator fleet.** One canonical family per run, run correctly — not a leaderboard of half-checked methods.
- **Handle continuous/dose treatment, non-absorbing treatment, or IV-DiD.** Out of scope (see "When NOT to use").
