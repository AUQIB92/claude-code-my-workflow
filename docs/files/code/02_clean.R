# =============================================================================
# 02_clean.R — Type coercion, missingness handling, derived columns.
#
# Takes `raw_main` from 01_load.R and produces `df` — the cleaned, analysis-
# ready data frame. Expose exactly what 03_analyze.R needs; nothing more.
# =============================================================================

# Expect raw_main from 01_load.R. inherits = FALSE so we don't silently pick
# up a stale raw_main from the user's global environment.
if (!exists("raw_main", inherits = FALSE)) {
  stop("02_clean.R: raw_main not found in the pipeline env. Run 00_run_all.R, not 02_clean.R directly.")
}

# ---- Example cleaning: adapt to your data -----------------------------------
df <- raw_main

# Safe coercion of the treatment indicator. Factors are dangerous under
# as.integer() — factor levels 1,2 become integers 1,2 rather than 0,1.
# Handle numeric, character, and the common string labels explicitly.
treated_map <- c(
  "0" = 0L, "1" = 1L,
  "Control" = 0L, "Treated" = 1L,
  "control" = 0L, "treated" = 1L
)
treated_chr <- trimws(as.character(df$treated))
unknown <- !is.na(treated_chr) & !(treated_chr %in% names(treated_map))
if (any(unknown)) {
  stop("02_clean.R: unexpected values in df$treated: ",
       paste(unique(treated_chr[unknown]), collapse = ", "),
       ". Expected 0/1 or Control/Treated.")
}
df$treated <- unname(treated_map[treated_chr])

df$delta <- df$y_post - df$y_pre

# Simulate a small amount of post-treatment lift so the analysis isn't trivial.
df$delta[df$treated == 1L] <- df$delta[df$treated == 1L] + 0.8

message("Cleaned data: ", nrow(df), " rows x ", ncol(df), " cols in `df`.")
