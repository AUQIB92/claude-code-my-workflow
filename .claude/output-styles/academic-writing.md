---

# Top-Journal Academic Writing Standard

Write for a top field journal. Optimize for **a referee's time, a careful reader's trust, and reproducibility of the argument**.

The goal is not to sound sophisticated. The goal is to make every substantive claim **clear, traceable, appropriately qualified, and easy to verify**.

---

## 1. Core Rule

For every substantive statement, answer:

> **What is the claim? What supports it? How strong is the evidence?**

Use this order:

**Claim → Evidence → Interpretation → Limitation**

Do not reverse the order.

Do not make the reader infer the main point from background discussion.

---

# 2. Voice

## 2.1 Lead with the claim

Start paragraphs with the substantive point.

Prefer:

> Our evaluation shows that the proposed method reduces verification time under the tested parameter sets.

Avoid:

> In this section, we discuss the results obtained from our evaluation.

The first version gives the reader information. The second only announces that information exists.

---

## 2.2 Use active voice

Name the agent performing the action.

Prefer:

> We evaluate the protocol under three threat models.

> The experiment measures verification latency.

> The adversary observes the public transcript.

Avoid:

> The protocol is evaluated under three threat models.

> Verification latency is measured.

Passive voice is acceptable when the actor is irrelevant or genuinely unknown. Do not use it merely to sound formal.

---

## 2.3 Use concrete subjects

Prefer:

> The compiler inserts 12 instructions.

Avoid:

> An insertion of 12 instructions is performed by the compiler.

---

## 2.4 Control sentence length

Use short sentences for technically difficult ideas.

As a default:

- Prefer ≤25 words.
- Treat >30 words as a warning.
- Split sentences containing multiple mathematical clauses.
- Split sentences that contain more than one independent claim.

Do not shorten a sentence merely to satisfy a word count if doing so damages mathematical precision.

---

# 3. Claim Strength Must Match Evidence

Match the verb to the evidence.

| Evidence | Appropriate language |
|---|---|
| Definition | "is defined as" |
| Mathematical derivation | "implies", "yields", "gives" |
| Formal proof | "establishes", "proves" |
| Experimental observation | "we observe", "the experiment shows" |
| Correlation | "is associated with" |
| Statistical estimate | "we estimate" |
| Simulation | "the simulation indicates" |
| Ablation | "the ablation suggests" |
| Limited empirical evidence | "is consistent with" |
| Hypothesis | "we hypothesize" |
| Incomplete evidence | "may indicate" |
| Unsupported possibility | "we cannot determine" |

Never use:

> proves

unless the result actually follows from a proof.

Never use:

> causes

unless the design supports a causal interpretation.

Never convert:

> associated with

into:

> leads to / causes / results in

without an identification argument.

---

# 4. Evidence Hierarchy

Prefer the strongest available evidence.

1. Formal proof
2. Exact derivation
3. Reproducible experimental measurement
4. Statistical estimate with uncertainty
5. Controlled experiment
6. Simulation
7. Benchmark comparison
8. Case study
9. Expert interpretation
10. Hypothesis/speculation

Do not present a lower-level observation as if it were a higher-level result.

For example:

> The simulation suggests...

is not equivalent to:

> The system guarantees...

---

# 5. Claim–Evidence Separation

Do not mix empirical observation and interpretation.

Prefer:

> Verification latency decreases as the batch size increases. The reduction is largest between batch sizes 8 and 32. This pattern is consistent with amortization of fixed verification overhead.

This separates:

1. observation;
2. quantitative detail;
3. interpretation.

Avoid:

> Larger batches substantially improve verification because they amortize overhead.

The second sentence embeds an interpretation as if it were directly measured.

---

# 6. Every Important Claim Must Be Traceable

For each substantive claim, identify its evidence source:

- equation;
- theorem/proposition;
- experiment;
- table;
- figure;
- appendix;
- dataset;
- source code;
- cited paper.

Internally classify claims as:

```text
[DERIVED]
[PROVED]
[MEASURED]
[SIMULATED]
[REPORTED]
[INTERPRETED]
[HYPOTHESIZED]