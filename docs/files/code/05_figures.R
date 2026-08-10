# =============================================================================
# 05_figures.R — Figures → PDF and SVG.
#
# PDF for Beamer (crisp vector). SVG for Quarto slides (native browser render).
# Both from the same ggplot object so there's one source of truth per figure.
# =============================================================================

if (!exists("df", inherits = FALSE)) {
  stop("05_figures.R: df missing. Run 00_run_all.R (not this script directly).")
}
if (!exists("OUT_DIR", inherits = FALSE)) {
  stop("05_figures.R: OUT_DIR missing. Run 00_run_all.R (not this script directly).")
}
# Re-seed for reproducibility if geom_jitter or anything else pulls RNG.
if (exists("PROJECT_SEED", inherits = FALSE)) {
  set.seed(PROJECT_SEED)
}

# ggplot2 is a HARD dependency — figure quality is not negotiable and silent
# fallback to base-R plotting breaks the reproducibility contract (two forks
# would emit different outputs with no failure signal). See scripts/R/README.md.
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  stop(
    "05_figures.R: 'ggplot2' is required for figure generation and is not installed.\n",
    "Install with: install.packages('ggplot2')\n",
    "The pipeline will not silently fall back to base-R plots."
  )
}

# svglite is OPTIONAL but documented. If absent, fail LOUDLY (warning + explicit
# note in the output list) rather than silently skipping a promised artifact.
has_svg   <- requireNamespace("svglite", quietly = TRUE)
has_cairo <- tryCatch(capabilities("cairo"), error = function(e) FALSE)

fig_main_pdf <- file.path(OUT_DIR, "fig_main.pdf")
fig_main_svg <- file.path(OUT_DIR, "fig_main.svg")

# Choose the best available PDF device. cairo_pdf gives nicer anti-aliasing
# and font embedding but isn't compiled into every R build.
pdf_device <- if (has_cairo) grDevices::cairo_pdf else grDevices::pdf

library(ggplot2)

p <- ggplot(df, aes(x = factor(treated, labels = c("Control", "Treated")),
                    y = delta)) +
  geom_boxplot(width = 0.5, fill = "#E8EDF5", color = "#012169") +
  geom_jitter(width = 0.1, alpha = 0.4, color = "#1A1A1A") +
  labs(x = NULL, y = expression(Delta == y[post] - y[pre])) +
  theme_minimal(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),
    axis.text = element_text(color = "#1A1A1A")
  )

ggsave(fig_main_pdf, p, width = 5, height = 3.5, device = pdf_device)
message("Wrote ", fig_main_pdf)

if (has_svg) {
  ggsave(fig_main_svg, p, width = 5, height = 3.5, device = svglite::svglite)
  message("Wrote ", fig_main_svg)
} else {
  # Loud skip — warning() not message() so it shows up in `summary(sessionInfo())`
  # and in any CI log that collects warnings.
  warning(
    "05_figures.R: 'svglite' not installed — skipping fig_main.svg.\n",
    "Quarto slides that expect the SVG will fail to render this figure.\n",
    "Install with: install.packages('svglite')",
    call. = FALSE
  )
  message("SKIPPED: ", fig_main_svg, " (svglite missing)")
}
