#!/usr/bin/env bash
# skill.sh - POSIX shim for scripts/skill.py (git-bash / Linux / macOS)
# Usage: skill <skill-name> [args...] | skill --list
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/skill.py" "$@"
