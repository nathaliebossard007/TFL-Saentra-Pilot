# Current Task

## REVIEW_REQUIRED — DYNAMIC-001 v1.2 exploratory run

Review `experiments/TFL-UAS-DYNAMIC-001/v1.2/REVIEW_REQUIRED.md` and the
versioned diagnostics before any further work. Do not execute extensions,
benchmarks, classifiers, confirmatory seeds, held-out seeds, or make a
scientific decision without explicit review authorization.

The authorized implementation/run is complete: 120 unchanged exploratory
samples from seeds 101–120 were processed under the frozen v1.2 protocol.

The prior implementation task follows for provenance:

Implement **TFL-UAS-DYNAMIC-001 v1.2 exploratory spatiotemporal relational Laplacian exactly as frozen**, using unchanged exploratory data only, then stop at `REVIEW_REQUIRED`.

The v1.2 protocol-freeze task is complete. Do not modify v1.0, v1.1, or v1.2
frozen protocol/config files, do not tune D1–D6, and do not execute
confirmatory or held-out seeds.

Frozen v1.2 files:

- `experiments/TFL-UAS-DYNAMIC-001/v1.2/TFL-UAS-DYNAMIC-001_PROTOCOL_v1.2.md`
- `experiments/TFL-UAS-DYNAMIC-001/v1.2/config/tfl_uas_dynamic_001_protocol_v1.2.json`
- `experiments/TFL-UAS-DYNAMIC-001/v1.2/PROTOCOL_FREEZE.md`

The prior protocol-freeze task description follows for provenance:

Prepare and freeze **TFL-UAS-DYNAMIC-001 v1.2 — Spatiotemporal Relational Laplacian** before implementation.

Preserve DYNAMIC-001 v1.0 and v1.1 unchanged as frozen exploratory records. Do not modify their protocols, configs, implementations, raw states, diagnostics, or review files.

## Scientific reason for v1.2

The v1.1 operator revision improved independent-motion and perturbation sensitivity, but D4 apparent/block-stable geometry remained highly persistent. Review indicates this may not be a defect of pairwise motion correlation alone: D4 can contain locally stable relational dynamics while lacking persistence of the **time-integrated relative spatial structure actually occupied by the objects**.

The next hypothesis is therefore operator-level and explicitly Laplacian:

`space -> spatial relations -> motion relations -> relative spatial occupancy over time -> spatiotemporal relational operator -> organization`

Primary research question:

**Does a time-integrated Laplacian of relative spatial occupancy preserve organized motion states while rejecting merely block-stable apparent organization?**

Here "relative spatial structure" means object-relative / transformation-aware spatial structure, not a claim about physical spacetime relativity.

## Scope

This is an operator revision only.

- Reuse the unchanged D1–D6 exploratory track data from DYNAMIC-001 v1.0.
- Do not tune or regenerate the simulator.
- Do not add new scenarios or labels.
- Do not add a classifier, benchmark, learned edge weights, neural model, confirmatory seeds, or held-out seeds.
- Raw v1.2 operator outputs must be serialized before evaluator metadata is loaded.

## Required v1.2 operator layers

Freeze explicit deterministic definitions for at least:

1. **Instantaneous relational graph** `G_t=(V,W_t)` using registered functions of pair distance, normalized distance, distance derivative, relative velocity, and velocity-direction coherence.
2. **Relative spatial occupancy state** over each registered temporal window. Use centroid-relative / pair-relative trajectories so absolute translation is removed by construction; define rotation and scale treatment explicitly rather than implicitly.
3. **Time-integrated occupancy weights** `W_occ(t,W)` that summarize persistence of same-object relative spatial occupancy across the full window rather than adjacent-frame quietness.
4. **Normalized occupancy Laplacian** `L_occ = I - D^(-1/2) W_occ D^(-1/2)` with registered zero-degree handling.
5. Parallel **rigid**, **shape-normalized**, **motion**, and **occupancy** operators where needed so expansion/contraction is not erased unintentionally.
6. Spectral diagnostics: ordered eigenvalues, spectral gap, spectrum distance across windows, and explicitly stable eigenspace/projector distances that avoid raw-eigenvector sign ambiguity and handle repeated/near-repeated eigenvalues conservatively.
7. Window-to-window operator distance and reference-operator distance relative to a frozen pre-event baseline.
8. D6 disturbance/recovery measurement in operator space.

## D4 requirement

Do not alter D4 to force a lower score. D4 remains the hard control exactly because its local geometry is block-stable.

The v1.2 protocol must test whether:

- adjacent-frame or short-block similarity can remain high,
- while the integrated relative occupancy operator changes across longer windows.

Any apparent D4 separation must arise from the frozen operator definition, not simulator tuning.

## D1/D2/D5 invariance requirements

The protocol must separately state expected behavior for:

- D1 common translation: relative occupancy/operator approximately invariant to absolute translation;
- D2 coordinated rotation/maneuver: rigid/rotation-aware operator should preserve organization under common rotation according to the frozen alignment/invariant rule;
- D5 organized expansion/contraction: rigid spatial operator may change while shape/motion/occupancy organization can remain coherent.

Do not collapse these layers into one score before exploratory review.

## Protocol-freeze task only

For this task:

1. Create versioned `experiments/TFL-UAS-DYNAMIC-001/v1.2/` artifacts.
2. Create `TFL-UAS-DYNAMIC-001_PROTOCOL_v1.2.md` and companion config.
3. Freeze all windows, graph-weight formulas, normalization constants, occupancy definitions, Laplacian construction, spectral/projector distance rules, baselines, tolerances, and D6 recovery rules before implementation.
4. Create `PROTOCOL_FREEZE.md` with SHA-256 hashes and provenance to v1.0/v1.1.
5. Update repository guards, STATUS.md, docs/decisions.md, and tasks/backlog.md.
6. Do **not** implement or execute v1.2 in the same freeze task.

After freeze, set the next task to:

**Implement TFL-UAS-DYNAMIC-001 v1.2 exploratory spatiotemporal relational Laplacian exactly as frozen, using unchanged exploratory data only, then stop at REVIEW_REQUIRED.**

## Scientific gates

- Negative results are valid.
- No post-hoc tuning to make D4 separate.
- No silent change to D1–D6 data or simulator.
- No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision during protocol freeze.
- Stop at REVIEW_REQUIRED after later exploratory execution before any benchmark/classification/confirmatory extension.
- TFL-UAS-001B confirmatory seeds 201–220 and held-out seeds 301–320 remain prohibited.
