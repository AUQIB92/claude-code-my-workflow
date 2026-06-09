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

## Staggered + sensitivity path — VALIDATED (did::mpdta, the canonical CS example)

Installed `HonestDiD` 0.2.8 + `didFF` 0.1.0 (local source). Ran the full skill pipeline with his defaults:

| Step | Result | Status |
|---|---|---|
| `att_gt` (notyettreated, `dr`, universal base, bootstrap+cband) | runs clean | ✅ |
| Overall ATT (his notyettreated default) | **−0.0323** (se 0.0115) | ✅ |
| Overall ATT (nevertreated, vignette ref) | **−0.0328** vs documented ≈−0.031 | ✅ |
| Event study `aggte(dynamic)` | pre ≈ 0 (`e=-1`=0), post −0.02→−0.14 (canonical) | ✅ |
| `ggdid` | plot produced | ✅ |
| HonestDiD relative-magnitudes (direct path) | robust CIs at Mbar 0/0.5/1 | ✅ |
| `didFF` functional-form test | p = 0.998 (can't reject insensitivity) | ✅ |

**2nd real bug found & fixed:** the skill said `honest_did()` is "README glue, not an export." Precisely, it's a **non-exported internal S3 method** in `HonestDiD 0.2.8` — bare `honest_did()` errors. The skill now ships the **validated direct recipe** (`createSensitivityResults_relativeMagnitudes` with betahat + IF-based sigma from `aggte(dynamic)`), confirmed to run on `mpdta`.

## Overall verdict
The `/did-event-study` pipeline is **validated end-to-end on real data** — 2×2 (Card–Krueger, 1e-14) and staggered + sensitivity (mpdta) — driving *his* packages, with **2 real bugs found by running it and fixed**. Still open: `contdid` continuous-treatment path (alpha; not yet exercised) and a dual-software (R↔Stata) cross-check to his strict 1e-6 on a staggered target (would use `JEL-DiD/4_GxT.R` + `csdid`).
