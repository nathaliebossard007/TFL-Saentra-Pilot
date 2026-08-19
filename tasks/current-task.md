# Current Task

## REVIEW_REQUIRED — TFL-ORG-RELREP-001 v1.0 exploratory run

Review `experiments/TFL-ORG-RELREP-001/v1.0/REVIEW_REQUIRED.md` and the
parallel raw representations before any further work. Do not assign
`RELATIONAL_REPRESENTATION_CANDIDATE` or `REPRESENTATION_INSUFFICIENT`, and do
not extend the experiment without explicit review authorization.

The authorized implementation is complete: 120 unchanged historical samples
were processed and raw G/R_id/R_wt/R_t/P outputs were serialized before
evaluator interpretation.

The prior implementation task follows for provenance.

## AUTHORIZED — TFL-ORG-RELREP-001 exploratory implementation

Implement `TFL-ORG-RELREP-001 v1.0` exactly as frozen, serialize raw G,
R_id, R_wt, R_t, and P representations before evaluator interpretation, then
stop at `REVIEW_REQUIRED`. Preserve RECHECK v1.0 and all predecessor records
unchanged.

Frozen files:

- `experiments/TFL-ORG-RELREP-001/v1.0/TFL-ORG-RELREP-001_PROTOCOL_v1.0.md`
- `experiments/TFL-ORG-RELREP-001/v1.0/config/tfl_org_relrep_001_protocol_v1.json`
- `experiments/TFL-ORG-RELREP-001/v1.0/PROTOCOL_FREEZE.md`

The prior protocol-freeze task follows for provenance.

## AUTHORIZED — TFL-ORG-RELREP-001 protocol freeze only

Use `docs/TFL-ORG-CONSOLIDATED-ANCHOR-001.md` as the canonical research anchor.
Preserve `TFL-ORG-RECHECK-001 v1.0` unchanged as `NO_GO_TOY_MODEL_ONLY` for its preregistered cross-over criterion.
Do **not** tune or replace the failed v1.0 Laplacian merely to make Condition B pass.

Open a narrow follow-up:

**TFL-ORG-RELREP-001 — Minimal Relational Representation and Information-Retention Test**

## Scientific purpose

Determine the minimum non-learned representation that preserves organization-relevant coupling identity and temporal dependency information that can be lost by degree sequence or coarse Laplacian spectral summaries.

Primary question:

**Which representation preserves `who is coupled to whom`, how those couplings evolve, and which transformations leave the same relational organization unchanged?**

## Required parallel representations

Freeze at least four separate views; do not collapse them into one score:

- `G` — geometry / kinematics, retained only as the realization baseline;
- `R_id` — explicit node/edge coupling identity with canonical label-handling;
- `R_wt` — independently justified relation weights / dependency strengths where supported by source data;
- `R_t` — temporal evolution of relation identity/weights over preregistered windows;
- `P` — operator summaries derived from the explicit relation state, treated as lossy diagnostics rather than the organizational state itself.

If the selected data cannot independently justify `R_wt`, record it as unsupported rather than inventing weights.

## Dataset gate

Before implementation or result inspection:

1. Inventory pre-existing eligible historical data already frozen in the repository.
2. Prefer reuse of the same DYNAMIC-001 algorithm-visible track source if it supports the required representation without evaluator leakage; otherwise document why another frozen historical source is necessary.
3. No new simulator or synthetic replacement dataset is authorized in this task.
4. Record algorithm-visible versus evaluator-only fields before metric inspection.

## Representation requirements

The protocol must freeze, before execution:

1. canonical node identity and permutation handling;
2. explicit edge/dependency representation;
3. relation-weight definition, normalization, and missing-data rule;
4. temporal windowing and transition representation;
5. admissible organization-preserving transformations;
6. at least one organization-breaking relational perturbation that does not rely on evaluator labels;
7. comparison metrics for each representation separately;
8. operator construction(s), if any, only after the explicit relation representation is fixed;
9. degeneracy/cospectrality handling;
10. trivial-marginal and information-loss checks.

## Mandatory information-loss test

The protocol must explicitly test whether two states can satisfy

`P(X1) = P(X2)` (or be indistinguishable under the registered operator summary)

while

`R_id(X1) != R_id(X2)`.

Such a case is not an implementation failure. It is evidence that the registered `P` representation is many-to-one with respect to explicit coupling identity.

The protocol must distinguish:

- relational difference;
- graph isomorphism / mere relabeling;
- degree-sequence equivalence;
- spectral/cospectral equivalence;
- temporal-equivalence or temporal divergence.

## Transformation logic

At minimum preregister:

### A — realization change / relational organization preserved

Use transformations whose invariance properties are proved from the frozen representation definition. Geometry may change strongly, but `R_id/R_wt/R_t` should remain equivalent under the registered canonicalization.

### B — relational organization change / realization preserved

Change explicit coupling/dependency structure while leaving raw geometry unchanged or nearly unchanged. Do not require the operator summary to change; instead measure whether and where information is lost between `R_*` and `P`.

## Interpretation gate

The exploratory run may later support only a human-reviewed statement about representation adequacy, for example:

- `RELATIONAL_REPRESENTATION_CANDIDATE` — explicit relation identity/temporal representation survives invariance controls and distinguishes registered relational changes without trivial marginal leakage;
- `REPRESENTATION_INSUFFICIENT` — the proposed explicit representation itself fails to distinguish the registered organizational changes or depends on unsupported semantics.

Do not assign either outcome automatically.

## Protocol-freeze task only

For this task:

1. Create `experiments/TFL-ORG-RELREP-001/v1.0/`.
2. Freeze dataset choice and provenance before new result inspection.
3. Write protocol and machine-readable config.
4. Freeze exact `G`, `R_id`, `R_wt`, `R_t`, and `P` definitions.
5. Freeze canonicalization/permutation/isomorphism rules.
6. Freeze A/B transformations and invariance proofs.
7. Freeze information-loss/cospectrality diagnostics.
8. Freeze trivial-marginal and leakage checks.
9. Create `PROTOCOL_FREEZE.md` with hashes.
10. Add guards protecting predecessor data and the new protocol/config.
11. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
12. Do **not** implement or execute in the same task.

After a successful freeze, set the next task to implement exactly as frozen, serialize raw parallel representations before evaluator interpretation, then stop at `REVIEW_REQUIRED`.

## Scientific gates

- No classifier, neural model, learned representation, learned threshold, or post-hoc tuning.
- No new simulator or synthetic replacement dataset.
- No hostile/attack semantics are needed.
- Preserve all predecessor records unchanged.
- `TFL-RELSTATE-001` remains deferred until this representation question is reviewed.
- Operator success is not required; operator information loss is a valid result.
- Negative/null outcome is valid.
- Stop on ambiguous representation semantics, unsupported weights, leakage, protocol-change requirement, or missing eligible data.
