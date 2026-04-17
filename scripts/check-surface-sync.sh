#!/usr/bin/env bash
# Runs two pre-commit gates:
#   1. check-surface-sync.py — count assertions (skills/agents/rules/hooks)
#      agree across README, CLAUDE.md, guide source + rendered HTML,
#      landing page, skill template.
#   2. check-skill-integrity.py — frontmatter/body parity, argument-hint
#      flag parity, internal anchor resolution, rule-skill keyword parity.
#
# Both exit 0 on success, 1 on detected drift/findings, 2 on internal error.
# The wrapper's exit code is the max of the two, so any failure propagates.
# Each tool runs to completion even if the other fails — the user sees the
# full picture on a single invocation.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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
