# REVIEW_REQUIRED — DYNAMIC-001 v1.2 Exploratory Run

## 1. What happened

The frozen v1.2 spatiotemporal relational Laplacian was implemented and run
against unchanged DYNAMIC-001 v1.0 algorithm-visible exploratory data. Seeds
101–120 only were used. Raw label-free operator states were serialized before
evaluator-only metadata was loaded. The run produced 120 raw samples and 120
diagnostic records, with 20 samples for each D1–D6 scenario.

## 2. Relevant metrics

- Input samples: 120
- Scenarios: D1–D6, 20 samples each
- Registered windows: 5, 15, 30 seconds
- Raw output files: 120
- Diagnostic records: 120
- Simulator changed: no
- Classifier or learned parameter: no
- Confirmatory/held-out seeds: not executed
- Leakage/schema and determinism checks: passed

These are execution and integrity metrics only. No scientific performance
metric or decision is interpreted here.

## 3. Why automatic continuation stopped

The frozen task requires review immediately after exploratory execution and
before any extension, benchmark, classifier, confirmatory run, or scientific
GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision.

## 4. Options available

- Review D1/D2 invariance diagnostics.
- Review D4 hard-control behavior across occupancy windows.
- Review D5 rigid versus shape/motion/occupancy behavior.
- Review D6 operator-space recovery and reformation diagnostics.
- Authorize a narrowly specified follow-up only after review.

## 5. Recommended scientifically conservative next action

Inspect the frozen raw outputs and diagnostics, verify D4/D5/D6 operator
behavior, and make no extension or scientific decision until human review
explicitly authorizes it.
