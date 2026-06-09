---
paths:
  - "**/*did*.R"
  - "**/*did*.do"
  - "**/*event*study*.R"
  - "**/*att_gt*.R"
  - "**/*csdid*.do"
  - "**/*drdid*"
  - "scripts/**/*did*.qmd"
---

# DiD / Event-Study Conventions (Sant'Anna practitioner standard)

Methodological standards for difference-in-differences and event-study work, after Callaway & Sant'Anna (2021), Sant'Anna & Zhao (2020), and Roth, Sant'Anna, Bilinski & Poe (2023, *"What's Trending in DiD?"*). The skill [`/did-event-study`](../skills/did-event-study/SKILL.md) implements this; this rule keeps any DiD work in the repo consistent with it.

**The governing principle (from the DiD-vault audit standard): the paper and the original author code are the source of truth; translated wrappers and printed numbers are derived artifacts to be verified against them.** If a result looks implausible, debug the wrapper — sample, weights, clustering, data construction, software engine, target mapping — *before* interpreting it.

The opinionated defaults here reflect **Pedro Sant'Anna's sign-off** (2026-06-09).

## Data & coding — HARD
- Data MUST be **LONG**: one row per unit-period.
- `gname` (group) = the **first period a unit is treated**; **never-treated coded EXACTLY `0`**.
- `idname` must be **time-invariant and numeric**, and **unique within each period**. **Check panel balance before any `panel = TRUE` estimation** — unbalanced or duplicate-`(id,period)` data errors in `DRDID`/`did` or silently changes the estimand (balancing drops attriters → a different target). For the full-sample textbook 2×2, use `panel = FALSE` with a row-unique id.
- These estimators are **staggered-adoption / absorbing only** — once treated, always treated. No reversal.
- `ATT(g,t)` is identified only for `t ≥ g`; `t < g` estimates are **pseudo-ATTs for pre-testing only** (valid only under no-anticipation).

## Estimator — HARD
- **Doubly robust is the default:** `did::att_gt(est_method = "dr")`, `DRDID::drdid(estMethod = "imp")` (IPT propensity score + WLS outcome regression — doubly robust for *inference*). `est_method` matters only when covariates are included.
- 2×2 → `DRDID::drdid`; multi-period/staggered → `did::att_gt` (which calls `drdid` internally per `ATT(g,t)`).
- Continuous dose → `contdid::cont_did` (`dname` time-invariant, its **real** value pre-treatment, **not 0**). *ALPHA — API may change; no covariates/RC/unbalanced/time-varying-dose yet.*
- Covariates must be **time-invariant / baseline** (time-varying → use the base-period value; never condition on post-treatment / treatment-affected covariates).
- DRDID convention: always `cbind(1, covariates)`.

## Control group — HARD
- **`notyettreated` is the default for staggered designs** (a larger, time-varying comparison; it imposes stronger cross-group PT — "no free lunch"); use `nevertreated` for a clean 2×T design.
- **Never use already-treated units as controls** under heterogeneity (the source of "forbidden comparisons").

## Inference — HARD
- Multiplier bootstrap with **uniform/simultaneous** bands: `bstrap = TRUE, cband = TRUE` (`biters ≥ 1000`; **25000** for publication). **Never** ship pointwise-only bands as the headline.
- `set.seed(...)` before any estimation — inference is bootstrap-based.
- `clustervars ≤ 2`, one must equal `idname`; cluster TWFE benchmarks at the unit level. Few-treated-cluster settings need care (e.g. a wild-cluster bootstrap via `fwildclusterboot`/`boottest`).
- Report design-relevant weights (`weightsname`) AND report results weighted *and* unweighted.

## Aggregation & reporting — HARD
- **Always aggregate;** never present the full `ATT(g,t)` matrix as the result. Pass `type` explicitly to `aggte()`; **avoid `type = "simple"`** (overweights early-treated).
- Headline = **Overall ATT from `aggte(type = "group")`**; dynamics = `type = "dynamic"`; per-period = `type = "calendar"`.
- Event-study plots show **both** simultaneous and pointwise bands. Map every table/figure to its generating script + line.

## Diagnostics — HARD (none skippable)
- **Pre-trends is a PRE-TEST, not a test** — *evidence on credibility*, never proof. Do **NOT** pre-test with a TWFE event study (it can reject PT under selective timing even when it holds); use the `ATT(g,t)` pre-test.
- **Sensitivity is robustness, not a gate:** report **HonestDiD** (Rambachan & Roth) breakdown values and **`didFF`** functional-form sensitivity (parallel trends is **not** invariant to levels vs logs). Formal sensitivity should be standard practice, paired with substantive reasoning about plausible confounders.
- Confirm `att_gt(est_method = "reg")` matches the TWFE event study in simple cases, so divergence is attributable to *design* (negative weights), not a coding bug.

## Verification — HARD
- **R is the benchmark for the estimators.** His R packages (`did`/`DRDID`/`didFF`/`contdid`) are the canonical implementations — **Stata (`csdid`/`drdid` via `asinr` = "as in R") and Python ports must reproduce R** to `abs_diff < 1e-6` on point estimate AND analytic SE (bootstrap-SE and cosmetic graphing differences excepted).
- **Replicating a published paper is a separate check:** translate from, and verify against, *that paper's* original author code (often Stata) — there, the paper's author code is the truth for its numbers. Benchmark against the actual `esttab`/`outreg` outputs, not printed numbers; match to `1e-6`, loosening only deliberately and documented.
- "Replication first — match original numbers before extending."

## Pitfalls Pedro warns against — DON'T
- ❌ Read pre-trends (or anything) off **dynamic TWFE** event-study coefficients under staggered timing.
- ❌ Use **already-treated** units as controls.
- ❌ **Over-read pre-trends** — condition the analysis on "passing" a pre-test, or treat passing as proof of PT.
- ❌ Wrong **clustering** level (cluster where treatment is independently assigned).
- ❌ Ignore **functional form** — PT in levels ≠ PT in logs.
- ❌ Present **`type = "simple"`** or the raw `ATT(g,t)` matrix as the headline.
- ❌ Condition on **post-treatment / treatment-affected covariates** ("bad controls").
- ❌ Interpret an implausible number before **debugging the wrapper**.

## Cross-references
- [`.claude/skills/did-event-study/SKILL.md`](../skills/did-event-study/SKILL.md) — the pipeline.
- [`.claude/rules/replication-protocol.md`](replication-protocol.md) · [`.claude/rules/r-code-conventions.md`](r-code-conventions.md) · [`.claude/rules/simulation-conventions.md`](simulation-conventions.md).
- Canonical resources: <https://psantanna.com/did-resources/> (the JEL Practitioner's Guide, *What's Trending*, the course, all packages).
