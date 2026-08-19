# TFL-ORG-RECHECK-001 Protocol v1.0 — Geometry / Relation / Projector Cross-over

Status: FROZEN FOR PROTOCOL-FREEZE TASK ONLY — 2026-08-19

## Scope and selected historical source

This pilot re-evaluates one pre-existing dataset before any systematic
TFL/RDL re-analysis. The selected source is the algorithm-visible track data
from `experiments/TFL-UAS-DYNAMIC-001/data/algorithm_visible/`, consisting of
120 opaque samples with four stable per-object tracks and position, velocity,
acceleration, timestamp, and uncertainty fields. It predates
TFL-ORG-SNAPSHOT-001, remains unchanged, and contains no evaluator labels.

Candidate inventory was recorded before any new G/R/P metric inspection:

| Candidate | Decision | Reason |
|---|---|---|
| TFL-UAS-DYNAMIC-001 algorithm-visible tracks | SELECTED | Per-object temporal state and stable IDs support G/R/P construction; raw source is frozen and pre-existing. |
| TFL-UAS-SPATIAL-001 algorithm-visible tracks | EXCLUDED | Pre-existing relational-state source, but its registered input is reserved for the separate SPATIAL-001 lineage and is not the selected historical basis for this pilot. |
| TFL-UAS-001A observation files | EXCLUDED | Sensor detections do not provide stable per-object temporal nodes without reintroducing the frozen tracking problem. |
| TFL-UAS-001A evaluator/ground-truth files | EXCLUDED | Evaluator-only and never algorithm-visible. |

No G/R/P cross-over results were inspected during this freeze. If the
selected source is unavailable or schema verification fails, execution must
stop with `REVIEW_REQUIRED` and `NO ELIGIBLE HISTORICAL DATASET`.

## Information separation

The algorithm may read only the selected `data/algorithm_visible` files. It
may not read evaluator-only metadata, scenario identifiers, seeds, or labels
until transformed/raw G/R/P outputs have been serialized. Evaluator metadata
may be loaded only afterward for audit and review diagnostics.

## Registered bases

For every sample and registered timestamp, emit parallel bases without a
learned score:

- `G`: all six pair distances and relative velocity magnitudes;
- `R`: a deterministic undirected graph on four nodes, formed from the top
  two incident pair weights per node using frozen normalized distance and
  velocity-direction coherence; ties break by pair index;
- `P`: normalized Laplacian of `R`, with unit edge weights, zero-degree inverse
  factor zero and identity diagonal, ordered eigenvalues, algebraic
  connectivity `lambda_2`, and low-mode projector rank 2 only when the gap
  around rank 2 is at least `1e-6`.

No individual eigenvector is compared. Projector distance is Frobenius
distance divided by `sqrt(4)` and is invariant to sign and basis rotation.

## Counterfactual conditions

Counterfactuals are derived per sample without evaluator labels and never
overwrite source files.

### A — geometry-breaking / organization-preserving

For each timestamp, subtract the four-object centroid, apply a fixed
rotation of 37 degrees around z, and multiply centered positions by 1.80.
Multiply velocities and accelerations by 1.80 after rotation; preserve track
IDs and timestamps. G uses physical distances and therefore must respond to
the scale change. R/P use normalized distances and velocity direction, so
their registered relational construction is invariant by rule.

### B — geometry-preserving / organization-breaking

Construct the registered R graph from the unmodified sample, then apply one
deterministic degree-preserving 2-switch to edges `(a,b)` and `(c,d)`, choosing
the lexicographically first valid non-edge replacement `(a,c),(b,d)` that
changes the edge set, avoids self-loops and duplicate edges, and preserves
all node degrees. Positions and velocities remain unchanged. If no valid
2-switch exists, record B as unavailable; do not invent a replacement.

## Metrics

### G

Record mean and median pair-distance change, pair-distance Pearson
correlation where defined, and relative-velocity magnitude change. Aggregates
use valid finite values only; undefined correlations are missing.

### R

Record edge-set Jaccard overlap, degree sequence equality, and changed-edge
count. No semantic role is inferred beyond graph adjacency.

### P

Record normalized-Laplacian spectrum distance, `lambda_2` change, and rank-2
projector distance when both eigengaps meet `1e-6`. Repeated or near-repeated
eigenspaces produce a missing projector distance, not an arbitrary basis
comparison.

## Frozen cross-over criterion

The desired pattern is evaluated separately for A and B, never collapsed into
a learned score. A qualifies as a geometric/relational cross-over if G mean
distance change is at least 0.50, while R Jaccard is exactly 1.0 and defined P
distances are at most `1e-9`. B qualifies as a relational/operator cross-over
if G pair-distance correlation is at least 0.95, while R Jaccard is at most
0.80 and either spectrum distance is at least 0.10 or `lambda_2` change is at
least 0.05; projector evidence is recorded when defined but is not required
when rank degeneracy makes it unavailable.

Trivial-marginal checks compare A/B changes in mean distance, median distance,
and degree sequence before any interpretation. No threshold is fitted after
inspection.

## Freeze boundary and interpretation gate

This task freezes the protocol only. No implementation, transformed output,
metric inspection, or outcome assignment is authorized. Later exploratory
execution must serialize transformed/raw G/R/P outputs before evaluator
interpretation and stop at `REVIEW_REQUIRED`.

Only later human review may consider `GO_CANDIDATE_FOR_SYSTEMATIC_REANALYSIS`
or `NO_GO_TOY_MODEL_ONLY`. No other scientific decision is authorized.
