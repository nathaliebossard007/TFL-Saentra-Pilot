# REVIEW_REQUIRED — DYNAMIC-001 v1.1 Exploratory Operator Revision

## What happened

The v1.1 operator-only revision was applied to the unchanged v1.0 exploratory
D1–D6 track data for seeds 101–120. It produced 120 revised raw dynamic-state
files. Evaluator metadata was loaded only after those raw states were written.
No simulator change, classifier, benchmark, confirmatory, or held-out run was
performed.

## Descriptive diagnostics

Values below are means over samples and per-pair summaries for the 15-second
operator window unless noted otherwise.

| Scenario | Lag 1 persistence | Lag 15 persistence | Mean pair lifetime (s) | Reference distance | 30 s window distance | Recovery |
|---|---:|---:|---:|---:|---:|---:|
| D1 common translation | 1.00 | 0.99 | 3.54 | 0.13 | 0.16 | — |
| D2 coordinated maneuver | 1.00 | 0.99 | 3.46 | 0.15 | 0.16 | — |
| D3 independent motion | 0.77 | 0.51 | 0.92 | 0.27 | 0.35 | — |
| D4 apparent block-stable geometry | 0.98 | 0.94 | 7.46 | 0.17 | 0.21 | — |
| D5 organized expansion/contraction | 1.00 | 0.99 | 3.49 | 0.14 | 0.16 | — |
| D6 perturbation/recovery | 0.81 | 0.70 | 2.79 | 0.50 | 1.01 | 8.2 s |

These are exploratory diagnostics, not evidence of organization-detection
performance and not a scientific GO/NO-GO decision.

## Why automatic continuation stopped

The protocol requires a review stop before any benchmark, classifier, or
confirmatory extension. D4 remains the registered hard control, and the revised
operator behavior and D6 reformation calculation require methodological review
before interpretation. No protocol or simulator tuning is performed here.

## Options

1. Accept the revised operators and authorize a separately specified extension.
2. Review or revise the v1.1 operator definitions in a new protocol version.
3. Preserve v1.1 as a technical exploratory record without extension.

## Recommended conservative action

Review per-pair lifetimes, D4 behavior, and D6 recovery/reformation against the
raw v1.1 states. Freeze any approved change before further execution.
