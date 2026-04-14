# =============================================================================
# 03_analyze.R — Regressions, tests, model fits. Save everything to RDS.
#
# Persist fitted objects to `_outputs/*.rds` so 04_tables.R and 05_figures.R
# don't have to refit. Keeps the downstream steps fast and deterministic.
# =============================================================================

# inherits = FALSE so a stale `df` from the user's global environment
# cannot satisfy this guard — matches the contract in 00_run_all.R and
# 02_clean.R / 05_figures.R. Without this, debug reruns can silently
# analyze the wrong dataset and persist results.rds from it.
if (!exists("df", inherits = FALSE)) {
  stop("03_analyze.R: df not found in the pipeline env. Run 00_run_all.R, not this script directly.")
}

# ---- Primary specification -------------------------------------------------
fit_main <- lm(delta ~ treated, data = df)

# ---- Persist for downstream scripts ---------------------------------------
results_path <- file.path(OUT_DIR, "results.rds")
saveRDS(
  list(
    fit_main = fit_main,
    n        = nrow(df),
    seed     = PROJECT_SEED
  ),
  file = results_path
)

message("Saved analysis results to ", results_path)
