---
name: commit
description: Stage, commit, push, open a PR, and merge to main. Use ONLY on explicit commit intent — user says "commit", "ship it", "push this", "open a PR", "merge to main", "let's commit this", or prefixes with `/commit`. Do NOT auto-invoke on vague end-of-task phrases ("we're done", "wrap up") — those require explicit confirmation first. Runs the standard commit-PR-merge cycle; never force-pushes or skips hooks.
argument-hint: "[optional: commit message]"
allowed-tools: ["Bash", "Read", "Glob", "Task"]
---

# Commit, PR, and Merge

Stage changes, verify quality gates, commit with a descriptive message, create a PR, and merge to main.

## Steps

### Step 0: Quality Gate (Pre-Commit)

**Run before branching.** For every changed `.qmd`, `.tex`, or `.R` file that has quality rubrics, run:

```bash
python3 scripts/quality_score.py <changed-file-paths>
```

- If any file scores below **80**, halt and report the findings. The user must either fix the issues or explicitly override with phrases like *"commit anyway"* or *"skip quality gate"*.
- If all files score 80+, continue.

Spawn the **verifier** agent (via `Task` with `subagent_type=verifier`) to run compilation/render checks on the changed files. Report pass/fail before committing.

### Step 0b: Surface-Sync Gate (Pre-Commit)

**Runs unconditionally.** Four chained checks — count claims (`"14 agents, 28 skills, 24 rules, 6 hooks"` and siblings) across README.md, CLAUDE.md, the guide source + rendered HTML, the landing page, and the skill template all agree with the on-disk counts of `.claude/{skills,agents,rules,hooks}`; skill frontmatter/body integrity; Claude model-version currency; and TikZ-extraction freshness — every `Figures/<CODE>/<lecture>/extract_tikz.tex` still matches the `\begin{tikzpicture}` blocks in its Beamer source, so a diagram fix in `Slides/` can never silently leave a stale, broken diagram embedded in the Quarto mirror:

```bash
./scripts/check-surface-sync.sh
```

- **Exit 0:** all four gates clean — continue.
- **Exit 1:** drift detected in any gate — print the diff and halt. Fix the stale counts / integrity finding / model reference / TikZ drift, then re-run. Do NOT proceed past this gate on drift, even with "commit anyway" — the purpose is to catch the exact class of issue that produced PRs #70, #76, and #78 (count drift) and a same-session near-miss (a Beamer diagram fix that never propagated to its Quarto-embedded SVG).
- **Exit 2:** script error (missing surface file, unreadable directory) — investigate before proceeding.

### Step 1: Check current state

```bash
git status
git diff --stat
git log --oneline -5
```

### Step 2: Create a branch

```bash
git checkout -b <short-descriptive-branch-name>
```

### Step 3: Stage files

Add specific files (never use `git add -A`):

```bash
git add <file1> <file2> ...
```

Do NOT stage `.claude/settings.local.json` or any files containing secrets.

### Step 4: Commit with a descriptive message

If `$ARGUMENTS` is provided, use it as the commit message. Otherwise, analyze the staged changes and write a message that explains *why*, not just *what*.

```bash
git commit -m "$(cat <<'EOF'
<commit message here>
EOF
)"
```

### Step 5: Push and create PR

```bash
git push -u origin <branch-name>
```

**Check for `gh` before depending on it** — don't let a missing CLI silently stall the whole step:

```bash
command -v gh >/dev/null 2>&1 && echo "gh available" || echo "gh NOT available"
```

- **`gh` available:**
  ```bash
  gh pr create --title "<short title>" --body "$(cat <<'EOF'
  ## Summary
  <1-3 bullet points>

  ## Test plan
  <checklist>

  🤖 Generated with [Claude Code](https://claude.com/claude-code)
  EOF
  )"
  ```
- **`gh` NOT available:** don't fail the step. `git push` on a new branch already prints a `https://github.com/<owner>/<repo>/pull/new/<branch>` URL in its own output (GitHub prints this on every push of a branch with no open PR) — surface that exact link to the user as the next action, along with a one-line note that installing `gh` (`winget install --id GitHub.cli -e` on Windows, `brew install gh` on macOS) would let this step create the PR automatically next time. Do not attempt to install `gh` yourself mid-task without asking — package installers can require elevation this session can't grant, and retrying a failed install in a loop wastes the user's time; ask once, let them retry themselves if they want it, and move on with the manual-link fallback either way.

### Step 6: Merge and clean up

- **`gh` available:**
  ```bash
  gh pr merge <pr-number> --merge --delete-branch
  git checkout main
  git pull
  ```
- **`gh` NOT available:** this step can't be automated without it. Tell the user the branch is pushed and ready, give them the PR link from Step 5, and wait — once they report the PR is merged (via the web UI), verify it landed (`git fetch origin && git log origin/main --oneline -3`) before syncing local `main`:
  ```bash
  git checkout main
  git pull
  git branch -d <branch-name>
  ```
  Never assume a merge happened just because time has passed — confirm it on the remote first.

### Step 7: Report

Report the PR URL (or the manual `pull/new` link if `gh` was unavailable) and what was merged.

## Important

- **Never skip Step 0.** Quality gates catch broken compilation, bad citations, and hardcoded paths before they reach `main`. If the user insists on skipping, record their override reason in the commit message.
- Always create a NEW branch — never commit directly to main.
- Exclude `settings.local.json` and sensitive files from staging.
- Use `--merge` (not `--squash` or `--rebase`) unless asked otherwise.
- If the commit message from `$ARGUMENTS` is provided, use it exactly.
