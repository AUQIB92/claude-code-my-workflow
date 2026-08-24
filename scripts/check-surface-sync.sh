#!/usr/bin/env bash
# Runs five BLOCKING pre-commit gates, plus one ADVISORY (non-blocking) one:
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
#   4. check-tikz-freshness.py — every Figures/<CODE>/<lecture>/extract_tikz.tex
#      still matches the TikZ blocks in its Beamer source. Catches the class
#      of bug where a Beamer diagram is fixed but the Quarto-embedded SVG
#      (extracted earlier) silently keeps the old, broken version.
#      Exit codes: 0 = fresh (or nothing to check), 1 = drift, 2 = internal error.
#   5. check-fork-identity.py — flags community-health files (SECURITY.md,
#      CODE_OF_CONDUCT.md, CONTRIBUTING.md, TROUBLESHOOTING.md) that still
#      hardcode the upstream template author's repo/contact instead of this
#      fork's own (compares against `git remote get-url origin`). No-op on
#      the upstream repo itself. ACKNOWLEDGMENTS.md/CITATION.cff/LICENSE/
#      CHANGELOG.md are permanently exempt (intentional attribution).
#      Exit codes: 0 = clean (or running on upstream), 1 = drift, 2 = internal error.
#
# ADVISORY (does not affect the final exit code):
#   6. check-concept-scope.py — cross-checks each course's declared
#      per-symbol introduction week (knowledge-base-<CODE>.md's Symbol
#      Reference table) against its actual first use in Slides/<CODE>/*.tex.
#      Deliberately kept non-blocking: real testing found its only live
#      hits on this repo are legitimate roadmap/preview mentions (a
#      "coming up next week" teaser), not genuine prerequisite bugs — making
#      it commit-blocking today would just train people to bypass it.
#      Findings are always printed so they inform review.
#      Exit codes: 0 = clean, 1 = finding(s) (informational only here), 2 = internal error.
#
# All tools run to completion even if one fails — the user sees the full
# picture on a single invocation. The wrapper's final exit code is the max
# of the five BLOCKING gates (any failure propagates); the advisory gate
# never changes it.
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

echo ""
echo "── check-tikz-freshness ──"
python3 "$SCRIPT_DIR/check-tikz-freshness.py"
TIKZ_RC=$?

echo ""
echo "── check-fork-identity ──"
python3 "$SCRIPT_DIR/check-fork-identity.py"
FORK_RC=$?

echo ""
echo "── check-concept-scope (advisory — does not block) ──"
python3 "$SCRIPT_DIR/check-concept-scope.py"
SCOPE_RC=$?
if [ "$SCOPE_RC" -eq 2 ]; then
    echo "check-concept-scope: internal error (advisory gate — not blocking the commit)" >&2
fi

# Final exit code is the max of the five BLOCKING gates (any failure
# propagates). check-concept-scope (SCOPE_RC) is intentionally excluded —
# see the advisory-gate note in the header comment above.
RC="$SYNC_RC"
[ "$INTEGRITY_RC" -gt "$RC" ] && RC="$INTEGRITY_RC"
[ "$MODELS_RC" -gt "$RC" ] && RC="$MODELS_RC"
[ "$TIKZ_RC" -gt "$RC" ] && RC="$TIKZ_RC"
[ "$FORK_RC" -gt "$RC" ] && RC="$FORK_RC"
exit "$RC"
