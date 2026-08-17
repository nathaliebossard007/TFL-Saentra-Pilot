# Current Task

REVIEW_REQUIRED: review the completed **TFL-UAS-SPATIAL-001 exploratory v1.0** before any extension.

The protocol-freeze and exploratory implementation tasks are complete. Do not modify the frozen protocol or
configuration, do not execute 001B confirmatory/held-out seeds, and do not
add classification or benchmark extensions. Write raw relational-state
outputs before interpretation and stop at `REVIEW_REQUIRED` after the
exploratory run.

Frozen files:

- `experiments/TFL-UAS-SPATIAL-001/TFL-UAS-SPATIAL-001_PROTOCOL_v1.0.md`
- `experiments/TFL-UAS-SPATIAL-001/config/tfl_uas_spatial_001_protocol_v1.json`
- `experiments/TFL-UAS-SPATIAL-001/PROTOCOL_FREEZE.md`

The prior protocol-freeze branch description follows for provenance:

Start a new exploratory branch:

**TFL-UAS-SPATIAL-001 — Spatial Relational State Persistence**

This is a perspective shift away from group-label classification. Preserve TFL-UAS-001B v1.0 and v1.1 unchanged as failed anti-trivial-separation classification-path records. Do not continue automatic 001B simulator tuning.

## Primary research question

Can persistent relational spatial organization be detected independently of absolute position, orientation, scale, and predefined group labels?

## Core principle

Model the observation space as:

`space -> relations -> organization -> state change`

Do not ask primarily whether a sample belongs to a coordinated-group class. Instead construct and test an unlabeled **Spatial Relational State** `S_t` from relations between established object tracks.

Algorithms may use track identity only as a stable within-sample reference. No group label or coordination label may be algorithm-visible.

## Required relational layers

Define explicitly before execution:

1. Pair relational state `R_ij(t)` using interpretable quantities such as pairwise distance, normalized distance, relative velocity, distance derivative, and relative heading.
2. Local relational neighborhood state `N_i(t)` summarizing persistent relations of each object.
3. Global spatial relational state `S_t` based on the weighted relational graph and deterministic graph/operator summaries.

Maintain two parallel representations where useful:

- **Rigid Relational State**: translation/rotation invariant but not scale invariant.
- **Shape State**: additionally normalized for scale.

This distinction must prevent physically meaningful expansion/contraction from being erased by normalization.

## Candidate graph/operator layer

Construct a time-dependent weighted relational graph `G_t=(V,E_t,W_t)` without ground-truth labels. Include the normalized Laplacian where mathematically meaningful:

`L_norm(t) = I - D^(-1/2) W_t D^(-1/2)`

Candidate deterministic diagnostics may include pair-relation persistence, local-neighborhood persistence, graph-state distance, spectral gap, eigenvalue quantiles, eigenspace/projector distance, connectivity, clustering, and temporal operator change.

No learned classifier is required for the first experiment.

## Required exploratory scenarios

Implement at minimum:

S1 — Global Translation
- Same relational organization translated through space.
- Expected: relational state remains approximately invariant.

S2 — Global Rotation / Formation Maneuver
- Same relational organization translated and rotated over time.
- Expected: rigid relational organization remains approximately invariant despite large coordinate changes.

S3 — Independent Random Motion
- Similar initial spatial arrangement, then independent motion.
- Expected: relational persistence decays and state distance increases.

S4 — Apparent Spatial Organization
- Similar local density, speed/heading distribution, and temporary proximity without persistent same-object relational organization.
- Expected: density/proximity alone must not produce stable global relational state.

S5 — Perturbation and Recovery
- Stable organization, temporary disturbance, then restoration of the prior organization.
- Expected: state distance rises during disturbance and falls after recovery; record recovery latency.

## Primary measurements

Do not start with coordinated-group classification F1.

Define and measure at minimum:

- pair relational persistence;
- local relational persistence;
- global relational-state persistence;
- relational-state distance `D_S(t1,t2)`;
- temporal state-change magnitude;
- recovery latency after perturbation;
- false persistence in the apparent-organization control;
- sensitivity to translation, rotation, and scale changes.

The first falsification question is:

**Does the proposed relational state show the expected invariances under organization-preserving transformations and degrade when the underlying same-object relational organization is destroyed?**

## Scientific discipline

- Synthetic only.
- No real sensor data.
- No group-label classifier in the primary test.
- No neural model.
- No post-hoc feature invention after viewing evaluator scenario identities.
- Ground truth / scenario identity remains evaluator-only until state outputs are serialized.
- Raw state trajectories and diagnostics must be written before interpretation.
- Negative results are valid.

## 001B status

Do not modify or reinterpret TFL-UAS-001B v1.0/v1.1.

Confirmatory seeds 201–220 and held-out seeds 301–320 from 001B remain prohibited.

## Required workflow

1. Create and freeze `TFL-UAS-SPATIAL-001` protocol v1.0 and config before implementation.
2. Record protocol/config SHA-256 hashes.
3. Add leakage and reproducibility gates.
4. Implement only after the protocol freeze.
5. Run exploratory scenarios only.
6. Stop at `REVIEW_REQUIRED` before any later benchmark/classification/confirmatory extension.

At completion of the protocol-freeze task, set the next task to implement **TFL-UAS-SPATIAL-001 exploratory v1.0 exactly as frozen**. Do not execute the exploratory run in the same protocol-freeze task.

## Current gate

REVIEW_REQUIRED: the exploratory implementation and run are complete. Review
`experiments/TFL-UAS-SPATIAL-001/REVIEW_REQUIRED.md` before any benchmark,
classifier, or confirmatory extension.
