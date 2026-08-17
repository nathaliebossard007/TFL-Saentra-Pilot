# REVIEW_REQUIRED — TFL-UAS-DYNAMIC-001 Exploratory v1.0

## What happened

The frozen DYNAMIC-001 v1.0 pipeline generated 120 opaque algorithm-visible
track samples: 20 exploratory seeds (101–120) across D1–D6. It constructed
registered motion relations over 5/15/30 second windows and 1/5/15/30 second
lags. Raw dynamic relational states were serialized before evaluator-only
metadata was loaded. No classifier, benchmark, confirmatory, or held-out run
was executed.

## Descriptive diagnostics

| Scenario | Lag 1 persistence | Lag 15 persistence | 30 s window distance | Spatial change | Motion change | Recovery |
|---|---:|---:|---:|---:|---:|---:|
| D1 common translation | 1.00 | 0.99 | 0.24 | 9.30 | 1.45 | — |
| D2 coordinated maneuver | 1.00 | 0.99 | 0.25 | 9.23 | 1.45 | — |
| D3 independent motion | 0.92 | 0.87 | 0.66 | 25.30 | 3.62 | — |
| D4 apparent block-stable geometry | 0.99 | 0.96 | 0.32 | 10.83 | 1.72 | — |
| D5 organized expansion/contraction | 1.00 | 0.99 | 0.25 | 10.36 | 1.45 | — |
| D6 perturbation/recovery | 0.92 | 0.86 | 1.81 | 60.07 | 8.95 | 23.8 s |

These are exploratory diagnostics only and do not establish organization
detection performance.

## Why automatic continuation stopped

The frozen protocol requires review after exploratory execution and before any
benchmark, classifier, confirmatory, or held-out extension. The D4 control and
the D6 recovery/reformation calculation require methodological review before
any interpretation or protocol revision. No GO, PARTIAL GO, NO-GO, or
INCONCLUSIVE decision is made.

## Options

1. Accept the registered dynamic measurements and authorize a separately
   specified extension.
2. Review or revise the dynamic normalization, D4 control, or D6 recovery
   operator in a new protocol version.
3. Preserve DYNAMIC-001 as a technical exploratory record without extension.

## Recommended conservative action

Review raw dynamic states and the spatial-vs-motion separation, with special
attention to D4 and D6. Freeze any approved measurement changes before any
further execution.
