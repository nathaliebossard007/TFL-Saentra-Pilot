# TFL-UAS-001A — Exploratory Result

## Question
Does the relational representation provide measurable information beyond the conventional baseline in the minimal crossing-track problem?

## Frozen run
20 deterministic seeds (101–120), two crossing objects, 20 fixed sensor nodes, noisy bearing/elevation/range reconstruction, missed observations, sparse false detections, and a forced temporary observation loss for object 1 from t=54 s through t=62 s.

## Mean results
| Metric | KF + gated NN | RIC graph v0 |
|---|---:|---:|
| Track purity | 0.997 | 0.943 |
| Identity switches | 1.40 | 0.60 |
| Fragmentation | 0.95 | 2.75 |
| False merge rate | 0.317 | 0.155 |
| Track precision | 0.995 | 0.890 |
| Track recall | 0.993 | 0.483 |
| False track rate | 0.050 | 0.000 |
| Mean inferred track count | 2.30 | 4.15 |
| Recovery after forced occlusion | 1.05 s (20/20 seeds) | no same-track recovery (0/20 seeds) |

## Interpretation
The relational representation contains a narrow measurable association signal: it produced fewer identity switches and fewer merged tracks than the conventional baseline. However, this did not translate into a better tracker. The current RIC graph/path extraction fragmented trajectories heavily, recovered less than half of each ground-truth trajectory in its best corresponding track, and failed to bridge the forced observation gap in every seed.

Therefore the present result must not be presented as a TFL tracking advantage. The conventional baseline is decisively better for overall track reconstruction in this minimal test.

The normalized-Laplacian quantities were recorded as diagnostics only. They were not used for association and therefore cannot be credited for the reduced switch/merge counts. No claim of predictive spectral value is supported by 001A.

## Falsification result
**Track association candidate v0: NO-GO.**

This is a NO-GO for using the present TFL/RIC graph as a replacement for ordinary point tracking. It is not evidence that relational organization has no value at a higher level.

## Scientifically justified next step
Do not add complexity to rescue the 001A tracker. Preserve this frozen negative result. The next test should move to the hypothesis that motivated TFL more directly: **relation → organization → state dynamics**.

Recommended next experiment: a minimal organization discrimination test with two already-established track sets:
- hard negative: nearby independent objects with temporarily aligned heading,
- positive: deliberately coordinated objects with persistent relative geometry and synchronized maneuvers.

Use identical per-track kinematics for the baseline inputs where possible, then test whether relational temporal structure adds out-of-seed information. This cleanly separates organization detection from the failed point-to-track replacement hypothesis.
