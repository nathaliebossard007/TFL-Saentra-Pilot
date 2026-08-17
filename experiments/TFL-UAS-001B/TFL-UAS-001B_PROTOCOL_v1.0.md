# TFL-UAS-001B — Relational Organization Discrimination

Protocol version: 1.0  
Status: FROZEN BEFORE IMPLEMENTATION  
Predecessor: TFL-UAS-001A — Track Association: NO-GO

## 1. Scientific question and scope

Can persistent relational organization distinguish genuinely coordinated four-object behavior from mere spatial proximity, aligned movement, or temporarily similar kinematics better than a reasonable conventional track-level baseline?

This is an organization experiment, not a tracking experiment. All algorithms receive the same already-established synthetic track states. No point-to-track association, sensor fusion, identity recovery, or tracker comparison is performed in 001B.

Primary comparisons:

- B vs A: whether temporal relational representation adds value over a conventional kinematic baseline.
- C vs B: whether spectral features add reproducible value beyond the non-spectral relational representation.

The result of each scientific question is reported separately. A spectral NO-GO does not invalidate a relational GO.

## 2. Fixed geometry and input state

The experiment uses four airborne objects in a synthetic 10,000 m × 10,000 m area for 180 s at 1 s intervals, including t=0 and t=180. Established tracks are supplied directly; 001B does not simulate or infer sensor detections.

Every algorithm receives the same six-field schema: `track_id`, `timestamp`, `position_xyz`, `velocity_xyz`, `acceleration_xyz`, and `state_uncertainty`. Track IDs are opaque and generated independently of class and seed.

## 3. Strict separation of layers

### A. Simulator and evaluator-only truth

Simulator controls and truth live only under `data/evaluator_only/` and may contain `ground_truth_object_id`, `ground_truth_group_id`, `ground_truth_coordination_state`, `scenario_class`, `scenario_variant`, `coordination_start_time`, `coordination_end_time`, simulator controls, and seed.

### B. Algorithm-visible track states

Only the six state fields above may appear under `data/algorithm_visible/`. Files use opaque names such as `sample_0001.json`; filenames contain no class, seed, family, or coordination status.

### C. Organization algorithms

All three primary models receive identical algorithm-visible samples and no evaluator metadata.

### D. Evaluation

Predictions are serialized under `results/predictions/` before the evaluator loads hidden truth. A failed leakage check invalidates the run and metrics are not treated as scientific evidence.

## 4. Scenario classes

### Negative: Apparent Group

Objects are independently controlled but intentionally difficult to distinguish from a coordinated group. Each negative family includes periods of spatial proximity, similar headings, similar speeds, a common operating region, and temporary formation-like geometry. Independent maneuver timing, acceleration changes, heading corrections, and relative-spacing drift must remain present. The negative class is a hard negative, not random dispersal.

### Positive: Coordinated Group

Objects exhibit persistent relational dynamics combining bounded relative geometry, correlated heading, synchronized but perturbed turns, coordinated acceleration/deceleration, bounded relative-spacing error, and coherent centroid translation. Realistic perturbations, timing variation, and nonzero state noise are required; mathematically perfect rigid motion is prohibited.

Development positive family: synchronized heading-change formation. Held-out positive family: coordinated acceleration/deceleration with different formation geometry and maneuver profile. The held-out family is not used for feature or threshold tuning.

Exploratory, confirmatory, and held-out samples are balanced by class. Seed-to-class mapping exists only in evaluator metadata.

## 5. Anti-trivial-separation gate

Before model fitting, compare the two classes for mean speed, altitude, centroid speed, mean pairwise distance, group extent, mean heading, trajectory duration, and spatial operating region. Report class summaries, standardized differences, and a one-variable classifier audit. The numerical audit thresholds are explicitly `TO_BE_FROZEN_AFTER_EXPLORATORY_SANITY_CHECK`; confirmatory labels may not alter them.

If a single marginal variable trivially separates the classes, the experiment fails validation. If overlap cannot be achieved without corrupting scenario semantics, the organization result is INCONCLUSIVE and implementation stops for protocol review.

## 6. Primary model A: conventional kinematic baseline

Model A is transparent fixed-window logistic regression. Allowed feature families are mean and variance of pairwise distance, relative-position variance, heading correlation, velocity correlation, acceleration correlation, centroid coherence, and formation persistence. Features use trailing windows of 5 s, 15 s, and 30 s and are standardized from training data only. L2 regularization and its value are declared in configuration. No neural model is allowed. The baseline must not be deliberately weakened.

## 7. Primary model B: temporal relational, no spectral features

Model B constructs `G_t=(V_t,E_t)`, where vertices are the four established tracks and edges represent relational coherence, never identity.

For pair i,j, use relative position, velocity, acceleration, distance, heading, and reported uncertainty. Over a window W, define interpretable components in [0,1]: distance stability `exp(-variance(distance_ij over W)/sigma_distance^2)`; velocity compatibility `exp(-mean(||relative_velocity_ij - median||^2)/sigma_velocity^2)`; heading compatibility as the mean of `(1+cos(heading_i-heading_j))/2`; acceleration synchrony `exp(-mean(||relative_acceleration_ij||^2)/sigma_acceleration^2)`; geometry persistence as the fraction of valid samples with bounded distance drift; and uncertainty penalty `exp(-mean(uncertainty_i+uncertainty_j)/sigma_uncertainty)`.

The edge score is the equal-weight arithmetic mean of available components. An edge exists only after deterministic distance, velocity, uncertainty, and minimum-score gates. No learned edge weights are allowed.

Model B evaluates `G_t → G_(t+1)` and `ΔG_t`. Its features are edge persistence, edge-weight variance, relation lifetime, connected-structure persistence, topology change rate, relative-geometry stability, temporal coherence, edge count, degree summaries, and edge/node ratio. It contains no Laplacian eigensummary.

## 8. Primary model C: temporal relational with spectral features

Model C is exactly B plus the pre-registered spectral block. For weighted adjacency A and degree matrix D, use `L_norm = I - D^(-1/2) A D^(-1/2)`.

The spectral block may contain eigenvalue quantiles, spectral gap, normalized-Laplacian standard deviation, connectivity, clustering, edge/node ratio, and temporal spectral change. C uses the same preprocessing, classifier family, split, and training protocol as B. 001A established no predictive spectral advantage; C must earn any added value.

## 9. Required ablations

Freeze these ablations before confirmatory labels are inspected:

1. geometry only;
2. instantaneous kinematics only;
3. temporal relation only;
4. spectral only;
5. relation + temporal;
6. relation + temporal + spectral.

No new confirmatory feature family, threshold, or ablation may be invented after labels are inspected.

## 10. Seeds and discipline

Exploratory seeds: 101–120. Confirmatory seeds: 201–220. Held-out family seeds: 301–320.

Exploratory data may be used for debugging, numerical sanity checks, reasonable fixed parameter-range selection, and freezing feature definitions. Confirmatory data may not be used for tuning. Held-out data are run only after definitions, thresholds, classifier structure, and configuration hash are frozen. A changed definition requires a new protocol version.

## 11. Outputs and metrics

Use `data/algorithm_visible/sample_0001.json`, evaluator-only metadata, `results/exploratory/`, `results/confirmatory/`, and `diagnostics/`. Raw predictions, hashes, model definitions, and leakage results are written before interpretation.

For every model and split, report precision, recall, F1, balanced accuracy, confusion matrix, and ROC-AUC where applicable. Report sample-level effect sizes for A vs B and B vs C with a pre-registered confidence procedure. Temporal metrics are detection latency, false organization duration, and organization-state stability. Report class-wise and family-wise results.

## 12. Leakage tests

Automated checks must prove that algorithm-visible data contain no hidden labels; filenames and track IDs contain no class information; seeds are not features; evaluator-only directories are inaccessible during prediction; and predictions are written before evaluator truth is loaded. The prediction process may not open, import, glob, or traverse `data/evaluator_only/`. Any failure invalidates the run.

## 13. Falsification and GO logic

NO-GO applies when B is worse than A; B is approximately equal to A with substantially higher complexity; gains disappear on confirmatory or held-out data; gains require post-hoc tuning; C has no reproducible gain over B; organization collapses to proximity detection; marginal validation fails; or leakage occurs.

A GO for Relational Organization Detection requires reproducible confirmatory advantage over A, meaningful effect size, no leakage, no trivial marginal explanation, and survival of held-out variation. A valid outcome may be Relational Organization Detection: GO and Spectral Added Value: NO-GO.

Separate final statuses are mandatory for Relational Organization Detection, Temporal-State Added Value, Spectral Added Value, and Out-of-Family Generalization. Allowed values only: `GO`, `PARTIAL GO`, `NO-GO`, `INCONCLUSIVE`.

## 14. Explicitly unresolved parameters

The following must be frozen after exploratory sanity checks and before confirmatory execution: anti-trivial-separation thresholds; distance and velocity gates; `edge_weight_min`; sigma values for distance, velocity, acceleration, and uncertainty; minimum valid history per window; and logistic-regression regularization if the configured default is numerically inadequate. Values may only be selected from documented exploratory ranges and may not be adjusted to improve confirmatory or held-out performance.

## 15. Reproducibility gate

An implementation team must conform to this document, the companion JSON, and the recorded protocol hashes. Changes to scenario generation, input schema, features, graph scoring, model structure, split discipline, leakage rules, or decision thresholds require a new protocol version.

No TFL-UAS-001B implementation is included in this protocol-freeze task.
