# TFL-UAS-001B Exploratory Report

**EXPLORATORY — NOT CONFIRMATORY EVIDENCE**

## Scope

Only seeds 101–120 were executed. Confirmatory seeds 201–220 and held-out seeds 301–320 were not executed. The run generated 40 opaque samples: 20 `apparent_group` and 20 `coordinated_group`, with four established tracks per sample.

Protocol SHA-256 and configuration SHA-256 matched the frozen v1.0 values. The 001A frozen manifest and protocol guard passed.

## Exploratory model results

| Model | Precision | Recall | F1 | Balanced accuracy | ROC-AUC | Confusion matrix |
|---|---:|---:|---:|---:|---:|---|
| A conventional kinematic | 0.500 | 1.000 | 0.667 | 0.500 | 1.000 | [[0,20],[0,20]] |
| B temporal relational | 0.000 | 0.000 | 0.000 | 0.500 | 1.000 | [[20,0],[20,0]] |
| C relational + spectral | 0.500 | 1.000 | 0.667 | 0.500 | 1.000 | [[0,20],[0,20]] |

Temporal exploratory outputs were also written for detection latency, false organization duration, and organization-state stability. These thresholded diagnostics are not interpreted because the anti-trivial-separation gate failed.

Descriptive F1 differences were B−A = −0.667 and C−B = +0.667. They are not evidence of relational or spectral advantage.

## Ablations

| Ablation | F1 | Balanced accuracy | ROC-AUC |
|---|---:|---:|---:|
| geometry only | 0.000 | 0.500 | 0.530 |
| instantaneous kinematics only | 0.667 | 0.500 | 1.000 |
| temporal relation only | 0.000 | 0.500 | 0.500 |
| spectral only | 0.667 | 0.500 | 1.000 |
| relation + temporal | 0.000 | 0.500 | 1.000 |
| relation + temporal + spectral | 0.667 | 0.500 | 1.000 |

## Anti-trivial-separation result

The one-variable audit produced balanced accuracy 1.0 for mean speed, altitude, centroid speed, mean pairwise distance, group extent, mean heading, and operating region. Trajectory duration scored 0.5. This is a validation failure. Model performance is therefore not scientifically interpretable as organization discrimination.

## Spectral diagnostics

Model C recorded eigenvalue-derived features, spectral gap, spectral quantiles, normalized-Laplacian standard deviation, connectivity, clustering, edge/node ratio, and temporal spectral change for the configured windows. These are diagnostic records only. No causal or predictive spectral claim is made.

## Integrity and next step

Algorithm-visible schema and filename/track-ID leakage tests passed. Predictions were written before evaluator truth was loaded. The deterministic repeated-seed check is required before the next commit review. The exploratory freeze proposal recommends middle physical parameter values but does not authorize confirmatory execution. The simulator's marginal-overlap failure and the label-free logistic-score interpretation must be reviewed before any confirmatory run.
