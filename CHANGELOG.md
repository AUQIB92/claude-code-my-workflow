# Changelog

All notable changes to this template are documented here. We follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and use loose semantic versioning: **major** when fork upgrades require manual migration, **minor** for new skills or features that are additive, **patch** for fixes and docs.

If you have forked this template, see the **Upgrading** section at the bottom for how to pull updates without losing your customizations.

---

## v1.2.0 — 2026-04-13

### Added

- **`/respond-to-referees` skill** — parses a referee report, classifies each concern (addressed / partially / deferred / disagreement), points to specific revisions, and drafts a complete response document using `templates/response-to-referees.md`. Use during the R&R stage of paper revision.
- **HelloWorld sample** — `Slides/HelloWorld.tex` and `Quarto/HelloWorld.qmd` — minimal decks that compile/render on a fresh fork before any project customization.
- **`scripts/validate-setup.sh`** — colored dependency checker for Claude Code, XeLaTeX, Quarto, R, Python, git, gh, and hook permissions.
- **GitHub templates** — `.github/CONTRIBUTING.md`, issue templates, and PR template.
- **CHANGELOG.md** — this file.

### Changed

- **`/commit` skill** — now runs `scripts/quality_score.py` and the `verifier` agent on changed files as a pre-commit gate. Halts on score < 80 unless the user explicitly overrides.
- **`/extract-tikz` skill** — now invokes the `tikz-reviewer` agent after SVG generation and loops on revisions to the Beamer source until APPROVED.
- **`/slide-excellence` skill** — `domain-reviewer` agent is now MANDATORY for `.tex` files (was optional).
- **`CLAUDE.md`** — example rows in the Beamer environments and Quarto CSS classes tables are now visible (not hidden in HTML comments). Added links to `MEMORY.md` and `quality_reports/` so Claude knows where cross-session context lives.
- **`README.md`** — added "Verify Your Setup" step in the Quick Start; replaced "Work in progress" disclaimer; added badges and CHANGELOG link.
- **`docs/index.html`** — added SEO metadata (description, keywords, Open Graph, JSON-LD `SoftwareApplication` schema).
- **Skill count: 22 → 23** across all surfaces.

### Fixed

- `scripts/quality_score.py` — Quarto compilation check no longer doubles the path when `cwd` is set to the file's parent (was producing spurious 0/100 scores).
- `scripts/validate-setup.sh` — git config check now guards behind `command -v git` to avoid misleading warnings when git is missing.
- `Slides/HelloWorld.tex` — added a citation and bibliography slide so `/compile-latex`'s 3-pass + bibtex pipeline completes cleanly on the onboarding sample.

---

## v1.1.0 — 2026-03-20

### Added

- **`/deep-audit` skill** — repository-wide consistency audit (4 parallel specialist agents).
- **2026 Claude Code feature support** — effort levels (`/effort low|medium|high|max`), 5 permission modes, 4 hook handler types, 11 new hook events documented.
- **Skill frontmatter reference** — `effort`, `context: fork`, `agent`, `hooks`, dynamic `!\`command\`` injection.
- **Pattern 15: Sequential Adversarial Audits** — seven-audit protocol for paper review (inspired by ClaudeCodeTools).
- **Ecosystem section** — autoresearch (Karpathy), ClaudeCodeTools, clo-author, claudeblattman, MixtapeTools.
- **Prerequisites section** — install command (`curl -fsSL https://claude.ai/install.sh | bash`), Node.js, Claude account, cost notes.
- **`plansDirectory` setting** — explicit `quality_reports/plans/` location.
- **Automatic "Last Modified" date** — `date-modified: last-modified` in guide YAML.

### Changed

- Major guide refresh: 2400+ lines, all 25 factual claims verified against official docs across two deep-audit rounds.
- Template cleanup for fork-friendliness — removed project-specific session logs, emptied `Bibliography_base.bib`, renamed Emory SCSS to generic `theme-template.scss`.

### Fixed

- All 5 Python hooks: `from __future__ import annotations`, fail-open `try/except`, `~/.claude/sessions/` storage, hash length consistency.
- `pre-compact.py` exit code (2 → 0) and stdout → stderr (PreCompact ignores stdout).
- `post-compact-restore.py` reads `source` field (was reading `type`, never ran).

---

## v1.0.0 — 2026-02-28

### Initial Release

- 10 specialized agents: proofreader, slide-auditor, pedagogy-reviewer, r-reviewer, tikz-reviewer, beamer-translator, quarto-critic, quarto-fixer, verifier, domain-reviewer.
- 22 skills covering LaTeX, Quarto, R, reproducibility, research, and meta-workflows.
- 18 rules (4 always-on, 14 path-scoped) for quality gates, verification, and domain standards.
- 7 hooks for notifications, file protection, context monitoring, session logging, and compaction state.
- Orchestrator protocol (contractor mode) with adversarial critic-fixer loop (max 5 rounds).
- Plan-first workflow with on-disk plan persistence across context compaction.
- Three-tier memory system: `CLAUDE.md` (project), `MEMORY.md` (auto-memory), session logs.
- GitHub Pages deployment via `scripts/sync_to_docs.sh`.

---

## Upgrading Your Fork

If you forked this repo and want to pull our updates:

```bash
git remote add upstream https://github.com/pedrohcgs/claude-code-my-workflow.git
git fetch upstream
git merge upstream/main           # or: git rebase upstream/main
```

Files you almost certainly customized — `CLAUDE.md`, `Bibliography_base.bib`, `Quarto/theme-template.scss`, your lecture files in `Slides/` and `Quarto/`, `.claude/agents/domain-reviewer.md` — may produce merge conflicts. Resolve in favor of your customizations; pull only the infrastructure improvements.

To pin to a specific version: `git checkout v1.2.0`.
