#!/bin/bash
# Cross-platform desktop notification when Claude needs attention
# Triggers on: permission prompts, idle prompts, auth events
set -uo pipefail

INPUT="$(cat)"

# Fail open if jq is missing — notification is best-effort.
if ! command -v jq >/dev/null 2>&1; then
    exit 0
fi

MESSAGE="$(printf '%s' "$INPUT" | jq -r '.message // "Claude needs attention"')"
TITLE="$(printf '%s' "$INPUT" | jq -r '.title // "Claude Code"')"

case "$(uname -s)" in
  Darwin)
    # Escape double quotes in message/title for osascript
    MESSAGE="${MESSAGE//\"/\\\"}"
    TITLE="${TITLE//\"/\\\"}"
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null
    ;;
  Linux)
    if command -v notify-send &>/dev/null; then
      notify-send "$TITLE" "$MESSAGE" 2>/dev/null
    else
      echo "[$TITLE] $MESSAGE" >&2
    fi
    ;;
  *)
    echo "[$TITLE] $MESSAGE" >&2
    ;;
esac
exit 0
