# Current Task

Prepare and execute a scientifically reviewed **TFL-UAS-001B Protocol Revision v1.1 — Exploratory Redesign Only**.

The v1.0 exploratory run remains a preserved failed-validation record and MUST NOT be overwritten, reinterpreted, or used as confirmatory evidence.

## Scientific purpose

Repair two methodological defects identified at the review gate:

1. The simulator made the classes trivially separable in 7/8 simple marginal observables.
2. Model A used a deterministic label-free logistic score rather than the intended supervised logistic-regression baseline.

The redesign must preserve the original research question: distinguish **persistent relational organization** from **mere proximity / aligned motion**.

## Required v1.1 changes

### A. Marginal-matched simulator

Create positive and negative exploratory scenarios whose simple marginal distributions substantially overlap for at least:

- mean speed;
- altitude;
- centroid speed;
- mean pairwise distance;
- group extent;
- mean heading;
- trajectory duration;
- spatial operating region.

Where practical, generate positive/negative scenario pairs from a shared latent macroscopic trajectory envelope so that class identity is not encoded by global speed, altitude, location, scale, heading, or duration.

The intended distinguishing signal should primarily be **temporal dependence of relative relationships**, e.g. persistence/synchrony of pairwise geometry, velocity and acceleration relations.

Do not make coordinated motion mathematically perfect. Do not make the hard negative random dispersal.

### B. Proper supervised baseline boundary

Implement Model A as a real supervised logistic-regression baseline while preserving evaluator isolation.

Use a separate exploratory training partition with labels available only to the training procedure. Test-sample ground truth remains evaluator-only until predictions are serialized.

Training labels must never be exposed as test features or copied into algorithm-visible test samples.

Document the exact train/test boundary and leakage guarantees.

### C. Protocol revision

Create a new protocol/config version (v1.1) rather than modifying frozen v1.0 in place.

Record new hashes and provenance. Preserve v1.0 hashes and all v1.0 exploratory outputs unchanged.

Explicitly document why v1.1 is required: failed anti-trivial-separation validation plus baseline-model interpretation defect.

## Exploratory execution only

After v1.1 is frozen, run only a new exploratory dataset. Do NOT execute:

- confirmatory seeds 201–220;
- held-out seeds 301–320.

Do not reuse the failed v1.0 exploratory metrics as evidence.

If using seeds 101–120 again, ensure generated artifacts are versioned separately under v1.1 and cannot overwrite v1.0 outputs. A new exploratory seed namespace/range is also acceptable if explicitly frozen before execution.

## Required gates before interpreting model results

1. protocol/config hash verification;
2. 001A frozen-manifest validation;
3. v1.0 preservation check;
4. leakage/schema tests;
5. simulator determinism;
6. anti-trivial-separation audit;
7. supervised train/test separation audit.

If the anti-trivial-separation gate still fails, stop again at REVIEW_REQUIRED and do not interpret A/B/C performance.

## Model comparison

Retain the scientific comparison:

- A: conventional supervised fixed-window kinematic logistic regression;
- B: temporal relational model without spectral features;
- C: B plus frozen normalized-Laplacian spectral block.

Retain the registered ablations unless v1.1 explicitly documents a scientifically necessary protocol change.

## Decision discipline

Do not issue GO / PARTIAL GO / NO-GO / INCONCLUSIVE from the exploratory redesign.

Do not authorize confirmatory execution automatically.

After a valid exploratory v1.1 run, freeze all remaining unresolved parameters and stop at review before any confirmatory seed is touched.

## Required repository updates

Update:

- STATUS.md
- docs/decisions.md
- tasks/backlog.md
- protocol/config freeze records for v1.1
- exploratory v1.1 report and diagnostics

Preserve REVIEW_REQUIRED.md as the historical v1.0 review record unless a clearly versioned review archive is preferable.

At completion, set the next task to:

**Review TFL-UAS-001B v1.1 exploratory validation and parameter freeze before confirmatory authorization.**

## Current gate

REVIEW_REQUIRED: v1.1 anti-triviality validation failed. Mean pairwise distance
and group extent each reached one-variable balanced accuracy 1.0. Do not
interpret A/B/C metrics, tune automatically, or execute further seeds. See
`experiments/TFL-UAS-001B/v1.1/REVIEW_REQUIRED_v1.1.json`.
