# REVIEW_REQUIRED — TFL-ORG-RECHECK-001 v1.0 Exploratory Run

## 1. What happened

The frozen pilot was implemented on the selected historical
DYNAMIC-001 algorithm-visible track source. Conditions A and B were derived
without evaluator metadata. For all 120 samples and 181 timestamps, raw G/R/P
outputs were serialized before any evaluator interpretation. The source data
was not modified.

## 2. Relevant metrics

- Selected source samples: 120
- Stable tracks per sample: 4
- Timestamps per sample: 181
- Raw G/R/P output files: 120
- Condition A outputs: 120 × 181 timestamps
- Condition B valid 2-switch timestamps: 18,565
- Evaluator metadata loaded: no
- Classifier/learned representation: no
- Confirmatory/held-out execution: no
- Schema, determinism, source-count, and frozen-hash guards: passed

These are execution and integrity metrics only. Cross-over measurements are
not interpreted and no authorized outcome is assigned.

## 3. Why automatic continuation stopped

The protocol requires raw outputs to be frozen before evaluator interpretation
and requires human review before assigning either permitted high-level outcome
or extending the pilot.

## 4. Options available

- Review G/R/P outputs for Condition A.
- Review the availability and behavior of the preregistered Condition B
  degree-preserving 2-switch.
- Review trivial-marginal checks and projector degeneracy handling.
- Authorize a narrowly scoped follow-up only after review.

## 5. Recommended scientifically conservative next action

Inspect the frozen raw outputs and diagnostics, verify that the selected
historical source supports the preregistered constructions, and assign no
scientific outcome until explicit human review.
