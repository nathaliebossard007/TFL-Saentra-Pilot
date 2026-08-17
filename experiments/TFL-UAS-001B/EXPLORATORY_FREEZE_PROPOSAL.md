# TFL-UAS-001B Exploratory Parameter-Freeze Proposal

Status: **EXPLORATORY — NOT CONFIRMATORY EVIDENCE**  
Seeds used: 101–120 only  
Date: 2026-08-17

## Candidate ranges were recorded before classification

Candidate ranges are stored in `diagnostics/exploratory_parameter_candidates.json`. The selection priority was numerical stability, physical interpretability, balanced graph density, anti-trivial-separation validity, and only then classification diagnostics. No candidate was selected by maximizing A/B/C performance.

## Proposed values

| Parameter | Candidate range | Proposed value | Reason | Label-dependent? | Ranking sensitivity |
|---|---|---:|---|---|---|
| distance gate | 1500, 2500, 3500 m | 2500 m | middle physical operating scale | No | not used for ranking selection |
| velocity gate | 60, 80, 100 m/s | 80 m/s | middle permissive compatibility gate | No | not used for ranking selection |
| edge_weight_min | 0.25, 0.35, 0.45 | 0.35 | middle interpretable coherence cutoff | No | class-blind density spot-check showed no material change |
| sigma_distance | 25, 50, 100 m | 50 m | middle measurement-scale normalization | No | not used for ranking selection |
| sigma_velocity | 5, 10, 20 m/s | 10 m/s | middle kinematic normalization | No | not used for ranking selection |
| sigma_acceleration | 0.5, 1.0, 2.0 m/s² | 1.0 m/s² | middle perturbation scale | No | not used for ranking selection |
| sigma_uncertainty | 25, 50, 100 | 50 | middle uncertainty scale | No | not used for ranking selection |
| minimum valid history | 5, 10, 15 s | 10 s | enough history for temporal statistics | No | not used for ranking selection |
| logistic regularization | 0.1, 1.0, 10.0 | 1.0 | middle conventional value | No | fixed label-free score in this implementation |
| marginal audit thresholds | not preselected | NOT FROZEN | validation failed; requires protocol review | No | not applicable |

## Required review before confirmatory execution

The exploratory simulator failed the anti-trivial-separation gate: every marginal except trajectory duration reached one-variable balanced accuracy of 1.0 in the exploratory audit. Therefore A/B/C metrics must not be interpreted as evidence of organization detection. The simulator requires redesign so class-marginal summaries overlap substantially while relational temporal structure remains different.

The current implementation uses a deterministic, label-free logistic score rather than fitting coefficients from evaluator-only labels. This preserves the strict prediction/evaluation separation but requires explicit review against the frozen protocol's intended logistic-regression baseline before any confirmatory run.

No parameter should be frozen for confirmatory use until the marginal-overlap failure and the model-fitting interpretation are resolved in a new reviewed protocol decision.
