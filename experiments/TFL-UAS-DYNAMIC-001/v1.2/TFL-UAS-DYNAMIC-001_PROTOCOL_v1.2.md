# TFL-UAS-DYNAMIC-001 Protocol v1.2 — Spatiotemporal Relational Laplacian

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-17

## Lineage and scope

This operator-only revision addresses the v1.1 finding that D4 can retain
locally stable pairwise motion dynamics. It reuses unchanged DYNAMIC-001 v1.0
D1–D6 exploratory track data, seeds 101–120, and evaluator separation. It does
not tune or regenerate the simulator, add scenarios, use labels algorithmically,
or introduce a classifier, benchmark, learned weight, confirmatory seed, or
held-out seed. v1.0 and v1.1 artifacts are preserved unchanged.

## Registered windows and states

Use windows of 5, 15, and 30 seconds. Preserve parallel coordinate, rigid
spatial, shape-normalized, motion, and occupancy states. Absolute translation
is removed through pair-relative coordinates; rotation treatment is explicit:
the rigid occupancy uses pair-distance/relative-velocity invariants, while the
shape occupancy additionally divides pair distances by the window median pair
distance. Physical scale is retained in the rigid branch and normalized only in
the shape branch.

## Instantaneous relational graph

For each time `t`, pair `(i,j)` receives the registered feature vector:

`q_ij(t) = [d_norm, |d_dot|/12, ||Delta_v||/8, (1+cos(v_i,v_j))/2]`.

The instantaneous edge weight is:

`w_ij(t) = exp(-mean(q_ij(t)^2)/2)`.

The diagonal is zero and weights are symmetric. No evaluator field enters the
graph. All constants are frozen in the companion configuration.

## Time-integrated relative spatial occupancy

For each pair and window `[t-W+1,t]`, define occupancy persistence as the mean
of `exp(-((d_norm(k)-d_norm(t))^2 + (d_dot(k)-d_dot(t))^2)/2)` over valid k,
multiplied by the mean velocity-direction coherence `(1+cos)/2` in the same
window. The occupancy edge is the time mean of `w_ij(k)` multiplied by this
persistence factor. This integrates same-object relative spatial occupancy
over the full window rather than counting adjacent-frame quietness.

The rigid and shape branches are both emitted. No single score collapses them.

## Normalized occupancy Laplacian

For each occupancy matrix `W_occ`, let `D` be its degree matrix and define:

`L_occ = I - D^(-1/2) W_occ D^(-1/2)`.

If a degree is below `1e-12`, its inverse factor is zero and the corresponding
diagonal contribution remains identity. Record zero-degree count explicitly.
Record ordered eigenvalues, spectral gap, spectrum distance to the previous
registered window, and reference spectrum distance to the baseline interval
30–60 seconds.

## Stable spectral/projector distances

For the low-eigenspace projector use the first `r=2` eigenvectors only when
the eigenvalue gap around the r-th eigenvalue is at least `1e-6`. Otherwise
record projector distance as missing/conservative failure. Define the projector
as `P_r = U_r U_r^T`; compare subspaces with Frobenius distance
`||P_r - P'_r||_F / sqrt(2r)`. This is invariant to eigenvector sign and basis
rotations within repeated eigenspaces. Never compare raw eigenvector signs.

## Temporal and recovery measurements

Report occupancy operator distance between registered windows, reference
operator distance to the 30–60 s baseline, spectral/projector distances,
zero-degree counts, and separate rigid/shape/motion changes. For D6, recovery
begins after t=100 when occupancy reference distance is at most 1.20 times the
pre-event baseline for 15 consecutive seconds. Reformation requires at least
5 of 6 pair occupancy edges to exceed the frozen occupancy persistence rule for
15 consecutive seconds. Unmet conditions are recorded as 180 s.

## Expected invariances and control

- D1 common translation: relative occupancy and Laplacian approximately
  invariant despite absolute coordinate movement.
- D2 coordinated rotation: invariant branches preserve organization under the
  registered rigid/relative rule.
- D4 remains unchanged as the hard block-stable control; any longer-window
  effect must arise from the frozen occupancy operator, not data tuning.
- D5 may change rigid spatial geometry while shape, motion, and occupancy
  organization remain coherent.

Raw v1.2 outputs must be serialized before evaluator metadata is loaded. Stop at
`REVIEW_REQUIRED` after later exploratory execution. No scientific GO,
PARTIAL GO, NO-GO, or INCONCLUSIVE decision is authorized by this freeze task.
