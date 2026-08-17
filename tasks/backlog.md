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

## 2026-08-17 — v1.1 exploratory validation stopped

- v1.1 protocol/config and versioned artifacts were created without modifying v1.0.
- Training seeds 101–110 and exploratory test seeds 111–120 were used only in the v1.1 namespace; no confirmatory or held-out seeds ran.
- The supervised train/test boundary and raw-output ordering checks passed.
- The anti-triviality gate failed again: mean pairwise distance and group extent each had one-variable balanced accuracy 1.0.
- Automatic continuation stopped at `REVIEW_REQUIRED_v1.1.json`; A/B/C metrics are not interpreted.
- Next action is human review; no confirmatory authorization.
