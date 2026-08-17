# REVIEW_REQUIRED — DYNAMIC-001 v1.2.1 Exploratory Correction

## 1. What happened

The frozen v1.2.1 diagnostic correction was implemented against the exact
frozen v1.2 raw operator states for seeds 101–120. The v1.2 operator was not
recomputed. Corrected label-free diagnostics were serialized before loading
evaluator-only metadata.

## 2. Relevant metrics

- Input/raw source samples: 120
- Scenarios: D1–D6, 20 each
- Corrected raw diagnostic files: 120
- Diagnostic records: 120
- Registered windows: 5, 15, 30 seconds
- Window distances for `t < W`: explicitly `null`
- D6 pair restoration: fixed reference, similarity threshold 0.80, at least 5/6 pairs for 15 seconds
- Simulator/operator recomputation: no
- Confirmatory/held-out seeds: not executed
- Repository, schema, determinism, ordering, and frozen-hash checks: passed

These are execution and integrity metrics only. No scientific performance
metric or GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision is made.

## 3. Why automatic continuation stopped

The authorized task requires review after the diagnostic correction and before
any extension or scientific interpretation.

## 4. Options available

- Review the corrected valid-window aggregates.
- Review D6 operator recovery and pair-reformation diagnostics.
- Compare corrected diagnostics with the frozen v1.2 record without rewriting it.
- Authorize a narrowly scoped follow-up only after review.

## 5. Recommended scientifically conservative next action

Inspect the corrected diagnostics and verify that the non-trivial D6 rule is
appropriate. Preserve both v1.2 and v1.2.1 records; make no scientific
decision or extension until explicit review authorization.
