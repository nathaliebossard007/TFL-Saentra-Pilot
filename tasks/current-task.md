# Current Task

## REVIEW_REQUIRED — TFL-ORG-SYM-001 v1.0 exploratory run

The frozen exploratory implementation completed on 120 unchanged
DYNAMIC-001 algorithm-visible samples. Raw outputs were serialized before
interpretation and evaluator-only metadata was not loaded. Review the record
at `experiments/TFL-ORG-SYM-001/v1.0/REVIEW_REQUIRED.md`.

Do not assign `NONTRIVIAL_ORG_SYMMETRY_CANDIDATE`,
`IDENTITY_ONLY_ON_SELECTED_SOURCE`, or `SYMMETRY_MODEL_INSUFFICIENT`, and do
not execute confirmatory, held-out, classifier, or protocol-extension work
until human review is documented.

The authorized implementation task is complete and is retained below for
provenance.

## AUTHORIZED — TFL-ORG-SYM-001 exploratory implementation

Implement `TFL-ORG-SYM-001 v1.0` exactly as frozen, serialize labeled,
structural, and named operator-layer transformation outputs before
interpretation, then stop at `REVIEW_REQUIRED`. Preserve RELREP v1.0 and all
predecessor records unchanged.

Frozen files:

- `experiments/TFL-ORG-SYM-001/v1.0/TFL-ORG-SYM-001_PROTOCOL_v1.0.md`
- `experiments/TFL-ORG-SYM-001/v1.0/config/tfl_org_sym_001_protocol_v1.json`
- `experiments/TFL-ORG-SYM-001/v1.0/PROTOCOL_FREEZE.md`

The prior protocol-freeze task follows for provenance.

## AUTHORIZED — TFL-ORG-SYM-001 protocol freeze only

Use these records as the governing research basis:

- `docs/TFL-ORG-CONSOLIDATED-ANCHOR-001.md`
- `experiments/TFL-ORG-RELREP-001/v1.0/HUMAN_REVIEW.md`

Preserve `TFL-ORG-RELREP-001 v1.0` unchanged as `REPRESENTATION_INSUFFICIENT`.
Do **not** repair or reinterpret that result after the fact.

Open a narrow theoretical/empirical follow-up:

**TFL-ORG-SYM-001 — Organizational Symmetry Before Quotienting**

## Scientific purpose

Determine which permutations of persistent entities are justified as organization-preserving symmetries and which permutations change the organizational state.

The experiment must not assume that all node permutations are symmetries, and must not assume that no node permutations are symmetries.

Primary question:

**Which identity transformations can be quotiented without losing organization-relevant information?**

## Required representation layers

The protocol must freeze these layers separately before any execution:

- `R_labeled` — relation graph/matrix in stable source-track identity, preserving concrete endpoint assignment;
- `R_struct` — structural relation modulo only an explicitly registered permutation set `G_allow`;
- `R_role` — optional role quotient only if a role partition can be independently defined from algorithm-visible observables without evaluator labels or semantic invention;
- `P_labeled` and/or `P_struct` — operator summaries only if the source relational layer is named explicitly. No operator is itself the organizational state.

Do not collapse the layers into one score.

## Symmetry definition gate

Before execution, define a candidate admissible permutation set

`G_allow(X)`

or a state-independent `G_allow` only if justified.

A permutation `g` may be treated as an organizational symmetry only when the protocol preregisters observable criteria under which

`C(gX) ≅ C(X)`

without using the desired experimental outcome.

The protocol must explicitly allow the possibility that admissible symmetries are:

- only the identity;
- a proper subgroup of the full permutation group;
- state-dependent stabilizers;
- not representable by one global group at all.

If closure/composition fails for the observed admissible transformations, record a groupoid/pseudogroup-style interpretation rather than forcing a group model.

## Required permutation classes

Freeze at least the following classes separately:

1. **Identity-preserving relabeling control** — representation/index relabeling with the physical coupling assignment transformed consistently. This should not count as an organizational change.
2. **Endpoint reassignment** — stable entities retain identity while coupling endpoints are reassigned. This is a candidate organizational change and must not be quotiented automatically.
3. **Role-preserving entity swap** — only if an independently defined observable role partition exists; swap entities inside the same role class while preserving registered role/dependency constraints.
4. **Cross-role swap** — only if roles are independently defined; exchange entities across distinct role classes while keeping realization as similar as feasible.

If `R_role` cannot be justified from existing historical data, freeze the protocol without it rather than inventing roles.

## Dataset gate

Before implementation or result inspection:

1. Inventory frozen historical sources already present in the repository.
2. Prefer the unchanged DYNAMIC-001 algorithm-visible source if it supports stable track identity and the required permutation tests.
3. No new simulator or synthetic replacement data is authorized in this task.
4. No evaluator labels may be used to define symmetry, role, or admissibility.
5. Record all algorithm-visible and evaluator-only fields before any new metric inspection.

## Required diagnostics

For every registered transformation, compare separately:

- labeled edge/dependency equality and Jaccard;
- structural equality under `G_allow`;
- degree sequence;
- edge-weight difference where justified;
- temporal relation-transition difference;
- optional role-partition preservation;
- operator summary difference only as a downstream diagnostic.

Explicitly distinguish:

- mere coordinate/index relabeling;
- graph isomorphism;
- permitted organizational symmetry;
- forbidden/non-permitted permutation;
- endpoint reassignment;
- role-preserving substitution;
- role-breaking substitution.

Graph isomorphism alone must **not** be treated as proof of organizational equivalence.

## Information-loss maps

The protocol must preregister and evaluate the maps separately:

`R_labeled -> R_struct`

`R_labeled -> R_role`  (only if independently justified)

`R_struct -> P_struct`

`R_labeled -> P_labeled`

For each map, record collisions: distinct source states that become indistinguishable after the map.

A collision is a valid result, not an implementation failure.

## Falsification / stop conditions

Stop and return to human review if any of the following occurs:

- no nontrivial symmetry can be justified from algorithm-visible data;
- candidate `G_allow` depends on evaluator semantics;
- role definitions are post-hoc or semantically invented;
- closure required for a claimed group fails;
- the protocol would need a new simulator or tuned operator;
- stable source identity cannot be maintained;
- a protocol change is required after seeing results.

Negative outcome is valid: the correct symmetry model may be identity-only for the selected source.

## Interpretation gate

After a later exploratory execution, only human review may assign one of these high-level outcomes:

- `NONTRIVIAL_ORG_SYMMETRY_CANDIDATE` — at least one non-identity transformation is independently justified and preserves the registered organizational constraints while endpoint/role-breaking controls remain distinguishable;
- `IDENTITY_ONLY_ON_SELECTED_SOURCE` — no nontrivial permutation survives the preregistered organizational-symmetry criteria on the selected source;
- `SYMMETRY_MODEL_INSUFFICIENT` — the proposed symmetry definition conflates distinct organizational states, depends on unsupported role semantics, or is otherwise not operationally adequate.

Do not assign an outcome automatically.

## Protocol-freeze task only

For this task:

1. Create `experiments/TFL-ORG-SYM-001/v1.0/`.
2. Inventory eligible historical datasets and freeze the selected source before new result inspection.
3. Write `TFL-ORG-SYM-001_PROTOCOL_v1.0.md` and machine-readable config.
4. Freeze exact `R_labeled`, `R_struct`, optional `R_role`, and named operator-layer definitions.
5. Freeze candidate `G_allow` logic and whether it is global, state-dependent, or intentionally left as stabilizer sets.
6. Freeze permutation classes and controls.
7. Freeze information-loss maps and collision diagnostics.
8. Freeze temporal windows and comparison metrics.
9. Document leakage boundaries and unsupported role handling.
10. Create `PROTOCOL_FREEZE.md` with hashes and provenance.
11. Add guards protecting all predecessor records and the selected historical source.
12. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
13. Do **not** implement or execute in the same task.

After a successful freeze, set the next task to:

**Implement TFL-ORG-SYM-001 v1.0 exactly as frozen, serialize all labeled/structural/optional-role transformation outputs before interpretation, then stop at REVIEW_REQUIRED.**

## Scientific gates

- No classifier, neural model, learned representation, learned symmetry, or learned threshold.
- No new simulator or synthetic replacement dataset.
- No new operator introduced merely to obtain a positive result.
- No hostile/attack semantics.
- Preserve all predecessor records unchanged.
- `TFL-RELSTATE-001` remains deferred.
- Do not define quotient distance or quotient geometry yet.
- First determine the admissible symmetry relation; quotienting comes only afterward.
