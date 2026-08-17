# TFL-UAS-001B Protocol v1.1 — Exploratory Redesign

Status: frozen for exploratory execution only (2026-08-17).

This version is a versioned redesign after the failed v1.0 anti-triviality
validation. v1.0 remains immutable and is not overwritten or reinterpreted.

## Question and scope

Test whether temporal relational structure distinguishes coordinated four-track
behavior from a hard apparent-group negative when broad one-variable marginals
are matched. This is synthetic exploratory work only. No confirmatory seeds
(201–220) or held-out seeds (301–320) are authorized.

## Data and split

- Training seeds: 101–110, two classes per seed.
- Exploratory test seeds: 111–120, two classes per seed.
- Four established tracks; duration 180 s; dt 1 s; area 10,000 m × 10,000 m.
- `data/training_visible/` contains training features and labels and is read
  only by the fitting procedure.
- `data/algorithm_visible/` contains test track states without labels.
- `data/evaluator_only/` contains test truth and is opened only after raw
  predictions are serialized.
- Sample IDs are opaque and filenames do not encode class or seed.

Both classes share the same centroid macro-envelope and object-level noise.
The intended difference is temporal dependence of relative geometry: the
coordinated class uses one shared bounded formation scale/turn process; the
apparent-group class uses the same phase family independently permuted across
objects. The coordinated class is not perfectly rigid.

## Models

Model A is a real supervised logistic-regression baseline fitted only on the
training partition. Model B uses temporal relational features without spectral
features. Model C adds normalized-Laplacian features. All test predictions
are produced from algorithm-visible states only. Threshold 0.5 is fixed before
execution; no test-label tuning is permitted. The feature blocks and candidate
parameters are frozen in the accompanying config before generation.

## Gates

Before interpretation, verify predecessor hashes, v1.0 preservation, schema,
determinism, leakage separation, supervised train/test separation, and the
anti-triviality audit. If the audit fails, write `REVIEW_REQUIRED_v1.1.md`,
do not interpret A/B/C performance, and stop. This exploratory run cannot
produce a GO, PARTIAL GO, NO-GO, or INCONCLUSIVE decision.
