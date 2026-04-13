## Summary

<!-- 1-3 bullet points describing what changed and why. -->

## Type

- [ ] Bug fix (`fix/...`)
- [ ] New feature: skill / agent / rule / hook (`feat/...`)
- [ ] Docs / guide / README (`docs/...`)
- [ ] Chore / cleanup (`chore/...`)

## Test plan

- [ ] `./scripts/validate-setup.sh` exits 0
- [ ] `python3 scripts/quality_score.py <changed-files>` ≥ 80
- [ ] `/deep-audit` finds no new inconsistencies
- [ ] Manually exercised the changed skill/agent/hook on a real file
- [ ] Updated **both** `README.md` and `guide/workflow-guide.qmd` if user-facing
- [ ] Skill counts agree across `CLAUDE.md`, `README.md`, `docs/index.html`, and the guide

## Generality (for new skills/agents/rules)

- [ ] Works for ≥2 academic domains (not specific to one field)
- [ ] No hardcoded paths, machine-specific config, or institutional branding
- [ ] No project-specific examples in shared infrastructure

## Notes for reviewer

<!-- Anything reviewers should know — design tradeoffs, follow-up work, etc. -->
