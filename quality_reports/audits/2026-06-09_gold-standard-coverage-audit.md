# Gold-Standard Coverage + Coherence Audit

**Date:** 2026-06-09  ·  **Method:** multi-agent workflow (63 agents, 6 coverage finders + adversarial verify, 5 coherence finders + verify, synthesis + completeness critic)

**Bar:** "gold standard for empirical economics research IN GENERAL, with DiD as the proven flagship."

**True surface:** 50 skills · 18 agents · 32 rules · 9 references.


## Verdict

> No — the repo is a gold standard for DiD specifically, and a strong general-purpose research-workflow scaffold, but it is NOT yet a gold standard for empirical economics IN GENERAL on the methods axis. The reduced-form world it serves (~55% of top-5 empirical econ per its own discipline-card) is dominated by DiD, IV, and RD; only DiD has a flagship (deep skill + HARD-rule companion + verification contract anchored on Pedro's own packages). IV and RD exist only as passing mentions in lists and a 'tailor as needed' line in /stata-replication, with no diagnostic workflow, no robust-inference guidance, no companion rule. Selection-on-observables (matching/PS/IPW) has zero implementation surface. The three moves that would most change the answer: (1) build a /iv-2sls flagship (highest-frequency uncovered workhorse, carries weak-instrument inference + LATE/MTE as bundled modules); (2) build a /rdd-analysis flagship (sharp+fuzzy, rdrobust/rddensity, mirrors the /did-event-study pattern); (3) ship a shared quasi-experimental-design rule + a selection-on-observables surface (matching/PS/IPW/overlap), so every new method inherits one inference/robustness substrate instead of re-deriving it. The coherence side is healthy: nearly all overlap findings resolve to 'leave as is' (the review/verification/memory families are intentional, complementary layers), so the work is almost entirely additive — build the missing method flagships, not untangle existing ones.


## Build map — flagship candidates


### [P0] `/iv-2sls (IV / 2SLS flagship, with weak-instrument inference and LATE/MTE as bundled modules)`

IV/2SLS is the highest-frequency uncovered workhorse in reduced-form econ (the dominant ~55% paper-type per the repo's own discipline-card lists DiD, IV, RD as the core trio). Current coverage is passing mentions only (methods-referee F>10 sanity line, power-analysis 'weak-instrument-aware' phrase, lists in research-ideation/grant-proposal) — no diagnostic workflow, no robust inference, no companion rule. Build to general best practice mirroring /did-event-study: design+specification, first-stage diagnostics (effective F / Kleibergen-Paap), weak-ID-robust inference (Anderson-Rubin, Stock-Yogo), and LATE-vs-ATE interpretation. CONFIRMED: weak-instrument inference and LATE/MTE are genuinely absent as substantive coverage; fold them in as modules of this skill rather than separate skills so IV is taught as a coherent whole (what it identifies, on whom, and when it is credible). Package orchestration: ivreg/estimatr/ivDiag (R), ivreg2/weakivtest (Stata).

*depends_on:* shared quasi-experimental design + inference rule (see consolidate_retire); reuses /power-analysis + /simulation-study harness for weak-instrument simulation-based power


### [P0] `/rdd-analysis (Regression discontinuity — sharp and fuzzy)`

RDD is the third leg of the reduced-form trio (~10% of applied-micro reduced-form work) and, like IV, exists only in lists plus a 'RD with rdrobust' tailoring line in /stata-replication — no skill, no rule, no diagnostic suite. Build to general best practice on the /did-event-study template: continuity/no-manipulation verification, data-driven bandwidth selection and robustness, local-polynomial estimation, balance and covariate-smoothness at the cutoff, McCrary/rddensity manipulation test, fake-cutoff placebos, bandwidth sensitivity. Support both sharp and fuzzy (fuzzy shares the first-stage/compliers logic with the IV flagship, so build IV first). Package orchestration: rdrobust, rddensity, rdpower.

*depends_on:* /iv-2sls (fuzzy RD reuses IV first-stage/LATE machinery); shared quasi-experimental design + inference rule


### [P0] `did-conventions.md / /did-event-study (the proven flagship — already shipped; keep as the template all others copy)` — **⟨anchored on Pedro's packages⟩**

This is the existing gold-standard exemplar, anchored on Pedro's own packages (did/DRDID/didFF/contdid) with a HARD-rule companion, a verification contract (R is the benchmark; ports must match to 1e-6), and an 8-phase diagnostic pipeline. pedro_resource=TRUE here only. It is NOT a build candidate — it is listed as P0 to mark it as the reference architecture every other flagship in this map must replicate (deep skill + HARD-rule companion + verification + sensitivity-not-gate framing). Continuous-dose (contdid) is flagged ALPHA in the rule; keep that caveat as the API stabilizes.

*depends_on:* none — it is the dependency target / pattern source


### [P1] `/matching-weighting (selection-on-observables: matching / propensity score / IPW / entropy balancing)`

CONFIRMED genuinely thin: PS appears only inside the DiD doubly-robust context (did-conventions PS trimming) and as an editor overlap/common-support peeve; zero standalone selection-on-observables workflow and zero matching/weighting package surface in the repo. Standard across observational work in many econ subfields and adjacent disciplines the template targets. Build to general best practice: PS specification + diagnostics, balance assessment (SMD/Love plot), overlap/common-support verification, estimator choice (matching, IPW, AIPW/doubly-robust, entropy balancing), and sensitivity to unobserved confounding (E-value / Rosenbaum bounds). Natural conceptual sibling to the DiD DR estimator already in the repo, so it strengthens the existing flagship's foundations. Packages: MatchIt, WeightIt, cobalt (R).

*depends_on:* shared quasi-experimental design + inference rule


### [P1] `/panel-models (correlated random effects / Mundlak + generic panel FE guardrails; dynamic-panel GMM as a P2 module)`

Two CONFIRMED/PLAUSIBLE panel gaps consolidate into one flagship. (a) Mundlak/CRE is CONFIRMED entirely absent — no FE-vs-RE specification testing, no Hausman/CRE framework. (b) Generic (non-DiD) panel FE is PLAUSIBLE-thin: TWFE is taught well but ONLY inside the staggered-DiD context; standard panel-FE settings, within-estimator asymptotics, Nickell bias, and clustering guardrails have no home. Build to general best practice as a single panel-estimation skill that covers when TWFE is correct (clean 2-period/static designs), CRE/Mundlak as the short-panel alternative, FE-vs-RE choice, and proper clustering — explicitly cross-referencing /did-event-study for the 'under staggered timing, do not headline TWFE' boundary so the two never contradict. Dynamic-panel GMM (Arellano-Bond / system GMM, CONFIRMED absent) is a lower-frequency macro/finance/growth tool — ship it as a P2 module inside this skill, not its own flagship.

*depends_on:* shared quasi-experimental design + inference rule; reuses /data-analysis fixest panel scaffolding


### [P2] `/synth-control (synthetic control / synthetic DiD)`

CONFIRMED thin (three list-mentions only), but deliberately deprioritized: the v2.0-backlog records an explicit, reasoned decision NOT to ship a standalone synthetic-control estimator skill, citing the risk that 'a plausible-but-wrong estimator launders authority.' Honor that decision — keep at P2 and, if built, build it as a verification-and-diagnostics wrapper (donor-pool/weight transparency, pre-fit balance, placebo/permutation inference) around a vetted package (synth, synthdid, scpi), NOT as a from-scratch estimator. Synthetic DiD (Arkhangelsky et al.) is the natural bridge to the DiD flagship and could alternatively live as a --synthetic note cross-referenced from /did-event-study.

*depends_on:* /did-event-study (synthetic DiD bridges to it); shared inference rule for placebo/permutation inference


## Extend generic (module, not a new skill)

- **Regression kink design** — _module within /rdd-analysis (or the shared quasi-experimental design rule)_ : CONFIRMED absent, medium priority. Do NOT build a standalone skill — kink shares continuity/local-polynomial logic with RDD. Add as an optional module inside /rdd-analysis once that flagship exists (it is a slope-change-at-threshold variant of the same machinery).
- **Bunching / notch design (excess-mass and counterfactual-density tests)** — _module within /rdd-analysis_ : CONFIRMED absent, medium priority and lower-frequency (labor/public econ niche). Saez(2010)/Kleven-Waseem framework is specialized; do not spin up its own flagship. Add as a narrow module within /rdd-analysis or the shared threshold/discontinuity rule, after IV and RDD ship.
- **Local projections / impulse-response / dynamic causal effects (Jorda 2005)** — _deferred module (future time-series-causal skill) — not /data-analysis_ : CONFIRMED absent, medium priority and mostly macro/time-series (less central to the applied-micro core the repo serves). Better as a future module than a standalone flagship; if a time-series-causal surface ever emerges, fold it there. Do not build ahead of the reduced-form trio.
- **Weak-instrument inference / many-instrument asymptotics** — _module within /iv-2sls + a paragraph in the shared quasi-experimental design + inference rule_ : CONFIRMED a real gap, but explicitly NOT a separate skill — it is core IV content. Fold Anderson-Rubin / Stock-Yogo / effective-F / many-instrument guidance directly into the /iv-2sls flagship and reference it from the shared inference rule. Listed here only to record the routing decision (extend the IV flagship, do not create a standalone surface).
- **LATE / MTE / complier interpretation** — _module within /iv-2sls_ : PLAUSIBLE gap; pedagogical and interpretive rather than a separate workflow. Ship as the 'what does IV identify' module of /iv-2sls (LATE vs ATE, monotonicity/exclusion/relevance, external-validity-only-on-compliers). Do not create a standalone skill.
- **Dynamic-panel GMM (Arellano-Bond / system GMM)** — _P2 module within /panel-models_ : CONFIRMED absent but lower-frequency (macro/finance/growth). Ship as a P2 module inside the /panel-models flagship (Nickell bias, lag structure, first-difference vs system GMM, instrument-count/overid diagnostics), not its own flagship.

## Consolidate / retire / fix

- **create-new-rule** (new file: .claude/rules/quasi-experimental-conventions.md (HARD/SHOULD companion for IV, RDD, matching/PS — the sibling to did-conventions.md)): The single highest-leverage coherence move. did-conventions.md proves the pattern: a deep skill needs a HARD-rule companion. Rather than each new method flagship (/iv-2sls, /rdd-analysis, /matching-weighting, /panel-models) re-deriving inference and robustness, create ONE shared design rule that states the per-method HARD guardrails and points to the existing inference-robustness.md for multiple-testing/clustering/spec-robustness substrate and to /power-analysis + /simulation-study for design-stage power. This is what 'depends_on' references throughout the flagship list. Build this rule first, then hang the skills off it. NOT a consolidation of existing surfaces — it is the missing connective tissue that keeps four new flagships mutually consistent and consistent with the DiD flagship.
- **leave (do NOT consolidate) — clarify positioning only** (.claude/skills/review-paper/SKILL.md, .claude/skills/seven-pass-review/SKILL.md): PLAUSIBLE overlap but recommendation is LEAVE with HIGH risk-if-changed. review-paper is the default; seven-pass is the heavier ~7x-token maximum-lens option for submission-ready/R&R papers. Both are load-bearing (review-paper --peer is used in cross-artifact pipelines; seven-pass is called by /slide-excellence for teaching papers). Do NOT merge. The only action is a one-line positioning clarification ('default to /review-paper; reach for /seven-pass-review only when maximum lens coverage justifies the token cost') so users stop confusing the two.
- **fix dead reference** (.claude/skills/deep-audit/SKILL.md:87): PLAUSIBLE low-stakes clarity fix. Line 87's prose 'rules/guide' reads as a literal path that does not exist; it means 'the rules and the guide.' Reword to the concrete targets (e.g. '.claude/rules/*.md and guide/workflow-guide.qmd') so the audit instruction is unambiguous. Not load-bearing, no user-facing API depends on it; aligns with the documented drift-hazard pattern (pet-peeve #18).
- **defer naming disambiguation (do NOT rename now)** (.claude/agents/claim-verifier.md, .claude/agents/verifier.md, .claude/agents/domain-referee.md, .claude/agents/domain-reviewer.md): Pure UX/clarity issue, ZERO functional overlap (CoVe-prose vs build-compilation; manuscript-peer-review vs slide-content-template). The similar names confuse new users but the agents own distinct surfaces and the names are not load-bearing conflicts. Defer a future rename (e.g. cove-verifier / build-verifier / manuscript-referee / slide-content-reviewer) to a later cleanup release; do not touch as part of the methods build-out.

## Leave as-is (already strong)

- /did-event-study + did-conventions.md — the proven flagship; the reference architecture, already gold-standard. Do not over-build around it; copy its pattern instead.
- /simulation-study + simulation-conventions.md + sim-reviewer — Monte Carlo capability already shipped (v1.10.0); reuse it as the engine for simulation-based power and method validation rather than re-implementing.
- /power-analysis — already routes non-closed-form designs (DiD, IV, panel) to the simulation harness; extend it from the new method skills, don't replace it.
- inference-robustness.md — already consolidates multiple-testing (Romano-Wolf / Anderson q-values), spec-multiverse, leave-one-out, and few-cluster inference. This is the shared inference substrate; new flagships should reference it, not duplicate it.
- audit-reproducibility + verify-claims — orthogonal verification surfaces (numeric-claim-vs-code vs CoVe-on-prose), both load-bearing; correctly separate.
- Review/verification/memory/context families (review-paper vs seven-pass, claim-verifier vs verifier, learn vs promote-memory, checkpoint vs compress-session vs context-status, visual-audit vs slide-excellence, domain-referee vs domain-reviewer) — all verified as intentional complementary layers, recommendation LEAVE. The coherence audit found no genuine consolidation targets; the work is additive (build missing methods), not subtractive.
- orchestrator-protocol.md fan-out -> reduce -> judge + hallucination-gate -> loop-until-dry runtime — mature and reusable; every new method flagship's review loop should plug into it unchanged.

## Recommended sequencing

1. FIRST build the connective tissue: create .claude/rules/quasi-experimental-conventions.md (the did-conventions.md sibling) that states per-method HARD guardrails and points to the existing inference-robustness.md and /simulation-study + /power-analysis harness. Every method flagship depends on this, so it must exist before the skills to avoid four divergent inference re-derivations.
2. Build /iv-2sls (P0) on the /did-event-study template, with weak-instrument inference and LATE/MTE folded in as modules. IV is the highest-frequency uncovered workhorse and its first-stage/compliers machinery is reused by fuzzy RD, so it precedes RDD.
3. Build /rdd-analysis (P0) — sharp + fuzzy; fuzzy reuses the IV first-stage from step 2. Kink and bunching attach later as optional modules here, not as separate skills.
4. Build /matching-weighting (P1) — selection-on-observables; conceptually reinforces the DiD doubly-robust foundation already in the repo and has zero current surface.
5. Build /panel-models (P1) — CRE/Mundlak + generic panel-FE guardrails, cross-referencing /did-event-study's 'no TWFE headline under staggered timing' boundary so the two never contradict; add dynamic-panel GMM as a P2 module afterward.
6. P2 / opportunistic: /synth-control only as a vetted-package verification wrapper (honoring the v2.0-backlog non-goal), plus the small kink/bunching/local-projections modules. Build only after the reduced-form trio (IV, RDD) and panel/matching are solid.
7. Cheap parallel cleanup (any time, non-blocking): fix the deep-audit:87 'rules/guide' dead-ref wording; add the one-line review-paper-vs-seven-pass positioning note. Defer the agent renames to a later cleanup release — do not bundle them with the methods build-out.

## Completeness critic (confidence: high) — blind spots no finder checked

- **RCT / field-experiment ANALYSIS workflow (balance, attrition, ITT/LATE, multiple arms, spillovers) — distinct from the design-stage /preregister + /power-analysis** → Build a /rct-analysis (a.k.a. /experiment-analysis) flagship on the /did-event-study template: pre-specified-analysis adherence check against the PAP, balance + differential-attrition tables (iebaltab/cobalt), ITT as headline + LATE/TOT via the IV first-stage, multiple-arm and multiple-outcome correction (reuse inference-robustness.md Romano-Wolf / Anderson q-values), clustered + randomization inference, and a heterogeneity/pre-registered-subgroup module. It closes the loop with the already-strong /preregister + /power-analysis design stage and inherits the shared quasi-experimental inference rule.
- **Structural estimation + welfare / counterfactual policy simulation (the ~20% structural slice's PRODUCTION surface)** → At minimum add a structural-conventions rule + a sufficient-statistics / welfare-counterfactual reporting checklist (identification of structural parameters, calibration-vs-estimation transparency, moment fit on non-targeted moments, counterfactual within covariate support, standard errors that propagate estimation uncertainty into welfare numbers, sensitivity to functional-form/distributional assumptions). A /structural-counterfactual or /welfare-simulation skill is the larger move; even the lightweight reporting rule would stop structural papers from inheriting only a reduced-form substrate. Note this is lower-frequency-per-paper but high-stakes (welfare claims drive policy).
- **Measurement / index construction / latent-variable methods (PCA, factor analysis, IRT, scale reliability, inter-rater agreement)** → Add a /measurement (index-construction) skill or at least a measurement-conventions rule: standardization and weighting choices, PCA/factor extraction and rotation, IRT for binary/ordinal items, reliability (Cronbach's alpha / omega), inter-rater reliability (kappa/ICC) for hand-coded data, and how measurement error propagates into downstream regressions (attenuation, EIV corrections). Cross-reference it from /data-analysis (which currently goes straight from load to regression with no construct-validity step).
- **Text-as-data / NLP-for-economics (scraping, dictionary methods, topic models, embeddings, LLM-as-annotator validation)** → Add a /text-as-data skill (or a textmeasurement-conventions rule): reproducible scraping + provenance/ToS capture, preprocessing decisions as researcher-degrees-of-freedom (tokenization, stemming, vocabulary cuts), dictionary vs supervised vs topic-model vs embedding measurement, and — critically for 2026 — a validation protocol for LLM-as-annotator pipelines (human-coded gold set, inter-rater agreement, measurement-error propagation into downstream regressions). This also has an integrity angle the repo cares about (reproducibility of a moving web corpus).
- **Missing-data methodology + survey/sampling weights (multiple imputation, MAR/MCAR/MNAR, raking/post-stratification, design weights)** → Add a /missing-and-weights skill or a survey-data-conventions rule covering: missingness diagnostics + mechanism reasoning (MCAR/MAR/MNAR), multiple imputation (mice/Amelia) vs complete-case vs IPW-for-missingness with the bias trade-offs, and complex-survey handling (design weights, strata/PSU, raking/post-stratification with survey/srvyr in R, svy: in Stata). Explicitly distinguish survey/design weights from the causal IPW/entropy-balancing weights in the planned /matching-weighting flagship so the two are not conflated.
- **AI-use / authorship disclosure and research-integrity norms (CRediT, COI, journal AI-disclosure statements) — NOT statistical disclosure** → Add a lightweight /submission-disclosures skill (or fold into /replication-package's README phase): generate an AI-use disclosure statement matching the target journal's policy, a CRediT contributor-roles block, a COI statement, and a data-availability statement. Pair with the journal-profiles reference so the statement matches venue policy. Low cost, high relevance to this specific toolkit's own positioning.
- **Causal mediation analysis (decomposing direct vs indirect effects; mechanism estimation)** → Add a causal-mediation module — most naturally a module inside the shared quasi-experimental inference rule or a /mechanism-analysis skill: natural direct/indirect effect estimation (mediation/CMAverse), the sequential-ignorability assumption and its implausibility, sensitivity analysis for mediator-outcome confounding, and an explicit 'do not just add the mediator as a control' bad-controls warning. Cross-reference from /review-paper's identification dimension.
- **Forecasting / nowcasting / out-of-sample predictive evaluation** → Defer, but record the routing: if a time-series-causal surface (local projections, per the action-map's deferred Jorda module) is ever built, fold forecasting/nowcasting evaluation (proper-scoring/loss, rolling-origin CV, Diebold-Mariano/Giacomini-White, nowcast revision triangles) in alongside it rather than spinning up a standalone flagship ahead of the reduced-form trio.
- **Reproducible-compute build orchestration (Make / targets / Snakemake pipeline DAGs) as a first-class artifact** → Add a build-orchestration module to /capture-environment or /replication-package: when to graduate from a linear 00_run_all to a targets (R) / Make / Snakemake DAG, how to express Table->script dependencies as build targets (mirroring the cross-artifact dependency graph the repo already documents), and how the DAG makes 'the package rebuilds from scratch deterministically' verifiable rather than asserted. Low effort, high payoff for the post-analysis lifecycle the repo already invests in.

### Critic disagreements with the synthesis

- PRIORITY MIS-WEIGHT — RCT analysis is under-counted. The action-map treats RCTs as fully served by /preregister + /power-analysis (design) and folds LATE/compliers into /iv-2sls. But the repo's own econ discipline-card makes field-experiments/RCTs the ONE paper type with MANDATORY preregistration (AEA RCT Registry), i.e. a self-declared first-class object. A toolkit that can design and power an RCT but cannot run the balance/attrition/ITT/LATE/multiple-arm analysis has a hole at least as large as the RD hole the map ranks P0. /rct-analysis deserves P0-P1, not silent absorption into /iv-2sls.
- SEQUENCING — /matching-weighting (selection-on-observables) is ranked P1 below the IV/RDD P0 flagships, but the action-map itself notes it is the conceptual sibling that strengthens the EXISTING DiD doubly-robust flagship (DRDID), and it is the substrate every observational-econ and adjacent-discipline paper needs. Given the repo's stated multi-discipline-template ambition (poli-sci shipped; psych/socio/public-health on the backlog), selection-on-observables generalizes far better across disciplines than IV/RDD do. I would argue it is effectively P0.5 — build it right after the shared inference rule and before RDD, because it has the highest reuse-per-build of the four new flagships.
- FRAMING GAP, not a ranking error — the action-map is explicitly and correctly scoped to the METHODS (estimator) axis and the COHERENCE axis, and it says so. My disagreement is that the headline ('gold standard for DiD, not yet for empirical econ in general') is stated as a methods-axis verdict but reads as a general verdict. The cross-cutting blind spots above (measurement, text-as-data, missing-data/weights, structural-welfare PRODUCTION, integrity/AI-disclosure) mean the gap to 'gold standard for empirical econ in general' is WIDER than the four-reduced-form-flagships story implies — even after IV/RDD/matching/panel all ship, the data-production and integrity surfaces would still be empty. The map should say so explicitly so a reader does not conclude 'four flagships ~= done.'
- SYNTHETIC CONTROL — agree with P2 and with honoring the documented 'plausible-but-wrong estimator launders authority' non-build decision. No disagreement on the verdict; I only note the map's own logic (wrap a vetted package, never re-implement the estimator) is exactly the right template for the structural-welfare and text-as-data blind spots too, where the from-scratch risk is even higher — the map could state that principle once as a reusable build-policy rather than per-skill.

## Full coverage matrix


**Quasi-experimental causal (non-DiD)**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| Instrumental variables (IV) / 2SLS / Two-stage least squares | thin | build-flagship | PLAUSIBLE |  |
| Weak-instrument inference / many-instrument asymptotics | thin | extend-generic | CONFIRMED |  |
| LATE (local average treatment effect) / Marginal treatment effect (MTE) | absent | build-flagship | PLAUSIBLE |  |
| Regression discontinuity design (RDD) — sharp and fuzzy | thin | build-flagship | PLAUSIBLE |  |
| Regression kink design / Kink estimator | absent | extend-generic | CONFIRMED |  |
| Bunching / Notch design (mass point & density tests) | absent | extend-generic | CONFIRMED |  |
| Synthetic control method / Synthetic DiD | thin | extend-generic | CONFIRMED |  |
| Matching / Propensity score methods / IPW (inverse probability weighting) | thin | build-flagship | CONFIRMED |  |
| Local projections / Dynamic treatment effects / Impulse-response analysis | absent | extend-generic | CONFIRMED |  |

**Panel / DiD-adjacent / causal-ML**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| Panel fixed effects & TWFE (Two-Way FE) | thin | extend-generic | PLAUSIBLE |  |
| Mundlak / Correlated Random Effects (CRE) | absent | build-flagship | CONFIRMED |  |
| Dynamic panel / GMM (Arellano-Bond, system GMM) | absent | build-flagship | CONFIRMED |  |
| Event-study (canonical focus) | flagship | leave | — | ✓ |
| Double / Debiased ML (DML), Chernozhukov-type approaches | absent | build-flagship | CONFIRMED |  |
| Causal forests / GRF (Athey-Wager) | absent | build-flagship | CONFIRMED |  |
| Heterogeneous treatment effects / CATE (conditional average treatment effects) | thin | extend-generic | CONFIRMED |  |
| Continuous-treatment / dose-response | adequate | extend-generic | — | ✓ |
| Local projections / lag-response dynamics | absent | leave | CONFIRMED |  |
| Regression discontinuity (RDD) / sharp & fuzzy designs | thin | build-flagship | CONFIRMED |  |
| Instrumental variables (IV / TSLS) | thin | build-flagship | PLAUSIBLE |  |
| Panel inference robustness (clustering, wild bootstrap, few-treated) | adequate | leave | — |  |
| Synthetic control & related methods | thin | build-flagship | CONFIRMED |  |
| Matching / propensity-score methods | thin | extend-generic | REFUTED |  |
| Covariate balance & covariate control (selection on observables) | adequate | extend-generic | — |  |
| Specification robustness / specification curves / multiverse | adequate | extend-generic | — |  |
| Simulation study (finite-sample properties, power, design validation) | flagship | leave | — |  |

**Structural / time-series / distributional**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| GMM / MLE / SMM estimation | absent | build-flagship | REFUTED |  |
| Discrete choice & demand (logit, BLP) | thin | extend-generic | PLAUSIBLE |  |
| Dynamic structural models & estimation | thin | extend-generic | REFUTED |  |
| Time-series econometrics (ARIMA, VAR, LP) | absent | build-flagship | CONFIRMED |  |
| Macro-econometrics (DSGE, GE, calibration) | thin | extend-generic | PLAUSIBLE |  |
| Quantile & distributional regression | absent | build-flagship | CONFIRMED |  |
| Spatial econometrics & network econometrics | thin | extend-generic | CONFIRMED |  |
| Bootstrap & resampling inference (wild, cluster, block) | adequate | leave | — |  |
| Heterogeneous treatment effects & effect modification | adequate | leave | — |  |
| Regression discontinuity & local methods | thin | extend-generic | PLAUSIBLE |  |
| Synthetic control & matching methods | thin | extend-generic | PLAUSIBLE |  |

**Pre-analysis research lifecycle**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| Research Ideation | flagship | leave | — |  |
| Literature Review | flagship | leave | — |  |
| Data Acquisition (APIs, web-scraping, admin data) | thin | extend-generic | PLAUSIBLE |  |
| Data Provenance & Licensing | adequate | leave | — |  |
| Data Cleaning & Wrangling | thin | extend-generic | PLAUSIBLE |  |
| Data Validation & Quality Assurance | thin | extend-generic | REFUTED |  |
| Power & MDE Calculation | flagship | leave | — |  |
| Pre-Registration & Pre-Analysis Plans | flagship | leave | — |  |
| Sampling & Sample Weights | thin | extend-generic | CONFIRMED |  |
| Data Management Planning | flagship | leave | — |  |

**Post-analysis research lifecycle**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| Regression tables & statistical exhibits (esttab/modelsummary conventions) | adequate | extend-generic | — |  |
| Figure production (ggplot2, visualization best-practices, readability standards) | thin | extend-generic | CONFIRMED |  |
| Scientific writing quality (prose, tone, hedge accuracy, AI-voice detection) | flagship | leave | — |  |
| Comprehensive manuscript review (single-pass, adversarial, simulated peer-review pipeline) | flagship | leave | — |  |
| Seven-pass review (7 parallel lenses, synthesized) | flagship | leave | — |  |
| Responding to referees (mapping referee concerns to revisions, classification, drafting responses) | flagship | leave | — |  |
| Replication packages (DCAS-compliant deposit, README, environment capture, Table→Script map) | flagship | leave | — |  |
| Disclosure/statistical-disclosure-limitation screening (pre-release data checking for restricted data) | flagship | leave | — |  |
| IRB/human-subjects oversight (protocol design, consent, data minimization) | adequate | extend-generic | — |  |
| Journal submission & manuscript formatting (journal-specific conventions, submission checklists) | thin | extend-generic | PLAUSIBLE |  |
| Environment capture & computational reproducibility (lockfiles, seeds, session info) | flagship | leave | — |  |
| Verification of numeric claims (audit-reproducibility, tolerance contracts, EXPLAINED mechanism) | flagship | leave | — |  |
| Bibliography validation & citation consistency (structural + semantic audit) | adequate | leave | — |  |

**Inference, robustness & computation**

| topic | status | recommendation | verify | pedro |
|---|---|---|---|---|
| Cluster-Robust & HAC Standard Errors | adequate | extend-generic | — |  |
| Multiple Testing Correction (Romano-Wolf, Sharpened-q, Anderson FDR) | flagship | leave | — |  |
| Randomization & Permutation Inference | thin | extend-generic | PLAUSIBLE |  |
| Bootstrap & Wild-Cluster Bootstrap | adequate | extend-generic | — |  |
| Specification Curve & Sensitivity Analysis | thin | build-flagship | PLAUSIBLE |  |
| Partial Identification & Bounds | absent | na | REFUTED |  |
| Reproducibility: Seeds, Environment Capture, Containers | flagship | leave | — |  |
| HPC, Parallel Workflows, Large-Data Scaling | thin | extend-generic | REFUTED |  |
| DiD-Specific Diagnostics & Sensitivity (Pedro Sant'Anna Vault) | flagship | leave | — | ✓ |
| Data Validation & Panel Balance Checking | adequate | extend-generic | — |  |
| Cross-Artifact Verification (Code ↔ Manuscript Numeric Claims) | flagship | leave | — |  |

## Coherence findings


**Redundancy / overlapping surfaces**

- [overlap→leave —] Review/audit family: deep-audit, seven-pass-review, review-paper, and review-r span mechanical checks, parallel adversarial lenses, and comprehensive pipelines with overlapping scope.
- [overlap→leave —] Verification family: verify-claims and audit-reproducibility both implement verification gates but target different factual-type domains (citations/literature vs numeric-claim reproducibility).
- [overlap→leave —] Claim-verifier vs verifier agents: claim-verifier (forked, fresh-context CoVe) and verifier (TikZ/compilation checks) are DISTINCT agents with no functional overlap despite similar names.
- [overlap→leave —] Context/session family: checkpoint, compress-session, and context-status are COMPLEMENTARY, not overlapping. checkpoint is explicit stop-point snapshot; compress-session is forced distillation before auto-compact; context-status is a read-only health check.
- [overlap→leave —] Memory family: learn and promote-memory are a two-stage pipeline (capture → promotion), not duplicative. learn extracts skills from sessions; promote-memory runs a five-critic council to decide what enters MEMORY.md (generic) vs stays in personal-memory.md (local).
- [overlap→leave —] Referee/review agents: domain-referee (manuscript disposition-primed substantive reviewer) and domain-reviewer (slide template reviewer for pedagogical correctness) are DISTINCT despite similar names.
- [depth-gap→leave —] Visual-audit skill (Quarto/Beamer layout) vs slide-excellence orchestrator: visual-audit is a single lens; slide-excellence fans out visual-audit + pedagogy-review + proofread in parallel.
- [naming→leave —] Three agents with similar names in different contexts could confuse new users: claim-verifier (CoVe prose), domain-referee (manuscript peer-review), domain-reviewer (lecture content template).

**Dead / stale cross-references**

- [dead-ref→fix PLAUSIBLE] Dead reference to 'rules/guide' which does not exist
- [other→leave —] Retired skills `/prompt` and `/prompt-only` are correctly documented as historical references, not dead cross-references

**Surface-count drift**

- [count-drift→fix CONFIRMED] CHANGELOG v2.0.0 asserts '30 rules' but README, guide, and on-disk inventory show 32 rules
- [count-drift→leave REFUTED] Briefing document claims 51 skills but repository contains 50; README correctly asserts 50
- [count-drift→leave CONFIRMED] Briefing claims 33 rules but repository contains 32; README correctly asserts 32

**Rule contradictions & depth asymmetry**

- [contradiction→consolidate REFUTED] BEAMER-QUARTO-SYNC vs. SINGLE-SOURCE-OF-TRUTH conflict on handling manual Quarto edits
- [depth-gap→fix —] DID-CONVENTIONS has 'insanely high' 73-line standard with numeric tolerances (1e-6), HonestDiD + didFF mandatory, exact bootstrap iterations (25000 for publication); INFERENCE-ROBUSTNESS gives generic 3-paragraph guidance on specification robustness with no methodology names, no numeric standards, no enforcement mechanism.
- [contradiction→fix —] QUALITY-GATES § thresholds are 'advisory' (80/90/95 in harness, real enforcement only post-hook install); DID-CONVENTIONS requires exact numeric precision (1e-6 point estimates, 1e-6 SEs) with no opt-out.
- [dead-ref→fix REFUTED] CONTENT-INVARIANTS § INV-6 references no-pause-beamer.md but NO-PAUSE-BEAMER gives zero rationale, contradicting the pedagogical design of other invariants.
- [depth-gap→consolidate REFUTED] REPLICATION-PROTOCOL has heavyweight passport.yaml system (PASS/FAIL/EXPLAINED/STALE/UNVERIFIED statuses, git integration with /commit enforcement). INFERENCE-ROBUSTNESS on specification robustness has only prose guidance with no tracking mechanism.
- [contradiction→consolidate —] VERIFICATION-PROTOCOL (task completion, mechanical: 'did the PDF render?') vs. POST-FLIGHT-VERIFICATION (hallucination, semantic: 'did the literature claim hold?') — both called 'verification' but measuring opposite things.
- [overlap→consolidate —] DID-CONVENTIONS § Verification (R as benchmark, 1e-6 tolerance) duplicates replication-protocol.md § Phase 3 (tolerance thresholds, PASS/FAIL status tracking) with different language and enforcement.
- [overlap→leave —] TIKZ-MEASUREMENT.md (six-pass protocol with Pass 0-6 systematic checks) and TIKZ-PREVENTION.md (rules P1-P6 about not writing colliding TikZ in the first place) and TIKZ-VISUAL-QUALITY.md (label positioning, visual semantics) — all three rules govern TikZ but at different stages (design/authoring vs. review vs. measurement).
- [naming→fix —] SESSION-LOGGING.md defines 'Quality Reports' (line 57-59) as merged-time artifacts, but ORCHESTRATOR-PROTOCOL.md line 6 references 'Step 6: SCORE — quality_score.py / hard-gate roll-up', suggesting quality reports are generated on every run of the review loop.
- [depth-gap→leave —] MODEL-ROUTING.md gives detailed 70/20/10 allocation and effort-axis guidance for cost optimization. NO comparable cost/effort guidance exists for other dimensions (e.g., should a literature review use Sonnet or Haiku? should a slide audit be low/medium/high effort?).

**Naming / discoverability / frontmatter**

- [overlap→fix —] Two skills (context-status, deep-audit) are missing the optional 'argument-hint' frontmatter field, while most peers include it. Neither skill takes arguments, but inconsistency signals they may have been created before the field became standard.
- [naming→leave —] Skill naming conventions are inconsistent across three patterns: imperative verbs (audit-reproducibility, compile-latex), nouns (syllabus, checkpoint), and adj-noun compounds (slide-excellence, seven-pass-review). No single pattern dominates. This creates mild cognitive friction when users scan the full skill list, as some skills look like commands and others like objects.
- [dead-ref→fix —] The skill r-package-check claims in its description to 'produce a check report + CRAN-submission checklist' (lines 1-2 of SKILL.md), yet its allowed-tools field does not include 'Write' or 'Edit'. This creates a discrepancy: the frontmatter promises written output, but the declared tools don't include writing capabilities.
- [count-drift→fix —] The prompt inventory states '51 skills' but the actual directory count is 50. The discrepancy arises because 'learn' is a template/example skill (at .claude/skills/learn/SKILL.md) that contains placeholder names ('descriptive-kebab-case-name', 'fixest-missing-covariate-handling') in its body, not a deployed skill. The learn/SKILL.md file itself uses 'name: learn' in the frontmatter, but its body serves as a tutorial showing users how to create skills, not a live skill.
- [other→leave —] Eight v2.0 skills appear after the v1.10.0 skills in the README comprehensive table, grouped at the end (lines 258-271). This creates a discovery friction: users scanning the README table quickly may assume newer skills stop after the '(v1.10.0)' section and miss power-analysis, replication-package, did-event-study, capture-environment, disclosure-check, grant-proposal, data-management-plan, coauthor-brief, triage-inbox, syllabus, teach-from-paper, respond-to-eval, scaffold-exercises, and new-skill. A user skimming to 'most recent' would have to scan down further.

---

## Decisions (2026-06-09)

- **Methods build-out DEFERRED.** Coverage gaps confirmed (the reduced-form trio: DiD shipped; IV, RD, matching/PS, panel-CRE missing) but the build program is not started this session. The full prioritized map above is the standing roadmap.
- **When built, priority order is (critic-adopted):** Step-0 `quasi-experimental-conventions.md` rule → `/iv-2sls` (P0) → **`/matching-weighting` (moved ahead of RDD** — selection-on-observables generalizes across disciplines and reinforces the existing DiD-DR foundation) → `/rdd-analysis` (P0, fuzzy reuses IV first-stage) → `/panel-models` (P1) → **`/rct-analysis` is a first-class P0** (field experiments are the only mandatory-prereg paper type; not absorbed into IV's LATE module). `/synth-control` stays P2, wrapper-only (honors the documented "plausible-but-wrong estimator launders authority" non-goal).
- **Bar distinction:** only DiD carries Pedro's name (1e-6-against-his-own-packages). The new method flagships are COMMUNITY-STANDARD — built by orchestrating the canonical vetted packages (rdrobust, ivreg/ivDiag, MatchIt/WeightIt, fixest), never reimplementing, validated against those packages — NOT to the DiD 1e-6 bar.
- **Wider program (completeness critic, high confidence):** even after the method flagships, data-production + integrity surfaces stay empty — measurement/index construction, text-as-data (incl. LLM-as-annotator validation), missing-data + survey weights, structural-welfare production checklist, AI-use/authorship disclosure, reproducible-compute DAGs. These are later phases, not "four skills ≈ done."
- **This session:** coherence cleanup only — CHANGELOG rule-count drift (30→32, +2→+4 rules) and deep-audit:87 "rules/guide" wording. r-package-check `Write` and argument-hint findings inspected and intentionally NOT changed (gate-green non-issues).
