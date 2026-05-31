#!/usr/bin/env bash
# Runs three pre-commit gates:
#   1. check-surface-sync.py — count assertions (skills/agents/rules/hooks)
#      agree across README, CLAUDE.md, guide source + rendered HTML,
#      landing page, skill template.
#      Exit codes: 0 = clean, 1 = drift, 2 = internal error.
#   2. check-skill-integrity.py — frontmatter/body parity, argument-hint
#      flag parity (bidirectional), internal anchor resolution, rule-skill
#      keyword parity.
#      Exit codes: 0 = clean OR only P2 advisories, 1 = P0/P1 findings,
#      2 = internal script error.
#   3. check-model-versions.sh — flags superseded Claude model versions
#      presented as current in user-facing surfaces.
#      SSoT: .claude/references/model-versions.md.
#      Exit codes: 0 = clean, 1 = drift, 2 = internal error.
#
# All tools run to completion even if one fails — the user sees the full
# picture on a single invocation. The wrapper's final exit code is the max
# of the three (any failure propagates).
#
# We deliberately do NOT use `set -e` because that would abort after the
# first gate fails, hiding the second gate's output. We use `set -uo
# pipefail` for basic safety. SCRIPT_DIR resolution is checked explicitly
# below rather than relying on `-e` to catch failures.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
if [ -z "$SCRIPT_DIR" ] || [ ! -d "$SCRIPT_DIR" ]; then
    echo "check-surface-sync.sh: cannot resolve script directory" >&2
    exit 2
fi

echo "── check-surface-sync ──"
python3 "$SCRIPT_DIR/check-surface-sync.py" "$@"
SYNC_RC=$?

echo ""
echo "── check-skill-integrity ──"
python3 "$SCRIPT_DIR/check-skill-integrity.py" "$@"
INTEGRITY_RC=$?

echo ""
echo "── check-model-versions ──"
"$SCRIPT_DIR/check-model-versions.sh"
MODELS_RC=$?

# Final exit code is the max of all three gates (any failure propagates).
RC="$SYNC_RC"
[ "$INTEGRITY_RC" -gt "$RC" ] && RC="$INTEGRITY_RC"
[ "$MODELS_RC" -gt "$RC" ] && RC="$MODELS_RC"
exit "$RC"
