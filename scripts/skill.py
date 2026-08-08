#!/usr/bin/env python3
"""
scripts/skill.py - Tool-agnostic skill dispatcher.

Turn any skill in `.claude/skills/<name>/SKILL.md` into a terminal command:

    python scripts/skill.py compile-latex CS401/05-addressing-cpu-bus
    skill compile-latex CS401/05-addressing-cpu-bus     (via skill.cmd / skill.sh)

The launcher reads the skill's frontmatter + body (NEVER modifies the skill),
builds a CLI-agnostic prompt that points at the SKILL.md path and passes
`$ARGUMENTS`, and dispatches to whichever agent CLI is available:

    SKILL_AGENT=<name>      force a backend: claude | opencode | codex
    (default: auto-detect  claude -> opencode -> codex)

Exit codes: 0 = CLI ran (its own exit code is returned), 1 = usage/skill error.

Design constraints honored:
  - Zero changes under `.claude/skills/**` - the skill file stays the single
    source of truth; we only READ it.
  - Tool-agnostic: the prompt names the skill file path + arguments so any
    CLI (or a future one) can execute it; no CLI-specific skill plumbing.
"""

import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, ".claude", "skills")


def _safe_write(stream, text):
    """Write text to a stream, degrading gracefully on a narrow console codec
    (e.g. cp1252 on Windows) instead of raising UnicodeEncodeError."""
    try:
        stream.write(text)
    except UnicodeEncodeError:
        stream.write(text.encode(stream.encoding or "ascii", "replace").decode(
            stream.encoding or "ascii", "replace"
        ))
    stream.flush()

# Backends in preference order. The value is a list of argv prefixes.
BACKENDS = {
    "claude": ["claude", "-p"],
    "opencode": ["opencode", "run"],
    "codex": ["codex", "exec"],
}


def find_backend(forced=None):
    """Return (backend_name, [argv_prefix]) for the first available CLI."""
    if forced:
        if forced not in BACKENDS:
            _safe_write(sys.stderr, 
                "skill: unknown agent %r (choose one of %s)\n"
                % (forced, ", ".join(sorted(BACKENDS)))
            )
            sys.exit(1)
        prefix = BACKENDS[forced]
        if not shutil.which(prefix[0]):
            _safe_write(sys.stderr, "skill: agent %r not found on PATH\n" % prefix[0])
            sys.exit(1)
        return forced, prefix
    for name, prefix in BACKENDS.items():
        if shutil.which(prefix[0]):
            return name, prefix
    _safe_write(sys.stderr, "skill: no agent CLI found (need claude, opencode, or codex on PATH)\n")
    sys.exit(1)


def read_frontmatter(path):
    """Parse the YAML frontmatter block between the leading `---` markers.

    Returns a dict of raw key -> raw value strings. We intentionally do not
    import yaml (not guaranteed installed); the fields we need are simple
    `key: value` lines.
    """
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm, text


def list_skills():
    rows = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(skill_path):
            continue
        fm, _ = read_frontmatter(skill_path)
        desc = fm.get("description", "")
        # Trim to the first sentence for a compact one-line listing.
        first = re.split(r"[.!?]\s", desc)[0] if desc else ""
        rows.append("%-32s %s" % (name, first))
    return rows


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        _safe_write(sys.stdout, 
            "usage: skill <skill-name> [args...]\n"
            "       skill --list\n"
            "       skill --help\n\n"
            "Runs a skill from .claude/skills/<name>/SKILL.md through the\n"
            "available agent CLI (claude, opencode, or codex). Set SKILL_AGENT\n"
            "to force a specific backend.\n"
        )
        return 0
    if args[0] == "--list":
        for row in list_skills():
            _safe_write(sys.stdout, row + "\n")
        return 0

    name = args[0]
    skill_dir = os.path.join(SKILLS_DIR, name)
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isdir(skill_dir) or not os.path.isfile(skill_path):
        _safe_write(sys.stderr, 
            "skill: %r not found under .claude/skills/ (run `skill --list`)\n" % name
        )
        return 1

    fm, body = read_frontmatter(skill_path)
    skill_args = " ".join(args[1:]) if len(args) > 1 else ""

    backend_name, prefix = find_backend(os.environ.get("SKILL_AGENT"))

    # CLI-agnostic prompt: name the skill file and the arguments verbatim.
    # `claude -p` resolves the skill itself; for the others we still point at
    # the authoritative file so execution is tool-independent.
    prompt = (
        "Execute the skill defined in `%s`.\n"
        "Skill name: %s\n"
        "Description: %s\n"
        "Arguments ($ARGUMENTS): %s\n"
        "Follow the skill's workflow exactly and report what you did."
        % (os.path.normpath(skill_path), name, fm.get("description", ""), skill_args)
    )

    argv = list(prefix) + [prompt]
    _safe_write(sys.stderr, "skill: running %s via `%s`\n" % (name, " ".join(prefix)))
    try:
        # On Windows the agent CLIs are npm `.CMD` shims, which require
        # shell=True to resolve; on POSIX an execvp is cleaner (avoids any
        # shell quoting surprises), so we pass a list there.
        if os.name == "nt":
            proc = subprocess.run(" ".join(argv), cwd=REPO_ROOT, shell=True)
        else:
            proc = subprocess.run(argv, cwd=REPO_ROOT)
    except FileNotFoundError:
        _safe_write(sys.stderr, "skill: failed to launch %s\n" % prefix[0])
        return 1
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
