---
paths:
  - "Slides/**/*.tex"
  - "Quarto/**/*.qmd"
---

# Quarto Is Outside Course Workflows

Course lecture and build workflows use Beamer, Notes, and the other configured
course deliverables. Do not create, translate, sync, render, or update Quarto
course mirrors as part of course work.

Existing `.qmd` files and published pages are legacy artifacts: preserve them,
but do not treat them as required, optional, or automatically maintained course
deliverables. Keep the existing Quarto guide and site/deployment infrastructure
available for maintaining the guide and existing site.

## Enforcement

- Do not add Quarto stages to course plans, pipelines, or course progress.
- Do not propagate Beamer edits into legacy course `.qmd` files.
- Do not make course completion or verification depend on Quarto.
- Preserve Quarto files and site tooling. Only change a legacy guide/site
  artifact when the user specifically requests that separate maintenance task.
