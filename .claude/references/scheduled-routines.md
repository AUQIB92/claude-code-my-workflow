# Scheduled & Background Routines

The loop-first half of the workflow: recurring scholarly chores that should run *on a schedule* and surface only when they find something — not when you remember to run them. These are **Routines** (cron-scheduled remote agents managed by `/schedule`), not committed cron files, so they survive a closed laptop and run on web infrastructure.

> **Use Routines, not `CronCreate`,** for any away-from-keyboard work — Routines run on managed infra and persist; a local cron dies with the REPL. Each routine below is a *prompt + interval*; set them up once with `/schedule`.

## The four standing routines

| Routine | Interval | What it does | Push when |
|---|---|---|---|
| **Reproducibility drift** | nightly | Re-run `/audit-reproducibility` against the passport; diff stale claims | any FAIL (not EXPLAINED) |
| **Literature delta** | weekly | `/lit-review` sweep on your saved topics; diff against last week | new directly-relevant work |
| **Memory promotion** | monthly | `/promote-memory` — the five-critic council reviews `[LEARN]` candidates | items graduate to MEMORY.md |
| **Inbox triage** | daily / weekdays | `/triage-inbox` — referee requests, R&R deadlines, co-author asks | action proposed (always human-gated) |

**Push-on-failure, silence-on-success.** A nightly job that emails "all good" every day trains you to ignore it. These notify only on a real finding; a quiet run leaves no trace but a log line.

## Event-driven, not just scheduled

The nightly reproducibility job is the *backstop*. The *immediate* signal is the [`claim-reconcile`](../hooks/claim-reconcile.py) PostToolUse hook: the moment an analysis script or `_outputs/` artifact changes, it flags the manuscript claims that depend on it as potentially stale and points you at `/audit-reproducibility` — so you catch drift during analysis, not the next morning. For *external* regenerations (you ran `Rscript` outside Claude), the harness `FileChanged` hook event can drive the same check; wire it in `.claude/settings.json` if your workflow regenerates outputs outside the tool layer.

## Setting one up

```text
/schedule create "nightly-repro" --cron "0 6 * * *" \
  --prompt "Run /audit-reproducibility against the current passport. If any claim FAILs (not EXPLAINED), summarize which tables are affected and push a notification; otherwise exit quietly."
```

`scripts/nightly-repro-check.sh` is a thin local equivalent for users who prefer a machine cron over a Routine (note: a local cron does not survive a closed laptop — prefer `/schedule`).

## Guardrails for unattended runs

- **Never point an unattended loop at a submission portal, shared/restricted data, or a co-author's inbox without a human gate.** Routines *propose*; a human *sends*. (`/triage-inbox` never auto-sends; the [`git-guardrails`](../hooks/git-guardrails.py) hook still blocks destructive git even in a routine.)
- **Bound the cost.** A nightly full-manuscript re-audit is fine; a nightly 7× `/seven-pass-review` is not — cost-pilot first.
- **MCP may be absent in headless/cron runs** (interactively-authenticated servers like Gmail). Routines that need them must degrade gracefully.

## Cross-references

- `/schedule` — create/list/run routines.
- [`.claude/hooks/claim-reconcile.py`](../hooks/claim-reconcile.py) — the event-driven reconciliation hook.
- [`.claude/rules/replication-protocol.md`](../rules/replication-protocol.md) — what the reproducibility routine checks.
- [`.claude/rules/confidential-data.md`](../rules/confidential-data.md) — why unattended runs stay human-gated near restricted data.
