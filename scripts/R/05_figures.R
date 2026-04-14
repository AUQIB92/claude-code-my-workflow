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

has_ggplot <- requireNamespace("ggplot2", quietly = TRUE)
has_svg    <- requireNamespace("svglite", quietly = TRUE)
has_cairo  <- tryCatch(capabilities("cairo"), error = function(e) FALSE)

fig_main_pdf <- file.path(OUT_DIR, "fig_main.pdf")
fig_main_svg <- file.path(OUT_DIR, "fig_main.svg")

# Choose the best available PDF device. cairo_pdf gives nicer anti-aliasing
# and font embedding but isn't compiled into every R build.
pdf_device <- if (has_cairo) grDevices::cairo_pdf else grDevices::pdf

if (has_ggplot) {
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
    message("Skipped SVG - install 'svglite' for Quarto-native figures.")
  }
} else {
  # Fallback: base-R plot in PDF so the pipeline still finishes cleanly.
  pdf_device(fig_main_pdf, width = 5, height = 3.5)
  boxplot(delta ~ treated, data = df, xlab = "treated", ylab = "delta")
  dev.off()
  message("Wrote ", fig_main_pdf, " (base-R fallback; install 'ggplot2' for styled output)")
}
