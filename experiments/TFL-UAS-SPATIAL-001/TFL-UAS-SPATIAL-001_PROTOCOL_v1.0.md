# TFL-UAS-SPATIAL-001 Protocol v1.0

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-17

## Research question

Can a deterministic, unlabeled spatial relational state detect persistent
organization independently of absolute position, orientation, scale, and
predefined group labels? The primary test is invariance under
organization-preserving transformations and degradation when same-object
relations are destroyed.

This is synthetic exploratory work. No classifier, neural model, 001B
confirmatory seed, or held-out seed is authorized.

## Input and isolation

The algorithm receives four established tracks with stable within-sample track
identities and timestamps. Algorithm-visible records contain only track state:
position, velocity, acceleration, uncertainty, track ID, and time. Scenario
identity and evaluator controls are written separately under
`data/evaluator_only/` and may be loaded only after raw relational-state
outputs have been serialized. Raw state trajectories and diagnostics precede
any interpretation.

Exploratory seeds are 101–120 in this experiment's own namespace. No filename
or algorithm feature encodes the scenario identity or seed.

## Relational state construction

For every pair, define `R_ij(t)` from Euclidean distance, distance derivative,
relative velocity, relative heading, and normalized distance. Construct a
weighted graph `G_t=(V,E_t,W_t)` from deterministic pair weights based on
registered scale parameters only. Define:

- **Rigid Relational State**: pair distances, distance derivatives, and
  relative headings; invariant to common translation and rotation but not
  physical scale.
- **Shape State**: rigid relations normalized by instantaneous group extent;
  additionally scale-normalized, while the rigid state preserves real
  expansion/contraction.
- **Local state** `N_i(t)`: weighted summaries of the relations incident to
  object `i`, including persistence and neighborhood-weight statistics.
- **Global state** `S_t`: deterministic graph summaries, weighted edge
  persistence, connectivity, clustering, graph-state distance, and normalized
  Laplacian summaries. Where degrees are nonzero,
  `L_norm = I - D^(-1/2) W D^(-1/2)`; zero-degree handling is registered as
  identity contribution with an explicit diagnostic.

No label, scenario class, or learned parameter enters these constructions.

## Scenarios

- **S1 Global Translation**: identical organization translated through the
  operating area. Expected rigid-state invariance; coordinate displacement is
  large.
- **S2 Global Rotation / Formation Maneuver**: common translation and rotation
  of the same formation with bounded motion noise. Expected rigid-state
  invariance despite coordinate and heading changes.
- **S3 Independent Random Motion**: similar initial arrangement followed by
  independent bounded maneuvers. Expected decaying pair/local/global
  persistence and increasing state distance.
- **S4 Apparent Spatial Organization**: matched local density and
  speed/heading distributions with temporary proximity, but no persistent
  same-object relational organization. Expected low stable-global persistence
  and a recorded false-persistence rate.
- **S5 Perturbation and Recovery**: stable organization, registered temporary
  disturbance, then restoration. Expected state distance increase during the
  disturbance, decline after restoration, and measurable recovery latency.

Scenario identities are evaluator-only. No scenario-specific thresholds may be
chosen after inspecting evaluator identities.

## Measurements and gates

Report pair relational persistence, local relational persistence, global
relational-state persistence, `D_S(t1,t2)`, temporal state-change magnitude,
recovery latency, apparent-control false persistence, and sensitivity to
translation, rotation, and scale. Do not begin with F1 or a group classifier.

Before execution, verify protocol/config hashes, the 001A frozen manifest,
algorithm/evaluator schema separation, absence of labels in algorithm-visible
data, deterministic regeneration, and raw-output ordering. Any leakage,
unexpected methodological issue, or failed exploratory validation creates
`REVIEW_REQUIRED` and stops further work.

After the exploratory run, stop at review before benchmark, classification,
or confirmatory extension. No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision is
authorized by this protocol-freeze task.
