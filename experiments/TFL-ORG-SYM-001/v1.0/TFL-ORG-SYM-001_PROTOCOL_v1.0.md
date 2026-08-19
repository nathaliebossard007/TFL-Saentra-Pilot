# TFL-ORG-SYM-001 Protocol v1.0 — Organizational Symmetry Before Quotienting

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-19

## Lineage and selected source

This follow-up preserves `TFL-ORG-RELREP-001 v1.0` unchanged as
`REPRESENTATION_INSUFFICIENT` and uses the same frozen DYNAMIC-001
algorithm-visible source: 120 opaque samples, four stable tracks, 181
timestamps. Evaluator-only files, scenario labels, seeds, and prior review
outcomes are not algorithm inputs. No new simulator or dataset is authorized.

## Representation layers

`R_labeled` uses stable source-track identity and the complete symmetric
weighted relation matrix. Endpoint assignment is concrete; permutations are
not silently treated as relabeling. `R_struct` is derived only through the
candidate admissible set `G_allow(X)` below. `R_role` is intentionally omitted:
the selected source has no independent algorithm-visible role partition.

Named downstream `P_labeled`/`P_struct` diagnostics may include normalized
Laplacian spectrum, lambda2, and a rank-2 projector only when the eigengap
around rank 2 is at least `1e-6`. Zero-degree inverse factor is zero with
identity diagonal. No quotient distance or quotient geometry is defined.

## Candidate admissible symmetries

Enumerate all 24 node permutations. For each state and windows 5, 15, and 30
seconds, a permutation is a candidate element of state-dependent `G_allow(X)`
only if it preserves within `1e-9` the full weighted temporal relation
sequence, the complete geometry/kinematics sequence, and every relation
transition encoding after endpoint permutation. Identity is always retained;
non-identity elements are not assumed.

Test closure and composition on observed candidate sets. If closure fails,
record a groupoid/pseudogroup-style relation and do not force a global group.

## Permutation classes

1. Identity-preserving index relabeling transforms every physical endpoint
   assignment consistently and is not an organizational change.
2. Endpoint reassignment retains stable identities and applies the
   lexicographically first valid degree-preserving 2-switch; it is never
   quotiented automatically.
3. Role-preserving entity swap is unavailable because `R_role` is unsupported.
4. Cross-role swap is unavailable for the same reason.

## Diagnostics and information-loss maps

For every transformation, record labeled edge equality/Jaccard, structural
equality under `G_allow`, degree sequence, weighted difference, temporal
transition difference, and named operator differences. Distinguish coordinate
relabeling, graph isomorphism, permitted symmetry, endpoint reassignment, and
forbidden permutation. Record collisions for `R_labeled -> R_struct`,
`R_struct -> P_struct`, and `R_labeled -> P_labeled`. Degree equivalence,
isomorphism, cospectrality, and organizational equivalence remain separate.

## Leakage and stop rules

Only algorithm-visible IDs, timestamps, positions, velocities, accelerations,
and uncertainty fields may be read. Raw labeled/structural transformations
must be serialized before evaluator interpretation. Stop at `REVIEW_REQUIRED`
if no nontrivial symmetry is justified, closure fails, roles remain
unsupported, or a protocol change is needed. Human review alone may assign
`NONTRIVIAL_ORG_SYMMETRY_CANDIDATE`, `IDENTITY_ONLY_ON_SELECTED_SOURCE`, or
`SYMMETRY_MODEL_INSUFFICIENT`.
