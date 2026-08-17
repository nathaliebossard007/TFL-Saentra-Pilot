# REVIEW_REQUIRED — TFL-UAS-SPATIAL-001 Exploratory v1.0

## What happened

The frozen SPATIAL-001 v1.0 implementation generated 100 opaque
algorithm-visible track samples: 20 seeds (101–120) across S1–S5. Relational
states were serialized before evaluator-only scenario metadata was loaded.
No classifier or 001B confirmatory/held-out seed was executed.

## Relevant descriptive diagnostics

| Scenario | Pair persistence | Global persistence | Mean state distance | Shape change |
|---|---:|---:|---:|---:|
| S1 translation | 0.997 | 1.000 | 2.760 | 0.007 |
| S2 rotation | 0.997 | 1.000 | 2.746 | 0.017 |
| S3 independent motion | 0.815 | 0.484 | 5.888 | 0.105 |
| S4 apparent organization | 0.929 | 0.933 | 18.493 | 0.119 |
| S5 perturbation/recovery | 0.986 | 1.000 | 7.853 | 0.031 |

These are exploratory diagnostics only, not a scientific decision.

## Why automatic continuation stopped

The protocol requires a review stop after the exploratory run and before any
benchmark, classifier, or confirmatory extension. The registered state-distance
and recovery diagnostics require methodological review before being treated as
validated measurements. No GO, PARTIAL GO, NO-GO, or INCONCLUSIVE decision is
made here.

## Options

1. Accept the state definitions and authorize a separately specified extension.
2. Review or revise state-distance normalization and recovery measurement in a
   new protocol version.
3. Preserve SPATIAL-001 as a technical exploratory record without extension.

## Recommended conservative action

Review the raw states, invariance diagnostics, apparent-control behavior, and
recovery calculation. Freeze any approved measurement revisions before any
benchmark, classification, or confirmatory work.
