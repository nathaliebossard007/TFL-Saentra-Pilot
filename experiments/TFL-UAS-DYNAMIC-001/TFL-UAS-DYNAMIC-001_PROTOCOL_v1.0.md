# TFL-UAS-DYNAMIC-001 Protocol v1.0

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-17

## Question and scope

Can persistent organization be detected from the temporal evolution of
pairwise motion relations independently of absolute position and predefined
group labels? This is deterministic, synthetic, unlabeled exploratory work.
No classifier, learned edge weight, neural model, benchmark, or confirmatory
extension is authorized.

The progression is `space -> spatial relations -> motion relations ->
persistent relational dynamics -> organization`. Spatial-state change and
motion-organization persistence are reported separately; organized expansion
or contraction is not treated as a contradiction.

## Input and isolation

Algorithm-visible files contain only established track states: timestamp,
stable within-sample track ID, position, velocity, acceleration, and state
uncertainty. Scenario identity, expected property, perturbation interval, and
seed mapping are evaluator-only. They are physically separate and can be
loaded only after raw dynamic relational states are serialized.

Use opaque sample IDs and the separate DYNAMIC namespace. Exploratory seeds are
101–120. TFL-UAS-001B confirmatory 201–220 and held-out 301–320 remain
prohibited.

## State hierarchy

1. Coordinate State: absolute position, velocity, acceleration diagnostics.
2. Rigid Spatial Relational State: pair distance, distance derivative, and
   relative heading; translation/rotation invariant but not scale invariant.
3. Shape State: registered extent-normalized spatial relations.
4. Motion Relational State: pair relative velocity, direction coherence,
   speed correlation, relative-velocity stability, and acceleration coherence.
5. Dynamic Organizational State: deterministic temporal summaries of motion
   relations, relation lifetimes, reference-state distance, and window-to-
   window change. No learned aggregation is used.

## Pair motion relation

For every pair `(i,j)` and registered window `W`, define `M_ij(t;W)` from:

- `d_ij(t)` and extent-normalized distance;
- `d_dot_ij(t)`;
- `Delta_v_ij(t) = v_i(t) - v_j(t)`;
- velocity-direction cosine;
- `corr_W(||v_i||,||v_j||)`;
- variation of `Delta_v_ij` within W;
- acceleration-direction coherence and acceleration correlation when stable.

These are retained as distinct diagnostics. Registered windows are 5, 15,
and 30 seconds. Registered lags for lagged persistence are 1, 5, 15, and 30
seconds where available.

## Temporal operators

- `P_M(tau)`: fraction of pair/window motion relations within the frozen
  motion tolerance at lag `tau`.
- Relation lifetime: consecutive samples/windows satisfying the frozen
  stability condition for the same object pair.
- `D_ref(t)`: distance from the registered baseline interval [30, 60] s,
  using the unweighted deterministic dynamic-state vector.
- Window state distance: distance between non-overlapping registered windows,
  not only adjacent frames.
- Spatial-state change and motion-state change are emitted separately.

No lag, window, threshold, or scenario-specific operator may be selected after
evaluator identities are inspected.

## Scenarios

- **D1 Common Translation**: common velocity evolution with stable relative
  motion relations; absolute position changes.
- **D2 Coordinated Rotation / Maneuver**: individual velocity directions turn,
  while pairwise motion evolution remains organized.
- **D3 Independent Motion**: similar initial geometry but independently
  evolving velocities and accelerations.
- **D4 Apparent Organization / Block-Stable Geometry**: short blocks retain
  local density and spatial quietness while longer-window same-object motion
  relations change.
- **D5 Organized Expansion / Contraction**: pair distances change
  substantially while common velocity evolution remains coherent.
- **D6 Perturbation and Recovery**: dynamic organization is disrupted and later
  restored; measure reference-state recovery and relation reformation.

Scenario identity remains evaluator-only.

## Measurements and gates

Report lagged motion persistence, relation lifetime, reference-state distance,
window relational-state distance, separate spatial/motion changes, recovery
latency, and reformation latency. Before interpretation verify protocol/config
hashes, 001A frozen manifest, SPATIAL-001 preservation, schema/leakage
separation, deterministic regeneration, and raw-output ordering. Any leakage,
unexpected methodological issue, or failed exploratory validation creates
`REVIEW_REQUIRED` and stops. Exploratory execution must stop at review before
any benchmark, classification, or confirmatory extension. No GO/PARTIAL GO/
NO-GO/INCONCLUSIVE decision is authorized by this freeze task.
