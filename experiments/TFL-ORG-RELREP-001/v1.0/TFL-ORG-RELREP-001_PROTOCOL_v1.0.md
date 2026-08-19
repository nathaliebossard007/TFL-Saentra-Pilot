# TFL-ORG-RELREP-001 Protocol v1.0 — Minimal Relational Representation

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-19

## Scope and selected source

This follow-up preserves `TFL-ORG-RECHECK-001 v1.0` unchanged, including its
`NO_GO_TOY_MODEL_ONLY` outcome for the preregistered cross-over criterion. It
uses the same frozen DYNAMIC-001 algorithm-visible source:
`experiments/TFL-UAS-DYNAMIC-001/data/algorithm_visible/`, 120 opaque samples,
four stable tracks, 181 timestamps. Evaluator-only files are excluded from
algorithm input. No new simulator, dataset, classifier, learned threshold,
or systematic re-analysis is authorized.

## Parallel representations

All views are emitted separately; no combined score is defined.

### G — geometry baseline

At each timestamp, retain the six labeled pair distances, six relative-speed
magnitudes, and their temporal first differences. G is a realization baseline,
not the organizational state.

### R_id — explicit coupling identity

Construct the deterministic undirected four-node graph from the frozen
normalized distance/velocity-direction edge weights used in RECHECK v1.0:
select the top two incident edges per node, union the selections, and break
ties by pair index. Preserve canonical source track IDs in the raw view.
For comparisons under node permutation, canonicalize by lexicographically
minimum adjacency encoding over all 24 permutations; a permutation-equivalent
graph is not a relational change.

### R_wt — relation weights

R_wt is supported by the source because position and velocity fields exist.
For pair `(i,j)`, use the frozen deterministic weight
`exp(-((d/median(d))^2 + ((1+cos(v_i,v_j))/2)^2)/2)` with median-distance floor
1 m. Missing/non-finite velocity or distance yields a missing edge weight, not
zero. Store the complete symmetric weighted matrix separately from R_id.

### R_t — temporal relation state

For windows of 5, 15, and 30 seconds, retain the ordered sequence of canonical
R_id edge encodings and R_wt matrices. A transition is the tuple
`(edge-set delta, weighted Frobenius delta, node permutation used for
canonicalization)`. Missing timestamps break a transition; they are not
imputed.

### P — lossy operator diagnostics

Only after R_id/R_wt are constructed, emit normalized-Laplacian summaries for
the weighted R_wt matrix: zero-degree inverse factor zero with identity
diagonal, ordered eigenvalues, lambda2 when defined, and rank-2 projector only
when the eigengap around rank 2 is at least `1e-6`. Projector distance is
Frobenius distance divided by `sqrt(4)`. Never compare single eigenvector
signs; near-degenerate projectors are missing.

## Canonicalization and equivalence

Node IDs are stable within a source sample but are not treated as semantic
roles. Graph equality is checked both in source labeling and under the
24-permutation canonical form. R_id differences are classified as:

1. mere relabeling/isomorphism;
2. degree-sequence equivalent but non-isomorphic or edge-different;
3. explicitly relationally different.

R_t additionally records temporal equivalence only when every registered
window transition is canonical-equivalent and weight differences are within
`1e-9`; otherwise it records temporal divergence.

## Registered transformations

### A — realization change, relational organization preserved

Subtract the object centroid, rotate positions/velocities/accelerations by 37
degrees about z, and scale centered positions and kinematics by 1.80. Under
the normalized R_wt definition, R_id/R_wt/R_t are expected invariant by
construction; G changes. Source records are never overwritten.

### B — relational change, realization preserved

Apply the lexicographically first valid degree-preserving graph 2-switch to
R_id. Keep source G and R_wt unchanged, and set the perturbed R_wt edges to
the corresponding source weights of the switched endpoint pairs. Reject
self-loops, duplicate edges, and unavailable switches explicitly. This tests
whether explicit relation identity and temporal representation retain a
change that P may lose.

## Mandatory information-loss test

For every valid B state, record whether the source and perturbed states have:

- identical P summaries within `1e-9` while R_id differs;
- equal degree sequence;
- canonical graph isomorphism or genuine edge difference;
- equal or divergent R_t transitions.

`P(X1)=P(X2)` with `R_id(X1) != R_id(X2)` is a valid information-loss result,
not an implementation failure. Spectral/cospectral equivalence must be
reported separately from graph isomorphism and degree equivalence.

## Metrics and integrity gates

Report G pair-distance change/correlation; R_id edge Jaccard, canonical
equivalence, degree sequence, and changed-edge count; R_wt weighted Frobenius
and missing-edge counts; R_t transition overlap and divergence; and P spectrum,
lambda2, projector, and degeneracy diagnostics. No metric is collapsed into a
learned score. Trivial-marginal checks compare G changes and degree sequences
before interpretation.

Raw parallel representations and transformed states must be serialized before
evaluator-only metadata is loaded. Determinism, source immutability, schema
separation, and frozen-hash checks are mandatory. Stop at `REVIEW_REQUIRED`
after exploratory execution; do not assign an interpretation outcome
automatically.
