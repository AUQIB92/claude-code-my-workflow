---
name: deploy
description: Render Quarto `.qmd` slides to HTML and sync to `docs/` for GitHub Pages. Use when user says "deploy", "publish the slides", "ship to pages", "push the lecture live", "render and publish", or after Quarto edits that need to go public. NOT for local Quarto render only — use `quarto render` directly for that.
argument-hint: "[CourseCode, CourseCode/lecture, or omit for 'all']"
allowed-tools: ["Read", "Bash"]
---

# Deploy Slides to GitHub Pages

Render Quarto slides and sync all files to `docs/` for GitHub Pages deployment.

## Steps

0. **Pre-flight: confirm Quarto is on PATH before running anything.**
   ```bash
   command -v quarto >/dev/null 2>&1 || echo "quarto not found"
   ```
   If missing, `sync_to_docs.sh` will still run — but it fails silently per-file (`quarto render ... || { echo Warning; continue; }`), so a whole-course deploy can look like it "worked" while every HTML render was skipped. Stop and tell the user, pointing at `./scripts/validate-setup.sh` (which now prints an OS-aware auto-install hint, e.g. `winget install --id Posit.Quarto -e` on Windows) rather than letting them discover it from a wall of `Warning: Failed to render` lines.

1. **Run the sync script:**
   - Whole course (e.g., "CS401"): `./scripts/sync_to_docs.sh CS401`
   - One lecture (e.g., "CS401/05-addressing-cpu-bus"): `./scripts/sync_to_docs.sh CS401/05-addressing-cpu-bus`
   - No argument: `./scripts/sync_to_docs.sh` (syncs every course)

2. **Verify deployment:**
   - Check that HTML files exist in `docs/slides/<CourseCode>/`
   - Check that `_files/` directories were copied (RevealJS assets)
   - Check that `docs/Figures/` was synced from `Figures/`

3. **Verify interactive charts** (if applicable):
   - Grep rendered HTML for interactive widget count
   - Confirm count matches expected

4. **Verify TikZ SVGs** (if applicable):
   - Check that all referenced SVG files exist in `docs/Figures/<CourseCode>/<lecture>/`

5. **Open in browser** for visual verification:
   - `open docs/slides/CS401/05-addressing-cpu-bus.html`          # macOS
   - `# xdg-open docs/slides/CS401/05-addressing-cpu-bus.html`    # Linux
   - Confirm slides render, images display, navigation works

6. **Report results** to the user

## What the sync script does:
- Recursively finds `.qmd` files under `Quarto/` (skips `*_backup*` files), matched against the argument if given
- Renders each match, copies its HTML and `_files/` directory to `docs/slides/<same subpath as under Quarto/>`
- Recursively finds Beamer PDFs under `Slides/` and copies each to the matching `docs/slides/<same subpath as under Slides/>`
- Syncs `Figures/` to `docs/Figures/` using rsync (mirrors whatever course/lecture nesting exists)
