# Current Task

Implement **TFL-UAS-DYNAMIC-001 exploratory v1.0 exactly as frozen**.

The protocol-freeze task is complete. Do not modify the frozen protocol or
configuration, do not execute 001B confirmatory/held-out seeds, and do not
add classification or benchmark extensions. Write raw dynamic relational
states before interpretation and stop at `REVIEW_REQUIRED` after the
exploratory run.

Frozen files:

- `experiments/TFL-UAS-DYNAMIC-001/TFL-UAS-DYNAMIC-001_PROTOCOL_v1.0.md`
- `experiments/TFL-UAS-DYNAMIC-001/config/tfl_uas_dynamic_001_protocol_v1.json`
- `experiments/TFL-UAS-DYNAMIC-001/PROTOCOL_FREEZE.md`

The prior protocol-freeze task description follows for provenance:

Create and freeze a new exploratory experiment:

**TFL-UAS-DYNAMIC-001 — Relational Motion-State Persistence**

Do not modify or reinterpret the frozen TFL-UAS-SPATIAL-001 v1.0 run. Preserve it as the geometric-relational baseline that exposed a limitation of frame-to-frame spatial persistence. Do not modify TFL-UAS-001B v1.0/v1.1.

## Scientific motivation

SPATIAL-001 showed promising translation/rotation invariance and clear degradation under independent motion, but its current persistence operator mainly measures small frame-to-frame changes in spatial relations. The apparent-organization control can therefore look persistent whenever local geometry remains quiet for short blocks.

The next hypothesis is that persistent organization is better characterized by the **evolution of relations** than by spatial configuration alone.

Research progression:

`space -> spatial relations -> motion relations -> persistent relational dynamics -> organization`

## Primary research question

**Can persistent organization be detected from the temporal evolution of pairwise motion relations independently of absolute position and predefined group labels?**

The experiment must remain deterministic, unlabeled in the algorithm-visible path, synthetic, and exploratory.

## Required dynamic pair state

Define a pairwise motion relation `M_ij(t; W)` over registered temporal windows `W` using interpretable quantities. At minimum include:

1. pair distance `d_ij(t)` and normalized distance;
2. distance derivative `d_dot_ij(t)`;
3. relative velocity vector `Delta_v_ij(t) = v_i(t) - v_j(t)`;
4. velocity-direction coherence, e.g. cosine similarity of `v_i` and `v_j`;
5. speed correlation over the window `corr_W(||v_i||, ||v_j||)`;
6. relative-velocity stability over the window, based on variation of `Delta_v_ij`;
7. acceleration coherence/correlation over the window where numerically stable.

Treat these as distinct diagnostics rather than collapsing them immediately into one learned score.

## Required temporal operators

The protocol must define before implementation:

- Lagged relational persistence `P_M(tau)` for registered lags, at least `tau = 1, 5, 15, 30 s` where data length permits.
- Relation lifetime for each stable same-object relation.
- Reference-state distance `D_ref(t)` relative to a registered baseline interval/state.
- Temporal relational-state distance between windows, not only adjacent frames.
- Separate spatial-state and motion-state change so a geometric change can occur while motion organization remains coherent.

No post-hoc lag selection after evaluator identities are visible.

## State hierarchy

Maintain an explicit hierarchy:

- Coordinate State
- Rigid Spatial Relational State
- Shape State
- Motion Relational State
- Dynamic Organizational State

The protocol must allow results such as:

`spatial state changed, motion organization persisted`

without treating that as contradiction.

## Exploratory scenarios

Use a newly versioned DYNAMIC namespace. Scenarios should test dynamic organization directly and be frozen before execution. At minimum include equivalents of:

D1 — Common Translation
- Similar velocity evolution and stable relative motion relations.

D2 — Coordinated Rotation / Maneuver
- Individual velocity vectors change direction, but pairwise motion evolution remains organized.

D3 — Independent Motion
- Similar initial spatial geometry but independently evolving velocities/accelerations.

D4 — Apparent Organization / Block-Stable Geometry
- Local density and short spatial persistence can remain high while same-object motion relations change across longer windows.
- This is the direct control for the SPATIAL-001 v1.0 limitation.

D5 — Organized Expansion / Contraction
- Pair distances change substantially while velocity relations indicate coherent common evolution.
- Expected: rigid spatial state changes, dynamic organization may persist.

D6 — Perturbation and Recovery
- Dynamic organization is disrupted and later restored; measure reference-state recovery and relation lifetime/reformation.

Scenario identity remains evaluator-only.

## Separation and leakage discipline

- Algorithm-visible input: established tracks only (time, stable within-sample track ID, position, velocity, acceleration, uncertainty).
- No scenario/class/group/coordination labels algorithm-visible.
- Evaluator metadata physically separate.
- Raw dynamic relational states must be serialized before evaluator metadata is loaded.
- No classifier, logistic regression, neural model, or learned edge weights in DYNAMIC-001 v1.0.

## Protocol-freeze task only

For this task:

1. Create `experiments/TFL-UAS-DYNAMIC-001/`.
2. Create `TFL-UAS-DYNAMIC-001_PROTOCOL_v1.0.md`.
3. Create companion config with all windows, lags, normalization constants, stability definitions, thresholds/tolerances, scenario parameters, seeds, and recovery rules frozen.
4. Create `PROTOCOL_FREEZE.md` with SHA-256 hashes.
5. Add repository guards for the new frozen protocol/config.
6. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
7. Do **not** implement or execute DYNAMIC-001 in this same task.

After the protocol/config freeze, set the next task to:

**Implement TFL-UAS-DYNAMIC-001 exploratory v1.0 exactly as frozen.**

## Scientific gates

- Negative results are valid.
- Do not tune the simulator or operator to make TFL win.
- No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision during protocol freeze.
- Exploratory execution must later stop at REVIEW_REQUIRED before any benchmark/classification/confirmatory extension.
- TFL-UAS-001B confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited.
