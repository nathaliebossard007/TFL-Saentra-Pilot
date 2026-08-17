# Current Task

Implement **TFL-UAS-DYNAMIC-001 v1.2.1 diagnostic correction exactly as frozen** on the unchanged 120 exploratory samples, then stop at `REVIEW_REQUIRED`.

The v1.2.1 protocol/config freeze is complete. Do not execute this task's
implementation until the frozen artifacts below are used exactly; do not
modify v1.0, v1.1, v1.2, or the v1.2.1 protocol/config.

Frozen v1.2.1 files:

- `experiments/TFL-UAS-DYNAMIC-001/v1.2.1/TFL-UAS-DYNAMIC-001_PROTOCOL_v1.2.1.md`
- `experiments/TFL-UAS-DYNAMIC-001/v1.2.1/config/tfl_uas_dynamic_001_protocol_v1.2.1.json`
- `experiments/TFL-UAS-DYNAMIC-001/v1.2.1/PROTOCOL_FREEZE.md`

The prior freeze task follows for provenance.

Preserve DYNAMIC-001 v1.0, v1.1, and v1.2 frozen protocols, configs, implementations, raw states, diagnostics, and review records unchanged.

## Scientific reason

Review of the completed v1.2 exploratory run identified two implementation-level diagnostic defects that block scientific interpretation but do not justify changing the simulator or the frozen spatiotemporal Laplacian itself:

1. `window_operator_distance` is evaluated for times earlier than the registered window length, so negative Python indices compare early states with states from the end of the sequence. Valid window-distance samples must begin only when `t >= W`; earlier entries must be explicitly unavailable and excluded from aggregates.
2. D6 `reformation_latency_s` currently treats `occupancy_edge > 0.0` as evidence that a pair relation has reformed. Because the occupancy edge is constructed from positive exponential weights, this condition is effectively trivial. Reformation must instead use a frozen non-trivial relation-restoration criterion tied to the pre-disturbance operator/edge state and sustained over a registered duration.

These are diagnostic/recovery corrections only. They are not grounds to tune D4, alter D1–D6, or change the v1.2 Laplacian/occupancy construction.

## Scope of v1.2.1

Freeze a narrowly scoped correction that:

- reuses the exact same 120 exploratory algorithm-visible samples (seeds 101–120, D1–D6) from v1.0;
- reuses the frozen v1.2 spatiotemporal relational occupancy/Laplacian operator unchanged;
- changes only diagnostic indexing and D6 recovery/reformation measurement;
- preserves rigid, shape, motion, occupancy, spectral, and projector outputs;
- does not introduce a classifier, learned threshold, learned edge weight, benchmark, new scenario, confirmatory seed, or held-out seed.

## Required correction definitions to freeze before implementation

### A. Window-distance validity

For every registered window `W in {5,15,30}`:

- define window-to-window operator distance only for `t >= W`;
- for `t < W`, record the value as explicitly unavailable (`null`/missing), never via negative indexing;
- compute means/quantiles only over valid times;
- apply the same validity rule to rigid, shape, motion, occupancy, spectrum, and projector window distances where those are reported.

### B. D6 operator recovery

Preserve the frozen pre-disturbance baseline interval and reference-operator construction from v1.2 unless a correction is strictly required for indexing consistency.

Recovery remains an operator-space concept: after disturbance end, the occupancy operator must remain within the frozen reference tolerance continuously for the registered recovery duration before recovery is declared.

### C. D6 pair reformation

Replace the trivial `occupancy_edge > 0` condition with a non-trivial, pre-registered pair-restoration rule derived without evaluator labels. The protocol must define before implementation:

- a per-pair pre-disturbance reference occupancy edge/state over the frozen baseline interval;
- a deterministic similarity or normalized distance from each post-disturbance pair edge/state to its own reference;
- a frozen restoration threshold that is not fitted to D6 outcomes or scenario labels;
- at least 5 of 6 pair relations restored simultaneously for at least 15 consecutive seconds before reformation is declared;
- unmet recovery/reformation remains recorded explicitly rather than silently coerced into success.

Prefer a dimensionless relative/reference-normalized criterion so the rule does not merely test whether a positive edge exists.

## Protocol-freeze task only

For this task:

1. Create versioned `experiments/TFL-UAS-DYNAMIC-001/v1.2.1/` artifacts.
2. Create `TFL-UAS-DYNAMIC-001_PROTOCOL_v1.2.1.md` and companion config describing only the diagnostic corrections.
3. Create `PROTOCOL_FREEZE.md` with SHA-256 hashes and provenance to frozen v1.2.
4. Add/extend repository guards so v1.0/v1.1/v1.2 remain immutable and v1.2.1 is hash-protected after freeze.
5. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
6. Do **not** implement or execute v1.2.1 in this same freeze task.

After freeze, set the next task to:

**Implement TFL-UAS-DYNAMIC-001 v1.2.1 diagnostic correction exactly as frozen on the unchanged 120 exploratory samples, then stop at REVIEW_REQUIRED.**

## Scientific gates

- No simulator change or D4 tuning.
- No change to the frozen v1.2 occupancy/Laplacian operator except the explicitly authorized diagnostic/recovery corrections.
- No post-hoc threshold fitting to D1–D6 outcomes.
- No classifier, benchmark, confirmatory, or held-out extension.
- Negative or null results are valid.
- No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision during freeze or automatic execution.
- After later v1.2.1 exploratory execution, stop at `REVIEW_REQUIRED` for scientific interpretation.
- TFL-UAS-001B confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited.
