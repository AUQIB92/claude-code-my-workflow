# Discipline Cards

Short reference cards naming each discipline's dominant paper-type frequencies, top journals, preregistration norms, and method conventions. Read by `/research-ideation`, `/interview-me`, `/preregister`, and the `editor` agent (in `/review-paper --peer`) when the user gives a `paper_type` or domain hint without specifying a target journal.

**Scope.** Four cards ship: **computer science**, **economics**, **mathematics**, and **political science**. Other social sciences (psychology, sociology, public health) are deferred to a later release. To add your own discipline, copy a card section, fill the four fields (paper-type frequencies, journals, preregistration norms, method conventions), and reference the new short-name from `journal-profiles.md` and `methods-referee.md`.

> **⚠️ CS and mathematics break two assumptions baked into the econ-derived tooling.** (1) CS is **conference-first**: the review model is a program committee with a fixed deadline and an author rebuttal, ending in accept/reject — there is no revise-and-resubmit. `/review-paper --peer` simulates the journal model (editor → 2 referees → R&R) and will therefore simulate the *wrong process* for a CS submission. (2) Mathematics is **proof-first**: preregistration, standard errors, and replication packages are largely inapplicable; correctness is established by proof, not by data. Read the two cards below before pointing a peer-review skill at work in either field.

**Maintenance.** When you add a journal profile to `journal-profiles.md`, cross-reference it here. When you add a paper type to `methods-referee.md`, cross-reference it here.

---

## Computer Science (`cs`)

**Paper-type frequencies (rough share across the major venues; CS is far more subfield-partitioned than econ, so these are indicative rather than a single population).**

| Type | Share | Notes |
|---|---|---|
| Systems / empirical | ~30% | Build-a-system-and-measure-it: OS, networking, storage, databases. Evaluation section is the load-bearing part. |
| ML / empirical | ~30% | Benchmark-driven. Ablations, seeds, and error bars are the credibility currency. |
| Algorithms / theory | ~20% | Proof-based: correctness + complexity bounds. No data, no evaluation section. |
| PL / formal methods | ~10% | Type systems, semantics, verification. Often proof + implementation. |
| HCI / user study | ~10% | Human-subjects; the one CS corner with social-science-style stats and IRB. |

**Dominant venues — conferences, not journals.** ML: NeurIPS, ICML, ICLR. Systems: SOSP, OSDI, NSDI, EuroSys. Networking: SIGCOMM. Theory: STOC, FOCS, SODA. PL: POPL, PLDI, OOPSLA. Security: IEEE S&P ("Oakland"), USENIX Security, ACM CCS. HCI: CHI, UIST. Databases: SIGMOD, VLDB.

Journals exist (*CACM*, *JACM*, ACM *TOPLAS*/*TOCS*/*TODS*, IEEE *TSE*) but are generally **not** where a result is first published — they carry extended versions, surveys, and some theory. Treating a CS journal as the primary target is usually a category error.

**Review-process norms (this is the big structural difference).**
- **Program-committee review** against a hard deadline. Typically 3–5 reviewers, double-blind at most major venues.
- **Author rebuttal / response period** — a short window to answer reviewers before the final decision. This is the CS analogue of an R&R, but it is days long and cannot include new experiments at most venues.
- **Outcome is accept / reject** (sometimes with shepherding or a "major revision" track at a few venues, e.g. VLDB, TMLR). There is no multi-round R&R culture.
- **Artifact evaluation** is the reproducibility mechanism, replacing the econ replication-package model. ACM badging: *Artifacts Available*, *Artifacts Evaluated — Functional / Reusable*, *Results Reproduced*. Often a separate committee and a separate deadline after acceptance.

**Preregistration norms.**
- Broadly **not a norm** in systems, ML, theory, or PL.
- **HCI / human-subjects work** is the exception — OSF preregistration is increasingly expected, alongside IRB approval.
- ML venues instead use **submission checklists** (the NeurIPS paper checklist and similar) covering reproducibility, compute, limitations, and broader impact — a checklist culture, not a registry culture.

**Method conventions.**
- Significance stars are uncommon; ML reports **mean ± std over seeds**, systems reports percentiles (p50/p95/p99) and throughput/latency curves.
- Report hardware, compute budget, and software versions — the systems/ML analogue of a standard-error convention.
- **arXiv preprinting is near-universal** and compatible with double-blind at most venues (policies vary — check the specific CFP).
- Code: **Python** dominates ML; **C/C++** systems; **Rust** rising in systems/PL; **Java** in some SE/DB work.

**Cross-references.** `methods-referee.md` paper types: reduced-form and structural do **not** apply — the useful analogues are formal-theory (for algorithms/PL) and descriptive (for measurement studies); systems/ML empirical work needs its own type. `journal-profiles.md`: **JACM** (theory), **TSE** (empirical software engineering) — genuine journals only; conferences need the not-yet-built `--conference` mode, see the warning at the top of the CS journal-profiles section.

---

## Economics (`econ`)

**Paper-type frequencies (rough share of empirical work in top-5 journals).**

| Type | Share | Notes |
|---|---|---|
| Reduced-form | ~55% | DiD, IV, RD, event study, synthetic control. The dominant mode. |
| Structural | ~20% | DSGE, GE, IO empirical. Concentrated in macro / IO / labour. |
| Theory + empirics | ~15% | Theory-paper-with-empirical-test or empirical-paper-with-theory-section. |
| Descriptive | ~5% | Measurement / data-construction. Often the AEA P&P route. |
| Formal-theory | ~5% | Pure theory (micro, IO, contracts). More common in ECMA / TE / JET. |

**Dominant journals (shipped in `journal-profiles.md`).** AER, QJE, JPE, ECMA, ReStud. AEA P&P (proceedings) for descriptive / measurement work.

**Preregistration norms.**
- **Field experiments / RCTs:** mandatory in the **AEA RCT Registry** since 2018 for AEA-journal submission. Use `/preregister --style aea-rct`.
- **Lab experiments:** OSF / AsPredicted increasingly common; not yet uniformly required.
- **Observational / archival:** preregistration uncommon; pre-analysis plans appearing in some applied-micro corners.
- **Replication packages:** AEA Data and Code Availability Policy enforced; replication archive at JEL data archive.

**Method conventions.**
- Significance stars: AEA journals do **NOT** use stars in tables (since 2018 AEA Code style guide). Other journals (e.g., ReStud, JPubE) still allow them.
- Standard-error reporting: clustered SEs at treatment-assignment level expected; Conley / spatial SEs required for spatial data.
- Code: R, Stata, Python, Julia all accepted; replication packages must be self-contained and deterministic (`set.seed`).

**Cross-references.** `methods-referee.md` paper types: reduced-form, structural, theory+empirics, descriptive, formal-theory. `journal-profiles.md`: AER, QJE, JPE, ECMA, ReStud.

---

## Mathematics (`math`)

**Paper-type frequencies.**

| Type | Share | Notes |
|---|---|---|
| Pure / proof-based | ~75% | A theorem and its proof. No data, no evaluation, no statistics. The dominant mode. |
| Applied / numerical | ~15% | PDEs, numerical analysis, optimization. May include convergence experiments. |
| Computational / experimental | ~5% | Computer-assisted search or verification (e.g. large case checks); the result is still a theorem. |
| Expository / survey | ~5% | *Bulletin of the AMS*, *Notices*, *American Mathematical Monthly*. |

**Dominant journals.** *Annals of Mathematics*, *Journal of the AMS*, *Inventiones Mathematicae*, *Acta Mathematica*, *Duke Mathematical Journal*. Strong subfield outlets are the norm and carry real prestige. Mathematics is genuinely **journal-first** — the opposite of CS.

**Review-process norms.**
- Single referee is common (sometimes two); **not** blinded in practice, since arXiv preprinting precedes submission almost universally.
- **Review times are long** — commonly 6 months to 2+ years at top journals, because refereeing means verifying a proof line by line.
- Outcome is accept / revise / reject, but "revise" usually means *fix this gap in the argument*, not *run more analysis*.

**Preregistration norms.**
- **Not applicable.** There is no registry culture, and no meaningful sense in which a proof can be preregistered. `/preregister` should not be offered for `math` work.
- The functional analogue of a replication package is a **formalization** (Lean 4 / mathlib, Coq, Isabelle) — still rare but growing fast, and increasingly requested for results with long or computer-assisted case analyses.

**Method conventions.**
- No significance stars, no standard errors, no confidence intervals — correctness is binary and established by proof.
- **arXiv preprint first** is near-universal (math.* categories); MathSciNet / zbMATH carry post-publication reviews.
- LaTeX with `amsmath` / `amsthm` is universal; AMS style governs theorem environments and citation format.
- Numbered theorem/lemma/definition environments with explicit cross-referencing are the structural backbone — dependency between results is the thing a referee traces.
- Code: mostly absent. Where present: SageMath, Mathematica, Magma, GAP (computational); Lean 4 / Coq / Isabelle (formalization).

**Cross-references.** `methods-referee.md` paper types: **formal-theory** is the only one that applies; reduced-form / structural / survey-experiment are meaningless here. `journal-profiles.md`: **Annals**, **JAMS**, **Inventiones**.

---

## Political Science (`poli-sci`)

**Paper-type frequencies (rough share of empirical work in top-3 journals).**

| Type | Share | Notes |
|---|---|---|
| Reduced-form | ~40% | Causal inference (DiD, IV, RD), observational identification. Strongest at AJPS. |
| Survey-experiment | ~25% | Vignette, conjoint, list-experiment, factorial. Strong at AJPS, JOP; rising at APSR. |
| Formal-theory | ~15% | Game-theoretic, mechanism-design, formal political theory. Strongest at APSR. |
| Descriptive | ~10% | Cross-national / historical / case-study description. |
| Theory + empirics | ~10% | Formal theory with empirical test of equilibrium predictions. |

**Dominant journals (shipped in `journal-profiles.md`).** APSR, AJPS, JOP. Subfield outlets (IO, World Politics, JOP-research-notes track) also strong.

**Preregistration norms.**
- **Survey experiments / lab experiments / field experiments:** OSF or AsPredicted increasingly expected. **AJPS Replication Policy** (since 2015) makes replication archive mandatory at acceptance, but preregistration itself is a community norm not a hard requirement.
- **Observational:** PAP (preanalysis plan) appearing in applied work; not yet uniform.
- **AEA RCT Registry** is for econ; political-science field experiments more often use OSF or EGAP's repository (egap.org) — though EGAP merged its registry into OSF in 2022.

**Method conventions.**
- Significance stars: ARE used (typical floor 0.05/0.01/0.001). APSA Style Manual governs citations.
- Standard-error reporting: clustered SEs at subject level for survey experiments, robust SEs (HC2 or HC3) standard.
- Replication archive: AJPS Replication Policy requires deposit before acceptance; APSR and JOP recommend.
- Code: R is dominant; Stata still common in IR / comparative; Python rising for text-as-data work.

**Cross-references.** `methods-referee.md` paper types: reduced-form, formal-theory, survey-experiment, theory+empirics, descriptive (structural is rare in poli-sci). `journal-profiles.md`: APSR, AJPS, JOP.

---

## How skills consume these cards

- **`/research-ideation`** — when the user names a topic without a discipline, the skill may infer one from context (citation style, vocabulary). The card supplies the default `paper_type` distribution to bias hypothesis generation.
- **`/interview-me`** — Phase 1 paper-type question uses the card's frequency table to order the option list (most-likely-first per discipline).
- **`/preregister`** — `--style` defaults to the card's preregistration-norms suggestion (e.g., `osf` for poli-sci, `aea-rct` for econ field experiments). **Not offered for `math`**; for `cs`, only meaningful for HCI/human-subjects work.
- **`editor`** (`/review-paper --peer`) — when the user gives `--peer` without naming a specific journal but with a discipline hint, the editor uses the card's "Dominant journals" list as the candidate set and asks for clarification. **For `cs`, the editor must select a *conference* and use the PC-review + rebuttal model, not the journal R&R model** — see the warning at the top of this file.

---

## Adding a new discipline card

Copy this template:

```markdown
## [Discipline name] (`short-slug`)

**Paper-type frequencies.**
| Type | Share | Notes |
|---|---|---|
| ... |

**Dominant journals (shipped in `journal-profiles.md`).** [list]. [Optional: subfield outlets.]

**Preregistration norms.**
- [registry conventions per study type]

**Method conventions.**
- [significance stars / SE conventions / replication norms / dominant code language]

**Cross-references.** `methods-referee.md` paper types: [list]. `journal-profiles.md`: [list].
```

Then:

1. Add the card section above (alphabetically by short-slug).
2. Add concrete journal profiles to `journal-profiles.md` for at least the top-3 journals.
3. Add paper types to `methods-referee.md` if your field uses categories not already there (e.g., qualitative-case-study for sociology, mixed-methods for public health).
4. Cross-reference the new short-slug from `/research-ideation` and `/interview-me` if those skills should respect the new defaults.

---

## Where this file lives

- **File:** `.claude/references/discipline-cards.md`
- **Schema parallel:** `.claude/references/journal-profiles.md` (per-journal) and `.claude/references/audit-pet-peeves.md` (living-catalogue format).
- **Consumed by:** `/research-ideation`, `/interview-me`, `/preregister`, `editor` agent.
