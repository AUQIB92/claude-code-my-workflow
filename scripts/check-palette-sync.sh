#!/usr/bin/env bash
# =============================================================================
# check-palette-sync.sh — verify Preambles/header.tex and Quarto/theme-template.scss
# define the same palette color names.
#
# This is a non-blocking diagnostic. Exits 0 on success, 0 with warnings on
# missing counterparts, 1 on genuine failure (files missing, unreadable).
#
# Called directly by users, and non-blocking by ./scripts/validate-setup.sh.
# =============================================================================

set -uo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

# Resolve paths relative to this script so it works from any cwd.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
LATEX_FILE="$REPO_ROOT/Preambles/header.tex"
SCSS_FILE="$REPO_ROOT/Quarto/theme-template.scss"

if [ ! -f "$LATEX_FILE" ]; then
  echo -e "${RED}✗${RESET} Missing $LATEX_FILE"
  exit 1
fi
if [ ! -f "$SCSS_FILE" ]; then
  echo -e "${RED}✗${RESET} Missing $SCSS_FILE"
  exit 1
fi

# Extract color names from LaTeX: \definecolor{NAME}{...}{HEX} OR \colorlet{NAME}{...}
latex_names=$(grep -E '\\(definecolor|colorlet)\{[a-zA-Z0-9_-]+\}' "$LATEX_FILE" \
              | sed -E 's/.*\\(definecolor|colorlet)\{([a-zA-Z0-9_-]+)\}.*/\2/' \
              | sort -u)

# Extract color-like SCSS variables: $name: #HEX (or $name: <literal color value>)
# Only pick up variables whose value starts with `#` (HEX) to avoid catching
# font-family / numeric variables. Strip any !default suffix and trailing ;.
scss_names=$(grep -E '^\$[a-zA-Z0-9_-]+:\s*#[0-9a-fA-F]{3,8}' "$SCSS_FILE" \
             | sed -E 's/^\$([a-zA-Z0-9_-]+):.*/\1/' \
             | sort -u)

# Names we expect on BOTH sides of the contract.
# LaTeX has more (semantic accents like hi-slate are defined only in LaTeX
# because the SCSS hard-codes those hex values inline in rules). We only
# enforce sync on the *core* palette names that both surfaces should share.
core_names=(primary-blue primary-gold highlight-yellow light-bg jet)

echo ""
echo -e "${BOLD}Palette sync check${RESET}"
echo -e "  LaTeX: ${LATEX_FILE}"
echo -e "  SCSS:  ${SCSS_FILE}"
echo ""

warn=0
missing_latex=()
missing_scss=()

for name in "${core_names[@]}"; do
  in_latex=false
  in_scss=false
  echo "$latex_names" | grep -qx "$name" && in_latex=true
  echo "$scss_names"  | grep -qx "$name" && in_scss=true

  if $in_latex && $in_scss; then
    echo -e "  ${GREEN}✓${RESET} $name — defined in both"
  elif $in_latex; then
    echo -e "  ${YELLOW}⚠${RESET} $name — missing from SCSS"
    missing_scss+=("$name")
    warn=$((warn + 1))
  elif $in_scss; then
    echo -e "  ${YELLOW}⚠${RESET} $name — missing from LaTeX"
    missing_latex+=("$name")
    warn=$((warn + 1))
  else
    echo -e "  ${RED}✗${RESET} $name — missing from both"
    warn=$((warn + 1))
  fi
done

echo ""
# Exit code is the machine-readable contract for validate-setup.sh and CI:
#   0 = in sync (core palette names present on both sides)
#   1 = divergence(s) detected (core names missing from one or both files)
# The warnings above are human-readable; the exit code is what automation uses.
if [ "$warn" -eq 0 ]; then
  echo -e "${GREEN}Core palette in sync.${RESET}"
  echo ""
  exit 0
fi

echo -e "${YELLOW}Core palette has $warn divergence(s).${RESET}"
if [ "${#missing_latex[@]}" -gt 0 ]; then
  echo "  Add to $LATEX_FILE: \\definecolor{NAME}{HTML}{<hex>}"
  printf '    - %s\n' "${missing_latex[@]}"
fi
if [ "${#missing_scss[@]}" -gt 0 ]; then
  echo "  Add to $SCSS_FILE: \$NAME: #<hex>;"
  printf '    - %s\n' "${missing_scss[@]}"
fi
echo ""
exit 1
