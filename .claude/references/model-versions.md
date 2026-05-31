<!-- CURRENT: Opus 4.8 | Sonnet 4.6 | Haiku 4.5 -->

# Current Model Versions (single source of truth)

**Last verified against Anthropic docs:** 2026-05-31

This file is the **one place** that names current Claude model point versions. Everything else in the template should either refer to tiers abstractly ("newest Opus", "the Haiku tier") or point here. `scripts/check-model-versions.sh` flags any **superseded** version that is presented as **current** in the template's user-facing surfaces.

The machine-readable `<!-- CURRENT: ... -->` marker at the top is parsed by the checker — keep it in sync with the table.

| Tier | Current version | Model ID | Notes |
|------|-----------------|----------|-------|
| Opus (high-judgment) | **Opus 4.8** | `claude-opus-4-8` | newest; API default; GA 2026-05-28; $5/$25 per MTok; 1M context; defaults to `high` effort |
| Sonnet (workhorse) | **Sonnet 4.6** | `claude-sonnet-4-6` | 1M context |
| Haiku (fast / mechanical) | **Haiku 4.5** | `claude-haiku-4-5-20251001` | fast tier; ID is the snapshot-pinned alias |

**Retiring 2026-06-15:** Sonnet 4 + original Opus 4 → migrate to Sonnet 4.6 / Opus 4.8.

**Fast mode:** Opus 4.8 fast mode is $10/$50 per MTok (~2.5× speed). Opus 4.7 fast mode is $30/$150; Opus 4.6 fast mode is deprecated (~2026-06).

## Prior generations

It is fine to mention older versions in **historical** contexts (CHANGELOG entries) or in explicit **"prior generation" / comparison** lines (e.g. "Opus 4.8's `high` does what Opus 4.7's `xhigh` did"). They must **not** be presented as the current / newest / default model.

- **Opus 4.7** — prior Opus generation.

The checker allows a line to mention an older version when it carries a marker such as `prior generation`, `retire`, `migrat`, `deprecat`, `or later`, `historical`, an `X.Y's` comparison, or an inline `<!-- model-allow -->` comment.

## Update protocol (when Anthropic ships a new model)

1. Update the table **and** the `<!-- CURRENT: ... -->` marker above, plus the "Last verified" date.
2. Run `./scripts/check-model-versions.sh` and fix every current-state surface it flags.
3. Add a "Changed — model refresh" entry to `CHANGELOG.md`; leave historical CHANGELOG entries intact.
