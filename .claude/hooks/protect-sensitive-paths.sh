#!/bin/bash
# =============================================================================
# protect-sensitive-paths.sh — PreToolUse guard for policy + executable files.
#
# The earlier permissions.deny list only covered Edit/Write on
# .claude/settings.json and .claude/hooks/**, but allowlisted Bash commands
# (python3, cp, mv, chmod) could still rewrite those files. Codex round-2
# flagged this as a porous trust boundary.
#
# This hook runs on every PreToolUse event. For Edit/Write it inspects the
# file_path. For Bash it inspects the command string for path arguments that
# resolve to the sensitive set. Blocks (exit 2) on a match unless one of the
# two explicit bypass signals is present:
#
#   - CLAUDE_CODE_DISABLE_FILE_PROTECTION=1 in the environment
#   - permission_mode == "bypassPermissions" in the hook input
#
# Fail-open on any parse error: exit 0 so a buggy hook never blocks Claude.
# =============================================================================

set -uo pipefail

# ---- Escape hatches — check BEFORE reading stdin ---------------------------
if [ "${CLAUDE_CODE_DISABLE_FILE_PROTECTION:-0}" = "1" ]; then
  exit 0
fi

INPUT=$(cat 2>/dev/null || true)
if [ -z "$INPUT" ]; then
  exit 0
fi

PERM_MODE=$(echo "$INPUT" | jq -r '
  .permission_mode //
  .permissionMode //
  .session.permission_mode //
  .session.permissionMode //
  empty
' 2>/dev/null)
case "$PERM_MODE" in
  bypassPermissions|bypass|bypass_permissions) exit 0 ;;
esac

TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
if [ -z "$TOOL" ]; then
  exit 0
fi

SENSITIVE_PATHS=(
  ".claude/settings.json"
  ".claude/hooks/"
)

is_sensitive() {
  local candidate="$1"
  candidate="${candidate#./}"
  candidate="${candidate%\"}"; candidate="${candidate#\"}"
  candidate="${candidate%\'}"; candidate="${candidate#\'}"
  for p in "${SENSITIVE_PATHS[@]}"; do
    case "$candidate" in
      *"$p"*) return 0 ;;
    esac
  done
  return 1
}

block() {
  local reason="$1"
  cat >&2 <<EOF
Blocked: tool '$TOOL' attempted to access a sensitive path.
$reason

These paths require explicit approval to modify:
  - .claude/settings.json  (permission policy — changes affect every future run)
  - .claude/hooks/*        (executable code that runs on session + tool events)

To proceed, approve the operation via the interactive prompt, or grant bypass:
  - Set CLAUDE_CODE_DISABLE_FILE_PROTECTION=1 in your shell
  - Use bypassPermissions permission mode
EOF
  exit 2
}

case "$TOOL" in
  Edit|Write|MultiEdit)
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    if [ -n "$FILE" ] && is_sensitive "$FILE"; then
      block "  Tool input file_path: $FILE"
    fi
    ;;
  Bash)
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
    if [ -n "$CMD" ] && is_sensitive "$CMD"; then
      block "  Bash command: $CMD"
    fi
    ;;
esac

exit 0
