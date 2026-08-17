# Decisions

## 2026-08-17 — Repository initialization

- Created the TFL-Saentra-Pilot repository as the authoritative project-memory workspace.
- No 001B implementation, result, hash, output, or test claim is recorded here.
- TFL-UAS-001A remains a frozen predecessor and will be imported separately.

## 2026-08-17 — Import and freeze TFL-UAS-001A

- Imported the predecessor from `TFL-UAS/TFL-UAS-001A_frozen_v0.1.0.zip` without modifying scientific contents.
- Archive integrity is VERIFIED: SHA-256 `00e61bd2aedaff30fa9c19422cdd38fa19bd0e86ca3fcc437607813206a1c9be`, 428050 bytes.
- The raw configuration hash is VERIFIED as `08773ac135820dbffb2948163dd25d36bd0a581a60d0ab838efe0597f98b4797`.
- The imported predecessor is frozen and protected by a SHA-256 manifest and pilot check.
- Track Association remains NO-GO. No TFL-UAS-001B implementation has started.

## 2026-08-17 — TFL-UAS-001B protocol frozen before implementation

- Frozen the v1.0 protocol and companion configuration for relational organization discrimination.
- Locked four-object established-track input, apparent-group and coordinated-group classes, exploratory/confirmatory/held-out seed ranges, three primary models, required ablations, leakage gates, metrics, and separate GO statuses.
- Recorded protocol SHA-256 `73fb85b80f8fde41b285f8208e894b0846d2832e60fd0bd1413fddc1e2041f73`.
- Recorded configuration SHA-256 `6dc01ba9c0d06dfb6bf26d5a00bf276193d084afd679f84ffeb1283e5d8af14a`.
- No TFL-UAS-001B implementation or result was created.

## 2026-08-17 — TFL-UAS-001B exploratory phase completed

- Executed exploratory seeds 101–120 only: 40 opaque samples, balanced 20 apparent-group and 20 coordinated-group samples.
- Implemented separated simulator, label-free prediction path, evaluator-after-prediction path, Models A/B/C, six required ablations, diagnostics, and leakage tests.
- Determinism and schema/leakage checks passed; 001A manifest and 001B protocol hash checks passed.
- The anti-trivial-separation gate failed: seven of eight one-variable audits reached balanced accuracy 1.0. Exploratory A/B/C metrics are therefore not interpreted as organization evidence.
- Confirmatory seeds 201–220 and held-out seeds 301–320 were not executed. No GO/NO-GO conclusion was changed.
- Next action is review of the exploratory freeze proposal and simulator/modeling concerns before any confirmatory authorization.

## 2026-08-17 — Automatic continuation stopped at review gate

- Created `REVIEW_REQUIRED.md` because the exploratory anti-trivial-separation validation failed.
- Preserved all exploratory outputs as technical diagnostics only; no GO, PARTIAL GO, NO-GO, or INCONCLUSIVE conclusion was made for 001B.
- Confirmatory seeds 201–220 and held-out seeds 301–320 remain unauthorized.
- The frozen v1.0 protocol and hashes were not changed.

## 2026-08-17 — TFL-UAS-001B v1.1 exploratory redesign authorized

- Scientific review accepts that a new protocol version is justified because v1.0 failed the anti-trivial-separation gate and the intended supervised baseline was not implemented as a fitted logistic-regression model.
- The v1.0 protocol, hashes, source and exploratory outputs remain preserved as a failed-validation record and must not be overwritten or reinterpreted.
- v1.1 must redesign the simulator so positive and negative classes substantially overlap in simple macroscopic marginals; the intended class signal should reside primarily in persistent temporal relational dependence rather than global speed, altitude, heading, scale, duration, or operating region.
- v1.1 must define a proper supervised training boundary for Model A while keeping test/confirmatory ground truth evaluator-only until predictions are written.
- Only exploratory v1.1 work is authorized. Confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited until a subsequent explicit review authorizes them.
- A repeated anti-trivial-separation failure must trigger another review gate rather than further automatic tuning.

## 2026-08-17 — TFL-UAS-001B v1.1 exploratory gate failed

- v1.1 was frozen with new hashes and versioned artifacts; v1.0 remained unchanged.
- The supervised train/test boundary was implemented and test truth was loaded only after prediction serialization.
- Validation failed because `mean_pairwise_distance` and `group_extent` each reached one-variable balanced accuracy 1.0.
- No A/B/C performance interpretation or scientific decision was made. Confirmatory 201–220 and held-out 301–320 remain prohibited.
- Conservative action: stop at `REVIEW_REQUIRED_v1.1.json` for human review; do not continue automatic simulator tuning.

## 2026-08-17 — Open TFL-UAS-SPATIAL-001 exploratory branch

- Scientific review concludes that repeated 001B anti-triviality failures indicate a likely perspective problem with group-label classification, not a justification for indefinite simulator tuning.
- Preserve TFL-UAS-001B v1.0/v1.1 unchanged as failed-validation records of the classification path. Do not reinterpret them as evidence for or against relational-state persistence.
- Open a separate exploratory experiment: `TFL-UAS-SPATIAL-001 — Spatial Relational State Persistence`.
- Primary question: can persistent relational spatial organization be detected independently of absolute position, orientation, scale, and predefined group labels?
- Primary observable shifts from class prediction to unlabeled relational-state construction and persistence under transformations.
- The first test must distinguish organization-preserving translation/rotation from independent motion, apparent spatial organization, and perturbation/recovery controls.
- Maintain separate rigid-relational and scale-normalized shape states where useful so physical expansion/contraction is not accidentally erased.
- No classifier is required in the primary SPATIAL-001 test. Graph/Laplacian quantities remain candidate deterministic diagnostics and must earn any role empirically.
- SPATIAL-001 protocol v1.0 must be frozen before implementation. Exploratory execution must stop at review before any benchmark/classification/confirmatory extension.
- 001B confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited.

## 2026-08-17 — TFL-UAS-SPATIAL-001 protocol v1.0 frozen

- Frozen a separate spatial relational-state persistence protocol before implementation.
- Protocol SHA-256: `b3cbf5e30981c13b670010563dee6004f7262f3d6190da6a73f492d9cff219fe`.
- Configuration SHA-256: `88f47cce9a2b4089813320092e437956a2ea3d2c45f08c8e260b3262b08b9ac6`.
- Registered S1–S5 scenarios, rigid and shape states, local/global relational layers, graph/Laplacian diagnostics, persistence measures, and recovery measurements.
- No implementation or exploratory execution occurred in the freeze task. The next task is implementation exactly as frozen.
