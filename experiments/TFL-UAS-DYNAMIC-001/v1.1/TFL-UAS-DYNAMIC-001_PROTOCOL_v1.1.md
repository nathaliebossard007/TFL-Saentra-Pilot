# TFL-UAS-DYNAMIC-001 Protocol v1.1 — Motion Correlation Operator Revision

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-17

## Purpose and lineage

This is a measurement-only revision of DYNAMIC-001 v1.0. It repairs the
threshold-count lag persistence and global pseudo-lifetime operators identified
in review. D1–D6 scenario roles, seed namespace, track simulator, data
separation, and exploratory-only scope remain unchanged. v1.0 artifacts are
immutable and are not overwritten or reinterpreted.

## Pair state and normalization

For every same-object pair `(i,j)`, retain a time-resolved pair state with:

- distance `d_ij` and normalized distance `d_ij / max(mean_window_distance, 1 m)`;
- distance derivative `d_dot_ij` normalized by 12 m/s;
- relative velocity vector `Delta_v_ij`, each component normalized by 8 m/s;
- velocity-direction cosine;
- windowed speed correlation;
- relative-velocity stability `exp(-mean(std(Delta_v))/8)`;
- acceleration correlation and direction coherence when both variances are
  at least `1e-9`; otherwise the value is explicitly missing and excluded
  from that pair/window aggregate.

Registered windows remain 5, 15, and 30 seconds. Registered lags remain 1, 5,
15, and 30 seconds. No lag/window is selected after evaluator metadata is
loaded.

## Genuine pair operators

### Windowed motion correlation

For each pair, window, and time `t`, calculate the named scalar diagnostics
independently. The primary velocity-correlation quantity is the mean of the
available speed correlation and velocity-direction coherence, with missing
acceleration terms excluded rather than imputed as agreement.

### Pair relation similarity

Let `z_ij(t,W)` be the standardized vector containing normalized distance,
normalized distance derivative, normalized relative-velocity components,
direction cosine, speed correlation, relative-velocity stability, and available
acceleration diagnostics. Define:

`sim_ij(t,W) = exp(-mean((z_ij(t,W)-z_ij(t-1,W))^2)/2)`.

The relation is stable when `sim_ij >= 0.80` and the pair's motion-correlation
quantity is at least `0.70`. These thresholds are frozen protocol constants.

### Lagged pair persistence

For each pair and registered lag `tau`, compare `z_ij(t,W)` with
`z_ij(t-tau,W)` using the same standardized Euclidean similarity. `P_M(tau)`
is the mean of `sim_lag >= 0.80` across valid times and pairs. This is a
pair-level similarity operator, not a count of feature components under
independent absolute thresholds.

### Per-pair relation lifetime

For each pair and window, form the boolean stable series from the frozen
similarity and motion-correlation thresholds. Extract every contiguous true
interval, recording start, end, and duration. Report pair-level mean, maximum,
and interval count. No global persistence boolean is substituted for this
operation.

### Reference and window distances

The reference state for each pair/window is the mean `z_ij(t,W)` over the
registered baseline interval 30–60 seconds. `D_ref(t)` is the mean pairwise
Euclidean distance from that reference, normalized by `sqrt(feature_count)`.
Window-to-window motion-state distance compares the mean pair state vectors in
non-overlapping windows separated by the registered window length. Spatial-state
distance remains separately reported from the six rigid spatial pair values.

### D6 recovery/reformation

Using the pre-disturbance reference, recovery begins after second 100 when the
mean `D_ref` is at most 1.20 times the pre-disturbance baseline for at least
15 consecutive seconds. Reformation latency is the first post-disturbance
time when at least 5 of 6 pairs have a new contiguous stable interval of at
least 15 seconds. If either condition is not met by the run end, record 180 s
and mark the condition unmet.

## Scope and controls

D1–D6 remain exactly the v1.0 conceptual controls, especially D4 block-stable
geometry and D5 organized expansion/contraction. No simulator tuning, new
scenario, classifier, learned edge weight, benchmark, confirmatory seed, or
held-out seed is permitted.

Algorithm-visible input remains established tracks only. Raw revised dynamic
states and diagnostics must be serialized before evaluator-only metadata is
loaded. Exploratory execution must stop at `REVIEW_REQUIRED` before any
extension. No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision is authorized by this
freeze task.
