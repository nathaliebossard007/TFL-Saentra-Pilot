# Current Task

Prepare and freeze **TFL-UAS-DYNAMIC-001 v1.1 — Motion Correlation Operator Revision** before implementation.

Preserve DYNAMIC-001 v1.0 unchanged as an exploratory record. Do not modify its frozen protocol, config, implementation, raw states, diagnostics, or review record.

## Scientific reason for v1.1

The v1.0 exploratory run produced a promising spatial-vs-motion separation, especially for organized expansion/contraction, but review found two operator defects that prevent scientific interpretation:

1. `lagged_motion_persistence` currently measures the fraction of feature components whose absolute change is below a fixed threshold. This is not yet a genuine relational motion-correlation operator and can overrate the D4 apparent/block-stable control.
2. `relation_lifetime` is not implemented per pair over time; it is derived from a global lag-1 persistence boolean repeated across the sequence and therefore does not measure same-object relation lifetime.

These are measurement/operator defects, not grounds for simulator tuning or a positive/negative scientific conclusion.

## Scope of v1.1

Revise the **measurement operators only**. Do not redesign D1–D6 to improve separation and do not add new scenario classes.

The v1.1 protocol must freeze, before implementation:

- genuine per-pair windowed velocity correlation/coherence;
- per-pair speed correlation over registered windows;
- per-pair relative-velocity stability as a time-resolved series;
- per-pair acceleration correlation/coherence where numerically stable;
- per-pair relation similarity/distance with explicit normalization;
- lagged pair-relation persistence for the registered lags 1/5/15/30 s;
- true per-pair relation lifetime based on contiguous intervals satisfying the frozen relation-similarity rule;
- aggregate dynamic organizational persistence derived from pair-level results without learned weights;
- reference-state distance using a frozen baseline interval;
- window-to-window motion-state distance;
- D6 recovery/reformation based on the revised reference-state and pair-lifetime operators.

Do not collapse the diagnostics into a classifier or learned score.

## Controls that must remain conceptually unchanged

Retain the D1–D6 roles from v1.0, especially:

- D4 as the hard control: short/block-stable geometry must not automatically imply persistent motion organization.
- D5 as the spatial-vs-motion separation case: rigid spatial geometry may change while dynamic organization persists.
- D6 as disruption and recovery/reformation.

Any unavoidable simulator change must trigger REVIEW_REQUIRED rather than being made silently.

## Protocol-freeze task only

For this task:

1. Create a versioned v1.1 protocol/config and freeze record under `experiments/TFL-UAS-DYNAMIC-001/v1.1/` (or an equivalently clear versioned structure).
2. Record SHA-256 hashes and provenance.
3. Preserve all v1.0 hashes and artifacts unchanged.
4. Update repository guards to protect v1.0 and v1.1.
5. Update STATUS.md, docs/decisions.md, and tasks/backlog.md.
6. Do **not** implement or execute v1.1 in the same protocol-freeze task.

After the v1.1 protocol/config freeze, set the next task to:

**Implement TFL-UAS-DYNAMIC-001 v1.1 exploratory operator revision exactly as frozen, using exploratory data only, then stop at REVIEW_REQUIRED.**

## Scientific gates

- No classifier, benchmark, neural model, or learned edge weights.
- No tuning to make DYNAMIC-001 outperform a control.
- No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision during protocol freeze.
- Raw revised dynamic states/diagnostics must be serialized before evaluator metadata is loaded during later execution.
- After the later v1.1 exploratory execution, stop at REVIEW_REQUIRED before any benchmark or confirmatory extension.
- TFL-UAS-001B confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited.
