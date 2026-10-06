# Symbolic Verification: JKSSB Unit 1

**Date:** 2026-10-11  
**Artifacts:** Unit 1 Notes and practice answer keys  
**SymPy version:** 1.14.0  
**Claim inventory:** [`symbolic_claims_JKSSB_Unit1.json`](./symbolic_claims_JKSSB_Unit1.json)

## Summary

| Status | Count |
|---|---:|
| PASS (exact arithmetic / radix conversion) | 46 |
| PASS (encoding lookup / exhaustive truth table) | 2 |
| PASS (numeric substitution only) | 0 |
| FAIL | 0 |
| UNTRANSLATABLE / AMBIGUOUS | 0 |
| **Inventory entries** | **48** |
| **Overall verdict** | **PASS** |

Exact rational arithmetic was used for averages, the Lesson 01 percentage,
rates, and the binary fraction. Integer arithmetic and exact base conversion
were used for the integer conversions, BCD digit encodings, capacity ladder,
and channel counts. The ASCII character code is a standard encoding lookup,
not a symbolic computation. Boolean truth tables were exhaustively evaluated
over all four pairs of binary inputs. All 48 inventory entries passed.
Multiple inventory entries can be validated by one exact check when they
state the same operation in different artifacts.

## Claims checked

The audit covers the arithmetic and base-conversion examples in the
Lesson 01, 03, and 50 Notes, including the added percentage, MB/s conversion,
and 1024-based GB/TB examples, plus numeric claims in the Lesson 03 and 50
answer keys. The inventory records each checked claim's artifact location,
expression, and claimed result.

## Next steps

No arithmetic or base-conversion corrections are required. This audit does
not independently establish the identity or provenance of official PYQs;
those are sourced separately to the official JKSSB paper booklets and
answer-key records.
