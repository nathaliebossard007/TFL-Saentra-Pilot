# REVIEW_REQUIRED — TFL-UAS-001B Exploratory Gate

Date: 2026-08-17  
Experiment: TFL-UAS-001B — Relational Organization Discrimination  
Scope reached: exploratory seeds 101–120 only

## 1. What happened

The exploratory implementation generated 40 opaque established-track samples: 20 apparent-group and 20 coordinated-group samples. Models A, B, and C plus the six required ablations executed. Algorithm-visible and evaluator-only roots remained physically separate. Predictions were written before evaluator truth was loaded.

The anti-trivial-separation validation failed. The one-variable audit reached balanced accuracy 1.0 for mean speed, altitude, centroid speed, mean pairwise distance, group extent, mean heading, and operating region. Only trajectory duration scored 0.5.

## 2. Relevant metrics

All values below are exploratory diagnostics, not scientific evidence:

| Model | Precision | Recall | F1 | Balanced accuracy | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| A conventional kinematic | 0.500 | 1.000 | 0.667 | 0.500 | 1.000 |
| B temporal relational | 0.000 | 0.000 | 0.000 | 0.500 | 1.000 |
| C relational + spectral | 0.500 | 1.000 | 0.667 | 0.500 | 1.000 |

Descriptive F1 differences were B−A = −0.667 and C−B = +0.667. They must not be interpreted as relational or spectral effects because the marginal gate failed.

Technical gates passed: protocol/config hashes, 001A frozen manifest, deterministic sample generation, schema validation, filename/track-ID checks, and prediction-before-evaluation ordering.

## 3. Why automatic continuation stopped

The repository workflow requires a review gate when exploratory validation fails. Continuing would risk measuring trivial marginal class differences rather than persistent relational organization. Confirmatory seeds 201–220 and held-out seeds 301–320 are therefore not authorized. The frozen v1.0 protocol and hashes must not be changed automatically.

A second methodological issue also requires review: the exploratory implementation used a deterministic label-free logistic score to preserve evaluator-only truth separation rather than fitting coefficients from hidden labels. Its equivalence to the protocol's intended conventional logistic-regression baseline must be resolved before confirmatory work.

## 4. Options available

1. Redesign the simulator so class-marginal distributions overlap substantially while relational temporal structure differs, then rerun exploratory sanity checks under a new reviewed protocol version if frozen definitions change.
2. Define an approved training-data boundary and supervised baseline procedure that preserves evaluator-only test truth, then document it before any confirmatory execution.
3. Review the current exploratory implementation and accept only the non-scientific infrastructure while discarding these model metrics.
4. Stop the 001B line if a valid anti-trivial separation cannot be achieved without artificial scenario construction.

## 5. Recommended scientifically conservative next action

Do not run confirmatory or held-out seeds. Review the simulator marginal diagnostics and the label-free baseline interpretation, then decide whether a new protocol version is scientifically justified. Preserve the current exploratory outputs as a failed validation record and do not convert them into GO, PARTIAL GO, NO-GO, or INCONCLUSIVE conclusions.
