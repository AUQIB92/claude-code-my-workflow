---
paths:
  - "**/*simulation*.R"
  - "**/*_sim.R"
  - "**/*_mc.R"
  - "scripts/**/simulations/**"
  - "explorations/**/*.R"
---

# Monte Carlo Simulation Standards

**Standard:** A simulation study is an experiment. It must be reproducible, its estimand must be unambiguous, and every headline number must carry its own Monte Carlo uncertainty.

> **Scope:** This rule covers *simulation-specific* discipline. General R standards (header, `library()` at top, relative paths, figure theme, no float `==`, CDF clamping, pre-allocation) live in [`r-code-conventions.md`](r-code-conventions.md) and the [`r-reviewer`](../agents/r-reviewer.md) Cat 9 (error handling) + Cat 11 (numerical discipline) checklists. Do not restate those here — follow both.

---

## 1. The simulation contract

Every Monte Carlo script must make four things explicit and inspectable:

1. **The DGP** — a single parameterized function `generate_data(params)` that returns a dataset. No data generation scattered through the run loop.
2. **The truth** — the true value of the target parameter, computed from `params` (not from any estimate), stored alongside the results.
3. **The estimand** — which quantity each estimator targets (e.g., ATT, ATE, a specific event-study coefficient). An estimator that targets a *different* estimand than `the truth` is a bug, not a finding.
4. **The replication budget** — `R` (number of replications) and the resulting Monte Carlo standard error on the headline metrics.

## 2. Reproducibility & seeding

- `set.seed(YYYYMMDD)` **once**, at the top — never inside the replication loop or the DGP.
- **Parallel runs are not reproducible with a single seed.** When replications run in parallel (`future`/`furrr`, `parallel`, `foreach`), use independent streams:

  ```r
  RNGkind("L'Ecuyer-CMRG")
  set.seed(20260531)
  # furrr: carry streams explicitly
  results <- furrr::future_map(seq_len(R), run_one_rep,
                               .options = furrr::furrr_options(seed = TRUE))
  ```

- Record the seed and `R` in the saved output object so a result can be traced to the exact run that produced it.

## 3. Replication count & Monte Carlo standard error (MCSE)

**A simulation result without an MCSE is an opinion.** Always report the Monte Carlo uncertainty of the headline metrics, and choose `R` so it is small relative to the effects you claim.

| Metric | Monte Carlo SE | Rule of thumb |
|---|---|---|
| Bias / mean estimate | `sd(estimates) / sqrt(R)` | Report next to every bias number |
| Coverage `p` | `sqrt(p * (1 - p) / R)` | For MCSE ≈ 0.005 (±0.5 pp) on coverage near 0.95, need `R ≈ 1900`; for ±1 pp, `R ≈ 475` |
| Rejection rate / power | `sqrt(p * (1 - p) / R)` | Same as coverage |
| RMSE | bootstrap or delta-method over reps | At minimum report `R` so readers can gauge it |

If two estimators differ by less than a couple of MCSEs, say so — do not present the smaller number as "better."

## 4. Metrics: compute them correctly

Define against **the truth**, never against another estimate:

- **Bias** = `mean(est) - truth`.
- **Empirical SE** = `sd(est)` across reps (the actual sampling variability).
- **RMSE** = `sqrt(mean((est - truth)^2))`.
- **Coverage** = share of reps whose CI **contains `truth`** — i.e. `mean(ci_lo <= truth & truth <= ci_hi)`. The single most common simulation bug is checking the CI against the point estimate or a mislabeled "true" value.
- **Size / power** = rejection rate of the test under the null DGP (size) and under the alternative DGP (power). Size must be evaluated under a DGP where the null is literally true.

## 5. Storage: save raw, not just summary

- `saveRDS()` the **per-replication raw results** (a tibble: one row per rep × estimator, with `est`, `se`, `ci_lo`, `ci_hi`, `converged`), not only the aggregated table. Re-aggregation, new metrics, and `sim-reviewer` all need the raw object.
- Save the summary table as `.rds` **and** a human-readable `.csv`/`.tex`. Outputs go to `scripts/R/_outputs/` (repo canonical path).
- Never let a headline number exist only in console output — it cannot be audited or re-rendered onto slides.

## 6. Performance & robustness

- **Pre-allocate**; never grow result vectors with `c()`/`append()` inside the loop (see `r-code-conventions.md` §8).
- Count and report **failed/non-converged replications** explicitly (`converged` flag) — silently dropping them biases every metric.
- No per-replication `print()`/`cat()`. Use a single progress bar (`progressr`) or nothing.
- Guard `NA`/`NaN`/`Inf` in estimates before computing summaries; decide and document whether they count as failures or are excluded.

## 7. Common pitfalls

| Pitfall | Impact | Prevention |
|---|---|---|
| `set.seed()` inside the loop | Identical / correlated reps; understated variance | Seed once at top; L'Ecuyer streams for parallel |
| Coverage vs. the estimate, not the truth | Coverage ≈ nominal by construction — meaningless | `mean(ci_lo <= truth & truth <= ci_hi)` |
| No MCSE reported | "Estimator A beats B" within noise | Report MCSE on bias/coverage/power |
| Estimator targets a different estimand than `truth` | Apparent "bias" that is really a mismatch | State each estimator's estimand; align with truth |
| Raw per-rep results discarded | Can't re-aggregate or audit | `saveRDS()` the raw tibble |
| Dropped failed reps unrecorded | Survivorship bias in all metrics | Track + report `converged` count |

## 8. Checklist

```
[ ] DGP is one parameterized generate_data() function
[ ] truth computed from params, stored with results
[ ] each estimator's estimand stated and aligned with truth
[ ] set.seed() once at top (YYYYMMDD); L'Ecuyer streams if parallel
[ ] R chosen for adequate MCSE; MCSE reported on bias/coverage/power
[ ] coverage = CI contains truth (not the estimate)
[ ] failed/non-converged reps counted and reported
[ ] per-rep raw results saved via saveRDS() to scripts/R/_outputs/
[ ] no per-replication console printing
```

## Cross-references

- [`r-code-conventions.md`](r-code-conventions.md) — general R standards (seeding format, pre-allocation, numerical discipline).
- [`../agents/sim-reviewer.md`](../agents/sim-reviewer.md) — the agent that enforces this rule.
- [`../agents/r-reviewer.md`](../agents/r-reviewer.md) — Cat 9 (error handling) + Cat 11 (numerical discipline).
- [`replication-protocol.md`](replication-protocol.md) — replicate-then-extend tolerance contract (applies when a simulation reproduces a published table).
