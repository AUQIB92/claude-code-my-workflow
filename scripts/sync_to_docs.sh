#!/bin/bash
# sync_to_docs.sh
# Renders Quarto slides and syncs everything to docs/ for GitHub Pages
#
# Courses live one level deep: Quarto/<CourseCode>/NN-topic.qmd,
# Slides/<CourseCode>/NN-topic.pdf. Course-less decks (e.g. HelloWorld) stay
# at the Quarto/ and Slides/ top level. Output mirrors the same nesting
# under docs/slides/, so docs/slides/<CourseCode>/NN-topic.html.
#
# Usage: ./scripts/sync_to_docs.sh [target]
# Examples:
#   ./scripts/sync_to_docs.sh                    # Sync everything
#   ./scripts/sync_to_docs.sh CS401               # Sync every lecture in course CS401
#   ./scripts/sync_to_docs.sh CS401/05-addressing-cpu-bus   # Sync one lecture
#   ./scripts/sync_to_docs.sh HelloWorld          # Sync a course-less deck

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
QUARTO_DIR="$REPO_ROOT/Quarto"
SLIDES_DIR="$REPO_ROOT/Slides"
DOCS_DIR="$REPO_ROOT/docs"

echo "=== Syncing Quarto slides to docs/ ==="
echo "Repo root: $REPO_ROOT"

# 1. Find matching .qmd files (recursive; skip backups)
cd "$QUARTO_DIR"

matched_qmds=()
if [ -n "$1" ]; then
    while IFS= read -r qmd; do
        matched_qmds+=("$qmd")
    done < <(find . -type f -name '*.qmd' ! -name '*_backup*' \
              \( -path "./${1}.qmd" -o -path "./${1}_*.qmd" -o -path "./${1}/*.qmd" \))
    if [ ${#matched_qmds[@]} -eq 0 ]; then
        echo "Error: No QMD file found matching '${1}'"
        exit 1
    fi
else
    while IFS= read -r qmd; do
        matched_qmds+=("$qmd")
    done < <(find . -type f -name '*.qmd' ! -name '*_backup*')
fi

# 2. Render each match and sync HTML + _files to docs/slides/<same subpath>/
echo "Rendering ${#matched_qmds[@]} Quarto file(s)..."
for qmd in "${matched_qmds[@]}"; do
    qmd="${qmd#./}"
    echo "  Rendering $qmd..."
    quarto render "$qmd" || { echo "  Warning: Failed to render $qmd"; continue; }

    reldir="$(dirname "$qmd")"
    [ "$reldir" = "." ] && reldir=""
    outdir="$DOCS_DIR/slides/$reldir"
    mkdir -p "$outdir"

    html="${qmd%.qmd}.html"
    if [ -f "$html" ]; then
        echo "  Copying $html -> $outdir/"
        cp "$html" "$outdir/"

        files_dir="${html%.html}_files"
        if [ -d "$files_dir" ]; then
            echo "  Copying $files_dir/..."
            rm -rf "$outdir/$(basename "$files_dir")"
            cp -r "$files_dir" "$outdir/"
        fi
    fi
done

# 3. Sync Beamer PDFs to the matching docs/slides/<CourseCode>/ (recursive)
echo "Syncing Beamer PDFs..."
while IFS= read -r pdf; do
    relpdf="${pdf#"$SLIDES_DIR"/}"
    reldir="$(dirname "$relpdf")"
    [ "$reldir" = "." ] && reldir=""
    outdir="$DOCS_DIR/slides/$reldir"
    mkdir -p "$outdir"
    echo "  Copying $relpdf..."
    cp "$pdf" "$outdir/"
done < <(find "$SLIDES_DIR" -type f -name '*.pdf')

# 4. Sync R scripts to docs/files/code/
echo "Syncing R scripts..."
mkdir -p "$DOCS_DIR/files/code"
for rscript in "$REPO_ROOT/scripts/R/"*.R; do
    if [ -f "$rscript" ]; then
        echo "  Copying $(basename "$rscript")..."
        cp "$rscript" "$DOCS_DIR/files/code/"
    fi
done

# 5. Sync Figures directory (using rsync for efficiency; already nests by
#    CourseCode/lecture, rsync mirrors whatever depth exists)
echo "Syncing Figures/..."
if command -v rsync &> /dev/null; then
    rsync -av --delete "$REPO_ROOT/Figures/" "$DOCS_DIR/Figures/"
else
    rm -rf "$DOCS_DIR/Figures"
    cp -r "$REPO_ROOT/Figures" "$DOCS_DIR/Figures"
fi

# 6. Sync Assignments to docs/assignments/<CourseCode>/ (recursive).
#    Solution keys (*-solutions.pdf) are NEVER published — excluded here and
#    gitignored, so answer keys never reach the public GitHub Pages site.
echo "Syncing Assignments (solutions excluded)..."
while IFS= read -r pdf; do
    relpdf="${pdf#"$REPO_ROOT/Assignments"/}"
    reldir="$(dirname "$relpdf")"
    [ "$reldir" = "." ] && reldir=""
    outdir="$DOCS_DIR/assignments/$reldir"
    mkdir -p "$outdir"
    echo "  Copying $relpdf..."
    cp "$pdf" "$outdir/"
done < <(find "$REPO_ROOT/Assignments" -type f -name '*.pdf' ! -name '*solutions*')

# 7. Sync prose Lecture Notes to docs/notes/<CourseCode>/ (recursive).
#    Notes are student-facing and derived from the Beamer decks.
echo "Syncing Lecture Notes..."
while IFS= read -r pdf; do
    relpdf="${pdf#"$REPO_ROOT/Notes"/}"
    reldir="$(dirname "$relpdf")"
    [ "$reldir" = "." ] && reldir=""
    outdir="$DOCS_DIR/notes/$reldir"
    mkdir -p "$outdir"
    echo "  Copying $relpdf..."
    cp "$pdf" "$outdir/"
done < <(find "$REPO_ROOT/Notes" -type f -name '*.pdf')

# 8. Sync CompetitiveExam practice sets to docs/competitive-exam/<CourseCode>/.
#    Only per-course question/answer PDFs are published — the copyrighted
#    textbook scans under CompetitiveExam/Books/ are NEVER synced.
echo "Syncing CompetitiveExam practice sets (Books excluded)..."
while IFS= read -r pdf; do
    relpdf="${pdf#"$REPO_ROOT/CompetitiveExam"/}"
    reldir="$(dirname "$relpdf")"
    [ "$reldir" = "." ] && reldir=""
    case "$relpdf" in
        Books/*) continue ;;  # skip copyrighted scans
    esac
    outdir="$DOCS_DIR/competitive-exam/$reldir"
    mkdir -p "$outdir"
    echo "  Copying $relpdf..."
    cp "$pdf" "$outdir/"
done < <(find "$REPO_ROOT/CompetitiveExam" -type f -name '*.pdf')

echo ""
echo "=== Sync complete! ==="
echo "Files synced to: $DOCS_DIR/slides/"
