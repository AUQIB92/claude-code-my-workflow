#!/usr/bin/env bash
# Runs two pre-commit gates:
#   1. check-surface-sync.py — count assertions (skills/agents/rules/hooks)
#      agree across README, CLAUDE.md, guide source + rendered HTML,
#      landing page, skill template.
#      Exit codes: 0 = clean, 1 = drift, 2 = internal error.
#   2. check-skill-integrity.py — frontmatter/body parity, argument-hint
#      flag parity (bidirectional), internal anchor resolution, rule-skill
#      keyword parity.
#      Exit codes: 0 = clean OR only P2 advisories, 1 = P0/P1 findings,
#      2 = internal script error.
#
# Both tools run to completion even if the other fails — the user sees
# the full picture on a single invocation. The wrapper's final exit code
# is the max of the two (any failure propagates).
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

if [ "$SYNC_RC" -gt "$INTEGRITY_RC" ]; then
    exit "$SYNC_RC"
else
    exit "$INTEGRITY_RC"
fi
