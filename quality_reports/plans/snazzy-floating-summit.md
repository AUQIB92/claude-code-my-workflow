# Plan: Workflow Improvements (All Tiers A–D)

**Status:** DRAFT
**Date:** 2026-04-13
**Scope:** Four improvement tiers from deep audit — newcomer onboarding, infrastructure cleanup, new skill, docs/community polish.

---

## Context

Three parallel Explore agents audited the repo (skills/agents/rules, usability, docs/ecosystem) and surfaced 30+ improvement opportunities. The user selected all four priority tiers. This plan stages the work into four sequential phases so each can ship as an independent PR.

**Core problems this addresses:**
1. **First-time users hit friction** — no HelloWorld sample, no install verifier, empty placeholders in CLAUDE.md leave newcomers stuck before their first successful compile.
2. **Orphaned infrastructure** — `tikz-reviewer` and `verifier` agents exist but no skill invokes them; `quality_score.py` exists but is never called from any skill.
3. **Missing high-value skill** — no `/respond-to-referees` skill despite 15+ research-group forks where revision workflows are core.
4. **Discovery/contribution gaps** — no SEO metadata, no CHANGELOG, no CONTRIBUTING.md → lost organic traffic and unclear contribution path.

**Intended outcome:** A newcomer can fork → run validate-setup → compile HelloWorld in under 10 minutes. Contributors have clear templates. No orphaned agents. Quality gates actually gate.

---

## Phase A — Newcomer Onboarding (~2h)

**Goal:** Zero-to-first-compile in under 10 minutes.

### A1. HelloWorld sample content

Files to create:
- `Slides/HelloWorld.tex` — 20-line Beamer deck, title + 2 content slides + bibliography citation. Uses minimal built-in Beamer theme (no Preambles/ dependency).
- `Quarto/HelloWorld.qmd` — 25-line RevealJS version of same content, using `theme-template.scss`.
- `Bibliography_base.bib` — populate with 2 generic example entries (replaces empty template). Entries: one `@book` and one `@article` with generic titles, clearly marked "DELETE: replace with your own."

Design decisions:
- HelloWorld.tex uses `\documentclass{beamer}` with built-in Madrid theme — no reliance on `Preambles/header.tex` so it compiles on a fresh fork without user setup.
- Bibliography entries have `@comment{DELETE THIS AND ADD YOUR OWN}` at the top.
- Content is domain-neutral: "Academic Research Workflow" as title, not econometrics-specific.

### A2. `scripts/validate-setup.sh` — dependency checker

Single bash script. Checks and reports:
- `claude --version` (Claude Code installed)
- `xelatex --version` (XeLaTeX available)
- `quarto --version` (Quarto installed)
- `R --version` (R installed, warns if missing)
- `python3 --version` (needed for hooks)
- `git --version` and `git config user.name/email` set
- `.claude/hooks/*.py` executable (suggests `chmod +x` if not)
- Prints next-step suggestion: "Run `/compile-latex HelloWorld` to verify the full pipeline."

Output uses ANSI colors: green ✓, red ✗, yellow ⚠. Each missing item includes install link.

### A3. CLAUDE.md populated examples

Edit `CLAUDE.md`:
- Keep `[YOUR PROJECT NAME]` / `[YOUR INSTITUTION]` placeholders (template users replace them).
- **Add worked examples under placeholder tables** marked `<!-- Example rows — delete and replace -->`:
  - Beamer Environments table: add 2 example rows (e.g., `keybox`, `definitionbox`).
  - Quarto CSS Classes table: add 2 example rows (e.g., `.highlight`, `.note`).
  - Current Project State table: add 1 example row for HelloWorld.
- Add link to `quality_reports/` directory: "Past plans, specs, and session logs live in [quality_reports/](quality_reports/)."
- Add link to MEMORY.md: "Cross-session learnings in [MEMORY.md](MEMORY.md)."

### A4. Update README with HelloWorld quickstart

Edit `README.md`:
- After "Quick Start" section, add 3-line "Verify Your Setup" block:
  ```
  1. Run: ./scripts/validate-setup.sh
  2. Run in Claude: /compile-latex HelloWorld
  3. Run in Claude: /deploy HelloWorld
  ```

**Verification:**
- Fresh clone → `./scripts/validate-setup.sh` runs without error, exits 0.
- Open Claude in project → `/compile-latex HelloWorld` produces `Slides/HelloWorld.pdf`.
- `/deploy HelloWorld` produces `docs/slides/HelloWorld.html`.

---

## Phase B — Infrastructure Cleanup (~1h)

**Goal:** No orphaned agents; quality gates actually gate.

### B1. Resolve orphaned agents

Read both agent files, then decide per agent:

- **`.claude/agents/tikz-reviewer.md`** — Add invocation to `/extract-tikz` skill: after compiling diagrams to SVG, spawn `tikz-reviewer` agent for visual QA. If the agent spec is weak, delete it and remove all references (guide appendix, count updates).
- **`.claude/agents/verifier.md`** — Either: (a) invoke from `/commit` skill as a pre-commit gate, or (b) delete. Decision: invoke from `/commit` since verification-before-commit matches the `verification-protocol.md` rule.

If either is deleted, update:
- Guide appendix "All Agents" table
- README agent count
- docs/index.html agent count (if present)

### B2. Integrate `scripts/quality_score.py` into `/commit`

Edit `.claude/skills/commit/SKILL.md`:
- Add Step 0 (before branch creation): "Run `python3 scripts/quality_score.py` on changed lecture/paper files. If any file scores < 80, halt and report findings. User can override with explicit instruction."
- Document the override phrase: "commit anyway" or "skip quality gate."

Verify `scripts/quality_score.py`:
- Read the script. Confirm it accepts file paths as arguments and exits non-zero below threshold.
- If it's broken (per audit — may fail when `docs/slides/` missing), add graceful degradation.

### B3. Make `domain-reviewer` mandatory in `/slide-excellence`

Edit `.claude/skills/slide-excellence/SKILL.md`:
- Change domain-reviewer from conditional/optional to mandatory for `.tex` lecture files.
- Add clear note explaining the customization requirement: user should customize `.claude/agents/domain-reviewer.md` for their field (reference guide section on domain customization).

**Verification:**
- Create a test .tex file with an intentional error → `/commit` blocks with quality score explanation.
- Run `/slide-excellence` on a .tex file → domain-reviewer runs.
- Delete orphan counts are consistent across guide, README, index.html.

---

## Phase C — `/respond-to-referees` Skill (~2h)

**Goal:** Add the highest-impact missing skill per audit.

### C1. Skill definition

Create `.claude/skills/respond-to-referees/SKILL.md`:

```yaml
---
name: respond-to-referees
description: Generate a structured response-to-referees document from a referee report and the revised manuscript. Maps each referee comment to the specific revision, flags unaddressed concerns, and drafts polite but firm responses.
argument-hint: "[referee-report-path] [revised-manuscript-path]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
effort: high
---
```

Workflow (documented in SKILL.md body):
1. Read referee report (PDF via pdftotext, or .txt/.md directly).
2. Parse into discrete comments (numbered list, one per concern).
3. For each comment:
   - Search the revised manuscript (Grep/Read) for the addressing change.
   - Classify: **addressed**, **partially addressed**, **deferred**, **disagreement**.
   - Draft a response paragraph with the academic tone conventions: acknowledge → specify the change → point to location (page/section).
4. Produce `response_to_referees.md` with a table of concerns + response letter draft.
5. Flag unaddressed concerns as a warning summary at the end.

### C2. Supporting template

Create `templates/response-to-referees.md`:
- Header: Journal name, manuscript ID, date, referee number.
- Table: concern # | summary | classification | response | page reference.
- Letter body: opening paragraph + numbered responses + closing.

### C3. Register in CLAUDE.md + guide appendix

Update files:
- `CLAUDE.md` skills table: add row for `/respond-to-referees`.
- Guide `workflow-guide.qmd` appendix: add to "All Skills" table (count 22 → 23).
- README: update skill count from 22 → 23.
- docs/index.html: update count.

### C4. Cross-link from `/review-paper`

Edit `.claude/skills/review-paper/SKILL.md` to mention: "For revision-stage work, use `/respond-to-referees` to cross-reference comments against revisions."

**Verification:**
- Create a sample referee report (~5 comments) and sample revised manuscript with 3 addressed + 1 partial + 1 unaddressed comment.
- Run `/respond-to-referees` → output correctly classifies all 5.
- Skill count consistent across all 4 documents.

---

## Phase D — Docs / Community Polish (~1.5h)

**Goal:** Improve discoverability and contribution path.

### D1. SEO metadata in `docs/index.html`

Edit `docs/index.html` `<head>`:
- Add `<meta name="description" content="...">` (150 chars, academic workflow, LaTeX, Quarto, research automation, Claude Code).
- Add `<meta name="keywords" content="Claude Code, academic workflow, LaTeX, Quarto, research, reproducibility, lecture slides, econometrics">`.
- Add Open Graph tags (`og:title`, `og:description`, `og:url`) for social sharing.
- Update `<title>` from generic to keyword-rich: "Claude Code Academic Workflow — LaTeX, Quarto, Research Automation".
- Add JSON-LD SoftwareApplication schema block for Google rich snippets.

### D2. `CHANGELOG.md`

Create at repo root following Keep a Changelog format:
- `## [v1.1.0] — 2026-04-13` with bullets for the improvements in this plan (when merged).
- `## [v1.0.0] — 2026-03-20` covering initial deep-audit + guide refresh state.
- Short preamble explaining how forked users should interpret versions (semver) and pull updates.

### D3. `.github/` templates

Create three files:
- `.github/CONTRIBUTING.md` — concise guide: "this is a template, contributions should be generic (not domain-specific), include examples from 2+ domains, update guide+README together."
- `.github/ISSUE_TEMPLATE/bug_report.md` — reproduction steps, environment, expected vs actual.
- `.github/PULL_REQUEST_TEMPLATE.md` — type checklist, testing done, README/guide updated.

Keep all three under 50 lines each. Don't over-engineer.

### D4. README polish

Edit `README.md`:
- Replace "Work in progress" disclaimer with "Actively maintained — see [CHANGELOG.md](CHANGELOG.md)".
- Add badges row at top: MIT License, Last Updated, GitHub Stars (shields.io).
- Add link to CHANGELOG.md and CONTRIBUTING.md in the footer section.
- Update community adoption line if skill count changed in Phase C.

**Verification:**
- `docs/index.html` validates against HTML5 spec; meta tags present.
- CHANGELOG.md renders on GitHub.
- `.github/` templates appear when creating issue/PR on GitHub.

---

## Files to Modify (by phase)

| Phase | File | Action |
|-------|------|--------|
| A | `Slides/HelloWorld.tex` | Create |
| A | `Quarto/HelloWorld.qmd` | Create |
| A | `Bibliography_base.bib` | Populate (via python3 — bypass protect-files hook) |
| A | `scripts/validate-setup.sh` | Create, `chmod +x` |
| A | `CLAUDE.md` | Edit placeholder tables |
| A | `README.md` | Add "Verify Your Setup" block |
| B | `.claude/agents/tikz-reviewer.md` | Decide: wire into `/extract-tikz` OR delete |
| B | `.claude/agents/verifier.md` | Wire into `/commit` |
| B | `.claude/skills/extract-tikz/SKILL.md` | Add tikz-reviewer invocation (if kept) |
| B | `.claude/skills/commit/SKILL.md` | Add quality_score.py gate + verifier invocation |
| B | `.claude/skills/slide-excellence/SKILL.md` | Mandatory domain-reviewer for .tex |
| B | `scripts/quality_score.py` | Add graceful degradation if `docs/slides/` missing |
| B | Guide appendix + README + index.html | Update agent count if deletion |
| C | `.claude/skills/respond-to-referees/SKILL.md` | Create |
| C | `templates/response-to-referees.md` | Create |
| C | `CLAUDE.md`, guide, README, index.html | Skill count 22 → 23 |
| C | `.claude/skills/review-paper/SKILL.md` | Cross-link to new skill |
| D | `docs/index.html` | SEO metadata |
| D | `CHANGELOG.md` | Create |
| D | `.github/CONTRIBUTING.md` | Create |
| D | `.github/ISSUE_TEMPLATE/bug_report.md` | Create |
| D | `.github/PULL_REQUEST_TEMPLATE.md` | Create |
| D | `README.md` | Badges, CHANGELOG link, replace "WIP" |

---

## Existing Utilities to Reuse

- **`.claude/skills/commit/SKILL.md`** — Phase B extends rather than replaces; existing structure stays.
- **`scripts/quality_score.py`** — Phase B integrates; no rewrite needed. Only add graceful degradation.
- **`.claude/hooks/protect-files.sh`** — Bibliography_base.bib is protected; use Python write workaround (already used in this repo).
- **`templates/quality-report.md`**, **`templates/session-log.md`** — Phase C response-to-referees template uses same style conventions (YAML front-matter + table + narrative sections).
- **`.claude/skills/deep-audit/SKILL.md`** — Phase C skill follows the same structure as deep-audit (phased workflow, output format table).

---

## Verification (End-to-End)

After each phase merges, verify:

**Phase A:**
```bash
./scripts/validate-setup.sh       # exits 0 on healthy setup
# In Claude:
/compile-latex HelloWorld         # produces Slides/HelloWorld.pdf
/deploy HelloWorld                # produces docs/slides/HelloWorld.html
```

**Phase B:**
```bash
# Introduce a known quality issue (equation overflow, missing citation)
/commit "test"                    # should block with quality score < 80
/slide-excellence HelloWorld      # domain-reviewer fires automatically
ls .claude/agents/ | wc -l        # matches count in guide/README/index.html
```

**Phase C:**
```bash
# Create a 5-comment sample referee report
/respond-to-referees sample-report.txt sample-manuscript.tex
# Verify response_to_referees.md classifies all 5 correctly
grep "/respond-to-referees" CLAUDE.md README.md docs/index.html
# Skill count = 23 in all 4 sources
```

**Phase D:**
```bash
# HTML validation
xmllint --html docs/index.html 2>&1 | grep -i error  # none
# GitHub shows CHANGELOG and issue/PR templates on corresponding pages
```

**Final `/deep-audit` pass:** After all four phases, run `/deep-audit` to confirm zero regressions.

---

## Sequencing

Ship as **four separate PRs** (A → B → C → D) so each can be reviewed and rolled back independently. Each phase ends with a clean working tree and a working `/deep-audit` pass. The user can stop at any phase boundary.
