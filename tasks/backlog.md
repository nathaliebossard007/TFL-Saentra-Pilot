# Research Backlog

## P0

- [x] Import frozen TFL-UAS-001A predecessor.
- [x] Verify archive structure.
- [x] Verify available hashes.
- [x] Record frozen experiment lineage.
- [x] Mark predecessor immutable.

## P1

- [x] Specify and freeze TFL-UAS-001B protocol v1.0.
- [x exploratory] Build four-object apparent-group simulator.
- [x exploratory] Build four-object coordinated-group simulator.
- [x exploratory] Establish algorithm-visible / evaluator-only data separation.
- [x exploratory] Implement conventional organization baseline.
- [x exploratory] Implement relational model without spectral features.
- [x exploratory] Implement relational model with spectral features.
- [x] Run exploratory seeds 101–120.
- [review required] Review failed anti-trivial-separation validation and baseline-training interpretation.
- Freeze feature definitions only after review.
- Run confirmatory seeds.
- Run ablations.
- Produce research report.

## Future — only if scientifically justified

- TFL-UAS-001C group-state transitions.
- Group split.
- Group merge.
- Member departure.
- degraded observation organization tests.

## TFL-UAS-SPATIAL-001

- [x] Freeze protocol v1.0 and configuration with hashes.
- [x] Implement algorithm-visible/evaluator-only schema and leakage guards.
- [x] Implement S1–S5 synthetic exploratory scenarios.
- [x] Implement rigid relational state, shape state, local state, and global graph state.
- [x] Write raw state trajectories and diagnostics before interpretation.
- [x] Run exploratory validation only; stop at review.
- [ ] Review invariance, persistence, disturbance/recovery, and apparent-control results.
- [ ] Do not execute classifier, benchmark, 001B confirmatory, or held-out extensions without explicit authorization.

## TFL-UAS-DYNAMIC-001 v1.1

- [x] Freeze operator-revision protocol/config and hashes.
- [x] Implement genuine per-pair motion correlation/coherence.
- [x] Implement true per-pair contiguous relation lifetimes.
- [x] Implement revised lagged persistence, reference/window distances, and D6 recovery/reformation.
- [x] Run v1.1 exploratory operator revision only; stop at review.
- [ ] Review D4/D5/D6 and operator behavior before any extension.
- [ ] Do not execute classifier, benchmark, 001B confirmatory, or held-out extensions without explicit authorization.

## TFL-UAS-DYNAMIC-001 v1.2

- [x] Freeze spatiotemporal occupancy/Laplacian protocol/config and hashes.
- [x] Implement instantaneous and time-integrated relative occupancy graphs.
- [x] Implement normalized Laplacian, spectrum, and stable projector distances.
- [x] Implement parallel rigid, shape, motion, occupancy, and D6 recovery diagnostics.
- [x] Run v1.2 exploratory operator revision only; stop at review.
- [ ] Review D1/D2 invariance, D4 hard-control behavior, D5 expansion, and D6 recovery.
- [ ] Do not execute classifier, benchmark, 001B confirmatory, or held-out extensions without explicit authorization.

## 2026-08-17 — DYNAMIC-001 v1.2 exploratory run stopped at review

- Applied the frozen v1.2 operator to unchanged v1.0 D1–D6 data for seeds 101–120.
- Serialized 120 raw spatiotemporal states before evaluator-only metadata and produced 120 diagnostic records.
- Integrity, schema, determinism, raw-output ordering, and frozen-protocol checks passed.
- Created `experiments/TFL-UAS-DYNAMIC-001/v1.2/REVIEW_REQUIRED.md`; no scientific decision or extension is authorized.

## 2026-08-17 — DYNAMIC-001 v1.1 exploratory run stopped at review

- Applied the frozen operator-only revision to unchanged v1.0 D1–D6 exploratory track data: 120 samples, seeds 101–120.
- Wrote revised raw states before evaluator metadata; no simulator change, classifier, benchmark, confirmatory, or held-out execution occurred.
- Genuine per-pair motion correlation, contiguous lifetimes, lag persistence, reference/window distances, and D6 recovery/reformation were serialized.
- Created `experiments/TFL-UAS-DYNAMIC-001/v1.1/REVIEW_REQUIRED.md`; no scientific decision or extension is authorized.

## 2026-08-17 — v1.1 exploratory validation stopped

- v1.1 protocol/config and versioned artifacts were created without modifying v1.0.
- Training seeds 101–110 and exploratory test seeds 111–120 were used only in the v1.1 namespace; no confirmatory or held-out seeds ran.
- The supervised train/test boundary and raw-output ordering checks passed.
- The anti-triviality gate failed again: mean pairwise distance and group extent each had one-variable balanced accuracy 1.0.
- Automatic continuation stopped at `REVIEW_REQUIRED_v1.1.json`; A/B/C metrics are not interpreted.
- Next action is human review; no confirmatory authorization.

## 2026-08-17 — SPATIAL-001 exploratory run stopped at review

- Generated 100 raw algorithm-visible track samples across seeds 101–120 and S1–S5.
- Constructed rigid, shape, local-neighborhood, weighted-graph, and normalized-Laplacian state diagnostics.
- Leakage, schema, determinism, raw-output ordering, and frozen-protocol guards passed.
- Evaluator metadata was loaded only after raw relational states were serialized.
- Created `experiments/TFL-UAS-SPATIAL-001/REVIEW_REQUIRED.md`; no scientific decision or extension is authorized.

## TFL-UAS-DYNAMIC-001

- [x] Freeze protocol v1.0 and configuration with hashes.
- [x] Implement algorithm-visible/evaluator-only schema and leakage guards.
- [x] Implement D1–D6 synthetic dynamic scenarios.
- [x] Implement pair motion relations, registered lags/windows, lifetimes, reference distance, and recovery operators.
- [x] Write raw dynamic relational states before interpretation.
- [x] Run exploratory validation only; stop at review.
- [ ] Review spatial-vs-motion persistence and D4/D5/D6 behavior.
- [ ] Do not execute classifier, benchmark, 001B confirmatory, or held-out extensions without explicit authorization.

## 2026-08-17 — DYNAMIC-001 exploratory run stopped at review

- Generated 120 raw algorithm-visible samples across seeds 101–120 and D1–D6.
- Implemented registered motion relations, lags 1/5/15/30 s, windows 5/15/30 s, relation lifetimes, reference-state distance, spatial-vs-motion change, and D6 recovery diagnostics.
- Leakage, schema, determinism, raw-output ordering, and frozen-protocol checks passed.
- Created `experiments/TFL-UAS-DYNAMIC-001/REVIEW_REQUIRED.md`; no scientific decision or extension is authorized.
