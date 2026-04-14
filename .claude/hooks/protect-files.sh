#!/bin/bash
# Block accidental edits to protected files.
# Customize PROTECTED_PATTERNS below for your project.
#
# This hook respects two explicit bypass signals so Claude can run
# fully automated when the user has granted bypass permissions:
#
#   1. CLAUDE_CODE_DISABLE_FILE_PROTECTION=1 in the environment, or
#   2. permission_mode == "bypassPermissions" in the hook input JSON
#      (field name probed across known variants).
#
# If neither bypass is present, the hook enforces protection as before.

set -uo pipefail

INPUT=$(cat)

# Escape hatch 1 — explicit env var
if [ "${CLAUDE_CODE_DISABLE_FILE_PROTECTION:-0}" = "1" ]; then
  exit 0
fi

# Escape hatch 2 — bypass permission mode detected in hook input.
# Claude Code has used slightly different field names across versions;
# probe all known variants and fall through to protection if none match.
PERM_MODE=$(echo "$INPUT" | jq -r '
  .permission_mode //
  .permissionMode //
  .session.permission_mode //
  .session.permissionMode //
  empty
' 2>/dev/null)

case "$PERM_MODE" in
  bypassPermissions|bypass|bypass_permissions)
    exit 0
    ;;
esac

TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=""

# Extract file path based on tool type
if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

# No file path = not a file operation, allow
if [ -z "$FILE" ]; then
  exit 0
fi

# ============================================================
# CUSTOMIZE: Add patterns for files you want to protect
# Uses basename matching — add full paths for more precision
# ============================================================
PROTECTED_PATTERNS=(
  "Bibliography_base.bib"
  "settings.json"
)

BASENAME=$(basename "$FILE")
for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$BASENAME" == "$PATTERN" ]]; then
    cat >&2 <<EOF
Protected file: $BASENAME.
Edit manually, or disable protection with one of:
  - Set CLAUDE_CODE_DISABLE_FILE_PROTECTION=1 in your shell
  - Use bypassPermissions mode
  - Remove "$PATTERN" from PROTECTED_PATTERNS in .claude/hooks/protect-files.sh
EOF
    exit 2
  fi
done

exit 0
