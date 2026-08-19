# HUMAN REVIEW — TFL-ORG-RELREP-001 v1.0

**Date:** 2026-08-19  
**Outcome:** `REPRESENTATION_INSUFFICIENT`

## Scope

This review interprets only the frozen `TFL-ORG-RELREP-001 v1.0` protocol, implementation, and raw exploratory outputs. It does not modify predecessor results and does not reject the broader relational-organization hypothesis.

## 1. Execution integrity

The exploratory run completed on the unchanged frozen DYNAMIC-001 algorithm-visible source:

- 120 samples;
- 4 stable tracks per sample;
- 181 timestamps per sample;
- raw `G`, `R_id`, `R_wt`, `R_t`, and `P` representations serialized before evaluator interpretation;
- no evaluator metadata, classifier, learned representation, confirmatory, or held-out execution;
- schema, determinism, source-count, and frozen-hash checks passed.

The implementation is therefore technically admissible for human review.

## 2. Condition A — realization change / relation preserved

Condition A subtracts the centroid, applies a fixed 37-degree z rotation, and scales centered positions and kinematics by 1.80.

Under the frozen definitions:

- pair geometry changes strongly;
- normalized distance ratios are invariant under the common scale factor;
- velocity-direction cosines are invariant under common rotation and positive scaling;
- therefore the deterministic `R_wt` construction is invariant by construction;
- the top-two incident-edge selection and `R_id` induced from those weights are consequently invariant apart from numerical tie edge cases;
- `R_t` is correspondingly invariant when its underlying registered relation sequence is invariant.

Condition A therefore supports the intended separation between geometric realization and the registered relation representation. This is primarily a construction/invariance check, not independent evidence of organizational state.

## 3. Condition B — frozen definition exposes a representation conflict

Condition B applies a degree-preserving graph 2-switch to `R_id` while preserving raw geometry.

However, `R_id` is stored for comparison as the lexicographically minimal adjacency encoding over all 24 node permutations. This deliberately treats graph-isomorphic relabelings as equivalent.

With four nodes and the frozen top-two-incident-edge union, valid degree-preserving 2-switch cases are dominated by sparse four-node graphs for which the switched graph can be graph-isomorphic to the source graph. In the canonicalized `R_id` view, a change in the labeled endpoint pairing can therefore map to the same `R_id` representation.

This creates a direct mismatch between two frozen intents:

1. preserve `who is coupled to whom`;
2. quotient all node permutations as mere relabeling.

For anonymous structural organization these may legitimately be equivalent. For stable coupling identity they are not. A single `R_id` representation cannot serve both meanings without an explicit identity/role layer.

## 4. Information-loss interpretation

The v1.0 protocol correctly treats `P` as a potentially lossy operator summary, but the current review finds an earlier loss channel:

\[
\text{labeled coupling state}
\longrightarrow
R_{id}^{\mathrm{canonical}}
\]

can already be many-to-one before the operator `P` is constructed.

Therefore a case in which `P` fails to distinguish two B states cannot by itself be attributed uniquely to operator information loss, because `R_id` may already have quotiented away the endpoint-assignment difference.

The scientifically important distinction is now:

\[
R_{\mathrm{labeled}}
\neq
R_{\mathrm{structural\ quotient}}
\neq
P.
\]

These must be retained as separate representations in the next version.

## 5. Why the outcome is `REPRESENTATION_INSUFFICIENT`

The frozen interpretation gate permits `RELATIONAL_REPRESENTATION_CANDIDATE` only if the explicit relational representation survives invariance controls and distinguishes the registered relational changes without unsupported semantics.

v1.0 does not meet that requirement because its canonical `R_id` conflates two different questions:

- structural equivalence up to anonymous node permutation;
- persistent endpoint/coupling identity.

The representation is therefore insufficient for the stated primary question `who is coupled to whom`.

This is a representation-design result, not a falsification of relational organization.

## 6. Required conceptual correction before any new run

A follow-up must separate at least three layers before operator construction:

1. **`R_labeled`** — stable endpoint/coupling identity in source track coordinates;
2. **`R_struct`** — graph structure modulo permitted node permutations/isomorphisms;
3. **`R_role`** — optional role-equivalence layer only if roles are independently and non-semantically defined from observable structure.

Then `P` must be derived from one explicitly named layer, and information-loss tests must state which map is being tested:

\[
R_{\mathrm{labeled}}\to R_{\mathrm{struct}},
\qquad
R_{\mathrm{struct}}\to P,
\qquad
R_{\mathrm{labeled}}\to P.
\]

No new operator should be introduced merely to force Condition B to pass.

## 7. Research consequence

The strongest surviving lesson is not that node labels are always organizationally meaningful. It is that organizational equivalence cannot be defined by silently quotienting all identities before deciding which identities, roles, or dependencies the application treats as interchangeable.

The next theoretical question is therefore:

> Which permutations are organizational symmetries, and which permutations change organizational state?

That symmetry relation must be defined before quotienting the relational representation.
