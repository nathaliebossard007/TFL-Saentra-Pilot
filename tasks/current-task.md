# Current Task

## REVIEW_REQUIRED — TFL-ORG-RECHECK-001 v1.0 exploratory run

Review `experiments/TFL-ORG-RECHECK-001/v1.0/REVIEW_REQUIRED.md` and the
frozen G/R/P raw outputs before any further work. Do not assign either
authorized outcome, extend the pilot, or start TFL-RELSTATE-001 without
explicit review authorization.

The authorized implementation is complete: 120 selected historical samples
were processed and raw outputs were serialized before evaluator interpretation.

The prior implementation task follows for provenance:

## AUTHORIZED — TFL-ORG-RECHECK-001 exploratory implementation

Implement `TFL-ORG-RECHECK-001 v1.0` exactly as frozen on the selected
historical DYNAMIC-001 algorithm-visible dataset. Serialize transformed/raw
G/R/P outputs before evaluator interpretation, then stop at `REVIEW_REQUIRED`.

Frozen files:

- `experiments/TFL-ORG-RECHECK-001/v1.0/TFL-ORG-RECHECK-001_PROTOCOL_v1.0.md`
- `experiments/TFL-ORG-RECHECK-001/v1.0/config/tfl_org_recheck_001_protocol_v1.json`
- `experiments/TFL-ORG-RECHECK-001/v1.0/PROTOCOL_FREEZE.md`

The prior protocol-freeze task follows for provenance.

## AUTHORIZED — TFL-ORG-RECHECK-001 protocol freeze only

Use `docs/TFL-ORG-SNAPSHOT-001.md` as the working research anchor.

Do **not** yet implement the broader synthetic `TFL-RELSTATE-001` experiment. Preserve that concept as deferred follow-up only.

Open a narrow re-evaluation pilot:

**TFL-ORG-RECHECK-001 — Geometry / Relation / Projector Cross-over on Existing Data**

## Scientific purpose

Test whether the toy-model cross-over in `TFL-ORG-SNAPSHOT-001` is reproducible on one pre-existing historical TFL/RDL dataset before authorizing any systematic re-analysis.

Primary question:

**Which observation basis remains stable under organization-preserving geometric change, and which basis detects organization-breaking relational change when geometry remains similar?**

Parallel bases:

- `G` — geometry/kinematic observables
- `R` — explicit relational observables
- `P` — spectral/eigenspace/projector observables derived from the registered relational graph/operator

No basis may be collapsed into a learned score.

## Dataset selection gate

Before any implementation or metric inspection:

1. Inventory historical datasets already present in the repository or frozen imported artifacts.
2. Select exactly one eligible pre-existing dataset using preregistered criteria only:
   - generated/collected before `TFL-ORG-SNAPSHOT-001`;
   - contains sufficient algorithm-visible per-object/per-node temporal or relational data to construct G/R/P without scenario-label leakage;
   - was not generated specifically for this new hypothesis;
   - frozen/raw source remains unchanged.
3. Record candidate datasets, exclusion reasons, and the selected dataset in the protocol **before looking at new G/R/P cross-over results**.
4. If no eligible dataset exists, stop at `REVIEW_REQUIRED` with `NO ELIGIBLE HISTORICAL DATASET`; do not synthesize a replacement in this task.

## Required paired perturbation logic

The protocol must preregister a deterministic, label-free way to form or identify two counterfactual conditions from the selected historical data without altering its source record:

### A — geometry-breaking / organization-preserving

Apply only transformations that strongly change geometric realization while preserving the registered relational-role/dependency structure by construction or by a preregistered invariance rule.

Examples may include translation, rotation, admissible scale/shape transform, coordinate-frame transform, or node-position remapping **only if** the protocol proves which relational invariants are preserved.

### B — geometry-preserving / organization-breaking

Apply a preregistered relational perturbation that minimally changes raw geometry but changes `who is coupled to whom / in what relational role`.

A degree-preserving graph 2-switch is admissible only if it can be derived from the selected dataset's registered relational graph without using evaluator labels and if graph validity constraints are frozen before execution.

The perturbations are counterfactual analysis transforms; they must not overwrite historical raw data.

## Required measurements

Freeze deterministic metrics before implementation.

### G — Geometry

At minimum:
- mean/median pair-distance change;
- pair-distance correlation;
- optional registered trajectory/vector distances if available in the selected dataset.

### R — Relation

At minimum:
- edge/neighbor Jaccard or equivalent registered relational overlap;
- role/dependency preservation where the historical data supports such a definition;
- no invented semantic roles unsupported by the source dataset.

### P — Operator / projector

At minimum where mathematically defined:
- normalized Laplacian construction and zero-degree rule;
- spectrum distance;
- algebraic-connectivity change (`lambda_2`) where applicable;
- low-mode projector/subspace distance using a preregistered rank-selection rule;
- sign, permutation, degeneracy and near-degeneracy handling.

Single eigenvectors must not be treated as invariant organizational identifiers.

## Cross-over criterion to freeze

The protocol must define a non-learned qualitative/quantitative cross-over criterion before execution.

Desired pattern, stated as a hypothesis rather than assumed outcome:

- Condition A: `G` changes strongly while `R/P` remain comparatively stable.
- Condition B: `G` remains comparatively stable while `R/P` change substantially.

The criterion must compare relative behavior across G/R/P and must not be tuned after viewing results.

## Interpretation gate

Only two high-level outcomes are authorized after review:

- `GO_CANDIDATE_FOR_SYSTEMATIC_REANALYSIS` — the preregistered cross-over is reproduced on the eligible historical dataset and survives trivial-marginal checks.
- `NO_GO_TOY_MODEL_ONLY` — the cross-over is not reproduced or depends on a construction unavailable in the historical data.

Automatic execution must not assign either outcome. It must stop at `REVIEW_REQUIRED`.

## Protocol-freeze task only

For this task:

1. Create `experiments/TFL-ORG-RECHECK-001/v1.0/`.
2. Inventory historical candidate datasets and freeze inclusion/exclusion criteria.
3. Select exactly one eligible dataset before new metric inspection, or stop if none exists.
4. Write `TFL-ORG-RECHECK-001_PROTOCOL_v1.0.md` and machine-readable config.
5. Freeze exact G/R/P definitions, perturbations, invariances, projector-rank rule, degeneracy handling, cross-over criterion, and trivial-marginal checks.
6. Document algorithm-visible versus evaluator-only information.
7. Create `PROTOCOL_FREEZE.md` with hashes and provenance.
8. Add guards protecting the selected historical raw source and protocol/config.
9. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
10. Do **not** implement or execute in the same task.

After a successful freeze, set the next task to:

**Implement TFL-ORG-RECHECK-001 v1.0 exactly as frozen on the selected historical dataset, serialize transformed/raw G/R/P outputs before evaluator interpretation, then stop at REVIEW_REQUIRED.**

## Scientific gates

- Preserve all frozen predecessor results unchanged.
- No full TFL/RDL re-analysis yet.
- No new simulator or synthetic replacement dataset in this pilot.
- No hostile/attack semantics are required.
- No classifier, neural model, learned representation, learned threshold, or post-hoc tuning.
- No confirmatory/held-out extension.
- No physical quantum claim; Hilbert/operator language is mathematical analogy/state-space language only.
- Negative/null outcome is valid.
- Stop on missing eligible dataset, ambiguous relational definition, leakage, protocol change requirement, or completion of the exploratory run.
