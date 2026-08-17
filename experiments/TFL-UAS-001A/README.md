# SÆNTRA / TFL-UAS-001A — Minimal Two-Track Association Test

Status: frozen exploratory pilot, code version 0.1.0.

Purpose: falsify or support the narrow claim that a deterministic TFL/RIC-derived relational representation adds measurable association information in a two-object crossing problem.

Scientific separation:
- `results/obs_seed_*.json`: algorithm-visible observations only; no object labels.
- `results/ground_truth_eval_seed_*.json`: evaluator-only object mapping.
- `src/run_experiment.py`: simulator, baseline, RIC graph, evaluator.
- `config/tfl_uas_001a_v1.json`: frozen parameters and seeds.

Algorithms:
1. Baseline: gated nearest-neighbor association with constant-velocity Kalman filter.
2. RIC candidate v0: time-directed relational compatibility graph. Edge weight uses temporal admissibility, displacement plausibility and explicit uncertainty penalty. Best weighted paths are extracted without labels. Normalized-Laplacian features are diagnostic only and are not used to tune or classify tracks.

Run:
`python src/run_experiment.py --config config/tfl_uas_001a_v1.json`

No post-hoc parameter tuning was performed after inspecting seed labels/results.
