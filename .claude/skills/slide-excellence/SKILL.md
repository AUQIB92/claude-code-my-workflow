---
name: slide-excellence
description: Multi-agent slide review (visual, pedagogy, proofreading). Use for comprehensive quality check before milestones.
argument-hint: "[QMD or TEX filename]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
context: fork
---

# Slide Excellence Review

Run a comprehensive multi-dimensional review of lecture slides. Multiple agents analyze the file independently, then results are synthesized.

## Steps

### 1. Identify the File

Parse `$ARGUMENTS` for the filename. Resolve path in `Quarto/` or `Slides/`.

### 2. Run Review Agents in Parallel

**Agent 1: Visual Audit** (slide-auditor)
- Overflow, font consistency, box fatigue, spacing, images
- Save: `quality_reports/[FILE]_visual_audit.md`

**Agent 2: Pedagogical Review** (pedagogy-reviewer)
- 13 pedagogical patterns, narrative, pacing, notation
- Save: `quality_reports/[FILE]_pedagogy_report.md`

**Agent 3: Proofreading** (proofreader)
- Grammar, typos, consistency, academic quality, citations
- Save: `quality_reports/[FILE]_report.md`

**Agent 4: TikZ Review** (only if file contains TikZ)
- Label overlaps, geometric accuracy, visual semantics
- Save: `quality_reports/[FILE]_tikz_review.md`

**Agent 5: Content Parity** (only for .qmd files with corresponding .tex)
- Frame count comparison, environment parity, content drift
- Save: `quality_reports/[FILE]_parity_report.md`

**Agent 6: Substance Review** (MANDATORY for .tex files, optional for .qmd)
- Spawn via `Task` with `subagent_type=domain-reviewer`
- Domain correctness via the 5-lens framework (Assumption Audit, Derivation Check, Citation Fidelity, Code-Theory Alignment, Logic Chain)
- Save: `quality_reports/[FILE]_substance_review.md`
- **Customize first:** `.claude/agents/domain-reviewer.md` ships as a template. Replace the 5 lenses with checks for your field (economics, physics, biology, etc.) before running. See the guide's "Customizing for Your Domain" section.

### 3. Synthesize Combined Summary

```markdown
# Slide Excellence Review: [Filename]

## Overall Quality Score: [EXCELLENT / GOOD / NEEDS WORK / POOR]

| Dimension | Critical | Medium | Low |
|-----------|----------|--------|-----|
| Visual/Layout | | | |
| Pedagogical | | | |
| Proofreading | | | |

### Critical Issues (Immediate Action Required)
### Medium Issues (Next Revision)
### Recommended Next Steps
```

## Quality Score Rubric

| Score | Critical | Medium | Meaning |
|-------|----------|--------|---------|
| Excellent | 0-2 | 0-5 | Ready to present |
| Good | 3-5 | 6-15 | Minor refinements |
| Needs Work | 6-10 | 16-30 | Significant revision |
| Poor | 11+ | 31+ | Major restructuring |
