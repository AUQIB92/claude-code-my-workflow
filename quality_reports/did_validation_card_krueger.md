# `/did-event-study` validation — Card & Krueger (1994)

**Date:** 2026-06-09 · **Model:** Opus 4.8 · **Standard:** `DiD_book` 1e-6 tolerance
**Source of truth:** Pedro Sant'Anna's `DiD_book/Card_Krueger_American_Economic_Review_1994` (his code + recorded outputs).

## Result: PASS (principle) + 1 real bug found & fixed (prescription)

| Check | Value | vs target | Status |
|---|---|---|---|
| Reproduce his canonical 2×2 DiD (`feols(fte ~ treated*post)`) | `2.913982357430426` | his `…376` | **1e-14** ✅ |
| Skill's estimator `DRDID::drdid` reproduces it (fixed: RC + row-id) | `2.913982357430…` | his 2×2 | **2.7e-14** ✅ |
| Skill's *original* prescription `DRDID(panel=TRUE, idname=id)` | **ERROR** | — | ✗ bug |

## The bug (why this validation mattered)
Card–Krueger is an **unbalanced** panel (409 stores; only 389 in both waves) with **2 duplicate `(id,wave)` rows**. The skill prescribed `DRDID::drdid(panel = TRUE)` with the panel id, which **errors** ("idname must be unique by tname") on exactly this common real-world shape.

**Fixes applied:**
- Skill Phase 3: a pre-flight balance/uniqueness check; full-sample 2×2 via `panel = FALSE` + a **row-unique id** (matches `feols` to ~1e-10); balancing → `panel = TRUE` is flagged as a **different estimand**.
- `did-conventions` rule: idname-unique-by-period + check-balance-before-panel-mode is now HARD.

## Estimand note (the `EXPLAINED` pattern, live)
- Full-sample textbook 2×2 (his target): **ATT = 2.914**
- Balanced-panel DR (389 stores, 19 attriters dropped): **ATT = 2.972**

Both are defensible — they answer different questions. The skill now records this as a named alternative rather than presenting one number as "the" answer.

## Caveat
SE comparison is not 1e-6: `DRDID` RC SE (1.73) treats waves as independent; `feols` clustered SE (1.29) uses the panel. For a true panel, report the clustered/panel SE. Point-estimate equivalence is the validation test.

## Not yet validated
`HonestDiD`/`didFF`/`contdid` are not installed → the staggered `att_gt` path + sensitivity suite (HonestDiD breakdown, `didFF`) and continuous-treatment path remain to be validated on a genuinely staggered `DiD_book` application.
