#!/usr/bin/env bash
# Flags SUPERSEDED Claude model versions that are presented as CURRENT in the
# template's user-facing surfaces. The single source of truth is the
# `<!-- CURRENT: ... -->` marker in .claude/references/model-versions.md.
#
# Historical references (CHANGELOG.md is excluded entirely) and explicit
# "prior generation" / comparison / "or later" lines are allowed via markers.
# Rendered HTML is derived from the .qmd, so we scan the source, not the HTML.
#
# Exit codes: 0 = clean, 1 = drift detected, 2 = internal error.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)"
if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
    echo "check-model-versions: cannot resolve repo root" >&2
    exit 2
fi

SSOT="$REPO/.claude/references/model-versions.md"
if [ ! -f "$SSOT" ]; then
    echo "check-model-versions: SSoT missing: $SSOT" >&2
    exit 2
fi

CURRENT_LINE="$(grep -E "<!-- CURRENT:" "$SSOT" | head -1)"
if [ -z "$CURRENT_LINE" ]; then
    echo "check-model-versions: no '<!-- CURRENT: ... -->' marker in $SSOT" >&2
    exit 2
fi

# Current-state surfaces to scan (sources; rendered HTML is derived from the qmd).
SURFACES=(
    "README.md"
    "CLAUDE.md"
    "TROUBLESHOOTING.md"
    "MEMORY.md"
    "guide/workflow-guide.qmd"
    "docs/index.html"
    ".claude/rules/model-routing.md"
    ".claude/scripts/statusline.sh"
)

# A line is allowed to name an older version if it carries one of these markers.
ALLOW='prior generation|prior gen|prior Opus|retire|migrat|historical|deprecat|was:|was |or later|incl\. 4\.|rolling out|GA 2026-0|beta|4\.[0-9]+.s |model-allow'

drift=0
for tier in "Opus" "Sonnet" "Haiku"; do
    current="$(echo "$CURRENT_LINE" | grep -oE "$tier 4\.[0-9]+" | head -1)"
    [ -n "$current" ] || continue
    for f in "${SURFACES[@]}"; do
        [ -f "$REPO/$f" ] || continue
        while IFS=: read -r lineno text; do
            ver="$(echo "$text" | grep -oE "$tier 4\.[0-9]+" | head -1)"
            [ -n "$ver" ] || continue
            [ "$ver" = "$current" ] && continue                 # names the current version → fine
            echo "$text" | grep -qiE "$ALLOW" && continue       # allow-marked line → fine
            echo "  $f:$lineno  presents '$ver' (current $tier is '$current')" >&2
            echo "      → $(echo "$text" | sed -E 's/^[[:space:]]+//' | cut -c1-110)" >&2
            drift=1
        done < <(grep -nE "$tier 4\.[0-9]+" "$REPO/$f")
    done
done

if [ "$drift" -ne 0 ]; then
    echo "" >&2
    echo "MODEL-VERSION DRIFT: a superseded version is presented as current." >&2
    echo "Fix the surface to name the current version, or add an allow-marker" >&2
    echo "(e.g. 'prior generation', 'or later', a comparison) if the mention is intentional." >&2
    echo "Source of truth: .claude/references/model-versions.md" >&2
    exit 1
fi

echo "check-model-versions: current-state surfaces match $(echo "$CURRENT_LINE" | sed -E 's/.*<!-- CURRENT: *//; s/ *-->.*//')"
exit 0
