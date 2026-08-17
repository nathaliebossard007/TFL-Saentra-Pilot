# TFL-UAS-DYNAMIC-001 Protocol v1.2.1 — Diagnostic Correction

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-17

## Lineage and scope

This is a diagnostic-only correction to frozen v1.2. It reuses the exact
120 v1.0 algorithm-visible exploratory samples (seeds 101–120, D1–D6) and
the v1.2 spatiotemporal occupancy/Laplacian unchanged. No simulator,
operator, classifier, learned parameter, scenario, or seed range changes.

## A. Valid window distances

For each registered window `W in {5,15,30}`, window-to-window distances are
defined only at timestamps `t >= W`, comparing the state at `t` with the
state at `t-W`. Values for `t < W` are explicitly missing (`null`) and are
excluded from means and quantiles. This validity rule applies to rigid,
shape, motion, occupancy, spectrum, and projector distances.

## B. D6 operator recovery

The frozen v1.2 baseline interval, reference operator, and tolerance remain
unchanged. After disturbance end `t=100`, recovery is declared only when the
15-second occupancy reference-distance series is within `1.20` times its
pre-disturbance baseline for 15 consecutive valid seconds. Unmet recovery is
recorded as `180` seconds.

## C. D6 pair reformation

For each pair, compute its pre-disturbance reference edge as the arithmetic
mean occupancy edge over timestamps 30–60 in the 15-second window. For each
post-disturbance timestamp, define restoration similarity as
`1 - abs(edge - reference) / max(reference, 1e-12)`, clipped to `[0,1]`.
A pair is restored only when similarity is at least `0.80`. Reformation is
declared only when at least 5 of 6 pairs are restored simultaneously for 15
consecutive seconds after `t=100`. Unmet reformation is recorded as `180`
seconds. This threshold is fixed before execution and is not fitted to labels
or D6 outcomes.

No scientific GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision is authorized by this
freeze. After later exploratory execution, stop at `REVIEW_REQUIRED`.
